import importlib.util
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
GUI_MAIN = REPO_ROOT / "ndlocr-lite-gui" / "main.py"


def load_module(module_name: str, relative_path: str):
    module_path = REPO_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


localelabel = load_module("localelabel", "src/uicomponent/localelabel.py")

SUPPORTED_LANGCODES = ("ja", "en", "zh")


class LocalizationTest(unittest.TestCase):
    def test_every_entry_covers_all_supported_languages(self):
        for key, entry in localelabel.TRANSLATIONS.items():
            for langcode in SUPPORTED_LANGCODES:
                self.assertIn(langcode, entry, f"{key} has no {langcode} translation")
                self.assertTrue(entry[langcode].strip(), f"{key}/{langcode} is empty")

    def test_chinese_text_is_actually_translated(self):
        for key, entry in localelabel.TRANSLATIONS.items():
            if key.startswith("language_name"):
                continue
            self.assertNotEqual(
                entry["zh"], entry["ja"], f"{key} zh translation is a copy of the Japanese text"
            )

    def test_get_text_formats_and_falls_back(self):
        self.assertEqual(
            localelabel.get_text("main_models_ready", "zh", elapsed=1.5),
            "OCR 模型加载完成（1.5 秒）",
        )
        # 未知语言回退到 en
        self.assertEqual(
            localelabel.get_text("main_process_complete", "fr"),
            localelabel.TRANSLATIONS["main_process_complete"]["en"],
        )
        # 未知键回退为键名
        self.assertEqual(localelabel.get_text("no_such_key", "zh"), "no_such_key")

    def test_gui_only_uses_defined_translation_keys(self):
        source = GUI_MAIN.read_text(encoding="utf-8")
        used = set(re.findall(r"tr\(\s*['\"]([a-z0-9_]+)['\"]", source))
        used |= set(re.findall(r"'main_models_ready[a-z_]*'", source))
        used = {key.strip("'") for key in used}
        missing = sorted(key for key in used if key not in localelabel.TRANSLATIONS)
        self.assertEqual(missing, [])

    def test_translate_literal_replaces_known_source_text(self):
        self.assertEqual(localelabel.translate_literal("\u8a2d\u5b9a", "zh"), "\u8bbe\u7f6e")
        # 未知原文原样返回，不误伤
        self.assertEqual(localelabel.translate_literal("LLM feature", "zh"), "LLM feature")

    def test_register_translations_merges_feature_entries(self):
        localelabel.register_translations(
            {"llm_fix_btn": {"ja": "LLM\u88dc\u6b63", "en": "LLM Correct", "zh": "LLM \u6821\u6b63"}}
        )
        try:
            self.assertEqual(localelabel.get_text("llm_fix_btn", "zh"), "LLM \u6821\u6b63")
            # 注册后原文替换也能命中
            self.assertEqual(localelabel.translate_literal("LLM\u88dc\u6b63", "zh"), "LLM \u6821\u6b63")
            # 内置条目不会被覆盖掉缺失语言
            localelabel.register_translations({"main_process_complete": {"zh": "\u5904\u7406\u5b8c\u6210"}})
            self.assertEqual(localelabel.get_text("main_process_complete", "en"), "Processing complete")
        finally:
            localelabel.TRANSLATIONS.pop("llm_fix_btn", None)

    def test_localize_tree_rewrites_control_like_objects(self):
        class FakeControl:
            def __init__(self, **kwargs):
                self.__dict__.update(kwargs)

        child = FakeControl(label="JSON\u5f62\u5f0f", value=True)
        button = FakeControl(content="\u30ad\u30e3\u30f3\u30bb\u30eb")
        root = FakeControl(
            title="\u8a2d\u5b9a",
            controls=[child, button, FakeControl(text="%s" % "\u672a\u77e5\u6587\u6848")],
        )
        collected = set()
        localelabel.localize_tree(root, "zh", collected)
        self.assertEqual(root.title, "\u8bbe\u7f6e")
        self.assertEqual(child.label, "JSON \u683c\u5f0f")
        self.assertEqual(button.content, "\u53d6\u6d88")
        self.assertIn("\u672a\u77e5\u6587\u6848", collected)

    def test_gui_has_three_language_segments(self):
        source = GUI_MAIN.read_text(encoding="utf-8")
        self.assertIn("UI_LANGCODES = ('ja', 'en', 'zh')", source)


if __name__ == "__main__":
    unittest.main()

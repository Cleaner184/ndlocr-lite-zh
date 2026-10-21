# NDLOCR-Lite 简体中文版（Windows 便携版）

> 基于 [ndl-lab/ndlocr-lite](https://github.com/ndl-lab/ndlocr-lite) 的二次分发与中文化改造。
> 原项目版权归 国立国会図書館（National Diet Library）所有，遵循仓库内 `LICENCE`。

## 这个仓库是什么

1. **界面中文适配**：把 GUI 的语言支持从「日本語 / English」扩展为 **日本語 / English / 简体中文** 三档，
   文案字典 51 条 × 3 语言，新增回退机制与可选功能模块接入 API。
2. **Windows 便携版**：`windows-build/NDLOCR-Lite-GUI/` 是官方 `flet build windows` 产物（v1.3.1）注入中文适配后的成品，
   **拷贝后双击 `ndlocr-lite-gui.exe` 即用**，无需安装 Python、无需联网（模型随包）。

## 下载（Windows）

- **Release 直下**：[v1.3.1-zh](https://github.com/Cleaner184/ndlocr-lite-zh/releases/tag/v1.3.1-zh)
  Windows → `ndlocr_lite_zh_windows.zip`（CI 编译）/ `NDLOCR-Lite-GUI-zh-v1.3.1-win-x64.zip`（本机编译已验证）；
  另有 Linux / macOS(arm/intel) 产物
- 或直接用仓库内的 `windows-build/NDLOCR-Lite-GUI/`（内容相同）

## 快速开始（Windows）

```
windows-build/NDLOCR-Lite-GUI/ndlocr-lite-gui.exe      ← 双击运行（默认简体中文）
```

- 右上角分段按钮切换 日本語 / English / 简体中文，选择保存在 `%APPDATA%\National_Diet_Library\ndlocr-lite-gui\data\userconf.yaml`
- 首次启动如遇 SmartScreen 提示，点「更多信息 → 仍要运行」
- 详细说明见 `windows-build/NDLOCR-Lite-GUI/使用说明.txt`

## 从源码运行 / 自己打包

```powershell
cd ndlocr-lite
py -m venv ocrenv
.\ocrenv\Scripts\Activate.ps1
pip install -r requirements.txt
python ndlocr-lite-gui\main.py
```

- GitHub 下载受限时，可先手动下载 `flet-windows.zip`（约 40MB）并设置 `FLET_CLIENT_URL`，详见 `ndlocr-lite-gui/README.md` 附录。
- 中文适配的完整改动清单、验收记录、打包踩坑：见 **`中文适配说明.md`**。

## 目录

| 路径 | 说明 |
| --- | --- |
| `src/` `ndlocr-lite-gui/` | 上游源码（已套用中文适配） |
| `src/uicomponent/localelabel.py` | 文案字典（ja/en/zh）+ `get_text` / `register_translations` / `localize_tree` |
| `ndlocr-lite-gui/main.py` | 3 档语言切换、文案查表、可选模块兜底本地化 |
| `ndlocr-lite-gui/tests/test_localization.py` | 8 项本地化单测（不依赖 flet） |
| `windows-build/` | Windows 便携版成品 + 原始文件备份 |
| `验收截图/` | 开发版与打包版的界面实机截图 |
| `中文适配说明.md` | 改动清单、验收记录、打包与上传说明 |
| `*.patch` | 相对上游 HEAD 的补丁（可用 `git apply` 复现） |

## 许可

沿用上游 `LICENCE`（国立国会図書館）与 `LICENCE_DEPENDENCEIES`；本仓库仅做界面中文化与打包，未修改 OCR 算法。

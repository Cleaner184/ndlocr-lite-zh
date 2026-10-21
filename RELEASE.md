# 发行说明（Release）

本仓库的发行版通过 **GitHub Release** 分发，产物由 `.github/workflows/build-release.yml` 编译。
该工作流借鉴上游 `ndl-lab/ndlocr-lite` 的 `build-flet-cross.yml`（原件见 `docs/upstream-build-flet-cross.yml`）。

## 已有发行版

| Tag | 平台 | 产物 | 大小 | 说明 |
| --- | --- | --- | --- | --- |
| `v1.3.1-zh` | Windows x64 | `ndlocr_lite_zh_windows.zip` | 249.6MB | CI 编译（工作流产出，推荐） |
| `v1.3.1-zh` | Windows x64 | `NDLOCR-Lite-GUI-zh-v1.3.1-win-x64.zip` | 247MB | 本机编译，已实机验证（默认中文/切换/模型加载 13.2s） |
| `v1.3.1-zh` | Linux x64 | `ndlocr_lite_zh_linux.tar.gz` | 265.3MB | CI 编译 |
| `v1.3.1-zh` | macOS Apple Silicon | `ndlocr_lite_zh_macos_apple_silicon.tar.gz` | 303MB | CI 编译 |
| `v1.3.1-zh` | macOS Intel | `ndlocr_lite_zh_macos_intel.tar.gz` | 282.5MB | CI 编译 |

Release 页面：https://github.com/Cleaner184/ndlocr-lite-zh/releases/tag/v1.3.1-zh

> CI 运行记录：
> - 第 1 次：Linux / macOS(arm) 失败于 `jni` 版本冲突（模板覆盖 jni=1.0.0，而 jni_flutter 要求 ^1.1.0）；
> - 修复：`ndlocr-lite-gui/pyproject.toml` 增加 `jni="^1.1.0"` 覆盖；
> - 第 2 次：4 平台构建全部成功，仅 publish 步骤因缺 checkout 失败；
> - 第 3 次（最终）：**prepare-release / linux / macOS(arm) / macOS(intel) / windows / publish 全部 success**
>   → https://github.com/Cleaner184/ndlocr-lite-zh/actions/runs/39608354493

Windows 包解压后双击 `NDLOCR-Lite-GUI\ndlocr-lite-gui.exe` 即用（默认简体中文，无需 Python、无需联网）。

## 发一个新版本

```bash
git tag v1.3.2-zh
git push origin v1.3.2-zh        # 触发 build-release 工作流
```

工作流会：
1. 建/复用同名 Release（先 draft）；
2. 在 ubuntu / macos / macos-intel / windows 上分别 `flet build`（Flutter 3.44.8 + flet 0.86.5）；
3. 跑本地化单测；
4. 把 `ndlocr_lite_zh_{linux,macos_apple_silicon,macos_intel,windows}` 上传到该 Release；
5. 全部成功后把 Release 从 draft 转为正式发布。

也可以手动触发：Actions → build-release → Run workflow，填入已有 tag。

## 本地手工编译（Windows，已验证）

```powershell
cd ndlocr-lite
py -m venv ocrenv; .\ocrenv\Scripts\Activate.ps1
pip install -r requirements.txt
cd ndlocr-lite-gui
xcopy ..\src .\src /E /I /Y
python src\set_version.py 1.3.1
flet build windows --output ..\dist --build-version 1.3.1
```

注意事项（踩过的坑）：
- `requirements.txt` 里 `flet==0.86.5` 要求 **Flutter 3.44.8**；
- `pyproject.toml` 已覆盖 `jni=^1.1.0`，否则 `jni_flutter` 生成代码会报 `Constant evaluation error`；
- `flet build` 首次需要从 GitHub Releases 拉 Flutter / 构建模板 / python-build-standalone / `python-windows-for-dart` / dart-bridge；国内网络可先手动下载并设置 `FLET_CLIENT_URL` 等缓存（详见 `中文适配说明.md` 第 7 章）；
- 构建路径**不要含非 ASCII 字符**（如中文用户名），否则 Flutter/MSBuild 会读不到 `app.dill`。

## 上传产物到已有 Release（本机网络受限时的做法）

本仓库首次发 `v1.3.1-zh` 时，`uploads.github.com` 经本地代理会 502，重试 + `--http1.1` 后 247MB 单文件可成功；
若仍失败可拆成 <100MB 分卷后逐个上传。

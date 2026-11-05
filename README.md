# 电子中阮 · Electronic Zhongruan

用 Web Audio 实时合成的**电子中阮**：一台可以在浏览器、Android 手机和 Windows 桌面上演奏的虚拟中阮。

木质琴身、四根弦、简谱按键；按下键盘 1–7 即可发声，按住 Ctrl / Shift 切换低八度 / 高八度，支持和弦。

> 整个乐器没有任何音频采样文件，所有音色都由 Web Audio API 实时计算（Karplus-Strong 拨弦模型 + 卷积混响），因此一份 44 KB 的 HTML 就是完整的乐器。

---

## 功能

| 功能 | 说明 |
| --- | --- |
| 🎹 键盘演奏 | 数字键 1–7 对应 do–ti，Ctrl / Shift 升降八度，同时按多个键即和弦，也支持鼠标 / 触屏点击 |
| 🎼 简谱自动播放 | 支持 `1-7` 音符、`1'` 高八度、`1,` 低八度、`-` 延长、`[135]` 和弦、`0` 休止 |
| 📏 节拍器 | 可调速度的节拍器，带节拍闪烁 |
| 🎤 录音回放 | 录制演奏、回放、清除（MediaRecorder） |
| 💾 导出音频 | 将演奏导出为音频文件 |
| 🎨 国风界面 | 楷体、宣纸配色、木质琴身与弦振动动画 |

## 目录结构

```
zhongruan/
├── apk/
│   └── 电子中阮-release.apk      # 已签名的发布版 APK（v1.0，targetSdk 34，minSdk 24）
├── android/                      # Android 工程（WebView 壳）
│   ├── app/src/main/
│   │   ├── assets/zhongruan.html     # 乐器本体（较新的版本）
│   │   ├── java/com/zhongruan/app/MainActivity.java
│   │   └── res/…
│   ├── build.gradle
│   └── settings.gradle
└── desktop/                      # Windows 桌面端（Electron 壳）
    ├── main.js
    ├── package.json
    ├── zhongruan.html
    └── icon.ico
```

`android/app/src/main/assets/zhongruan.html` 与 `desktop/zhongruan.html` 是同一份实现的两个快照，后者较早。

## 构建

### Android

```bash
cd android
./gradlew assembleDebug      # 产物：app/build/outputs/apk/debug/app-debug.apk
./gradlew assembleRelease    # 需自备签名配置，见下
```

需要 JDK 17+、Android SDK Platform 34。

### Windows 桌面端

```bash
cd desktop
npm install
npm start                    # 直接运行
npm run dist                 # 打包 exe（electron-builder，NSIS + portable）
```

## 关于签名

仓库**不包含**签名密钥（`zhongruan.jks`）与密码（`keystore.properties`）。
若要构建签名版 APK，在 `android/` 下按 `keystore.properties.example` 建一份 `keystore.properties`：

```properties
storeFile=your.jks
storePassword=******
keyAlias=your_alias
keyPassword=******
```

缺少该文件时 `assembleRelease` 会产出未签名 APK。

## 技术栈

- 纯 HTML + CSS + JavaScript，无前端框架、无音频素材
- Web Audio API：Karplus-Strong 拨弦合成、`ConvolverNode` 混响、滤波
- Android：`WebView` 加载 `assets` 本地页面，运行时申请录音权限
- Windows：Electron 33（`contextIsolation` 开启、`nodeIntegration` 关闭）

## 授权 / License

本项目采用**双许可**：你可以任选下列许可之一来使用、修改和分发本项目。

| 许可 | 全文 | 特点 |
| --- | --- | --- |
| Apache License 2.0 | [LICENSE-APACHE-2.0](LICENSE-APACHE-2.0) | 宽松许可，含明确的专利授权，商业使用友好 |
| GNU GPL v3.0 或更高版本 | [LICENSE-GPL-3.0](LICENSE-GPL-3.0) | 强 copyleft，衍生作品需以同样许可开源 |

SPDX 标识：`Apache-2.0 OR GPL-3.0-or-later`

源文件头部已标注 `SPDX-License-Identifier`。选择 GPL-3.0 时，也可按 GPLv3 的条款与 Apache-2.0 代码组合使用。

Copyright © 2026 Zhongruan

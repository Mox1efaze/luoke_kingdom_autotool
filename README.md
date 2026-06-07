# 基于dd模型的洛克王国世界丢球助手-仅是用于大量出没，无需显卡要求

***

基于图像识别的洛手自动化丢球工具

仿照原作者<https://github.com/Makapic/RocoPilot>

因为interception驱动不好安装，这里给出dd驱动的解决方案,其他方案可以直接参考原作者


## 运行环境

> 以下为实测可用的环境配置。其他相近版本（如 Windows 10、Python 3.11、CUDA 11.8）通常也能正常运行。


### 1. 安装dd 驱动

dd 是内核级输入驱动，游戏无法感知模拟输入，**必须先装**。

1. 访问 [ddxoft/master](https://github.com/ddxoft/master)
2. 下载 `2026.DD.EV.HVCI.63xxx.7z` 并解压到任意目录

   具体安装流程可参照ai,注意需要开启签名模式+内存完整性关闭，才能打上驱动

   <br />

2\. 安装 uv（Python 包管理器）

uv 会自动下载和管理 Python，**无需手动安装 Python**。

以**普通用户身份**打开终端：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

安装完成后**关闭并重新打开终端**，验证：

```powershell
uv --version
```

### 3. 克隆项目并安装依赖

```powershell
# 克隆到本地
git clone https://github.com/Mox1efaze/luoke_kingdom_autotool.git
cd RocoPilot
```

```powershell
# 安装基础依赖（约 500 MB）
uv sync
```

> uv 会自动创建 `.venv` 虚拟环境并安装所有依赖。基础依赖包括 OpenCV、numpy、mss（截图）、pywin32、interception-python。

###

### 6. 启动验证

```powershell
uv run main.py
```

看到模式选择菜单即环境配置成功。按 `Ctrl+C` 退出。

\--。

***

## 运行模式

启动后提供三种模式可选：

| 按键  | 模式   | 说明                |
| --- | ---- | ----------------- |
| `1` | 自动丢球 | 非战斗状态下检测可丢球画面自动点击 |

> **暂停/继续**：运行时按 `F8` 暂停引擎循环（三种模式均适用），再按 `F8` 恢复。可在 `config.py` 的 `pause_hotkey` 中自定义按键（`keyboard` 库格式，如 `f8`、`pause`、`ctrl+shift+p`）。

### 模式 1：自动丢球

- 仅在游戏窗口前台时触发，避免误操作
- 检测 `elf_P` / `exchange` 模板匹配分数，达到阈值才点击
- 适合大量精灵出没时挂机丢球

注意事项

- **分辨率**：推荐 1920×1080。脚本支持自适应缩放，阈值已下调至 0.4 以兼容其他分辨率。
- **自定义适配**：若分辨率特殊导致识别异常，可在当前分辨率下重新截图覆盖 `templates/` 中的同名文件。
- **窗口状态**：游戏窗口**不能最小化**（可被遮挡但不能最小化）。
- **前台要求**：键盘输入需游戏窗口在前台；鼠标点击需目标位置未被遮挡。
- **巡航模式**：模式 3 启动时会弹出独立悬浮窗，需框选小地图区域完成初始化。**首次运行需生成 SIFT 地图锚点缓存（约 2-3 分钟，取决于 CPU 性能），后续启动秒加载。**

***

## 项目结构

```
├── main.py              # 入口，模式选择和窗口选择
├── config.py            # 全局配置（阈值、ROI、模板名等）
├── core/                # 核心引擎
│   ├── engine.py        # 主循环，战斗状态机
│   ├── capture.py       # 游戏窗口截图
│   ├── vision.py        # OpenCV 模板匹配
│   ├── input.py         # Interception 键鼠模拟
│   ├── window.py        # 窗口查找和枚举
│   ├── pet_detector.py  # YOLO 精灵检测
│   └── ...
├── modes/               # 运行模式（策略模式）
│   ├── base.py          # 抽象基类
│   ├── ball.py          # 模式 1：自动丢球
│   ├── ball_pet.py      # 模式 2：精灵定位丢球
│   └── ball_cruise.py   # 模式 3：巡航 + 抓宠
├── cruise_capture/      # 巡航路径规划与状态机
├── luoke_location_src/  # SIFT 地图定位系统
├── scripts/             # 训练/标注/标定工具
├── templates/           # 模板匹配图片（按分辨率缩放）
├── models/              # YOLO 模型文件（.pt）
└── datasets/            # 训练数据集
```

***

## 免责声明

1. **仅供学习参考**：本工具仅用于计算机视觉（OpenCV 模板匹配、SIFT 特征跟踪、YOLO 目标检测）及输入模拟技术的研究与交流。
2. **驱动风险**：本工具使用 Interception 内核级驱动模拟键鼠输入，该驱动以管理员权限运行在系统内核层。请从 [Interception 官方仓库](https://github.com/oblitum/Interception) 下载，使用非官方来源的驱动文件可能存在安全风险。
3. **账号风险**：使用自动化脚本可能违反《洛克王国：世界》用户协议，存在被警告、限制或永久封禁的风险。**由此产生的一切后果由使用者本人承担。**
4. **技术边界**：本工具不修改游戏内存、不篡改网络封包、不注入游戏进程。所有操作均基于截屏 → 图像分析 → 模拟外设输入的技术路径，与人类观察屏幕后操作键鼠的行为等价。
5. **无担保责任**：本软件按"现状"提供，不提供任何明示或暗示的担保。作者不对因使用或无法使用本工具造成的任何直接或间接损失（包括但不限于账号封禁、数据丢失、硬件损坏）承担责任。

***

## 致谢

本项目基于以下开源项目二次开发：

- [yorusacri/Auto-rocokingdom](https://github.com/yorusacri/Auto-rocokingdom) — 原始自动化框架，提供了模板匹配引擎和战斗状态机的核心思路
- [761696148/Game-Map-Tracker](https://github.com/761696148/Game-Map-Tracker) — SIFT 地图定位追踪方案，用于巡航模式的位置感知
- [oblitum/Interception](https://github.com/oblitum/Interception) — 内核级输入驱动


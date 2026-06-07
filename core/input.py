import random
import time

from ctypes import windll
import win32gui

# DD驱动路径（HID 模式，已安装驱动）
_DD_DLL_PATH = r"D:\game\luokekingdom\2026.DD.EV.HVCI.63xxx\2.hid\ddhid.63340.dll"

_dd_dll = None
_dd_ready = False


def _ensure_dd():
    """初始化 DD 驱动（方案一）。"""
    global _dd_dll, _dd_ready
    if _dd_ready:
        return True
    try:
        _dd_dll = windll.LoadLibrary(_DD_DLL_PATH)
        st = _dd_dll.DD_btn(0)  # DD 初始化
        if st == 1:
            _dd_ready = True
            return True
    except Exception:
        pass
    return False


# 兼容性别名（供已导入 _ensure_interception 的代码使用）
_ensure_interception = _ensure_dd


# DD 虚拟键码映射
_DD_KEY_CODES = {
    'a': 401, 'b': 505, 'c': 503, 'd': 403, 'e': 303,
    'f': 404, 'g': 405, 'h': 406, 'i': 308, 'j': 407,
    'k': 408, 'l': 409, 'm': 507, 'n': 506, 'o': 309,
    'p': 310, 'q': 301, 'r': 304, 's': 402, 't': 305,
    'u': 307, 'v': 504, 'w': 302, 'x': 502, 'y': 306,
    'z': 501,
    '0': 210, '1': 201, '2': 202, '3': 203, '4': 204,
    '5': 205, '6': 206, '7': 207, '8': 208, '9': 209,
    # 功能键
    'f1': 112, 'f2': 113, 'f3': 114, 'f4': 115,
    'f5': 116, 'f6': 117, 'f7': 118, 'f8': 119,
    'f9': 120, 'f10': 121, 'f11': 122, 'f12': 123,
    # 特殊键
    'space': 200, 'enter': 313, 'esc': 128, 'tab': 209,
    'shift': 500, 'ctrl': 503, 'alt': 505,
    'left': 300, 'right': 303, 'up': 302, 'down': 301,
}


def _get_dd_key_code(key: str):
    """获取 DD 键码。"""
    key_lower = key.lower()
    code = _DD_KEY_CODES.get(key_lower)
    if code is not None:
        return code
    # 尝试直接使用 ASCII 码
    try:
        return ord(key_lower)
    except Exception:
        return None


def release_movement() -> None:
    """释放移动键，确保截图时游戏 UI 不被巡航输入干扰。"""
    try:
        if not _ensure_dd():
            return
        for key in ('w', 'a', 's', 'd'):
            code = _DD_KEY_CODES.get(key.lower())
            if code:
                _dd_dll.DD_key(code, 2)  # 2 = key up
    except Exception:
        pass


def press_once(hwnd: int, key: str) -> None:
    """按下并释放一个键（驱动级）。"""
    if not key:
        return
    if not _ensure_dd():
        return
    code = _get_dd_key_code(key)
    if code is None:
        return
    try:
        _dd_dll.DD_key(code, 1)  # 1 = key down
        time.sleep(random.uniform(0.04, 0.10))
        _dd_dll.DD_key(code, 2)  # 2 = key up
    except Exception:
        pass


def click_at(hwnd: int, x: int | None = None, y: int | None = None) -> bool:
    """在窗口客户区坐标 (x, y) 处点击（驱动级）。不传坐标则在当前位置点击。"""
    try:
        if not _ensure_dd():
            return False
        if x is not None and y is not None:
            sx, sy = win32gui.ClientToScreen(hwnd, (x, y))
            _dd_dll.DD_mov(
                sx + random.randint(-2, 2),
                sy + random.randint(-2, 2),
            )
            time.sleep(random.uniform(0.02, 0.05))
            _dd_dll.DD_btn(1)  # left down
            time.sleep(random.uniform(0.05, 0.12))
            _dd_dll.DD_btn(2)  # left up
        else:
            _dd_dll.DD_btn(1)
            time.sleep(random.uniform(0.20, 0.40))
            _dd_dll.DD_btn(2)
        return True
    except Exception:
        return False


# ── DD 驱动级鼠标键盘控制（替代 interception 直接调用） ──────────────────────


def mouse_down(button: str = 'right') -> None:
    """按下鼠标按钮。button: 'left', 'right', 'middle'"""
    if not _ensure_dd():
        return
    try:
        if button == 'right':
            _dd_dll.DD_btn(4)  # right down
        elif button == 'middle':
            _dd_dll.DD_btn(16)  # middle down
        else:  # left
            _dd_dll.DD_btn(1)  # left down
    except Exception:
        pass


def mouse_up(button: str = 'right') -> None:
    """抬起鼠标按钮。button: 'left', 'right', 'middle'"""
    if not _ensure_dd():
        return
    try:
        if button == 'right':
            _dd_dll.DD_btn(8)  # right up
        elif button == 'middle':
            _dd_dll.DD_btn(32)  # middle up
        else:  # left
            _dd_dll.DD_btn(2)  # left up
    except Exception:
        pass


def move_relative(dx: int, dy: int) -> None:
    """相对移动鼠标（驱动级）。"""
    if not _ensure_dd():
        return
    try:
        _dd_dll.DD_movR(dx, dy)
    except Exception:
        pass


def key_down(key: str) -> None:
    """按下键盘按键。"""
    if not _ensure_dd():
        return
    code = _get_dd_key_code(key)
    if code is None:
        return
    try:
        _dd_dll.DD_key(code, 1)  # 1 = key down
    except Exception:
        pass


def key_up(key: str) -> None:
    """抬起键盘按键。"""
    if not _ensure_dd():
        return
    code = _get_dd_key_code(key)
    if code is None:
        return
    try:
        _dd_dll.DD_key(code, 2)  # 2 = key up
    except Exception:
        pass

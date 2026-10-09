"""Open Lab1, execute, PrintWindow screenshots for report."""
from __future__ import annotations

import ctypes
import shutil
import time
from pathlib import Path

import pyautogui
from PIL import Image
from pywinauto import Application, Desktop

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
kernel32 = ctypes.windll.kernel32
user32.SetProcessDPIAware()
pyautogui.FAILSAFE = False

FIG = Path(r"D:\ycheba_guap\7 семестр\Методы искусственного интеллекта\lab1\figures\knime")
OUT = Path(r"D:\ycheba_guap\7 семестр\Методы искусственного интеллекта\lab1\figures")
LOG = Path(
    r"D:\ycheba_guap\7 семестр\Методы искусственного интеллекта\lab1"
    r"\knime_workspace\.metadata\knime\knime.log"
)


class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long)]


def find_knime() -> int:
    found: list[int] = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def foreach(hwnd, _lp):
        if user32.IsWindowVisible(hwnd):
            n = user32.GetWindowTextLengthW(hwnd)
            b = ctypes.create_unicode_buffer(n + 1)
            user32.GetWindowTextW(hwnd, b, n + 1)
            if b.value == "KNIME Analytics Platform":
                found.append(int(hwnd))
        return True

    user32.EnumWindows(foreach, 0)
    return found[0]


def force_fg(hwnd: int) -> None:
    fg = user32.GetForegroundWindow()
    cur = kernel32.GetCurrentThreadId()
    ft = user32.GetWindowThreadProcessId(fg, None)
    tt = user32.GetWindowThreadProcessId(hwnd, None)
    user32.AttachThreadInput(cur, ft, True)
    user32.AttachThreadInput(cur, tt, True)
    user32.ShowWindow(hwnd, 3)
    user32.BringWindowToTop(hwnd)
    user32.SetForegroundWindow(hwnd)
    user32.AttachThreadInput(cur, ft, False)
    user32.AttachThreadInput(cur, tt, False)
    time.sleep(0.35)


def print_window(hwnd: int, path: Path) -> Image.Image:
    rect = RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    w, h = rect.right - rect.left, rect.bottom - rect.top
    hdc = user32.GetWindowDC(hwnd)
    mdc = gdi32.CreateCompatibleDC(hdc)
    bmp = gdi32.CreateCompatibleBitmap(hdc, w, h)
    gdi32.SelectObject(mdc, bmp)
    user32.PrintWindow(hwnd, mdc, 2)
    buf = ctypes.create_string_buffer(w * h * 4)
    gdi32.GetBitmapBits(bmp, w * h * 4, buf)
    img = Image.frombuffer("RGB", (w, h), buf, "raw", "BGRX", 0, 1).crop((8, 8, w - 8, h - 8))
    img.save(path)
    print("saved", path.name, flush=True)
    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(mdc)
    user32.ReleaseDC(hwnd, hdc)
    return img


def close_dialogs() -> None:
    desk = Desktop(backend="uia")
    for w in desk.windows():
        try:
            t = w.window_text() or ""
            if any(k in t for k in ("Dialog", "Save", "Open", "Открыть", "Confirm", "Warning")):
                print("close", t, flush=True)
                try:
                    w.set_focus()
                    w.type_keys("{ESC}")
                except Exception:
                    pass
                time.sleep(0.3)
        except Exception:
            pass


def main() -> None:
    log_pos = LOG.stat().st_size if LOG.exists() else 0
    close_dialogs()
    hwnd = find_knime()
    force_fg(hwnd)
    rect = RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    print_window(hwnd, FIG / "320_start.png")

    app = Application(backend="uia").connect(handle=hwnd)
    win = app.window(handle=hwnd)

    # Find Lab1 tree item and open with Enter (not just select)
    item = None
    for ctrl in win.descendants():
        try:
            if ctrl.window_text() == "Lab1_Linear_Regression" and "TreeItem" in str(
                ctrl.element_info.control_type
            ):
                item = ctrl
                break
        except Exception:
            continue
    if item is None:
        for ctrl in win.descendants():
            try:
                if ctrl.window_text() == "Lab1_Linear_Regression":
                    item = ctrl
                    break
            except Exception:
                continue

    if item is None:
        raise RuntimeError("Lab1_Linear_Regression not found in explorer")

    print("item rect", item.rectangle(), flush=True)
    item.select()
    time.sleep(0.3)
    item.click_input()
    time.sleep(0.3)
    # Open via context menu Open
    item.click_input(button="right")
    time.sleep(0.8)
    print_window(hwnd, FIG / "321_ctx.png")
    # First item is usually Open
    pyautogui.press("enter")
    time.sleep(5)
    close_dialogs()
    # Also try Enter on item
    try:
        item.type_keys("{ENTER}")
    except Exception:
        pass
    time.sleep(2)
    img = print_window(hwnd, FIG / "322_opened.png")

    # If still welcome page, double-click item
    if b"Welcome" in img.tobytes()[:50000] or True:
        item.double_click_input()
        time.sleep(5)
        img = print_window(hwnd, FIG / "323_dbl.png")

    # Execute
    force_fg(hwnd)
    pyautogui.hotkey("shift", "f7")
    time.sleep(12)
    img = print_window(hwnd, FIG / "324_exec.png")

    new_log = LOG.read_bytes()[log_pos:].decode("utf-8", errors="replace")
    print("---LOG---", flush=True)
    for line in new_log.splitlines():
        if "End execute" in line or "Please specify" in line or "ERROR" in line and "CSV" in line:
            print(line[-200:], flush=True)

    # Save workflow figure - crop canvas
    wf = img.crop((480, 90, 1850, 520))
    wf.save(OUT / "fig1_workflow.png")
    wf.save(OUT / "knime_workflow.png")
    shutil.copy(FIG / "324_exec.png", OUT / "knime_full.png")

    # Click Numeric Scorer (rightmost upper) and open view via Node menu
    # From prior successful layouts: scorer ~ (1663, 300), scatter ~ (1663, 400)
    force_fg(hwnd)
    sx, sy = rect.left + 8 + 1663, rect.top + 8 + 300
    pyautogui.click(sx, sy)
    time.sleep(0.5)
    # Menu: Node -> Open View
    pyautogui.hotkey("alt", "n")
    time.sleep(0.8)
    print_window(hwnd, FIG / "325_nodemenu.png")
    # Walk down to Open View - try pressing 'o' for Open View
    pyautogui.press("o")
    time.sleep(0.5)
    print_window(hwnd, FIG / "326_o.png")
    pyautogui.press("enter")
    time.sleep(0.5)
    pyautogui.press("enter")
    time.sleep(2.5)
    print_window(hwnd, FIG / "327_view.png")

    desk = Desktop(backend="uia")
    for w in desk.windows():
        t = w.window_text() or ""
        if any(k in t for k in ("Dialog", "View", "Scorer", "Numeric")):
            print("view win", t, flush=True)
            try:
                wh = w.handle
                print_window(wh, OUT / "fig2_metrics.png")
                print_window(wh, FIG / "328_scorer.png")
            except Exception as e:
                print("pw fail", e)

    # Scatter
    force_fg(hwnd)
    pyautogui.press("escape")
    time.sleep(0.3)
    pyautogui.click(rect.left + 8 + 1663, rect.top + 8 + 400)
    time.sleep(0.4)
    pyautogui.hotkey("alt", "n")
    time.sleep(0.6)
    pyautogui.press("o")
    time.sleep(0.4)
    pyautogui.press("enter")
    time.sleep(0.3)
    pyautogui.press("enter")
    time.sleep(3)
    for w in desk.windows():
        t = w.window_text() or ""
        if any(k in t for k in ("Interactive", "Scatter", "View", "Dialog", "Plot")):
            print("scatter win", t, flush=True)
            try:
                print_window(w.handle, OUT / "fig3_scatter.png")
                print_window(w.handle, FIG / "329_scatter.png")
            except Exception as e:
                print(e)

    force_fg(hwnd)
    pyautogui.hotkey("ctrl", "s")
    time.sleep(1)
    print_window(hwnd, FIG / "330_final.png")
    print("DONE", flush=True)


if __name__ == "__main__":
    main()

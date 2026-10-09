"""Fix CSV Reader via F6 dialog, execute workflow, capture KNIME screenshots."""
from __future__ import annotations

import ctypes
import shutil
import time
from collections import defaultdict
from pathlib import Path

import pyautogui
import pyperclip
from PIL import Image

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
kernel32 = ctypes.windll.kernel32
user32.SetProcessDPIAware()
pyautogui.FAILSAFE = False

FIG = Path(r"D:\ycheba_guap\7 семестр\Методы искусственного интеллекта\lab1\figures\knime")
OUT = Path(r"D:\ycheba_guap\7 семестр\Методы искусственного интеллекта\lab1\figures")
CSV = r"D:\KNIME\lab1_data\Salary_Data.csv"
FIG.mkdir(parents=True, exist_ok=True)


class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long)]


def find_knime() -> int:
    found: list[int] = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def foreach(hwnd, _lparam):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            if buff.value == "KNIME Analytics Platform":
                found.append(int(hwnd))
        return True

    user32.EnumWindows(foreach, 0)
    return found[0]


def list_wins() -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def foreach(hwnd, _lparam):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            if buff.value:
                out.append((int(hwnd), buff.value))
        return True

    user32.EnumWindows(foreach, 0)
    return out


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
    print("saved", path.name)
    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(mdc)
    user32.ReleaseDC(hwnd, hdc)
    return img


def find_reds(img: Image.Image):
    pix = img.load()
    cells: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
    for y in range(200, 450):
        for x in range(700, 1800):
            r, g, b = pix[x, y][:3]
            if r > 180 and g < 90 and b < 90:
                cells[(x // 25, y // 25)].append((x, y))
    return sorted(
        [
            (sum(p[0] for p in v) // len(v), sum(p[1] for p in v) // len(v), len(v))
            for v in cells.values()
            if len(v) >= 6
        ],
        key=lambda t: t[0],
    )


def find_greens(img: Image.Image):
    pix = img.load()
    cells: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
    for y in range(200, 450):
        for x in range(700, 1800):
            r, g, b = pix[x, y][:3]
            if g > 145 and r < 100 and b < 100 and g - r > 50:
                cells[(x // 25, y // 25)].append((x, y))
    return sorted(
        [
            (sum(p[0] for p in v) // len(v), sum(p[1] for p in v) // len(v), len(v))
            for v in cells.values()
            if len(v) >= 8
        ],
        key=lambda t: (t[0], t[1]),
    )


def main() -> None:
    hwnd = find_knime()
    force_fg(hwnd)
    rect = RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    for _ in range(3):
        pyautogui.press("escape")
        time.sleep(0.2)

    # Close stray dialogs
    for h, t in list_wins():
        if t.startswith("Dialog"):
            user32.SetForegroundWindow(h)
            time.sleep(0.2)
            pyautogui.press("escape")
            time.sleep(0.3)

    force_fg(hwnd)
    img = print_window(hwnd, FIG / "200_start.png")
    reds = find_reds(img)
    greens = find_greens(img)
    print("reds", reds)
    print("greens", greens)

    # CSV Reader is leftmost red or leftmost node ~ x from reds[0] or ~880
    if reds:
        csv_x, csv_y = reds[0][0], reds[0][1] - 35
    else:
        csv_x, csv_y = 886, 265

    force_fg(hwnd)
    pyautogui.click(rect.left + 8 + csv_x, rect.top + 8 + csv_y)
    time.sleep(0.4)
    pyautogui.press("f6")
    time.sleep(2.5)
    print_window(hwnd, FIG / "201_f6.png")

    # Find CSV Reader dialog
    dlg = None
    for h, t in list_wins():
        print("win:", t)
        if "CSV" in t or (t.startswith("Dialog") and "Reader" in t):
            dlg = h
            break
    if dlg is None:
        for h, t in list_wins():
            if t.startswith("Dialog"):
                dlg = h
                break

    if dlg:
        force_fg(dlg)
        drect = RECT()
        user32.GetWindowRect(dlg, ctypes.byref(drect))
        print_window(dlg, FIG / "202_dlg.png")
        # Click Browse button area (right side of path row) then paste in file dialog
        # Or click path field and paste absolute path
        mid_x = (drect.left + drect.right) // 2
        # Path field is typically near top of dialog body
        for dy in (120, 140, 160, 100, 180, 200):
            pyautogui.click(mid_x - 40, drect.top + dy)
            time.sleep(0.1)
        pyperclip.copy(CSV)
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.1)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.4)
        print_window(dlg, FIG / "203_pasted.png")

        # Try Browse... button then type path in Windows dialog
        # Click Browse near path field right side
        pyautogui.click(drect.right - 80, drect.top + 140)
        time.sleep(1.5)
        # Windows Open dialog: Ctrl+L or click address, paste path
        pyautogui.hotkey("alt", "n")  # File name field
        time.sleep(0.3)
        pyperclip.copy(CSV)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.3)
        pyautogui.press("enter")
        time.sleep(1.5)
        print_window(dlg, FIG / "204_after_browse.png")

        # OK
        pyautogui.hotkey("alt", "o")
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(1)
    else:
        print("NO DIALOG")
        force_fg(hwnd)
        pyautogui.press("escape")

    force_fg(hwnd)
    pyautogui.hotkey("shift", "f7")
    time.sleep(10)
    img = print_window(hwnd, FIG / "205_executed.png")
    greens = find_greens(img)
    print("greens after", greens)

    # Workflow crop for report
    wf = img.crop((520, 110, 1780, 480))
    wf.save(OUT / "fig1_workflow.png")
    wf.save(OUT / "knime_workflow.png")
    shutil.copy(FIG / "205_executed.png", OUT / "knime_full.png")

    # Scorer / scatter positions
    right = [g for g in greens if g[0] > 1500]
    right = sorted(right, key=lambda t: t[1])
    if not right and greens:
        right = [greens[-1]]
    scorer = right[0] if right else (1663, 280, 0)
    scatter = right[-1] if len(right) > 1 else (scorer[0], scorer[1] + 90, 0)
    print("scorer", scorer, "scatter", scatter)

    # Select scorer + Node Monitor
    force_fg(hwnd)
    pyautogui.click(rect.left + 8 + scorer[0], rect.top + 8 + scorer[1] - 30)
    time.sleep(0.8)
    # Double-click often opens view for scorer
    pyautogui.doubleClick(rect.left + 8 + scorer[0], rect.top + 8 + scorer[1] - 30)
    time.sleep(2)
    print_window(hwnd, FIG / "206_scorer_dbl.png")
    for h, t in list_wins():
        if t.startswith("Dialog") or "View" in t or "Scorer" in t or "Numeric" in t:
            im = print_window(h, OUT / "fig2_metrics.png")
            im.save(FIG / "207_scorer_view.png")
            print("got scorer view", t)
            pyautogui.press("escape")
            time.sleep(0.5)

    # Context Open View
    force_fg(hwnd)
    pyautogui.click(rect.left + 8 + scorer[0], rect.top + 8 + scorer[1] - 30)
    time.sleep(0.3)
    pyautogui.hotkey("shift", "f10")
    time.sleep(1)
    print_window(hwnd, FIG / "208_ctx.png")
    # Walk menu: Configure is first; Open View often 2nd with submenu
    for _ in range(6):
        pyautogui.press("down")
        time.sleep(0.12)
        print_window(hwnd, FIG / f"209_menu_{_}.png")
    pyautogui.press("right")
    time.sleep(0.4)
    print_window(hwnd, FIG / "210_submenu.png")
    pyautogui.press("enter")
    time.sleep(2.5)
    for h, t in list_wins():
        print("after open view:", t)
        if t.startswith("Dialog") or "View" in t or "Scorer" in t:
            im = print_window(h, OUT / "fig2_metrics.png")
            im.save(FIG / "211_scorer.png")
            print("captured", t)

    # Scatter interactive view
    force_fg(hwnd)
    pyautogui.press("escape")
    time.sleep(0.3)
    pyautogui.click(rect.left + 8 + scatter[0], rect.top + 8 + scatter[1] - 30)
    time.sleep(0.4)
    pyautogui.doubleClick(rect.left + 8 + scatter[0], rect.top + 8 + scatter[1] - 30)
    time.sleep(2.5)
    print_window(hwnd, FIG / "212_scatter_dbl.png")
    for h, t in list_wins():
        if "Interactive" in t or "Scatter" in t or "View" in t or t.startswith("Dialog"):
            im = print_window(h, OUT / "fig3_scatter.png")
            im.save(FIG / "213_scatter.png")
            print("captured scatter", t)

    force_fg(hwnd)
    pyautogui.hotkey("ctrl", "s")
    time.sleep(1)
    print_window(hwnd, FIG / "214_final.png")
    print("DONE")


if __name__ == "__main__":
    main()

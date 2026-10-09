import time, ctypes, sys
from pathlib import Path
from PIL import Image

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
user32.SetProcessDPIAware()

fig = Path(r"D:\ycheba_guap\7 семестр\Методы искусственного интеллекта\lab1\figures\knime")
fig.mkdir(parents=True, exist_ok=True)
name = sys.argv[1] if len(sys.argv) > 1 else "shot"

class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long)]

def find_knime():
    found = []
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def foreach(hwnd, lParam):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            if buff.value == "KNIME Analytics Platform":
                found.append(int(hwnd))
        return True
    user32.EnumWindows(EnumWindowsProc(foreach), 0)
    return found[0] if found else None

hwnd = find_knime()
if not hwnd:
    raise SystemExit("KNIME window not found")
rect = RECT(); user32.GetWindowRect(hwnd, ctypes.byref(rect))
w = rect.right - rect.left; h = rect.bottom - rect.top
hwndDC = user32.GetWindowDC(hwnd)
mfcDC = gdi32.CreateCompatibleDC(hwndDC)
hbmp = gdi32.CreateCompatibleBitmap(hwndDC, w, h)
gdi32.SelectObject(mfcDC, hbmp)
user32.PrintWindow(hwnd, mfcDC, 2)
buf = ctypes.create_string_buffer(w * h * 4)
gdi32.GetBitmapBits(hbmp, w * h * 4, buf)
img = Image.frombuffer("RGB", (w, h), buf, "raw", "BGRX", 0, 1).crop((8, 8, w - 8, h - 8))
out = fig / f"{name}.png"
img.save(out)
gdi32.DeleteObject(hbmp); gdi32.DeleteDC(mfcDC); user32.ReleaseDC(hwnd, hwndDC)
print(out)

"""Drive KNIME Classic UI via pywinauto and capture screenshots."""
from __future__ import annotations

import shutil
import time
from pathlib import Path

import pyperclip
from PIL import ImageGrab
from pywinauto import Application, Desktop

FIG = Path(r"D:\ycheba_guap\7 семестр\Методы искусственного интеллекта\lab1\figures\knime")
OUT = Path(r"D:\ycheba_guap\7 семестр\Методы искусственного интеллекта\lab1\figures")
CSV = r"D:\KNIME\lab1_data\Salary_Data.csv"
FIG.mkdir(parents=True, exist_ok=True)


def shot(name: str):
    img = ImageGrab.grab()
    path = FIG / name
    img.save(path)
    print("shot", name, flush=True)
    return img


def dump_windows(desk: Desktop) -> None:
    for w in desk.windows():
        try:
            t = w.window_text()
            if t:
                print("WIN:", repr(t)[:100], flush=True)
        except Exception:
            pass


def close_modals(desk: Desktop) -> None:
    for w in desk.windows():
        try:
            t = w.window_text() or ""
            if not t:
                continue
            if any(k in t for k in ("Dialog", "Save", "Confirm", "Warning", "Error", "CSV", "Configure")):
                print("modal:", t, flush=True)
                try:
                    w.set_focus()
                except Exception:
                    pass
                time.sleep(0.2)
                # Prefer Discard / No / Cancel / Escape
                try:
                    w.type_keys("%n")
                except Exception:
                    pass
                time.sleep(0.2)
                try:
                    w.type_keys("{ESC}")
                except Exception:
                    pass
                time.sleep(0.3)
        except Exception:
            pass


def main() -> None:
    desk = Desktop(backend="uia")
    dump_windows(desk)
    close_modals(desk)
    time.sleep(0.5)

    app = Application(backend="uia").connect(title="KNIME Analytics Platform", timeout=20)
    win = app.window(title="KNIME Analytics Platform")
    try:
        win.set_focus()
    except Exception as e:
        print("focus fail", e)
        close_modals(desk)
        win.set_focus()
    time.sleep(0.5)
    shot("300_focus.png")
    dump_windows(desk)

    # Close current editor tab
    try:
        win.type_keys("^w")
    except Exception:
        pass
    time.sleep(1.2)
    close_modals(desk)
    time.sleep(0.5)
    shot("301_after_close.png")

    # Open Lab1 from explorer
    opened = False
    try:
        item = win.descendant(title="Lab1_Linear_Regression", control_type="TreeItem")
        print("tree item found", item.rectangle(), flush=True)
        item.double_click_input()
        opened = True
        time.sleep(4)
    except Exception as e:
        print("tree item fail", e, flush=True)

    if not opened:
        try:
            # Any control with that name
            for ctrl in win.descendants():
                try:
                    if ctrl.window_text() == "Lab1_Linear_Regression":
                        print("ctrl", ctrl.element_info.control_type, ctrl.rectangle())
                        ctrl.double_click_input()
                        opened = True
                        time.sleep(4)
                        break
                except Exception:
                    continue
        except Exception as e:
            print("descendants fail", e)

    if not opened:
        print("fallback double-click coords", flush=True)
        win.double_click_input(coords=(168, 272))
        time.sleep(4)

    close_modals(desk)
    shot("302_opened.png")

    # Execute all
    try:
        win.set_focus()
        win.type_keys("+{F7}")
    except Exception as e:
        print("exec keys", e)
    time.sleep(10)
    img = shot("303_executed.png")
    wf = img.crop((520, 110, 1780, 500))
    wf.save(OUT / "fig1_workflow.png")
    wf.save(OUT / "knime_workflow.png")
    print("workflow saved", flush=True)

    # List interesting descendants
    for title in ("Numeric Scorer", "Scatter Plot", "CSV Reader", "Node 7"):
        try:
            found = [c for c in win.descendants() if c.window_text() == title]
            print(title, len(found), flush=True)
        except Exception as e:
            print(title, e)

    # Configure CSV Reader via double-click
    try:
        csv_nodes = [c for c in win.descendants() if c.window_text() == "CSV Reader"]
        if csv_nodes:
            csv_nodes[0].double_click_input()
            time.sleep(2.5)
            shot("304_csv_dlg.png")
            dump_windows(desk)
            for w in desk.windows():
                t = w.window_text() or ""
                if "CSV" in t or "Reader" in t:
                    print("configuring", t, flush=True)
                    w.set_focus()
                    time.sleep(0.3)
                    # Try to find edit/browse
                    try:
                        edits = w.descendants(control_type="Edit")
                        print("edits", len(edits))
                        if edits:
                            edits[0].set_edit_text(CSV)
                            time.sleep(0.3)
                    except Exception as e:
                        print("edit fail", e)
                        pyperclip.copy(CSV)
                        w.type_keys("^a^v")
                    time.sleep(0.3)
                    # OK button
                    try:
                        ok = w.child_window(title="OK", control_type="Button")
                        ok.click_input()
                    except Exception:
                        w.type_keys("%o")
                    time.sleep(1)
            win.set_focus()
            win.type_keys("+{F7}")
            time.sleep(10)
            img = shot("305_reexec.png")
            wf = img.crop((520, 110, 1780, 500))
            wf.save(OUT / "fig1_workflow.png")
    except Exception as e:
        print("csv path", e)

    # Open Numeric Scorer view
    try:
        scorers = [c for c in win.descendants() if c.window_text() == "Numeric Scorer"]
        print("scorers", len(scorers), flush=True)
        if scorers:
            scorers[0].click_input()
            time.sleep(0.4)
            scorers[0].click_input(button="right")
            time.sleep(1.2)
            shot("306_scorer_ctx.png")
            dump_windows(desk)
            # Context menu is often a separate window
            for w in desk.windows():
                t = w.window_text() or ""
                ct = ""
                try:
                    ct = w.element_info.control_type
                except Exception:
                    pass
                if ct in ("Menu", "MenuItem") or "Context" in t:
                    print("menu win", t, ct)
            # Navigate Open View
            import pyautogui

            pyautogui.press("down")
            time.sleep(0.15)
            pyautogui.press("down")
            time.sleep(0.15)
            pyautogui.press("right")
            time.sleep(0.4)
            shot("307_submenu.png")
            pyautogui.press("enter")
            time.sleep(2.5)
            dump_windows(desk)
            for w in desk.windows():
                t = w.window_text() or ""
                if any(k in t for k in ("Dialog", "View", "Scorer", "Numeric", "score")):
                    print("capture scorer", t, flush=True)
                    r = w.rectangle()
                    ImageGrab.grab(bbox=(r.left, r.top, r.right, r.bottom)).save(OUT / "fig2_metrics.png")
                    ImageGrab.grab(bbox=(r.left, r.top, r.right, r.bottom)).save(FIG / "308_scorer.png")
                    try:
                        w.type_keys("{ESC}")
                    except Exception:
                        pass
    except Exception as e:
        print("scorer", e)

    # Scatter
    try:
        plots = [c for c in win.descendants() if "Scatter" in (c.window_text() or "") or c.window_text() == "Node 7"]
        print("plots", [(c.window_text(), c.rectangle()) for c in plots[:5]], flush=True)
        if plots:
            plots[0].click_input()
            time.sleep(0.3)
            plots[0].click_input(button="right")
            time.sleep(1)
            import pyautogui

            pyautogui.press("down")
            time.sleep(0.12)
            pyautogui.press("down")
            time.sleep(0.12)
            pyautogui.press("right")
            time.sleep(0.4)
            pyautogui.press("enter")
            time.sleep(3)
            dump_windows(desk)
            for w in desk.windows():
                t = w.window_text() or ""
                if any(k in t for k in ("Interactive", "Scatter", "View", "Dialog")):
                    print("capture scatter", t, flush=True)
                    r = w.rectangle()
                    ImageGrab.grab(bbox=(r.left, r.top, r.right, r.bottom)).save(OUT / "fig3_scatter.png")
                    ImageGrab.grab(bbox=(r.left, r.top, r.right, r.bottom)).save(FIG / "309_scatter.png")
    except Exception as e:
        print("scatter", e)

    try:
        win.set_focus()
        win.type_keys("^s")
    except Exception:
        pass
    time.sleep(1)
    shot("310_done.png")
    if (FIG / "305_reexec.png").exists():
        shutil.copy(FIG / "305_reexec.png", OUT / "knime_full.png")
    elif (FIG / "303_executed.png").exists():
        shutil.copy(FIG / "303_executed.png", OUT / "knime_full.png")
    print("DONE", flush=True)


if __name__ == "__main__":
    main()

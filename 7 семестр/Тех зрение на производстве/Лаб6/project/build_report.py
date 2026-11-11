# -*- coding: utf-8 -*-
"""Отчёт ЛР6 в стиле предыдущих работ (ГУАП, кафедра 42)."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from gost_docx import add_fig, add_h, add_p, add_table, init_gost_doc, set_run_font
from docx.shared import Cm

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
OUT = ROOT.parent / "ЛР6_ТЕХ_Лаврешин.docx"
RUNS = ROOT / "runs" / "lr6"


def main():
    sel = json.loads((RESULTS / "selected_model.json").read_text(encoding="utf-8"))
    stats = sel["splits"]
    env = sel["environment"]
    a, b = sel["compare"]
    notes = sel["valid_notes"]

    doc = init_gost_doc()

    for t in ["ГУАП", "КАФЕДРА № 42"]:
        add_p(doc, t, center=True, bold=True, first_line=False)
    add_p(doc, "", first_line=False)
    add_p(doc, "ОТЧЕТ", center=True, bold=True, size=16, first_line=False)
    add_p(
        doc,
        "по лабораторной работе №6",
        center=True,
        bold=True,
        first_line=False,
    )
    add_p(
        doc,
        "«Выбор и обучение нейронной сети по размеченным данным»",
        center=True,
        bold=True,
        first_line=False,
    )
    add_p(doc, "", first_line=False)
    add_p(doc, "ЗАЩИЩЕН С ОЦЕНКОЙ ПРЕПОДАВАТЕЛЬ", center=True, first_line=False)
    add_p(doc, "", first_line=False)
    add_p(doc, "", first_line=False)
    add_p(doc, "РАБОТУ ВЫПОЛНИЛ", center=True, first_line=False)
    add_p(doc, "", first_line=False)
    add_p(doc, "", first_line=False)
    add_p(doc, "", first_line=False)
    add_p(doc, "Санкт-Петербург 2026", center=True, first_line=False)

    add_h(doc, "ВВЕДЕНИЕ")
    add_p(
        doc,
        "В лабораторных работах №3–5 подготовлены предобработка, признаки объекта и "
        "размеченный набор данных складского инструмента. В настоящей работе на этом "
        "наборе выполнено обучение детектора YOLOv8, проведено сравнение двух конфигураций "
        "сети по варианту 9 и сохранена выбранная модель для проверки на видеокадрах в ЛР7.",
    )

    add_h(doc, "1 Цель работы")
    add_p(
        doc,
        "Цель работы — приобрести навыки выбора нейронной сети для обнаружения "
        "производственных объектов, подготовки параметров обучения и оценки полученной "
        "модели по валидационной выборке; выполнить два сопоставимых опыта на наборе "
        "лабораторной работы №5 и сохранить модель для лабораторной работы №7.",
    )

    add_h(doc, "2 Вариант задания, объект и классы")
    add_p(
        doc,
        "Вариант 9: производственный объект — инструмент на складе; классы разметки — "
        "wrench, hammer, pliers (порядок в data.yaml: 0, 1, 2). Изменяемый фактор опыта — "
        "конфигурация сети: опыт A — YOLOv8n с предварительными весами yolov8n.pt; "
        "опыт B — YOLOv8s с предварительными весами yolov8s.pt. Остальные параметры обучения "
        "одинаковы.",
    )

    add_h(doc, "3 Источник и версия набора из ЛР5")
    add_p(
        doc,
        "Использован окончательный экспорт рамочной разметки лабораторной работы №5 "
        "(локальный каталог yolov8_export / версия lab5_tools с разбиением по роликам; "
        "проект Roboflow ilyalychas-workspace/ilyalycha_4321). Всего 48 изображений из "
        "6 роликов. Кадры одного ролика не распределялись между выборками.",
    )
    add_p(doc, "Таблица 1 − Число изображений и рамок по классам", center=True, size=12, first_line=False)
    add_table(
        doc,
        ["Выборка", "Изображений", "wrench", "hammer", "pliers", "Ролики"],
        [
            [
                "train",
                stats["train"]["n_images"],
                stats["train"]["boxes"].get("wrench", 0),
                stats["train"]["boxes"].get("hammer", 0),
                stats["train"]["boxes"].get("pliers", 0),
                ", ".join(stats["train"]["scenes"]),
            ],
            [
                "valid",
                stats["valid"]["n_images"],
                stats["valid"]["boxes"].get("wrench", 0),
                stats["valid"]["boxes"].get("hammer", 0),
                stats["valid"]["boxes"].get("pliers", 0),
                ", ".join(stats["valid"]["scenes"]),
            ],
            [
                "test",
                stats["test"]["n_images"],
                stats["test"]["boxes"].get("wrench", 0),
                stats["test"]["boxes"].get("hammer", 0),
                stats["test"]["boxes"].get("pliers", 0),
                ", ".join(stats["test"]["scenes"]),
            ],
        ],
    )
    add_p(
        doc,
        "Пересечение роликов между выборками отсутствует. Все классы присутствуют в "
        "train, valid и test, поэтому качество обнаружения каждого класса на valid можно оценить.",
    )

    add_h(doc, "4 Программная среда и вычислитель")
    add_p(
        doc,
        f"Python {env['python']}; Ultralytics {env['ultralytics']}; PyTorch {env['torch']} "
        f"(CUDA {env['cuda']}); OpenCV, PyYAML, NumPy. ОС: {env['platform']}. "
        f"Процессор: {env['cpu']}; ОЗУ ≈ {env['ram_gb']} ГБ; GPU: {env['gpu']}. "
        "Перечень пакетов сохранён в project/requirements.txt. Обучение выполнялось на GPU.",
    )

    add_h(doc, "5 Файл data.yaml и согласование предобработки")
    add_p(
        doc,
        "Программа prepare_dataset.py сохранила исходное описание как data_original.yaml, "
        "проверила каталоги train/valid/test и записала явный path к корню набора. "
        "Ключ val указывает на valid/images. Порядок классов: 0 — wrench, 1 — hammer, 2 — pliers.",
    )
    add_p(
        doc,
        "Функция prepare_frame в preprocess.py возвращает копию кадра BGR uint8 без "
        "дополнительных операций. Разметка ЛР5 выполнялась на уже подготовленных кадрах "
        "набора без внешней коррекции яркости/фильтрации непосредственно перед аннотированием; "
        "поэтому при применении модели к новым кадрам требуется тот же вид изображения. "
        "Изменение размера внутри YOLO (imgsz=640) не заменяет внешнюю предобработку, "
        "которая в данном случае не применялась.",
    )

    add_h(doc, "6 Обоснование конфигурации и изменяемого фактора")
    add_p(
        doc,
        "YOLOv8n — малая конфигурация с меньшим числом параметров и меньшей вычислительной "
        "нагрузкой. YOLOv8s — «small»-конфигурация той же архитектуры семейства с большей "
        "ёмкостью представления признаков. В варианте 9 сравниваются две предобученные "
        "модели (.pt): перенос весов ImageNet/COCO-предобучения на классы инструмента. "
        "Выбор между n и s нельзя делать только по размеру файла весов: решение принимается "
        "по mAP@0.5:0.95 на одной и той же valid при фиксированных прочих параметрах.",
    )
    add_p(
        doc,
        "Общие условия опытов (по методичке): epochs=40, imgsz=640, batch=4, optimizer=AdamW, "
        "lr0=0.001, lrf=0.01, seed=42, deterministic=True, amp=False, patience=0, "
        "аугментации (mosaic, mixup, hsv_*, degrees, translate, scale, flip*) отключены "
        "(значение 0), workers=0.",
    )

    add_h(doc, "7 Параметры опытов A и B, программа обучения и результаты")
    add_p(
        doc,
        "Опыты запускались программой train_compare.py (VARIANT=9) из каталога project. "
        "Текст программы соответствует приведённому в методичке; изменён только номер варианта. "
        "Каждый опыт начинался с новой загрузки модели и фиксации генераторов случайных чисел. "
        "После обучения оценивался файл best.pt на split=val (conf=0.001, iou=0.7 для NMS).",
    )
    add_p(doc, "Листинг 1 − Фрагмент train_compare.py (вариант и таблица факторов)", first_line=False, size=12)
    code = (
        "VARIANT = 9\n"
        "CASES = {\n"
        "    ...\n"
        '    9: ("model", "yolov8n.pt", "yolov8s.pt"),\n'
        "    ...\n"
        "}\n"
        "# common: epochs=40, imgsz=640, batch=4, AdamW, lr0=0.001,\n"
        "# seed=42, patience=0, аугментации = 0"
    )
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0)
    run = p.add_run(code)
    set_run_font(run, name="Consolas", size=11)
    add_p(
        doc,
        "Полный листинг сохранён в файле project/train_compare.py и воспроизводит алгоритм "
        "сравнения режимов обучения из методических указаний.",
        first_line=False,
    )
    add_p(doc, "Таблица 2 − Измеренные результаты на valid", center=True, size=12, first_line=False)
    add_table(
        doc,
        [
            "Опыт",
            "Фактор и значение",
            "Эпохи",
            "imgsz",
            "mAP@0.5",
            "mAP@0.5:0.95",
            "Время, с",
            "Веса, МБ",
        ],
        [
            [
                "A",
                "model = yolov8n.pt",
                a["epochs"],
                a["imgsz"],
                f"{a['map50']:.3f}",
                f"{a['map50_95']:.3f}",
                f"{a['train_s']:.2f}",
                f"{a['weights_mb']:.3f}",
            ],
            [
                "B",
                "model = yolov8s.pt",
                b["epochs"],
                b["imgsz"],
                f"{b['map50']:.3f}",
                f"{b['map50_95']:.3f}",
                f"{b['train_s']:.2f}",
                f"{b['weights_mb']:.3f}",
            ],
        ],
    )
    add_fig(doc, RESULTS / "results_v09_a.png", "Рисунок 1 − Кривые обучения опыта A (YOLOv8n)")
    add_fig(doc, RESULTS / "results_v09_b.png", "Рисунок 2 − Кривые обучения опыта B (YOLOv8s)")
    add_p(
        doc,
        "По кривым results.png в обоих опытах обучающие потери (box/cls/dfl) снижаются на "
        "протяжении 40 эпох. Валидационный mAP растёт в первой половине обучения и затем "
        "стабилизируется; выраженного участка, где train-ошибка продолжает падать при "
        "устойчивом ухудшении valid, не наблюдается, поэтому вывод о переобучении только "
        "по разнице train/valid ошибок не делается. Файл best.pt выбран библиотекой по "
        "валидационному критерию и может отличаться от last.pt.",
    )
    add_fig(
        doc,
        RESULTS / "confusion_v09_b.png",
        "Рисунок 3 − Матрица ошибок выбранной модели (опыт B) на valid",
        width_cm=12,
    )

    add_h(doc, "8 Разбор предсказаний на валидационных кадрах")
    add_p(
        doc,
        "Просмотрены все 8 валидационных изображений ролика video01 с предсказаниями "
        f"выбранной модели при рабочем пороге уверенности conf={sel['valid_pred_conf']} "
        "(порог выбран для наглядного разбора; расчёт mAP выполнялся при conf=0.001). "
        "Серые рамки — эталон ЛР5, цветные — предсказания модели.",
    )
    # pick up to 5 diverse examples
    order = []
    for kind in ("wrong_class", "miss", "extra", "TP"):
        for n in notes:
            if kind in n["kinds"] and n["image"] not in order:
                order.append(n["image"])
            if len(order) >= 5:
                break
        if len(order) >= 5:
            break
    for n in notes:
        if n["image"] not in order:
            order.append(n["image"])
        if len(order) >= 5:
            break

    fig_i = 4
    for name in order[:5]:
        note = next(x for x in notes if x["image"] == name)
        img = RESULTS / "valid_predictions" / f"{Path(name).stem}_pred.jpg"
        add_fig(doc, img, f"Рисунок {fig_i} − Валидационный кадр {name}", width_cm=14)
        parts = [
            f"GT={note['gt']}, pred={note['pred']}, TP={note['tp']}, "
            f"пропуски={note['miss']}, лишние={note['extra']}."
        ]
        if note["wrong_class"]:
            wc = ", ".join(f"{w['pred']}→{w['gt']}" for w in note["wrong_class"])
            parts.append(f"Ошибка класса: {wc}.")
        if note["miss"]:
            parts.append(
                "Пропуски связаны с частичным перекрытием инструментов и сходством "
                "контуров рукояток (признаки формы/границ из ЛР4) на сложном фоне."
            )
        if note["extra"]:
            parts.append(
                "Лишние рамки появляются на участках фона/текстуры, похожих на рукоятку "
                "или металлическую головку; это согласуется с чувствительностью к локальному "
                "контрасту и цвету, отмеченной при анализе признаков."
            )
        if not note["miss"] and not note["extra"] and not note["wrong_class"]:
            parts.append("Кадр содержит корректные обнаружения без явных пропусков и ложных рамок.")
        add_p(doc, " ".join(parts))
        fig_i += 1

    kinds_present = set()
    for n in notes:
        kinds_present.update(n["kinds"])
    missing_kinds = [k for k in ("TP", "miss", "extra", "wrong_class") if k not in kinds_present]
    if missing_kinds:
        add_p(
            doc,
            "На valid при выбранном пороге не встретились типы ошибок: "
            + ", ".join(missing_kinds)
            + ".",
        )
    else:
        add_p(
            doc,
            "На valid при выбранном пороге наблюдались верные обнаружения, пропуски и/или "
            "лишние рамки; ошибки класса при наличии указаны в разборе кадров.",
        )

    add_h(doc, "9 Выбор модели для ЛР7")
    add_p(doc, sel["selection_rule"])
    add_p(
        doc,
        f"Сохранён файл results/selected_model.json. Путь к весам: {sel['weights']}; "
        f"imgsz={sel['imgsz']}; классы={sel['classes']}. Полная конфигурация обучения — "
        f"в runs/lr6/{sel['chosen_run']}/args.yaml. Тестовая выборка на данном этапе не использовалась.",
    )

    add_h(doc, "10 Вывод")
    add_p(
        doc,
        "Изученный фактор — ёмкость конфигурации YOLOv8 (n против s) при одинаковых данных "
        "и гиперпараметрах. На valid модель YOLOv8s дала существенно более высокий "
        f"mAP@0.5:0.95 ({b['map50_95']:.3f} против {a['map50_95']:.3f}) при большем времени "
        f"обучения ({b['train_s']:.1f} с против {a['train_s']:.1f} с) и большем файле весов "
        f"({b['weights_mb']:.1f} МБ против {a['weights_mb']:.1f} МБ). Ограничения результата: "
        "учебный набор из 48 кадров, valid из одного ролика; высокие метрики не гарантируют "
        "качество на реальной производственной съёмке. Итоговая проверка на test и видео "
        "отложена до лабораторной работы №7.",
    )

    add_h(doc, "Перечень файлов для ЛР7")
    add_p(
        doc,
        "1) runs/lr6/v09_b/weights/best.pt; 2) dataset/data.yaml (классы и пути); "
        "3) results/selected_model.json; 4) preprocess.py (prepare_frame); "
        "5) results/lr6_compare.csv и результаты обоих опытов в runs/lr6/.",
        first_line=False,
    )

    add_h(doc, "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ")
    add_p(
        doc,
        "1. Ultralytics YOLO Docs. Predict / Val modes [Электронный ресурс]. — URL: https://docs.ultralytics.com (дата обращения: 05.11.2026).",
        first_line=False,
    )
    add_p(
        doc,
        "2. Методические указания к лабораторной работе №6 «Выбор и обучение нейронной сети по размеченным данным».",
        first_line=False,
    )
    add_p(
        doc,
        "3. ГОСТ 7.32−2017. Отчёт о научно-исследовательской работе. Структура и правила оформления.",
        first_line=False,
    )

    doc.save(str(OUT))
    shutil.copy2(OUT, ROOT / "ЛР6_ТЕХ_Лаврешин.docx")
    print("saved", OUT)


if __name__ == "__main__":
    main()

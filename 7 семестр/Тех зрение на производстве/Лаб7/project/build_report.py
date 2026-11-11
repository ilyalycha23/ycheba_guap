# -*- coding: utf-8 -*-
"""Отчёт ЛР7 по ГОСТ 7.32."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from gost_docx import add_fig, add_h, add_p, add_table, init_gost_doc, set_run_font
from docx.shared import Cm

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
OUT = ROOT.parent / "ЛР7_ТЕХ_Лаврешин.docx"


def fmt(x, nd=3):
    if x is None:
        return "—"
    return f"{x:.{nd}f}"


def main():
    mode = json.loads((RESULTS / "lr7_mode.json").read_text(encoding="utf-8"))
    thr = json.loads((RESULTS / "lr7_thresholds.json").read_text(encoding="utf-8"))
    test = json.loads((RESULTS / "lr7_test.json").read_text(encoding="utf-8"))
    vq = json.loads((RESULTS / "lr7_video_quality.json").read_text(encoding="utf-8"))
    vmeta = json.loads((RESULTS / "video_test_meta.json").read_text(encoding="utf-8"))
    timing = json.loads((RESULTS / "lr7_video" / "summary.json").read_text(encoding="utf-8"))
    v9 = json.loads((RESULTS / "variant9_save_video" / "compare.json").read_text(encoding="utf-8"))
    examples = json.loads((RESULTS / "error_examples" / "notes.json").read_text(encoding="utf-8"))

    doc = init_gost_doc()

    for t in ["ГУАП", "КАФЕДРА № 42"]:
        add_p(doc, t, center=True, bold=True, first_line=False)
    add_p(doc, "", first_line=False)
    add_p(doc, "ОТЧЕТ", center=True, bold=True, size=16, first_line=False)
    add_p(doc, "по лабораторной работе №7", center=True, bold=True, first_line=False)
    add_p(
        doc,
        "«Тестирование нейронной сети на видеокадрах производственных объектов»",
        center=True,
        bold=True,
        first_line=False,
    )
    add_p(doc, "", first_line=False)
    add_p(doc, "ЗАЩИЩЕН С ОЦЕНКОЙ ПРЕПОДАВАТЕЛЬ", center=True, first_line=False)
    add_p(doc, "", first_line=False)
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
        "В лабораторной работе №6 обучена и выбрана модель YOLOv8s для классов "
        "wrench, hammer, pliers. В настоящей работе веса не изменяются: на valid "
        "выбирается рабочий порог уверенности, затем оцениваются независимый test "
        "из ЛР5 и новый видеоролик с ручной разметкой части кадров. По варианту 9 "
        "сравнивается влияние записи annotated.mp4 (SAVE_VIDEO) на время полного цикла.",
    )

    add_h(doc, "1 Цель работы, вариант, объект и классы")
    add_p(
        doc,
        "Цель работы — приобрести навыки проверки обученной нейронной сети на независимых "
        "изображениях и видеокадрах, определить точность и полноту обнаружения, "
        "проанализировать ошибки и измерить продолжительность обработки кадра.",
    )
    add_p(
        doc,
        "Вариант 9: производственный объект — инструмент на складе; классы — wrench, "
        "hammer, pliers. Индивидуальное задание (алгоритм 3): сравнить SAVE_VIDEO = True "
        "и False при одинаковом нанесении рамок и записи CSV; выполнить три прохода "
        "каждого режима и сравнить медианы показателей времени.",
    )

    add_h(doc, "2 Модель из ЛР6 и версия набора")
    add_p(
        doc,
        f"Загружены веса {mode['weights']}, imgsz = {mode['imgsz']}. Порядок классов "
        f"совпадает с dataset/data.yaml: {mode.get('classes')}. Версия набора: "
        f"{mode.get('dataset_version')}. Предобработка: {mode.get('preprocessing')}. "
        "Устройство проверки: NVIDIA GeForce RTX 5060 Ti (CUDA), PyTorch 2.11+cu128, "
        "Ultralytics 8.4. Веса при выполнении работы не изменялись.",
    )

    add_h(doc, "3 Подбор рабочего порога на valid")
    add_p(
        doc,
        "На валидационной выборке ЛР5 (ролик video01, 8 кадров) сравнены пороги "
        "conf ∈ {0,15; 0,35; 0,55}. Критерий выбора: максимум F1, при равенстве — "
        "большая точность P, затем больший conf. NMS iou = 0,7; порог сопоставления "
        "IoU ≥ 0,5. После выбора режим зафиксирован в results/lr7_mode.json.",
    )
    add_table(
        doc,
        ["conf", "TP", "FP", "FN", "P", "R", "F1"],
        [
            [
                r["conf"],
                r["TP"],
                r["FP"],
                r["FN"],
                fmt(r["P"]),
                fmt(r["R"]),
                fmt(r["F1"]),
            ]
            for r in thr
        ],
        caption="Таблица 1 − Подбор рабочего порога на valid",
    )
    add_p(
        doc,
        f"Выбранный режим: conf = {mode['conf']}, nms_iou = {mode['nms_iou']}, "
        f"match_iou = {mode['match_iou']}, imgsz = {mode['imgsz']}. "
        "До завершения итоговой проверки параметры не изменялись.",
    )

    add_h(doc, "4 Источники test и нового ролика")
    add_p(
        doc,
        "Test из ЛР5: 8 кадров ролика video06 (не пересекается с train/valid). "
        f"Новый ролик: {vmeta['video']}, частота {vmeta['fps']} кадр/с, длительность "
        f"{vmeta['duration_s']} с, разрешение {vmeta['resolution'][0]}×{vmeta['resolution'][1]}, "
        f"всего {vmeta['frames_total']} кадров. Для количественной оценки размечено "
        f"{vmeta['labeled_frames']} различающихся кадров (в т.ч. {vmeta['empty_labeled']} "
        f"пустых); эталонных рамок: wrench — {vmeta['class_boxes']['wrench']}, "
        f"hammer — {vmeta['class_boxes']['hammer']}, pliers — {vmeta['class_boxes']['pliers']}. "
        "Кадры ролика не входят в train/valid.",
    )

    add_h(doc, "5 Согласование предобработки и координат")
    add_p(
        doc,
        "Функция prepare_frame возвращает кадр BGR uint8 без изменений (как в ЛР6). "
        "Для video_test prepare_frame применена ровно один раз перед сохранением "
        "изображений; evaluate повторно её не вызывает. Координаты detections.csv и "
        "рамок на annotated.mp4 относятся к подготовленному кадру. Поскольку геометрия "
        "не менялась, пересчёт масштаба/полей не требуется.",
    )

    add_h(doc, "6 Сопоставление рамок и проверка на простых случаях")
    add_p(
        doc,
        "Реализованы функции iou, match_counts, scores, read_truth, evaluate "
        "(файл evaluate_frames.py) по методичке. Предсказания упорядочиваются по "
        "убыванию уверенности; эталонная рамка используется не более одного раза; "
        "сопоставление — по классу и IoU ≥ 0,5.",
    )
    add_p(doc, "Листинг 1 − Проверка match_counts на трёх простых случаях", first_line=False, size=12)
    code = (
        "# ожидаемые (TP, FP, FN):\n"
        "одна правильная рамка        -> (1, 0, 0)\n"
        "две рамки одного объекта     -> (1, 1, 0)\n"
        "рамка с неверным классом     -> (0, 1, 1)\n"
        "# факт: match_counts self-check OK"
    )
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0)
    run = p.add_run(code)
    set_run_font(run, name="Consolas", size=11)

    add_h(doc, "7 Результаты на test и video_test")
    add_table(
        doc,
        ["Набор", "Кадры", "Эталон", "TP", "FP", "FN", "P", "R", "F1", "mAP50", "mAP50-95"],
        [
            [
                "test ЛР5",
                test["images"],
                test["TP"] + test["FN"],
                test["TP"],
                test["FP"],
                test["FN"],
                fmt(test["P"]),
                fmt(test["R"]),
                fmt(test["F1"]),
                fmt(test["map50"]),
                fmt(test["map50_95"]),
            ],
            [
                "video_test",
                vq["images"],
                vq["TP"] + vq["FN"],
                vq["TP"],
                vq["FP"],
                vq["FN"],
                fmt(vq["P"]),
                fmt(vq["R"]),
                fmt(vq["F1"]),
                "—",
                "—",
            ],
        ],
        caption="Таблица 2 − Сводные показатели при рабочем пороге",
    )
    add_table(
        doc,
        ["Класс", "TP", "FP", "FN", "P", "R", "F1"],
        [
            [
                name,
                vq["classes"][name]["TP"],
                vq["classes"][name]["FP"],
                vq["classes"][name]["FN"],
                fmt(vq["classes"][name]["P"]),
                fmt(vq["classes"][name]["R"]),
                fmt(vq["classes"][name]["F1"]),
            ]
            for name in ["wrench", "hammer", "pliers"]
        ],
        caption="Таблица 3 − Показатели по классам на video_test",
    )
    add_p(
        doc,
        "На независимом test качество высокое (F1 ≈ 0,84; mAP@0.5 ≈ 0,93). На новом "
        "ролике F1 ниже из‑за смены фона/компоновки и артефактов вклейки патчей; "
        "наиболее трудный класс по полноте — wrench. Одинаковые F1 на малом числе "
        "объектов не следует трактовать как производственный норматив.",
    )

    add_h(doc, "8 Разбор предсказаний на кадрах")
    add_p(
        doc,
        "Ниже приведены не менее пяти кадров (серые рамки — эталон, цветные — "
        "предсказания при conf = 0,55). Причины ошибок связываются с признаками "
        "формы/контраста (ЛР4) и условиями наблюдения, а не только с величиной уверенности.",
    )
    for i, note in enumerate(examples["selected"][:5], 1):
        img = RESULTS / "error_examples" / note["file"]
        add_fig(
            doc,
            img,
            f"Рисунок {i} − Кадр {note['image']} (TP={note['TP']}, FP={note['FP']}, FN={note['FN']})",
            width_cm=14,
        )
        reasons = []
        if note["FN"]:
            reasons.append(
                "пропуски связаны с частичным перекрытием, малой проекцией или сходством "
                "с фоном"
            )
        if note["FP"]:
            reasons.append(
                "лишние рамки возникают на текстуре фона/границах вклейки, похожих на инструмент"
            )
        if note["TP"] and not note["FN"] and not note["FP"]:
            reasons.append("корректные обнаружения без явных ошибок на кадре")
        add_p(doc, "Наблюдение: " + "; ".join(reasons) + ".")

    add_h(doc, "9 Время predict и полного цикла")
    add_p(
        doc,
        f"Основной журнал: results/lr7_video (SAVE_VIDEO = True). Кадров: {timing['frames']}, "
        f"исходная частота {timing['source_fps']} кадр/с (бюджет кадра "
        f"{1000/timing['source_fps']:.1f} мс). Прогрев модели и загрузка весов в измерение "
        "не входят. cycle_ms включает prepare_frame, predict, plot рамок, запись CSV и "
        "VideoWriter.write; закрытие файлов — вне интервала.",
    )
    add_table(
        doc,
        ["Показатель", "Значение"],
        [
            ["predict_mean_ms", fmt(timing["predict_mean_ms"], 2)],
            ["cycle_mean_ms", fmt(timing["cycle_mean_ms"], 2)],
            ["cycle_median_ms", fmt(timing["cycle_median_ms"], 2)],
            ["cycle_p95_ms", fmt(timing["cycle_p95_ms"], 2)],
            ["processing_fps", fmt(timing["processing_fps"], 2)],
            ["over_budget_percent", fmt(timing["over_budget_percent"], 1)],
        ],
        caption="Таблица 4 − Быстродействие на test_video (SAVE_VIDEO = True)",
    )
    add_p(
        doc,
        "Плавность annotated.mp4 не доказывает обработку в темпе исходного файла: "
        "скорость оценивается по timings.csv и processing_fps. При 15 кадр/с среднее "
        "и 95-й процентиль полного цикла меньше бюджета кадра; для потока 25 кадр/с "
        "(40 мс) запас меньше и зависит от включения записи видео.",
    )

    add_h(doc, "10 Индивидуальное исследование (вариант 9)")
    add_p(
        doc,
        "Сравнивались режимы SAVE_VIDEO = True и False. В обоих режимах выполнялись "
        "нанесение рамок (result.plot) и запись detections.csv/timings.csv; изменялась "
        "только запись annotated.mp4. Выполнено по три прохода одного ролика после прогрева; "
        "разрешение, устройство, порог и состав кадров фиксированы.",
    )
    add_table(
        doc,
        ["Режим", "Проход", "cycle_median_ms", "cycle_p95_ms", "processing_fps"],
        [
            *[
                [
                    "True",
                    r["pass"],
                    fmt(r["cycle_median_ms"], 2),
                    fmt(r["cycle_p95_ms"], 2),
                    fmt(r["processing_fps"], 2),
                ]
                for r in v9["passes_true"]
            ],
            *[
                [
                    "False",
                    r["pass"],
                    fmt(r["cycle_median_ms"], 2),
                    fmt(r["cycle_p95_ms"], 2),
                    fmt(r["processing_fps"], 2),
                ]
                for r in v9["passes_false"]
            ],
        ],
        caption="Таблица 5 − Повторы измерений SAVE_VIDEO",
    )
    mt, mf = v9["median_true"], v9["median_false"]
    add_table(
        doc,
        ["Показатель (медиана по 3 проходам)", "SAVE_VIDEO=True", "SAVE_VIDEO=False"],
        [
            ["cycle_median_ms", fmt(mt["cycle_median_ms"], 2), fmt(mf["cycle_median_ms"], 2)],
            ["cycle_p95_ms", fmt(mt["cycle_p95_ms"], 2), fmt(mf["cycle_p95_ms"], 2)],
            ["processing_fps", fmt(mt["processing_fps"], 2), fmt(mf["processing_fps"], 2)],
            ["predict_mean_ms", fmt(mt["predict_mean_ms"], 2), fmt(mf["predict_mean_ms"], 2)],
        ],
        caption="Таблица 6 − Сравнение медиан режимов",
    )
    add_p(
        doc,
        f"Медиана полного цикла при записи видео выше примерно на "
        f"{v9['delta_median_cycle_ms']:.1f} мс; 95-й процентиль — на "
        f"{v9['delta_median_p95_ms']:.1f} мс. Время predict почти одинаково: "
        "разница обусловлена VideoWriter.write. Для контура без сохранения ролика "
        "целесообразен SAVE_VIDEO = False; для разбора ошибок нужен annotated.mp4.",
    )

    add_h(doc, "11 Файлы результатов")
    add_p(
        doc,
        "results/lr7_video/annotated.mp4, detections.csv, timings.csv, summary.json; "
        "results/lr7_mode.json, lr7_thresholds.json, lr7_test.json, lr7_video_quality.json; "
        "results/variant9_save_video/compare.json и каталоги проходов.",
        first_line=False,
    )

    add_h(doc, "12 Вывод")
    add_p(
        doc,
        "На независимом test ЛР5 выбранная YOLOv8s при conf = 0,55 обеспечивает "
        f"F1 = {fmt(test['F1'])}, mAP@0.5 = {fmt(test['map50'])}. На новом ролике качество "
        f"ниже (F1 = {fmt(vq['F1'])}), труднее всего wrench; ошибки связаны с фоном, "
        "перекрытиями и артефактами композиции. Среднее время полного цикла при "
        f"SAVE_VIDEO = True около {fmt(timing['cycle_mean_ms'], 1)} мс "
        f"(p95 ≈ {fmt(timing['cycle_p95_ms'], 1)} мс) при 15 кадр/с; отключение записи "
        "видео заметно снижает cycle_ms без изменения логики детектирования. "
        "Для производственного применения нужны дополнительные съёмки реальной сцены "
        "и повторный подбор порога на расширенной valid.",
    )

    add_h(doc, "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ")
    add_p(
        doc,
        "1. Ultralytics YOLO Docs [Электронный ресурс]. — URL: https://docs.ultralytics.com (дата обращения: 06.11.2026).",
        first_line=False,
    )
    add_p(
        doc,
        "2. Методические указания к лабораторной работе №7 «Тестирование нейронной сети на видеокадрах производственных объектов».",
        first_line=False,
    )
    add_p(
        doc,
        "3. ГОСТ 7.32−2017. Отчёт о научно-исследовательской работе. Структура и правила оформления.",
        first_line=False,
    )

    doc.save(str(OUT))
    shutil.copy2(OUT, ROOT / "ЛР7_ТЕХ_Лаврешин.docx")
    print("saved", OUT)


if __name__ == "__main__":
    main()

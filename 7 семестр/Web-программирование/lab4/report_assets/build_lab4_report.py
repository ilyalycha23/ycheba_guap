# -*- coding: utf-8 -*-
import json
import statistics
import sys
from datetime import datetime

sys.path.insert(0, r"D:\ycheba_guap\7 семестр\Web-программирование\_report_tools")
from report_lib import Report  # noqa: E402

r = Report(4, "РЕАЛИЗАЦИЯ АДАПТИВНОСТИ КЛИЕНТСКОЙ ЧАСТИ ВЕБ-ПРИЛОЖЕНИЯ")
lh = json.loads(r.read_asset("lighthouse/summary.json"))
mx = json.loads(r.read_asset("matrix.json"))

base_runs = [lh[f"baseline_{i}"] for i in (1, 2, 3)]
final_runs = [lh[f"final_{i}"] for i in (1, 2, 3)]


def med(runs, key):
    return statistics.median(run[key] for run in runs)


def fmt(v, key):
    if key in ("LCP", "TBT"):
        return f"{int(v)} мс"
    if key == "CLS":
        return f"{v:g}"
    return str(int(v))


run_date = datetime.fromisoformat(base_runs[0]["time"].replace("Z", "+00:00")).strftime("%d.%m.%Y")
browser = "Google Chrome 154.0.8037.98"

r.heading("1", "Цель работы")
r.body(
    "Реализовать адаптивную клиентскую часть веб-приложения SignalBoard на Next.js: "
    "создать гибкие макеты для галереи, модального окна, бургер-меню и карты, настроить "
    "responsive-изображения, проверить приложение на нескольких ширинах viewport, "
    "выполнить Lighthouse-аудит и документированно устранить обнаруженные проблемы."
)

r.heading("2", "Задание")
r.body(
    "Продолжить проект лабораторной работы № 3. Проверить автоматический viewport "
    "metadata в App Router, применить mobile-first подход и обоснованные контрольные "
    "точки, использовать относительные размеры, CSS Grid, Flexbox, minmax() и clamp(), "
    "исключить горизонтальную прокрутку на узких экранах, настроить свойство sizes "
    "компонента next/image, адаптировать модальное окно к ширине и динамической высоте "
    "viewport, адаптировать бургер-меню с сохранением клавиатурной доступности, "
    "обновлять размеры карты после изменения контейнера, учесть hover, тип указателя и "
    "prefers-reduced-motion. Проверить интерфейс на ширинах 320, 375, 768, 1024 и 1440 "
    "CSS px и при масштабе 200 %, выполнить по три исходных и итоговых Lighthouse-запуска "
    "production-сборки с одинаковой конфигурацией, исправить не менее трёх "
    "подтверждённых проблем и проверить npm run lint и npm run build."
)

r.heading("3", "Ход выполнения задания")
r.body(
    "Исходное состояние. После лабораторной работы № 3 приложение содержало галерею "
    "сигналов с фотографиями, модальное окно, бургер-меню и карту, но размеры были "
    "заданы преимущественно в пикселях: сетка карточек minmax(240px, 1fr), карта "
    "фиксированной высоты 480px, модальное окно ограничивалось 100dvh без учёта "
    "альбомной ориентации, hover-эффект срабатывал и на сенсорных экранах, а "
    "изображения имели общее значение sizes."
)
r.body(
    "Контрольные точки выбраны по содержимому, а не по моделям устройств. 30rem "
    "(480 px) – ширина, на которой модальному окну и карте становится тесно и нужно "
    "уменьшить отступы; 48rem (768 px) – с этой ширины в ряд помещаются две карточки "
    "минимальной ширины 16rem с отступами. Остальная перестройка выполняется без "
    "медиазапросов за счёт auto-fit, minmax() и clamp(). Базовые стили написаны для "
    "узкого экрана (mobile-first), медиазапросы min-width только добавляют возможности."
)

r.body(
    "Viewport metadata. Next.js App Router автоматически добавляет в head тег "
    "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">, поэтому "
    "вручную его писать не нужно. Масштабирование не отключено (нет maximum-scale и "
    "user-scalable=no). В layout.tsx через экспорт viewport задаются только цвет темы "
    "и цветовая схема:"
)
r.code(
    'export const viewport: Viewport = {\n'
    '  themeColor: "#eef3f8",\n'
    '  colorScheme: "light",\n'
    '};'
)

r.body(
    "Адаптивная галерея. Одна и та же разметка перестраивается от одной до трёх-четырёх "
    "колонок без дублирования JSX. Функция min(100%, 15rem) не даёт карточке стать шире "
    "экрана 320 px, aspect-ratio резервирует место изображения до загрузки:"
)
r.code(
    ".grid {\n"
    "  display: grid;\n"
    "  grid-template-columns: repeat(auto-fit, minmax(min(100%, 15rem), 1fr));\n"
    "  gap: clamp(0.9rem, 2.5vw, 1.5rem);\n"
    "}\n"
    ".imageWrap { position: relative; aspect-ratio: 3 / 2; overflow: hidden; }\n"
    "@media (hover: hover) and (pointer: fine) {\n"
    "  .card:hover { transform: translateY(-0.15rem); }\n"
    "}\n"
    "@media (min-width: 48rem) {\n"
    "  .grid { grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr)); }\n"
    "}"
)
r.body(
    "Свойство sizes сообщает браузеру реальную ширину слота изображения, чтобы из srcset "
    "выбирался подходящий файл. Для первой карточки, которая является LCP-изображением "
    "первого экрана, отключена ленивая загрузка и задан высокий приоритет:"
)
r.code(
    "<Image\n"
    "  src={signal.image}\n"
    "  alt={signal.imageAlt}\n"
    "  fill\n"
    '  sizes="(max-width: 47.99rem) calc(100vw - 2rem), (max-width: 74.99rem) 45vw, 22rem"\n'
    "  className={styles.image}\n"
    '  loading={index === 0 ? "eager" : "lazy"}\n'
    '  fetchPriority={index === 0 ? "high" : "auto"}\n'
    "/>"
)
r.body(
    "Адаптивное модальное окно помещается в динамическую высоту viewport 100dvh, "
    "которая учитывает появление и скрытие панели адреса мобильного браузера, и "
    "прокручивает длинное содержимое. Клавиатурная модель лабораторной работы № 3 "
    "сохранена:"
)
r.code(
    ".overlay { padding: clamp(0.5rem, 3vw, 1.5rem); }\n"
    ".dialog {\n"
    "  width: min(47.5rem, 100%);\n"
    "  max-height: calc(100dvh - 1rem);\n"
    "  overflow-y: auto;\n"
    "  padding: clamp(1rem, 4vw, 1.75rem);\n"
    "}\n"
    "@media (orientation: landscape) and (max-height: 32rem) {\n"
    "  .dialog { max-height: calc(100dvh - 0.5rem); }\n"
    "}"
)
r.body(
    "Адаптивное бургер-меню занимает всю высоту 100dvh, учитывает вырезы экрана через "
    "env(safe-area-inset-*) и на ширине до 30rem раскрывается на весь экран:"
)
r.code(
    ".openButton {\n"
    "  top: max(0.75rem, env(safe-area-inset-top));\n"
    "  right: max(0.75rem, env(safe-area-inset-right));\n"
    "}\n"
    ".panel {\n"
    "  width: min(26rem, 100%);\n"
    "  height: 100dvh;\n"
    "  overflow-y: auto;\n"
    "  padding: max(1rem, env(safe-area-inset-top)) max(1rem, env(safe-area-inset-right))\n"
    "    max(1rem, env(safe-area-inset-bottom)) 1rem;\n"
    "}"
)
r.body(
    "Карта. Высота контейнера задана через clamp(18rem, 58vh, 32rem), на узком экране – "
    "min(65dvh, 24rem). API Яндекс Карт само не узнаёт об изменении размеров контейнера, "
    "поэтому ResizeObserver вызывает map.container.fitToViewport(), а в cleanup "
    "наблюдатель отключается:"
)
r.code(
    "resizeObserver = new ResizeObserver(() => {\n"
    "  map?.container.fitToViewport();\n"
    "});\n"
    "resizeObserver.observe(containerRef.current);\n"
    "// cleanup\n"
    "return () => {\n"
    "  disposed = true;\n"
    "  resizeObserver?.disconnect();\n"
    "  map?.destroy();\n"
    "};"
)
r.body(
    "Режим уменьшенного движения задаётся в globals.css и отключает необязательные "
    "анимации и плавную прокрутку по системной настройке пользователя:"
)
r.code(
    "@media (prefers-reduced-motion: reduce) {\n"
    "  *, *::before, *::after {\n"
    "    scroll-behavior: auto !important;\n"
    "    animation-duration: 0.01ms !important;\n"
    "    transition-duration: 0.01ms !important;\n"
    "  }\n"
    "}"
)

r.body(
    "Ручная матрица ширин. Production-сборка открыта в браузере с viewport 320, 375, 768, "
    "1024 и 1440 CSS px; для каждого маршрута сравнивались scrollWidth и clientWidth "
    "корневого элемента и считалось число колонок сетки. Результаты приведены в таблице 1: "
    "горизонтальной прокрутки нет ни на одной ширине."
)
r.center("Таблица 1 – Ручная матрица контрольных ширин", size=12)
rows = []
for width in (320, 375, 768, 1024, 1440):
    items = [m for m in mx["matrix"] if m["width"] == width]
    gallery = next(m for m in items if m["route"] == "/gallery")
    signals = next(m for m in items if m["route"] == "/signals")
    overflow = any(m["overflow"] for m in items)
    rows.append(
        [
            f"{width} px",
            str(gallery["columns"]),
            str(signals["columns"]),
            "есть" if overflow else "нет",
            "Помещаются, фокус сохранён",
        ]
    )
r.table(["Ширина", "Колонок /gallery", "Колонок /signals", "Гориз. прокрутка", "Модальное окно, меню"], rows)

r.picture("fig_1440.png", "Галерея на ширине 1440 CSS px")
r.picture("fig_375.png", "Галерея на ширине 375 CSS px", width=7)
r.picture("fig_modal_375.png", "Модальное окно на узком экране 375 CSS px", width=7)
r.picture("fig_burger_375.png", "Открытое бургер-меню на узком экране", width=7)
r.body(
    "Карта после изменения ширины. Окно браузера было сужено с 1440 до 800 CSS px без "
    "перезагрузки. Контейнер карты изменил размер вместе с сеткой, ResizeObserver "
    "сработал и вызвал fitToViewport. Без собственного ключа API Яндекс Карт не "
    "загружается, поэтому на снимке виден контейнер и сообщение о ключе. Снимок с "
    "загруженной картой выполняется после записи ключа в .env.local."
)
r.picture("fig_map_resized.png", "Раздел карты после сужения окна до 800 CSS px")
r.placeholder(
    "Карта с метками после изменения ширины окна",
    "карта с ключом: сузить окно браузера и показать, что серых областей нет",
)
r.body(
    "Проверка масштаба 200 %. Масштаб 200 % при окне шириной 1280 px соответствует "
    f"viewport 640 CSS px. На этой ширине scrollWidth = {mx['zoom200']['scrollWidth']} и "
    f"clientWidth = {mx['zoom200']['clientWidth']}: горизонтальной прокрутки нет, текст "
    "не обрезается, кнопка меню и карточки остаются доступными."
)
r.picture("fig_zoom200.png", "Галерея при масштабе 200 %", width=12)

r.body(
    f"Конфигурация Lighthouse. Lighthouse {base_runs[0]['lh']} (тот же движок, что во "
    f"вкладке Lighthouse DevTools), браузер {browser}, дата проверки {run_date}. Режим "
    "Navigation, устройство Mobile, троттлинг simulated (по умолчанию), категории "
    "Performance, Accessibility, Best Practices и SEO, адрес "
    "http://localhost:3004/gallery. Проверялась production-сборка (npm run build и "
    "npm run start), расширения браузера не участвовали (чистый headless-профиль). "
    "Конфигурация всех шести запусков одинакова."
)
keys = ["performance", "accessibility", "best-practices", "seo", "LCP", "TBT", "CLS"]
heads = ["Запуск", "Perf.", "Access.", "Best Pr.", "SEO", "LCP", "TBT", "CLS"]
r.center("Таблица 2 – Исходные результаты Lighthouse", size=12)
r.table(
    heads,
    [[f"Исходный {i}"] + [fmt(run[k], k) for k in keys] for i, run in enumerate(base_runs, 1)]
    + [["Медиана"] + [fmt(med(base_runs, k), k) for k in keys]],
)
r.picture("fig_lh_baseline_2.png", "Исходный Lighthouse-отчёт (медианный запуск)")

r.body("Подтверждённые проблемы (failed audits), выбранные для исправления:")
r.bullets(
    [
        "aria-prohibited-attr (Accessibility) – у div-контейнера карты был атрибут "
        "aria-label без роли; для элемента без роли доступное имя запрещено и "
        "скринридер его не объявляет;",
        "lcp-lazy-loaded (Performance) – изображение первой карточки, являющееся "
        "Largest Contentful Paint, загружалось лениво (loading=\"lazy\" по умолчанию у "
        "next/image) и запрашивалось позже необходимого;",
        "lcp-discovery-insight, пункт «fetchpriority=high should be applied» "
        "(Performance) – LCP-изображению не был назначен высокий приоритет загрузки.",
    ]
)
r.body("Внесённые исправления:")
r.bullets(
    [
        "контейнеру карты добавлен role=\"region\", после чего aria-label стал "
        "допустимым и карта объявляется как именованная область;",
        "для первой карточки галереи задан loading=\"eager\", остальные карточки "
        "оставлены ленивыми – предзагрузка всех изображений конкурировала бы за сеть;",
        "для первой карточки задан fetchPriority=\"high\", остальные получают \"auto\".",
    ]
)
r.body(
    "Аудиты render-blocking-resources, unused-javascript и legacy-javascript "
    "относятся к служебным CSS- и JS-чанкам самого фреймворка Next.js, а не к коду "
    "приложения; их исправление потребовало бы изменения конфигурации сборки, поэтому "
    "они зафиксированы как известные и не исправлялись."
)
r.center("Таблица 3 – Итоговые результаты Lighthouse", size=12)
r.table(
    heads,
    [[f"Итоговый {i}"] + [fmt(run[k], k) for k in keys] for i, run in enumerate(final_runs, 1)]
    + [["Медиана"] + [fmt(med(final_runs, k), k) for k in keys]],
)
r.picture("fig_lh_final_2.png", "Итоговый Lighthouse-отчёт (медианный запуск)")

r.center("Таблица 4 – Сравнение медиан до и после исправлений", size=12)
names = {
    "performance": "Performance",
    "accessibility": "Accessibility",
    "best-practices": "Best Practices",
    "seo": "SEO",
    "LCP": "LCP",
    "TBT": "TBT",
    "CLS": "CLS",
}
r.table(
    ["Показатель", "До", "После"],
    [[names[k], fmt(med(base_runs, k), k), fmt(med(final_runs, k), k)] for k in keys],
)
r.body(
    "Accessibility вырос с 95 до 100 за счёт устранения aria-prohibited-attr. Аудиты "
    "lcp-lazy-loaded и lcp-discovery-insight перестали быть failed. Performance "
    "остался 99: приложение небольшое и работает на локальном сервере, поэтому LCP "
    "около 2,2 с определяется в основном моделью simulated-троттлинга, а разница "
    "медиан LCP и TBT между сериями находится в пределах разброса запусков. CLS равен "
    "нулю благодаря aspect-ratio у областей изображений. Регрессий функциональности "
    "нет: модальное окно, меню и карта проверены вручную после исправлений."
)
r.body(
    "Лабораторные и полевые данные. Lighthouse даёт лабораторные (lab) данные: один "
    "запуск на конкретной машине с эмуляцией устройства и сети. Полевые (field) данные "
    "собираются у реальных пользователей (например, Chrome UX Report) на разных "
    "устройствах и сетях и отражают 75-й перцентиль. Поэтому локальный аудит помогает "
    "найти и воспроизвести проблемы, но не заменяет полевые метрики; INP Lighthouse не "
    "измеряет вовсе, так как для него нужно реальное взаимодействие, и использует TBT "
    "как лабораторный индикатор отзывчивости."
)
r.body(
    "Проверка кода. Команды npm run lint и npm run build выполнены после всех "
    f"исправлений и завершились без ошибок (рисунки {r.nxt()}–{r.nxt(2)})."
)
r.picture("fig_lint.png", "Результат npm run lint", width=15)
r.picture("fig_build.png", "Результат npm run build", width=15)

r.questions(
    "4",
    [
        ("Что означает responsive web design?",
         "Подход, при котором одна страница хорошо отображается и остаётся удобной на "
         "экранах разных размеров за счёт гибкой сетки, гибких медиа и медиазапросов."),
        ("Для чего нужен viewport meta tag?",
         "Он сообщает мобильному браузеру, что ширина layout viewport равна ширине "
         "устройства, иначе страница рисуется на виртуальных 980 px и уменьшается."),
        ("Какой viewport Next.js добавляет по умолчанию?",
         "width=device-width, initial-scale=1; дополнительные поля задаются экспортом "
         "viewport из layout или page."),
        ("В чём состоит mobile-first подход?",
         "Базовые стили пишутся для узкого экрана, а медиазапросы min-width добавляют "
         "раскладку для более широких экранов."),
        ("Почему breakpoint выбирают по содержимому, а не по модели телефона?",
         "Моделей и размеров бесконечно много и они меняются; контрольная точка ставится "
         "там, где ломается конкретный макет."),
        ("Чем CSS Grid отличается от Flexbox?",
         "Grid – двумерная раскладка по строкам и колонкам одновременно, Flexbox – "
         "одномерная раскладка вдоль одной оси."),
        ("Как работают auto-fit и minmax() в сетке карточек?",
         "minmax задаёт минимальную и максимальную ширину колонки, а auto-fit создаёт "
         "столько колонок, сколько помещается, растягивая их на свободное место."),
        ("Для чего используется clamp()?",
         "Для плавного изменения размера между минимумом и максимумом в зависимости от "
         "viewport: clamp(min, preferred, max)."),
        ("Когда нужна единица dvh?",
         "Когда элемент должен занимать видимую высоту на мобильных, где панель адреса "
         "появляется и скрывается; dvh пересчитывается вместе с ней."),
        ("Что проверяют hover и pointer в media query?",
         "Есть ли у основного устройства ввода наведение и насколько он точный; это "
         "позволяет не включать hover-эффекты на сенсорных экранах."),
        ("Для чего применяется prefers-reduced-motion?",
         "Чтобы уменьшить анимации для пользователей, включивших в системе режим "
         "уменьшения движения (например, из-за вестибулярных нарушений)."),
        ("Почему Image с fill должен иметь sizes?",
         "Без sizes браузер считает, что изображение занимает 100vw, и загружает самый "
         "крупный файл из srcset."),
        ("Как aspect-ratio помогает визуальной стабильности?",
         "Резервирует место нужной пропорции до загрузки изображения, предотвращая "
         "сдвиг макета (CLS)."),
        ("Для чего карте нужен ResizeObserver?",
         "API карты не отслеживает изменения размера контейнера, ResizeObserver "
         "сообщает об этом и позволяет пересчитать область без серых полос."),
        ("Что делает map.container.fitToViewport()?",
         "Пересчитывает размеры карты по текущему размеру DOM-контейнера и "
         "дорисовывает тайлы."),
        ("Какие категории формирует Lighthouse в Chrome DevTools?",
         "Performance, Accessibility, Best Practices и SEO."),
        ("Чем Opportunities и Diagnostics отличаются от метрик Performance?",
         "Метрики (FCP, LCP, TBT, CLS, Speed Index) формируют балл; Opportunities и "
         "Diagnostics – рекомендации с оценкой экономии, которые на балл прямо не влияют."),
        ("Почему Performance score может меняться между запусками?",
         "Из-за фоновой нагрузки процессора, сети, расширений и кэша; поэтому "
         "делают несколько запусков и берут медиану."),
        ("Что измеряют LCP, INP и CLS?",
         "LCP – время отрисовки крупнейшего элемента, INP – задержку реакции на "
         "взаимодействия, CLS – суммарный неожиданный сдвиг макета."),
        ("Почему Lighthouse не измеряет INP напрямую?",
         "Lighthouse загружает страницу без действий пользователя, а INP требует "
         "реальных взаимодействий."),
        ("Для чего в лаборатории используется TBT?",
         "Total Blocking Time показывает, сколько времени основной поток был занят "
         "длинными задачами, и коррелирует с отзывчивостью (INP)."),
        ("Почему локальный Lighthouse-аудит не заменяет полевые данные?",
         "Он отражает одну машину и эмулированную сеть, а пользователи работают на "
         "разных устройствах и сетях."),
        ("Почему Accessibility score не заменяет ручную проверку?",
         "Автоматически проверяется лишь часть критериев; порядок фокуса, понятность "
         "текста и работу с клавиатурой нужно проверять вручную."),
        ("Зачем сравнивать production-сборки с одинаковой конфигурацией?",
         "Dev-режим содержит отладочный код и не оптимизирован; одинаковая конфигурация "
         "делает результаты до и после сравнимыми."),
    ],
)

r.heading("4", "Вывод")
r.body(
    "В ходе работы клиентская часть SignalBoard сделана адаптивной по принципу "
    "mobile-first: сетка карточек перестраивается через auto-fit и minmax() без "
    "дублирования разметки, размеры заданы через clamp() и относительные единицы, "
    "изображения получили корректный sizes и резерв пропорций, модальное окно и меню "
    "учитывают динамическую высоту 100dvh и безопасные области, карта пересчитывается "
    "через ResizeObserver и fitToViewport, hover включается только для точного указателя, "
    "учтён prefers-reduced-motion. Ручная проверка на пяти контрольных ширинах и при "
    "масштабе 200 % не выявила горизонтальной прокрутки. По результатам трёх исходных и "
    "трёх итоговых Lighthouse-запусков устранены три подтверждённые проблемы, медиана "
    "Accessibility выросла с 95 до 100. Проект проходит npm run lint и npm run build."
)

r.appendix(
    [
        "app/layout.tsx",
        "app/globals.css",
        "app/gallery/_components/SignalsGallery.tsx",
        "app/gallery/_components/SignalsGallery.module.css",
        "app/gallery/_components/PhotoModal.module.css",
        "app/gallery/_components/PhotoMap.tsx",
        "app/gallery/_components/PhotoMap.module.css",
        "app/ui/BurgerMenu/styles.module.css",
    ]
)
r.save()

# -*- coding: utf-8 -*-
import sys

sys.path.insert(0, r"D:\ycheba_guap\7 семестр\Web-программирование\_report_tools")
from report_lib import Report  # noqa: E402

r = Report(
    7,
    "СОЕДИНЕНИЕ И ТЕСТИРОВАНИЕ КЛИЕНТСКОЙ И СЕРВЕРНОЙ ЧАСТЕЙ ВЕБ-ПРИЛОЖЕНИЯ",
)


def src(rel: str) -> str:
    return (r.src / rel).read_text(encoding="utf-8")


def fragment(rel: str, start: str, end: str) -> str:
    text = src(rel)
    a = text.index(start)
    b = text.index(end, a) + len(end)
    return text[a:b]


r.heading("1", "Цель работы")
r.body(
    "Соединить клиентские компоненты SignalBoard с серверными Route Handlers и "
    "PostgreSQL, заменить демонстрационное состояние пользователя и отслеживания "
    "реальными запросами, реализовать состояния загрузки и ошибок, проверить "
    "HTTP-контракты и авторизацию, добавить модульные и end-to-end тесты и выполнить "
    "итоговую проверку всего приложения."
)

r.heading("2", "Задание")
r.body(
    "Определить HTTP-контракт между клиентом и сервером, реализовать GET /api/signals с "
    "преобразованием Decimal-координат и вычислением isTracked для текущего "
    "пользователя. Заменить DemoAuthProvider на AuthProvider, восстанавливать сессию "
    "через GET /api/auth/me, подключить формы регистрации, входа и выхода к API, "
    "получать галерею из PostgreSQL, реализовать loading, error и empty состояния, "
    "сохранять отслеживание через POST и DELETE, обрабатывать 400, 401, 404, 409 и 500, "
    "не доверять userId и isTracked от клиента. Сохранить модальное окно, карту, меню "
    "и адаптивность. Установить Vitest и написать модульные тесты нормализации и "
    "валидации, установить Playwright и написать сквозной сценарий регистрации и "
    "отслеживания, выполнить итоговую проверку validate, migrate status, lint, unit, "
    "build и e2e."
)

r.heading("3", "Ход выполнения задания")
r.body(
    "Схема прохождения запроса: Client Component (SignalsGallery, AuthProvider) → "
    "fetch с cookie signal_session → Route Handler app/api/.../route.ts → проверка "
    "сессии (readSession, getCurrentUser) → Prisma Client → PostgreSQL → DTO в JSON → "
    "обновление состояния React."
)
r.code(
    "Браузер (Client Components)            Next.js server               PostgreSQL\n"
    "──────────────────────────             ──────────────               ──────────\n"
    "AuthProvider    ── GET /api/auth/me ──▶ route.ts ─ getCurrentUser ─▶ User\n"
    "SignalsGallery  ── GET /api/signals ──▶ route.ts ─ prisma.findMany ─▶ NeighborSignal\n"
    "                ── POST/DELETE ───────▶ /api/favorites/[id] ───────▶ TrackedSignal\n"
    "                ◀── JSON DTO ──────────"
)
r.center("Таблица 1 – HTTP-контракты", size=12)
r.table(
    ["Метод и путь", "Тело запроса", "Успех", "Ошибки"],
    [
        ["GET /api/signals", "—", "200 {signals: NeighborSignalDTO[]}", "500"],
        ["GET /api/auth/me", "—", "200 {user: UserDTO | null}", "—"],
        ["POST /api/auth/register", "name, email, password, confirmPassword", "201 {user}", "400, 409, 500"],
        ["POST /api/auth/login", "email, password", "200 {user}", "400, 401, 500"],
        ["POST /api/auth/logout", "—", "200 {ok: true}", "—"],
        ["POST /api/favorites/{signalId}", "—", "201 {favorite}", "401, 404"],
        ["DELETE /api/favorites/{signalId}", "—", "200 {deleted}", "401"],
    ],
)
r.body(
    "UserDTO содержит только id, name и email: passwordHash, createdAt и updatedAt "
    "клиенту не нужны, а хеш пароля нельзя раскрывать. NeighborSignalDTO содержит id, "
    "slug, title, summary, category, location, image, imageAlt, latitude, longitude и "
    "isTracked. Координаты в базе имеют тип Decimal, который Prisma возвращает объектом "
    "Decimal.js; JSON.stringify превратил бы его в строку, поэтому сервер явно "
    "преобразует значения через Number(). Поле isTracked вычисляется на сервере по "
    "строкам TrackedSignal пользователя из проверенной сессии и не принимается от клиента."
)
r.body("Маршрут app/api/signals/route.ts:")
r.code(src("app/api/signals/route.ts"))
r.body(
    "AuthProvider заменил DemoAuthProvider в корневом layout. При монтировании он "
    "запрашивает GET /api/auth/me и находится в состоянии loading, пока ответ не "
    "получен: без этого интерфейс на мгновение показал бы гостя вошедшему пользователю. "
    "Cookie httpOnly недоступна JavaScript, поэтому состояние восстанавливается только "
    "запросом к серверу; браузер сам прикладывает cookie к fetch с credentials: "
    "\"same-origin\". Функции login, register и logout вызывают соответствующие маршруты "
    "и обновляют user только после успешного ответа:"
)
r.code(fragment("app/providers/AuthProvider.tsx", "  // Восстанавливаем состояние", "  }, []);\n\n  const register"))
r.body(
    "Формы входа и регистрации передают данные в AuthProvider, блокируют кнопку на "
    "время запроса и показывают сообщение сервера при ошибке:"
)
r.code(fragment("app/auth/login/page.tsx", "  async function handleSubmit", "      setPending(false);\n    }\n  }"))
r.body(
    "Загрузка галереи. SignalsGallery запрашивает /api/signals в useEffect. "
    "AbortController отменяет запрос при размонтировании или повторной загрузке, "
    "чтобы устаревший ответ не перезаписал состояние. Реализованы три состояния: "
    "loading (role=\"status\" «Загрузка сигналов…»), error (role=\"alert\" с кнопкой "
    "«Повторить») и empty («Сигналы пока не добавлены.»). Loading означает, что ответа "
    "ещё нет, empty – что ответ получен, но массив пуст."
)
r.code(fragment("app/gallery/_components/SignalsGallery.tsx", "  useEffect(() => {\n    const controller", "  }, [reloadKey, status]);"))
r.body(
    "Переключение отслеживания выполняется пессимистично: интерфейс меняет карточку "
    "только после того, как сервер подтвердил POST или DELETE. При ответе 401 "
    "AuthProvider обновляется и пользователь видит сообщение о завершении сеанса. "
    "userId в запрос не передаётся – сервер берёт его из подписанной сессии:"
)
r.code(fragment("app/gallery/_components/SignalsGallery.tsx", "  async function toggleTracked", "      setPendingId(null);\n    }\n  }"))

r.body(
    "Обработка ошибки сервера на клиенте проверена при недоступной базе данных: "
    f"GET /api/signals вернул 500 без раскрытия деталей подключения (рисунок {r.nxt()}), "
    f"а галерея показала состояние ошибки с кнопкой «Повторить» (рисунок {r.nxt(2)})."
)
r.picture("fig_http_guest.png", "HTTP-ответы API без входа и без базы данных", width=15)
r.picture("fig_gallery_error.png", "Состояние error галереи при ответе 500")
r.placeholder(
    "Галерея с данными из PostgreSQL после входа",
    "/gallery после входа neighbor@example.test – карточки с кнопками «Добавить в отслеживание»",
)
r.placeholder(
    "Сохранение отслеживания после перезагрузки",
    "отметить сигнал, нажать F5 – кнопка «Удалить из отслеживания» осталась",
)
r.placeholder(
    "Вкладка Network без секретов",
    "DevTools → Network: GET /api/signals 200 и POST /api/favorites/{id} 201; Response без passwordHash",
)
r.placeholder(
    "SQL-проверка TrackedSignal",
    "psql: SELECT u.email, s.slug FROM \"TrackedSignal\" t JOIN \"User\" u ON u.id=t.\"userId\" JOIN \"NeighborSignal\" s ON s.id=t.\"signalId\";",
)

r.center("Таблица 2 – Матрица ручных сценариев", size=12)
r.table(
    ["Сценарий", "Ожидаемый результат", "Статус"],
    [
        ["Гость открывает /gallery", "Карточки и ссылка «Войдите, чтобы отслеживать сигнал»", "[[проверить с БД]]"],
        ["База недоступна", "500 и состояние error с кнопкой «Повторить»", "Проверено"],
        ["Гость: POST /api/favorites/{id}", "401", "Проверено"],
        ["Поддельная cookie", "401", "Проверено"],
        ["Регистрация с ошибками полей", "400 и сообщение в форме", "Проверено (API)"],
        ["Регистрация занятого email", "409 «Этот email уже зарегистрирован»", "[[проверить с БД]]"],
        ["Вход с неверным паролем", "401 «Неверный email или пароль»", "[[проверить с БД]]"],
        ["Вход seed-пользователя", "Переход в /gallery, имя в меню", "[[проверить с БД]]"],
        ["Отслеживание и reload", "Состояние сохраняется после F5", "[[проверить с БД]]"],
        ["Выход", "Cookie удалена, интерфейс гостя", "Проверено (API)"],
    ],
)

r.body(
    "Модульные тесты. Vitest настроен на окружение node и каталог tests/unit; "
    "плагин vite-tsconfig-paths подключает алиас @/. Тесты проверяют чистые функции "
    "normalizeEmail и validateRegistration и не требуют базы данных:"
)
r.code(src("vitest.config.mts"))
r.code(src("tests/unit/validation.test.ts"))
r.picture("fig_unit.png", "Результат npm run test:unit: 4 теста пройдены", width=15)

r.body(
    "End-to-end тест. Playwright запускает production-сервер (npm run start) через "
    "webServer и открывает страницы по baseURL. Используется один worker, потому что "
    "все тесты работают с одной локальной базой. Сценарий регистрирует пользователя с "
    "уникальным email вида e2e-<время>@example.test, добавляет сигнал в отслеживание, "
    "перезагружает страницу и проверяет, что состояние прочитано из PostgreSQL, затем "
    "выходит. В afterAll созданный пользователь удаляется, а его строки TrackedSignal "
    "удаляются каскадно, поэтому повторный запуск не накапливает тестовые данные."
)
r.code(src("playwright.config.ts"))
r.code(src("tests/e2e/auth-and-favorites.spec.ts"))

r.body(
    "Итоговая проверка. Команды, не требующие базы данных, выполнены: prisma validate "
    "– схема валидна, npm run lint – без ошибок, npm run test:unit – 4 из 4, npm run "
    f"build – успешно (рисунки {r.nxt()}–{r.nxt(2)}). Команды prisma migrate status и "
    "npm run test:e2e выполняются при запущенном PostgreSQL."
)
r.picture("fig_lint.png", "Результат npm run lint", width=15)
r.picture("fig_build.png", "Результат npm run build", width=15)
r.placeholder(
    "Результат prisma migrate status",
    "npm run db:status – «Database schema is up to date!»",
)
r.placeholder(
    "Результат npm run test:e2e",
    "после npm run build: «1 passed»",
)
r.body(
    "Повторная ручная проверка ЛР3–ЛР4 на production-сборке ЛР7: на ширинах 320, 375, "
    "768, 1024 и 1440 CSS px маршруты /start, /gallery, /auth/login и /auth/register "
    "не имеют горизонтальной прокрутки; бургер-меню открывается, закрывается клавишей "
    "Escape и автоматически закрывается после перехода по ссылке (рисунок "
    f"{r.nxt()}). Модальное окно и карта используют данные из API и проверяются после "
    "запуска базы."
)
r.picture("fig_burger_375.png", "Бургер-меню ЛР7 на ширине 375 CSS px", width=7)

r.questions(
    "4",
    [
        ("Как проходит запрос от Client Component до PostgreSQL?",
         "Компонент вызывает fetch, браузер прикладывает cookie, Route Handler "
         "проверяет сессию, через Prisma Client выполняет SQL в PostgreSQL и "
         "возвращает DTO в JSON, по которому компонент обновляет состояние."),
        ("Что такое HTTP-контракт?",
         "Соглашение о методе, пути, формате тела запроса и ответа и кодах статуса, "
         "на которое опираются клиент и сервер."),
        ("Где располагается Route Handler в App Router?",
         "В файле route.ts внутри каталога app, путь каталога задаёт URL, например "
         "app/api/signals/route.ts → /api/signals."),
        ("Какие HTTP-методы поддерживает route.ts?",
         "GET, POST, PUT, PATCH, DELETE, HEAD и OPTIONS – по экспортируемой функции "
         "с именем метода."),
        ("Почему response.ok нужно проверять вручную?",
         "fetch отклоняет Promise только при сетевой ошибке; ответы 4xx и 5xx считаются "
         "успешно полученными."),
        ("Что такое DTO?",
         "Data Transfer Object – явно сформированный объект для передачи по сети, "
         "содержащий только нужные клиенту поля."),
        ("Почему UserDTO не должен повторять всю строку User?",
         "Строка содержит passwordHash и служебные поля; их передача небезопасна и "
         "привязывает клиент к структуре таблицы."),
        ("Зачем Decimal преобразуется перед JSON?",
         "Prisma возвращает Decimal-объект, который сериализуется строкой; карте нужны "
         "числа."),
        ("Где вычисляется isFavorite и почему?",
         "На сервере по пользователю из проверенной сессии: значению от клиента "
         "доверять нельзя. В SignalBoard это isTracked."),
        ("Как httpOnly cookie участвует в fetch-запросе?",
         "Браузер автоматически прикладывает её к запросам того же источника "
         "(credentials: \"same-origin\"), но JavaScript прочитать её не может."),
        ("Чем loading отличается от empty?",
         "loading – ответ ещё не получен; empty – ответ получен, но данных нет."),
        ("Для чего нужен AbortController?",
         "Для отмены незавершённого запроса при размонтировании или повторной загрузке, "
         "чтобы устаревший ответ не обновил состояние."),
        ("Почему AuthProvider имеет состояние loading?",
         "Пока ответ /api/auth/me не пришёл, неизвестно, гость ли пользователь; без "
         "loading интерфейс мигал бы гостевым видом."),
        ("Чем пессимистичное обновление отличается от оптимистичного?",
         "Пессимистичное меняет интерфейс после подтверждения сервера, оптимистичное – "
         "сразу, с откатом при ошибке."),
        ("Почему userId нельзя принимать от клиента для избранного?",
         "Клиент может подставить чужой id; сервер берёт пользователя только из "
         "подписанной сессии."),
        ("Чем unit test отличается от integration и E2E?",
         "Unit проверяет отдельную функцию изолированно, integration – взаимодействие "
         "нескольких модулей, E2E – весь сценарий через браузер и реальный сервер."),
        ("Почему async Server Components удобнее проверять E2E?",
         "Они выполняются на сервере вместе с данными и окружением Next.js, которые "
         "сложно воспроизвести в unit-тесте."),
        ("Что проверяет Vitest в этой работе?",
         "Нормализацию email и правила validateRegistration без базы и браузера."),
        ("Что проверяет Playwright?",
         "Сквозной сценарий: регистрация, cookie-сессия, добавление в отслеживание и "
         "сохранение после перезагрузки."),
        ("Для чего нужны baseURL и webServer?",
         "baseURL позволяет писать относительные пути, webServer запускает и ожидает "
         "сервер приложения перед тестами."),
        ("Почему E2E выполняется после production build?",
         "Проверяется именно та сборка, которая будет развёрнута, без особенностей "
         "dev-режима."),
        ("Почему выбран один worker?",
         "Тесты используют одну локальную базу; параллельные worker могли бы мешать "
         "друг другу."),
        ("Зачем тесту уникальный email?",
         "Чтобы повторный запуск не упал с 409 из-за пользователя предыдущего запуска."),
        ("Почему тестовые данные нужно удалять?",
         "Чтобы база не засорялась и тесты оставались независимыми и повторяемыми."),
        ("Почему waitForTimeout является плохой синхронизацией?",
         "Фиксированная пауза либо слишком коротка (нестабильный тест), либо слишком "
         "длинна; нужно ждать конкретного состояния через expect."),
        ("Какие проверки остаются ручными?",
         "Клавиатурная навигация, масштаб 200 %, визуальная адаптивность, работа карты "
         "и понятность сообщений."),
        ("Почему проходящие тесты не доказывают полную безопасность?",
         "Тесты покрывают только описанные сценарии и не находят непредусмотренные "
         "уязвимости."),
    ],
)

r.heading("4", "Вывод")
r.body(
    "В ходе работы клиентская часть SignalBoard соединена с серверной: галерея получает "
    "сигналы из PostgreSQL через GET /api/signals, AuthProvider восстанавливает сессию "
    "из httpOnly-cookie через /api/auth/me, формы входа и регистрации работают через "
    "API, отслеживание сохраняется POST и DELETE с серверной проверкой пользователя. "
    "Реализованы состояния loading, error и empty, отмена запросов AbortController и "
    "обработка 400, 401, 404, 409 и 500. Модульные тесты Vitest проверяют валидацию "
    "независимо от базы, сценарий Playwright проверяет регистрацию и сохранение "
    "отслеживания на production-сборке и удаляет тестовые данные."
)
r.body(
    "Итог по курсу. За семь лабораторных работ SignalBoard прошёл путь от каркаса "
    "Next.js до полноценного приложения: маршрутизация App Router, интерактивная "
    "клиентская часть с доступными диалогами и картой, адаптивная вёрстка с проверкой "
    "Lighthouse, реляционная база PostgreSQL с Prisma, серверная авторизация с "
    "хешированием паролей и подписанной сессией, соединение клиента с API и "
    "автоматическое тестирование."
)

r.appendix(
    [
        "app/api/signals/route.ts",
        "app/providers/AuthProvider.tsx",
        "app/auth/login/page.tsx",
        "app/auth/register/page.tsx",
        "app/gallery/_components/SignalsGallery.tsx",
        "app/layout.tsx",
        "vitest.config.mts",
        "tests/unit/validation.test.ts",
        "playwright.config.ts",
        "tests/e2e/auth-and-favorites.spec.ts",
    ]
)
r.save()

# ⚡ Web-программирование

> Полноценный веб-проект **Signalboard** на современном стеке. Каждая лаба — следующий этап одного приложения.

## 📦 Содержимое

| Папка | Этап |
|-------|------|
| 🧪 `lab1` … `lab7` | Итерации Signalboard + отчёты |

В каждой лабе:

```
labN/
├── signalboard/          # код приложения
├── ЛР*_Веб_Лаврешин.pdf  # отчёт
└── …задание…             # методичка (где есть)
```

## 🛠 Стек (Signalboard)

| Технология | Роль |
|------------|------|
| ⚛️ **Next.js** (App Router) | фреймворк |
| 💙 **React** + **TypeScript** | UI |
| 🗃 **Prisma** | ORM / миграции |
| ✅ **Vitest** + **Playwright** | unit и e2e |

Полезные скрипты:

```bash
npm run dev          # 🔥 разработка
npm run db:migrate   # 🗄 миграции Prisma
npm run test:unit    # 🧪 unit-тесты
npm run test:e2e     # 🎭 e2e
npm run check:final  # 🚀 lint + тесты + build
```

---

## 🧭 Навигация

← [7️⃣ 7 семестр](../README.md)

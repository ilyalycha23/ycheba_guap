// Идемпотентно заполняет локальную development-базу учебными данными.

import "dotenv/config";
import { PrismaClient } from "@prisma/client";
import { hash } from "bcrypt";

// Для отдельного seed-процесса создаём собственный клиент.
const prisma = new PrismaClient();

// Описываем те же три сигнала, которые использовались в клиентской ЛР3.
const signals = [
  {
    slug: "lost-keys",
    title: "Ищу ключи от подъезда",
    summary:
      "Потерял связку ключей у детской площадки во дворе дома на Плесецкой 16 вечером, нужна помощь соседей.",
    category: "ищу",
    location: "Плесецкая ул., 16 — двор, детская площадка",
    image: "/images/places/lost-keys.jpg",
    imageAlt: "Детская площадка во дворе дома на Плесецкой 16",
    latitude: "60.036100",
    longitude: "30.221450",
  },
  {
    slug: "give-chair",
    title: "Отдаю офисный стул",
    summary:
      "Отдаю исправный стул самовывозом из второго подъезда дома на Плесецкой 16, забирать сегодня-завтра.",
    category: "отдаю",
    location: "Плесецкая ул., 16 — второй подъезд, 1 этаж",
    image: "/images/places/give-chair.jpg",
    imageAlt: "Офисный стул у входа во второй подъезд дома на Плесецкой 16",
    latitude: "60.035820",
    longitude: "30.222050",
  },
  {
    slug: "water-outage",
    title: "Отключение воды в доме",
    summary:
      "УК предупредила: завтра с 10:00 до 16:00 не будет холодной воды по всему стояку в доме на Плесецкой 16.",
    category: "предупреждаю",
    location: "Плесецкая ул., 16 — весь дом, стояк ХВС",
    image: "/images/places/water-outage.jpg",
    imageAlt: "Технический стояк холодной воды в подъезде дома на Плесецкой 16",
    latitude: "60.035620",
    longitude: "30.221350",
  },
];

async function main() {
  // Хешируем только демонстрационный пароль локальной development-базы.
  const passwordHash = await hash("12345678", 12);

  // Создаём или обновляем одного демонстрационного пользователя.
  const user = await prisma.user.upsert({
    where: { email: "neighbor@example.test" },
    update: {
      name: "Демонстрационный сосед",
      passwordHash,
    },
    create: {
      name: "Демонстрационный сосед",
      email: "neighbor@example.test",
      passwordHash,
    },
  });

  // Создаём или обновляем каждый сигнал по уникальному slug.
  for (const signal of signals) {
    await prisma.neighborSignal.upsert({
      where: { slug: signal.slug },
      update: signal,
      create: signal,
    });
  }

  // Находим сигнал про ключи, чтобы создать демонстрационную связь отслеживания.
  const lostKeys = await prisma.neighborSignal.findUniqueOrThrow({
    where: { slug: "lost-keys" },
  });

  // Upsert составного ключа не создаёт дубликат при повторном seed.
  await prisma.trackedSignal.upsert({
    where: {
      userId_signalId: {
        userId: user.id,
        signalId: lostKeys.id,
      },
    },
    update: {},
    create: {
      userId: user.id,
      signalId: lostKeys.id,
    },
  });

  // Выводим проверяемый итог без пароля и хеша.
  console.log("Seed complete: 1 user, 3 signals, 1 tracked");
}

main()
  .catch((error) => {
    console.error("Seed failed:", error);
    process.exitCode = 1;
  })
  .finally(async () => {
    // Закрываем соединения отдельного seed-процесса.
    await prisma.$disconnect();
  });

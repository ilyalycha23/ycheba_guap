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
    summary: "Потерял связку ключей у детской площадки вечером, нужна помощь соседей.",
    category: "ищу",
    location: "Двор дома, детская площадка",
    image: "/images/places/lost-keys.jpg",
    imageAlt: "Детская площадка во дворе, где были потеряны ключи",
    latitude: "59.931800",
    longitude: "30.298500",
  },
  {
    slug: "give-chair",
    title: "Отдаю офисный стул",
    summary: "Отдаю исправный стул самовывозом из второго подъезда, забирать сегодня-завтра.",
    category: "отдаю",
    location: "Второй подъезд, площадка 1 этажа",
    image: "/images/places/give-chair.jpg",
    imageAlt: "Офисный стул у входа во второй подъезд",
    latitude: "59.932600",
    longitude: "30.301200",
  },
  {
    slug: "water-outage",
    title: "Отключение воды в доме",
    summary: "УК предупредила: завтра с 10:00 до 16:00 не будет холодной воды по всему стояку.",
    category: "предупреждаю",
    location: "Весь дом, стояк холодной воды",
    image: "/images/places/water-outage.jpg",
    imageAlt: "Технический стояк холодной воды в подъезде",
    latitude: "59.933400",
    longitude: "30.296800",
  },
];

async function main() {
  // Хешируем только демонстрационный пароль локальной development-базы.
  const passwordHash = await hash("SignalPass_2026!", 12);

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

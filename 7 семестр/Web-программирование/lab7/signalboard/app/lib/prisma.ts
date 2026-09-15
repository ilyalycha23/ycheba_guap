// Создаёт единый серверный экземпляр PrismaClient для Next.js.

import { PrismaClient } from "@prisma/client";

// Расширяем тип globalThis полем, используемым только в development.
const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

// Переиспользуем клиент после горячей перезагрузки или создаём его впервые.
export const prisma = globalForPrisma.prisma ?? new PrismaClient();

// Сохраняем экземпляр глобально только вне production.
if (process.env.NODE_ENV !== "production") {
  globalForPrisma.prisma = prisma;
}

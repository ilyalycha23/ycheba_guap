// Проверяет соединение Prisma с PostgreSQL без создания предметных таблиц.

import "dotenv/config";
import { prisma } from "../app/lib/prisma";

// Описываем форму строки, которую возвращает диагностический SELECT.
type ConnectionInfo = {
  database: string;
  role: string;
  port: number;
};

async function main() {
  // Запрашиваем у сервера фактические параметры текущего соединения.
  const rows = await prisma.$queryRaw<ConnectionInfo[]>`
    SELECT
      current_database() AS database,
      current_user AS role,
      inet_server_port() AS port
  `;

  // Выводим только безопасные диагностические сведения, без DATABASE_URL.
  console.log("Prisma connected:", rows[0]);
}

// Завершаем процесс с ненулевым кодом при ошибке подключения.
main()
  .catch((error) => {
    console.error("Prisma connection failed:", error);
    process.exitCode = 1;
  })
  .finally(async () => {
    // Освобождаем ресурсы отдельного диагностического скрипта.
    await prisma.$disconnect();
  });

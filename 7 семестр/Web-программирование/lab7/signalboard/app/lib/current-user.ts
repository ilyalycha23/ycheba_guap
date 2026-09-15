// Проверяет сессию и загружает актуального пользователя из базы.

import { prisma } from "./prisma";
import { readSession } from "./auth";

export async function getCurrentUser() {
  // Сначала проверяем подписанный идентификатор сессии.
  const session = await readSession();
  if (!session) return null;

  // Затем убеждаемся, что пользователь всё ещё существует в базе.
  return prisma.user.findUnique({
    where: { id: session.userId },
    select: {
      id: true,
      name: true,
      email: true,
    },
  });
}

// Защищает добавление и удаление отслеживания серверной проверкой пользователя.

import { NextResponse } from "next/server";
import { getCurrentUser } from "@/app/lib/current-user";
import { prisma } from "@/app/lib/prisma";

type RouteParams = {
  params: Promise<{ signalId: string }>;
};

export async function POST(_request: Request, context: RouteParams) {
  // Авторизуем действие рядом с изменением данных.
  const user = await getCurrentUser();
  if (!user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { signalId } = await context.params;

  // Не создаём связь с отсутствующим сигналом.
  const signal = await prisma.neighborSignal.findUnique({
    where: { id: signalId },
    select: { id: true },
  });
  if (!signal) {
    return NextResponse.json({ error: "Signal not found" }, { status: 404 });
  }

  // Upsert делает повторный POST идемпотентным для одной пары ключей.
  const favorite = await prisma.trackedSignal.upsert({
    where: { userId_signalId: { userId: user.id, signalId } },
    update: {},
    create: { userId: user.id, signalId },
  });

  return NextResponse.json({ favorite }, { status: 201 });
}

export async function DELETE(_request: Request, context: RouteParams) {
  // Гость не может изменять строки TrackedSignal.
  const user = await getCurrentUser();
  if (!user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { signalId } = await context.params;

  // Удаляем только связь пользователя, полученного из проверенной сессии.
  const result = await prisma.trackedSignal.deleteMany({
    where: { userId: user.id, signalId },
  });

  return NextResponse.json({ deleted: result.count });
}

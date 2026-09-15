// Возвращает локальные сигналы и персональное состояние отслеживания.

import { NextResponse } from "next/server";
import { getCurrentUser } from "@/app/lib/current-user";
import { prisma } from "@/app/lib/prisma";

// Ответ зависит от cookie текущего запроса и не является общим кэшем.
export const dynamic = "force-dynamic";

export async function GET() {
  try {
    // Гость получает сигналы без персональных связей.
    const user = await getCurrentUser();

    // Читаем предметные данные и только нужные tracked signalId.
    const [signals, tracked] = await Promise.all([
      prisma.neighborSignal.findMany({ orderBy: { title: "asc" } }),
      user
        ? prisma.trackedSignal.findMany({
            where: { userId: user.id },
            select: { signalId: true },
          })
        : Promise.resolve([]),
    ]);

    // Set обеспечивает быструю проверку каждого сигнала.
    const trackedIds = new Set(tracked.map((item) => item.signalId));

    // Формируем стабильный DTO без внутренних временных полей.
    const result = signals.map((signal) => ({
      id: signal.id,
      slug: signal.slug,
      title: signal.title,
      summary: signal.summary,
      category: signal.category,
      location: signal.location,
      image: signal.image,
      imageAlt: signal.imageAlt,
      latitude: Number(signal.latitude),
      longitude: Number(signal.longitude),
      isTracked: trackedIds.has(signal.id),
    }));

    return NextResponse.json({ signals: result });
  } catch {
    // Не раскрываем клиенту объект ошибки подключения или DATABASE_URL.
    return NextResponse.json(
      { error: "Не удалось загрузить сигналы" },
      { status: 500 },
    );
  }
}

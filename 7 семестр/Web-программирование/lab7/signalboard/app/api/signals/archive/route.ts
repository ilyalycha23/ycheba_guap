import { NextResponse } from "next/server";
import { getCurrentUser } from "@/app/lib/current-user";
import { prisma } from "@/app/lib/prisma";
import { signalAuthorSelect, toSignalDto } from "@/app/lib/signal-dto";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export async function GET() {
  const current = await getCurrentUser();
  if (!current) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  try {
    const signals = await prisma.neighborSignal.findMany({
      where: {
        archivedAt: { not: null },
        authorId: current.id,
      },
      orderBy: { archivedAt: "desc" },
      include: { author: { select: signalAuthorSelect } },
    });

    return NextResponse.json({
      signals: signals.map((signal) => toSignalDto(signal, new Set(), current.id)),
    });
  } catch {
    return NextResponse.json(
      { error: "Не удалось загрузить архив" },
      { status: 500 },
    );
  }
}

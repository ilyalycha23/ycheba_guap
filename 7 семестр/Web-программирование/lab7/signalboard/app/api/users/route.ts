import { NextResponse } from "next/server";
import { resolveAvatarUrl } from "@/app/lib/avatar";
import { prisma } from "@/app/lib/prisma";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const users = await prisma.user.findMany({
      orderBy: { name: "asc" },
      select: {
        id: true,
        name: true,
        gender: true,
        avatarUrl: true,
      },
    });

    return NextResponse.json({
      users: users.map((user) => ({
        id: user.id,
        name: user.name,
        gender: user.gender,
        avatarUrl: resolveAvatarUrl(user.avatarUrl, user.gender),
        hasCustomAvatar: Boolean(user.avatarUrl),
      })),
    });
  } catch {
    return NextResponse.json(
      { error: "Не удалось загрузить пользователей" },
      { status: 500 },
    );
  }
}

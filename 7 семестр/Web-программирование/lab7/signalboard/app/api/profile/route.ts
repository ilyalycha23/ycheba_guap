import { NextResponse } from "next/server";
import { createSession } from "@/app/lib/auth";
import { normalizeGender } from "@/app/lib/avatar";
import { getCurrentUser } from "@/app/lib/current-user";
import { prisma } from "@/app/lib/prisma";

export const runtime = "nodejs";

export async function PATCH(request: Request) {
  const current = await getCurrentUser();
  if (!current) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = (await request.json().catch(() => null)) as
    | { name?: unknown; gender?: unknown }
    | null;

  const data: { name?: string; gender?: "male" | "female" } = {};

  if (body && "name" in body) {
    const name = String(body.name ?? "").trim();
    if (name.length < 2 || name.length > 80) {
      return NextResponse.json(
        { errors: ["Имя должно содержать от 2 до 80 символов"] },
        { status: 400 },
      );
    }
    data.name = name;
  }

  if (body && "gender" in body) {
    const gender = normalizeGender(body.gender);
    if (!gender) {
      return NextResponse.json(
        { errors: ["Укажите пол: мужской или женский"] },
        { status: 400 },
      );
    }
    data.gender = gender;
  }

  if (Object.keys(data).length === 0) {
    return NextResponse.json(
      { errors: ["Нет данных для обновления"] },
      { status: 400 },
    );
  }

  const user = await prisma.user.update({
    where: { id: current.id },
    data,
    select: { id: true, name: true, email: true, gender: true, avatarUrl: true },
  });

  if (data.name) {
    await createSession({ userId: user.id, name: user.name });
  }

  return NextResponse.json({ user });
}

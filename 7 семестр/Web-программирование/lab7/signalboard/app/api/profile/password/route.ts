import { compare, hash } from "bcrypt";
import { NextResponse } from "next/server";
import { getCurrentUser } from "@/app/lib/current-user";
import { prisma } from "@/app/lib/prisma";

export const runtime = "nodejs";

const HISTORY_LIMIT = 5;

export async function POST(request: Request) {
  const current = await getCurrentUser();
  if (!current) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = (await request.json().catch(() => null)) as
    | {
        currentPassword?: unknown;
        newPassword?: unknown;
        confirmPassword?: unknown;
      }
    | null;

  const currentPassword = String(body?.currentPassword ?? "");
  const newPassword = String(body?.newPassword ?? "");
  const confirmPassword = String(body?.confirmPassword ?? "");

  if (newPassword.length < 8) {
    return NextResponse.json(
      { errors: ["Новый пароль должен содержать не менее 8 символов"] },
      { status: 400 },
    );
  }

  if (newPassword !== confirmPassword) {
    return NextResponse.json(
      { errors: ["Пароли не совпадают"] },
      { status: 400 },
    );
  }

  const account = await prisma.user.findUnique({
    where: { id: current.id },
    select: {
      passwordHash: true,
      passwordHistory: {
        orderBy: { createdAt: "desc" },
        select: { id: true, passwordHash: true },
      },
    },
  });

  if (!account || !(await compare(currentPassword, account.passwordHash))) {
    return NextResponse.json(
      { errors: ["Неверный текущий пароль"] },
      { status: 401 },
    );
  }

  if (await compare(newPassword, account.passwordHash)) {
    return NextResponse.json(
      { errors: ["Новый пароль должен отличаться от текущего"] },
      { status: 400 },
    );
  }

  for (const entry of account.passwordHistory) {
    if (await compare(newPassword, entry.passwordHash)) {
      return NextResponse.json(
        { errors: ["Этот пароль уже использовался ранее. Выберите другой"] },
        { status: 400 },
      );
    }
  }

  const nextHash = await hash(newPassword, 12);
  const overflowIds = account.passwordHistory
    .slice(HISTORY_LIMIT - 1)
    .map((entry) => entry.id);

  await prisma.$transaction(async (tx) => {
    await tx.passwordHistory.create({
      data: {
        userId: current.id,
        passwordHash: account.passwordHash,
      },
    });

    if (overflowIds.length > 0) {
      await tx.passwordHistory.deleteMany({
        where: { id: { in: overflowIds } },
      });
    }

    await tx.user.update({
      where: { id: current.id },
      data: { passwordHash: nextHash },
    });
  });

  return NextResponse.json({ ok: true });
}

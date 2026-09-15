// Проверяет email и пароль, затем создаёт сессию пользователя.

import { compare } from "bcrypt";
import { NextResponse } from "next/server";
import { createSession } from "@/app/lib/auth";
import { prisma } from "@/app/lib/prisma";
import { normalizeEmail } from "@/app/lib/validation";

export const runtime = "nodejs";

export async function POST(request: Request) {
  try {
    // Нормализуем email и приводим пароль к строке.
    const body = (await request.json()) as Record<string, unknown>;
    const email = normalizeEmail(body.email);
    const password = String(body.password ?? "");

    if (!email || !password) {
      return NextResponse.json(
        { errors: ["Заполните email и пароль"] },
        { status: 400 },
      );
    }

    // Для проверки пароля временно загружаем passwordHash только на сервере.
    const account = await prisma.user.findUnique({ where: { email } });

    // Используем одно сообщение для отсутствующего аккаунта и неверного пароля.
    if (!account || !(await compare(password, account.passwordHash))) {
      return NextResponse.json(
        { errors: ["Неверный email или пароль"] },
        { status: 401 },
      );
    }

    // Создаём подписанную сессию после успешной проверки.
    await createSession({ userId: account.id, name: account.name });

    // Явно формируем DTO без passwordHash.
    const user = {
      id: account.id,
      name: account.name,
      email: account.email,
    };

    return NextResponse.json({ user });
  } catch {
    return NextResponse.json(
      { errors: ["Внутренняя ошибка сервера"] },
      { status: 500 },
    );
  }
}

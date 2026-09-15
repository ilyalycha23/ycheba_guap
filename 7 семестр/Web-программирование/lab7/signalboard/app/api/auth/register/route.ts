// Регистрирует пользователя, хеширует пароль и создаёт cookie-сессию.

import { Prisma } from "@prisma/client";
import { hash } from "bcrypt";
import { NextResponse } from "next/server";
import { createSession } from "@/app/lib/auth";
import { prisma } from "@/app/lib/prisma";
import { validateRegistration } from "@/app/lib/validation";

export const runtime = "nodejs";

export async function POST(request: Request) {
  try {
    // Читаем непроверенное тело запроса.
    const body = await request.json();
    const validation = validateRegistration(body);

    // Возвращаем ошибки клиента без обращения к базе.
    if (!validation.data) {
      return NextResponse.json(
        { errors: validation.errors },
        { status: 400 },
      );
    }

    const { name, email, password } = validation.data;

    // Хешируем пароль до записи строки User.
    const passwordHash = await hash(password, 12);

    // Создаём пользователя и сразу выбираем только безопасные поля.
    const user = await prisma.user.create({
      data: { name, email, passwordHash },
      select: { id: true, name: true, email: true },
    });

    // Сохраняем минимальные данные в подписанной cookie-сессии.
    await createSession({ userId: user.id, name: user.name });

    return NextResponse.json({ user }, { status: 201 });
  } catch (error) {
    // Преобразуем конфликт уникального email в согласованный HTTP 409.
    if (
      error instanceof Prisma.PrismaClientKnownRequestError &&
      error.code === "P2002"
    ) {
      return NextResponse.json(
        { errors: ["Этот email уже зарегистрирован"] },
        { status: 409 },
      );
    }

    // Не отправляем клиенту внутренний объект ошибки или секреты.
    return NextResponse.json(
      { errors: ["Внутренняя ошибка сервера"] },
      { status: 500 },
    );
  }
}

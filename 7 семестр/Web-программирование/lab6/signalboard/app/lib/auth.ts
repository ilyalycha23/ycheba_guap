// Подписывает, проверяет, устанавливает и удаляет учебную cookie-сессию.

import { SignJWT, jwtVerify } from "jose";
import { cookies } from "next/headers";

const COOKIE_NAME = "signal_session";
const SESSION_MAX_AGE = 60 * 60 * 24 * 7;

// Читаем серверный секрет и сразу запрещаем запуск с пустым значением.
function getSecret(): Uint8Array {
  const value = process.env.AUTH_SECRET;
  if (!value) {
    throw new Error("AUTH_SECRET is not configured");
  }
  return new TextEncoder().encode(value);
}

// Храним в сессии только минимальные данные пользователя.
export type SessionPayload = {
  userId: string;
  name: string;
};

// Создаём подписанный JWT с ограниченным сроком действия.
async function signSession(payload: SessionPayload): Promise<string> {
  return new SignJWT(payload)
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime("7d")
    .sign(getSecret());
}

// Устанавливаем cookie только из серверного Route Handler.
export async function createSession(payload: SessionPayload): Promise<void> {
  const token = await signSession(payload);
  const store = await cookies();

  store.set(COOKIE_NAME, token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    path: "/",
    maxAge: SESSION_MAX_AGE,
  });
}

// Возвращаем payload только после успешной проверки подписи и срока.
export async function readSession(): Promise<SessionPayload | null> {
  const token = (await cookies()).get(COOKIE_NAME)?.value;
  if (!token) return null;

  try {
    const { payload } = await jwtVerify(token, getSecret(), {
      algorithms: ["HS256"],
    });

    if (typeof payload.userId !== "string" || typeof payload.name !== "string") {
      return null;
    }

    return { userId: payload.userId, name: payload.name };
  } catch {
    // Любая ошибка подписи, формата или срока превращает запрос в гостевой.
    return null;
  }
}

// Удаляем cookie при выходе пользователя.
export async function deleteSession(): Promise<void> {
  (await cookies()).delete(COOKIE_NAME);
}

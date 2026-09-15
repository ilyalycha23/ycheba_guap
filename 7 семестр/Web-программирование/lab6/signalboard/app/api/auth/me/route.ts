// Возвращает безопасные данные текущего пользователя или null для гостя.

import { NextResponse } from "next/server";
import { getCurrentUser } from "@/app/lib/current-user";

export async function GET() {
  const user = await getCurrentUser();
  return NextResponse.json({ user });
}

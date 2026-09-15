// Завершает stateless-сессию удалением cookie в браузере.

import { NextResponse } from "next/server";
import { deleteSession } from "@/app/lib/auth";

export async function POST() {
  await deleteSession();
  return NextResponse.json({ ok: true });
}

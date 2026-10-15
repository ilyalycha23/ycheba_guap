import { randomUUID } from "crypto";
import { mkdir, unlink, writeFile } from "fs/promises";
import path from "path";
import { NextResponse } from "next/server";
import { getCurrentUser } from "@/app/lib/current-user";
import { prisma } from "@/app/lib/prisma";

export const runtime = "nodejs";

const MAX_BYTES = 2 * 1024 * 1024;
const ALLOWED = new Map([
  ["image/jpeg", "jpg"],
  ["image/png", "png"],
  ["image/webp", "webp"],
]);

export async function POST(request: Request) {
  const current = await getCurrentUser();
  if (!current) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const form = await request.formData().catch(() => null);
  const file = form?.get("avatar");
  if (!(file instanceof File) || file.size === 0) {
    return NextResponse.json(
      { errors: ["Выберите изображение JPEG, PNG или WebP"] },
      { status: 400 },
    );
  }

  if (file.size > MAX_BYTES) {
    return NextResponse.json(
      { errors: ["Размер файла не должен превышать 2 МБ"] },
      { status: 400 },
    );
  }

  const ext = ALLOWED.get(file.type);
  if (!ext) {
    return NextResponse.json(
      { errors: ["Допустимы только JPEG, PNG и WebP"] },
      { status: 400 },
    );
  }

  const dir = path.join(process.cwd(), "public", "uploads", "avatars");
  await mkdir(dir, { recursive: true });

  const fileName = `${current.id}-${randomUUID()}.${ext}`;
  const absolute = path.join(dir, fileName);
  const buffer = Buffer.from(await file.arrayBuffer());
  await writeFile(absolute, buffer);

  const avatarUrl = `/uploads/avatars/${fileName}`;
  const previous = current.avatarUrl;

  const user = await prisma.user.update({
    where: { id: current.id },
    data: { avatarUrl },
    select: { id: true, name: true, email: true, gender: true, avatarUrl: true },
  });

  if (previous?.startsWith("/uploads/avatars/")) {
    const oldPath = path.join(process.cwd(), "public", previous.replace(/^\//, ""));
    await unlink(oldPath).catch(() => undefined);
  }

  return NextResponse.json({ user });
}

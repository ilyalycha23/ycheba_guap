import { randomUUID } from "crypto";
import { mkdir, unlink, writeFile } from "fs/promises";
import path from "path";

const MAX_BYTES = 2 * 1024 * 1024;
const ALLOWED = new Map([
  ["image/jpeg", "jpg"],
  ["image/png", "png"],
  ["image/webp", "webp"],
]);

export async function saveSignalImage(
  file: File,
  ownerId: string,
): Promise<{ ok: true; url: string; alt: string } | { ok: false; error: string }> {
  if (!(file instanceof File) || file.size === 0) {
    return { ok: false, error: "Выберите изображение JPEG, PNG или WebP" };
  }
  if (file.size > MAX_BYTES) {
    return { ok: false, error: "Размер файла не должен превышать 2 МБ" };
  }
  const ext = ALLOWED.get(file.type);
  if (!ext) {
    return { ok: false, error: "Допустимы только JPEG, PNG и WebP" };
  }

  const dir = path.join(process.cwd(), "public", "uploads", "signals");
  await mkdir(dir, { recursive: true });
  const fileName = `${ownerId}-${randomUUID()}.${ext}`;
  await writeFile(path.join(dir, fileName), Buffer.from(await file.arrayBuffer()));

  return {
    ok: true,
    url: `/uploads/signals/${fileName}`,
    alt: "Фото к объявлению соседа",
  };
}

export async function deleteSignalImageIfUploaded(imageUrl: string | null | undefined) {
  if (!imageUrl?.startsWith("/uploads/signals/")) return;
  const absolute = path.join(process.cwd(), "public", imageUrl.replace(/^\//, ""));
  await unlink(absolute).catch(() => undefined);
}

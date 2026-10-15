import { NextResponse } from "next/server";
import { getCurrentUser } from "@/app/lib/current-user";
import { prisma } from "@/app/lib/prisma";
import {
  defaultImageForCategory,
  isSignalCategory,
  validateSignalCoords,
  validateSignalFields,
} from "@/app/lib/signal-categories";
import { signalAuthorSelect, toSignalDto } from "@/app/lib/signal-dto";
import { deleteSignalImageIfUploaded, saveSignalImage } from "@/app/lib/signal-image";

export const runtime = "nodejs";

type Params = { params: Promise<{ id: string }> };

async function loadOwnedSignal(id: string, userId: string) {
  return prisma.neighborSignal.findFirst({
    where: { id, authorId: userId },
    include: { author: { select: signalAuthorSelect } },
  });
}

export async function PATCH(request: Request, { params }: Params) {
  const current = await getCurrentUser();
  if (!current) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { id } = await params;
  const existing = await loadOwnedSignal(id, current.id);
  if (!existing || existing.archivedAt) {
    return NextResponse.json({ errors: ["Сигнал не найден"] }, { status: 404 });
  }

  const form = await request.formData().catch(() => null);
  if (!form) {
    return NextResponse.json({ errors: ["Некорректные данные формы"] }, { status: 400 });
  }

  const title = String(form.get("title") ?? "").trim();
  const summary = String(form.get("summary") ?? "").trim();
  const location = String(form.get("location") ?? "").trim();
  const categoryRaw = String(form.get("category") ?? "").trim();
  const latitude = Number(form.get("latitude"));
  const longitude = Number(form.get("longitude"));
  const photo = form.get("photo");
  const clearPhoto = String(form.get("clearPhoto") ?? "") === "1";

  const errors = validateSignalFields({
    title,
    summary,
    category: categoryRaw,
    location,
  });
  const coordsError = validateSignalCoords(latitude, longitude);
  if (coordsError) errors.push(coordsError);

  if (errors.length > 0 || !isSignalCategory(categoryRaw)) {
    return NextResponse.json({ errors }, { status: 400 });
  }

  let image = existing.image;
  let imageAlt = existing.imageAlt;

  if (clearPhoto) {
    await deleteSignalImageIfUploaded(existing.image);
    const defaults = defaultImageForCategory(categoryRaw);
    image = defaults.image;
    imageAlt = defaults.imageAlt;
  }

  if (photo instanceof File && photo.size > 0) {
    const saved = await saveSignalImage(photo, current.id);
    if (!saved.ok) {
      return NextResponse.json({ errors: [saved.error] }, { status: 400 });
    }
    await deleteSignalImageIfUploaded(existing.image);
    image = saved.url;
    imageAlt = saved.alt;
  } else if (!existing.image.startsWith("/uploads/signals/") && isSignalCategory(categoryRaw)) {
    // Если фото не своё, а заглушка — обновляем заглушку под новый тип.
    if (existing.image.startsWith("/images/places/")) {
      const defaults = defaultImageForCategory(categoryRaw);
      image = defaults.image;
      imageAlt = defaults.imageAlt;
    }
  }

  try {
    const signal = await prisma.neighborSignal.update({
      where: { id: existing.id },
      data: {
        title,
        summary,
        category: categoryRaw,
        location,
        image,
        imageAlt,
        latitude: latitude.toFixed(6),
        longitude: longitude.toFixed(6),
      },
      include: { author: { select: signalAuthorSelect } },
    });

    return NextResponse.json({
      signal: toSignalDto(signal, new Set(), current.id),
    });
  } catch {
    return NextResponse.json(
      { errors: ["Не удалось обновить сигнал"] },
      { status: 500 },
    );
  }
}

export async function DELETE(_request: Request, { params }: Params) {
  const current = await getCurrentUser();
  if (!current) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { id } = await params;
  const existing = await loadOwnedSignal(id, current.id);
  if (!existing) {
    return NextResponse.json({ errors: ["Сигнал не найден"] }, { status: 404 });
  }
  if (existing.archivedAt) {
    return NextResponse.json({ ok: true });
  }

  const signal = await prisma.neighborSignal.update({
    where: { id: existing.id },
    data: { archivedAt: new Date() },
    include: { author: { select: signalAuthorSelect } },
  });

  return NextResponse.json({
    signal: toSignalDto(signal, new Set(), current.id),
  });
}

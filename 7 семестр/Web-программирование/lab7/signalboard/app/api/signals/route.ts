import { randomUUID } from "crypto";
import { NextResponse } from "next/server";
import { getCurrentUser } from "@/app/lib/current-user";
import { prisma } from "@/app/lib/prisma";
import {
  defaultImageForCategory,
  isSignalCategory,
  slugifyTitle,
  validateSignalCoords,
  validateSignalFields,
} from "@/app/lib/signal-categories";
import { signalAuthorSelect, toSignalDto } from "@/app/lib/signal-dto";
import { saveSignalImage } from "@/app/lib/signal-image";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export async function GET() {
  try {
    const user = await getCurrentUser();

    const [signals, tracked] = await Promise.all([
      prisma.neighborSignal.findMany({
        where: { archivedAt: null },
        orderBy: { createdAt: "desc" },
        include: { author: { select: signalAuthorSelect } },
      }),
      user
        ? prisma.trackedSignal.findMany({
            where: { userId: user.id },
            select: { signalId: true },
          })
        : Promise.resolve([]),
    ]);

    const trackedIds = new Set(tracked.map((item) => item.signalId));
    return NextResponse.json({
      signals: signals.map((signal) => toSignalDto(signal, trackedIds, user?.id)),
    });
  } catch {
    return NextResponse.json(
      { error: "Не удалось загрузить сигналы" },
      { status: 500 },
    );
  }
}

export async function POST(request: Request) {
  const current = await getCurrentUser();
  if (!current) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
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

  let image = defaultImageForCategory(categoryRaw).image;
  let imageAlt = defaultImageForCategory(categoryRaw).imageAlt;

  if (photo instanceof File && photo.size > 0) {
    const saved = await saveSignalImage(photo, current.id);
    if (!saved.ok) {
      return NextResponse.json({ errors: [saved.error] }, { status: 400 });
    }
    image = saved.url;
    imageAlt = saved.alt;
  }

  const slugBase = slugifyTitle(title);
  let slug = `${slugBase}-${randomUUID().slice(0, 8)}`;
  for (let attempt = 0; attempt < 3; attempt += 1) {
    const existing = await prisma.neighborSignal.findUnique({
      where: { slug },
      select: { id: true },
    });
    if (!existing) break;
    slug = `${slugBase}-${randomUUID().slice(0, 8)}`;
  }

  try {
    const signal = await prisma.neighborSignal.create({
      data: {
        slug,
        title,
        summary,
        category: categoryRaw,
        location,
        image,
        imageAlt,
        latitude: latitude.toFixed(6),
        longitude: longitude.toFixed(6),
        authorId: current.id,
      },
      include: { author: { select: signalAuthorSelect } },
    });

    return NextResponse.json(
      { signal: toSignalDto(signal, new Set(), current.id) },
      { status: 201 },
    );
  } catch {
    return NextResponse.json(
      { errors: ["Не удалось сохранить сигнал"] },
      { status: 500 },
    );
  }
}

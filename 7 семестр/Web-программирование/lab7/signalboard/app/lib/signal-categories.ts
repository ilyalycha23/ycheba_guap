export const SIGNAL_CATEGORIES = [
  { value: "ищу", label: "Ищу", hint: "Что-то потеряли и просите помощи" },
  { value: "нашёл", label: "Нашёл", hint: "Нашли вещь и ищете хозяина" },
  { value: "отдаю", label: "Отдаю", hint: "Готовы отдать ненужную вещь" },
  { value: "предупреждаю", label: "Предупреждаю", hint: "Важно для соседей двора" },
] as const;

export type SignalCategory = (typeof SIGNAL_CATEGORIES)[number]["value"];

export function isSignalCategory(value: unknown): value is SignalCategory {
  return SIGNAL_CATEGORIES.some((item) => item.value === value);
}

export function defaultImageForCategory(category: SignalCategory): {
  image: string;
  imageAlt: string;
} {
  switch (category) {
    case "ищу":
      return {
        image: "/images/places/lost-keys.jpg",
        imageAlt: "Заглушка для объявления «ищу»",
      };
    case "нашёл":
      return {
        image: "/images/places/found-item.jpg",
        imageAlt: "Заглушка для объявления «нашёл»",
      };
    case "отдаю":
      return {
        image: "/images/places/give-chair.jpg",
        imageAlt: "Заглушка для объявления «отдаю»",
      };
    case "предупреждаю":
      return {
        image: "/images/places/water-outage.jpg",
        imageAlt: "Заглушка для объявления «предупреждаю»",
      };
  }
}

export function slugifyTitle(title: string): string {
  const base = title
    .trim()
    .toLowerCase()
    .replace(/ё/g, "е")
    .replace(/[^a-zа-я0-9]+/gi, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 48);
  return base || "signal";
}

/** Центр двора Плесецкая 16 — стартовая точка метки. */
export const COURTYARD_CENTER = {
  latitude: 60.03582,
  longitude: 30.22145,
} as const;

/** Прямоугольник вокруг дома + прилегающая полоса на схеме двора. */
export const COURTYARD_BOUNDS = {
  latMin: 60.03495,
  latMax: 60.03675,
  lngMin: 30.22025,
  lngMax: 30.22315,
} as const;

export const COURTYARD_MAP_IMAGE = "/images/courtyard/map-v2.jpg";

function clamp(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value));
}

/** Переводит lat/lng в проценты на схеме двора (0–100). */
export function latLngToPercent(latitude: number, longitude: number): {
  left: number;
  top: number;
} {
  const { latMin, latMax, lngMin, lngMax } = COURTYARD_BOUNDS;
  const left =
    ((longitude - lngMin) / (lngMax - lngMin)) * 100;
  const top = ((latMax - latitude) / (latMax - latMin)) * 100;
  return {
    left: clamp(left, 2, 98),
    top: clamp(top, 2, 98),
  };
}

/** Обратная проекция клика по схеме двора в lat/lng. */
export function percentToLatLng(
  leftPercent: number,
  topPercent: number,
): { latitude: number; longitude: number } {
  const { latMin, latMax, lngMin, lngMax } = COURTYARD_BOUNDS;
  const longitude = lngMin + (leftPercent / 100) * (lngMax - lngMin);
  const latitude = latMax - (topPercent / 100) * (latMax - latMin);
  return { latitude, longitude };
}

export function validateSignalCoords(latitude: number, longitude: number): string | null {
  if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) {
    return "Поставьте метку на карте";
  }
  const { latMin, latMax, lngMin, lngMax } = COURTYARD_BOUNDS;
  if (
    latitude < latMin ||
    latitude > latMax ||
    longitude < lngMin ||
    longitude > lngMax
  ) {
    return "Метка должна быть на территории двора на Плесецкой 16";
  }
  return null;
}

export function validateSignalFields(input: {
  title: string;
  summary: string;
  category: string;
  location: string;
}): string[] {
  const errors: string[] = [];
  if (input.title.length < 3 || input.title.length > 160) {
    errors.push("Название должно содержать от 3 до 160 символов");
  }
  if (input.summary.length < 5 || input.summary.length > 2000) {
    errors.push("Комментарий должен содержать от 5 до 2000 символов");
  }
  if (!isSignalCategory(input.category)) {
    errors.push("Выберите тип объявления");
  }
  if (input.location.length < 3 || input.location.length > 240) {
    errors.push("Укажите место (от 3 до 240 символов)");
  }
  return errors;
}

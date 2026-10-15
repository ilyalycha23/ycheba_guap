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

export function validateSignalCoords(latitude: number, longitude: number): string | null {
  if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) {
    return "Поставьте метку на карте";
  }
  if (
    Math.abs(latitude - COURTYARD_CENTER.latitude) > 0.01 ||
    Math.abs(longitude - COURTYARD_CENTER.longitude) > 0.01
  ) {
    return "Метка должна быть рядом с двором на Плесецкой 16";
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

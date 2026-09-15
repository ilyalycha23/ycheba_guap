// Расширяет локальный сигнал фотографией, альтернативным текстом и координатами.

// Описываем поля одной предметной сущности.
export type NeighborSignal = {
  id: string;
  title: string;
  summary: string;
  category: string;
  location: string;
  image: string;
  imageAlt: string;
  latitude: number;
  longitude: number;
};

// Храним демонстрационный набор объектов в типизированном массиве.
export const neighborSignals: NeighborSignal[] = [
  {
    id: "lost-keys",
    title: "Ищу ключи от подъезда",
    summary: "Потерял связку ключей у детской площадки вечером, нужна помощь соседей.",
    category: "ищу",
    location: "Двор дома, детская площадка",
    image: "/images/places/lost-keys.jpg",
    imageAlt: "Детская площадка во дворе, где были потеряны ключи",
    latitude: 59.9318,
    longitude: 30.2985,
  },
  {
    id: "give-chair",
    title: "Отдаю офисный стул",
    summary: "Отдаю исправный стул самовывозом из второго подъезда, забирать сегодня-завтра.",
    category: "отдаю",
    location: "Второй подъезд, площадка 1 этажа",
    image: "/images/places/give-chair.jpg",
    imageAlt: "Офисный стул у входа во второй подъезд",
    latitude: 59.9326,
    longitude: 30.3012,
  },
  {
    id: "water-outage",
    title: "Отключение воды в доме",
    summary: "УК предупредила: завтра с 10:00 до 16:00 не будет холодной воды по всему стояку.",
    category: "предупреждаю",
    location: "Весь дом, стояк холодной воды",
    image: "/images/places/water-outage.jpg",
    imageAlt: "Технический стояк холодной воды в подъезде",
    latitude: 59.9334,
    longitude: 30.2968,
  },
];

export function getNeighborSignal(id: string): NeighborSignal | undefined {
  return neighborSignals.find((signal) => signal.id === id);
}

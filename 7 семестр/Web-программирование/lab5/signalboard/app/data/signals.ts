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
    summary:
      "Потерял связку ключей у детской площадки во дворе дома на Плесецкой 16 вечером, нужна помощь соседей.",
    category: "ищу",
    location: "Плесецкая ул., 16 — двор, детская площадка",
    image: "/images/places/lost-keys.jpg",
    imageAlt: "Детская площадка во дворе дома на Плесецкой 16",
    latitude: 60.0361,
    longitude: 30.22145,
  },
  {
    id: "give-chair",
    title: "Отдаю офисный стул",
    summary:
      "Отдаю исправный стул самовывозом из второго подъезда дома на Плесецкой 16, забирать сегодня-завтра.",
    category: "отдаю",
    location: "Плесецкая ул., 16 — второй подъезд, 1 этаж",
    image: "/images/places/give-chair.jpg",
    imageAlt: "Офисный стул у входа во второй подъезд дома на Плесецкой 16",
    latitude: 60.03582,
    longitude: 30.22205,
  },
  {
    id: "water-outage",
    title: "Отключение воды в доме",
    summary:
      "УК предупредила: завтра с 10:00 до 16:00 не будет холодной воды по всему стояку в доме на Плесецкой 16.",
    category: "предупреждаю",
    location: "Плесецкая ул., 16 — весь дом, стояк ХВС",
    image: "/images/places/water-outage.jpg",
    imageAlt: "Технический стояк холодной воды в подъезде дома на Плесецкой 16",
    latitude: 60.03562,
    longitude: 30.22135,
  },
];

export function getNeighborSignal(id: string): NeighborSignal | undefined {
  return neighborSignals.find((signal) => signal.id === id);
}

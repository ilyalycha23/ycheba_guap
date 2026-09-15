// Описывает локальные сигналы соседей, демонстрационные данные и поиск объекта по id.

// Описываем поля одной предметной сущности.
export type NeighborSignal = {
  id: string;
  title: string;
  summary: string;
  category: string;
};

// Храним демонстрационный набор объектов в типизированном массиве.
export const neighborSignals: NeighborSignal[] = [
  {
    id: "lost-keys",
    title: "Ищу ключи от подъезда",
    summary: "Потерял связку ключей у детской площадки вечером, нужна помощь соседей.",
    category: "ищу",
  },
  {
    id: "give-chair",
    title: "Отдаю офисный стул",
    summary: "Отдаю исправный стул самовывозом из второго подъезда, забирать сегодня-завтра.",
    category: "отдаю",
  },
  {
    id: "water-outage",
    title: "Отключение воды в доме",
    summary: "УК предупредила: завтра с 10:00 до 16:00 не будет холодной воды по всему стояку.",
    category: "предупреждаю",
  },
];

export function getNeighborSignal(id: string): NeighborSignal | undefined {
  return neighborSignals.find((signal) => signal.id === id);
}

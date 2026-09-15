// Получает динамический id, находит объект и выводит страницу либо 404.

import Link from "next/link";
import { notFound } from "next/navigation";
import { getNeighborSignal } from "../../data/signals";

// Типизируем параметры динамического маршрута.
type SignalPageProps = {
  params: Promise<{ id: string }>;
};

// Объявляем основной компонент этого файла.
export default async function SignalPage({ params }: SignalPageProps) {
  // Получаем id из параметров динамического маршрута.
  const { id } = await params;
  // Ищем объект с идентификатором из URL.
  const signal = getNeighborSignal(id);

  if (!signal) {
    // Показываем стандартную страницу 404, если объект не найден.
    notFound();
  }

  // Возвращаем JSX-разметку, которую React выведет на странице.
  return (
    <main>
      <p className="eyebrow">Локальный сигнал</p>
      <h1>{signal.title}</h1>
      <p className="lead">{signal.summary}</p>
      <p>
        <strong>Тип:</strong> {signal.category}
      </p>
      <p>
        <strong>Место:</strong> {signal.location}
      </p>
      <Link href="/signals">Вернуться в ленту</Link>
    </main>
  );
}

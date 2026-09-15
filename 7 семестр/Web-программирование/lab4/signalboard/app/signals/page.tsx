// Строит ленту карточек из массива локальных сигналов.

import Link from "next/link";
import { neighborSignals } from "../data/signals";

// Объявляем основной компонент этого файла.
export default function SignalsPage() {
  // Возвращаем JSX-разметку, которую React выведет на странице.
  return (
    <main>
      <h1>Лента сигналов</h1>
      <div className="card-grid">
        {neighborSignals.map((signal) => (
          <article className="card" key={signal.id}>
            <h2>{signal.title}</h2>
            <p>{signal.summary}</p>
            <p>
              <strong>Тип:</strong> {signal.category}
            </p>
            <Link href={`/signals/${signal.id}`}>Подробнее</Link>
          </article>
        ))}
      </div>
    </main>
  );
}

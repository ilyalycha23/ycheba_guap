// Формирует главную страницу SignalBoard из смысловых разделов и карточек.

import Link from "next/link";
import FeatureCard from "./ui/FeatureCard";

// Объявляем основной компонент этого файла.
export default function HomePage() {
  // Возвращаем JSX-разметку, которую React выведет на странице.
  return (
    <main>
      <header>
        <p className="eyebrow">Учебный проект</p>
        <h1>SignalBoard</h1>
        <p>
          SignalBoard помогает соседям публиковать локальные сигналы — объявления
          «ищу», «отдаю», «предупреждаю» — в одном месте вместо разрозненных
          чатов дома и двора.
        </p>
      </header>

      <section aria-labelledby="audience-title">
        <h2 id="audience-title">Целевая аудитория</h2>
        <p>
          Жители одного дома, двора или ЖК, которым нужно быстро сообщить
          соседям о находке, просьбе помощи или важном предупреждении.
        </p>
      </section>

      <section aria-labelledby="features-title">
        <h2 id="features-title">Основные функции</h2>

        <div className="feature-list">
          <FeatureCard
            title="Лента сигналов"
            description="Просмотр актуальных объявлений соседей в одном потоке."
          />

          <FeatureCard
            title="Фильтры по типу"
            description="Отбор сигналов: ищу, отдаю, предупреждаю и другие категории."
          />

          <FeatureCard
            title="Личный кабинет"
            description="Управление своими сигналами: создание, статусы и архив."
          />
        </div>
      </section>

      <Link className="main-link" href="/about">
        Подробнее о проекте
      </Link>
    </main>
  );
}

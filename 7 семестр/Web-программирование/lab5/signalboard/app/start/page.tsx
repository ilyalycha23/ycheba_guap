// Выводит стартовую страницу и ссылки на основные пользовательские сценарии.

import Link from "next/link";
import FeatureCard from "../ui/FeatureCard";

// Объявляем основной компонент этого файла.
export default function StartPage() {
  // Возвращаем JSX-разметку, которую React выведет на странице.
  return (
    <main>
      <p className="eyebrow">Учебный проект</p>
      <h1>SignalBoard</h1>
      <p className="lead">
        Доска локальных сигналов для соседей одного дома, двора или ЖК. Объявления
        «ищу», «отдаю» и «предупреждаю» собраны в одном месте вместо разрозненных чатов.
      </p>

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

      <Link className="primary-link" href="/signals">
        Открыть ленту сигналов
      </Link>
    </main>
  );
}

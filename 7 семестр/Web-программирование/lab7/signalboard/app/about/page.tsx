import Link from "next/link";
import FeatureCard from "../ui/FeatureCard";
import styles from "./about.module.css";

export default function AboutPage() {
  return (
    <main className={styles.page}>
      <header className={styles.hero}>
        <p className="eyebrow">Учебный проект</p>
        <h1>О проекте SignalBoard</h1>
        <p className="lead">
          Доска локальных сигналов для соседей одного дома, двора или ЖК. Объявления
          «ищу», «нашёл», «отдаю» и «предупреждаю» собраны в одном месте вместо
          разрозненных чатов.
        </p>
      </header>

      <section className={styles.section}>
        <h2>Цель разработки</h2>
        <p>
          Создать веб-приложение для публикации и просмотра локальных сигналов между
          соседями одного двора или дома — на примере Плесецкой улицы, 16.
        </p>
      </section>

      <section className={styles.section}>
        <h2>Что умеет приложение</h2>
        <div className="feature-list">
          <FeatureCard
            title="Сигналы и карта"
            description="Публикация объявлений с фото, меткой на карте и категорией."
          />
          <FeatureCard
            title="Отслеживание"
            description="Сохраняйте важные сигналы соседей и смотрите их на главной."
          />
          <FeatureCard
            title="Архив"
            description="Удалённые объявления не пропадают — они переходят в личный архив."
          />
          <FeatureCard
            title="Личный кабинет"
            description="Профиль соседа: имя, аватар и смена пароля в защищённой сессии."
          />
        </div>
      </section>

      <section className={styles.section}>
        <h2>Основная предметная сущность</h2>
        <p>Сигнал — локальное объявление соседа с категорией, местом и координатами.</p>
      </section>

      <section className={styles.section}>
        <h2>Разделы приложения</h2>
        <ul className={styles.list}>
          <li>главная — отслеживаемые сигналы и быстрый вход в сценарии;</li>
          <li>сигналы с картой двора и архивом;</li>
          <li>соседи — список пользователей;</li>
          <li>личный кабинет;</li>
          <li>вход и регистрация;</li>
          <li>этот информационный раздел.</li>
        </ul>
      </section>

      <div className={styles.actions}>
        <Link className="btn btnPrimary" href="/start">
          На главную
        </Link>
        <Link className="btn btnGhost" href="/gallery">
          К сигналам
        </Link>
      </div>
    </main>
  );
}

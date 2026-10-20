import Image from "next/image";
import Link from "next/link";
import styles from "./about.module.css";

export default function AboutPage() {
  return (
    <main className={styles.page}>
      <header className={styles.hero}>
        <div className={styles.heroMedia} aria-hidden="true">
          <Image
            src="/images/about/hero-courtyard.jpg"
            alt=""
            fill
            priority
            sizes="100vw"
            className={styles.heroImage}
          />
          <div className={styles.heroWash} />
        </div>

        <div className={styles.heroInner}>
          <p className={styles.brand}>SignalBoard</p>
          <h1 className={styles.heroTitle}>
            Доска двора,
            <span>а не ещё один чат</span>
          </h1>
          <p className={styles.heroLead}>
            Локальные сигналы соседей у дома на Плесецкой, 16 — на карте, с фото
            и без хаоса переписок.
          </p>
          <div className={styles.heroCta}>
            <Link className={styles.ctaPrimary} href="/gallery">
              Открыть сигналы
            </Link>
            <a
              className={styles.ctaGhost}
              href="https://github.com/ilyalycha23"
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub автора
            </a>
          </div>
        </div>
      </header>

      <section className={styles.manifesto} aria-labelledby="about-manifesto">
        <p className={styles.manifestoEyebrow}>О проекте</p>
        <h2 id="about-manifesto" className={styles.manifestoTitle}>
          Один двор — одна доска
        </h2>
        <div className={styles.manifestoBody}>
          <p>
            SignalBoard собирает то, что обычно тонет в групповых чатах: «ищу
            ключи», «нашёл сумку», «отдаю стул», «завтра не будет воды». Каждое
            объявление — с местом на карте и лицом соседа.
          </p>
          <p>
            Это учебный веб-проект: живой интерфейс, серверная авторизация и
            PostgreSQL. После обновления страницы отслеживание и сессия на
            месте — потому что правда хранится в базе, а не в памяти браузера.
          </p>
        </div>
        <blockquote className={styles.quote}>
          Меньше шума в мессенджере — больше ясности у подъезда.
        </blockquote>
      </section>

      <section className={styles.author} aria-labelledby="about-author">
        <div className={styles.authorVisual} aria-hidden="true">
          <div className={styles.authorOrb} />
          <p className={styles.authorInitials}>ИА</p>
          <p className={styles.authorCity}>Санкт-Петербург</p>
        </div>

        <div className={styles.authorCopy}>
          <p className={styles.authorLabel}>Разработчик</p>
          <h2 id="about-author">Лаврешин Илья</h2>
          <p>
            Студент ГУАП. SignalBoard — курсовая работа по веб-программированию:
            Next.js, Prisma, PostgreSQL и всё, что между кнопкой «Отслеживать»
            и реальной строкой в базе.
          </p>
          <p>
            Код проекта и другие учебные и коммерческие работы — в открытом
            профиле на GitHub.
          </p>

          <a
            className={styles.githubBtn}
            href="https://github.com/ilyalycha23"
            target="_blank"
            rel="noopener noreferrer"
          >
            <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true">
              <path d="M12 2C6.477 2 2 6.586 2 12.253c0 4.53 2.865 8.367 6.839 9.72.5.094.682-.222.682-.482 0-.237-.009-.866-.014-1.7-2.782.616-3.369-1.37-3.369-1.37-.455-1.18-1.11-1.494-1.11-1.494-.908-.635.069-.622.069-.622 1.003.072 1.53 1.056 1.53 1.056.892 1.56 2.341 1.11 2.91.849.091-.66.35-1.11.636-1.366-2.22-.258-4.555-1.137-4.555-5.06 0-1.118.39-2.033 1.029-2.75-.103-.259-.446-1.3.098-2.71 0 0 .84-.274 2.75 1.05A9.35 9.35 0 0 1 12 6.844a9.3 9.3 0 0 1 2.504.345c1.909-1.324 2.747-1.05 2.747-1.05.546 1.41.203 2.451.1 2.71.64.717 1.028 1.632 1.028 2.75 0 3.933-2.338 4.798-4.566 5.052.359.316.679.942.679 1.9 0 1.372-.012 2.477-.012 2.814 0 .263.18.58.688.48A10.02 10.02 0 0 0 22 12.253C22 6.586 17.523 2 12 2Z" />
            </svg>
            <span>
              <strong>ilyalycha23</strong>
              <small>github.com/ilyalycha23</small>
            </span>
          </a>
        </div>
      </section>
    </main>
  );
}

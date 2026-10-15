"use client";

import Image from "next/image";
import Link from "next/link";
import { useCallback, useEffect, useMemo, useState } from "react";
import { useAuth } from "@/app/providers/AuthProvider";
import type { NeighborSignalDTO } from "@/app/gallery/_components/SignalsGallery";
import { formatPublishedAt, greetingByHour } from "@/app/lib/datetime";
import styles from "./home.module.css";

export default function HomeDashboard() {
  const { user, status } = useAuth();
  const [signals, setSignals] = useState<NeighborSignalDTO[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [reloadKey, setReloadKey] = useState(0);

  const retry = useCallback(() => setReloadKey((value) => value + 1), []);

  useEffect(() => {
    const controller = new AbortController();

    async function loadSignals() {
      setLoading(true);
      setError("");
      try {
        const response = await fetch("/api/signals", {
          cache: "no-store",
          credentials: "same-origin",
          signal: controller.signal,
        });
        if (!response.ok) throw new Error("Не удалось загрузить сигналы");
        const payload = (await response.json()) as { signals: NeighborSignalDTO[] };
        setSignals(payload.signals);
      } catch (value) {
        if (value instanceof DOMException && value.name === "AbortError") return;
        setError(value instanceof Error ? value.message : "Ошибка загрузки");
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    }

    void loadSignals();
    return () => controller.abort();
  }, [reloadKey, status]);

  const tracked = useMemo(() => signals.filter((item) => item.isTracked), [signals]);
  const recent = useMemo(() => signals.slice(0, 3), [signals]);

  const warningCount = useMemo(
    () => signals.filter((item) => item.category === "предупреждаю").length,
    [signals],
  );

  const dayPart = greetingByHour();
  const greeting =
    status === "authenticated" && user
      ? `${dayPart}, ${user.name}`
      : `${dayPart}! Добро пожаловать во двор`;

  return (
    <main className={styles.page}>
      <section className={styles.hero}>
        <div className={styles.heroCopy}>
          <p className="eyebrow">SignalBoard</p>
          <h1>{greeting}</h1>
          <p className={styles.heroLead}>
            Здесь собраны сигналы вашего двора: что отслеживаете, что происходит рядом
            и куда перейти дальше.
          </p>
          <div className={styles.heroActions}>
            <Link href="/gallery" className="btn btnPrimary">
              Открыть сигналы
            </Link>
            <Link href="/gallery/archive" className="btn btnGhost">
              Архив
            </Link>
          </div>
        </div>

        <div className={styles.stats} aria-label="Сводка по двору">
          <div className={styles.stat}>
            <span className={styles.statValue}>{loading ? "…" : signals.length}</span>
            <span className={styles.statLabel}>Всего</span>
          </div>
          <div className={styles.stat}>
            <span className={styles.statValue}>{loading ? "…" : tracked.length}</span>
            <span className={styles.statLabel}>Отслеживается</span>
          </div>
          <div className={styles.stat}>
            <span className={styles.statValue}>{loading ? "…" : warningCount}</span>
            <span className={styles.statLabel}>Предупреждения</span>
          </div>
        </div>
      </section>

      <section className={styles.section} aria-labelledby="tracked-heading">
        <div className={styles.sectionHead}>
          <div>
            <h2 id="tracked-heading">Отслеживаемые сигналы</h2>
            <p className={styles.sectionHint}>
              То, что вы отметили в разделе «Сигналы» — под рукой на главной.
            </p>
          </div>
          <Link href="/gallery" className="btn btnHot">
            Ко всем сигналам
          </Link>
        </div>

        {loading ? <p className={styles.status}>Загружаем сигналы…</p> : null}
        {error ? (
          <div className={styles.empty}>
            <p className="form-error">{error}</p>
            <button type="button" className="btn btnGhost" onClick={retry}>
              Повторить
            </button>
          </div>
        ) : null}

        {!loading && !error && status !== "authenticated" ? (
          <div className={styles.empty}>
            <p>
              Войдите в аккаунт, чтобы видеть здесь отслеживаемые сигналы и сохранять их
              между визитами.
            </p>
            <Link href="/auth/login" className="btn btnPrimary">
              Войти
            </Link>
          </div>
        ) : null}

        {!loading && !error && status === "authenticated" && tracked.length === 0 ? (
          <div className={styles.empty}>
            <p>
              Пока ничего не отслеживается. Откройте «Сигналы» и нажмите «Отслеживать» на
              нужном объявлении.
            </p>
            <Link href="/gallery" className="btn btnPrimary">
              Перейти к сигналам
            </Link>
          </div>
        ) : null}

        {!loading && !error && tracked.length > 0 ? (
          <div className={styles.grid}>
            {tracked.map((signal) => (
              <Link key={signal.id} href="/gallery" className={styles.card}>
                <div className={styles.cardMedia}>
                  <Image
                    src={signal.image}
                    alt={signal.imageAlt}
                    fill
                    sizes="(max-width: 40rem) 100vw, 18rem"
                  />
                </div>
                <div className={styles.cardBody}>
                  <span className={styles.badge}>{signal.category}</span>
                  <h3 className={styles.cardTitle}>{signal.title}</h3>
                  <p className={styles.cardText}>{signal.summary}</p>
                  <time dateTime={signal.createdAt} className={styles.publishedAt}>
                    {formatPublishedAt(signal.createdAt)}
                  </time>
                </div>
              </Link>
            ))}
          </div>
        ) : null}
      </section>

      <section className={styles.section} aria-labelledby="pulse-heading">
        <div className={styles.sectionHead}>
          <div>
            <h2 id="pulse-heading">Сигналы двора</h2>
            <p className={styles.sectionHint}>
              Актуальные объявления с Плесецкой 16 — ищу, отдаю, предупреждаю.
            </p>
          </div>
          <Link href="/gallery" className="btn btnGhost">
            Все сигналы
          </Link>
        </div>

        {!loading && !error && recent.length > 0 ? (
          <div className={styles.grid}>
            {recent.map((signal) => (
              <Link key={signal.id} href="/gallery" className={styles.card}>
                <div className={styles.cardMedia}>
                  <Image
                    src={signal.image}
                    alt={signal.imageAlt}
                    fill
                    sizes="(max-width: 40rem) 100vw, 18rem"
                  />
                </div>
                <div className={styles.cardBody}>
                  <span className={styles.badge}>{signal.category}</span>
                  <h3 className={styles.cardTitle}>{signal.title}</h3>
                  <p className={styles.cardText}>{signal.location}</p>
                  <time dateTime={signal.createdAt} className={styles.publishedAt}>
                    {formatPublishedAt(signal.createdAt)}
                  </time>
                </div>
              </Link>
            ))}
          </div>
        ) : null}
      </section>

      <section className={styles.section} aria-labelledby="shortcuts-heading">
        <div className={styles.sectionHead}>
          <div>
            <h2 id="shortcuts-heading">Быстрый переход</h2>
            <p className={styles.sectionHint}>Основные сценарии приложения в один клик.</p>
          </div>
        </div>
        <div className={styles.shortcuts}>
          <Link href="/gallery" className={styles.shortcut}>
            <span className={styles.shortcutMark} aria-hidden="true">
              С
            </span>
            <h3>Сигналы и карта</h3>
            <p>Объявления двора, метки на карте и отслеживание.</p>
          </Link>
          <Link href="/neighbors" className={styles.shortcut}>
            <span className={styles.shortcutMark} aria-hidden="true">
              Д
            </span>
            <h3>Соседи</h3>
            <p>Имена и фото всех зарегистрированных пользователей двора.</p>
          </Link>
          <Link
            href={status === "authenticated" ? "/cabinet" : "/auth/login"}
            className={styles.shortcut}
          >
            <span className={styles.shortcutMark} aria-hidden="true">
              К
            </span>
            <h3>{status === "authenticated" ? "Кабинет" : "Войти"}</h3>
            <p>
              {status === "authenticated"
                ? "Имя, фото профиля и смена пароля."
                : "Сессия нужна, чтобы сохранять отслеживание."}
            </p>
          </Link>
        </div>
      </section>
    </main>
  );
}

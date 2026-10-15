"use client";

import Image from "next/image";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { useAuth } from "@/app/providers/AuthProvider";
import { formatPublishedAt } from "@/app/lib/datetime";
import type { NeighborSignalDTO } from "../_components/SignalsGallery";
import styles from "./archive.module.css";

export default function ArchivePage() {
  const { status } = useAuth();
  const [signals, setSignals] = useState<NeighborSignalDTO[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [reloadKey, setReloadKey] = useState(0);

  const retry = useCallback(() => setReloadKey((value) => value + 1), []);

  useEffect(() => {
    if (status !== "authenticated") return;

    const controller = new AbortController();

    async function loadArchive() {
      setLoading(true);
      setError("");
      try {
        const response = await fetch("/api/signals/archive", {
          cache: "no-store",
          credentials: "same-origin",
          signal: controller.signal,
        });
        if (!response.ok) throw new Error("Не удалось загрузить архив");
        const payload = (await response.json()) as { signals: NeighborSignalDTO[] };
        setSignals(payload.signals);
      } catch (value) {
        if (value instanceof DOMException && value.name === "AbortError") return;
        setError(value instanceof Error ? value.message : "Ошибка загрузки");
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    }

    void loadArchive();
    return () => controller.abort();
  }, [reloadKey, status]);

  if (status === "loading") {
    return (
      <main className={styles.page}>
        <h1>Архив сигналов</h1>
        <p role="status">Проверяем сессию…</p>
      </main>
    );
  }

  if (status !== "authenticated") {
    return (
      <main className={styles.page}>
        <h1>Архив сигналов</h1>
        <p>Архив доступен только после входа.</p>
        <Link href="/auth/login" className="btn btnPrimary">
          Войти
        </Link>
      </main>
    );
  }

  return (
    <main className={styles.page}>
      <div className={styles.head}>
        <div>
          <h1>Архив сигналов</h1>
          <p className={styles.lead}>
            Здесь лежат ваши удалённые объявления. Они скрыты из общей ленты и карты.
          </p>
        </div>
        <Link href="/gallery" className="btn btnGhost">
          К сигналам
        </Link>
      </div>

      {loading ? <p role="status">Загружаем архив…</p> : null}
      {error ? (
        <div className={styles.empty}>
          <p className="form-error">{error}</p>
          <button type="button" className="btn btnGhost" onClick={retry}>
            Повторить
          </button>
        </div>
      ) : null}

      {!loading && !error && signals.length === 0 ? (
        <div className={styles.empty}>
          <p>Архив пока пуст.</p>
        </div>
      ) : null}

      {!loading && signals.length > 0 ? (
        <ul className={styles.list}>
          {signals.map((signal) => (
            <li key={signal.id} className={styles.card}>
              <div className={styles.media}>
                <Image
                  src={signal.image}
                  alt={signal.imageAlt}
                  fill
                  sizes="8rem"
                  className={styles.image}
                />
              </div>
              <div className={styles.body}>
                <span className={styles.badge}>{signal.category}</span>
                <h2>{signal.title}</h2>
                <p>{signal.summary}</p>
                <p className={styles.meta}>
                  Опубликован: {formatPublishedAt(signal.createdAt)}
                  {signal.archivedAt
                    ? ` · В архиве с ${formatPublishedAt(signal.archivedAt)}`
                    : ""}
                </p>
              </div>
            </li>
          ))}
        </ul>
      ) : null}
    </main>
  );
}

// Загружает реальные сигналы и сохраняет отслеживание через серверный API.

"use client";

import Image from "next/image";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import PhotoMap from "./PhotoMap";
import PhotoModal from "./PhotoModal";
import { useAuth } from "@/app/providers/AuthProvider";
import styles from "./SignalsGallery.module.css";

export type NeighborSignalDTO = {
  id: string;
  slug: string;
  title: string;
  summary: string;
  category: string;
  location: string;
  image: string;
  imageAlt: string;
  latitude: number;
  longitude: number;
  isTracked: boolean;
};

export default function SignalsGallery() {
  const { status, refresh } = useAuth();
  const [signals, setSignals] = useState<NeighborSignalDTO[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [pendingId, setPendingId] = useState<string | null>(null);
  const [reloadKey, setReloadKey] = useState(0);
  const [selected, setSelected] = useState<NeighborSignalDTO | null>(null);
  const [returnFocusTo, setReturnFocusTo] = useState<HTMLButtonElement | null>(null);

  function openFromCard(signal: NeighborSignalDTO, button: HTMLButtonElement) {
    setReturnFocusTo(button);
    setSelected(signal);
  }

  const openFromMap = useCallback((signal: NeighborSignalDTO) => {
    setReturnFocusTo(null);
    setSelected(signal);
  }, []);

  function closeModal() {
    setSelected(null);
  }

  // Повторная загрузка вызывается кнопкой после сетевой ошибки.
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
        // Игнорируем ожидаемую отмену при размонтировании компонента.
        if (value instanceof DOMException && value.name === "AbortError") return;
        setError(value instanceof Error ? value.message : "Ошибка загрузки");
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    }

    void loadSignals();

    // Отменяем запрос, если компонент больше не используется.
    return () => controller.abort();
  }, [reloadKey, status]);

  async function toggleTracked(signal: NeighborSignalDTO) {
    if (status !== "authenticated") return;

    setPendingId(signal.id);
    setError("");

    try {
      const response = await fetch(`/api/favorites/${signal.id}`, {
        method: signal.isTracked ? "DELETE" : "POST",
        credentials: "same-origin",
      });

      if (response.status === 401) {
        // Синхронизируем UI, если сервер больше не принимает сессию.
        await refresh();
        throw new Error("Сеанс завершён. Выполните вход снова.");
      }

      if (!response.ok) throw new Error("Не удалось изменить отслеживание");

      const nextTracked = !signal.isTracked;

      // Меняем только карточку, изменение которой подтвердил сервер.
      setSignals((current) =>
        current.map((item) =>
          item.id === signal.id
            ? { ...item, isTracked: nextTracked }
            : item,
        ),
      );
      setSelected((current) =>
        current && current.id === signal.id
          ? { ...current, isTracked: nextTracked }
          : current,
      );
    } catch (value) {
      setError(value instanceof Error ? value.message : "Ошибка отслеживания");
    } finally {
      setPendingId(null);
    }
  }

  if (loading) return <p role="status">Загрузка сигналов…</p>;

  if (error && signals.length === 0) {
    return (
      <div role="alert">
        <p>{error}</p>
        <button type="button" onClick={retry}>Повторить</button>
      </div>
    );
  }

  if (signals.length === 0) return <p>Сигналы пока не добавлены.</p>;

  return (
    <>
      {error ? <p role="alert">{error}</p> : null}

      <div className={styles.grid}>
        {signals.map((signal) => (
          <article className={styles.card} key={signal.id}>
            <button
              className={styles.cardOpen}
              type="button"
              onClick={(event) => openFromCard(signal, event.currentTarget)}
            >
              <span className={styles.imageWrap}>
                <Image
                  src={signal.image}
                  alt={signal.imageAlt}
                  fill
                  sizes="(max-width: 47.99rem) calc(100vw - 2rem), (max-width: 74.99rem) 45vw, 22rem"
                  className={styles.image}
                />
              </span>
              <span className={styles.cardBody}>
                <span className={styles.title}>{signal.title}</span>
                <span className={styles.summary}>{signal.summary}</span>
              </span>
            </button>

            {status === "authenticated" ? (
              <button
                type="button"
                className={styles.trackButton}
                disabled={pendingId === signal.id}
                aria-pressed={signal.isTracked}
                aria-label={`${
                  signal.isTracked
                    ? "Удалить из отслеживания"
                    : "Добавить в отслеживание"
                }: ${signal.title}`}
                onClick={() => void toggleTracked(signal)}
              >
                {signal.isTracked ? "В отслеживании" : "Отслеживать"}
              </button>
            ) : (
              <Link className={styles.trackLink} href="/auth/login">
                Войдите, чтобы отслеживать сигнал
              </Link>
            )}
          </article>
        ))}
      </div>

      <PhotoMap signals={signals} onSelect={openFromMap} />

      {selected ? (
        <PhotoModal
          signal={selected}
          pending={pendingId === selected.id}
          onToggleTracked={() => void toggleTracked(selected)}
          onClose={closeModal}
          returnFocusTo={returnFocusTo}
        />
      ) : null}
    </>
  );
}

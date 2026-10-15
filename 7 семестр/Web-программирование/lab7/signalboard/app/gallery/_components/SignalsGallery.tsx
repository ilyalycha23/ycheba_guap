"use client";

import Image from "next/image";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import UserAvatar from "@/app/ui/UserAvatar";
import { useAuth } from "@/app/providers/AuthProvider";
import { formatPublishedAt } from "@/app/lib/datetime";
import CreateSignalForm from "./CreateSignalForm";
import PhotoMap from "./PhotoMap";
import PhotoModal from "./PhotoModal";
import TrackToggle from "./TrackToggle";
import trackStyles from "./TrackToggle.module.css";
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
  createdAt: string;
  archivedAt?: string | null;
  isTracked: boolean;
  isOwn?: boolean;
  author: {
    id: string;
    name: string;
    gender: "male" | "female";
    avatarUrl: string;
  };
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
        await refresh();
        throw new Error("Сеанс завершён. Выполните вход снова.");
      }

      if (!response.ok) {
        const payload = (await response.json().catch(() => null)) as
          | { error?: string; errors?: string[] }
          | null;
        const message =
          payload?.errors?.[0] ??
          payload?.error ??
          "Не удалось изменить отслеживание";
        if (response.status === 404) {
          throw new Error("Сигнал не найден");
        }
        throw new Error(message);
      }

      const nextTracked = !signal.isTracked;

      setSignals((current) =>
        current.map((item) =>
          item.id === signal.id ? { ...item, isTracked: nextTracked } : item,
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

  function handleCreated(signal: NeighborSignalDTO) {
    setSignals((current) => [signal, ...current]);
    setSelected(signal);
  }

  function handleUpdated(signal: NeighborSignalDTO) {
    setSignals((current) =>
      current.map((item) => (item.id === signal.id ? signal : item)),
    );
    setSelected(signal);
  }

  function handleArchived(signalId: string) {
    setSignals((current) => current.filter((item) => item.id !== signalId));
    setSelected(null);
  }

  return (
    <>
      <CreateSignalForm onCreated={handleCreated} />

      {loading ? <p role="status">Загрузка сигналов…</p> : null}

      {error && signals.length === 0 && !loading ? (
        <div role="alert">
          <p>{error}</p>
          <button type="button" className="btn btnGhost" onClick={retry}>
            Повторить
          </button>
        </div>
      ) : null}

      {error && signals.length > 0 ? <p role="alert">{error}</p> : null}

      {!loading && signals.length === 0 && !error ? (
        <p>Сигналы пока не добавлены. Опубликуйте первый.</p>
      ) : null}

      {signals.length > 0 ? (
        <div className={styles.grid}>
          {signals.map((signal, index) => (
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
                    loading={index === 0 ? "eager" : "lazy"}
                    fetchPriority={index === 0 ? "high" : "auto"}
                  />
                </span>
                <span className={styles.cardBody}>
                  <span className={styles.badge}>{signal.category}</span>
                  <span className={styles.title}>{signal.title}</span>
                  <span className={styles.summary}>{signal.summary}</span>
                  <span className={styles.author}>
                    <UserAvatar
                      name={signal.author.name}
                      avatarUrl={signal.author.avatarUrl}
                      gender={signal.author.gender}
                      className={styles.authorAvatar}
                    />
                    <span className={styles.authorMeta}>
                      <span>{signal.author.name}</span>
                      <time dateTime={signal.createdAt} className={styles.publishedAt}>
                        {formatPublishedAt(signal.createdAt)}
                      </time>
                    </span>
                  </span>
                </span>
              </button>

              {status === "authenticated" ? (
                <TrackToggle
                  layout="card"
                  tracked={signal.isTracked}
                  pending={pendingId === signal.id}
                  title={signal.title}
                  onClick={() => void toggleTracked(signal)}
                />
              ) : (
                <Link className={trackStyles.link} href="/auth/login">
                  Войдите, чтобы отслеживать
                </Link>
              )}
            </article>
          ))}
        </div>
      ) : null}

      <PhotoMap signals={signals} onSelect={openFromMap} />

      {selected ? (
        <PhotoModal
          signal={selected}
          pending={pendingId === selected.id}
          onToggleTracked={() => void toggleTracked(selected)}
          onClose={closeModal}
          onUpdated={handleUpdated}
          onArchived={handleArchived}
          returnFocusTo={returnFocusTo}
        />
      ) : null}
    </>
  );
}

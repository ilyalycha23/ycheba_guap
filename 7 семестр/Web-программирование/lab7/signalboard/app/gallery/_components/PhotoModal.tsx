"use client";

import Image from "next/image";
import Link from "next/link";
import { useEffect, useRef, useState, type KeyboardEvent as ReactKeyboardEvent } from "react";
import { createPortal } from "react-dom";
import UserAvatar from "@/app/ui/UserAvatar";
import { formatPublishedAt } from "@/app/lib/datetime";
import { useAuth } from "../../providers/AuthProvider";
import type { NeighborSignalDTO } from "./SignalsGallery";
import SignalForm from "./SignalForm";
import TrackToggle from "./TrackToggle";
import styles from "./PhotoModal.module.css";

type PhotoModalProps = {
  signal: NeighborSignalDTO;
  pending: boolean;
  onToggleTracked: () => void;
  onClose: () => void;
  onUpdated: (signal: NeighborSignalDTO) => void;
  onArchived: (signalId: string) => void;
  returnFocusTo: HTMLElement | null;
};

const focusableSelector = [
  "a[href]",
  "button:not([disabled])",
  "input:not([disabled])",
  "select:not([disabled])",
  "textarea:not([disabled])",
  '[tabindex]:not([tabindex="-1"])',
].join(",");

export default function PhotoModal({
  signal,
  pending,
  onToggleTracked,
  onClose,
  onUpdated,
  onArchived,
  returnFocusTo,
}: PhotoModalProps) {
  const { user, status } = useAuth();
  const authReady = status !== "loading";
  const dialogRef = useRef<HTMLDivElement>(null);
  const closeButtonRef = useRef<HTMLButtonElement>(null);
  const [editing, setEditing] = useState(false);
  const [editPending, setEditPending] = useState(false);
  const [editError, setEditError] = useState("");
  const [archivePending, setArchivePending] = useState(false);

  useEffect(() => {
    const previousOverflow = document.documentElement.style.overflow;
    document.documentElement.style.overflow = "hidden";
    closeButtonRef.current?.focus();

    function handleEscape(event: globalThis.KeyboardEvent) {
      if (event.key === "Escape") {
        if (editing) setEditing(false);
        else onClose();
      }
    }

    window.addEventListener("keydown", handleEscape);
    return () => {
      window.removeEventListener("keydown", handleEscape);
      document.documentElement.style.overflow = previousOverflow;
      returnFocusTo?.focus();
    };
  }, [editing, onClose, returnFocusTo]);

  function keepFocusInside(event: ReactKeyboardEvent<HTMLDivElement>) {
    if (event.key !== "Tab") return;
    const focusable = Array.from(
      dialogRef.current?.querySelectorAll<HTMLElement>(focusableSelector) ?? [],
    );
    if (focusable.length === 0) {
      event.preventDefault();
      return;
    }
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  async function handleEdit(body: FormData) {
    setEditError("");
    setEditPending(true);
    try {
      const response = await fetch(`/api/signals/${signal.id}`, {
        method: "PATCH",
        credentials: "same-origin",
        body,
      });
      const payload = (await response.json().catch(() => null)) as
        | { signal?: NeighborSignalDTO; errors?: string[]; error?: string }
        | null;
      if (!response.ok) {
        throw new Error(payload?.errors?.[0] ?? payload?.error ?? "Не удалось сохранить");
      }
      if (!payload?.signal) throw new Error("Пустой ответ сервера");
      onUpdated(payload.signal);
      setEditing(false);
    } catch (value) {
      setEditError(value instanceof Error ? value.message : "Ошибка сохранения");
    } finally {
      setEditPending(false);
    }
  }

  async function handleArchive() {
    if (!window.confirm("Удалить сигнал в архив? Его можно будет посмотреть в архиве.")) {
      return;
    }
    setArchivePending(true);
    try {
      const response = await fetch(`/api/signals/${signal.id}`, {
        method: "DELETE",
        credentials: "same-origin",
      });
      if (!response.ok) {
        const payload = (await response.json().catch(() => null)) as
          | { errors?: string[]; error?: string }
          | null;
        throw new Error(payload?.errors?.[0] ?? payload?.error ?? "Не удалось удалить");
      }
      onArchived(signal.id);
    } catch (value) {
      setEditError(value instanceof Error ? value.message : "Ошибка удаления");
      setArchivePending(false);
    }
  }

  return createPortal(
    <div
      className={styles.overlay}
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) onClose();
      }}
    >
      <div
        ref={dialogRef}
        className={styles.dialog}
        role="dialog"
        aria-modal="true"
        aria-labelledby="signal-modal-title"
        onKeyDown={keepFocusInside}
      >
        <button
          ref={closeButtonRef}
          className={styles.close}
          type="button"
          aria-label="Закрыть окно"
          onClick={onClose}
        >
          ×
        </button>

        <h2 id="signal-modal-title">{editing ? "Редактирование сигнала" : signal.title}</h2>

        {editing ? (
          <SignalForm
            key={`edit-${signal.id}`}
            mode="edit"
            initial={signal}
            pending={editPending}
            error={editError}
            onCancel={() => {
              setEditing(false);
              setEditError("");
            }}
            onSubmit={handleEdit}
          />
        ) : (
          <>
            <Image
              src={signal.image}
              alt={signal.imageAlt}
              width={900}
              height={600}
              className={styles.image}
              sizes="(max-width: 700px) calc(100vw - 48px), 720px"
            />

            <p>{signal.summary}</p>
            <p>
              <strong>Тип:</strong> {signal.category}
            </p>
            <p>
              <strong>Место:</strong> {signal.location}
            </p>
            <div className={styles.authorRow}>
              <UserAvatar
                name={signal.author.name}
                avatarUrl={signal.author.avatarUrl}
                gender={signal.author.gender}
                className={styles.authorAvatar}
              />
              <div className={styles.authorText}>
                <p>
                  <strong>Опубликовал:</strong> {signal.author.name}
                </p>
                <time dateTime={signal.createdAt} className={styles.publishedAt}>
                  {formatPublishedAt(signal.createdAt)}
                </time>
              </div>
            </div>

            {editError ? <p className="form-error">{editError}</p> : null}

            <div className={styles.actions}>
              {authReady && user ? (
                <TrackToggle
                  tracked={signal.isTracked}
                  pending={pending}
                  title={signal.title}
                  onClick={onToggleTracked}
                />
              ) : (
                <Link href="/auth/login" className="btn btnGhost">
                  Войдите, чтобы отслеживать
                </Link>
              )}

              {signal.isOwn ? (
                <>
                  <button
                    type="button"
                    className="btn btnGhost"
                    onClick={() => {
                      setEditError("");
                      setEditing(true);
                    }}
                  >
                    Редактировать
                  </button>
                  <button
                    type="button"
                    className="btn btnDanger"
                    disabled={archivePending}
                    onClick={() => void handleArchive()}
                  >
                    {archivePending ? "В архив…" : "Удалить в архив"}
                  </button>
                </>
              ) : null}
            </div>
          </>
        )}
      </div>
    </div>,
    document.body,
  );
}

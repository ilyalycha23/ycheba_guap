// Создаёт доступное модальное окно с изображением, действиями и управлением фокусом.

"use client";

import Image from "next/image";
import Link from "next/link";
import { useEffect, useRef, type KeyboardEvent as ReactKeyboardEvent } from "react";
import { createPortal } from "react-dom";
import { useAuth } from "../../providers/AuthProvider";
import type { NeighborSignalDTO } from "./SignalsGallery";
import styles from "./PhotoModal.module.css";

// Типизируем входные свойства компонента.
type PhotoModalProps = {
  signal: NeighborSignalDTO;
  pending: boolean;
  onToggleTracked: () => void;
  onClose: () => void;
  returnFocusTo: HTMLElement | null;
};

// Собираем селектор элементов, которые могут получать фокус.
const focusableSelector = [
  "a[href]",
  "button:not([disabled])",
  "input:not([disabled])",
  "select:not([disabled])",
  "textarea:not([disabled])",
  '[tabindex]:not([tabindex="-1"])',
].join(",");

// Объявляем основной компонент этого файла.
export default function PhotoModal({
  signal,
  pending,
  onToggleTracked,
  onClose,
  returnFocusTo,
}: PhotoModalProps) {
  const { user, status } = useAuth();
  const authReady = status !== "loading";
  const dialogRef = useRef<HTMLDivElement>(null);
  const closeButtonRef = useRef<HTMLButtonElement>(null);

  // Синхронизируем компонент с браузерными событиями или внешним API.
  useEffect(() => {
    const previousOverflow = document.documentElement.style.overflow;
    document.documentElement.style.overflow = "hidden";
    closeButtonRef.current?.focus();

    function handleEscape(event: globalThis.KeyboardEvent) {
      if (event.key === "Escape") onClose();
    }

    window.addEventListener("keydown", handleEscape);

    // В cleanup освобождаем подписки и внешние ресурсы эффекта.
    return () => {
      window.removeEventListener("keydown", handleEscape);
      document.documentElement.style.overflow = previousOverflow;
      returnFocusTo?.focus();
    };
  }, [onClose, returnFocusTo]);

  // Не выпускаем клавиатурный фокус за границы открытого интерфейса.
  function keepFocusInside(event: ReactKeyboardEvent<HTMLDivElement>) {
    if (event.key !== "Tab") return;

    const focusable = Array.from(
      dialogRef.current?.querySelectorAll<HTMLElement>(focusableSelector) ?? [],
    );

    if (focusable.length === 0) {
      // Отменяем стандартное действие события и выполняем собственную логику.
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

  // Рендерим окно в document.body поверх основного интерфейса.
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

        <h2 id="signal-modal-title">{signal.title}</h2>

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

        <div className={styles.actions}>
          {authReady && user ? (
            <button type="button" disabled={pending} onClick={onToggleTracked}>
              {signal.isTracked ? "Не отслеживать сигнал" : "Отслеживать сигнал"}
            </button>
          ) : (
            <Link href="/auth/login">Войдите, чтобы отслеживать сигнал</Link>
          )}
        </div>
      </div>
    </div>,
    document.body,
  );
}

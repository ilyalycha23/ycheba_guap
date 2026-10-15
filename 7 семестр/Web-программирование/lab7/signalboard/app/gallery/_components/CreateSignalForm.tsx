"use client";

import Link from "next/link";
import { useState } from "react";
import { useAuth } from "@/app/providers/AuthProvider";
import type { NeighborSignalDTO } from "./SignalsGallery";
import SignalForm from "./SignalForm";
import styles from "./CreateSignalForm.module.css";

type Props = {
  onCreated: (signal: NeighborSignalDTO) => void;
};

export default function CreateSignalForm({ onCreated }: Props) {
  const { status } = useAuth();
  const [open, setOpen] = useState(false);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState("");
  const [ok, setOk] = useState("");
  const [formKey, setFormKey] = useState(0);

  if (status !== "authenticated") {
    return (
      <div className={styles.guest}>
        <p>Чтобы опубликовать сигнал для соседей, войдите в аккаунт.</p>
        <Link href="/auth/login" className="btn btnPrimary">
          Войти
        </Link>
      </div>
    );
  }

  async function handleSubmit(body: FormData) {
    setError("");
    setOk("");
    setPending(true);
    try {
      const response = await fetch("/api/signals", {
        method: "POST",
        credentials: "same-origin",
        body,
      });
      const payload = (await response.json().catch(() => null)) as
        | { signal?: NeighborSignalDTO; errors?: string[]; error?: string }
        | null;
      if (!response.ok) {
        throw new Error(
          payload?.errors?.[0] ?? payload?.error ?? "Не удалось создать сигнал",
        );
      }
      if (!payload?.signal) throw new Error("Пустой ответ сервера");
      onCreated(payload.signal);
      setOk("Сигнал опубликован");
      setFormKey((value) => value + 1);
      setOpen(false);
    } catch (value) {
      setError(value instanceof Error ? value.message : "Ошибка сохранения");
    } finally {
      setPending(false);
    }
  }

  return (
    <section className={styles.section} aria-labelledby="create-signal-heading">
      <div className={styles.head}>
        <div>
          <h2 id="create-signal-heading">Новый сигнал</h2>
          <p className={styles.hint}>
            Название, тип, комментарий и метка на карте обязательны. Фото — по желанию.
          </p>
        </div>
        <div className={styles.headActions}>
          <Link href="/gallery/archive" className="btn btnGhost">
            Архив
          </Link>
          <button
            type="button"
            className={`btn ${open ? "btnGhost" : "btnHot"}`}
            onClick={() => setOpen((value) => !value)}
          >
            {open ? "Скрыть форму" : "Опубликовать сигнал"}
          </button>
        </div>
      </div>

      {ok ? <p className="form-success">{ok}</p> : null}

      {open ? (
        <SignalForm
          key={formKey}
          mode="create"
          pending={pending}
          error={error}
          onSubmit={handleSubmit}
        />
      ) : null}
    </section>
  );
}

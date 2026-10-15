"use client";

import Link from "next/link";
import { useEffect, useRef, useState, type FormEvent } from "react";
import { hasCustomAvatar, resolveAvatarUrl } from "@/app/lib/avatar";
import UserAvatar from "@/app/ui/UserAvatar";
import { useAuth, type UserDTO } from "../providers/AuthProvider";
import AvatarCropper from "./AvatarCropper";
import styles from "./cabinet.module.css";

async function readError(response: Response): Promise<string> {
  const payload = (await response.json().catch(() => null)) as
    | { error?: string; errors?: string[] }
    | null;
  return payload?.errors?.[0] ?? payload?.error ?? "Ошибка запроса";
}

export default function CabinetPage() {
  const { user, status, logout, setUser } = useAuth();
  const fileRef = useRef<HTMLInputElement>(null);

  const [nameDraft, setNameDraft] = useState<string | null>(null);
  const [genderDraft, setGenderDraft] = useState<"male" | "female" | null>(null);
  const [nameMsg, setNameMsg] = useState<{ type: "ok" | "err"; text: string } | null>(null);
  const [namePending, setNamePending] = useState(false);

  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passMsg, setPassMsg] = useState<{ type: "ok" | "err"; text: string } | null>(null);
  const [passPending, setPassPending] = useState(false);

  const [avatarMsg, setAvatarMsg] = useState<{ type: "ok" | "err"; text: string } | null>(null);
  const [avatarPending, setAvatarPending] = useState(false);
  const [cropFile, setCropFile] = useState<File | null>(null);
  const [viewAvatar, setViewAvatar] = useState(false);

  useEffect(() => {
    if (!viewAvatar) return;
    function onKey(event: KeyboardEvent) {
      if (event.key === "Escape") setViewAvatar(false);
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [viewAvatar]);

  if (status === "loading") {
    return (
      <main className={`${styles.page} ${styles.emptyPage}`}>
        <h1>Личный кабинет</h1>
        <p role="status">Проверяем сессию…</p>
      </main>
    );
  }

  if (!user) {
    return (
      <main className={`${styles.page} ${styles.emptyPage}`}>
        <h1>Личный кабинет</h1>
        <p>Чтобы управлять профилем, войдите в аккаунт.</p>
        <Link href="/auth/login" className="btn btnPrimary">
          Перейти ко входу
        </Link>
      </main>
    );
  }

  const name = nameDraft ?? user.name;
  const gender = genderDraft ?? user.gender;
  const displayAvatar = resolveAvatarUrl(user.avatarUrl, gender);
  const customAvatar = hasCustomAvatar(user.avatarUrl);

  async function saveName(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setNameMsg(null);
    setNamePending(true);
    try {
      const response = await fetch("/api/profile", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify({ name, gender }),
      });
      if (!response.ok) throw new Error(await readError(response));
      const payload = (await response.json()) as { user: UserDTO };
      setUser(payload.user);
      setNameDraft(null);
      setGenderDraft(null);
      setNameMsg({ type: "ok", text: "Профиль обновлён" });
    } catch (error) {
      setNameMsg({
        type: "err",
        text: error instanceof Error ? error.message : "Не удалось сохранить профиль",
      });
    } finally {
      setNamePending(false);
    }
  }

  async function savePassword(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setPassMsg(null);
    setPassPending(true);
    try {
      const response = await fetch("/api/profile/password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify({ currentPassword, newPassword, confirmPassword }),
      });
      if (!response.ok) throw new Error(await readError(response));
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
      setPassMsg({ type: "ok", text: "Пароль изменён" });
    } catch (error) {
      setPassMsg({
        type: "err",
        text: error instanceof Error ? error.message : "Не удалось сменить пароль",
      });
    } finally {
      setPassPending(false);
    }
  }

  async function uploadAvatar(blob: Blob) {
    setCropFile(null);
    setAvatarMsg(null);
    setAvatarPending(true);
    try {
      const body = new FormData();
      body.set("avatar", blob, "avatar.jpg");
      const response = await fetch("/api/profile/avatar", {
        method: "POST",
        credentials: "same-origin",
        body,
      });
      if (!response.ok) throw new Error(await readError(response));
      const payload = (await response.json()) as { user: UserDTO };
      setUser(payload.user);
      setAvatarMsg({ type: "ok", text: "Аватар обновлён" });
    } catch (error) {
      setAvatarMsg({
        type: "err",
        text: error instanceof Error ? error.message : "Не удалось загрузить фото",
      });
    } finally {
      setAvatarPending(false);
      if (fileRef.current) fileRef.current.value = "";
    }
  }

  return (
    <main className={styles.page}>
      {cropFile ? (
        <AvatarCropper
          file={cropFile}
          onCancel={() => setCropFile(null)}
          onConfirm={(blob) => void uploadAvatar(blob)}
        />
      ) : null}

      {viewAvatar ? (
        <div
          className={styles.viewer}
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) setViewAvatar(false);
          }}
        >
          <div
            className={styles.viewerDialog}
            role="dialog"
            aria-modal="true"
            aria-label="Фото профиля"
            tabIndex={-1}
          >
            <button
              type="button"
              className={`btn btnGhost ${styles.viewerClose}`}
              onClick={() => setViewAvatar(false)}
            >
              Закрыть
            </button>
            <div className={styles.viewerFrame}>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={displayAvatar} alt={`Фото профиля ${user.name}`} />
            </div>
          </div>
        </div>
      ) : null}

      <div className={styles.layout}>
        <aside className={`${styles.sheet} ${styles.identity}`}>
          <button
            type="button"
            className={`${styles.avatarBtn} ${styles.hasPhoto}`}
            onClick={() => setViewAvatar(true)}
            aria-label="Открыть фото профиля"
          >
            <span className={styles.avatar}>
              <UserAvatar name={user.name} avatarUrl={user.avatarUrl} gender={gender} />
            </span>
            <span className={styles.avatarHint}>Смотреть</span>
          </button>

          <div className={styles.identityMeta}>
            <p className="eyebrow">Личный кабинет</p>
            <h1>{user.name}</h1>
            <p className={styles.email}>{user.email}</p>
          </div>

          <div className={styles.avatarTools}>
            <input
              ref={fileRef}
              className={styles.fileInput}
              id="avatar-file"
              type="file"
              accept="image/jpeg,image/png,image/webp"
              onChange={(event) => {
                const file = event.target.files?.[0];
                if (!file) return;
                if (!["image/jpeg", "image/png", "image/webp"].includes(file.type)) {
                  setAvatarMsg({ type: "err", text: "Допустимы только JPEG, PNG и WebP" });
                } else {
                  setCropFile(file);
                }
                event.target.value = "";
              }}
            />
            <button
              type="button"
              className="btn btnHot"
              disabled={avatarPending}
              onClick={() => fileRef.current?.click()}
            >
              {avatarPending ? "Загрузка…" : customAvatar ? "Сменить фото" : "Загрузить фото"}
            </button>
          </div>
          {avatarMsg ? (
            <p
              className={`${styles.statusLine} ${avatarMsg.type === "ok" ? "form-success" : "form-error"}`}
              role="status"
            >
              {avatarMsg.text}
            </p>
          ) : (
            <p className={`${styles.statusLine} ${styles.hint}`}>
              {customAvatar
                ? "JPEG / PNG / WebP · до 2 МБ"
                : "Сейчас заглушка по полу · JPEG / PNG / WebP · до 2 МБ"}
            </p>
          )}

          <div className={styles.footerActions}>
            <Link href="/gallery" className="btn btnGhost">
              К сигналам
            </Link>
            <button type="button" className="btn btnGhost" onClick={() => void logout()}>
              Выйти
            </button>
          </div>
        </aside>

        <div className={styles.settings}>
          <form className={`${styles.sheet} ${styles.section}`} onSubmit={saveName}>
            <div className={styles.sectionHead}>
              <h2>Имя</h2>
              <p className={styles.hint}>Так вас видят соседи в меню и в кабинете.</p>
            </div>
            <div className={styles.field}>
              <label htmlFor="profile-name">Отображаемое имя</label>
              <input
                id="profile-name"
                value={name}
                onChange={(event) => setNameDraft(event.target.value)}
                minLength={2}
                maxLength={80}
                required
              />
            </div>
            <div className={styles.field}>
              <label htmlFor="profile-gender">Пол</label>
              <select
                id="profile-gender"
                value={gender}
                onChange={(event) =>
                  setGenderDraft(event.target.value === "female" ? "female" : "male")
                }
              >
                <option value="male">Мужской</option>
                <option value="female">Женский</option>
              </select>
            </div>
            <div className={styles.actions}>
              <button type="submit" className="btn btnPrimary" disabled={namePending}>
                {namePending ? "Сохранение…" : "Сохранить"}
              </button>
            </div>
            {nameMsg ? (
              <p className={nameMsg.type === "ok" ? "form-success" : "form-error"} role="status">
                {nameMsg.text}
              </p>
            ) : null}
          </form>

          <form className={`${styles.sheet} ${styles.section}`} onSubmit={savePassword}>
            <div className={styles.sectionHead}>
              <h2>Пароль</h2>
              <p className={styles.hint}>
                Новый пароль — не короче 8 символов. Нельзя поставить текущий или ранее
                использованный.
              </p>
            </div>
            <div className={styles.field}>
              <label htmlFor="current-password">Текущий пароль</label>
              <input
                id="current-password"
                type="password"
                autoComplete="current-password"
                value={currentPassword}
                onChange={(event) => setCurrentPassword(event.target.value)}
                required
              />
            </div>
            <div className={styles.pair}>
              <div className={styles.field}>
                <label htmlFor="new-password">Новый пароль</label>
                <input
                  id="new-password"
                  type="password"
                  autoComplete="new-password"
                  minLength={8}
                  value={newPassword}
                  onChange={(event) => setNewPassword(event.target.value)}
                  required
                />
              </div>
              <div className={styles.field}>
                <label htmlFor="confirm-password">Повтор нового пароля</label>
                <input
                  id="confirm-password"
                  type="password"
                  autoComplete="new-password"
                  minLength={8}
                  value={confirmPassword}
                  onChange={(event) => setConfirmPassword(event.target.value)}
                  required
                />
              </div>
            </div>
            {passMsg ? (
              <p className={passMsg.type === "ok" ? "form-success" : "form-error"} role="status">
                {passMsg.text}
              </p>
            ) : null}
            <div className={styles.actions}>
              <button type="submit" className="btn btnPrimary" disabled={passPending}>
                {passPending ? "Сохранение…" : "Сменить пароль"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </main>
  );
}


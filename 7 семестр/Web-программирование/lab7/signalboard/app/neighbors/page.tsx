"use client";

import { useCallback, useEffect, useState } from "react";
import UserAvatar from "@/app/ui/UserAvatar";
import styles from "./neighbors.module.css";

type NeighborDTO = {
  id: string;
  name: string;
  gender: "male" | "female";
  avatarUrl: string;
  hasCustomAvatar: boolean;
};

export default function NeighborsPage() {
  const [users, setUsers] = useState<NeighborDTO[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [reloadKey, setReloadKey] = useState(0);

  const retry = useCallback(() => setReloadKey((value) => value + 1), []);

  useEffect(() => {
    const controller = new AbortController();

    async function loadUsers() {
      setLoading(true);
      setError("");
      try {
        const response = await fetch("/api/users", {
          cache: "no-store",
          signal: controller.signal,
        });
        if (!response.ok) throw new Error("Не удалось загрузить соседей");
        const payload = (await response.json()) as { users: NeighborDTO[] };
        setUsers(payload.users);
      } catch (value) {
        if (value instanceof DOMException && value.name === "AbortError") return;
        setError(value instanceof Error ? value.message : "Ошибка загрузки");
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    }

    void loadUsers();
    return () => controller.abort();
  }, [reloadKey]);

  return (
    <main className={styles.page}>
      <header className={styles.hero}>
        <p className="eyebrow">Двор</p>
        <h1>Соседи</h1>
        <p className={styles.lead}>
          Все зарегистрированные пользователи SignalBoard. Пока показываем имя и фото.
        </p>
      </header>

      {loading ? <p className={styles.status}>Загружаем список…</p> : null}
      {error ? (
        <div className={styles.empty}>
          <p className="form-error">{error}</p>
          <button type="button" className="btn btnGhost" onClick={retry}>
            Повторить
          </button>
        </div>
      ) : null}

      {!loading && !error && users.length === 0 ? (
        <div className={styles.empty}>
          <p>Пока никто не зарегистрирован.</p>
        </div>
      ) : null}

      {!loading && !error && users.length > 0 ? (
        <ul className={styles.grid}>
          {users.map((user) => (
            <li key={user.id} className={styles.card}>
              <div className={styles.avatar}>
                <UserAvatar name={user.name} avatarUrl={user.avatarUrl} gender={user.gender} />
              </div>
              <h2 className={styles.name}>{user.name}</h2>
            </li>
          ))}
        </ul>
      ) : null}
    </main>
  );
}

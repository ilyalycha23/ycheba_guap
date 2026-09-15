// Показывает гостевой экран либо сведения о вошедшем пользователе.

"use client";

import Link from "next/link";
import { useDemoAuth } from "../providers/DemoAuthProvider";

// Объявляем основной компонент этого файла.
export default function CabinetPage() {
  const { user, logout } = useDemoAuth();

  // Разделяем интерфейс гостя и вошедшего пользователя.
  if (!user) {
    // Возвращаем JSX-разметку, которую React выведет на странице.
    return (
      <main>
        <h1>Личный кабинет</h1>
        <p>В демонстрационном состоянии пользователь отсутствует.</p>
        <Link href="/auth/login">Перейти ко входу</Link>
      </main>
    );
  }

  return (
    <main>
      <h1>Личный кабинет</h1>
      <dl className="profile-list">
        <dt>Имя</dt>
        <dd>{user.name}</dd>
        <dt>Email</dt>
        <dd>{user.email}</dd>
      </dl>
      <button type="button" onClick={logout}>
        Выйти
      </button>
    </main>
  );
}

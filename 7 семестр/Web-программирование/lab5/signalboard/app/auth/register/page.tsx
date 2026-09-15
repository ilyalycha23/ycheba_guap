// Создаёт учебного пользователя после отправки формы регистрации.

"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";
import { useDemoAuth } from "../../providers/DemoAuthProvider";

// Объявляем основной компонент этого файла.
export default function RegisterPage() {
  const router = useRouter();
  const { register } = useDemoAuth();
  // Создаём локальное состояние компонента.
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmation, setConfirmation] = useState("");
  const [error, setError] = useState("");

  // Обрабатываем отправку формы без перезагрузки страницы.
  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    // Отменяем стандартное действие события и выполняем собственную логику.
    event.preventDefault();
    setError("");

    if (password.length < 8) {
      setError("Пароль должен содержать не менее 8 символов.");
      return;
    }

    if (password !== confirmation) {
      setError("Введённые пароли не совпадают.");
      return;
    }

    register(name, email.trim());
    // После успешного действия переходим на следующий маршрут.
    router.push("/cabinet");
  }

  // Возвращаем JSX-разметку, которую React выведет на странице.
  return (
    <main className="form-page">
      <h1>Регистрация</h1>
      <p className="demo-warning">
        Данные существуют только в состоянии текущей вкладки и не записываются в БД.
      </p>

      <form className="auth-form" onSubmit={handleSubmit}>
        <label htmlFor="name">Имя</label>
        <input
          id="name"
          value={name}
          onChange={(event) => setName(event.target.value)}
          autoComplete="name"
          required
        />

        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          autoComplete="email"
          required
        />

        <label htmlFor="password">Пароль</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          autoComplete="new-password"
          minLength={8}
          required
        />

        <label htmlFor="confirmation">Повторите пароль</label>
        <input
          id="confirmation"
          type="password"
          value={confirmation}
          onChange={(event) => setConfirmation(event.target.value)}
          autoComplete="new-password"
          minLength={8}
          required
        />

        {error ? <p className="form-error">{error}</p> : null}

        <button type="submit">Создать учебную запись</button>
      </form>

      <p>
        Уже есть учебная запись? <Link href="/auth/login">Войти</Link>
      </p>
    </main>
  );
}

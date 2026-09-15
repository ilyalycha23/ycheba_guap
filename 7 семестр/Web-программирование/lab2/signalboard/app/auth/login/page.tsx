// Обрабатывает учебный вход и переводит пользователя в личный кабинет.

"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";
import { useDemoAuth } from "../../providers/DemoAuthProvider";

// Объявляем основной компонент этого файла.
export default function LoginPage() {
  const router = useRouter();
  const { login } = useDemoAuth();
  // Создаём локальное состояние компонента.
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  // Обрабатываем отправку формы без перезагрузки страницы.
  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    // Отменяем стандартное действие события и выполняем собственную логику.
    event.preventDefault();
    setError("");

    if (password.length < 8) {
      setError("Введите не менее 8 символов.");
      return;
    }

    login(email.trim());
    // После успешного действия переходим на следующий маршрут.
    router.push("/cabinet");
  }

  // Возвращаем JSX-разметку, которую React выведет на странице.
  return (
    <main className="form-page">
      <h1>Вход</h1>
      <p className="demo-warning">
        Учебный прототип: пароль не проверяется сервером и не сохраняется.
      </p>

      <form className="auth-form" onSubmit={handleSubmit}>
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
          autoComplete="current-password"
          minLength={8}
          required
        />

        {error ? <p className="form-error">{error}</p> : null}

        <button type="submit">Войти в демонстрационном режиме</button>
      </form>

      <p>
        Нет учебной записи? <Link href="/auth/register">Регистрация</Link>
      </p>
    </main>
  );
}

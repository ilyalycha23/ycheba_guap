// Подключает форму входа к POST /api/auth/login через AuthProvider.

"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";
import { useAuth } from "@/app/providers/AuthProvider";

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [error, setError] = useState("");
  const [pending, setPending] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setPending(true);

    const form = new FormData(event.currentTarget);

    try {
      // Передаём пароль серверу только в теле HTTPS-запроса production-среды.
      await login(String(form.get("email") ?? ""), String(form.get("password") ?? ""));
      router.push("/gallery");
    } catch (value) {
      setError(value instanceof Error ? value.message : "Не удалось войти");
    } finally {
      setPending(false);
    }
  }

  return (
    <main className="form-page">
      <h1>Вход</h1>
      <form className="auth-form" onSubmit={handleSubmit}>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          autoComplete="email"
          required
        />

        <label htmlFor="password">Пароль</label>
        <input
          id="password"
          name="password"
          type="password"
          autoComplete="current-password"
          minLength={8}
          required
        />

        {error ? <p role="alert" className="form-error">{error}</p> : null}
        <button type="submit" disabled={pending}>
          {pending ? "Вход…" : "Войти"}
        </button>
      </form>
      <p>
        Нет учебной записи? <Link href="/auth/register">Регистрация</Link>
      </p>
    </main>
  );
}

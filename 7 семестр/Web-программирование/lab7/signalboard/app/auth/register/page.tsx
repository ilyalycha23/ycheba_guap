"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";
import { useAuth } from "@/app/providers/AuthProvider";

export default function RegisterPage() {
  const router = useRouter();
  const { register } = useAuth();
  const [error, setError] = useState("");
  const [pending, setPending] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setPending(true);

    const form = new FormData(event.currentTarget);
    const genderRaw = String(form.get("gender") ?? "");
    const gender = genderRaw === "female" ? "female" : genderRaw === "male" ? "male" : null;

    try {
      if (!gender) throw new Error("Укажите пол: мужской или женский");

      await register({
        name: String(form.get("name") ?? ""),
        email: String(form.get("email") ?? ""),
        password: String(form.get("password") ?? ""),
        confirmPassword: String(form.get("confirmPassword") ?? ""),
        gender,
      });
      router.push("/gallery");
    } catch (value) {
      setError(value instanceof Error ? value.message : "Не удалось зарегистрироваться");
    } finally {
      setPending(false);
    }
  }

  return (
    <main className="form-page">
      <h1>Регистрация</h1>
      <form className="auth-form" method="post" onSubmit={handleSubmit}>
        <label htmlFor="name">Имя пользователя</label>
        <input id="name" name="name" autoComplete="name" required />

        <label htmlFor="email">Email</label>
        <input id="email" name="email" type="email" autoComplete="email" required />

        <label htmlFor="gender">Пол</label>
        <select id="gender" name="gender" required defaultValue="">
          <option value="" disabled>
            Выберите…
          </option>
          <option value="male">Мужской</option>
          <option value="female">Женский</option>
        </select>

        <label htmlFor="password">Пароль</label>
        <input
          id="password"
          name="password"
          type="password"
          autoComplete="new-password"
          minLength={8}
          required
        />

        <label htmlFor="confirmPassword">Повторите пароль</label>
        <input
          id="confirmPassword"
          name="confirmPassword"
          type="password"
          autoComplete="new-password"
          minLength={8}
          required
        />

        {error ? <p role="alert" className="form-error">{error}</p> : null}
        <button type="submit" disabled={pending}>
          {pending ? "Регистрация…" : "Зарегистрироваться"}
        </button>
      </form>
      <p>
        Уже есть учебная запись? <Link href="/auth/login">Войти</Link>
      </p>
    </main>
  );
}

// Нормализует и проверяет непроверенные данные auth-запросов.

export type RegistrationInput = {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
};

// Приводим email к форме, используемой уникальным полем базы.
export function normalizeEmail(value: unknown): string {
  return String(value ?? "").trim().toLowerCase();
}

// Проверяем поля регистрации и возвращаем данные только при успехе.
export function validateRegistration(value: unknown): {
  data: RegistrationInput | null;
  errors: string[];
} {
  const source =
    typeof value === "object" && value !== null
      ? (value as Record<string, unknown>)
      : {};

  const data: RegistrationInput = {
    name: String(source.name ?? "").trim(),
    email: normalizeEmail(source.email),
    password: String(source.password ?? ""),
    confirmPassword: String(source.confirmPassword ?? ""),
  };

  const errors: string[] = [];

  // Проверяем учебные ограничения длины отображаемого имени.
  if (data.name.length < 2 || data.name.length > 80) {
    errors.push("Имя должно содержать от 2 до 80 символов");
  }

  // Выполняем базовую синтаксическую проверку email.
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
    errors.push("Некорректный email");
  }

  // Требуем минимальную длину учебного пароля.
  if (data.password.length < 8) {
    errors.push("Пароль должен содержать не менее 8 символов");
  }

  // Исключаем случайную регистрацию с несовпадающим подтверждением.
  if (data.password !== data.confirmPassword) {
    errors.push("Пароли не совпадают");
  }

  return {
    data: errors.length === 0 ? data : null,
    errors,
  };
}

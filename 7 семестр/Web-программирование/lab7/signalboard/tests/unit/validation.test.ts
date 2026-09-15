// Проверяет чистую нормализацию и server-side validation без базы.

import { describe, expect, test } from "vitest";
import {
  normalizeEmail,
  validateRegistration,
} from "@/app/lib/validation";

describe("normalizeEmail", () => {
  test("удаляет пробелы и приводит email к нижнему регистру", () => {
    expect(normalizeEmail("  Neighbor@Example.TEST ")).toBe(
      "neighbor@example.test",
    );
  });
});

describe("validateRegistration", () => {
  test("принимает корректный набор полей", () => {
    const result = validateRegistration({
      name: "Сосед",
      email: "neighbor@example.test",
      password: "SignalPass_2026!",
      confirmPassword: "SignalPass_2026!",
    });

    expect(result.errors).toEqual([]);
    expect(result.data?.email).toBe("neighbor@example.test");
  });

  test("отклоняет короткий пароль", () => {
    const result = validateRegistration({
      name: "Сосед",
      email: "neighbor@example.test",
      password: "short",
      confirmPassword: "short",
    });

    expect(result.data).toBeNull();
    expect(result.errors).toContain(
      "Пароль должен содержать не менее 8 символов",
    );
  });

  test("отклоняет несовпадающее подтверждение", () => {
    const result = validateRegistration({
      name: "Сосед",
      email: "neighbor@example.test",
      password: "SignalPass_2026!",
      confirmPassword: "Different_2026!",
    });

    expect(result.errors).toContain("Пароли не совпадают");
  });
});

// Проверяет регистрацию, cookie-сессию и сохранение отслеживания после reload.

import "dotenv/config";
import { PrismaClient } from "@prisma/client";
import { expect, test } from "@playwright/test";

const prisma = new PrismaClient();
let testEmail = "";

test.afterAll(async () => {
  // Удаляем только пользователя, созданного этим тестом.
  if (testEmail) {
    await prisma.user.deleteMany({ where: { email: testEmail } });
  }
  await prisma.$disconnect();
});

test("пользователь регистрируется и сохраняет сигнал в отслеживание", async ({
  page,
}) => {
  // Уникальный email исключает конфликт с предыдущим локальным запуском.
  testEmail = `e2e-${Date.now()}@example.test`;

  await page.goto("/auth/register");
  await page.getByLabel("Имя пользователя").fill("E2E сосед");
  await page.getByLabel("Email").fill(testEmail);
  await page.getByLabel("Пароль", { exact: true }).fill("SignalPass_2026!");
  await page.getByLabel("Повторите пароль").fill("SignalPass_2026!");
  await page.getByRole("button", { name: "Зарегистрироваться" }).click();

  // После успешного API-ответа форма переводит пользователя в галерею.
  await expect(page).toHaveURL(/\/gallery$/);

  const addTracked = page.getByRole("button", {
    name: "Добавить в отслеживание: Ищу ключи от подъезда",
  });
  await addTracked.click();

  // Сервер подтвердил изменение, поэтому доступно действие удаления.
  await expect(
    page.getByRole("button", {
      name: "Удалить из отслеживания: Ищу ключи от подъезда",
    }),
  ).toBeVisible();

  // Перезагрузка повторно читает cookie и TrackedSignal из PostgreSQL.
  await page.reload();
  await expect(
    page.getByRole("button", {
      name: "Удалить из отслеживания: Ищу ключи от подъезда",
    }),
  ).toBeVisible();

  // Завершаем сессию через тот же browser context.
  await page.request.post("/api/auth/logout");
  await page.reload();
  await expect(
    page.getByRole("link", { name: "Войдите, чтобы отслеживать сигнал" }).first(),
  ).toBeVisible();
});

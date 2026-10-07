import { chromium } from "@playwright/test";
import fs from "fs";
import path from "path";

const assets =
  "D:/ycheba_guap/7 семестр/Web-программирование/lab2/report_assets";
const browser = await chromium.launch({ channel: "msedge", headless: true });
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });

const tree = fs.readFileSync(path.join(assets, "tree_app.txt"), "utf8");
await page.setContent(
  `<!doctype html><html><body style="margin:0;background:#1e1e1e;color:#d4d4d4;font:16px/1.45 Consolas,monospace;padding:24px;white-space:pre">${tree.replaceAll("<", "&lt;")}</body></html>`,
);
await page.screenshot({
  path: path.join(assets, "fig_tree.png"),
  fullPage: true,
});

await page.goto("http://localhost:3002/start", { waitUntil: "networkidle" });
await page.screenshot({ path: path.join(assets, "fig_start.png") });

await page.goto("http://localhost:3002/signals", { waitUntil: "networkidle" });
await page.screenshot({ path: path.join(assets, "fig_signals.png") });

await page.goto("http://localhost:3002/signals/lost-keys", {
  waitUntil: "networkidle",
});
await page.screenshot({ path: path.join(assets, "fig_signal_id.png") });

await page.goto("http://localhost:3002/auth/login", {
  waitUntil: "networkidle",
});
await page.getByLabel("Email").fill("neighbor@example.test");
await page.getByLabel("Пароль").fill("123");
await page.evaluate(() => {
  const form = document.querySelector("form");
  if (form) form.noValidate = true;
});
await page
  .getByRole("button", { name: "Войти в демонстрационном режиме" })
  .click();
await page.waitForSelector(".form-error");
await page.screenshot({ path: path.join(assets, "fig_login_error.png") });

await page.getByLabel("Пароль").fill("SignalPass_2026!");
await page
  .getByRole("button", { name: "Войти в демонстрационном режиме" })
  .click();
await page.waitForURL(/\/cabinet/);
await page.screenshot({ path: path.join(assets, "fig_cabinet.png") });

await browser.close();
console.log("screenshots ok");

import { chromium } from "@playwright/test";
import fs from "fs";

const assets = "D:/ycheba_guap/7 семестр/Web-программирование/lab7/report_assets";
const url = "http://localhost:3007";
const browser = await chromium.launch({ channel: "msedge", headless: true });
const result = [];
for (const width of [320, 375, 768, 1024, 1440]) {
  const page = await browser.newPage({ viewport: { width, height: 800 } });
  for (const route of ["/start", "/gallery", "/auth/login", "/auth/register"]) {
    await page.goto(url + route, { waitUntil: "networkidle" });
    const m = await page.evaluate(() => ({
      sw: document.documentElement.scrollWidth,
      cw: document.documentElement.clientWidth,
    }));
    result.push({ width, route, overflow: m.sw > m.cw });
  }
  await page.close();
}
const page = await browser.newPage({ viewport: { width: 375, height: 740 }, deviceScaleFactor: 2 });
await page.goto(url + "/start", { waitUntil: "networkidle" });
await page.getByRole("button", { name: "Открыть меню" }).click();
const menu = page.getByRole("dialog", { name: "Основное меню" });
await menu.waitFor();
await page.keyboard.press("Escape");
await menu.waitFor({ state: "detached" });
await page.getByRole("button", { name: "Открыть меню" }).click();
await menu.waitFor();
await page.waitForTimeout(300);
await page.screenshot({ path: `${assets}/fig_burger_375.png` });
await page.getByRole("link", { name: "О проекте" }).click();
await page.waitForURL(/\/about/);
const closedAfterNav = (await page.getByRole("dialog", { name: "Основное меню" }).count()) === 0;
await browser.close();
const summary = { matrix: result, anyOverflow: result.some((r) => r.overflow), burgerEscape: true, closedAfterNav };
fs.writeFileSync(`${assets}/recheck.json`, JSON.stringify(summary, null, 2));
console.log(JSON.stringify({ anyOverflow: summary.anyOverflow, closedAfterNav }));

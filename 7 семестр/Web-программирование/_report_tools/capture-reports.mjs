import { chromium } from "@playwright/test";
import fs from "fs";
import path from "path";

const base = "D:/ycheba_guap/7 семестр/Web-программирование";
const only = process.argv.slice(2).map(Number);
const want = (n) => only.length === 0 || only.includes(n);

const browser = await chromium.launch({ channel: "msedge", headless: true });

function esc(s) {
  return s.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
}

async function terminal(assets, txt, png, title) {
  const file = path.join(assets, txt);
  if (!fs.existsSync(file)) return;
  const text = fs.readFileSync(file, "utf8").replace(/^\uFEFF/, "");
  const page = await browser.newPage({ viewport: { width: 1100, height: 400 } });
  await page.setContent(
    `<!doctype html><html><body style="margin:0;background:#0c0c0c;color:#cccccc;font:15px/1.4 Consolas,monospace">
    <div style="background:#2d2d2d;color:#fff;padding:8px 14px;font:13px Segoe UI,Arial">${esc(title)}</div>
    <pre style="margin:0;padding:16px 18px;white-space:pre-wrap">${esc(text)}</pre></body></html>`,
  );
  await page.screenshot({ path: path.join(assets, png), fullPage: true });
  await page.close();
}

async function demoLogin(page, url) {
  await page.goto(`${url}/auth/login`, { waitUntil: "networkidle" });
  await page.getByLabel("Email").fill("neighbor@example.test");
  await page.getByLabel("Пароль").fill("SignalPass_2026!");
  await page.getByRole("button", { name: /Войти/ }).click();
  await page.waitForURL(/\/cabinet/);
}

async function goGalleryByMenu(page) {
  await page.getByRole("button", { name: "Открыть меню" }).click();
  await page.getByRole("link", { name: /Галерея/ }).click();
  await page.waitForURL(/\/gallery/);
  await page.waitForTimeout(800);
}

// ---------- ЛР3 ----------
if (want(3)) {
  const assets = `${base}/lab3/report_assets`;
  const url = "http://localhost:3003";
  await terminal(assets, "tree_app.txt", "fig_tree.png", "Структура каталога app");
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });

  await page.goto(`${url}/gallery`, { waitUntil: "networkidle" });
  await page.waitForTimeout(800);
  await page.screenshot({ path: `${assets}/fig_gallery.png` });

  await page.locator("button", { hasText: "Потерялись ключи" }).first().click().catch(async () => {
    await page.locator("main button").first().click();
  });
  await page.getByRole("dialog").waitFor();
  await page.waitForTimeout(500);
  await page.screenshot({ path: `${assets}/fig_modal_guest.png` });
  await page.keyboard.press("Escape");

  await page.getByRole("button", { name: "Открыть меню" }).click();
  await page.getByRole("dialog", { name: "Основное меню" }).waitFor();
  await page.waitForTimeout(400);
  await page.screenshot({ path: `${assets}/fig_burger.png` });
  await page.keyboard.press("Escape");

  await page.locator("#map-title").scrollIntoViewIfNeeded();
  await page.waitForTimeout(300);
  await page.screenshot({ path: `${assets}/fig_map_nokey.png` });

  await demoLogin(page, url);
  await goGalleryByMenu(page);
  await page.locator("main button").first().click();
  await page.getByRole("dialog").waitFor();
  await page.waitForTimeout(500);
  await page.screenshot({ path: `${assets}/fig_modal_user.png` });
  await page.getByRole("button", { name: "Отслеживать сигнал" }).click();
  await page.waitForTimeout(300);
  await page.screenshot({ path: `${assets}/fig_modal_tracked.png` });
  await page.close();
  await terminal(assets, "lint_output.txt", "fig_lint.png", "npm run lint");
  await terminal(assets, "build_output.txt", "fig_build.png", "npm run build");
  console.log("lab3 ok");
}

// ---------- ЛР4 ----------
if (want(4)) {
  const assets = `${base}/lab4/report_assets`;
  const url = "http://localhost:3004";
  const matrix = [];
  for (const width of [320, 375, 768, 1024, 1440]) {
    const page = await browser.newPage({ viewport: { width, height: 900 } });
    for (const route of ["/start", "/signals", "/gallery", "/auth/login"]) {
      await page.goto(`${url}${route}`, { waitUntil: "networkidle" });
      await page.waitForTimeout(300);
      const m = await page.evaluate(() => ({
        scrollWidth: document.documentElement.scrollWidth,
        clientWidth: document.documentElement.clientWidth,
        columns: (() => {
          const grid = document.querySelector("main [class*='grid']");
          return grid ? getComputedStyle(grid).gridTemplateColumns.split(" ").length : null;
        })(),
      }));
      matrix.push({ width, route, ...m, overflow: m.scrollWidth > m.clientWidth });
    }
    await page.goto(`${url}/gallery`, { waitUntil: "networkidle" });
    await page.waitForTimeout(600);
    await page.screenshot({ path: `${assets}/fig_gallery_${width}.png`, fullPage: width <= 768 ? false : false });
    await page.close();
  }

  const narrow = await browser.newPage({ viewport: { width: 375, height: 740 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 });
  await narrow.goto(`${url}/gallery`, { waitUntil: "networkidle" });
  await narrow.waitForTimeout(600);
  await narrow.screenshot({ path: `${assets}/fig_375.png` });
  await narrow.locator("main button").first().click();
  await narrow.getByRole("dialog").waitFor();
  await narrow.waitForTimeout(500);
  await narrow.screenshot({ path: `${assets}/fig_modal_375.png` });
  await narrow.keyboard.press("Escape");
  await narrow.getByRole("button", { name: "Открыть меню" }).click();
  await narrow.getByRole("dialog", { name: "Основное меню" }).waitFor();
  await narrow.waitForTimeout(400);
  await narrow.screenshot({ path: `${assets}/fig_burger_375.png` });
  await narrow.close();

  const wide = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await wide.goto(`${url}/gallery`, { waitUntil: "networkidle" });
  await wide.waitForTimeout(600);
  await wide.screenshot({ path: `${assets}/fig_1440.png` });
  await wide.setViewportSize({ width: 800, height: 900 });
  await wide.locator("#map-title").scrollIntoViewIfNeeded();
  await wide.waitForTimeout(500);
  await wide.screenshot({ path: `${assets}/fig_map_resized.png` });
  await wide.close();

  const zoom = await browser.newPage({ viewport: { width: 640, height: 400 }, deviceScaleFactor: 2 });
  await zoom.goto(`${url}/gallery`, { waitUntil: "networkidle" });
  await zoom.waitForTimeout(600);
  const z = await zoom.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
  }));
  await zoom.screenshot({ path: `${assets}/fig_zoom200.png` });
  await zoom.close();

  fs.writeFileSync(`${assets}/matrix.json`, JSON.stringify({ matrix, zoom200: z }, null, 2));

  for (const name of ["baseline_2", "final_2"]) {
    const lhPage = await browser.newPage({ viewport: { width: 1100, height: 900 } });
    await lhPage.goto(`file:///${assets}/lighthouse/${name}.report.html`, { waitUntil: "load" });
    await lhPage.addStyleTag({ content: "*{animation:none!important;transition:none!important}" }); await lhPage.waitForTimeout(3500);
    await lhPage.screenshot({ path: `${assets}/fig_lh_${name}.png`, clip: { x: 0, y: 0, width: 1100, height: 135 } });
    await lhPage.close();
  }
  await terminal(assets, "lint_output.txt", "fig_lint.png", "npm run lint");
  await terminal(assets, "build_output.txt", "fig_build.png", "npm run build");
  console.log("lab4 ok");
}

// ---------- ЛР5 ----------
if (want(5)) {
  const assets = `${base}/lab5/report_assets`;
  await terminal(assets, "tree_new.txt", "fig_tree.png", "Новые файлы проекта");
  await terminal(assets, "prisma_version.txt", "fig_prisma_version.png", "npx prisma --version");
  await terminal(assets, "prisma_validate.txt", "fig_prisma_validate.png", "npm run prisma:format && npm run prisma:validate");
  await terminal(assets, "prisma_generate.txt", "fig_prisma_generate.png", "npm run prisma:generate");
  await terminal(assets, "db_check_nodb.txt", "fig_db_check_nodb.png", "npm run db:check (служба PostgreSQL не запущена)");
  await terminal(assets, "lint_output.txt", "fig_lint.png", "npm run lint");
  await terminal(assets, "build_output.txt", "fig_build.png", "npm run build");
  console.log("lab5 ok");
}

// ---------- ЛР6 ----------
if (want(6)) {
  const assets = `${base}/lab6/report_assets`;
  await terminal(assets, "prisma_validate.txt", "fig_prisma_validate.png", "npm run prisma:validate");
  await terminal(assets, "http_guest.txt", "fig_http_guest.png", "node http-check.mjs — HTTP-запросы к API без входа");
  await terminal(assets, "lint_output.txt", "fig_lint.png", "npm run lint");
  await terminal(assets, "build_output.txt", "fig_build.png", "npm run build");
  console.log("lab6 ok");
}

// ---------- ЛР7 ----------
if (want(7)) {
  const assets = `${base}/lab7/report_assets`;
  const url = "http://localhost:3007";
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  await page.goto(`${url}/gallery`, { waitUntil: "networkidle" });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: `${assets}/fig_gallery_error.png` });
  await page.goto(`${url}/auth/register`, { waitUntil: "networkidle" });
  await page.screenshot({ path: `${assets}/fig_register.png` });
  await page.close();
  await terminal(assets, "unit_output.txt", "fig_unit.png", "npm run test:unit");
  await terminal(assets, "http_guest.txt", "fig_http_guest.png", "node http-check.mjs — HTTP-запросы к API без входа");
  await terminal(assets, "lint_output.txt", "fig_lint.png", "npm run lint");
  await terminal(assets, "build_output.txt", "fig_build.png", "npm run build");
  console.log("lab7 ok");
}

await browser.close();
console.log("done");

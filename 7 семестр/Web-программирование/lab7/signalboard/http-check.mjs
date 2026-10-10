import fs from "fs";

const [, , baseUrl, outFile, withSignals] = process.argv;

const cases = [
  ["GET", "/api/auth/me", null, {}],
  ["POST", "/api/favorites/00000000-0000-4000-8000-000000000001", null, {}],
  ["DELETE", "/api/favorites/00000000-0000-4000-8000-000000000001", null, {}],
  [
    "POST",
    "/api/favorites/00000000-0000-4000-8000-000000000001",
    null,
    { cookie: "signal_session=forged.token.value" },
  ],
  ["POST", "/api/auth/register", { name: "", email: "bad", password: "short", confirmPassword: "x" }, {}],
  ["POST", "/api/auth/login", { email: "", password: "" }, {}],
  ["POST", "/api/auth/logout", null, {}],
];
if (withSignals === "signals") cases.unshift(["GET", "/api/signals", null, {}]);

const lines = [];
for (const [method, path, body, headers] of cases) {
  const response = await fetch(baseUrl + path, {
    method,
    headers: { ...(body ? { "content-type": "application/json" } : {}), ...headers },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await response.text();
  const extra = headers.cookie ? `  (Cookie: ${headers.cookie})` : "";
  lines.push(`$ ${method} ${path}${extra}`);
  if (body) lines.push(`  body: ${JSON.stringify(body)}`);
  lines.push(`HTTP ${response.status} ${response.statusText}`);
  const setCookie = response.headers.get("set-cookie");
  if (setCookie) lines.push(`set-cookie: ${setCookie}`);
  lines.push(text, "");
}
fs.writeFileSync(outFile, lines.join("\n"), "utf8");
console.log(lines.join("\n"));

// Настраивает быстрые unit tests чистой серверной логики.

import { defineConfig } from "vitest/config";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  // Поддерживаем алиасы путей из tsconfig.json.
  plugins: [tsconfigPaths()],
  test: {
    // Чистая валидация не требует DOM или браузера.
    environment: "node",
    include: ["tests/unit/**/*.test.ts"],
  },
});

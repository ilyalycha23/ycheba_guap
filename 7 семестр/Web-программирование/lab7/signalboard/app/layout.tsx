// Подключает реальный AuthProvider вместо учебного DemoAuthProvider.

import type { Metadata, Viewport } from "next";
import type { ReactNode } from "react";
import AuthProvider from "./providers/AuthProvider";
import BurgerMenu from "./ui/BurgerMenu/BurgerMenu";
import "./globals.css";

export const metadata: Metadata = {
  title: "SignalBoard",
  description: "Доска локальных сигналов соседям",
};

export const viewport: Viewport = {
  themeColor: "#eef3f8",
  colorScheme: "light",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  // Провайдер обслуживает только клиентские потребители auth-состояния.
  return (
    <html lang="ru">
      <body>
        <AuthProvider>
          <BurgerMenu />
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}

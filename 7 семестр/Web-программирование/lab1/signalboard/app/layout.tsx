// Задаёт корневой layout, метаданные и общую HTML-оболочку приложения.

import type { Metadata } from "next";
import type { ReactNode } from "react";
import "./globals.css";

// Задаём заголовок и описание страницы для Metadata API.
export const metadata: Metadata = {
  title: "SignalBoard",
  description: "Доска локальных сигналов соседям",
};

// Типизируем дочернее содержимое корневого layout.
type RootLayoutProps = Readonly<{
  children: ReactNode;
}>;

// Объявляем основной компонент этого файла.
export default function RootLayout({ children }: RootLayoutProps) {
  // Возвращаем JSX-разметку, которую React выведет на странице.
  return (
    <html lang="ru">
      <body>{children}</body>
    </html>
  );
}

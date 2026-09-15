// Перенаправляет корневой маршрут приложения на стартовую страницу.

import { redirect } from "next/navigation";

// Объявляем основной компонент этого файла.
export default function HomePage() {
  // Выполняем серверное перенаправление на нужный маршрут.
  redirect("/start");
}

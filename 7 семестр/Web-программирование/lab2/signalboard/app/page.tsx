// Перенаправляет корневой маршрут приложения на стартовую страницу.

import { redirect } from "next/navigation";

export default function HomePage() {
  redirect("/start");
}

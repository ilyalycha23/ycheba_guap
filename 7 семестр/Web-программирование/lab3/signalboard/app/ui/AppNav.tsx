// Формирует навигацию, отмечает активный маршрут и показывает состояние пользователя.

"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useDemoAuth } from "../providers/DemoAuthProvider";

// Описываем пункты меню единым массивом.
const links = [
  { href: "/start", label: "Главная" },
  { href: "/signals", label: "Лента" },
  { href: "/about", label: "О проекте" },
  { href: "/cabinet", label: "Кабинет" },
];

function isActive(pathname: string, href: string): boolean {
  return pathname === href || pathname.startsWith(`${href}/`);
}

// Объявляем основной компонент этого файла.
export default function AppNav() {
  const pathname = usePathname();
  const { user, logout } = useDemoAuth();

  // Возвращаем JSX-разметку, которую React выведет на странице.
  return (
    <header className="site-header">
      <Link className="brand" href="/start">
        SignalBoard
      </Link>

      <nav aria-label="Основная навигация">
        <ul className="nav-list">
          {links.map((link) => (
            <li key={link.href}>
              <Link
                className="nav-link"
                href={link.href}
                aria-current={isActive(pathname, link.href) ? "page" : undefined}
              >
                {link.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>

      {user ? (
        <div className="auth-summary">
          <span>{user.name}</span>
          <button type="button" onClick={logout}>
            Выйти
          </button>
        </div>
      ) : (
        <Link className="login-link" href="/auth/login">
          Войти
        </Link>
      )}
    </header>
  );
}

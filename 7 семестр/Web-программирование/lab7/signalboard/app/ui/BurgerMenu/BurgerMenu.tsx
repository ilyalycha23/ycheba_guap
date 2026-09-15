// Реализует доступное бургер-меню с маршрутами и состоянием пользователя.

"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  useEffect,
  useRef,
  useState,
  type KeyboardEvent as ReactKeyboardEvent,
} from "react";
import { useAuth } from "../../providers/AuthProvider";
import styles from "./styles.module.css";

// Описываем пункты меню единым массивом.
const links = [
  { href: "/start", label: "Главная" },
  { href: "/signals", label: "Лента" },
  { href: "/gallery", label: "Галерея и карта" },
  { href: "/about", label: "О проекте" },
  { href: "/cabinet", label: "Кабинет" },
];

// Собираем селектор доступных элементов внутри меню.
const menuFocusableSelector = [
  "a[href]",
  "button:not([disabled])",
  '[tabindex]:not([tabindex="-1"])',
].join(",");

function isActive(pathname: string, href: string): boolean {
  return pathname === href || pathname.startsWith(`${href}/`);
}

// Объявляем основной компонент этого файла.
export default function BurgerMenu() {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  // Создаём локальное состояние компонента.
  const [open, setOpen] = useState(false);
  const openButtonRef = useRef<HTMLButtonElement>(null);
  const closeButtonRef = useRef<HTMLButtonElement>(null);
  const panelRef = useRef<HTMLElement>(null);
  const ignoreCloseRef = useRef(false);

  // Закрываем панель при смене маршрута: layout живёт дольше страницы.
  useEffect(() => {
    setOpen(false);
  }, [pathname]);

  // Синхронизируем компонент с браузерными событиями или внешним API.
  useEffect(() => {
    if (!open) return;

    const previousOverflow = document.documentElement.style.overflow;
    const openButton = openButtonRef.current;
    document.documentElement.style.overflow = "hidden";
    closeButtonRef.current?.focus();

    function handleEscape(event: KeyboardEvent) {
      if (event.key === "Escape") setOpen(false);
    }

    window.addEventListener("keydown", handleEscape);

    // В cleanup освобождаем подписки и внешние ресурсы эффекта.
    return () => {
      window.removeEventListener("keydown", handleEscape);
      document.documentElement.style.overflow = previousOverflow;
      openButton?.focus();
    };
  }, [open]);

  function openMenu() {
    ignoreCloseRef.current = true;
    setOpen(true);
    window.setTimeout(() => {
      ignoreCloseRef.current = false;
    }, 400);
  }

  function closeMenu() {
    setOpen(false);
  }

  function closeMenuIfSettled() {
    if (ignoreCloseRef.current) return;
    setOpen(false);
  }

  // Не выпускаем клавиатурный фокус за границы открытого интерфейса.
  function keepFocusInside(event: ReactKeyboardEvent<HTMLElement>) {
    if (event.key !== "Tab") return;

    const focusable = Array.from(
      panelRef.current?.querySelectorAll<HTMLElement>(menuFocusableSelector) ?? [],
    );
    if (focusable.length === 0) {
      // Отменяем стандартное действие события и выполняем собственную логику.
      event.preventDefault();
      return;
    }

    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  // Возвращаем JSX-разметку, которую React выведет на странице.
  return (
    <>
      <button
        ref={openButtonRef}
        className={styles.openButton}
        type="button"
        aria-label="Открыть меню"
        aria-expanded={open}
        aria-controls="main-menu-panel"
        aria-hidden={open}
        tabIndex={open ? -1 : undefined}
        onClick={(event) => {
          event.stopPropagation();
          openMenu();
        }}
      >
        <span aria-hidden="true">☰</span>
      </button>

      {open ? (
        <div
          className={styles.overlay}
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) closeMenuIfSettled();
          }}
        >
          <section
            ref={panelRef}
            id="main-menu-panel"
            className={styles.panel}
            role="dialog"
            aria-modal="true"
            aria-label="Основное меню"
            onKeyDown={keepFocusInside}
          >
            <div className={styles.header}>
              <Link href="/start" onClick={closeMenu}>
                SignalBoard
              </Link>
              <button
                ref={closeButtonRef}
                type="button"
                aria-label="Закрыть меню"
                onClick={closeMenuIfSettled}
              >
                ×
              </button>
            </div>

            <nav aria-label="Разделы приложения">
              <ul className={styles.list}>
                {links.map((link) => (
                  <li key={link.href}>
                    <Link
                      href={link.href}
                      aria-current={isActive(pathname, link.href) ? "page" : undefined}
                      onClick={closeMenu}
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </nav>

            <div className={styles.authRow}>
              {user ? (
                <>
                  <span>Пользователь: {user.name}</span>
                  <button
                    type="button"
                    onClick={() => {
                      void logout().then(closeMenu);
                    }}
                  >
                    Выйти
                  </button>
                </>
              ) : (
                <Link href="/auth/login" onClick={closeMenu}>
                  Войти / зарегистрироваться
                </Link>
              )}
            </div>
          </section>
        </div>
      ) : null}
    </>
  );
}

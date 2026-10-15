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
import UserAvatar from "../UserAvatar";
import styles from "./styles.module.css";

const links = [
  { href: "/start", label: "Главная" },
  { href: "/gallery", label: "Сигналы" },
  { href: "/neighbors", label: "Соседи" },
  { href: "/about", label: "О проекте" },
];

const menuFocusableSelector = [
  "a[href]",
  "button:not([disabled])",
  '[tabindex]:not([tabindex="-1"])',
].join(",");

function isActive(pathname: string, href: string): boolean {
  return pathname === href || pathname.startsWith(`${href}/`);
}

function AvatarBadge({
  name,
  avatarUrl,
  gender,
  size = "sm",
}: {
  name: string;
  avatarUrl: string | null;
  gender: "male" | "female";
  size?: "sm" | "md";
}) {
  return (
    <span className={`${styles.avatar} ${size === "md" ? styles.avatarMd : ""}`}>
      <UserAvatar name={name} avatarUrl={avatarUrl} gender={gender} />
    </span>
  );
}

export default function SiteHeader() {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const [openedOn, setOpenedOn] = useState<string | null>(null);
  const open = openedOn === pathname;
  const openButtonRef = useRef<HTMLButtonElement>(null);
  const closeButtonRef = useRef<HTMLButtonElement>(null);
  const panelRef = useRef<HTMLElement>(null);
  const ignoreCloseRef = useRef(false);

  useEffect(() => {
    if (!open) return;

    const previousOverflow = document.documentElement.style.overflow;
    const openButton = openButtonRef.current;
    document.documentElement.style.overflow = "hidden";
    closeButtonRef.current?.focus();

    function handleEscape(event: KeyboardEvent) {
      if (event.key === "Escape") setOpenedOn(null);
    }

    window.addEventListener("keydown", handleEscape);
    return () => {
      window.removeEventListener("keydown", handleEscape);
      document.documentElement.style.overflow = previousOverflow;
      openButton?.focus();
    };
  }, [open]);

  function openMenu() {
    ignoreCloseRef.current = true;
    setOpenedOn(pathname);
    window.setTimeout(() => {
      ignoreCloseRef.current = false;
    }, 400);
  }

  function closeMenu() {
    setOpenedOn(null);
  }

  function closeMenuIfSettled() {
    if (ignoreCloseRef.current) return;
    setOpenedOn(null);
  }

  function keepFocusInside(event: ReactKeyboardEvent<HTMLElement>) {
    if (event.key !== "Tab") return;
    const focusable = Array.from(
      panelRef.current?.querySelectorAll<HTMLElement>(menuFocusableSelector) ?? [],
    );
    if (focusable.length === 0) {
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

  const navLinks = (
    <ul className={styles.navList}>
      {links.map((link) => (
        <li key={link.href}>
          <Link
            href={link.href}
            className={styles.navLink}
            aria-current={isActive(pathname, link.href) ? "page" : undefined}
            onClick={closeMenu}
          >
            {link.label}
          </Link>
        </li>
      ))}
    </ul>
  );

  return (
    <>
      <header className={styles.header}>
        <div className={styles.inner}>
          <Link href="/start" className={styles.brand}>
            <span className={styles.brandMark} aria-hidden="true" />
            SignalBoard
          </Link>

          <nav className={styles.desktopNav} aria-label="Разделы приложения">
            {navLinks}
          </nav>

          <div className={styles.desktopAuth}>
            {user ? (
              <>
                <Link href="/cabinet" className={styles.userChip}>
                  <AvatarBadge
                    name={user.name}
                    avatarUrl={user.avatarUrl}
                    gender={user.gender}
                  />
                  <span>{user.name}</span>
                </Link>
                <button
                  type="button"
                  className="btn btnGhost"
                  onClick={() => void logout()}
                >
                  Выйти
                </button>
              </>
            ) : (
              <Link href="/auth/login" className="btn btnPrimary">
                Войти
              </Link>
            )}
          </div>

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
            <span aria-hidden="true" className={styles.burgerIcon}>
              <i />
              <i />
              <i />
            </span>
          </button>
        </div>
      </header>

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
            <div className={styles.panelHeader}>
              <Link href="/start" className={styles.brand} onClick={closeMenu}>
                <span className={styles.brandMark} aria-hidden="true" />
                SignalBoard
              </Link>
              <button
                ref={closeButtonRef}
                type="button"
                className={styles.closeButton}
                aria-label="Закрыть меню"
                onClick={closeMenuIfSettled}
              >
                ×
              </button>
            </div>

            <nav aria-label="Разделы приложения">{navLinks}</nav>

            <div className={styles.authRow}>
              {user ? (
                <>
                  <Link href="/cabinet" className={styles.userChip} onClick={closeMenu}>
                    <AvatarBadge
                      name={user.name}
                      avatarUrl={user.avatarUrl}
                      gender={user.gender}
                      size="md"
                    />
                    <span>{user.name}</span>
                  </Link>
                  <button
                    type="button"
                    className="btn btnGhost"
                    onClick={() => {
                      void logout().then(closeMenu);
                    }}
                  >
                    Выйти
                  </button>
                </>
              ) : (
                <Link href="/auth/login" className="btn btnPrimary" onClick={closeMenu}>
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

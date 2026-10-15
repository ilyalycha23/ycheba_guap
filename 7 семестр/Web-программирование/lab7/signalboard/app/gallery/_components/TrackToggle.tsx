"use client";

import styles from "./TrackToggle.module.css";

type Props = {
  tracked: boolean;
  pending?: boolean;
  onClick: () => void;
  title?: string;
  layout?: "card" | "inline";
};

function PlusIcon() {
  return (
    <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
      <path
        d="M10 4.5v11M4.5 10h11"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
      />
    </svg>
  );
}

function CheckIcon() {
  return (
    <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
      <path
        d="M4.5 10.5 8.2 14.2 15.5 5.8"
        stroke="currentColor"
        strokeWidth="2.2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export default function TrackToggle({
  tracked,
  pending = false,
  onClick,
  title,
  layout = "inline",
}: Props) {
  const label = tracked ? "В отслеживании" : "Отслеживать";
  const aria = title
    ? `${tracked ? "Удалить из отслеживания" : "Добавить в отслеживание"}: ${title}`
    : tracked
      ? "Удалить из отслеживания"
      : "Добавить в отслеживание";

  const button = (
    <button
      type="button"
      className={`${styles.button} ${tracked ? styles.tracked : ""}`}
      disabled={pending}
      aria-pressed={tracked}
      aria-label={aria}
      onClick={onClick}
    >
      <span className={styles.icon}>{tracked ? <CheckIcon /> : <PlusIcon />}</span>
      <span>{pending ? "…" : label}</span>
    </button>
  );

  if (layout === "card") {
    return <div className={styles.cardWrap}>{button}</div>;
  }

  return button;
}

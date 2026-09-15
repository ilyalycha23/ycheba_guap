// Управляет карточками, выбранным объектом, отслеживанием, модальным окном и картой.

"use client";

import Image from "next/image";
import { useCallback, useState } from "react";
import { neighborSignals, type NeighborSignal } from "../../data/signals";
import PhotoMap from "./PhotoMap";
import PhotoModal from "./PhotoModal";
import styles from "./SignalsGallery.module.css";

// Объявляем основной компонент этого файла.
export default function SignalsGallery() {
  // Создаём локальное состояние компонента.
  const [selected, setSelected] = useState<NeighborSignal | null>(null);
  const [trackedIds, setTrackedIds] = useState<Set<string>>(
    () => new Set<string>(),
  );
  const [returnFocusTo, setReturnFocusTo] = useState<HTMLButtonElement | null>(null);

  function openFromCard(signal: NeighborSignal, button: HTMLButtonElement) {
    setReturnFocusTo(button);
    setSelected(signal);
  }

  const openFromMap = useCallback((signal: NeighborSignal) => {
    setReturnFocusTo(null);
    setSelected(signal);
  }, []);

  function closeModal() {
    setSelected(null);
  }

  function toggleTracked(id: string) {
    setTrackedIds((current) => {
      const next = new Set(current);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  // Возвращаем JSX-разметку, которую React выведет на странице.
  return (
    <>
      <div className={styles.grid}>
        {neighborSignals.map((signal) => (
          <button
            className={styles.card}
            type="button"
            key={signal.id}
            onClick={(event) => openFromCard(signal, event.currentTarget)}
          >
            <span className={styles.imageWrap}>
              <Image
                src={signal.image}
                alt={signal.imageAlt}
                fill
                sizes="(max-width: 700px) 100vw, 33vw"
                className={styles.image}
              />
            </span>
            <span className={styles.title}>{signal.title}</span>
            <span className={styles.summary}>{signal.summary}</span>
          </button>
        ))}
      </div>

      <p className={styles.demoNote}>
        Отслеживание в этой работе хранится только до обновления страницы.
      </p>

      <PhotoMap signals={neighborSignals} onSelect={openFromMap} />

      {selected ? (
        <PhotoModal
          signal={selected}
          isTracked={trackedIds.has(selected.id)}
          onToggleTracked={() => toggleTracked(selected.id)}
          onClose={closeModal}
          returnFocusTo={returnFocusTo}
        />
      ) : null}
    </>
  );
}

"use client";

import Image from "next/image";
import {
  COURTYARD_MAP_IMAGE,
  latLngToPercent,
} from "@/app/lib/signal-categories";
import type { NeighborSignalDTO } from "./SignalsGallery";
import styles from "./PhotoMap.module.css";

export default function PhotoMap({
  signals,
  onSelect,
}: {
  signals: NeighborSignalDTO[];
  onSelect: (signal: NeighborSignalDTO) => void;
}) {
  return (
    <section className={styles.section} aria-labelledby="map-title">
      <div className={styles.heading}>
        <h2 id="map-title">Карта двора · Плесецкая, 16</h2>
        <p className={styles.subtitle}>
          Локальная схема только вашего дома и двора — не городская карта.
          Нажмите на метку, чтобы открыть сигнал.
        </p>
      </div>

      <div
        className={styles.canvas}
        role="region"
        aria-label="Схема двора на Плесецкой, 16 с метками сигналов"
      >
        <Image
          src={COURTYARD_MAP_IMAGE}
          alt="Схема дома и двора на Плесецкой улице, 16"
          fill
          sizes="(max-width: 768px) 100vw, 72rem"
          className={styles.basemap}
          priority={false}
        />

        <ul className={styles.pins}>
          {signals.map((signal) => {
            const { left, top } = latLngToPercent(
              signal.latitude,
              signal.longitude,
            );
            return (
              <li
                key={signal.id}
                className={styles.pinItem}
                style={{ left: `${left}%`, top: `${top}%` }}
              >
                <button
                  type="button"
                  className={styles.pin}
                  title={signal.title}
                  aria-label={`Сигнал: ${signal.title}`}
                  onClick={() => onSelect(signal)}
                >
                  <span className={styles.pinDot} aria-hidden="true" />
                  <span className={styles.pinLabel}>{signal.title}</span>
                </button>
              </li>
            );
          })}
        </ul>

        {signals.length === 0 ? (
          <p className={styles.empty}>Пока нет сигналов на карте двора.</p>
        ) : null}
      </div>
    </section>
  );
}

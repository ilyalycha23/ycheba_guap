"use client";

import Image from "next/image";
import { useCallback, type KeyboardEvent, type MouseEvent } from "react";
import {
  COURTYARD_MAP_IMAGE,
  latLngToPercent,
  percentToLatLng,
} from "@/app/lib/signal-categories";
import styles from "./MapPicker.module.css";

type Props = {
  latitude: number;
  longitude: number;
  onChange: (coords: { latitude: number; longitude: number }) => void;
};

export default function MapPicker({ latitude, longitude, onChange }: Props) {
  const { left, top } = latLngToPercent(latitude, longitude);

  const placeFromEvent = useCallback(
    (event: MouseEvent<HTMLDivElement>) => {
      const rect = event.currentTarget.getBoundingClientRect();
      if (rect.width <= 0 || rect.height <= 0) return;
      const leftPercent = ((event.clientX - rect.left) / rect.width) * 100;
      const topPercent = ((event.clientY - rect.top) / rect.height) * 100;
      onChange(percentToLatLng(leftPercent, topPercent));
    },
    [onChange],
  );

  function onKeyDown(event: KeyboardEvent<HTMLDivElement>) {
    const step = event.shiftKey ? 0.00008 : 0.000035;
    let nextLat = latitude;
    let nextLng = longitude;

    if (event.key === "ArrowUp") nextLat += step;
    else if (event.key === "ArrowDown") nextLat -= step;
    else if (event.key === "ArrowLeft") nextLng -= step;
    else if (event.key === "ArrowRight") nextLng += step;
    else return;

    event.preventDefault();
    onChange({ latitude: nextLat, longitude: nextLng });
  }

  return (
    <div className={styles.wrap}>
      <div
        className={styles.canvas}
        role="button"
        tabIndex={0}
        aria-label="Схема двора: кликните, чтобы поставить метку сигнала"
        onClick={placeFromEvent}
        onKeyDown={onKeyDown}
      >
        <Image
          src={COURTYARD_MAP_IMAGE}
          alt=""
          fill
          sizes="(max-width: 768px) 100vw, 40rem"
          className={styles.basemap}
        />
        <span
          className={styles.pin}
          style={{ left: `${left}%`, top: `${top}%` }}
          aria-hidden="true"
        />
      </div>
      <p className={styles.hint}>
        Кликните по схеме двора (Плесецкая, 16), чтобы поставить метку. Стрелки
        клавиатуры двигают точку.
      </p>
    </div>
  );
}

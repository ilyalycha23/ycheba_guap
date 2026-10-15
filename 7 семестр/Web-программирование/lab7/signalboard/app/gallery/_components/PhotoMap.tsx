"use client";

import { useEffect, useRef, useState } from "react";
import { COURTYARD_CENTER } from "@/app/lib/signal-categories";
import { loadYandexMaps, type YandexMap } from "@/app/lib/yandex-maps";
import type { NeighborSignalDTO } from "./SignalsGallery";
import styles from "./PhotoMap.module.css";

export default function PhotoMap({
  signals,
  onSelect,
}: {
  signals: NeighborSignalDTO[];
  onSelect: (signal: NeighborSignalDTO) => void;
}) {
  const containerRef = useRef<HTMLDivElement>(null);
  const apiKey = process.env.NEXT_PUBLIC_YANDEX_MAPS_API_KEY ?? "";
  const [status, setStatus] = useState<"loading" | "ready" | "error" | "no-key">(
    apiKey ? "loading" : "no-key",
  );

  useEffect(() => {
    if (!apiKey || !containerRef.current) return;

    let disposed = false;
    let map: YandexMap | null = null;
    let resizeObserver: ResizeObserver | null = null;

    async function buildMap() {
      try {
        const ymaps = await loadYandexMaps(apiKey);
        if (disposed || !containerRef.current) return;

        const first = signals[0];
        map = new ymaps.Map(containerRef.current, {
          center: first
            ? [first.latitude, first.longitude]
            : [COURTYARD_CENTER.latitude, COURTYARD_CENTER.longitude],
          zoom: 17,
          controls: ["zoomControl"],
        });

        signals.forEach((signal) => {
          const placemark = new ymaps.Placemark(
            [signal.latitude, signal.longitude],
            {
              hintContent: signal.title,
              balloonContent: signal.location,
            },
            {
              preset: "islands#circleDotIcon",
              iconColor: "#134f9c",
            },
          );

          placemark.events.add("click", () => onSelect(signal));
          map?.geoObjects.add(placemark);
        });

        if (signals.length > 0) {
          const bounds = map.geoObjects.getBounds();
          if (bounds) {
            map.setBounds(bounds, { checkZoomRange: true, zoomMargin: 40 });
          }
        }

        if (containerRef.current && typeof ResizeObserver !== "undefined") {
          resizeObserver = new ResizeObserver(() => {
            map?.container.fitToViewport();
          });
          resizeObserver.observe(containerRef.current);
        }

        setStatus("ready");
      } catch {
        if (!disposed) setStatus("error");
      }
    }

    void buildMap();

    return () => {
      disposed = true;
      resizeObserver?.disconnect();
      map?.destroy();
    };
  }, [apiKey, onSelect, signals]);

  return (
    <section className={styles.section} aria-labelledby="map-title">
      <h2 id="map-title">Карта сигналов двора</h2>

      {status === "no-key" ? (
        <p className={styles.status}>
          Добавьте NEXT_PUBLIC_YANDEX_MAPS_API_KEY в файл .env.local.
        </p>
      ) : null}

      {status === "error" ? (
        <p className={styles.status}>Не удалось загрузить карту.</p>
      ) : null}

      {status === "loading" ? (
        <p className={styles.status}>Карта загружается…</p>
      ) : null}

      <div
        ref={containerRef}
        className={styles.canvas}
        role="region"
        aria-label="Интерактивная карта локальных сигналов"
      />
    </section>
  );
}

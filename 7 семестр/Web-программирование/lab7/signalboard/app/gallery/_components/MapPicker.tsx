"use client";

import { useEffect, useRef, useState } from "react";
import { COURTYARD_CENTER } from "@/app/lib/signal-categories";
import {
  loadYandexMaps,
  type YandexMap,
  type YandexPlacemark,
} from "@/app/lib/yandex-maps";
import styles from "./MapPicker.module.css";

type Props = {
  latitude: number;
  longitude: number;
  onChange: (coords: { latitude: number; longitude: number }) => void;
};

export default function MapPicker({ latitude, longitude, onChange }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const onChangeRef = useRef(onChange);
  const apiKey = process.env.NEXT_PUBLIC_YANDEX_MAPS_API_KEY ?? "";
  const [status, setStatus] = useState<"loading" | "ready" | "error" | "no-key">(
    apiKey ? "loading" : "no-key",
  );

  useEffect(() => {
    onChangeRef.current = onChange;
  }, [onChange]);

  useEffect(() => {
    if (!apiKey || !containerRef.current) return;

    let disposed = false;
    let map: YandexMap | null = null;
    let placemark: YandexPlacemark | null = null;

    async function build() {
      try {
        const ymaps = await loadYandexMaps(apiKey);
        if (disposed || !containerRef.current) return;

        const start: [number, number] = [
          latitude || COURTYARD_CENTER.latitude,
          longitude || COURTYARD_CENTER.longitude,
        ];

        map = new ymaps.Map(containerRef.current, {
          center: start,
          zoom: 17,
          controls: ["zoomControl"],
        });

        placemark = new ymaps.Placemark(
          start,
          { hintContent: "Место сигнала" },
          {
            preset: "islands#circleDotIcon",
            iconColor: "#0f766e",
            draggable: true,
          },
        );
        map.geoObjects.add(placemark);

        const publish = (coords: [number, number]) => {
          onChangeRef.current({ latitude: coords[0], longitude: coords[1] });
        };

        map.events.add("click", (event) => {
          const coords = event.get("coords");
          placemark?.geometry.setCoordinates(coords);
          publish(coords);
        });

        placemark.events.add("dragend", () => {
          const coords = placemark?.geometry.getCoordinates();
          if (coords) publish(coords);
        });

        setStatus("ready");
      } catch {
        if (!disposed) setStatus("error");
      }
    }

    void build();

    return () => {
      disposed = true;
      map?.destroy();
    };
    // Карту инициализируем один раз; координаты меняет клик/перетаскивание.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [apiKey]);

  return (
    <div className={styles.wrap}>
      {status === "no-key" ? (
        <p className={styles.status}>Нет ключа карты. Можно указать координаты вручную ниже.</p>
      ) : null}
      {status === "error" ? (
        <p className={styles.status}>Карта недоступна. Укажите координаты вручную.</p>
      ) : null}
      {status === "loading" ? <p className={styles.status}>Карта загружается…</p> : null}
      <div
        ref={containerRef}
        className={styles.canvas}
        role="region"
        aria-label="Выбор места сигнала на карте"
      />
      <p className={styles.hint}>Кликните по карте или перетащите метку.</p>
    </div>
  );
}

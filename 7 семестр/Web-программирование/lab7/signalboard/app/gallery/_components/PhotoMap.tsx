// Загружает API Яндекс Карт, создаёт карту и связывает метки с объектами.

"use client";

import { useEffect, useRef, useState } from "react";
import type { NeighborSignalDTO } from "./SignalsGallery";
import styles from "./PhotoMap.module.css";

// Координаты представлены парой широты и долготы.
type Coordinates = [number, number];

type YandexPlacemark = {
  events: {
    add: (eventName: string, handler: () => void) => void;
  };
};

type YandexMap = {
  container: {
    fitToViewport: () => void;
  };
  geoObjects: {
    add: (placemark: YandexPlacemark) => void;
  };
  destroy: () => void;
};

type YandexMapsApi = {
  ready: (callback: () => void) => void;
  Map: new (
    container: HTMLElement,
    state: { center: Coordinates; zoom: number; controls: string[] },
  ) => YandexMap;
  Placemark: new (
    coordinates: Coordinates,
    properties: { hintContent: string; balloonContent: string },
    options: { preset: string; iconColor: string },
  ) => YandexPlacemark;
};

// Дополняем тип Window объектом, который добавляет внешний API.
declare global {
  interface Window {
    ymaps?: YandexMapsApi;
  }
}

const scriptId = "signalboard-yandex-maps";
let mapsPromise: Promise<YandexMapsApi> | null = null;

// Загружаем скрипт карты один раз и ожидаем готовности API.
function loadMaps(apiKey: string): Promise<YandexMapsApi> {
  if (window.ymaps) {
    return new Promise((resolve) => {
      window.ymaps?.ready(() => resolve(window.ymaps as YandexMapsApi));
    });
  }

  if (mapsPromise) return mapsPromise;

  mapsPromise = new Promise((resolve, reject) => {
    function resolveWhenReady() {
      if (!window.ymaps) {
        mapsPromise = null;
        reject(new Error("Yandex Maps API is unavailable"));
        return;
      }

      window.ymaps.ready(() => resolve(window.ymaps as YandexMapsApi));
    }

    const existing = document.getElementById(scriptId) as HTMLScriptElement | null;
    if (existing) {
      existing.addEventListener("load", resolveWhenReady, { once: true });
      existing.addEventListener("error", () => reject(new Error("Map script error")), {
        once: true,
      });
      return;
    }

    const script = document.createElement("script");
    script.id = scriptId;
    script.src = `https://api-maps.yandex.ru/2.1/?apikey=${encodeURIComponent(apiKey)}&lang=ru_RU`;
    script.async = true;
    script.addEventListener("load", resolveWhenReady, { once: true });
    script.addEventListener(
      "error",
      () => {
        mapsPromise = null;
        reject(new Error("Map script error"));
      },
      { once: true },
    );
    // Подключаем внешний скрипт к документу.
    document.head.appendChild(script);
  });

  return mapsPromise;
}

// Объявляем основной компонент этого файла.
export default function PhotoMap({
  signals,
  onSelect,
}: {
  signals: NeighborSignalDTO[];
  onSelect: (signal: NeighborSignalDTO) => void;
}) {
  const containerRef = useRef<HTMLDivElement>(null);
  // Создаём локальное состояние компонента.
  const apiKey = process.env.NEXT_PUBLIC_YANDEX_MAPS_API_KEY ?? "";
  const [status, setStatus] = useState<"loading" | "ready" | "error" | "no-key">(
    apiKey ? "loading" : "no-key",
  );

  // Синхронизируем компонент с браузерными событиями или внешним API.
  useEffect(() => {
    if (!apiKey) {
      return;
    }

    if (!containerRef.current || signals.length === 0) return;

    let disposed = false;
    let map: YandexMap | null = null;
    let resizeObserver: ResizeObserver | null = null;

    async function buildMap() {
      try {
        const ymaps = await loadMaps(apiKey);
        if (disposed || !containerRef.current) return;

        const first = signals[0];
        // Создаём экземпляр карты в подготовленном DOM-контейнере.
        map = new ymaps.Map(containerRef.current, {
          center: [first.latitude, first.longitude],
          zoom: 15,
          controls: ["zoomControl"],
        });

        // Добавляем на карту метку для каждого сигнала.
        signals.forEach((signal) => {
          // Создаём метку с координатами и данными текущего объекта.
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

        // Следит за размером контейнера и уведомляет карту об изменении viewport.
        if (containerRef.current && typeof ResizeObserver !== "undefined") {
          // Создаём наблюдатель за изменением размеров контейнера.
          resizeObserver = new ResizeObserver(() => {
            // Просим API карты пересчитать доступную область.
            map?.container.fitToViewport();
          });
          // Начинаем наблюдение за DOM-контейнером карты.
          resizeObserver.observe(containerRef.current);
        }

        setStatus("ready");
      } catch {
        if (!disposed) setStatus("error");
      }
    }

    void buildMap();

    // Освобождает наблюдатель и экземпляр карты при размонтировании компонента.
    return () => {
      disposed = true;
      // Отключаем наблюдатель размеров.
      resizeObserver?.disconnect();
      // Уничтожаем экземпляр карты и его обработчики.
      map?.destroy();
    };
  }, [apiKey, onSelect, signals]);

  // Возвращаем JSX-разметку, которую React выведет на странице.
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
        aria-label="Интерактивная карта локальных сигналов"
      />
    </section>
  );
}

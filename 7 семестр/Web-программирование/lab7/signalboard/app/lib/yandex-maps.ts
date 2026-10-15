export type Coordinates = [number, number];

export type YandexPlacemark = {
  geometry: {
    getCoordinates: () => Coordinates;
    setCoordinates: (coords: Coordinates) => void;
  };
  events: {
    add: (eventName: string, handler: () => void) => void;
  };
};

export type YandexMap = {
  container: {
    fitToViewport: () => void;
  };
  setBounds: (
    bounds: [Coordinates, Coordinates],
    options?: { checkZoomRange?: boolean; zoomMargin?: number },
  ) => void;
  events: {
    add: (
      eventName: string,
      handler: (event: { get: (key: string) => Coordinates }) => void,
    ) => void;
  };
  geoObjects: {
    add: (placemark: YandexPlacemark) => void;
    removeAll: () => void;
    getBounds: () => [Coordinates, Coordinates] | null;
  };
  destroy: () => void;
};

export type YandexMapsApi = {
  ready: (callback: () => void) => void;
  Map: new (
    container: HTMLElement,
    state: { center: Coordinates; zoom: number; controls: string[] },
  ) => YandexMap;
  Placemark: new (
    coordinates: Coordinates,
    properties: Record<string, string>,
    options: {
      preset: string;
      iconColor: string;
      draggable?: boolean;
    },
  ) => YandexPlacemark;
};

declare global {
  interface Window {
    ymaps?: YandexMapsApi;
  }
}

const scriptId = "signalboard-yandex-maps";
let mapsPromise: Promise<YandexMapsApi> | null = null;

export function loadYandexMaps(apiKey: string): Promise<YandexMapsApi> {
  if (typeof window === "undefined") {
    return Promise.reject(new Error("Yandex Maps only works in the browser"));
  }

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
    document.head.appendChild(script);
  });

  return mapsPromise;
}

"use client";

import {
  useCallback,
  useEffect,
  useRef,
  useState,
  type PointerEvent as ReactPointerEvent,
} from "react";
import styles from "./ImageCropper.module.css";

type Props = {
  file: File;
  onCancel: () => void;
  onConfirm: (blob: Blob) => void;
  /** width / height. 1 = квадрат, 1.5 = 3:2 для карточки сигнала */
  aspect?: number;
  shape?: "circle" | "rect";
  title?: string;
  outputWidth?: number;
};

export default function ImageCropper({
  file,
  onCancel,
  onConfirm,
  aspect = 1,
  shape = "circle",
  title = "Выберите область фото",
  outputWidth = 512,
}: Props) {
  const viewW = 320;
  const viewH = Math.round(viewW / aspect);
  const outputH = Math.round(outputWidth / aspect);

  const [img, setImg] = useState<HTMLImageElement | null>(null);
  const [zoom, setZoom] = useState(1);
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const drag = useRef<{ x: number; y: number; ox: number; oy: number } | null>(null);
  const dialogRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const url = URL.createObjectURL(file);
    const image = new Image();
    let alive = true;
    image.onload = () => {
      if (alive) setImg(image);
    };
    image.src = url;
    return () => {
      alive = false;
      URL.revokeObjectURL(url);
    };
  }, [file]);

  useEffect(() => {
    dialogRef.current?.focus();
    function onKey(event: KeyboardEvent) {
      if (event.key === "Escape") onCancel();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onCancel]);

  const baseScale = img ? Math.max(viewW / img.width, viewH / img.height) : 1;
  const scale = baseScale * zoom;
  const drawW = img ? img.width * scale : viewW;
  const drawH = img ? img.height * scale : viewH;

  const clamp = useCallback(
    (x: number, y: number) => {
      const maxX = Math.max(0, (drawW - viewW) / 2);
      const maxY = Math.max(0, (drawH - viewH) / 2);
      return {
        x: Math.min(maxX, Math.max(-maxX, x)),
        y: Math.min(maxY, Math.max(-maxY, y)),
      };
    },
    [drawW, drawH, viewW, viewH],
  );

  const pos = clamp(offset.x, offset.y);

  function onPointerDown(event: ReactPointerEvent<HTMLDivElement>) {
    event.currentTarget.setPointerCapture(event.pointerId);
    drag.current = { x: event.clientX, y: event.clientY, ox: pos.x, oy: pos.y };
  }

  function onPointerMove(event: ReactPointerEvent<HTMLDivElement>) {
    if (!drag.current) return;
    const dx = event.clientX - drag.current.x;
    const dy = event.clientY - drag.current.y;
    setOffset(clamp(drag.current.ox + dx, drag.current.oy + dy));
  }

  function onPointerUp() {
    drag.current = null;
  }

  function confirm() {
    if (!img) return;
    const canvas = document.createElement("canvas");
    canvas.width = outputWidth;
    canvas.height = outputH;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const ratioX = outputWidth / viewW;
    const ratioY = outputH / viewH;
    const left = (viewW - drawW) / 2 + pos.x;
    const top = (viewH - drawH) / 2 + pos.y;
    ctx.drawImage(img, left * ratioX, top * ratioY, drawW * ratioX, drawH * ratioY);

    canvas.toBlob(
      (blob) => {
        if (blob) onConfirm(blob);
      },
      "image/jpeg",
      0.92,
    );
  }

  return (
    <div
      className={styles.overlay}
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) onCancel();
      }}
    >
      <div
        ref={dialogRef}
        className={styles.dialog}
        role="dialog"
        aria-modal="true"
        aria-label={title}
        tabIndex={-1}
      >
        <h2 className={styles.title}>{title}</h2>
        <p className={styles.hint}>Перетащите фото и настройте масштаб.</p>

        <div
          className={styles.stage}
          style={{ width: viewW, height: viewH }}
          onPointerDown={onPointerDown}
          onPointerMove={onPointerMove}
          onPointerUp={onPointerUp}
          onPointerCancel={onPointerUp}
        >
          {img ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={img.src}
              alt=""
              draggable={false}
              className={styles.image}
              style={{
                width: drawW,
                height: drawH,
                transform: `translate(calc(-50% + ${pos.x}px), calc(-50% + ${pos.y}px))`,
              }}
            />
          ) : (
            <span className={styles.loading}>Загрузка…</span>
          )}
          <span
            className={shape === "circle" ? styles.maskCircle : styles.maskRect}
            aria-hidden="true"
          />
        </div>

        <label className={styles.zoom}>
          <span>Масштаб</span>
          <input
            type="range"
            min={1}
            max={3}
            step={0.01}
            value={zoom}
            onChange={(event) => setZoom(Number(event.target.value))}
          />
        </label>

        <div className={styles.actions}>
          <button type="button" className="btn btnGhost" onClick={onCancel}>
            Отмена
          </button>
          <button type="button" className="btn btnPrimary" disabled={!img} onClick={confirm}>
            Сохранить
          </button>
        </div>
      </div>
    </div>
  );
}

"use client";

import { useState, type FormEvent } from "react";
import {
  COURTYARD_CENTER,
  SIGNAL_CATEGORIES,
} from "@/app/lib/signal-categories";
import ImageCropper from "@/app/ui/ImageCropper";
import type { NeighborSignalDTO } from "./SignalsGallery";
import MapPicker from "./MapPicker";
import styles from "./CreateSignalForm.module.css";

type Props = {
  mode: "create" | "edit";
  initial?: NeighborSignalDTO | null;
  pending: boolean;
  error: string;
  onCancel?: () => void;
  onSubmit: (form: FormData) => Promise<void>;
};

export default function SignalForm({
  mode,
  initial,
  pending,
  error,
  onCancel,
  onSubmit,
}: Props) {
  const [title, setTitle] = useState(initial?.title ?? "");
  const [summary, setSummary] = useState(initial?.summary ?? "");
  const [category, setCategory] = useState(initial?.category ?? "");
  const [location, setLocation] = useState(
    initial?.location ?? "Плесецкая ул., 16 — двор",
  );
  const [latitude, setLatitude] = useState<number>(
    initial?.latitude ?? COURTYARD_CENTER.latitude,
  );
  const [longitude, setLongitude] = useState<number>(
    initial?.longitude ?? COURTYARD_CENTER.longitude,
  );
  const [photo, setPhoto] = useState<File | null>(null);
  const [photoPreview, setPhotoPreview] = useState<string | null>(null);
  const [cropFile, setCropFile] = useState<File | null>(null);
  const [clearPhoto, setClearPhoto] = useState(false);

  function clearChosenPhoto() {
    if (photoPreview) URL.revokeObjectURL(photoPreview);
    setPhoto(null);
    setPhotoPreview(null);
  }

  function applyCroppedPhoto(blob: Blob) {
    const cropped = new File([blob], "signal.jpg", { type: "image/jpeg" });
    if (photoPreview) URL.revokeObjectURL(photoPreview);
    setPhoto(cropped);
    setPhotoPreview(URL.createObjectURL(cropped));
    setClearPhoto(false);
    setCropFile(null);
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const body = new FormData();
    body.set("title", title);
    body.set("summary", summary);
    body.set("category", category);
    body.set("location", location);
    body.set("latitude", String(latitude));
    body.set("longitude", String(longitude));
    if (photo) body.set("photo", photo);
    if (clearPhoto) body.set("clearPhoto", "1");
    await onSubmit(body);
  }

  return (
    <>
      {cropFile ? (
        <ImageCropper
          file={cropFile}
          aspect={3 / 2}
          shape="rect"
          title="Область фото для объявления"
          outputWidth={900}
          onCancel={() => setCropFile(null)}
          onConfirm={applyCroppedPhoto}
        />
      ) : null}

      <form className={styles.form} onSubmit={(event) => void handleSubmit(event)}>
        <div className={styles.field}>
          <label htmlFor={`${mode}-signal-title`}>Название объявления</label>
          <input
            id={`${mode}-signal-title`}
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            minLength={3}
            maxLength={160}
            required
            placeholder="Например: Нашёл связку ключей у площадки"
          />
        </div>

        <div className={styles.field}>
          <label htmlFor={`${mode}-signal-category`}>Тип объявления</label>
          <select
            id={`${mode}-signal-category`}
            value={category}
            onChange={(event) => setCategory(event.target.value)}
            required
          >
            <option value="" disabled>
              Выберите категорию…
            </option>
            {SIGNAL_CATEGORIES.map((item) => (
              <option key={item.value} value={item.value}>
                {item.label} — {item.hint}
              </option>
            ))}
          </select>
        </div>

        <div className={styles.field}>
          <label htmlFor={`${mode}-signal-summary`}>Комментарий</label>
          <textarea
            id={`${mode}-signal-summary`}
            value={summary}
            onChange={(event) => setSummary(event.target.value)}
            minLength={5}
            maxLength={2000}
            required
            rows={4}
            placeholder="Кратко опишите ситуацию для соседей"
          />
        </div>

        <div className={styles.field}>
          <label htmlFor={`${mode}-signal-location`}>Место (текстом)</label>
          <input
            id={`${mode}-signal-location`}
            value={location}
            onChange={(event) => setLocation(event.target.value)}
            minLength={3}
            maxLength={240}
            required
          />
        </div>

        <div className={styles.field}>
          <label htmlFor={`${mode}-signal-photo`}>Фото объявления</label>
          <input
            id={`${mode}-signal-photo`}
            type="file"
            accept="image/jpeg,image/png,image/webp"
            onChange={(event) => {
              const file = event.target.files?.[0];
              event.target.value = "";
              if (!file) return;
              if (!["image/jpeg", "image/png", "image/webp"].includes(file.type)) {
                return;
              }
              setCropFile(file);
            }}
          />
          <p className={styles.coords}>
            Необязательно. После выбора откроется окно кадрирования 3:2 — как на
            карточке. Без фото будет заглушка типа. JPEG / PNG / WebP · до 2 МБ.
          </p>

          {photoPreview ? (
            <div className={styles.preview}>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={photoPreview} alt="Предпросмотр обрезанного фото" />
              <button type="button" className="btn btnGhost" onClick={clearChosenPhoto}>
                Убрать выбранное фото
              </button>
            </div>
          ) : null}

          {mode === "edit" &&
          !photo &&
          !clearPhoto &&
          initial?.image.startsWith("/uploads/signals/") ? (
            <div className={styles.preview}>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={initial.image} alt="Текущее фото сигнала" />
            </div>
          ) : null}

          {mode === "edit" && initial?.image.startsWith("/uploads/signals/") ? (
            <label className={styles.check}>
              <input
                type="checkbox"
                checked={clearPhoto}
                onChange={(event) => {
                  setClearPhoto(event.target.checked);
                  if (event.target.checked) clearChosenPhoto();
                }}
              />
              Убрать своё фото и вернуть заглушку типа
            </label>
          ) : null}
        </div>

        <div className={styles.field}>
          <span className={styles.label}>Метка на карте</span>
          <MapPicker
            latitude={latitude}
            longitude={longitude}
            onChange={(coords) => {
              setLatitude(coords.latitude);
              setLongitude(coords.longitude);
            }}
          />
          <p className={styles.coords}>
            Координаты: {latitude.toFixed(6)}, {longitude.toFixed(6)}
          </p>
        </div>

        {error ? <p className="form-error">{error}</p> : null}

        <div className={styles.actions}>
          <button type="submit" className="btn btnPrimary" disabled={pending}>
            {pending
              ? "Сохранение…"
              : mode === "create"
                ? "Опубликовать"
                : "Сохранить изменения"}
          </button>
          {onCancel ? (
            <button type="button" className="btn btnGhost" onClick={onCancel} disabled={pending}>
              Отмена
            </button>
          ) : null}
        </div>
      </form>
    </>
  );
}

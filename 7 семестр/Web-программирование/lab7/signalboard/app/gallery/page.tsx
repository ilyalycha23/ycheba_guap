import Link from "next/link";
import SignalsGallery from "./_components/SignalsGallery";
import styles from "./gallery.module.css";

export default function GalleryPage() {
  return (
    <main>
      <div className={styles.head}>
        <div>
          <h1>Сигналы</h1>
          <p>
            Объявления двора: публикация, метки на карте, отслеживание и архив ваших
            сигналов.
          </p>
        </div>
        <Link href="/gallery/archive" className="btn btnGhost">
          Архив сигналов
        </Link>
      </div>
      <SignalsGallery />
    </main>
  );
}

// Подключает интерактивную галерею к серверной странице маршрута.

import SignalsGallery from "./_components/SignalsGallery";

// Объявляем основной компонент этого файла.
export default function GalleryPage() {
  // Возвращаем JSX-разметку, которую React выведет на странице.
  return (
    <main>
      <h1>Галерея сигналов</h1>
      <p>
        Выберите карточку или метку на карте, чтобы открыть подробное окно.
      </p>
      <SignalsGallery />
    </main>
  );
}

/**
 * Задание 1: три изображения, смена каждую 1 с;
 * ссылка ведёт на файл текущего кадра.
 */
const slides = [
  { file: 'image/spb.jpg', title: 'Санкт-Петербург' },
  { file: 'image/msk.jpg', title: 'Москва' },
  { file: 'image/krd.jpg', title: 'Краснодар' },
];

let slideIndex = 0;

function updateSlide() {
  const s = slides[slideIndex];
  const link = document.getElementById('slide-link');
  const img = document.getElementById('slide-img');
  const cap = document.getElementById('slide-caption');
  link.href = s.file;
  img.src = s.file;
  img.alt = s.title;
  cap.textContent = s.title + ' — перейти к файлу изображения можно по клику на фото';
}

document.addEventListener('DOMContentLoaded', function () {
  updateSlide();
  setInterval(function () {
    slideIndex = (slideIndex + 1) % slides.length;
    updateSlide();
  }, 1000);
});

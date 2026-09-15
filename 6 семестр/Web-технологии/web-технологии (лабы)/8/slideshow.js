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
  updateSlide(); // Отрисовать первый кадр
  setInterval(function () {
    // Циклическое увеличение индекса
    slideIndex = (slideIndex + 1) % slides.length;
    updateSlide(); // след слайд
  }, 1000); // интервал 1 секунда
});

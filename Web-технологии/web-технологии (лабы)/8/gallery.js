/**
 * Задание 3: не менее 7 изображений, одновременно видны три; кнопки влево/вправо.
 */
const galleryImages = [
  { src: 'image/3cc96a9d82a0c10bfc5acad04b874a6e.jpg', title: 'Фото 1' },
  { src: 'image/81-sankt_peterburg.jpg', title: 'Санкт-Петербург' },
  { src: 'image/ieijxw12dj25cjjt6lw0wuob1sg8j3fj.jpg', title: 'Фото 3' },
  { src: 'image/images.jpg', title: 'Коллаж' },
  { src: 'image/krd.jpg', title: 'Краснодар' },
  { src: 'image/msk.jpg', title: 'Москва' },
  { src: 'image/piter-1-2190x1230.jpg', title: 'Петербург' },
  { src: 'image/spb.jpg', title: 'СПб' },
];

let offset = 0;

function updateGallery() {
  const maxOffset = galleryImages.length - 3;
  const imgs = Array.from(document.querySelectorAll('.gallery-strip img'));
  const caps = Array.from(document.querySelectorAll('.gallery-strip figcaption'));
  for (let i = 0; i < 3; i += 1) {
    const item = galleryImages[offset + i];
    imgs[i].src = item.src;
    imgs[i].alt = item.title;
    caps[i].textContent = item.title;
  }
  document.getElementById('gallery-counter').textContent =
    'Позиция: ' + (offset + 1) + '–' + (offset + 3) + ' из ' + galleryImages.length;
}

document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('btn-prev').addEventListener('click', function () {
    const maxOffset = galleryImages.length - 3;
    offset = (offset - 1 + (maxOffset + 1)) % (maxOffset + 1);
    updateGallery();
  });
  document.getElementById('btn-next').addEventListener('click', function () {
    const maxOffset = galleryImages.length - 3;
    offset = (offset + 1) % (maxOffset + 1);
    updateGallery();
  });
  updateGallery();
});

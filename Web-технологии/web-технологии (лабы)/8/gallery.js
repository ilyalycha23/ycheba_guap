const galleryImages = [
  { src: 'image/3cc96a9d82a0c10bfc5acad04b874a6e.jpg', title: 'Театральный зал' },
  { src: 'image/81-sankt_peterburg.jpg', title: 'Исаакиевский собор' },
  { src: 'image/ieijxw12dj25cjjt6lw0wuob1sg8j3fj.jpg', title: 'Большой Петергофский дворец' },
  { src: 'image/images.jpg', title: 'Алые паруса' },
  { src: 'image/krd.jpg', title: 'Краснодар' },
  { src: 'image/msk.jpg', title: 'Москва' },
  { src: 'image/piter-1-2190x1230.jpg', title: 'Панорама Санкт-Петербурга' },
  { src: 'image/spb.jpg', title: 'Казанский собор' },
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

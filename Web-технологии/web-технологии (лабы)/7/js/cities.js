const cityPhotos = {
  krd: { src: 'image/krd.jpg', label: 'Краснодар' },
  sbp: { src: 'image/spb.jpg', label: 'Санкт-Петербург' },
  msk: { src: 'image/msk.jpg', label: 'Москва' },
};

const img = document.getElementById('city-photo');

document.getElementById('btn-krd').onclick = function () {
  img.src = cityPhotos.krd.src;
  img.alt = cityPhotos.krd.label;
};

document.getElementById('btn-sbp').onclick = function () {
  img.src = cityPhotos.sbp.src;
  img.alt = cityPhotos.sbp.label;
};

document.getElementById('btn-msk').onclick = function () {
  img.src = cityPhotos.msk.src;
  img.alt = cityPhotos.msk.label;
};

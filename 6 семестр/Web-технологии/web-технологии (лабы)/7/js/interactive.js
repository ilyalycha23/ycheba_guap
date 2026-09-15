function showSimpleResult() {
  alert('Function Declaration');
}

const showSimpleResultExpr = function () {
  alert('Function Expression');
};

const showSimpleResultArrow = () => {
  alert('Стрелочная функция (arrow function)');
};

const favoritePlaces = [
  'Исаакиевский собор',
  'Гранд Макет Россия',
  'Петропавловская крепость',
];

function showPetersburgPlaces() {
  favoritePlaces.forEach(function (place) {
    alert(place);
  });
}

document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('btn-declaration').addEventListener('click', showSimpleResult);
  document.getElementById('btn-expression').addEventListener('click', showSimpleResultExpr);
  document.getElementById('btn-arrow').addEventListener('click', showSimpleResultArrow);
  document.getElementById('btn-petersburg').addEventListener('click', showPetersburgPlaces);
});

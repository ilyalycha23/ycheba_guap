/**
 * Задание 2: три пункта меню с выпадающими списками.
 * Закрытие по клику вне меню — через target и Element.closest().
 */
document.addEventListener('DOMContentLoaded', function () {
  setupPulldown('list-html', 'pulldown-html');
  setupPulldown('list-css', 'pulldown-css');
  setupPulldown('list-js', 'pulldown-js');
});

function setupPulldown(linkId, menuId) {
  const link = document.querySelector('#' + linkId);
  const menu = document.querySelector('#' + menuId);

  link.addEventListener('click', function (e) {
    e.preventDefault();
    document.querySelectorAll('.pulldown_menu').forEach(function (m) {
      if (m !== menu) {
        m.classList.remove('show');
      }
    });
    menu.classList.toggle('show');
  });

  window.addEventListener('click', function (e) {
    const target = e.target;
    if (!target.closest('#' + menuId) && !target.closest('#' + linkId)) {
      menu.classList.remove('show');
    }
  });
}

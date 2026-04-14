/**
 * Задание 2: один HTML-файл.
 * Контент подменяется по клику на пункты выпадающих списков.
 */
const topics = {
  'html-semantics': {
    title: 'HTML: семантическая разметка',
    text: 'Семантические теги (header, main, section, article, footer) помогают браузеру и поисковым системам понимать структуру документа.',
  },
  'html-structure': {
    title: 'HTML: структура документа',
    text: 'Базовый каркас страницы включает <!DOCTYPE html>, элементы head и body. В head размещаются метаданные, стили и подключение скриптов.',
  },
  'html-links': {
    title: 'HTML: гиперссылки',
    text: 'Тег a связывает страницы между собой. Полезно задавать информативный текст ссылки, а для внешних ресурсов использовать target и rel при необходимости.',
  },
  'css-selectors': {
    title: 'CSS: селекторы',
    text: 'Селекторы определяют, к каким элементам применяются стили: по тегу, классу, id, состоянию (:hover, :focus) и структуре документа.',
  },
  'css-layout': {
    title: 'CSS: вёрстка',
    text: 'Современная вёрстка обычно строится на Flexbox и CSS Grid. Они позволяют удобно создавать адаптивные и читаемые интерфейсы.',
  },
  'css-adaptive': {
    title: 'CSS: адаптивный дизайн',
    text: 'С помощью медиазапросов интерфейс подстраивается под разные ширины экрана: перестраиваются колонки, размеры шрифтов и отступы.',
  },
  'js-syntax': {
    title: 'JavaScript: синтаксис',
    text: 'Язык поддерживает переменные let/const, функции, условия, циклы и объекты. Скрипты делают страницу интерактивной и динамичной.',
  },
  'js-dom': {
    title: 'JavaScript: DOM',
    text: 'DOM API позволяет находить элементы, менять текст, классы и атрибуты. Именно так подменяется содержимое текущего блока на странице.',
  },
  'js-events': {
    title: 'JavaScript: события',
    text: 'События (click, input, submit и др.) связывают действия пользователя с кодом. Обработчики можно задавать через addEventListener.',
  },
};

document.addEventListener('DOMContentLoaded', function () {
  const titleEl = document.getElementById('topic-title');
  const textEl = document.getElementById('topic-text');

  document.querySelectorAll('.pulldown-item').forEach(function (item) {
    item.addEventListener('click', function (e) {
      e.preventDefault();
      const key = item.dataset.topic;
      const topic = topics[key];
      if (!topic) {
        return;
      }
      titleEl.textContent = topic.title;
      textEl.textContent = topic.text;
    });
  });
});

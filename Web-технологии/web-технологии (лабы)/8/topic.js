const TOPIC_MAP = {
  "html-semantics": {
    title: "HTML: семантическая разметка",
    description: "Использование тегов header, main, section, article и footer делает структуру страницы понятной для браузера и поисковых систем.",
  },
  "html-structure": {
    title: "HTML: структура документа",
    description: "Базовый шаблон включает <!DOCTYPE html>, элементы head и body, а также подключение стилей и скриптов в корректных местах.",
  },
  "html-links": {
    title: "HTML: гиперссылки",
    description: "Ссылки создаются тегом a. Для удобства пользователя текст ссылки должен быть понятным и отражать конечную цель перехода.",
  },
  "css-selectors": {
    title: "CSS: селекторы",
    description: "Селекторы позволяют выбирать элементы по тегу, классу, id, атрибутам и состояниям, включая псевдоклассы hover и focus.",
  },
  "css-layout": {
    title: "CSS: вёрстка",
    description: "Современная вёрстка строится с помощью Flexbox и Grid, что помогает создавать адаптивные и аккуратные интерфейсы.",
  },
  "css-adaptive": {
    title: "CSS: адаптивный дизайн",
    description: "Медиазапросы позволяют менять структуру и размеры элементов для корректного отображения на телефонах, планшетах и ПК.",
  },
  "js-syntax": {
    title: "JavaScript: синтаксис",
    description: "JavaScript поддерживает переменные let и const, функции, условия, циклы и объекты для управления логикой веб-страницы.",
  },
  "js-dom": {
    title: "JavaScript: DOM",
    description: "DOM API используется для поиска элементов, изменения текста и атрибутов, а также динамического обновления содержимого страницы.",
  },
  "js-events": {
    title: "JavaScript: события",
    description: "События click, input и submit связывают действия пользователя с кодом. Обычно обработчики задаются через addEventListener.",
  },
};

document.addEventListener("DOMContentLoaded", function () {
  const params = new URLSearchParams(window.location.search);
  const topicKey = params.get("topic");
  const topic = TOPIC_MAP[topicKey];

  const titleEl = document.getElementById("topic-title");
  const descEl = document.getElementById("topic-description");

  if (!topic) {
    titleEl.textContent = "Тема не найдена";
    descEl.textContent = "Параметр topic отсутствует или имеет некорректное значение.";
    return;
  }

  titleEl.textContent = topic.title;
  descEl.textContent = topic.description;
});

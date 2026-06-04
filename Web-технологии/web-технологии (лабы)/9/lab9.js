(function () {
  'use strict';

  function runIntroAnimation() {
    var $box = $('#anim-box'); // jQuery: находим элемент
    $box.css({
      marginLeft: -280,
      opacity: 0, // прозрачность
    });
    $box.animate(
      {
        marginLeft: 0,
        opacity: 1,
      },
      {
        duration: 1400, // Длительность 
        easing: 'swing', // Тип плавности
        complete: function () {
          // первая фаза закончилась, начинается изменение горизонтальных padding
          $box.animate(
            { paddingLeft: 28, paddingRight: 28 }, // расширяем внутренние отступы
            {
              duration: 500,
              easing: 'linear', // Равномерная скорость
              complete: function () {
                // возвращение к исходным значениям
                $(this).animate(
                  { paddingLeft: 16, paddingRight: 16 },
                  { duration: 400, easing: 'swing' }
                );
              },
            }
          );
        },
      }
    );
  }

  $(function () {
    runIntroAnimation(); // Запуск при открытии страницы
    $('#replay-anim').on('click', function () {
      runIntroAnimation(); // Повтор по кнопке replay-anim
    });

    // горизонтальный bar chart
    var ctx = document.getElementById('libraries-chart'); // Canvas-элемент Chart.js (обычный DOM API)
    if (!ctx || typeof Chart === 'undefined') {
      return;
    }

    var labels = [
      'Российская государственная библиотека (Москва)',
      'Российская национальная библиотека (СПб)',
      'Научная библиотека им. М. Горького (СПбГУ)',
      'Государственная публичная историческая библиотека России',
      'Национальная библиотека Республики Татарстан',
      'Российская государственная библиотека искусств',
    ];
    var dataMln = [48.2, 36.5, 6.8, 4.1, 3.5, 2.9];

    new Chart(ctx, {
      type: 'bar', // столб диаграмма
      data: {
        labels: labels, // категории
        datasets: [
          {
            label: 'Фонд, млн ед. хранения', 
            data: dataMln, // Значения столбцов
            backgroundColor: [
              'rgba(14, 116, 144, 0.75)',
              'rgba(13, 148, 136, 0.75)',
              'rgba(59, 130, 246, 0.7)',
              'rgba(99, 102, 241, 0.7)',
              'rgba(168, 85, 247, 0.65)',
              'rgba(236, 72, 153, 0.65)',
            ],
            borderColor: 'rgba(15, 23, 42, 0.25)', // Цвет обводки
            borderWidth: 1,
          },
        ],
      },
      options: {
        indexAxis: 'y', // Горизонтальные столбцы
        responsive: true, // подстраивается под размер контейнера
        maintainAspectRatio: false, // Запрет смены соотношений сторон под контейнер
        plugins: {
          legend: {
            display: true, // Показываем легенду
            position: 'bottom', // Легенда снизу
          },
          title: {
            display: true,
            text: 'Крупнейшие библиотеки России (по фонду, вариант 9)',
          },
        },
        scales: {
          x: {
            beginAtZero: true, // Ось значений начинается с нуля
            title: {
              display: true,
              text: 'Млн единиц хранения', // Подпись оси X
            },
          },
        },
        animation: {
          duration: 2200, // Длительность
          easing: 'easeOutQuart', // замедление к концу
        },
      },
    });
  });
})(); 
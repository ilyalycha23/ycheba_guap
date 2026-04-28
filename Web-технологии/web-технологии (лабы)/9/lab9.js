(function () {
  'use strict';

  function runIntroAnimation() {
    var $box = $('#anim-box');
    //смещение влево и прозрачность
    $box.css({
      marginLeft: -280,
      opacity: 0,
    });
    $box.animate(
      {
        marginLeft: 0,
        opacity: 1,
      },
      {
        duration: 1400,
        easing: 'swing',
        complete: function () {
          //параметр функция плавности
          $box.animate(
            { paddingLeft: 28, paddingRight: 28 },
            {
              duration: 500,
              easing: 'linear',
              complete: function () {
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
    runIntroAnimation();
    $('#replay-anim').on('click', function () {
      runIntroAnimation();
    });

    // горизонтальный bar chart
    var ctx = document.getElementById('libraries-chart');
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
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Фонд, млн ед. хранения',
            data: dataMln,
            backgroundColor: [
              'rgba(14, 116, 144, 0.75)',
              'rgba(13, 148, 136, 0.75)',
              'rgba(59, 130, 246, 0.7)',
              'rgba(99, 102, 241, 0.7)',
              'rgba(168, 85, 247, 0.65)',
              'rgba(236, 72, 153, 0.65)',
            ],
            borderColor: 'rgba(15, 23, 42, 0.25)',
            borderWidth: 1,
          },
        ],
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'bottom',
          },
          title: {
            display: true,
            text: 'Крупнейшие библиотеки России (по фонду, вариант 9)',
          },
        },
        scales: {
          x: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Млн единиц хранения',
            },
          },
        },
        // параметры анимации построения диаграммы
        animation: {
          duration: 2200,
          easing: 'easeOutQuart',
        },
      },
    });
  });
})();

/* Лаб. 9: Chart.js по данным /chart_data и /stats */

async function loadStats() {
  var r = await fetch("/stats");
  var j = await r.json();
  document.getElementById("stats").textContent =
    "среднее: " + (j.avg_temperature != null ? j.avg_temperature.toFixed(2) : "—") +
    ", макс: " + (j.max_temperature != null ? j.max_temperature.toFixed(2) : "—");
}

async function loadChart() {
  var r = await fetch("/chart_data");
  var data = await r.json();
  var ctx = document.getElementById("tempChart");
  if (!ctx) return;
  if (!data.labels || data.labels.length === 0) {
    ctx.parentNode.innerHTML = "<p>Нет точек в журнале. Откройте эмулятор и несколько раз отправьте температуру через /connect.</p>";
    return;
  }

  new Chart(ctx, {
    type: "line",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: "Температура, °C",
          data: data.values,
          borderColor: "rgb(54, 162, 235)",
          backgroundColor: "rgba(54, 162, 235, 0.15)",
          tension: 0.35,
          fill: true,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: true },
        title: { display: true, text: "Журнал температуры (MongoDB или память)" },
      },
      scales: {
        y: { beginAtZero: false },
      },
    },
  });
}

document.addEventListener("DOMContentLoaded", function () {
  loadStats();
  loadChart();
});

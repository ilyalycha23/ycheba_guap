/* Лаб. 3: setInterval + ajax GET (методичка, рис. 16); лаб. 4 — отправка команд. */

function poll(url, id, pick) {
  $.ajax({
    type: "GET",
    url: url,
    dataType: "json",
    contentType: "application/json",
    data: {},
    success: function (response) {
      document.getElementById(id).value = pick(response);
    },
  });
}

function startMonitoring() {
  setInterval(function () {
    poll("/monitor/env", "mon_env", function (r) {
      return r.temperature != null ? r.temperature : r.value;
    });
  }, 1000);

  setInterval(function () {
    poll("/monitor/score", "mon_score", function (r) {
      return r.is_goal ? "гол" : "нет";
    });
  }, 1000);

  setInterval(function () {
    poll("/monitor/zone", "mon_zone", function (r) {
      return r.zone;
    });
  }, 1000);

  setInterval(function () {
    poll("/monitor/board", "mon_board", function (r) {
      return r.scoreA + ":" + r.scoreB + " t=" + r.timer;
    });
  }, 1000);
}

function sendCommand(url, valueFieldId, extra) {
  var v = document.getElementById(valueFieldId).value;
  $.ajax({
    type: "GET",
    url: url,
    dataType: "json",
    data: { value: v },
    success: function (response) {
      if (extra) extra(response);
    },
  });
}

$(function () {
  startMonitoring();

  $("#btn_env").on("click", function () {
    sendCommand("/connect", "cmd_env", function (r) {
      $("#cmd_env_reply").text("heat=" + r.heater_power);
      $("#chain_out").text(JSON.stringify(r, null, 2));
    });
  });

  $("#btn_score").on("click", function () {
    sendCommand("/command/score", "cmd_score");
  });
  $("#btn_zone").on("click", function () {
    sendCommand("/command/zone", "cmd_zone");
  });
  $("#btn_board").on("click", function () {
    sendCommand("/command/board", "cmd_board");
  });
});

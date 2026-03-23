function send_data() {
    $.ajax({
        type: 'GET',
        url: '/connect',
        dataType: 'json',
        contentType: 'application/json',
        data: { "value": document.getElementById("value").value },
        success: function (response) {
            document.getElementById("command").value = response["power"];
            $.get('/connect_scoreboard', function(r) {
                var data = typeof r === 'string' ? JSON.parse(r) : r;
                document.getElementById("scoreboard").value = data["scoreboard_power"];
            });
        }
    });
}

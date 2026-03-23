function send_data() {
    $.ajax({
        type: 'GET',
        url: '/connect',
        dataType: 'json',
        contentType: 'application/json',
        data: {
            "value": document.getElementById("value").value,
        },
        success: function (response) {
            document.getElementById("command").value = response["power"];
        }
    });
}

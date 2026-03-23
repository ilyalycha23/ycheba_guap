setInterval(get_data, 1000);

function get_data() {
    $.ajax({
        type: 'GET',
        url: '/connect',
        dataType: 'json',
        contentType: 'application/json',
        data: {},
        success: function (response) {
            document.getElementById("value").value = response["value"];
        }
    });
}

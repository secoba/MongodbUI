function sendPost(url, json_data) {
    let rst;
    $.ajax({
        type: "POST",
        url: url,
        dataType: "json",
        data: json_data,
        async: false,
        success: function (data) {
            rst = data
        },
        error: function () {
            rst = {"msg": "请求有误"}
        }
    });
    return rst;
}

function sendGet(url) {
    let rst;
    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        async: false,
        success: function (data) {
            rst = data
        },
        error: function () {
            rst = {"msg": "请求有误"}
        }
    });
    return rst;
}


$(".save-config").click(function () {
    let rst = sendPost("/config/save_config", {
        "host": $("#host").val(),
        "port": $("#port").val(),
        "database": $("#database").val(),
        "username": $("#username").val(),
        "password": $("#password").val(),
    });
    alert(rst["msg"])
});

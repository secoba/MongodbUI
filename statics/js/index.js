const utf8ToB64 = (str) => {
    return btoa(unescape(encodeURIComponent(str)))
};

/**
  * base64Str to string
  * @param {string} b64Str base64Str
  *
  * @returns {string} string
  */
const b64ToUtf8 = (b64Str) => {
    return decodeURIComponent(escape(atob(b64Str)))
};


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

function limitText(oldText, len) {
    if (oldText.length > len) {
        return oldText.substring(0, len - 2) + "...";
    }
    return oldText;
}


function delItem(item_id) {
    var status = confirm("delete confirm？");
    if (!status) {
        return false;
    }
    sendGet("/data/data_del?id=" + item_id);
    window.location.reload();
}


function viewItem(item_id) {
    console.log(sendGet("/data/data_info?id=" + item_id));
}


$(".save-config").click(function () {
    let rst = sendPost("/config/save_config", {
        "host": $("#host").val(),
        "port": $("#port").val(),
        "database": $("#database").val(),
        "username": $("#username").val(),
        "password": $("#password").val(),
    });
    alert(rst["msg"]);
    window.location.href = "/"
});


function getPageData(page, queryString) {
    let collection = $("#collect-select option:selected").attr("value");
    if (queryString !== undefined && queryString.length > 0) {
        queryString = utf8ToB64(queryString)
    }
    let rst = sendGet("/data/data_list?collection=" + collection + "&page=" + page + "&query=" + queryString);
    console.log(rst);
    if (rst["status"] === 1) {
        console.log(rst["msg"]);
        $("#item-list").html("");
    } else {
        let table_data = "";
        let total = rst["data"]["current_page"] * rst["data"]["current_size"];
        $("#current_collection").html(rst["data"]["current_collection"]);
        rst["data"]["list"].map(function (value, index, array) {
            table_data += "<tr>" +
                // "<td>" + value["_id"] + "</td>" +
                "<td class='td-detail'>" +
                "<details class='item-detail'>" +
                // "<summary class='item-summary'>" + limitText(JSON.stringify(value), 80) + "</summary>" +
                "<summary class='item-summary'>" + value["_id"] + "</summary>" +
                "<div>" + JSON.stringify(value) + "</div>" +
                "</details>" +
                "</td>" +
                "<td>" +
                "<div class='operation'>" +
                "<button class=\"view\" onclick=viewItem('" + value["_id"] + "')>查 看</button>" +
                "</div>" +
                "<div class='operation'>" +
                "<button class=\"delete\"  onclick=delItem('" + value["_id"] + "')>删 除</button>" +
                "</div>" +
                "</td>" +
                "</tr>"
        });
        $("#item-list").html(table_data);
        if (total < rst["data"]["count"]) {
            $("#next_page").attr("disable", "");
            $("#next_page").attr("value", rst["data"]["current_page"] + 1);
        } else {
            $("#next_page").attr("value", "");
            $("#next_page").attr("disable", "disable");
        }
        if (rst["data"]["current_page"] > 1) {
            $("#prev_page").attr("disable", "");
            $("#prev_page").attr("value", rst["data"]["current_page"] - 1);
        } else {
            $("#prev_page").attr("value", "");
            $("#prev_page").attr("disable", "disable");
        }
    }
}

$("#prev_page").click(function () {
    let page = $("#prev_page").val();
    if (page.length > 0) {
        getPageData(page, $(".search-input").val())
    }
});

$("#next_page").click(function () {
    let page = $("#next_page").val();
    if (page.length > 0) {
        getPageData(page, $(".search-input").val())
    }
});


$("#collect-select").change(function (data) {
    getPageData(1, $(".search-input").val())
});

// search
$(".search-input").keypress(function (e) {
    if (e.which === 13) {
        getPageData(1, $(".search-input").val())
    }
});


getPageData(1, "true");
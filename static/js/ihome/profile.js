function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    // 为表单的提交事件添加事件函数
    $("#form-avatar").submit(function (e) {
        e.preventDefault();
        // ajax请求的配置信息
        var ajax_options = {
            url: "/api/user/avatar",
            type: "post",
            dataType: "json",
            headers: {
                "X-XSRFToken": getCookie("_xsrf")
            },
            success: function (data) {
                if ("0" == data.errcode ) {
                    $("#user-avatar").attr("src", data.avatar_url);
                } else if ("4101" == data.errcode) {
                    document.location.href = "/login.html";
                } else {
                    alert(data.errmsg);
                }
            }
        };
        $(this).ajaxSubmit(ajax_options);
    });
    $("#form-name").submit(function(e){
        e.preventDefault();
        var data = {};
        $(this).serializeArray().map(function(x){data[x.name] = x.value;});
        var jsonData = JSON.stringify(data);
        $.ajax({
            url:"/api/user/name",
            type:"POST",
            data: jsonData,
            contentType: "application/json",
            dataType: "json",
            headers:{
                "X-XSRFTOKEN":getCookie("_xsrf")
            },
            success: function (data) {
                if ("0" == data.errcode) {
                    $(".error-msg").hide();
                    showSuccessMsg(); // 展示保存成功的页面效果
                } else if ("4001" == data.errcode) {
                    $(".error-msg").show();
                } else if ("4101" == data.errcode) { // 4101代表用户未登录，强制跳转到登录页面
                    location.href = "/login.html";
                }
            }
        });
    })
})
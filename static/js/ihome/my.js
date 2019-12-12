function logout() {
    $.get("/api/logout", function(data){
        if ("0" == data.errcode) {
            location.href = "/";
        }
    })
}

$(document).ready(function(){

    // 页面加载后想后端请求个人信息
    $.get("/api/user/info", function(data) {
        // 4101错误代表用户未登录
        if ("4101" == data.errcode) {
            location.href = "/login.html";
        }
        else if ("0" == data.errcode) {
            $("#user-name").html(data.data.name);
            $("#user-mobile").html(data.data.mobile);
            if (data.data.avatar) {
                $("#user-avatar").attr("src", data.data.avatar);
            }
        }
    }, "json");
})

//JS
layui.use(function () {
    let layer = layui.layer;
    let util = layui.util;
    let $ = layui.$;

    //头部事件
    util.event('lay-header-event', {
        menuLeft: function () { // 左侧菜单事件
            layer.msg('展开左侧菜单的操作', {icon: 1});
        },
        menuRight: function () {  // 右侧菜单事件
            layer.open({
                type: 1,
                title: '更多',
                content: '<div style="padding: 15px;">处理右侧面板的操作</div>',
                area: ['260px', '100%'],
                offset: 'rt', // 右上角
                anim: 'slideLeft', // 从右侧抽屉滑出
                shadeClose: true,
                scrollbar: false
            });
        }
    });

    $("#logout").bind("click", () => {
        $.ajax({
            type: "post",
            url: "/api/logout",
            success(result, status, xhr) {
                console.log(result, status, xhr)
                if (result.status === "ok" && status === "success") {
                    layer.msg("已退出登录", {
                        icon: 1,
                        shade: [0.8, '#393D49']
                    });
                    setTimeout(() => {
                        $(location).attr("href", window.location.href.split("login")[0] + "login")
                    }, 1000)
                }
            },
            error(xhr, status, error) {
                layer.msg(xhr.status + " " + error, {
                    icon: 2,
                    title: "错误 " + error,
                    shade: [0.8, '#393D49']
                });
            },

        })
    })
});
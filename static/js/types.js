layui.use(function () {
    let $ = layui.$;
    let form = layui.form;
    let layer = layui.layer;
    let layPage = layui.laypage;

    // 页面加载完成
    $(document).ready(function () {
        refresh = $(".layui-laypage-refresh");

        // 请求后端一共多少种图片类型
        $.ajax({
            type: "post",
            url: "/api/image/types",
            success(result) {
                let selectType = $("#select-type");

                for (let item of result) {
                    if (item[0] === "") {
                        selectType.append(`<option value="default">默认类型</option>`);
                        continue;
                    }
                    let option = $(`<option value="${item[0]}">${item[0]}</option>`);
                    selectType.append(option);
                }
                form.render("select");
            },
            error() {
                layer.msg("获取图片类型失败");
            },
        })
    })

    let codeInst = layui.code({
        elem: '.code-link'
    });

    // select 事件
    form.on('select(select-filter)', function (data) {
        let value = data.value; // 获得被选中的值
        let urlLink = $('#url-link');   // 显示链接元素

        // 如果没有选中清空选中元素内容
        if (!value) {
            urlLink.text("");
            codeInst.reload({
                elem: '.code-link'
            });
            $(waterfall).empty();
            return false;
        }

        // 渲染链接标签元素
        urlLink.text(`//${window.location.host}/api/type/link/${value}`);
        codeInst.reload({
            elem: '.code-link'
        });

        // 请求当前类型一共有多少图片
        $.ajax({
            type: "post",
            url: "/api/type/image/length",
            data: {
                type: value
            },
            success(result) {
                // 渲染当前类型分页，完整显示
                layPage.render({
                    elem: 'page', // 元素 id
                    count: result[0][0], // 数据总数
                    limit: 50,
                    limits: [30, 50, 70, 100],
                    groups: 5,
                    layout: ['count', 'prev', 'page', 'next', 'limit', 'refresh', 'skip'], // 功能布局
                    jump: function (obj) {
                        let limit = obj.limit;
                        let limits = obj.limits;
                        let curr = obj.curr;
                        // 根据类型请求图片信息
                        $.ajax({
                            type: "post",
                            url: "/api/type/image/range",
                            data: {
                                limits,
                                limit: limit,
                                offset: (curr - 1) * limit,
                                type: value
                            },
                            success(result) {
                                // 清空容器之前的图片
                                $(waterfall).empty().css("height", "0");
                                // 根据请求信息构建新的图片元素
                                createImagesItem(result, $)
                            },
                            error() {
                                layer.msg("获取图片信息失败");
                            },
                        })
                    }
                });
            },
            error() {
            },
        })
    });
});

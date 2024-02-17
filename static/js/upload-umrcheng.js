//JS
layui.use(function () {
    let upload = layui.upload;
    let layer = layui.layer;
    let element = layui.element;
    let $ = layui.$;

    // 渲染
    upload.render({
        elem: '#upload-drag',
        field: "image",
        elemList: $('#ID-upload-demo-files-list'), // 列表元素对象
        url: '/api/upload', // 实际使用时改成您自己的上传接口即可。
        accept: 'images',
        multiple: true,
        number: 1000,
        auto: false,
        bindAction: '#ID-upload-demo-files-action',
        data: {
            "user": function () {
                return $('[name="user"]').val();
            },
            "type": function () {
                return $('[name="type"]').val();
            }
        },
        choose: function (obj) {
            let that = this;
            let files = this.files = obj.pushFile(); // 将每次选择的文件追加到文件队列
            // 读取本地文件
            obj.preview(function (index, file, result) {
                let tr = $(['<tr id="upload-' + index + '">', '<td>' + file.name + '</td>', '<td>' + (file.size / 1024).toFixed(1) + 'kb</td>', '<td><div class="layui-progress" lay-filter="progress-demo-' + index + '"><div class="layui-progress-bar" lay-percent=""></div></div></td>', '<td>', '<button class="layui-btn layui-btn-xs demo-reload layui-hide">重传</button>', '<button class="layui-btn layui-btn-xs layui-btn-danger demo-delete">删除</button>', '</td>', '</tr>'].join(''));

                // 单个重传
                tr.find('.demo-reload').on('click', function () {
                    obj.upload(index, file);
                });

                // 删除
                tr.find('.demo-delete').on('click', function () {
                    delete files[index]; // 删除对应的文件
                    tr.remove(); // 删除表格行
                    // 清空 input file 值，以免删除后出现同名文件不可选
                    uploadListIns.config.elem.next()[0].value = '';
                });

                that.elemList.append(tr);
                element.render('progress'); // 渲染新加的进度条组件
            });
        },
        done: function (res, index, upload) {
            // layer.msg('单个文件上传成功');
            // $('#ID-upload-demo-preview').removeClass('layui-hide')
            //     .find('img').attr('src', res.files.file);
            // console.log(res)

            let that = this;
            let tr = that.elemList.find('tr#upload-' + index)
            let tds = tr.children();
            tds.eq(3).html(''); // 清空操作
            delete this.files[index]; // 删除文件队列已经上传成功的文件
        },
        allDone: function (obj) { // 多文件上传完毕后的状态回调
            console.log(obj)
            layer.open({
                title: '状态', content: '上传成功'
            });
        },
        error: function (index, upload) { // 错误回调
            let that = this;
            let tr = that.elemList.find('tr#upload-' + index);
            let tds = tr.children();
            // 显示重传
            tds.eq(3).find('.demo-reload').removeClass('layui-hide');
        },
        progress: function (n, elem, e, index) { // 注意：index 参数为 layui 2.6.6 新增
            element.progress('progress-demo-' + index, n + '%'); // 执行进度条。n 即为返回的进度百分比
        }
    });
});

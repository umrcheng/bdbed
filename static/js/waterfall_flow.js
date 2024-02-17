class WaterFall {
    constructor(container, options) {
        this.gap = options.gap || 0;
        this.container = container;
        this.items = container.children || [];
        this.heightArr = [];
        this.renderIndex = 0;
        window.addEventListener('resize', () => {
            this.renderIndex = 0;
            this.heightArr = [];
            this.layout()
        });
    }

    layout() {
        if (this.items.length === 0) return;
        const gap = this.gap;
        // const pageWidth = this.container.offsetWidth;
        const pageWidth = window.innerWidth;
        const itemWidth = this.items[0].offsetWidth;
        const columns = pageWidth / (itemWidth + gap); // 总共有多少列
        while (this.renderIndex < this.items.length) {
            let top, left;
            if (this.renderIndex <= columns - 1) { // 第一行
                top = 0;
                left = (itemWidth + gap) * this.renderIndex;
                this.heightArr.push(this.items[this.renderIndex].offsetHeight)
            } else {
                const minIndex = this.getMinIndex(this.heightArr);
                top = this.heightArr[minIndex] + gap;
                left = this.items[minIndex].offsetLeft
                this.heightArr[minIndex] += (this.items[this.renderIndex].offsetHeight + gap);
            }
            this.container.style.height = this.getMaxHeight(this.heightArr) + 'px';
            this.items[this.renderIndex].style.top = top + 'px';
            this.items[this.renderIndex].style.left = left + 'px';
            this.renderIndex++;
        }
    }

    getMinIndex(heightArr) {
        let minIndex = 0;
        let min = heightArr[minIndex]
        for (let i = 1; i < heightArr.length; i++) {
            if (heightArr[i] < min) {
                min = heightArr[i]
                minIndex = i;
            }
        }
        return minIndex;
    }

    getMaxHeight(heightArr) {
        let maxHeight = heightArr[0]
        for (let i = 1; i < heightArr.length; i++) {
            if (heightArr[i] > maxHeight) {
                maxHeight = heightArr[i]
            }
        }
        return maxHeight;
    }
}


// 图片预览组件
const waterfall = document.getElementById('waterfall')
const viewer = new Viewer(waterfall, {
    url: 'src',
    show: function () {        // 动态加载图片后，更新实例
        viewer.update();
    },
});

// 监听图片元素容器是否加入新的图片
const config = {childList: true, subtree: true};
let observer = new MutationObserver(() => {
    const water = new WaterFall(waterfall, {gap: 15})
    water.layout()
});
observer.observe(waterfall, config);

let refresh;

/** 创建图片对象
 *
 * @param data 后台图片信息
 * @param $ jquery对象
 */
function createImagesItem(data, $) {
    let scroll = 0;
    $(document).scroll(function () {
        if ($(document).scrollTop() > 0) {
            scroll = $(document).scrollTop();
        }
    })

    const waterfall = document.getElementById('waterfall');
    const fragment = document.createDocumentFragment();
    for (let item of data) {
        const div = $(document.createElement('div'));
        div.addClass('waterfall-item');

        const img = $(document.createElement('img'));
        img.addClass('image-item');
        img.attr("src", '/api' + item[2])
        img.bind("load", function () {
            div.append(img);
        })
        img.bind('click', function () {
            viewer.update();
            this.click();
        });

        const buttonGroup = $('<div class="layui-btn-container copy hidden"></div>')

        const deleteButton = $('<button type="button" class="layui-btn layui-btn-sm layui-bg-red">删除图片</button>');
        deleteButton.bind("click", function () {
            layer.confirm("确认删除？" + item[1], {icon: 3}, function () {
                $.ajax({
                    type: 'post',
                    url: '/api/del/photo',
                    data: {
                        id: item[0],
                        md: item[1]
                    },
                    success() {
                        layer.msg("删除成功");
                        refresh = $(".layui-laypage-refresh");
                        refresh[0].click();
                        setTimeout(() => {
                            $(document).scrollTop(scroll);
                        }, 70)
                    },
                    error() {
                        layer.msg("删除失败");
                    }
                })
            }, function () {
                layer.msg('取消');
            })
        });
        const copyButton = $('<button type="button" class="layui-btn layui-btn-sm layui-bg-blue">复制地址</button>');
        copyButton.bind("click", function () {
            layer.msg("复制成功");
            let address = `//${window.location.host}/api${item[2]}`;

            let temp = $('<input>');
            $('body').append(temp);
            temp.val(address).select();
            document.execCommand('copy');
            temp.remove();
        });

        div.hover(function () {
            buttonGroup.removeClass("hidden")
            buttonGroup.addClass("show");
            buttonGroup.css("display", "")
        }, function () {
            buttonGroup.removeClass("show")
            buttonGroup.addClass("hidden");
            buttonGroup.css("display", "none")
        })


        buttonGroup.append(deleteButton)
        buttonGroup.append(copyButton)
        div.append(buttonGroup)
        fragment.appendChild(div[0]);
    }
    waterfall.appendChild(fragment);
}

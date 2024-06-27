export function waterFallInit(columns, card_columns, arrHeight, cards) {
    columns.value = waterfall_column()  //// 获取列数4
    card_columns.value = {} // 初始化存储每列卡片的对象
    arrHeight.value = []    // 初始化存储每列高度的数组
    for (let i = 0; i < columns.value; i++) {
        card_columns.value[i] = []
    }
    // 遍历所有卡片，将它们分配到列中
    for (let i = 0; i < cards.value.length; i++) {
        var height = cards.value[i].img_info.height / (cards.value[i].img_info.width / cardwidth)
        // 如果是前 `columns.value` 个卡片，直接放入对应的列中
        if (i < columns.value) {
            card_columns.value[i].push(cards.value[i])
            arrHeight.value.push(height) // 记录每列的高度
        } else {
            // 找出当前高度最小的列
            let obj = {
                minH: arrHeight.value[0],
                minI: 0
            }
            for (let j = 0; j < arrHeight.value.length; j++) {
                if (arrHeight.value[j] < obj.minH) {
                    obj.minH = arrHeight.value[j]
                    obj.minI = j
                }
            }
            // 将卡片放入高度最小的列中，并更新该列的高度
            card_columns.value[obj.minI].push(cards.value[i])
            arrHeight.value[obj.minI] += height
        }
    }
}

export function waterFallMore(arrHeight, card_columns, more) {
    for (let i = 0; i < more.length; i++) {
        var height = more[i].img_info.height / (more[i].img_info.width / 250)
        let obj = {
            minH: arrHeight.value[0],
            minI: 0
        }
        for (let j = 0; j < arrHeight.value.length; j++) {
            if (arrHeight.value[j] < obj.minH) {
                obj.minH = arrHeight.value[j]
                obj.minI = j
            }
        }
        card_columns.value[obj.minI].push(more[i])
        arrHeight.value[obj.minI] += height
    }
}
// 重置瀑布流的分布
export function resizeWaterFall(columns, card_columns, arrHeight, cards) {
    var timerId = null;
    // 全局的 window.onresize 处理程序
    window.onresize = function () {
        if (timerId) {
            clearTimeout(timerId);
        }
        timerId = setTimeout(() => {
            waterFallInit(columns, card_columns, arrHeight, cards)
        }, 300)
    }
}

function waterfall_column() {
    // 1.获取主容器的宽度
    var content = document.getElementById('content')
    
    var contentWidth = content.offsetWidth
    console.log("总宽度:",contentWidth);    //总宽度736
    return Math.floor(contentWidth / (colwidth)) //会有4列
    // 这行代码将 content 元素的总宽度除以每列的宽度（假设每列的宽度是 280 像素），
    // 然后使用 Math.floor 函数对结果进行向下取整，计算出可以容纳的列数。
}

const colwidth = 280
const cardwidth = 250

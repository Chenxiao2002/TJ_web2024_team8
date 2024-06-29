<script lang="ts" setup>
import {onMounted, ref} from "vue";
import HomeCard from "@/components/homeCard.vue";
import {Back} from "@element-plus/icons-vue";
import CardDetail from "@/components/cardDetail.vue";
import {queryPost} from "@/apis/main";
import {useRoute} from "vue-router";
import {controlDetail} from "@/stores/controlDetail";
import {onClickOutside} from '@vueuse/core';
import {resizeWaterFall, waterFallInit, waterFallMore} from "@/utils/waterFall";
import { ElLoading } from 'element-plus';
import 'element-plus/theme-chalk/el-loading.css';

const query = useRoute().query.query
//route.query.query访问名为query的查询参数的值。例如，如果当前URL是/somepath?query=value，那么route.query.query的值将是value。
// 获得搜索值
const Details = controlDetail()

// 主页卡片 //////////////////////////////////////////////////////////////////
const cards = ref([]);
const disabled = ref(true); // 初始禁用滚动加载

const columns = ref(0)
const card_columns = ref({})
const arrHeight = ref([])
// 加载动画相关变量
const loading = ref(false);
const loadingContainer = ref(null);
let loadingInstance: any = null;

// 主页获取帖子
const doQuery = async (offset,category) => {
  try {
    loading.value = true;
    loadingInstance = ElLoading.service({
      target: loadingContainer.value,
      lock: true,
      text: '加载中...',
      background: 'rgba(0, 0, 0, 0.7)',
    });
    const res = await queryPost({offset, category,query});
    console.log(res);
    cards.value = res.info;
    console.log('卡片详情',cards.value[0].title);
    waterFallInit(columns, card_columns, arrHeight, cards)
    disabled.value = false; // 启用滚动加载
  } catch (error) {
    console.error('Error fetching messages:', error);
  } finally {
    loading.value = false;
    if (loadingInstance) {
      loadingInstance.close();
    }
  }
};
// 无限滚动
const load = async () => {
  disabled.value = true;
  const offset = cards.value.length;
  const category = activeName.value
  const res = await queryPost({offset,category, query});
  const more = res.info;
  if (more.length === 0) {
    disabled.value = true; // 没有更多数据，禁用滚动加载
  } else {
    cards.value = [...cards.value, ...more];
    waterFallMore(arrHeight, card_columns, more)
    disabled.value = false;
  }
};
// 主页卡片结束////////////////////////////////////////////////////////////////

// 卡片详情 //////////////////////////////////////////////////////////////////
const detail = Details.detail;
const show = ref(false);
const overlayX = ref(0); // 覆盖层的水平位置
const overlayY = ref(0); // 覆盖层的垂直位置
const overlay = ref(null)

const getDetails = async (id) => Details.getDetail(id)
const showMessage = async (id, left, top) => {
  window.history.pushState({}, "", `/explore/${id}`);
  overlayX.value = left;
  overlayY.value = top;
  await getDetails(id);
  show.value = true;
};
const afterDoComment = (comment) => Details.afterDoComment(comment)
const close = () => {
  window.history.pushState({}, "", "/");
  show.value = false;
  document.title = '欢迎来到TJ论坛!'
};
onClickOutside(overlay, () => {
  window.history.pushState({}, "", "/");
  show.value = false;
  document.title = '欢迎来到TJ论坛!'
});

let style = null;
const onBeforeEnter = () => {
  style = document.createElement('style')
  style.innerHTML =
      `@keyframes scale-up-center {
          0% {
            transform: scale(0.5);
            transform-origin: ${overlayX.value}px ${overlayY.value}px;
          }
          10% {
            transform: scale(0.5);
          }
          100% {
            transform: scale(1);
          }
       }`
  document.head.appendChild(style);
}

const onAfterEnter = (el) => {
  el.style = 'background-color: #fff'
  const button = el.querySelector('.backPage')
  button.style.display = ''
}
const onBeforeLeave = (el) => {
  const button = el.querySelector('.backPage')
  button.style.display = 'none'
  el.style = 'background-color: transparent'
}

const onAfterLeave = () => {
  if (style) {
    document.head.removeChild(style);
    style = null;
  }
}

// 卡片详情结束 //////////////////////////////////////////////////////////////////

// onMounted()钩子函数，在组件挂载后执行某些操作
// async()=>{}异步函数
onMounted(async () => {
  await doQuery(0,activeName.value);  //等待doQuery完成
  resizeWaterFall(columns, card_columns, arrHeight, cards)
  // 调整瀑布流布局
});

const activeName = ref('')

const handleClick = async (tab) => {
  activeName.value = tab.props.name;
  await doQuery(0,activeName.value); // 重新加载数据
  console.log(tab.props.name,'',activeName.value) //这个就是el-tab-pane中的name
}
</script>

<template>
  <div>
    <!-- 标签页提供选项卡功能 -->
    <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
      <el-tab-pane label="所有" name="" ></el-tab-pane>
      <el-tab-pane label="日常" name="日常"></el-tab-pane>
      <el-tab-pane label="学习" name="学习"></el-tab-pane>
      <el-tab-pane label="选课" name="选课"></el-tab-pane>
      <el-tab-pane label="拼车" name="拼车"></el-tab-pane>
      <el-tab-pane label="实习" name="实习"></el-tab-pane>
      <el-tab-pane label="交友" name="交友"></el-tab-pane>
    </el-tabs>
    <div class="Empty" v-if="cards.length === 0">
      <el-empty description="没有帖子..."/>
    </div>
    <div v-else>
      <div v-infinite-scroll="load" :infinite-scroll-disabled="disabled" :infinite-scroll-distance="200">
        <home-card :card_columns="card_columns" @show-detail="showMessage" ref="homeCardRef"></home-card>
      </div>
      <!-- 打开卡片帖子的过渡动画 -->
      <transition
          name="fade"
          @before-enter="onBeforeEnter"
          @after-enter="onAfterEnter"
          @before-leave="onBeforeLeave"
          @after-leave="onAfterLeave"
      >
        <div class="overlay" v-if="show">
          <button style="display:none;" class="backPage" @click="close">
            <el-icon>
              <Back/>
            </el-icon>
          </button>
          <card-detail :detail="detail" @afterDoComment="afterDoComment" ref="overlay"/>
        </div>
      </transition>
    </div>
  </div>
</template>


<style lang='scss' scoped>
/* 当前激活的标签 */
:deep(.el-tabs__item.is-active) {
  color:#2f779d;
  font-weight: bold;
}
/* 标签项切换长条颜色 */
:deep(.el-tabs__active-bar) {
  background-color: #2f779d;
}
// 鼠标悬停在标签上
:deep(.el-tabs__item:hover) {
  color: #52cff2;
}
// 标签项
:deep(.el-tabs__item) {
  font-size: 16px;
  /* font-family: 'Helvetica Neue', Arial, sans-serif !important; 设置字体族 */
  /* 字体族暂不起作用 */
}

.demo-tabs{
  box-sizing: border-box;
}

.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
.Empty {
  margin-top: 10%;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 9999;
}

.backPage {
  position: fixed;
  top: 5%;
  left: 3%;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid var(--color-border);
  cursor: pointer;
  transition: all .3s;
  background-color: #2f779d;
  color: #ffffff;
  font-size: 20px; /* 调整图标大小 */
}

.fade-enter-active {
  animation: scale-up-center 0.5s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
}

.fade-leave-active {
  animation: scale-up-center 0.3s ease-out both reverse;
}

</style>

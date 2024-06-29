<template>
  <div ref="loadingContainer" class="collection-container">
    <div v-if="messages.length === 0 && !loading">
      <el-empty description="现在还没有收藏消息..." />
    </div>
    <div v-else>
      <ul class="agree-container">
        <li class="agree-item" v-for="message in messages" :key="message.createTime" @click="goToDetail(message.post_id)">
          <a class="user-avatar">
            <img class="avatar-item" :src="message.avatar" />
          </a>
          <div class="main">
            <div class="info">
              <div class="user-info">
                <a>{{ message.username }}</a>
              </div>
              <div class="interaction-hint">
                <span>收藏了您的帖子&nbsp;</span><span>{{ formatDate(message.createTime) }}</span>
              </div>
              <div class="interaction-content">
                <span>{{ message.content }}</span>
              </div>
            </div>
            <div class="extra">
              <img class="extra-image" :src="message.post_img0" />
            </div>
          </div>
        </li>
      </ul>
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



<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { getCollectInfo } from '@/apis/main';
import { ElLoading } from 'element-plus';
import 'element-plus/theme-chalk/el-loading.css';
import {controlDetail} from "@/stores/controlDetail";
import {onClickOutside} from "@vueuse/core";
import {Back} from "@element-plus/icons-vue";
import {useUserStore} from "@/stores/user";

const Details = controlDetail()
const route = useRoute();
const messages = ref([]);
const loading = ref(false);
const loadingContainer = ref(null);
let loadingInstance: any = null;
const userStore = useUserStore();
const userInfo = userStore.userInfo;


const fetchMessages = async () => {
  const user_id = route.params.id;
  try {
    loading.value = true;
    loadingInstance = ElLoading.service({
      target: loadingContainer.value,
      lock: true,
      text: '加载中...',
      background: 'rgba(0, 0, 0, 0.7)',
    });
    const post = await getCollectInfo({ user_id });
    messages.value = post.info;
  } catch (error) {
    console.error('Error fetching messages:', error);
  } finally {
    loading.value = false;
    if (loadingInstance) {
      loadingInstance.close();
    }
  }
};

// 卡片详情页的内容 //////////////////////////////////////////////////////////
const detail = Details.detail
const overlayX = ref(0); // 覆盖层的水平位置
const overlayY = ref(0); // 覆盖层的垂直位置
const overlay = ref(null)
const show = ref(false)

const getDetails = async (id) => Details.getDetail(id)
const goToDetail = async(id: string) => {
  window.history.pushState({}, "", `/explore/${id}`);
  const target = event.target;
  overlayX.value = target.x;
  overlayY.value = target.y;
  await getDetails(id);
  show.value = true;
};
const afterDoComment = (comment) => Details.afterDoComment(comment)
const close = () => {
  window.history.pushState({}, "", "/user/control/collection");
  document.title = userInfo.username + '-消息通知'
  show.value = false
}
onClickOutside(overlay, () => {
  window.history.pushState({}, "", "/user/control/collection");
  document.title = userInfo.username + '-消息通知'
  show.value = false;
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
// 卡片详情页的内容结束 //////////////////////////////////////////////////////////

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString();
};

onMounted(async () => {
  // await getUserInfo()
  await fetchMessages()

});
</script>

<style lang="less" scoped>
textarea {
  overflow: auto;
}

.collection-container {
  position: relative; /* 确保遮罩层相对定位 */
  width: 100%;
  height: 100%;
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
  justify-content: center;
  align-items: center;
  width: 40px;
  height: 40px;
  border-radius: 40px;
  border: 1px solid var(--color-border);
  cursor: pointer;
  transition: all .3s;
}
.agree-container {
  width: 40rem;

  .agree-item {
    display: flex;
    flex-direction: row;
    padding-top: 24px;

    .user-avatar {
      margin-right: 24px;
      flex-shrink: 0;

      .avatar-item {
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        border-radius: 100%;
        border: 1px solid rgba(0, 0, 0, 0.08);
        object-fit: cover;
      }
    }

    .main {
      flex-grow: 1;
      flex-shrink: 1;
      display: flex;
      flex-direction: row;
      padding-bottom: 12px;
      border-bottom: 1px solid rgba(0, 0, 0, 0.08);

      .info {
        flex-grow: 1;
        flex-shrink: 1;

        .user-info {
          display: flex;
          flex-direction: row;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 4px;

          a {
            color: #333;
            font-size: 16px;
            font-weight: 600;
          }
        }

        .interaction-hint {
          font-size: 14px;
          color: rgba(51, 51, 51, 0.6);
          margin-bottom: 8px;
        }

        .interaction-content {
          display: flex;
          font-size: 14px;
          color: #333;
          line-height: 140%;
          cursor: pointer;
          margin-bottom: 12px;

          .msg-count {
            width: 20px;
            height: 20px;
            line-height: 20px;
            font-size: 13px;
            color: #fff;
            background-color: red;
            text-align: center;
            border-radius: 100%;
          }
        }

        .quote-info {
          font-size: 12px;
          display: flex;
          align-items: center;
          color: rgba(51, 51, 51, 0.6);
          margin-bottom: 12px;
          cursor: pointer;
        }

        .quote-info::before {
          content: "";
          display: inline-block;
          border-radius: 8px;
          margin-right: 6px;
          width: 4px;
          height: 17px;
          background: rgba(0, 0, 0, 0.08);
        }
      }

      .extra {
        min-width: 48px;
        flex-shrink: 0;
        margin-left: 24px;

        .extra-image {
          cursor: pointer;
          width: 48px;
          height: 48px;
          border: 1px solid rgba(0, 0, 0, 0.02);
          border-radius: 6px;
          object-fit: cover;
        }
      }
    }
  }
}
</style>

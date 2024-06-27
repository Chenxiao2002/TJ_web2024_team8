<template>
  <div class="container">
    <div class="header" v-show="$route.meta.showfater">
      <div class="reds-sticky">
        <div class="reds-tabs-list">
          <div :class="['reds-tab-item', 'tab-item', { active: activeTab === 'comment' }]" @click="toComment">
            <div class="badge-container">
              <span>收到的评论</span>
            </div>
          </div>
          <div :class="['reds-tab-item', 'tab-item', { active: activeTab === 'agree' }]" @click="toAgree">
            <div class="badge-container">
              <span>收到的赞</span>
            </div>
          </div>
          <div :class="['reds-tab-item', 'tab-item', { active: activeTab === 'collection' }]" @click="toCollection">
            <div class="badge-container">
              <span>被收藏</span>
            </div>
          </div>
          <div :class="['reds-tab-item', 'tab-item', { active: activeTab === 'follower' }]" @click="toFollower">
            <div class="badge-container">
              <span>新增粉丝</span>
            </div>
          </div>
        </div>
        <div class="divider" style="margin: 16px 32px 0px"></div>
      </div>
    </div>
    <router-view />
  </div>
</template>
<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

const activeTab = ref('comment');

const toComment = () => {
  router.push({ path: 'comment' });
  activeTab.value = 'comment';
};

const toAgree = () => {
  router.push({ name: 'agree' });
  activeTab.value = 'agree';
};

const toCollection = () => {
  router.push({ name: 'collection' });
  activeTab.value = 'collection';
};

const toFollower = () => {
  router.push({ name: 'follower' });
  activeTab.value = 'follower';
};

// 设置初始状态
onMounted(() => {
  const path = route.path;
  if (path.includes('comment')) {
    activeTab.value = 'comment';
  } else if (path.includes('agree')) {
    activeTab.value = 'agree';
  } else if (path.includes('collection')) {
    activeTab.value = 'collection';
  } else if (path.includes('follower')) {
    activeTab.value = 'follower';
  } else {
    router.push({ name: 'comment' });
  }
});
</script>

<style lang="less" scoped>
.container {
  flex: 1;
  padding: 0 24px;
  padding-top: 72px;
  width: 67%;
  margin: 0 auto;

  .reds-sticky {
    top: 72px;
    position: fixed;
    z-index: 1;
    width: 40rem;
    box-sizing: border-box;
    height: 72px;
    padding-top: 16px;
    justify-content: center;
    flex-direction: column;
    background: #fff;

    .reds-tabs-list {
      justify-content: flex-start;
      display: flex;
      flex-wrap: nowrap;
      position: relative;
      font-size: 16px;
      padding: 0 32px;

      .active {
        font-weight: 600;
        color: #333;
        background-color: rgba(0, 0, 0, 0.03);
        border-radius: 20px;
      }

      .reds-tab-item {
        padding: 0px 16px;
        margin-right: 0px;
        font-size: 16px;
        display: flex;
        align-items: center;
        box-sizing: border-box;
        height: 40px;
        cursor: pointer;
        color: rgba(51, 51, 51, 0.8);
        white-space: nowrap;
        transition: transform 0.3s cubic-bezier(0.2, 0, 0.25, 1);
        z-index: 1;

        .badge-container {
          position: relative;
        }
      }
    }

    .divider {
      margin: 4px 8px;
      list-style: none;
      height: 0;
      border: solid rgba(0, 0, 0, 0.08);
      border-width: 1px 0 0;
    }
  }
}
</style>

<template>
        <div v-if="followers.length === 0">
      <el-empty description="现在还没有关注消息..." />
    </div>
  <div>
    <ul class="agree-container">
      <li class="agree-item" v-for="follower in followers" :key="follower.id">
        <a class="user-avatar">
          <img class="avatar-item" :src="follower.avatarUrl" />
        </a>
        <div class="main">
          <div class="info">
            <div class="user-info">
              <a>{{ follower.name }}</a>
            </div>
            <div class="interaction-hint"><span>开始关注您了&nbsp;</span><span>{{ formatDate(follower.followedAt) }}</span></div>
          </div>
          <div class="extra">
            <button
              class="reds-button-new follow-button large"
              :class="{'primary': !follower.isMutual, 'mutual': follower.isMutual}"
              @click="toggleFollow(follower)"
            >
              <span class="reds-button-new-box"><span class="reds-button-new-text">{{ follower.isMutual ? '互相关注' : '回关' }}</span></span>
            </button>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>
<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

interface Follower {
  id: string;
  name: string;
  avatarUrl: string;
  followedAt: string;
  isMutual: boolean;
}

const followers = ref<Follower[]>([]);

const fetchFollowers = async () => {
  try {
    const response = await axios.get('/api/followers'); // 假设后端API路径是/api/followers
    followers.value = response.data;
  } catch (error) {
    console.error('Error fetching followers:', error);
  }
};

const toggleFollow = async (follower: Follower) => {
  try {
    if (follower.isMutual) {
      await axios.post(`/api/unfollow`, { userId: follower.id });
      follower.isMutual = false;
    } else {
      await axios.post(`/api/focusOn`, { userId: follower.id });
      follower.isMutual = true;
    }
  } catch (error) {
    console.error('Error toggling follow status:', error);
  }
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString();
};

onMounted(() => {
  fetchFollowers();
});
</script>
<style lang="less" scoped>
textarea {
  overflow: auto;
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
      }

      .extra {
        min-width: 48px;
        flex-shrink: 0;
        margin-left: 24px;
        .follow-button {
          width: 96px;
          &.primary {
            background-color: #2f779d;
            color: #fff;
          }
          &.mutual {
            background-color: #ccc;
            color: #333;
          }
        }
        .reds-button-new.large {
          font-size: 16px;
          font-weight: 600;
          line-height: 16px;
          padding: 0 24px;
          height: 40px;
        }
        .reds-button-new {
          position: relative;
          cursor: pointer;
          -webkit-user-select: none;
          user-select: none;
          white-space: nowrap;
          outline: none;
          background: none;
          border: none;
          vertical-align: middle;
          text-align: center;
          display: inline-block;
          padding: 0;
          border-radius: 100px;
          font-weight: 500;
        }
      }
    }
  }
}
</style>

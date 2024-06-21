<template>
      <div v-if="messages.length === 0">
      <el-empty description="现在还没有评论消息..." />
    </div>
  <div>
    <ul class="message-container">
      <li
        class="message-item"
        v-for="message in messages"
        :key="message.createTime"
        :class="{'main-comment': !message.comment_c.length, 'sub-comment': message.comment_c.length}"
        @click="goToDetail(message.post_id)"
      >
        <a class="user-avatar">
          <img class="avatar-item" :src="message.avatar" />
        </a>
        <div class="main">
          <div class="info">
            <div class="user-info">
              <a>{{ message.username }}</a>
            </div>
            <div class="interaction-hint">
              <span>评论了您的笔记&nbsp;</span><span>{{ formatDate(message.createTime) }}</span>
            </div>
            <div class="interaction-content">
              <span>{{ message.comment_p }}</span>
            </div>
            <div v-if="message.comment_c.length" class="quote-info">
              {{ message.comment_c }}
            </div>
          </div>
          <div class="extra">
            <img class="extra-image" :src="message.post_img0" />
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { useRouter,useRoute } from 'vue-router';
import { ChatRound } from '@element-plus/icons-vue';
import {getCommentInfo} from '@/apis/main';

const route = useRoute();
const router = useRouter();
const messages = ref([]);

const fetchMessages = async () => {
  const user_id = route.params.id;
  try {
    const post = await getCommentInfo({user_id})
    messages.value = post.info
    console.log(messages)
  } catch (error) {
    console.error('Error fetching comments:', error);
  }
};

const goToDetail = (postId: string) => {
  router.push(`/explore/${postId}`);
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString();
};

onMounted(async () => {
  fetchMessages()
});

</script>

<style lang="less" scoped>
textarea {
  overflow: auto;
}
.message-container {
  width: 40rem;
  .message-item {
    display: flex;
    flex-direction: row;
    padding-top: 24px;
    cursor: pointer;

    &.main-comment {
      background-color: #f9f9f9; // 主楼评论样式
    }

    &.sub-comment {
      background-color: #f0f0f0; // 楼中楼评论样式
    }

    .user-avatar {
      margin-right: 24px;
      flex-shrink: 0;

      .avatar-item {
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
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
          margin-bottom: 12px;
        }

        .quote-info {
          font-size: 12px;
          display: flex;
          align-items: center;
          color: rgba(51, 51, 51, 0.6);
          margin-bottom: 12px;
        }

        .action {
          display: flex;
          color: rgba(51, 51, 51, 0.8);

          .action-reply {
            cursor: pointer;
            width: 88px;
            height: 40px;
            border: 1px solid rgba(0, 0, 0, 0.08);
            border-radius: 999px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: rgba(51, 51, 51, 0.8);

            .action-text {
              margin-left: 4px;
              font-size: 16px;
            }
          }
        }
      }

      .extra {
        min-width: 48px;
        flex-shrink: 0;
        margin-left: 24px;

        .extra-image {
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

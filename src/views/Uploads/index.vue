<script setup>
//路由
import { useRouter } from "vue-router";
//用户信息
import { useUserStore } from "@/stores/user.js";
import { computed, onBeforeMount, ref } from "vue";
import { Back, Plus } from '@element-plus/icons-vue'
import { ElMessage } from "element-plus";
import CardDetail from "@/components/cardDetail.vue";
import { getCurrentTime } from "@/utils/getTime";
import { uploadPost } from "@/apis/main";

const router = useRouter()
const userStore = useUserStore()
const checkLogin = () => {
  if (!userStore.userInfo.id) {
    router.replace('/login')
  }
}

onBeforeMount(() => checkLogin())

const fileList = ref([])
const fileListUrl = computed(() => fileList.value.map(item => item.url))
const title = ref('')
const content = ref('')
const dialogImageUrl = ref('')
const dialogVisible = ref(false)
const postData = ref({})
const Post = ref({})
const PostId = ref(0)
//处理图片预览
const handlePictureCardPreview = (uploadFile) => {
  dialogImageUrl.value = uploadFile.url
  dialogVisible.value = true
  return true
}
//处理图像上传失败情况
const onError = async (error) => {
  ElMessage({
    type: 'warning',
    message: '图片上传失败'
  })
  //用户信息
  const userStore = useUserStore();
  await userStore.userLogout()
  //切换路由
  await router.replace('/')
}
//处理图片类型和图片大小
const handleChange = (uploadFile, uploadFiles) => {
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif']; // 可接受的图片类型
  const maxSize = 2; // 最大文件大小，单位：MB
  if (!allowedTypes.includes(uploadFile.raw.type)) {
    ElMessage.error('请上传正确的图片文件!');
    upload.value.handleRemove(uploadFile);
    return false;
  } else if (uploadFile.raw.size / 1024 / 1024 > maxSize) {
    ElMessage.error(`文件大小最多${maxSize}MB!`);
    upload.value.handleRemove(uploadFile);
    return false;
  }

  return true;
}
const upload = ref(null)
//获取发布者的ID信息
const beforeUpload = (rawFile) => {
  Post.value = {
    id: PostId.value
  }
}
const doUploads = async () => {
  if (fileListUrl.value.length === 0) {
    ElMessage.warning(
      '请至少上传一张图片!'
    )
    return
  }
  if (title.value === '') {
    ElMessage.warning(
      '请输入标题'
    )
    return
  }
  const data = {
    title: title.value,
    content: content.value + valueEmoji.value,
    user_id: userStore.userInfo.id,
    category: valueTopic.value,
    user: valueUser.value,
    // emoji: valueEmoji.value,
  }

  const res = await uploadPost(data)
  PostId.value = res.info
  upload.value.submit()
  ElMessage({ type: 'success', message: '发布成功，3秒后跳转到主页' })
  setTimeout(() => {
    router.replace('/')
  }, 3000)

}


//处理图片数量
const handleExceed = () => {
  ElMessage.warning(
    '最多可以添加9张图片哦!'
  )
}
// 制作预览页面
const show = ref(false)
const close = () => {
  show.value = false
}
const MakePrev = () => {
  if (fileListUrl.value.length === 0) {
    ElMessage.warning(
      '请至少上传一张图片!'
    )
    return
  }
  if (title.value === '') {
    ElMessage.warning(
      '请输入标题'
    )
    return
  }
  postData.value = {
    id: 1,
    title: title.value,
    content: content.value,
    user: userStore.userInfo,
    imgs: fileListUrl.value,
    createTime: getCurrentTime()
  }
  show.value = true
}

const empty = []
const valueTopic = ref('')
const valueUser = ref('')
const valueEmoji = ref('')
const topics = [
  {
    value: "学习",
    label: "学习"
  },
  {
    value: "选课",
    label: "选课"
  },
  {
    value: "拼车",
    label: "拼车"
  },
  {
    value: "实习",
    label: "实习"
  },
  {
    value: "交友",
    label: "交友"
  },
]
//获取用户信息


const user = [
  {
    value: "用户1",
    label: "wer"
  },
  {
    value: "用户2",
    label: "er"
  }
]

const emoji = [
  {
    value: "😀",
    label: "😀 开心"
  },
  {
    value: "🤣",
    label: "🤣 笑死了"
  },
  {
    value: "😂",
    label: "😂 笑哭了"
  },
  {
    value: "😁",
    label: "😁 嘻嘻"
  },
  {
    value: "😍",
    label: "😍 花痴"
  },
  {
    value: "😘",
    label: "😘 飞吻"
  },
  {
    value: "😒",
    label: "😒 不高兴"
  },
  {
    value: "😎",
    label: "😎  墨镜笑脸"
  },
]
const afterDoComment = (comment) => Details.afterDoComment(comment);
</script>

<template>
  <div style="height: 1200px;">
    <div class="boxw">
      <h1 style="text-align: left;margin-left:20px;font-size:20px">发布图文</h1>
      <div class="topArea">
        <div style="font-size: large;">图片编辑</div>
        <div class="img-container">
          <el-upload v-model:file-list="fileList" action="http://123.60.149.233:8000/upload/" class="preview"
            ref="upload" list-type="picture-card" multiple :headers="userStore.headersObj" :limit="9"
            :on-preview="handlePictureCardPreview" :on-change="handleChange" :auto-upload="false"
            :on-exceed="handleExceed" :data="Post" :before-upload="beforeUpload" :on-error="onError">
            <el-icon>
              <Plus />
            </el-icon>
          </el-upload>
        </div>
      </div>
      <div class="bottomArea">
        <div class="content-container">
          <div style="margin-left: 19px;font-family: STXihei">标题</div>
          <el-input v-model="title" maxlength="20" placeholder="填写标题，可能会有更多赞哦~" show-word-limit type="text"
            style="margin-top: 10px;width: 80%;margin-left: 20px;" />
          <div style="margin: 20px 0" />
          <div style="margin-left: 19px">内容</div>
          <el-input v-model="content" maxlength="300" placeholder="填写更全面的描述信息，让更多人看到你吧！" show-word-limit type="textarea"
            :rows=4 style="width: 80%;margin-left: 20px; margin-top: 10px; " />
        </div>
      </div>
      <div class="extra-info">
        <el-select v-model="valueTopic" placeholder="#话题" style="width: 100px; height: 30px;margin-right: 20px;">
          <el-option v-for="item in topics" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <el-select v-model="valueUser" placeholder="@用户" style="width: 100px; height: 30px;margin-right: 20px;">
          <el-option v-for="item in user" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>

        <el-select v-model="valueEmoji" placeholder="😊表情" style="width: 100px; height: 30px;margin-right: 20px;">
          <el-option v-for="item in emoji" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </div>

      <el-button style="margin-top: 20px;margin-left: 45px; color:white;" round color="#fd5656" size="large"
        @click="doUploads">发布推文
      </el-button>
      <el-button style="margin-top: 20px; margin-left: 30px" round type="primary" size="large"
        @click="MakePrev">生成预览</el-button>
      <el-dialog v-model="dialogVisible">
        <img :src="dialogImageUrl" style="width: 100%;" alt="Preview Image" />
      </el-dialog>

      <div class="overlay" v-if="show">
        <button class="backPage" @click="close">
          <el-icon>
            <Back />
          </el-icon>
        </button>
        <!-- <card-detail :detail="postData" :comments="empty" :review="true" /> -->
        <!-- <card-detail :detail="postData" :comments="null" :review="true" /> -->
        <card-detail :detail="postData" :isShow="false" :review="true" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.body {
  height: 900px;
}

/* 背景框图 */
.boxw {
  height: 600px;
  width: 600px;
  /* position: absolute; */
  overflow-y: scroll;
  margin: auto;
  /* display: flex; */
  /* flex-direction: column; */
  border-radius: 20px;
  border: #2c3e50 1px solid;
  overflow: auto;
}

.card .el-row {
  padding-left: 100px;
}

.topArea {
  display: block;
  margin: auto;
  width: 550px;
  height: 150px;
  /* background-color: rebeccapurple; */
}

.img-container {
  display: block;
  margin: auto;
  margin-left: 20px;
  margin-top: 10px;
  width: 550px;
  height: 150px;
  overflow: scroll;
}

/* 需要加穿透效果 */
>>>.el-upload--picture-card,
>>>.el-upload-list__item {
  width: 100px;
  height: 100px;
  line-height: 110px;
}


.bottomArea {
  display: block;
  margin: auto;
  width: 550px;


}

.content-container {
  margin-top: 20px;
  height: 230px;
  overflow: scroll;
}

.extra-info {
  margin-top: 8px;
  margin-left: 45px;
}

.extra-info el-button {
  width: 30px
}

.preview {
  width: 550px;
  height: 150px;
  margin: 22px;
}

/* 预览层卡牌 */
.card {
  margin-left: 10px;
  padding-left: 50px;
}

/* 预览层父元素 */
.overlay {
  position: fixed;
  margin: 0 auto;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: white;
  /* 设置透明度的背景色 */
  z-index: 99999;
  /* 设置一个较大的z-index值，确保图层位于其他内容之上 */
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
</style>

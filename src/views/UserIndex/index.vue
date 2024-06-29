<script setup>
import { useRoute } from "vue-router";
import { watch, onMounted, ref } from "vue";
import HomeCardAdv from "@/components/homeCardAdv.vue"
import CardDetail from "@/components/cardDetail.vue";

import { Back } from "@element-plus/icons-vue";
import {
  doFocus, unFollow, queryUserIndex, queryUserPost, controlUserCollectOrLike, postDelete,
  getFocusInfo, getFollowsInfo
} from "@/apis/main";
import { controlDetail } from "@/stores/controlDetail";
import { onClickOutside } from "@vueuse/core";
import { resizeWaterFall, waterFallInit, waterFallMore } from "@/utils/waterFall";
import { useUserStore } from "@/stores/user";
import { ElMessage, ElLoading } from "element-plus";


const route = useRoute()
const Details = controlDetail()
const userStore = useUserStore()

// 加载用户信息 //////////////////////////////////////////////////////////////
const userInfo = ref({})

const avatarSrc = ref('');
watch(userInfo, (newVal, oldVal) => {
  // 当userInfo对象更新时，检查是否有头像URL
  if (newVal && newVal.user && newVal.user.avatar) {
    avatarSrc.value = newVal.user.avatar;
  }
}, { deep: true });

const getUserInfo = async () => {
  const id = route.params.id
  const res = await queryUserIndex({ id })
  userInfo.value = res.data
  document.title = res.data.user.username + ' .TJ论坛'
}
const checkFollow = (id) => {
  return userStore.userFocus.includes(id)
}
const checkMine = (id) => {
  if (userStore.userInfo.id === id) {

    return false

  }
  return false;
}
const doFocusOn = async (id) => {
  if (userStore.userInfo.id === id) {
    ElMessage({ type: 'warning', message: '不能对自己进行关注操作' })
    return
  }
  const res = await doFocus({ id })
  userStore.extendUserInfo(1, id)

  await getUserInfo()
  ElMessage({ type: 'success', message: res.info })
}
const delFocusOn = async (id) => {
  if (userStore.userInfo.id === id) {
    ElMessage({ type: 'warning', message: '不能对自己进行取消关注' })
    return
  }
  const res = await unFollow({ id })
  userStore.removeFocus(1, id)

  await getUserInfo()
  ElMessage({ type: 'success', message: res.info })
}
const cancelFocusOn = async (id) => {
  const res = await unFollow({ id })
  userStore.removeFocus(1, id)
  ElMessage({ type: 'success', message: res.info })
}
// 加载用户信息结束 ////////////////////////////////////////////////////////////

// 主页切换标签 //////////////////////////////////////////////////////////////
const radio = ref('帖子')
const userPost = ref([])
const userCollect = ref([])
const userFavorite = ref([])
const disabled = ref(true); // 初始禁用滚动加载

const columns = ref(0)
const card_columns_posts = ref({})
const card_columns_like = ref({})
const card_columns_collect = ref({})
const arrHeight = ref([])


const Toggle = async () => {
  const user_id = route.params.id
  const offset = 0
  const types = radio.value
  if (radio.value === '帖子' && userPost.value.length === 0) {
    const post = await queryUserPost({ user_id, types, offset })
    userPost.value = post.info
    waterFallInit(columns, card_columns_posts, arrHeight, userPost)
  } else if (radio.value === '收藏' && userCollect.value.length === 0) {
    const post = await queryUserPost({ user_id, types, offset })
    userCollect.value = post.info
    waterFallInit(columns, card_columns_collect, arrHeight, userCollect)
  } else if (radio.value === '点赞' && userFavorite.value.length === 0) {
    const post = await queryUserPost({ user_id, types, offset })
    userFavorite.value = post.info
    waterFallInit(columns, card_columns_like, arrHeight, userFavorite)
  }
  disabled.value = false;
}
const load = async () => {
  disabled.value = true;
  const user_id = userInfo.value.user.id;
  const types = radio.value;
  if (types === '帖子') {
    const offset = userPost.value.length;
    const post = await queryUserPost({ user_id, types, offset });
    if (post.info.length === 0) {
      disabled.value = true;
    } else {
      userPost.value = [...userPost.value, ...post.info];
      waterFallMore(arrHeight, card_columns_posts, post.info)
      disabled.value = false;
    }
  } else if (types === '点赞') {
    const offset = userFavorite.value.length;
    const like = await queryUserPost({ user_id, types, offset });
    if (like.info.length === 0) {
      disabled.value = true;
    } else {
      userFavorite.value = [...userFavorite.value, ...like.info];
      waterFallMore(arrHeight, card_columns_like, like.info)
      disabled.value = false;
    }
  } else if (types === '收藏') {
    const offset = userCollect.value.length;
    const collect = await queryUserPost({ user_id, types, offset });
    if (collect.info.length === 0) {
      disabled.value = true;
    } else {
      userCollect.value = [...userCollect.value, ...collect.info];
      waterFallMore(arrHeight, card_columns_collect, collect.info)
      disabled.value = false;
    }
  }
};
// 主页切换标签结束 ///////////////////////////////////////////////////////////

// 卡片详情页的内容 //////////////////////////////////////////////////////////
const detail = Details.detail
const overlayX = ref(0); // 覆盖层的水平位置
const overlayY = ref(0); // 覆盖层的垂直位置
const overlay = ref(null)
const show = ref(false)

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
  window.history.pushState({}, '', `/user/index/${userInfo.value.user.id}`);
  document.title = userInfo.value.user.username + ' .TJ论坛'
  show.value = false
}
onClickOutside(overlay, () => {
  window.history.pushState({}, "", `/user/index/${userInfo.value.user.id}`);
  document.title = userInfo.value.user.username + ' .TJ论坛'
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
const resize = () => {
  if (radio.value === '帖子') {
    resizeWaterFall(columns, card_columns_posts, arrHeight, userPost)
  } else if (radio.value === '收藏') {
    resizeWaterFall(columns, card_columns_collect, arrHeight, userCollect)
  } else if (radio.value === '点赞') {
    resizeWaterFall(columns, card_columns_like, arrHeight, userFavorite)
  }
}

// 加载动画相关变量
const loading = ref(false);
const loadingContainer = ref(null);
let loadingInstance = null;

onMounted(async () => {
  loading.value = true;
  loadingInstance = ElLoading.service({
    target: loadingContainer.value,
    lock: true,
    text: '加载中...',
    background: 'rgba(0, 0, 0, 0.7)',
  });
  await getUserInfo()
  if (userInfo.value.user && userInfo.value.user.avatar) {
    avatarSrc.value = userInfo.value.user.avatar;
  }
  await Toggle()
  resize()
  // console.log("params: ", route.params.id)
  // console.log("my_uid: ", userStore.userInfo.id)
  // console.log("userStore: ")
  // console.log(userStore)
  loading.value = false;
  if (loadingInstance) {
    loadingInstance.close();
  }
})

import { genFileId } from 'element-plus'
import { updateUserInfo } from "@/apis/main";
import router from "../../router";

// 用户信息更新栏
////////////////////////////////////////////////////////////////
// 控制文件表单
const dialogFormVisible = ref(false)
// 文件上传对象
const upload = ref(null)
// 上传头像成功后修改pinia数据
const avatar = ref('')
const fileList = ref([])
const handleExceed = (files) => {
  upload.value.clearFiles()
  const file = files[0]
  file.uid = genFileId()
  upload.value.handleStart(file)
}
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
};
const onSuccess = async (response) => {
  avatar.value = response.info.filepath
}
const onError = async (error) => {
  ElMessage({
    type: 'warning',
    message: '头像上传失败'
  })
  const userStore = useUserStore();
  await userStore.userLogout()
  await router.replace('/')
}
// 控制表单信息
const form = ref({
  username: '',
  signature: ''
})
const openDialog = () => {
  dialogFormVisible.value = true
  form.value.username = userStore.userInfo.username
  form.value.signature = userStore.userInfo.signature
}
// 表单验证规则
const rules = {
  username: [
    { required: true, message: '用户名不能为空！', trigger: 'blur' }
  ],
  signature: [
    { required: true, message: '个性签名不能为空!', trigger: 'blur' }
  ]
}
// 表单对象
const formRef = ref(null)
const doUpdate = async () => {
  const { username, signature } = form.value;
  const isModified = username !== userStore.userInfo.username || signature !== userStore.userInfo.signature;
  const isAvatarUploaded = fileList.value.length === 1;

  if (!isModified && !isAvatarUploaded) {
    ElMessage({ type: 'warning', message: '未作任何修改！' });
    return;
  }

  if (isModified && !isAvatarUploaded) {
    await updateUserInfo({ username, signature });
    avatar.value = userStore.userInfo.avatar;
    userStore.changeInfo({ username, signature, avatar });
    ElMessage({ type: 'success', message: '用户信息更新成功' });
    dialogFormVisible.value = false;
    await getUserInfo()
    return;
  }

  if (!isModified && isAvatarUploaded) {
    await upload.value.submit();
    userStore.changeInfo({ username, signature, avatar });
    ElMessage({ type: 'success', message: '头像上传成功' });
    dialogFormVisible.value = false;
    await getUserInfo()
    avatarSrc.value = userStore.userInfo.avatar
    return;
  }

  if (isModified && isAvatarUploaded) {
    const res = await updateUserInfo({ username, signature });
    await upload.value.submit();
    userStore.changeInfo({ username, signature, avatar });
    ElMessage({ type: 'success', message: res.info });
    dialogFormVisible.value = false;
    await getUserInfo()
    avatarSrc.value = userStore.userInfo.avatar
  }
};

const allSent = ref(false)
const allStar = ref(false)
const allLike = ref(false)
const selSent = ref(null)
const selStar = ref(null)
const selLike = ref(null)

const doAllSent = () => {
  if (!selSent.value) {
    return
  }
  if (allSent.value) {
    selSent.value.selectedCardIds = userPost.value.map(item => item.id)
  }
  else {
    selSent.value.selectedCardIds = []
  }
  // console.log("allSent: ", allSent.value)
  // console.log("selSent: ", selSent.value.length)
}
const delSent = async () => {
  if (!selSent.value) {
    return
  }
  // console.log("sent: ", selSent.value.selectedCardIds)
  if (selSent.value.selectedCardIds.length === 0) {
    ElMessage({ type: 'warning', message: '您尚未选中发送的帖子' })
    return
  }

  const user_id = userInfo.value.user.id;

  for (const i in selSent.value.selectedCardIds) {
    const post_id = selSent.value.selectedCardIds[i]
    const res = await postDelete({
      id: post_id,
      user_id: user_id
    })

    ElMessage({ type: 'success', message: '成功删除帖子' })
  }

  userPost.value = userPost.value.filter(item => !selSent.value.selectedCardIds.includes(item.id))

  allSent.value = false
  selSent.value.selectedCardIds = []

  waterFallInit(columns, card_columns_posts, arrHeight, userPost)
  resizeWaterFall(columns, card_columns_posts, arrHeight, userPost)
}

const doAllStar = () => {
  if (!selStar.value) {
    return
  }
  if (allStar.value) {
    selStar.value.selectedCardIds = userCollect.value.map(item => item.id)
  }
  else {
    selStar.value.selectedCardIds = []
  }
  // console.log("allStar: ", allStar.value)
  // console.log("selStar: ", selStar.value.length)
}
const delStar = async () => {
  if (!selStar.value) {
    return
  }
  // console.log("star: ", selStar.value.selectedCardIds)
  if (selStar.value.selectedCardIds.length === 0) {
    ElMessage({ type: 'warning', message: '您尚未选中收藏的帖子' })
    return
  }

  for (const i in selStar.value.selectedCardIds) {
    const post_id = selStar.value.selectedCardIds[i]
    const res = await controlUserCollectOrLike({
      post_id: post_id,
      operator: true,
      type: 'collect'
    })

    userStore.removeFocus(3, post_id)
    ElMessage({ type: 'success', message: res.info })
  }

  userCollect.value = userCollect.value.filter(item => !selStar.value.selectedCardIds.includes(item.id))

  allStar.value = false
  selStar.value.selectedCardIds = []

  waterFallInit(columns, card_columns_collect, arrHeight, userCollect)
  resizeWaterFall(columns, card_columns_collect, arrHeight, userCollect)
}

const doAllLike = () => {
  if (!selLike.value) {
    return
  }
  if (allLike.value) {
    selLike.value.selectedCardIds = userFavorite.value.map(item => item.id)
  }
  else {
    selLike.value.selectedCardIds = []
  }
  // console.log("allLike: ", allLike.value)
  // console.log("selLike: ", selLike.value.selectedCardIds.length)
}
const delLike = async () => {
  if (!selLike.value) {
    return
  }
  // console.log("like: ", selLike.value.selectedCardIds)
  if (selLike.value.selectedCardIds.length === 0) {
    ElMessage({ type: 'warning', message: '您尚未选中点赞的帖子' })
    return
  }

  for (const i in selLike.value.selectedCardIds) {
    const post_id = selLike.value.selectedCardIds[i]
    const res = await controlUserCollectOrLike({
      post_id: post_id,
      operator: true,
      type: 'like'
    })

    userStore.removeFocus(2, post_id)
    ElMessage({ type: 'success', message: res.info })
  }

  userFavorite.value = userFavorite.value.filter(item => !selLike.value.selectedCardIds.includes(item.id))

  allLike.value = false
  selLike.value.selectedCardIds = []

  waterFallInit(columns, card_columns_like, arrHeight, userFavorite)
  resizeWaterFall(columns, card_columns_like, arrHeight, userFavorite)
}

const focusVisible = ref(false)
const focusInfo = ref([])

const followVisible = ref(false)
const followInfo = ref([])

const openFocusDialog = async () => {
  if (userStore.userInfo.id !== route.params.id) {
    ElMessage({ type: 'warning', message: '您不能查看其他人的关注列表' })
    return
  }
  focusVisible.value = true
  const res = await getFollowsInfo({ id: userStore.userInfo.id })
  focusInfo.value = res.info
  console.log("focus: ", focusInfo.value)
}
const openFollowDialog = async () => {
  if (userStore.userInfo.id !== route.params.id) {
    ElMessage({ type: 'warning', message: '您不能查看其他人的粉丝列表' })
    return
  }
  followVisible.value = true
  const res = await getFocusInfo({ id: userStore.userInfo.id })
  followInfo.value = res.info
  console.log("follow: ", followInfo.value)
}
const doFocusOnAdv = async (id) => {
  await doFocusOn(id)

  const res = await getFocusInfo({ id: userStore.userInfo.id })
  console.log("before follow: ", followInfo.value)
  followInfo.value = res.info
  console.log("after follow: ", followInfo.value)
}
const delFocusOnAdv = async (id) => {
  await delFocusOn(id)

  const res = await getFollowsInfo({ id: userStore.userInfo.id })
  console.log("before focus: ", focusInfo.value)
  focusInfo.value = res.info
  console.log("after focus: ", focusInfo.value)
}
</script>

<template>
  <div class="userInfo" v-if="userInfo.user">
    <el-row :gutter="10">
      <el-col :span="7" style="width: 250px;">
        <el-avatar :size="150" :src="avatarSrc" :key="avatarSrc"></el-avatar>
      </el-col>
      <el-col :span="7" style="width: 250px!important;">
        <div class="container">
          <h2>{{ userInfo.user.username }}</h2>

          <!-- <button class="updBtn" @click="openDialog" v-if="userStore.userInfo.id === route.params.id">

            <h5>编辑个人信息</h5>
          </button> -->
        </div>
        <p>{{ userInfo.user.signature }}</p>
        <div class="tagArea">
          <!-- 使用 el-tooltip 包裹 el-tag，并设置 content 属性 -->
          <el-tooltip content="关注数目" placement="bottom" effect="light">
            <el-tag class="ml-2" type="success" round @click="openFocusDialog">{{ userInfo.user.focusOn }} 关注</el-tag>
          </el-tooltip>
          <el-tooltip content="粉丝数目" placement="bottom" effect="light">
            <el-tag class="ml-2" type="info" round @click="openFollowDialog">{{ userInfo.user.fans }} 粉丝</el-tag>
          </el-tooltip>
          <el-tooltip content="笔记数目" placement="bottom" effect="light">
            <el-tag class="ml-2" type="warning" round>{{ userInfo.user.postsCount }} 笔记数</el-tag>
          </el-tooltip>
        </div>
      </el-col>

      <el-col :span="5" style="width: 100px;" v-if="userStore.userInfo.id !== route.params.id">
        <button class="focusOn" v-if="!checkFollow(route.params.id)" @click="doFocusOn(route.params.id)">关注</button>
        <button class="focusOff" v-else @click="delFocusOn(route.params.id)">取关</button>
      </el-col>
      <el-col :span="5" style="width: 100px;" v-else>
        <button class="focusOn" @click="openDialog">编辑信息</button>

      </el-col>
    </el-row>
  </div>
  <el-dialog v-model="focusVisible" title="我的关注列表" center draggable>
    <div class="following-list">
      <div class="user-item" v-for="focus in focusInfo" :key="focus.id">
        <RouterLink :to="`/user/index/${focus.id}`">
          <img :src="focus.avatar" alt="avatar" class="avatar" />
        </RouterLink>
        <p style="margin-left: 5%; margin-right: 5%;">用户昵称: {{ focus.username }}</p>
        <p style="margin-left: 5%; margin-right: 5%;">关注时间: {{ focus.createTime }}</p>
        <p style="margin-left: 5%; margin-right: 5%;">{{ focus.back ? "已互粉" : " " }}</p>
        <button class="delBtn" @click="delFocusOnAdv(focus.id)" style="position: absolute; right: 7%;">取关</button>
      </div>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="focusVisible = false" round>确认</el-button>
      </span>
    </template>
  </el-dialog>
  <el-dialog v-model="followVisible" title="我的粉丝列表" center draggable>
    <div class="following-list">
      <div class="user-item" v-for="follow in followInfo" :key="follow.id">
        <RouterLink :to="`/user/index/${follow.id}`">
          <img :src="follow.avatar" alt="avatar" class="avatar" />
        </RouterLink>
        <p style="margin-left: 5%; margin-right: 5%;">用户昵称: {{ follow.username }}</p>
        <p style="margin-left: 5%; margin-right: 5%;">关注时间: {{ follow.createTime }}</p>
        <p style="margin-left: 12%; margin-right: 5%;" v-if="follow.back">已互粉</p>
        <button class="addBtn" style="position: absolute; right: 12%;" @click="doFocusOnAdv(follow.id)" v-else>关注</button>
      </div>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="followVisible = false" round>确认</el-button>
      </span>
    </template>
  </el-dialog>
  <el-dialog v-model="dialogFormVisible" title="更新个人信息" center draggable>
    <div class="fileUpload">
      <div class="fileUploadContainer" style="margin-left: 7%; margin-top: 10px;">
        <el-upload v-model:file-list="fileList" ref="upload" action="http://123.60.149.233:8000/user/avatar/" :limit="1"
          :on-exceed="handleExceed" :auto-upload="false" :on-change="handleChange" :headers="userStore.headersObj"
          :on-success="onSuccess" :on-error="onError">
          <template #trigger>
            <el-button class="btn" color="#2f779d" type="primary" round>选择一个文件</el-button>
          </template>
          <template #tip>
            <div class="el-upload__tip" style="color:red;text-align: left">
              仅限一个文件，新文件将会被覆盖
            </div>
          </template>
        </el-upload>
      </div>
    </div>
    <div class="fileUpload">
      <el-form :model="form" ref="formRef" :rules="rules" label-position="top">
        <el-form-item prop="username" label="昵称" label-width="100px" style="margin: 30px;">
          <el-input v-model="form.username" maxlength="6" show-word-limit class="my" />
        </el-form-item>
        <el-form-item prop="signature" label="个性签名" label-width="100px" style="margin: 30px;">
          <el-input v-model="form.signature" class="my" />
        </el-form-item>
      </el-form>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogFormVisible = false" round>取消</el-button>
        <el-button color="#2f779d" type="primary" @click="doUpdate" round>
          确认
        </el-button>
      </span>
    </template>
  </el-dialog>
  <div class="checkBox" @change="Toggle" v-if="!loading">
    <el-radio-group fill="#2f779d" v-model="radio" size="large">
      <el-radio-button fill="#2f779d" class="radio" label="帖子" name="post" />
      <el-radio-button fill="#2f779d" class="radio" label="收藏" name="collect" />
      <el-radio-button fill="#2f779d" class="radio" label="点赞" name="like" />
    </el-radio-group>
  </div>
  <div style="margin-top: 30px;" v-if="userInfo.user">
    <div v-if="radio === '帖子'">
      <div class="checkbox-container" v-if="userStore.userInfo.id === route.params.id">
        <label>
          <input type="checkbox" v-model="allSent" @change="doAllSent" />
          全选帖子
        </label>
        <button class="delBtn" @click="delSent">删除所选帖子</button>
      </div>
      <div v-if="userPost.length === 0">
        <el-empty description="现在还没有帖子..." />
      </div>
      <div v-infinite-scroll="load" :infinite-scroll-disabled="disabled" :infinite-scroll-delay="200"
        :infinite-scroll-distance="100" v-else>
        <HomeCardAdv ref="selSent" :card_columns="card_columns_posts" @show-detail="showMessage"></HomeCardAdv>
      </div>
      <transition name="fade" @before-enter="onBeforeEnter" @after-enter="onAfterEnter" @before-leave="onBeforeLeave"
        @after-leave="onAfterLeave">
        <div class="overlay" v-if="show">
          <button style="display:none;" class="backPage" @click="close">
            <el-icon>
              <Back />
            </el-icon>
          </button>
          <card-detail :detail="detail" @afterDoComment="afterDoComment" ref="overlay" />
        </div>
      </transition>
    </div>
    <div v-else-if="radio === '收藏'">
      <div class="checkbox-container" v-if="userStore.userInfo.id === route.params.id">
        <label>
          <input type="checkbox" v-model="allStar" @change="doAllStar" />
          全选收藏
        </label>
        <button class="delBtn" @click="delStar">取消所选收藏</button>
      </div>
      <div v-if="userCollect.length === 0">
        <el-empty description="现在还没有收藏..." />
      </div>
      <div v-infinite-scroll="load" :infinite-scroll-disabled="disabled" :infinite-scroll-delay="200"
        :infinite-scroll-distance="100" v-else>
        <HomeCardAdv ref="selStar" :card_columns="card_columns_collect" @show-detail="showMessage"></HomeCardAdv>
      </div>
      <transition name="fade" @before-enter="onBeforeEnter" @after-enter="onAfterEnter" @before-leave="onBeforeLeave"
        @after-leave="onAfterLeave">
        <div class="overlay" v-if="show">
          <button style="display:none;" class="backPage" @click="close">
            <el-icon>
              <Back />
            </el-icon>
          </button>
          <card-detail :detail="detail" @afterDoComment="afterDoComment" ref="overlay" />
        </div>
      </transition>
    </div>
    <div v-else-if="radio === '点赞'">
      <div class="checkbox-container" v-if="userStore.userInfo.id === route.params.id">
        <label>
          <input type="checkbox" v-model="allLike" @change="doAllLike" />
          全选喜欢
        </label>
        <button class="delBtn" @click="delLike">取消所选点赞</button>
      </div>
      <div v-if="userFavorite.length === 0">
        <el-empty description="现在还没有点赞..." />
      </div>
      <div v-infinite-scroll="load" :infinite-scroll-disabled="disabled" :infinite-scroll-delay="200"
        :infinite-scroll-distance="100" v-else>
        <HomeCardAdv ref="selLike" :card_columns="card_columns_like" @show-detail="showMessage"></HomeCardAdv>
      </div>
      <transition name="fade" @before-enter="onBeforeEnter" @after-enter="onAfterEnter" @before-leave="onBeforeLeave"
        @after-leave="onAfterLeave">
        <div class="overlay" v-if="show">
          <button style="display:none;" class="backPage" @click="close">
            <el-icon>
              <Back />
            </el-icon>
          </button>
          <card-detail :detail="detail" @afterDoComment="afterDoComment" ref="overlay" />
        </div>
      </transition>
    </div>
  </div>
</template>

<style scoped>
.userInfo {
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: center;
}

.focusOn {
  align-items: center;
  justify-content: center;
  width: 96px;
  height: 40px;
  line-height: 18px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  background-color: #2f779d;
  border-radius: 0.8rem;
  color: #fff;
  border-color: transparent;
  margin-top: 1rem;
}

.focusOn:hover {
  background-color: #8db4ca;
}

.focusOff {
  align-items: center;
  justify-content: center;
  width: 96px;
  height: 40px;
  line-height: 18px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  background-color: lightcoral;
  border-radius: 0.8rem;
  color: #fff;
  border-color: transparent;
  margin-top: 1rem;
}

.focusOff:hover {
  background-color: pink;
}

.tagArea {
  width: 400px;
}

.tagArea .ml-2 {
  margin-right: 10px;
}

.checkBox {
  margin-top: 50px;
  position: relative;
  left: 40%;
}

.radio+.radio {
  margin-left: 30px;
}

.container {
  display: flex;
  align-items: center;
  width: 800px;
  gap: 200px;
}

.updBtn {
  width: 100px;
  background-color: #2f779d;
  color: white;
  border: none;
  padding: 12px 16px;
  font-size: 14px;
  cursor: pointer;
  border-radius: 0.8rem;
  transition: background-color 0.1s;
  display: flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
}

.updBtn:hover {
  background-color: #ffffffbb;
}

.updBtn h5 {
  margin: 0;
  font-size: 12px;
  display: inline;
}

.btn {
  align-items: center;
}

.el-upload__tip {
  align-items: center;
}

.checkbox-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
  position: fixed;
  right: 7%;
}

label {
  display: flex;
  align-items: center;
  font-size: 12px;
}

input[type="checkbox"] {
  margin-right: 8px;
}

.following-list {
  display: flex;
  flex-direction: column;
  padding: 20px;
  background-color: #fff;
  border-radius: 0.8rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.user-item {
  display: flex;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eaeaea;
  transition: background-color 0.3s;
}

.user-item:last-child {
  border-bottom: none;
  /* 移除最后一个用户项的底部边框 */
}

.avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  margin-right: 20px;
}

.username-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-right: 20px;
}

.username-info p {
  margin: 4px 0;
  font-size: 14px;
  color: #333;
}

.addBtn {
  width: 90px;
  border: 0px;
  background-color: #2f779d;
  color: white;
  padding: 8px 12px;
  font-size: 12px;
  cursor: pointer;
  border-radius: 0.8rem;
  transition: background-color 0.1s;
  display: flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
}

.addBtn:hover {
  background-color: #2f779db6;
}

.delBtn {
  width: 90px;
  border: 0px;
  background-color: lightcoral;
  color: white;
  padding: 8px 12px;
  font-size: 12px;
  cursor: pointer;
  border-radius: 0.8rem;
  transition: background-color 0.1s;
  display: flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
}

.delBtn:hover {
  background-color: rgb(240, 180, 180);
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

.fade-enter-active {
  animation: scale-up-center 0.5s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
}

.fade-leave-active {
  animation: scale-up-center 0.5s linear both reverse;
}
</style>

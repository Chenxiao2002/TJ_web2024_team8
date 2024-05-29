<script setup>
import {useRoute} from "vue-router";
import {onMounted, ref} from "vue";
import HomeCard from "@/components/homeCard.vue";
import CardDetail from "@/components/cardDetail.vue";
import {Back} from "@element-plus/icons-vue";
import {doFocus, queryUserIndex, queryUserPost} from "@/apis/main";
import {controlDetail} from "@/stores/controlDetail";
import {onClickOutside} from "@vueuse/core";
import {resizeWaterFall, waterFallInit, waterFallMore} from "@/utils/waterFall";
import {useUserStore} from "@/stores/user";
import {ElMessage} from "element-plus";

const route = useRoute()
const Details = controlDetail()
const userStore = useUserStore()

// 加载用户信息 //////////////////////////////////////////////////////////////
const userInfo = ref({})
const getUserInfo = async () => {
  const id = route.params.id
  const res = await queryUserIndex({id})
  userInfo.value = res.data
  document.title = res.data.user.username + ' .TJ论坛'
}
const checkFollow = (id) => {
  if (userStore.userInfo.id === id) {
    return true
  }
  return userStore.userFocus.includes(id)
}
const doFocusOn = async (id) => {
  if (userStore.userInfo.id === id) {
    ElMessage({type: 'warning', message: '不能对自己进行关注操作'})
    return
  }
  const res = await doFocus({id})
  userStore.extendUserInfo(1, id)
  ElMessage({type: 'success', message: res.info})
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
    const post = await queryUserPost({user_id, types, offset})
    userPost.value = post.info
    waterFallInit(columns, card_columns_posts, arrHeight, userPost)
  } else if (radio.value === '收藏' && userCollect.value.length === 0) {
    const post = await queryUserPost({user_id, types, offset})
    userCollect.value = post.info
    waterFallInit(columns, card_columns_collect, arrHeight, userCollect)
  } else if (radio.value === '点赞' && userFavorite.value.length === 0) {
    const post = await queryUserPost({user_id, types, offset})
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
    const post = await queryUserPost({user_id, types, offset});
    if (post.info.length === 0) {
      disabled.value = true;
    } else {
      userPost.value = [...userPost.value, ...post.info];
      waterFallMore(arrHeight, card_columns_posts, post.info)
      disabled.value = false;
    }
  } else if (types === '点赞') {
    const offset = userFavorite.value.length;
    const like = await queryUserPost({user_id, types, offset});
    if (like.info.length === 0) {
      disabled.value = true;
    } else {
      userFavorite.value = [...userFavorite.value, ...like.info];
      waterFallMore(arrHeight, card_columns_like, like.info)
      disabled.value = false;
    }
  } else if (types === '收藏') {
    const offset = userCollect.value.length;
    const collect = await queryUserPost({user_id, types, offset});
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
onMounted(async () => {
  await getUserInfo()
  await Toggle()
  resize()
})

import {genFileId} from 'element-plus'
import {updateUserInfo} from "@/apis/main";

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
    {required: true, message: '用户名不能为空！', trigger: 'blur'}
  ],
  signature: [
    {required: true, message: '个性签名不能为空!', trigger: 'blur'}
  ]
}
// 表单对象
const formRef = ref(null)
const doUpdate = async () => {
  const {username, signature} = form.value;
  const isModified = username !== userStore.userInfo.username || signature !== userStore.userInfo.signature;
  const isAvatarUploaded = fileList.value.length === 1;

  if (!isModified && !isAvatarUploaded) {
    ElMessage({type: 'warning', message: '未作任何修改！'});
    return;
  }

  if (isModified && !isAvatarUploaded) {
    await updateUserInfo({username, signature});
    avatar.value = userStore.userInfo.avatar;
    userStore.changeInfo({username, signature, avatar});
    ElMessage({type: 'success', message: '用户信息更新成功'});
    dialogFormVisible.value = false;
    return;
  }

  if (!isModified && isAvatarUploaded) {
    await upload.value.submit();
    userStore.changeInfo({username, signature, avatar});
    ElMessage({type: 'success', message: '头像上传成功'});
    dialogFormVisible.value = false;
    return;
  }

  if (isModified && isAvatarUploaded) {
    const res = await updateUserInfo({username, signature});
    await upload.value.submit();
    userStore.changeInfo({username, signature, avatar});
    ElMessage({type: 'success', message: res.info});
    dialogFormVisible.value = false;
  }
};

const all_sent = ref(false)
const all_star = ref(false)
const all_like = ref(false)

</script>

<template>
  <div class="userInfo" v-if="userInfo.user">
    <el-row :gutter="10">
      <el-col :span="7" style="width: 250px;">
        <el-avatar :size="150" :src="userInfo.user.avatar"></el-avatar>
      </el-col>
      <el-col :span="7" style="width: 250px!important;">
        <div class="container">
          <h2>{{ userInfo.user.username }}</h2>
          <button class="updBtn" @click="openDialog">
            <h5>编辑个人信息</h5>
          </button>
        </div>
        <p>{{ userInfo.user.signature }}</p>
        <div class="tagArea">
          <el-tag class="ml-2" type="success" round>{{ userInfo.user.focusOn }} 关注</el-tag>
          <el-tag class="ml-2" type="info" round>{{ userInfo.user.fans }} 粉丝</el-tag>
          <el-tag class="ml-2" type="warning" round>{{ userInfo.user.postsCount }} 笔记数</el-tag>
        </div>
      </el-col>
      <el-col :span="5" style="width: 100px;">
        <button class="focusOn" v-if="!checkFollow(userInfo.user.id)" @click="doFocusOn(userInfo.user.id)">关注</button>
      </el-col>
    </el-row>
  </div>
  <el-dialog v-model="dialogFormVisible" title="更新个人信息" center draggable>
    <div class="fileUpload">
      <el-upload v-model:file-list="fileList"
                 ref="upload"
                 action="http://localhost:8000/user/avatar/"
                 :limit="1"
                 :on-exceed="handleExceed"
                 :auto-upload="false"
                 :on-change="handleChange"
                 :headers="userStore.headersObj"
                 :on-success="onSuccess"
                 :on-error="onError"
      >
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
    <div class="fileUpload">
      <el-form :model="form" ref="formRef" :rules="rules" label-position="top">
        <el-form-item prop="username" label="昵称" label-width="100px" style="margin: 30px;">
          <el-input v-model="form.username" maxlength="6"
                    show-word-limit class="my"/>
        </el-form-item>
        <el-form-item prop="signature" label="个性签名" label-width="100px" style="margin: 30px;">
          <el-input v-model="form.signature" class="my"/>
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
  <div class="checkBox" @change="Toggle">
    <el-radio-group fill="#2f779d"  v-model="radio" size="large">
      <el-radio-button fill="#2f779d" class="radio" label="帖子" name="post"/>
      <el-radio-button fill="#2f779d" class="radio" label="收藏" name="collect"/>
      <el-radio-button fill="#2f779d" class="radio" label="点赞" name="like"/>
    </el-radio-group>
  </div>
  <div style="margin-top: 30px;" v-if="userInfo.user">
    <div v-if="radio === '帖子'">
      <div v-if="userPost.length === 0">
        <el-empty description="现在还没有帖子..."/>
      </div>
      <div v-infinite-scroll="load" :infinite-scroll-disabled="disabled" :infinite-scroll-delay="200"
           :infinite-scroll-distance="100"
           v-else>
        <home-card :card_columns="card_columns_posts" @show-detail="showMessage"></home-card>
      </div>
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
      <div class="checkbox-container">
        <label>
          <input type="checkbox" v-model="all_sent" />
          全选帖子
        </label>
        <button class="delBtn">删除所选帖子</button>
      </div>
    </div>
    <div v-else-if="radio === '收藏'">
      <div v-if="userCollect.length === 0">
        <el-empty description="现在还没有收藏..."/>
      </div>
      <div v-infinite-scroll="load" :infinite-scroll-disabled="disabled" :infinite-scroll-delay="200"
           :infinite-scroll-distance="100"
           v-else>
        <home-card :card_columns="card_columns_collect" ref="overlay" @show-detail="showMessage"></home-card>
      </div>
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
      <div class="checkbox-container">
        <label>
          <input type="checkbox" v-model="all_star" />
          全选收藏
        </label>
        <button class="delBtn">取消所选收藏</button>
      </div>
    </div>
    <div v-else-if="radio === '点赞'">
      <div v-if="userFavorite.length === 0">
        <el-empty description="现在还没有点赞..."/>
      </div>
      <div v-infinite-scroll="load" :infinite-scroll-disabled="disabled" :infinite-scroll-delay="200"
           :infinite-scroll-distance="100"
           v-else>
        <home-card :card_columns="card_columns_like" @show-detail="showMessage"></home-card>
      </div>
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
      <div class="checkbox-container">
        <label>
          <input type="checkbox" v-model="all_like" />
          全选喜欢
        </label>
        <button class="delBtn">取消所选点赞</button>
      </div>
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
  border-radius: 1000px;
  color: #fff;
  border-color: transparent;
  margin-top: 1rem;
}

.focusOn:hover {
  background-color: #8db4ca;
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

.radio + .radio {
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
  border-radius: 100px;
  transition: background-color 0.1s;
  display: flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
}

.updBtn:hover {
  opacity: .6;
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
  right: 10%;
}

label {
  display: flex;
  align-items: center;
  font-size: 12px;
}

input[type="checkbox"] {
  margin-right: 8px;
}

.delBtn {
  width: 90px;
  background-color: white;
  border: 1px solid lightcoral;
  color: black;
  padding: 8px 12px;
  font-size: 12px;
  cursor: pointer;
  border-radius: 6px;
  transition: background-color 0.1s;
  display: flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
}

.delBtn:hover {
  background-color: lightcoral;
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
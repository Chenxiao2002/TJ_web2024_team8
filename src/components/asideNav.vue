<script setup>
import {ref} from "vue";
import {Promotion, Expand, Close, Tools, Bell} from "@element-plus/icons-vue";
import {useUserStore} from "@/stores/user";
import Login from '@/views/Login/index.vue';
import {ElMessage} from "element-plus";
import router from "@/router";

const userStore = useUserStore();
// 控制菜单样式
const isMenuOpen = ref(false);
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

// 登出
const confirm = async () => {
  const res = await userStore.userLogout();
  ElMessage({type: 'success', message: res.info});
  router.push({path: '/'}); //登出后跳到“发现”主页
};

// 显示登录界面
const show = ref(false);
const changeShow = () => {
  show.value = !show.value;
};
</script>

<template>
<div>
  <!-- tooltip为文字提示 -->
  <nav class="menu" :class="{ open: isMenuOpen }">
    <el-tooltip effect="dark" content="切换菜单样式" placement="right">
      <div class="actionsBar">
        <div>
          <button id="menuBtn" type="button" @click="toggleMenu"><i class="iconfont icon-hanbaocaidan"></i></button>
          <h3 class="menuText" :class="{ open2: isMenuOpen }">{{ userStore.userInfo.username }}</h3>
        </div>
      </div>
    </el-tooltip>
    <ul class="optionsBar">
      <li class="menuItem">
        <el-tooltip effect="dark" content="发现" placement="right">
          <RouterLink to="/" class="menuOption">
            <i class="iconfont icon-shouye"></i>
            <h5 class="menuText" :class="{ open2: isMenuOpen }">发现</h5>
          </RouterLink>
        </el-tooltip>
      </li>
      <li class="menuBreak"> 
        <hr>
      </li>
      <li class="menuItem" v-if="userStore.userInfo.status != 2">
        <el-tooltip effect="dark" content="发布" placement="right">
          <RouterLink to="/user/uploads" class="menuOption">
            <el-icon size="x-large">
              <Promotion/>
            </el-icon>
            <h5 class="menuText" :class="{ open2: isMenuOpen }">发布</h5>
          </RouterLink>
        </el-tooltip>
      </li>
      <li class="menuItem" v-if="userStore.userInfo.id && userStore.userInfo.status != 2">
        <el-tooltip effect="dark" content="通知" placement="right">
          <RouterLink to="/user/control">
            <div class="menuOption">
               <i class="iconfont icon-tongzhi"></i>
              <h5 class="menuText" :class="{ open2: isMenuOpen }">通知</h5>
            </div>
          </RouterLink>
        </el-tooltip>
      </li>
      <li class="menuItem" v-if="userStore.userInfo.id && userStore.userInfo.status === 0">
        <el-tooltip effect="dark" content="用户管理" placement="right">
          <RouterLink to="/manager">
            <div class="menuOption">
              <el-icon size="x-large">
                <Tools/>
              </el-icon>
              <h5 class="menuText" :class="{ open2: isMenuOpen }">用户管理</h5>
            </div>
          </RouterLink>
        </el-tooltip>
      </li>
    </ul>
    <div class="about" id="about">
    </div>
    <div v-if="userStore.userInfo.id && userStore.userInfo.status != 2">
      <div class="menuUser">
        <RouterLink :to="`/user/index/${userStore.userInfo.id}`">
          <div>
            <img :src="userStore.userInfo.avatar" alt="">
          </div>
          <h5 class="Username menuText" :class="{ open2: isMenuOpen }" v-show="isMenuOpen">
            {{ userStore.userInfo.username }}
          </h5>
          <p class="menuText" :class="{ open2: isMenuOpen }"><i class="iconfont icon-youjiantou"></i></p>
        </RouterLink>
      </div>
      <div class="themeBar">
        <el-tooltip effect="dark" content="退出登录" placement="right">
          <div> 
            <!-- 气泡确认框，确认是否要退出登录 -->
            <el-popconfirm @confirm="confirm" title="确认退出吗?" confirm-button-text="确认"
                           cancel-button-text="取消">
              <template #reference>
                <button type="button"><i class="iconfont icon-tuichu"></i></button>
              </template>
            </el-popconfirm>
          </div>
        </el-tooltip>
      </div>
    </div>
    <div v-else>
      <el-tooltip effect="dark" content="登录" placement="right">
        <div class="themeBar">
          <div>
            <button title="登录" type="button" @click="changeShow">
              <el-icon size="x-large">
                <Expand/>
              </el-icon>
            </button>
          </div>
        </div>
      </el-tooltip>
    </div>
  </nav>
  <!-- 登录组件的显示 -->
  <div class="overlay" v-if="show">
    <el-button class="close" @click="changeShow" plain round>
      <el-icon size="x-large">
        <Close/>
      </el-icon>
    </el-button>
    <login @changeShow="changeShow" class="login"/>
  </div>
</div>
</template>


<style scoped>

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* 设置透明度的背景色 */
  z-index: 9999; /* 设置一个较大的z-index值，确保图层位于其他内容之上 */
  display: flex;
  justify-content: center;
  align-items: center;
}
.login{
  /* position: absolute; */
  position: fixed;
}

.close {
  border: 0;
  position: absolute;
  left: 68%;
  top: 17%;
  background-color: #fff;
  z-index: 1000; /* 设置一个较大的z-index值，确保图层位于其他内容之上 */
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.iconfont {
  font-size: 20px;
}

.menu {
  position: absolute;
  width: 60px;
  height: 86%;
  background-color: #f3f5f6;
  z-index: 2;
  top: 65px;
  bottom: 0;
  left: 10px;
  margin: auto;
  border-radius: 0.8rem;
  transition: 0.3s ease 0.15s;
  font-family: sans-serif;
}

.menu a {
  text-decoration: none;
}

.menu .actionsBar {
  width: 100%;
  height: 10%;
  padding: 0.5rem;
  overflow: hidden;
}

.menu .actionsBar div {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-around;
  border-radius: 0.5rem;
  transition: 0.3s ease;
}

.menu .actionsBar div button {
  background-color: transparent;
  outline: none;
  border: none;
  border-radius: 0.5rem;
  color: #000;
  width: 45px;
  height: 45px;
  transition: 0.3s ease;
  font-size: 1rem;
}

.menu .actionsBar div button:hover {
  background-color: #d0d3d5;
  color: #2f779d;

}

.menu .actionsBar div h3 {
  width: calc(100% - 45px);
  text-align: left;
}

.menu .optionsBar {
  overflow: hidden;
  display: flex;
  width: 100%;
  height: 60%;
  padding: 0 0.5rem;
  align-items: center;
  flex-direction: column;
}

.menu .optionsBar .menuItem {
  width: 100%;
  height: 45px;
  margin: 0.3rem;
}

.menu .optionsBar .menuItem .menuOption {
  font-size: 1rem;
  outline: none;
  border: none;
  background-color: transparent;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-around;
  border-radius: 0.5rem;
  transition: 0.3s ease;
}

.menu .optionsBar .menuItem .menuOption:hover {
  background-color: #d0d3d5;
  color: #2f779d;

}

.menu .optionsBar .menuItem .menuOption:hover i,
.menu .optionsBar .menuItem .menuOption:hover h5 {
  color: #2f779d;

}

.menu .optionsBar .menuItem .menuOption i {
  width: 45px;
  text-align: center;
  color: #000;
}

.menu .optionsBar .menuItem .menuOption h5 {
  width: calc(100% - 45px);
}

.menuText {
  color: #000;
  transform: translateX(-250px);
  opacity: 0;
  transition: transform 0.3s ease 0.1s;
}

.menu .about {
  width: 100%;
  height: 10%;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 1rem;
  flex-direction: column;
  font-family: sans-serif;
  opacity: 0;
  white-space: nowrap;
  transition: 0.3s ease 0.15s;
}

.menu.open {
  width: 240px;
  opacity: 0.9;
}

.menuText.open2 {
  opacity: 1;
  transform: translateX(0);
  text-align: left;
}

.menu .menuBreak {
  width: 100%;
  height: 10px;
  display: flex;
  align-items: left;
  justify-content:baseline;
}

.menu .menuBreak hr {
  width: 95%;
  height: 3px;
  background-color: #000;
  border: none;
  border-radius: 5px;
}

.menu .themeBar {
  overflow: hidden;
  width: 100%;
  height: 5%;
  padding: 0.5rem;
  position: absolute; /* 绝对定位 */
  bottom: 6%; /* 距离父元素底部20px */
}

.menu .themeBar div {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-around;
  border-radius: 0.5rem;
  transition: 0.3s ease;
}

.menu .themeBar div button {
  background-color: transparent;
  outline: none;
  border: none;
  border-radius: 0.5rem;
  color: #000;
  width: 100%;
  height: 45px;
  transition: 0.3s ease;
  font-size: 1rem;
}

.menu .themeBar div button:hover {
  background-color: #d0d3d5;
  color: #2f779d;

}

.menu .menuUser {
  position: absolute; /* 设置绝对定位 */
  bottom: 15%; /* 设置距离父元素底部的距离，例如20px */
  width: 100%;
  height: 10%;
}

.menu .menuUser a {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  text-decoration: none;
  padding: 0.5rem;
  position: relative;
}

.menu .menuUser a div {
  width: 45px;
  height: 45px;
  position: relative;
  border-radius: 0.5rem;
}

.menu .menuUser a div img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.menu .menuUser a .Username {
  width: calc(70% - 45px);
}

.menu .menuUser a p {
  width: calc(30% - 45px);
}

.menu .menuUser a:hover p {
  animation: animArrow 0.3s ease 2;
  color: #2f779d;

}

@keyframes animArrow {
  0% {
    transform: translateX(0);
  }

  50% {
    transform: translateX(5px);
  }

  100% {
    transform: translateX(0);
  }
}

.menu .menuUser .userInfo {
  position: absolute;
  width: 20rem;
  height: 18rem;
  opacity: 0;
  pointer-events: none;
  top: 34%;
  left: 1.5rem;
  transition: 0.3s ease;
  transform: scale(0);
  transform-origin: bottom left;
}

.menu .menuUser:hover .userInfo {
  pointer-events: all;
  opacity: 1;
  transform: scale(1);
  color: #2f779d;
}

.el-button--text {
  margin-right: 15px;
}

.el-select {
  width: 300px;
}

.el-input {
  width: 300px;
}

.dialog-footer button:first-child {
  margin-right: 10px;
}
</style>
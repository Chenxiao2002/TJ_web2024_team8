<script setup>
import { onMounted } from 'vue';

onMounted(() => {
  console.log('NotFound component mounted.');
  console.log('Current URL:', window.location.href);
});
</script>

<template>
  <div class="not-found">
    <h1 style="color:red;">404 - 页面不存在</h1>
    <p>你输入了一个错误的网址哦.</p>
    <router-link to="/">返回主页</router-link>
    <div>
      <h3>调试信息</h3>
      <p>当前URL: {{ currentUrl }}</p>
      <p>时间戳: {{ timestamp }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentUrl: window.location.href,
      timestamp: new Date().toLocaleString()
    };
  },
  mounted() {
    console.log('NotFound component data:', this.currentUrl, this.timestamp);
  }
}
</script>

<style scoped>
.not-found {
  text-align: center;
  padding: 20px;
}
</style>

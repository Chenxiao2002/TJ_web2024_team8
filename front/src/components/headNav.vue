<script setup>
import {ref} from "vue";
import {Search} from '@element-plus/icons-vue'
import {useRouter} from "vue-router";

const router = useRouter()
// searchValue
const searchInput = ref('')
// search
const searchThings = () => {
  router.replace(`/?query=${searchInput.value}`)
}

</script>

<template>
  <div class="header-row">
    <RouterLink to="/">
      <img  class="icon" width="180" height="70" src="/icon2.png" alt="">
    </RouterLink>
    <el-input class="my" v-model="searchInput" placeholder="搜索点什么...." @keyup.enter="searchThings" :prefix-icon="Search" clearable/>
  </div>
  
  
</template>

<style scoped>
.header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 5px;
}

.icon {
  width: 170px;
  height: 65px;
  margin-right: 20px;
}
.my {
  width: 100%;
}
</style>
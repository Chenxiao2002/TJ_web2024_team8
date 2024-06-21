<script setup>

</script>

<template>
  <el-container>
    <el-header style="padding-left:4px;padding-right:32px">
      <head-nav/>
    </el-header>
    <el-container>
      <el-aside width="80px" class="aside">
        <aside-nav/>
      </el-aside>
      <el-main class="maxSize" id="content">
        <RouterView :key="$route.fullPath"/>
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.maxSize {
  height: 700px;
  padding: 15px;
  margin-top: 10px;
  box-sizing: border-box;
  overflow-y: scroll;
}
.aside{
  
}
</style>
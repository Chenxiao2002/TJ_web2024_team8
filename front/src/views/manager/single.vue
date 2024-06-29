<script setup xmlns="http://www.w3.org/1999/html">
import {computed, onBeforeMount, onMounted, ref} from 'vue'
import {queryUserPostControl, postDelete, controlUserCollectOrLike, unFollow, removeFan} from "@/apis/main";
import {ElMessage} from 'element-plus'
import {Back} from "@element-plus/icons-vue";
import {useUserStore} from "@/stores/user";
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import {useTableStore} from "@/stores/tableStore";
import {InfoFilled} from "@element-plus/icons-vue";
import {useRouter,useRoute} from "vue-router";

const route = useRoute()
const id = route.params.id;
const router = useRouter()
const userStore = useUserStore();

// 配置全局语言和表格缓存//////////////////////////////////////////////
const locale = zhCn
const tableStore = useTableStore();
const loading = ref(true)
// 控制选择器 /////////////////////////////////////////////////////
const value = ref('posts')
const options = [
  {
    label: '帖子详情',
    options: [
      { value: 'posts', label: '个人帖子详情' },
      { value: 'collected', label: '收藏帖子详情' },
      { value: 'favorites', label: '喜欢帖子详情' }
    ],
  },
  {
    label: '个人用户详情',
    options: [
      { value: 'fans', label: '粉丝详情' },
      { value: 'follow', label: '关注详情' },
    ],
  },
]
const type = computed(() => {
  if (value.value === 'posts' || value.value === 'collected' || value.value === 'favorites')
    return 1
  else
    return 2
})
const changeShow = async () => {
  const valueType = value.value;
  const offset = 0;
  const types = valueType;
  
  loading.value = true
  try {
  const res = await queryUserPostControl({ offset, types, id });

    if (type.value === 1) {
      tableData.value = res.info;
      total_post.value = res.total;
    } else {
      userData.value = res.info;
      total_user.value = res.total;
    }

    // 重置当前页码为1
    currentPage.value = 1;
  } catch (error) {
    console.error("Error fetching data: ", error);
    ElMessage.error('获取数据失败');
  } finally {
    // 请求完成后，将loading设置为false
    loading.value = false;
  }
};
////////////////////////////////////////////////////////////////

// 表格/////////////////////////////////////////////////////////
const tableData = ref([])
const userData = ref([])
const multipleSelection = ref([])
const tableRef = ref(null)
// 获得初始数据
const getData = async () => {
  const offset = 0
  const types = value.value

  loading.value = true
  const res = await queryUserPostControl({offset, types ,id})
  console.log(res);
  tableData.value = res.info
  total_post.value = res.total
  
  loading.value = false
}
const handleSelectionChange = (val) => {
  multipleSelection.value = val
}
////////////////////////////////////////////////////////////////

// 分页器 ///////////////////////////////////////////////////////
const pageSize = ref(10)
const currentPage = ref(1)
const total_post = ref(0)
const total_user = ref(0)
const handleCurrentChange = async (val) => {
  const offset = (val - 1) * pageSize.value;
  const types = value.value;
  let data, total;
  if (type.value === 1) {
    loading.value = true
    const res = await queryUserPostControl({offset, types, id});
    data = res.info;
    total = res.total;
    loading.value = false
    tableData.value = data;
    total_post.value = total;
  } else {
    loading.value = true
    const res = await queryUserPostControl({offset, types});
    data = res.info;
    total = res.total;
    loading.value = false
    userData.value = data;
    total_user.value = total;
  }
};
//////////////////////////////////////////////////////////////////
onMounted(() => {
  getData()
})

const close = () => {
  router.push(`/manager`)
};
</script>

<template>
  <el-config-provider :locale="locale">
    <div class="head">
      <button class="backPage" @click="close">
        <el-icon>
          <Back/>
        </el-icon>
      </button>
      <el-select
          v-model="value"
          placeholder="Select"
          @change="changeShow"
          style="width:50%;"
      >
        <el-option-group
            v-for="group in options"
            :key="group.label"
            :label="group.label"
        >
          <el-option
              v-for="item in group.options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
          />
        </el-option-group>
      </el-select>
    </div>
    <div style="display:flex;align-items: center;flex-direction: column" v-if="type === 1">
      <el-table
          :data="tableData"
          style="width: 100%"
          ref="tableRef"
          :default-sort="{ prop: 'date', order: 'descending' }"
          @selection-change="handleSelectionChange"
          v-loading="loading"
          border
          stripe
      >
        <!-- <el-table-column type="selection" width="55"/> -->
        <el-table-column label="日期" sortable prop="date"/>
        <el-table-column label="作者" prop="username"/>
        <el-table-column label="标题" prop="title"/>
        <el-table-column label="内容" prop="content" :show-overflow-tooltip='true'/>
        <el-table-column label="评论量" sortable prop="commentCount"/>
        <el-table-column label="点赞量" sortable prop="likeCount"/>
        <el-table-column label="收藏量" sortable prop="collectCount"/>
      </el-table>
      <div class="pageArea">
        <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :background="true"
            layout="prev, pager, next, jumper"
            :total="total_post"
            @current-change="handleCurrentChange"
        />
      </div>
    </div>
    <div style="display:flex;align-items: center;flex-direction: column" v-else>
      <el-table
          :data="userData"
          style="width: 100%"
          ref="tableRef"
          @selection-change="handleSelectionChange"
          border
          v-loading="loading"
          stripe
      >
        <!-- <el-table-column type="selection" width="55"/> -->
        <el-table-column align="center" label="头像">
          <template #default="scope">
            <el-avatar :src="scope.row.avatar"></el-avatar>
          </template>
        </el-table-column>
        <el-table-column label="用户名" sortable prop="username" :show-overflow-tooltip='true'/>
        <el-table-column label="粉丝量" prop="fans"/>
        <el-table-column label="关注量" prop="follow"/>
        <el-table-column label="笔记数" prop="note"/>
      </el-table>
      <div class="pageArea">
        <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :background="true"
            layout="prev, pager, next, jumper"
            :total="total_user"
            @current-change="handleCurrentChange"
        />
      </div>
    </div>
  </el-config-provider>
</template>

<style scoped>
.pageArea {
  margin-top: 20px;
}
.head{
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px; /* 设置按钮和选择框之间的间隔 */
  margin-bottom: 20px;
}
.backPage {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  border: 1px solid var(--color-border);
  cursor: pointer;  
  /* 鼠标指针将变成手型（通常是一个指向的手指），这通常用于指示元素是可点击的。 */
  background-color: #2f779d;
  color: #ffffff;
  font-size: 20px; /* 调整图标大小 */
}

.item {
  margin-top: 10px;
  margin-right: 40px;
}

</style>
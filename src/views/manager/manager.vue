<script setup>
import { computed, onBeforeMount, onMounted, ref } from 'vue';
import { queryUserPostControl, getAllId } from "@/apis/main";
import { ElMessage } from 'element-plus';
import { useUserStore } from "@/stores/user";
import zhCn from 'element-plus/dist/locale/zh-cn.mjs';
import { useTableStore } from "@/stores/tableStore";
import { InfoFilled } from "@element-plus/icons-vue";
import { useRouter } from "vue-router";

const router = useRouter();
const userStore = useUserStore();
const checkLogin = () => {
    if (!userStore.userInfo.id) {
        router.replace('/login');
    }
};

onBeforeMount(() => checkLogin());

// 配置全局语言和表格缓存
const locale = zhCn;
const tableStore = useTableStore();
const loading = ref(true);

// 表格数据
const tableData = ref([]);
const userData = ref([]);
const multipleSelection = ref([]);
const tableRef = ref(null);

const getData = async () => {
    loading.value = true;
    try {
        const response = await getAllId(userStore.userInfo.id); // 获取所有用户ID
        const ids = response.info; // 直接使用返回的数组
        console.log(ids); // 打印返回的数据结构以进行调试
        const promises = ids.map(userId => queryUserPostControl({ offset: 0, types: 2, id: userId }));// 通过ID调用queryUserPostControl
        const results = await Promise.all(promises);
        userData.value = results.map(res => res.info);
        loading.value = false;
    } catch (error) {
        loading.value = false;
        console.error('获取数据失败:', error);
    }
};

const handleSelectionChange = (val) => {
    multipleSelection.value = val;
};

const handleDelete = async (index, row) => {
    const id = row.id;
    try {
        userData.value.splice(index, 1);
        ElMessage.success('删除成功');
    } catch (error) {
        ElMessage.error('删除失败');
    }
};

const handleRowClick = (row) => {
    router.push(`/singlr/${row.id}`);
};

// 分页器
const pageSize = ref(10);
const currentPage = ref(1);
const total_user = ref(0);
const handleCurrentChange = async (val) => {
    const offset = (val - 1) * pageSize.value;
    const cachedData = tableStore.retrieveData('user', val);
    let data, total;

    if (cachedData) {
        data = cachedData.data;
        total = cachedData.total;
    } else {
        loading.value = true;
        const response = await getAllId(userStore.userInfo.id); // 获取所有用户ID
        const ids = response.info; // 直接使用返回的数组
        console.log(ids); // 打印返回的数据结构以进行调试
        const promises = ids.map(userId => queryUserPostControl({ offset, types: 2, id: userId }));// 通过ID调用queryUserPostControl
        data = res.info;
        total = res.total;
        tableStore.storeMessage('user', val, data, total);
        loading.value = false;
    }
    userData.value = data;
    total_user.value = total;
};

onMounted(() => {
    getData();
});
</script>

<template>
    <el-config-provider :locale="locale">
        <div style="display:flex;align-items: center;flex-direction: column">
            <el-table :data="userData" style="width: 100%" ref="tableRef" @selection-change="handleSelectionChange"
                @row-click="handleRowClick" border v-loading="loading" stripe>
                <el-table-column type="selection" width="55" />
                <el-table-column label="ID" prop="id" />
                <el-table-column align="center" label="头像">
                    <template #default="scope">
                        <el-avatar :src="scope.row.avatar"></el-avatar>
                    </template>
                </el-table-column>
                <el-table-column label="用户名" sortable prop="username" :show-overflow-tooltip='true' />
                <el-table-column label="粉丝量" prop="fans" />
                <el-table-column label="关注量" prop="follow" />
                <el-table-column label="笔记数" prop="note" />
                <el-table-column align="center" label="操作">
                    <template #default="scope">
                        <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">
                            移除
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div style="margin-top: 20px" v-show="multipleSelection.length !== 0">
                <el-button disabled round>选中删除</el-button>
                <el-button @click="tableRef.clearSelection()" round>清空全选</el-button>
            </div>
            <div class="pageArea">
                <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :background="true"
                    layout="prev, pager, next, jumper" :total="total_user" @current-change="handleCurrentChange" />
            </div>
        </div>
    </el-config-provider>
</template>

<style scoped>
.pageArea {
    margin-top: 20px;
}

.item {
    margin-top: 10px;
    margin-right: 40px;
}
</style>

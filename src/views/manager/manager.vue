<script setup>
import { onBeforeMount, onMounted, ref } from 'vue';
import { getAllId,setAdmin,block,unblock } from "@/apis/main";
import { ElMessage } from 'element-plus'
import { useUserStore } from "@/stores/user";
import zhCn from 'element-plus/dist/locale/zh-cn.mjs';
import { useTableStore } from "@/stores/tableStore";
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
        const result = await getAllId(userStore.userInfo.id); // 获取所有用户ID
        console.log(result.info);
        userData.value = result.info;
        loading.value = false;
    } catch (error) {
        loading.value = false;
        console.error('获取数据失败:', error);
    }
};

const handleSelectionChange = (val) => {
    multipleSelection.value = val;
};

const handleDelete = async (row) => {
    const id = row.id;
    try {
        const res = await block({ id })
        ElMessage({ type: 'success', message: res.info })
        await getData();  // 刷新表格数据
    } catch (error) {
        ElMessage({ type: 'error', message: error });
        console.log(error);
    }
};

const set_Admin = async (row) => {
    const id = row.id;
    try {
        const res = await setAdmin({ id })
        ElMessage({ type: 'success', message: res.info });
        console.log(res);
        await getData();  // 刷新表格数据
    } catch (error) {
        ElMessage.error({ type: 'error', message: error });
        console.log(error);
    }
};

const unblockUser = async (row) => {
    const id = row.id;
    try {
        const res = await unblock({ id })
        ElMessage({ type: 'success', message: res.info });
        console.log(res);
        await getData();  // 刷新表格数据
    } catch (error) {
        ElMessage.error({ type: 'error', message: error });
    }
};

const handleRowClick = (row) => {
    router.push(`/single/${row.id}`);
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
        const res = await getAllId(userStore.userInfo.id); // 获取所有用户ID
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
                border v-loading="loading" stripe>
                <el-table-column label="ID" prop="id" />
                <el-table-column label="用户名" sortable prop="username" :show-overflow-tooltip='true' />
                <el-table-column label="状态">
                    <template #default="scope">
                        <span v-if="scope.row.status === 0">管理员</span>
                        <span v-if="scope.row.status === 1">普通用户</span>
                        <span v-if="scope.row.status === 2">黑名单</span>
                    </template>
                </el-table-column>
                <el-table-column align="center" label="操作">
                    <template #default="scope">
                        <el-button v-if="scope.row.status === 1" size="small" type="success" @click="set_Admin(scope.row)">
                            设为管理员
                        </el-button>
                        <el-button v-if="scope.row.status === 0 || scope.row.status === 1" size="small" type="danger" @click="handleDelete(scope.row)">
                            拉黑
                        </el-button>
                        <el-button v-if="scope.row.status === 2" size="small" type="warning" @click="unblockUser(scope.row)">
                            解除黑名单
                        </el-button>
                    </template>
                </el-table-column>
                <el-table-column align="center" label="详情">
                    <template #default="scope">
                        <el-button plain size="small" type="primary" @click="handleRowClick(scope.row)">
                            查看详情
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
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

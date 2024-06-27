import {ref} from "vue";
import {useUserStore} from "@/stores/user";
import {postDetail} from "@/apis/main";

export const controlDetail = () => {
    const detail = ref({})      // 存储帖子详情
    const comments = ref([])    // 存储评论列表
    const content = ref('')     // 评论内容
    const userStore = useUserStore()
    // 更新评论计数的函数
    const afterDoComment = () => {
        detail.value.commentCount += 1
    }
    // 获取帖子详情的函数
    const getDetail = async (id) => {
        const res = await postDetail({id});
        console.log("帖子详情",res.info);
        detail.value = res.info
        document.title = detail.value.title;    // 更新页面标题为帖子标题
    }

    const SetComment = (comment) => {
        comments.value = [...comments.value, ...comment]    // 合并新评论和现有评论
    }

    // 返回定义的数据和方法
    return {
        detail,
        comments,
        content,
        afterDoComment,
        getDetail,
        SetComment
    }
}
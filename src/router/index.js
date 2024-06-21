import {createRouter, createWebHistory} from 'vue-router';

const Home = () => import('@/views/Home/index.vue');
const Login = () => import('@/views/Login/index.vue');
const Detail = () => import('@/views/Details/index.vue');
const Explore = () => import('@/views/Explore/index.vue');
const UserIndex = () => import('@/views/UserIndex/index.vue');
const Uploads = () => import('@/views/Uploads/index.vue');
const NotFound = () => import('@/views/NotFound/index.vue');
const UserPostControl = () => import('@/views/UserPostControl/index.vue');
import {useUserStore} from "@/stores/user";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),//BASE_URL是一个全局变量，它是在vite.config.js中配置的
    routes: [
        {
            path: '/',
            component: Home,
            meta: {
                title: '欢迎来到TJ论坛~',
            },
            children: [
                {
                    path: '',
                    component: Explore,
                    meta: {
                        title: '欢迎来到TJ论坛~',
                    },
                },
                {
                    path: 'explore/:id',
                    component: Detail,
                    meta: {
                        title: '这里是卡片详情页！',
                    },
                },
                {
                    path: 'user/index/:id',
                    component: UserIndex,
                    meta: {
                        title: 'TJ论坛-分享你的生活',
                    },
                },
                {
                    path: 'user/uploads',
                    component: Uploads,
                    meta: {
                        title: '发布 .TJ论坛',
                    },
                },
                {
                    path: 'user/control',
                    component: UserPostControl,
                    meta: {
                        title: '信息管理 .TJ论坛',
                    },
                },
            ],
        },
        {
            path: '/login',
            component: Login,
            meta: {
                title: '欢迎登录TJ论坛分享你的生活',
            },
        },
        {
            path: '/:catchAll(.*)',
            component: NotFound,
            meta: {
                title: '你想找什么呢？',
            },
        },
    ],
});
router.beforeEach((to, from, next) => {
    // 获取目标路由的相关信息，例如路由元信息 meta
    const {meta} = to;

    // 获取用户信息
    const userStore = useUserStore();
    const userInfo = userStore.userInfo;

    // 根据用户信息动态设置网页标题
    if (userInfo.username && meta.title) {
        meta.title = `${userInfo.username} - ${meta.title}`;
    }
    // 继续导航
    next();
});


router.afterEach((to, from) => {
    // 根据当前路由信息来设置新的 title
    document.title = to.meta.title || '欢迎来到TJ论坛~';
});

export default router

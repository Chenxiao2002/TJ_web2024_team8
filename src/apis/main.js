import http from "@/utils/http";

// 登录
export const login = ({email, password}) => {
    return http({
        url: '/login/',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        data: {
            email,
            password
        }
    })
}


// 注册
export const Register = ({email, username, password}) => {
    return http({
        url: '/register/',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        data: {
            username,
            password,
            email
        }
    })
}

// 访问用户主页
export const queryUserIndex = ({id}) => {
    return http({
        url: '/index/',
        method: 'POST',
        data: {
            id
        }
    })
}

// 上传帖子
export const uploadPost = (data) => {
    return http({
        url: '/upload/info/',
        method: 'POST',
        data: data
    })
}

// 帖子详情
export const postDetail = ({id}) => {
    return http({
        url: '/post/detail/',
        method: 'POST',
        data: {
            id
        }
    })
}

// 主页帖子
export const queryPost = ({offset,category, query}) => {
    return http({
        url: '/post/',
        method: 'POST',
        data: {offset,category, query}
    })
}

// 评论帖子
export const doComment = ({data}) => {
    return http({
        url: '/comment/',
        method: 'POST',
        data: data
    })
}

// 用户关注
export const doFocus = ({id}) => {
    return http({
        url: '/focus/',
        method: 'POST',
        data: {id}
    })
}

// 获取用户关注
export const queryUserFocus = () => {
    return http({
        url: '/user/focus/',
    })
}

export const unFollow = ({id}) => {
    return http({
        url: '/user/unfollow/',
        method: 'POST',
        data: {id}
    })
}

export const updateUserInfo = ({username, signature}) => {
    return http({
        url: '/user/update/',
        method: 'POST',
        data: {
            username,
            signature
        }
    })
}

export const queryUserPost = ({user_id, types, offset}) => {
    return http({
        url: '/user/post/',
        method: 'POST',
        data: {
            user_id,
            types,
            offset
        }
    })
}

export const controlUserCollectOrLike = ({post_id, operator, type}) => {
    return http({
        url: '/post/control/',
        method: 'POST',
        data: {
            post_id,
            type,
            operator
        }
    })
}

export const getComment = ({id, offset}) => {
    return http({
        url: '/comment/main/',
        method: 'POST',
        data: {
            id,
            offset
        }
    })
}
//获取被评论消息
export const getCommentInfo = ({id}) => {
    return http({
        url: '/getCommentInfo/',
        method: 'POST',
        data: {
            id,
        }
    })
}
//获取被点赞消息
export const getLikeInfo = ({id}) => {
    return http({
        url: '/getLikeInfo/',
        method: 'POST',
        data: {
            id,
        }
    })
}
//获取被收藏消息
export const getCollectInfo = ({id}) => {
    return http({
        url: '/getCollectInfo/',
        method: 'POST',
        data: {
            id,
        }
    })
}
//获取被关注消息
export const getFocusInfo = ({id}) => {
    return http({
        url: '/getFocusInfo/',
        method: 'POST',
        data: {
            id,
        }
    })
}

//获取关注消息
export const getFollowsInfo = ({id}) => {
    return http({
        url: '/getFollowsInfo/',
        method: 'POST',
        data: {
            id,
           }
    })
}


//获取所有用户id
export const getAllId = ({id}) => {
    return http({
        url: '/admin/getAllUsers/',
        method: 'POST',
        data: {
            id
        }
    })
}

//设为管理员
export const setAdmin = ({id}) => {
    return http({
        url: '/admin/set_admin/',
        method: 'POST',
        data: {
            id
        }
    })
}

//拉黑
export const block = ({id}) => {
    return http({
        url: '/admin/block/',
        method: 'POST',
        data: {
            id
        }
    })
}
//取消拉黑
export const unblock = ({id}) => {
    return http({
        url: '/admin/unblock/',
        method: 'POST',
        data: {
            id
        }
    })
}
export const queryUserPostControl = ({offset, types, id}) => {
    return http({
        url: '/user/post/control/',
        method: 'POST',
        data: {
            offset,
            types,
            id
        }
    })
}

export const postDelete = ({id}) => {
    return http({
        url: '/post/delete/',
        method: 'POST',
        data: {
            id
        }
    })
}

export const removeFan = ({id}) => {
    return http({
        url: '/user/remove/fan/',
        method: 'POST',
        data: {
            id
        }
    })
}

export const loadReplies = ({id, offset}) => {
    return http({
        url: '/comment/reply/',
        method: 'POST',
        data: {
            id,
            offset
        }
    })
}

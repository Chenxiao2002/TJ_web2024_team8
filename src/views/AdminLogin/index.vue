<template>
    <div>
        <el-card class="box-card">
            <h2 style="text-align: center;">管理员登录</h2>
            <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-position="left"
                label-width="70px" class="login-from">
                <el-form-item label="用户名" prop="name">
                    <el-input v-model="ruleForm.name"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="pwd">
                    <el-input type="pwd" v-model="ruleForm.pwd" autocomplete="off"></el-input>
                </el-form-item>
            </el-form>
            <div class="btnGroup">
                <el-button style="margin-left: 110px;" type="primary" @click="submitForm('ruleForm')"
                    v-loading="loading">登录</el-button>
                <el-button @click="resetForm('ruleForm')" style="background: skyblue;margin-left: 30px;">重置</el-button>
            </div>
        </el-card>
    </div>
</template>

<script>
export default {
    data() {
        return {
            ruleForm: {
                name: "",
                pwd: "",
            },
            rules: {
                name: [
                    { required: true, message: "用户名不能为空！", trigger: "blur" },
                ],
                pwd: [
                    { required: true, message: "密码不能为空！", trigger: "blur" },
                ],
            },
            loading: false,
        };
    },
    methods: {
        submitForm(formName) {
            this.$refs[formName].validate((valid) => {
                this.loading = true;
                if (valid) {
                    let _this = this;
                    // 使用 axios 将登录信息发送到后端
                    this.axios({
                        url: "/api/user/admin",               // 请求地址
                        method: "post",                       // 请求方法
                        headers: {                            // 请求头
                            "Content-Type": "application/json",
                        },
                        params: {                             // 请求参数
                            name: _this.ruleForm.name,
                            pwd: _this.ruleForm.pwd,
                        },
                    }).then((res) => {
                        if (res.data.code === "0") {  // 当响应的编码为 0 时，说明登录成功
                            sessionStorage.setItem("userInfo", JSON.stringify(res.data.data));
                            // 跳转页面到管理员首页
                            this.$router.push('/plate');
                            // 显示后端响应的成功信息
                            this.$message({
                                message: res.data.msg,
                                type: "success",
                            });
                        } else {
                            // 显示后端响应的失败信息
                            this.$message({
                                message: res.data.msg,
                                type: "warning",
                            });
                        }
                        _this.loading = false;
                        console.log(res);
                    });
                } else {
                    console.log("error submit!!");
                    this.loading = false;
                    return false;
                }
            });
        },
        resetForm(formName) {
            this.$refs[formName].resetFields();
        },
    },
};
</script>

<style scoped>
.box-card {
    margin: auto auto;
    margin-top: 50px;
    width: 400px;
}

.login-from {
    margin: auto auto;
}
</style>

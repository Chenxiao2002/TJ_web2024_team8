import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'

// element-plus
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import {ElementPlusResolver} from 'unplugin-vue-components/resolvers'



// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        // element-plus
        AutoImport({
            resolvers: [ElementPlusResolver()],
        }),
        Components({
            // 1.配置elementPlus采用sass
            resolvers: [ElementPlusResolver({importStyle: "sass"})],
        }),
    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        }
    },
    server:{
        proxy:{
            '/api':{
                target:'http://123.60.149.233:8000',//后端接口地址
                changeOrigin:true,
                rewrite:path=>path.replace(/^\/api/,''),
            },
        },
    },
})

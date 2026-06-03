import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// 引入全局css配置
import '@/styles/index.css'
import '@/styles/font.css'
import '@/styles/color.css'

// 引入字体文件
import '@/assets/font/SmileySans/SmileySans-Oblique.ttf'
import '@/assets/font/SmileySans/SmileySans-Oblique.otf'
import '@/assets/font/SmileySans/SmileySans-Oblique.otf.woff2'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

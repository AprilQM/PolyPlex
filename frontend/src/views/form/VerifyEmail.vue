<template>
  <div class="verify-page">
    <div class="verify-card">

      <!-- 加载中 -->
      <template v-if="state === 'loading'">
        <div class="spinner"></div>
        <h2>验证中</h2>
        <p>正在验证您的邮箱，请稍候...</p>
      </template>

      <!-- 验证成功 -->
      <template v-else-if="state === 'success'">
        <div class="icon-circle success">
          <i class="iconfont icon-check" style="font-size:32px"></i>
        </div>
        <h2>邮箱验证成功</h2>
        <p class="desc">您的邮箱已通过验证，即将跳转至工作台...</p>
        <div class="spinner small"></div>
      </template>

      <!-- 已过期 -->
      <template v-else-if="state === 'expired'">
        <div class="icon-circle expired">
          <i class="iconfont icon-clock-alert" style="font-size:32px"></i>
        </div>
        <h2>链接已过期</h2>
        <p class="desc">该验证链接已过期（有效期 30 分钟），请重新注册。</p>
        <button class="btn-primary" @click="go('/form/register')">重新注册</button>
      </template>

      <!-- 已被使用 -->
      <template v-else-if="state === 'used'">
        <div class="icon-circle used">
          <i class="iconfont icon-check-done-02" style="font-size:32px"></i>
        </div>
        <h2>该链接已被使用</h2>
        <p class="desc">该验证码已使用过，您的账号已经激活。</p>
        <button class="btn-primary" @click="go('/form/login')">去登录</button>
      </template>

      <!-- 无效链接 -->
      <template v-else-if="state === 'invalid'">
        <div class="icon-circle invalid">
          <i class="iconfont icon-close-circle" style="font-size:32px"></i>
        </div>
        <h2>无效的验证链接</h2>
        <p class="desc">{{ errorMsg }}</p>
        <button class="btn-primary" @click="go('/form/login')">返回登录</button>
      </template>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore'
import '@/assets/icon/form/iconfont.css'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const state = ref('loading')
const errorMsg = ref('')

onMounted(async () => {
  const code = route.query.code
  if (!code) {
    state.value = 'invalid'
    errorMsg.value = '缺少验证码参数'
    return
  }

  // 延迟一小段时间让加载动画展示（体验更好）
  await new Promise(r => setTimeout(r, 600))

  try {
    await userStore.verifyCode(code)
    state.value = 'success'
    setTimeout(() => router.push('/form/pending-approval'), 2000)
  } catch (e) {
    const msg = e.message
    if (msg.includes('已过期') || msg.includes('无效')) {
      state.value = 'expired'
    } else if (msg.includes('已使用') || msg.includes('已验证')) {
      state.value = 'used'
    } else {
      state.value = 'invalid'
    }
    errorMsg.value = msg
  }
})

function go(path) {
  router.push(path)
}
</script>

<style scoped>
.verify-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: var(--gray-100);
}
.verify-card {
  background: var(--gray-0);
  padding: 56px 48px 48px;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.06);
  width: 400px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

/* 图标圆形容器 */
.icon-circle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}
.icon-circle.success { background: var(--green-50); color: var(--green-500); }
.icon-circle.expired { background: var(--yellow-50); color: var(--yellow-500); }
.icon-circle.used   { background: var(--blue-50); color: var(--blue-500); }
.icon-circle.invalid { background: var(--red-50); color: var(--red-500); }

h2 { margin: 0 0 12px; font-size: 20px; color: var(--gray-900); font-weight: 600; }
.desc { color: var(--gray-500); font-size: 14px; line-height: 1.6; margin: 0 0 24px; }

/* 加载动画 */
.spinner {
  width: 36px; height: 36px;
  border: 3px solid var(--gray-200);
  border-top-color: var(--green-deep-500);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 16px;
}
.spinner.small { width: 20px; height: 20px; border-width: 2px; margin: 0 auto; }
@keyframes spin { to { transform: rotate(360deg); } }

/* 按钮 */
.btn-primary {
  display: inline-block;
  padding: 10px 32px;
  background: var(--green-deep-500);
  color: var(--gray-0);
  border: none;
  border-radius: 8px;
  font-size: 15px;
  cursor: pointer;
  text-decoration: none;
}
.btn-primary:hover { background: var(--green-deep-600); }
.btn-primary.loading { position: relative; color: transparent; }
.btn-primary.loading::after {
  content: '';
  position: absolute;
  top: 50%; left: 50%;
  width: 20px; height: 20px;
  margin-top: -10px;
  margin-left: -10px;
  border: 3px solid rgba(255,255,255,0.3);
  border-top-color: var(--gray-0);
  border-radius: 50%;
  animation: btn-spin 0.7s linear infinite;
}
@keyframes btn-spin { to { transform: rotate(360deg); } }
</style>

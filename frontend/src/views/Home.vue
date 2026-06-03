<template>
    <div class="polyplex-landing">
        <!-- 导航栏 -->
        <nav class="navbar" :class="{ scrolled: isScrolled }">
            <div class="nav-container">
                <div class="logo" @click="scrollTo('home')">
                    <img :src="logoIconSrc" alt="PolyPlex Logo" class="logo-icon-img" />
                    <span class="logo-text">PolyPlex</span>
                    <div class="version">v0.1.0</div>
                </div>
                <div class="nav-links" :class="{ active: mobileMenuOpen }">
                    <a href="#home" @click.prevent="scrollTo('home')">首页</a>
                    <a href="#features" @click.prevent="scrollTo('features')">核心功能</a>
                    <a href="#workflow" @click.prevent="scrollTo('workflow')">工作流</a>
                    <a href="#unique" @click.prevent="scrollTo('unique')">独特优势</a>
                    <a href="#templates" @click.prevent="scrollTo('templates')">模板生态</a>
                </div>
                <div class="nav-actions">
                    <!-- 未登录状态：显示登录/注册按钮 -->
                    <template v-if="!isLoggedIn">
                        <button class="btn-login" @click="handleLogin">登录</button>
                        <button class="btn-register" @click="handleRegister">注册</button>
                    </template>
                    <!-- 已登录状态：显示用户信息和通知 -->
                    <template v-else>
                        <div :class="['notice-icon', 'iconfont', 'icon-tongzhi', { 'has-notice': userStore.hasUnreadMessage }]" @click="goToNotice"></div>
                        <div class="user-info">
                            <span class="username" @click="goToUserSpace">{{ userStore.username }}</span>
                            <span class="email">{{ userStore.email }}</span>
                        </div>
                        <img :src="userStore.avatar" @error="handleAvatarError" class="avatar" @click="goToUserSpace" />
                    </template>
                    <button class="mobile-toggle" @click="mobileMenuOpen = !mobileMenuOpen">
                        <i class="iconfont icon-menu"></i>
                    </button>
                </div>
            </div>
        </nav>

        <!-- Hero 区域 -->
        <section id="home" class="hero">
            <div class="hero-bg"></div>
            <div class="hero-content">
                <div class="hero-badge">
                    <span class="badge-pulse"></span>
                    AI-Native 创意协作平台
                </div>
                <h1 class="hero-title">
                    让灵感<br />
                    <span class="gradient-text">瞬间变成结构化项目</span>
                </h1>
                <p class="hero-desc">
                    PolyPlex 是首个为团队打造的灵感集存与项目共创平台。<br />
                    AI 将你的模糊想法一键转化为结构化草稿，配合 Git 式分支管理，<br />
                    让每一个创意分支都能有序生长。
                </p>
                <div class="hero-buttons">
                    <button class="btn-hero-primary" @click="goToWorkbench">前往工作台</button>
                    <button class="btn-hero-secondary" @click="scrollTo('features')">了解更多</button>
                </div>
            </div>
            <div class="hero-visual">
                <div class="floating-card card-1">
                    <i class="iconfont icon-lightbulb"></i>
                    <span>灵感速记</span>
                </div>
                <div class="floating-card card-2">
                    <i class="iconfont icon-robot"></i>
                    <span>AI 生成草稿</span>
                </div>
                <div class="floating-card card-3">
                    <i class="iconfont icon-branches"></i>
                    <span>分支探索</span>
                </div>
                <div class="demo-window">
                    <div class="demo-bar">
                        <i class="iconfont icon-sparkles"></i>
                        PolyPlex AI · 项目预览
                    </div>
                    <div class="demo-content">
                        <div class="demo-line"></div>
                        <div class="demo-line short"></div>
                        <div class="demo-block"></div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 核心功能 -->
        <section id="features" class="features">
            <div class="container">
                <div class="section-header">
                    <span class="section-tag">核心能力</span>
                    <h2>从灵感到落地的<span class="gradient-text">全流程 AI 共创</span></h2>
                    <p>打破传统工具的割裂体验，让 AI 成为团队的共创伙伴</p>
                </div>
                <div class="features-grid">
                    <div class="feature-card" v-for="feature in features" :key="feature.title">
                        <div class="feature-icon" :style="{ background: feature.gradient }">
                            <i :class="feature.iconClass"></i>
                        </div>
                        <h3>{{ feature.title }}</h3>
                        <p>{{ feature.desc }}</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- 工作流展示 -->
        <section id="workflow" class="workflow">
            <div class="container">
                <div class="section-header">
                    <span class="section-tag">三步启动</span>
                    <h2>极简<span class="gradient-text">核心工作流</span></h2>
                    <p>从想法到可协作的项目，只需三个步骤</p>
                </div>
                <div class="workflow-steps">
                    <div class="step" v-for="(step, idx) in steps" :key="idx">
                        <div class="step-number">{{ idx + 1 }}</div>
                        <div class="step-icon">
                            <i :class="step.iconClass"></i>
                        </div>
                        <h4>{{ step.title }}</h4>
                        <p>{{ step.desc }}</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- 分支管理特色 Banner -->
        <section id="unique" class="git-banner">
            <div class="git-content">
                <div class="git-text">
                    <div class="git-badge">Git 式分支管理</div>
                    <h2>大胆探索，<span class="gradient-text-light">安全合并</span></h2>
                    <p>每个疯狂的想法都可以在独立分支上自由实验，成熟后再合并到主分支。再大胆的脑洞，也不会冲撞项目主干。</p>
                    <div class="git-features">
                        <span><i class="iconfont icon-branches"></i> 无限功能分支</span>
                        <span><i class="iconfont icon-clock"></i> 完整版本记录</span>
                        <span><i class="iconfont icon-git-merge"></i> 合并请求审核</span>
                    </div>
                </div>
                <div class="git-visual">
                    <div class="branch-graph">
                        <div class="branch-line main"></div>
                        <div class="branch-line feature" style="top: 40px;"></div>
                        <div class="branch-line feature2" style="top: 80px;"></div>
                        <div class="branch-node"></div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 模板生态 -->
        <section id="templates" class="templates">
            <div class="container">
                <div class="section-header">
                    <span class="section-tag">丰富模板</span>
                    <h2>覆盖<span class="gradient-text">多领域</span>的页面模板</h2>
                    <p>每个模板都是专业组件的有机组合，告别空白页恐惧</p>
                </div>
                <div class="templates-grid">
                    <div class="template-category" v-for="cat in templateCategories" :key="cat.name">
                        <i :class="cat.iconClass"></i>
                        <span>{{ cat.name }}</span>
                    </div>
                </div>
                <div class="template-showcase">
                    <div class="showcase-item" v-for="tmpl in showcaseTemplates" :key="tmpl">
                        <div class="showcase-preview"></div>
                        <span>{{ tmpl }}</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- CTA 区域 -->
        <section class="cta">
            <div class="cta-card">
                <h3>准备好让创意有序生长了吗？</h3>
                <p>加入 PolyPlex，体验 AI 原生协作的未来</p>
                <div class="cta-buttons">
                    <button class="btn-cta-primary" @click="goToWorkbench">前往工作台</button>
                    <button class="btn-cta-outline" @click="handleContact">联系我们</button>
                </div>
            </div>
        </section>

        <!-- 页脚 -->
        <footer class="footer">
            <div class="footer-content">
                <div class="footer-brand">
                    <div class="footer-logo">
                        <img :src="logoIconSrc" alt="PolyPlex" class="footer-logo-icon" />
                        <span>PolyPlex</span>
                    </div>
                    <p>灵感集存 · 项目共创 · AI 原生</p>
                </div>
                <div class="footer-links">
                    <div class="link-group">
                        <h4>产品</h4>
                        <a href="#" @click.prevent="scrollTo('features')">功能</a>
                        <a href="#" @click.prevent="scrollTo('templates')">模板库</a>
                    </div>
                    <div class="link-group">
                        <h4>资源</h4>
                        <a href="#" @click.prevent="handleNavClick('help')">帮助中心</a>
                        <a href="#" @click.prevent="handleNavClick('community')">社区</a>
                    </div>
                    <div class="link-group">
                        <h4>公司</h4>
                        <a href="#" @click.prevent="handleNavClick('about')">关于我们</a>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <span>© 2025 PolyPlex. 让每一个创意都有生长的土壤。</span>
            </div>
        </footer>

        <!-- 全局 Toast 提示 -->
        <Transition name="toast-fade">
            <div v-if="toastVisible" class="global-toast">
                <i class="iconfont icon-info"></i>
                <span>{{ toastMessage }}</span>
            </div>
        </Transition>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore'
import defaultAvatar from '@/assets/image/user/default_avatar.png'
import "@/assets/icon/home/iconfont.css"

const router = useRouter()
const userStore = useUserStore()

// 响应式数据
const isScrolled = ref(false)
const mobileMenuOpen = ref(false)
const toastVisible = ref(false)
const toastMessage = ref('')

// Logo 资源路径
const logoIconSrc = new URL('@/assets/image/logo/PolyPlex-logo.svg', import.meta.url).href

// 登录状态判断
const isLoggedIn = computed(() => !!userStore.token)

// 核心功能卡片数据
const features = [
    { title: '灵感 → 项目草稿', desc: '一句话输入，AI 自动生成结构化项目骨架，包含预设页面与组件。', gradient: 'linear-gradient(135deg, #1a4d3e, #438f71)', iconClass: 'iconfont icon-cc-magic' },
    { title: '页面智能深化', desc: '选中任意组件，AI 生成结构化建议，不覆盖已有内容。', gradient: 'linear-gradient(135deg, #3b82f6, #60a5fa)', iconClass: 'iconfont icon-layers' },
    { title: 'AI 版本迭代', desc: '对整个页面进行智能升级，生成新版本提案，完整保留历史。', gradient: 'linear-gradient(135deg, #f59e0b, #fbbf24)', iconClass: 'iconfont icon-refresh' },
    { title: '分支探索模式', desc: '创建分支后让 AI 生成激进方向的修改提案，快速搭建平行宇宙。', gradient: 'linear-gradient(135deg, #10b981, #14b8a6)', iconClass: 'iconfont icon-branches' },
    { title: 'Git 式版本管理', desc: '完整的分支、提交、合并请求机制，创意探索有序可控。', gradient: 'linear-gradient(135deg, #ef4444, #f87171)', iconClass: 'iconfont icon-git' },
    { title: '多端同步', desc: '桌面端深度创作，移动端快速捕获灵感，数据实时同步。', gradient: 'linear-gradient(135deg, #8b5cf6, #d946ef)', iconClass: 'iconfont icon-Devices' }
]

// 工作流步骤数据
const steps = [
    { title: '灵感投喂', desc: '在灵感速记中输入任意想法，无需结构化。', iconClass: 'iconfont icon-lightbulb' },
    { title: 'AI 构建草稿', desc: 'AI 理解语义，自动生成多页面项目骨架。', iconClass: 'iconfont icon-robot' },
    { title: '团队协作', desc: '分支探索、页面深化、合并决策，全流程共创。', iconClass: 'iconfont icon-team' }
]

// 模板分类数据
const templateCategories = [
    { name: '商业与创业', iconClass: 'iconfont icon-charts-line' },
    { name: '软件开发', iconClass: 'iconfont icon-code' },
    { name: '产品设计', iconClass: 'iconfont icon-pen' },
    { name: '写作与内容', iconClass: 'iconfont icon-edit' },
    { name: '学术与研究', iconClass: 'iconfont icon-graduation-hat' },
    { name: '影视与游戏', iconClass: 'iconfont icon-film' },
    { name: '营销与运营', iconClass: 'iconfont icon-megaphone' },
    { name: '生活与个人', iconClass: 'iconfont icon-user' }
]

// 展示模板
const showcaseTemplates = ['精益画板', '用户旅程地图', 'SWOT 分析', '系统架构图', '情绪板', '故事大纲']

// Toast 提示函数
const showToast = (message) => {
    toastMessage.value = message
    toastVisible.value = true
    setTimeout(() => {
        toastVisible.value = false
    }, 2500)
}

// 滚动监听
const handleScroll = () => {
    isScrolled.value = window.scrollY > 60
}

// 平滑滚动到指定区域
const scrollTo = (sectionId) => {
    const element = document.getElementById(sectionId)
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' })
        mobileMenuOpen.value = false
    }
}

// 前往工作台
const goToWorkbench = () => {
    router.push('/workbench/dashboard')
}

// 登录处理
const handleLogin = () => {
    router.push('/form/login')
}

// 注册处理
const handleRegister = () => {
    router.push('/form/register')
}

// 通知页面
const goToNotice = () => {
    router.push('/workbench/notice')
}

// 个人空间
const goToUserSpace = () => {
    router.push(`/workbench/user-space/${userStore.id}`)
}

const handleContact = () => {
    router.push('/')
}

// 导航点击
const handleNavClick = (target) => {
    const messages = {
        pricing: '定价方案即将发布，敬请期待',
        help: '帮助中心正在建设中',
        api: 'API 文档即将开放',
        community: '社区即将上线',
        about: '关于我们 - 让每一个创意都有生长的土壤',
        blog: '技术博客即将上线',
        jobs: '招聘信息即将发布'
    }
    showToast(messages[target] || '功能开发中，敬请期待')
}

// 默认头像报错处理
const handleAvatarError = (e) => {
    e.target.src = defaultAvatar
}

// 生命周期
onMounted(() => {
    window.addEventListener('scroll', handleScroll)
})

onBeforeUnmount(() => {
    window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.polyplex-landing {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--gray-50);
    color: var(--gray-900);
    overflow-x: hidden;
}

.container {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 24px;
}

/* 导航栏 */
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100;
    padding: 16px 0;
    transition: all 0.3s ease;
    background: transparent;
}
.navbar.scrolled {
    background: var(--gray-0);
    backdrop-filter: blur(12px);
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    padding: 12px 0;
}
.nav-container {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.logo {
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
}
.logo-icon-img {
    height: 48px;
    width: auto;
    border-radius: 14px;
    box-shadow: 0 0 8px var(--green-deep-200);
}
.logo-text {
    font-size: 24px;
    font-weight: 700;
    background: linear-gradient(135deg, var(--green-deep-500) 0%, var(--peach-500) 100%);
    background-clip: text;
    -webkit-background-clip: text;
    color: transparent;
}
.version {
    background-color: var(--gray-200);
    white-space: nowrap;
    padding: 2px 12px;
    border-radius: 20px;
    box-shadow: 0 0 3px var(--gray-300) inset;
    font-size: 12px;
    color: var(--green-deep-800);
}
.nav-links {
    display: flex;
    gap: 32px;
    white-space: nowrap;
}
.nav-links a {
    text-decoration: none;
    color: var(--gray-600);
    font-weight: 500;
    transition: color 0.2s;
}
.nav-links a:hover {
    color: var(--green-deep-500);
}
.nav-actions {
    display: flex;
    gap: 16px;
    align-items: center;
}
.btn-login, .btn-register {
    padding: 8px 20px;
    border-radius: 40px;
    font-weight: 600;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
}
.btn-login {
    background: transparent;
    border: 1px solid var(--gray-300);
    color: var(--gray-700);
}
.btn-login:hover {
    border-color: var(--green-deep-500);
    color: var(--green-deep-500);
}
.btn-register {
    background: var(--green-deep-500);
    color: var(--gray-0);
    box-shadow: 0 2px 6px rgba(26, 77, 62, 0.2);
}
.btn-register:hover {
    background: var(--green-deep-600);
    transform: translateY(-1px);
}
.notice-icon {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    border-radius: 50%;
    cursor: pointer;
    position: relative;
    transition: background 0.2s;
}
.notice-icon:hover {
    background: var(--gray-100);
}
.notice-icon::after {
    content: '';
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: var(--green-deep-500);
    position: absolute;
    top: 8px;
    right: 8px;
    display: none;
}
.has-notice::after {
    display: block;
}
.user-info {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}
.username {
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: color 0.2s;
}
.username:hover {
    color: var(--green-deep-500);
}
.email {
    font-size: 12px;
    color: var(--gray-500);
}
.avatar {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    cursor: pointer;
    object-fit: cover;
}
.mobile-toggle {
    display: none;
    background: none;
    border: none;
    cursor: pointer;
    padding: 8px;
    font-size: 24px;
    color: var(--gray-600);
}

/* Hero 区域 */
.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 120px 5% 80px;
    position: relative;
    overflow: hidden;
}
.hero-bg {
    position: absolute;
    top: -50%;
    right: -20%;
    width: 80%;
    height: 120%;
    background: radial-gradient(circle, rgba(26,77,62,0.06) 0%, rgba(26,77,62,0.01) 70%);
    pointer-events: none;
}
.hero-content {
    flex: 1;
    max-width: 600px;
    z-index: 2;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(26, 77, 62, 0.1);
    padding: 6px 16px;
    border-radius: 40px;
    font-size: 14px;
    font-weight: 500;
    color: var(--green-deep-600);
    margin-bottom: 24px;
}
.badge-pulse {
    width: 8px;
    height: 8px;
    background: var(--green-deep-500);
    border-radius: 50%;
    animation: pulse 1.5s infinite;
}
.hero-title {
    font-size: 56px;
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 24px;
}
.gradient-text {
    background: linear-gradient(135deg, var(--green-deep-500), var(--green-deep-300));
    background-clip: text;
    -webkit-background-clip: text;
    color: transparent;
}
.hero-desc {
    font-size: 18px;
    color: var(--gray-500);
    line-height: 1.6;
    margin-bottom: 32px;
}
.hero-buttons {
    display: flex;
    gap: 16px;
    margin-bottom: 48px;
}
.btn-hero-primary, .btn-hero-secondary {
    padding: 12px 28px;
    border-radius: 40px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
}
.btn-hero-primary {
    background: var(--green-deep-500);
    color: var(--gray-0);
    border: none;
    box-shadow: 0 4px 12px rgba(26, 77, 62, 0.3);
}
.btn-hero-primary:hover {
    background: var(--green-deep-600);
    transform: translateY(-2px);
}
.btn-hero-secondary {
    background: transparent;
    border: 1px solid var(--gray-300);
    color: var(--gray-700);
}
.hero-visual {
    flex: 1;
    position: relative;
    min-height: 400px;
}
.floating-card {
    position: absolute;
    background: var(--gray-0);
    padding: 16px 24px;
    border-radius: 32px;
    box-shadow: 0 20px 35px -12px rgba(0,0,0,0.1);
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 500;
    font-size: 16px;
    animation: float 4s ease-in-out infinite;
}
.floating-card i {
    font-size: 28px;
    color: var(--green-deep-500);
}
.card-1 { top: 10%; left: 10%; animation-delay: 0s; }
.card-2 { top: 50%; right: 15%; animation-delay: 1s; }
.card-3 { bottom: 15%; left: 25%; animation-delay: 2s; }
.demo-window {
    position: absolute;
    bottom: 10%;
    right: 5%;
    width: 300px;
    background: var(--gray-0);
    border-radius: 20px;
    box-shadow: 0 25px 40px -12px rgba(0,0,0,0.2);
    overflow: hidden;
}
.demo-bar {
    background: var(--gray-100);
    padding: 14px 16px;
    font-size: 14px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--gray-600);
}
.demo-bar i {
    font-size: 18px;
}
.demo-content {
    padding: 20px;
    background: var(--gray-0);
}
.demo-line {
    height: 10px;
    background: var(--gray-200);
    border-radius: 6px;
    margin-bottom: 14px;
}
.demo-line.short { width: 60%; }
.demo-block { height: 70px; background: var(--green-deep-50); border-radius: 14px; }

/* 通用章节 */
.section-header {
    text-align: center;
    margin-bottom: 64px;
}
.section-tag {
    display: inline-block;
    background: var(--green-deep-50);
    color: var(--green-deep-600);
    padding: 4px 16px;
    border-radius: 40px;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 16px;
}
.section-header h2 {
    font-size: 40px;
    font-weight: 700;
    margin-bottom: 16px;
}
.section-header p {
    color: var(--gray-500);
    font-size: 18px;
}

/* 功能卡片 */
.features {
    padding: 80px 0;
    background: var(--gray-0);
}
.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 32px;
}
.feature-card {
    background: var(--gray-0);
    padding: 32px;
    border-radius: 32px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    border: 1px solid var(--gray-100);
    transition: all 0.3s;
}
.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 30px -12px rgba(0,0,0,0.08);
}
.feature-icon {
    width: 64px;
    height: 64px;
    border-radius: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 24px;
    color: var(--gray-0);
}
.feature-icon i {
    font-size: 36px;
}
.feature-card h3 {
    font-size: 20px;
    margin-bottom: 12px;
    color: var(--gray-800);
}
.feature-card p {
    color: var(--gray-500);
    line-height: 1.5;
}

/* 工作流 */
.workflow {
    padding: 80px 0;
}
.workflow-steps {
    display: flex;
    justify-content: space-between;
    gap: 40px;
    margin-bottom: 60px;
}
.step {
    flex: 1;
    text-align: center;
}
.step-number {
    width: 44px;
    height: 44px;
    background: var(--green-deep-50);
    color: var(--green-deep-600);
    border-radius: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 18px;
    margin: 0 auto 20px;
}
.step-icon i {
    font-size: 56px;
    color: var(--green-deep-500);
    margin-bottom: 20px;
}
.step h4 { font-size: 20px; margin-bottom: 12px; }
.step p { color: var(--gray-500); line-height: 1.5; }

/* Git 横幅 */
.git-banner {
    background: var(--green-deep-900);
    padding: 80px 5%;
    margin: 40px 0;
}
.git-content {
    max-width: 1280px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: 60px;
}
.git-text { flex: 1; color: var(--gray-0); }
.git-badge {
    background: rgba(67, 143, 113, 0.2);
    display: inline-block;
    padding: 6px 16px;
    border-radius: 40px;
    font-size: 13px;
    margin-bottom: 20px;
    color: var(--green-deep-200);
}
.git-text h2 { font-size: 40px; margin-bottom: 20px; }
.gradient-text-light {
    background: linear-gradient(135deg, var(--green-deep-200), var(--green-deep-400));
    background-clip: text;
    -webkit-background-clip: text;
    color: transparent;
}
.git-text p { color: var(--gray-400); line-height: 1.6; margin-bottom: 32px; font-size: 16px; }
.git-features { display: flex; gap: 32px; flex-wrap: wrap; }
.git-features span { display: flex; align-items: center; gap: 10px; font-size: 15px; color: var(--gray-300); }
.git-features i { font-size: 20px; color: var(--green-deep-300); }
.git-visual { flex: 1; height: 200px; position: relative; }

/* 模板区域 */
.templates {
    padding: 80px 0;
    background: var(--gray-0);
}
.templates-grid {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
    margin-bottom: 48px;
}
.template-category {
    background: var(--gray-50);
    padding: 12px 28px;
    border-radius: 60px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 500;
    color: var(--gray-700);
    font-size: 15px;
}
.template-category i {
    font-size: 20px;
    color: var(--green-deep-500);
}
.template-showcase {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 28px;
}
.showcase-item {
    text-align: center;
    width: 120px;
}
.showcase-preview {
    width: 100%;
    height: 80px;
    background: var(--gray-100);
    border-radius: 18px;
    margin-bottom: 10px;
    transition: all 0.2s;
}
.showcase-item:hover .showcase-preview {
    background: var(--green-deep-100);
}
.showcase-item span {
    font-size: 14px;
    color: var(--gray-600);
}

/* CTA */
.cta {
    padding: 60px 24px;
}
.cta-card {
    max-width: 800px;
    margin: 0 auto;
    background: linear-gradient(135deg, var(--green-deep-500), var(--green-deep-700));
    border-radius: 48px;
    padding: 60px 40px;
    text-align: center;
    color: var(--gray-0);
}
.cta-card h3 { font-size: 32px; margin-bottom: 16px; }
.cta-card p { font-size: 16px; opacity: 0.9; }
.cta-buttons { margin-top: 32px; display: flex; gap: 16px; justify-content: center; }
.btn-cta-primary, .btn-cta-outline {
    padding: 12px 28px;
    border-radius: 40px;
    font-weight: 600;
    cursor: pointer;
    font-size: 14px;
}
.btn-cta-primary { background: var(--gray-0); color: var(--green-deep-600); border: none; }
.btn-cta-outline { background: transparent; border: 1px solid white; color: var(--gray-0); }

/* 页脚 */
.footer {
    background: var(--gray-900);
    color: var(--gray-400);
    padding: 48px 5% 24px;
}
.footer-content {
    max-width: 1280px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 40px;
}
.footer-brand .footer-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 12px;
    color: var(--gray-0);
}
.footer-logo-icon {
    height: 40px;
    width: auto;
    border-radius: 10px;
}
.footer-brand p { font-size: 14px; }
.footer-links { display: flex; gap: 60px; }
.link-group h4 { color: var(--gray-0); margin-bottom: 16px; font-size: 14px; }
.link-group a { display: block; color: var(--gray-400); text-decoration: none; margin-bottom: 10px; font-size: 13px; transition: color 0.2s; }
.link-group a:hover { color: var(--green-deep-300); }
.footer-bottom { text-align: center; padding-top: 40px; font-size: 12px; border-top: 1px solid var(--gray-800); margin-top: 20px; }

/* Toast 提示 */
.global-toast {
    position: fixed;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(30, 41, 59, 0.95);
    color: var(--gray-0);
    padding: 14px 28px;
    border-radius: 50px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 14px;
    font-weight: 500;
    z-index: 1000;
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.2);
    backdrop-filter: blur(8px);
}
.global-toast i {
    font-size: 20px;
}
.toast-fade-enter-active,
.toast-fade-leave-active {
    transition: all 0.3s ease;
}
.toast-fade-enter-from,
.toast-fade-leave-to {
    opacity: 0;
    transform: translateX(-50%) translateY(20px);
}

/* 动画 */
@keyframes pulse {
    0% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.2); }
    100% { opacity: 1; transform: scale(1); }
}
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-15px); }
    100% { transform: translateY(0px); }
}

/* ========== 响应式样式 ========== */

/* 超大屏幕 (1440px+) */
@media (min-width: 1440px) {
    .container {
        max-width: 1400px;
    }
    .hero-title {
        font-size: 64px;
    }
    .hero-desc {
        font-size: 18px;
    }
}

/* 大屏幕 (1200px - 1439px) */
@media (max-width: 1439px) {
    .hero-title {
        font-size: 52px;
    }
    .floating-card {
        padding: 12px 20px;
        font-size: 14px;
    }
    .floating-card i {
        font-size: 24px;
    }
}

/* 中等屏幕 (992px - 1199px) */
@media (max-width: 1199px) {
    .hero {
        padding: 100px 4% 60px;
    }
    .hero-title {
        font-size: 44px;
    }
    .hero-desc {
        font-size: 16px;
    }
    .hero-desc br {
        display: none;
    }
    .section-header h2 {
        font-size: 36px;
    }
    .features-grid {
        gap: 24px;
    }
    .feature-card {
        padding: 24px;
    }
    .git-text h2 {
        font-size: 36px;
    }
    .demo-window {
        width: 260px;
    }
}

/* 平板横屏 (768px - 991px) */
@media (max-width: 991px) {
    .version {
        display: none;
    }
    .nav-links {
        gap: 24px;
    }
    .hero {
        flex-direction: column;
        text-align: center;
        padding: 100px 5% 60px;
    }
    .hero-content {
        max-width: 100%;
        margin-bottom: 60px;
    }
    .hero-buttons {
        justify-content: center;
    }
    .hero-visual {
        width: 100%;
        min-height: 350px;
    }
    .floating-card {
        position: relative;
        display: inline-flex;
        margin: 0 8px;
        animation: none;
        transform: none;
    }
    .card-1, .card-2, .card-3 {
        position: relative;
        top: auto;
        left: auto;
        right: auto;
        bottom: auto;
        display: inline-flex;
    }
    .hero-visual {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 16px;
        align-items: center;
    }
    .demo-window {
        position: relative;
        bottom: auto;
        right: auto;
        margin-top: 30px;
        width: 280px;
    }
    .workflow-steps {
        gap: 30px;
    }
    .step-icon i {
        font-size: 48px;
    }
    .git-content {
        flex-direction: column;
        text-align: center;
        gap: 40px;
    }
    .git-features {
        justify-content: center;
    }
    .git-visual {
        width: 100%;
        max-width: 300px;
        margin: 0 auto;
    }
    .templates-grid {
        gap: 12px;
    }
    .template-category {
        padding: 8px 20px;
        font-size: 13px;
    }
    .footer-content {
        flex-wrap: wrap;
        justify-content: center;
        text-align: center;
        gap: 32px;
    }
    .footer-brand {
        text-align: center;
    }
    .footer-logo {
        justify-content: center;
    }
    .footer-links {
        gap: 40px;
        justify-content: center;
    }
}

/* 平板竖屏/大手机 (576px - 767px) */
@media (max-width: 767px) {
    .navbar {
        padding: 12px 0;
    }
    .nav-links {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: var(--gray-0);
        flex-direction: column;
        gap: 0;
        padding: 16px 24px;
        box-shadow: 0 20px 25px -12px rgba(0,0,0,0.1);
        border-radius: 0 0 20px 20px;
    }
    .nav-links.active {
        display: flex;
    }
    .nav-links a {
        padding: 12px 0;
        border-bottom: 1px solid var(--gray-100);
    }
    .nav-links a:last-child {
        border-bottom: none;
    }
    .mobile-toggle {
        display: block;
    }
    .user-info {
        display: none;
    }
    .notice-icon {
        width: 40px;
        height: 40px;
        font-size: 20px;
    }
    .avatar {
        width: 40px;
        height: 40px;
    }
    .hero-title {
        font-size: 36px;
    }
    .hero-title br {
        display: none;
    }
    .hero-badge {
        font-size: 12px;
    }
    .hero-buttons {
        gap: 12px;
    }
    .btn-hero-primary, .btn-hero-secondary {
        padding: 10px 20px;
        font-size: 14px;
    }
    .section-header {
        margin-bottom: 40px;
    }
    .section-header h2 {
        font-size: 28px;
    }
    .section-header p {
        font-size: 14px;
    }
    .features {
        padding: 50px 0;
    }
    .features-grid {
        grid-template-columns: 1fr;
        gap: 20px;
    }
    .feature-card {
        padding: 20px;
    }
    .feature-icon {
        width: 52px;
        height: 52px;
    }
    .feature-icon i {
        font-size: 28px;
    }
    .feature-card h3 {
        font-size: 18px;
    }
    .workflow {
        padding: 50px 0;
    }
    .workflow-steps {
        flex-direction: column;
        gap: 32px;
    }
    .step {
        max-width: 280px;
        margin: 0 auto;
    }
    .step-icon i {
        font-size: 44px;
    }
    .git-banner {
        padding: 50px 5%;
        margin: 20px 0;
    }
    .git-text h2 {
        font-size: 28px;
    }
    .git-text p {
        font-size: 14px;
    }
    .git-features {
        gap: 16px;
    }
    .git-features span {
        font-size: 13px;
    }
    .templates {
        padding: 50px 0;
    }
    .template-category {
        padding: 6px 16px;
        font-size: 12px;
    }
    .template-category i {
        font-size: 16px;
    }
    .template-showcase {
        gap: 16px;
    }
    .showcase-item {
        width: 100px;
    }
    .showcase-preview {
        height: 70px;
    }
    .showcase-item span {
        font-size: 12px;
    }
    .cta-card {
        padding: 40px 24px;
        border-radius: 32px;
    }
    .cta-card h3 {
        font-size: 24px;
    }
    .cta-card p {
        font-size: 14px;
    }
    .cta-buttons {
        flex-direction: column;
        align-items: center;
        gap: 12px;
    }
    .btn-cta-primary, .btn-cta-outline {
        width: 200px;
    }
    .footer {
        padding: 40px 5% 20px;
    }
    .footer-links {
        flex-direction: column;
        gap: 24px;
        text-align: center;
    }
    .global-toast {
        padding: 10px 20px;
        font-size: 12px;
        bottom: 20px;
    }
    .global-toast i {
        font-size: 16px;
    }
}

/* 手机小屏 (480px以下) */
@media (max-width: 480px) {
    .logo-text {
        display: none;
    }
    .logo-icon-img {
        height: 40px;
    }
    .nav-container {
        padding: 0 16px;
    }
    .btn-login, .btn-register {
        padding: 6px 14px;
        font-size: 12px;
    }
    .hero {
        padding: 90px 16px 50px;
    }
    .hero-title {
        font-size: 28px;
    }
    .hero-desc {
        font-size: 14px;
    }
    .hero-buttons {
        flex-direction: column;
        align-items: center;
    }
    .btn-hero-primary, .btn-hero-secondary {
        width: 200px;
    }
    .floating-card {
        padding: 8px 14px;
        font-size: 12px;
    }
    .floating-card i {
        font-size: 18px;
    }
    .demo-window {
        width: 240px;
    }
    .demo-bar {
        padding: 10px 12px;
        font-size: 12px;
    }
    .demo-content {
        padding: 14px;
    }
    .demo-block {
        height: 55px;
    }
    .section-header h2 {
        font-size: 24px;
    }
    .feature-card {
        padding: 16px;
    }
    .feature-icon {
        width: 48px;
        height: 48px;
    }
    .feature-icon i {
        font-size: 24px;
    }
    .feature-card h3 {
        font-size: 16px;
    }
    .feature-card p {
        font-size: 13px;
    }
    .step-icon i {
        font-size: 38px;
    }
    .step h4 {
        font-size: 18px;
    }
    .step p {
        font-size: 13px;
    }
    .git-text h2 {
        font-size: 24px;
    }
    .git-badge {
        font-size: 11px;
    }
    .template-showcase {
        gap: 12px;
    }
    .showcase-item {
        width: 85px;
    }
    .showcase-preview {
        height: 60px;
    }
    .footer-brand .footer-logo {
        justify-content: center;
    }
    .footer-logo-icon {
        height: 32px;
    }
    .footer-bottom {
        font-size: 10px;
    }
}
</style>
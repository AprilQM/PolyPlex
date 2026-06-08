import { createRouter, createWebHistory } from 'vue-router'

const WorkbenchLayout = () => import("@/layouts/WorkbenchLayout.vue")
const AdminLayout = () => import("@/layouts/AdminLayout.vue")

const FormLayout = () => import("@/layouts/FormLayout.vue")

const Home = () => import("@/views/Home.vue")

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/home',
      component: Home
    },
    {
      path: '/workbench',
      meta: { requiresAuth: true },
      component: WorkbenchLayout,
      children:[
        {
          path: '/workbench',
          redirect: '/workbench/dashboard'
        },
        {
          path: 'dashboard',
          component: () => import("@/views/workbench/Dashboard.vue")
        },
        {
          path: 'square',
          component: () => import("@/views/workbench/Square.vue")
        },
        {
          path: 'project-manage',
          component: () => import("@/views/workbench/ProjectManage.vue")
        },
        {
          path: 'assist',
          component: () => import("@/views/workbench/Assist.vue")
        },
        {
          path: 'user-space',
          redirect: '/user-space/:id'
        },
        {
          path: 'user-space/:id',
          props: true,
          component: () => import("@/views/workbench/UserSpace.vue")
        },
        {
          path: 'notice',
          component: () => import("@/views/workbench/Notice.vue")
        }
      ]
    },
    {
      path: '/admin',
      component: AdminLayout,
      meta: { requiresAuth: true, requiresAdmin: true },
      children:[
        {
          path: '/admin',
          redirect: '/admin/dashboard'
        },
        {
          path: 'dashboard',
          component: () => import("@/views/admin/AdminDashboard.vue")
        },
        {
          path: 'pending-users',
          component: () => import("@/views/admin/PendingUsers.vue")
        },
        {
          path: 'users',
          component: () => import("@/views/admin/Users.vue")
        }
      ]
    },
    {
      path: '/form',
      component: FormLayout,
      children:[
        {
          path: 'login',
          component: () => import("@/views/form/Login.vue")
        },
        {
          path: 'register',
          component: () => import("@/views/form/Register.vue")
        },
        {
          path: 'verify',
          component: () => import("@/views/form/VerifyEmail.vue")
        },
        {
          path: 'pending-approval',
          component: () => import("@/views/form/PendingApproval.vue")
        },
        {
          path: 'rejected',
          component: () => import("@/views/form/Rejected.vue")
        },
        {
          path: 'banned',
          component: () => import("@/views/form/Banned.vue")
        }
      ]
    }
  ],
})

router.beforeEach(async (to, from, next) => {
  const { useUserStore } = await import('@/stores/useUserStore')
  const userStore = useUserStore()

  // 未登录 → 登录页
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!userStore.token) {
      next('/form/login')
      return
    }
  }

  // 管理员页面 → 验证管理员身份
  if (to.matched.some(record => record.meta.requiresAdmin)) {
    try {
      const res = await fetch('/api/admin/stats', {
        headers: { 'Authorization': `Bearer ${userStore.token}` },
      })
      if (res.status === 403) {
        next('/workbench/dashboard')
        return
      }
    } catch {
      next('/workbench/dashboard')
      return
    }
  }

  // 已登录 → 检查用户状态（pending / rejected / banned / approved）
  if (
    userStore.token &&
    !to.path.startsWith('/form/')
  ) {
    try {
      const res = await fetch('/api/auth/user-status', {
        headers: { 'Authorization': `Bearer ${userStore.token}` },
      })
      if (res.ok) {
        const data = await res.json()
        switch (data.status) {
          case 'pending':
            if (to.path !== '/form/pending-approval') {
              next('/form/pending-approval')
              return
            }
            break
          case 'rejected':
            if (to.path !== '/form/rejected') {
              next('/form/rejected')
              return
            }
            break
          case 'banned':
            if (to.path !== '/form/banned') {
              next('/form/banned')
              return
            }
            break
        }
      }
    } catch {
      // 网络错误时放行
    }
  }

  next()
})

export default router;

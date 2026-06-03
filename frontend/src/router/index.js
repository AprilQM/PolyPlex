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
      children:[]
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
        }
      ]
    }
  ],
})

router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const { useUserStore } = await import('@/stores/useUserStore')
    const userStore = useUserStore()
    if (!userStore.token) {
      next('/form/login')
      return
    }
  }
  next()
})

export default router;

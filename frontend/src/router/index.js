import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue')
  },
  {
    path: '/products',
    name: 'Products',
    component: () => import('@/views/ProductsView.vue')
  },
  {
    path: '/products/:id',
    name: 'ProductDetail',
    component: () => import('@/views/ProductDetailView.vue')
  },
  {
    path: '/admin',
    name: 'AdminLogin',
    component: () => import('@/views/admin/LoginView.vue')
  },
  {
    path: '/admin/products',
    name: 'AdminProducts',
    component: () => import('@/views/admin/AdminProductsView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/categories',
    name: 'AdminCategories',
    component: () => import('@/views/admin/AdminCategoriesView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/banners',
    name: 'AdminBanners',
    component: () => import('@/views/admin/AdminBannersView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/new-products',
    name: 'AdminNewProducts',
    component: () => import('@/views/admin/AdminNewProductsView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/settings',
    name: 'AdminSettings',
    component: () => import('@/views/admin/AdminSettingsView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/videos',
    name: 'AdminVideos',
    component: () => import('@/views/admin/AdminVideosView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/media',
    name: 'AdminMedia',
    component: () => import('@/views/admin/AdminMediaView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guard
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const isLoggedIn = localStorage.getItem('admin_token')
    if (!isLoggedIn) {
      next({ name: 'AdminLogin' })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router

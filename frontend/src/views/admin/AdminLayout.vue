<template>
  <div class="min-h-screen bg-background">
    <!-- Admin Header -->
    <header class="bg-primary text-white">
      <div class="px-6 h-16 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <button @click="toggleSidebar" class="md:hidden p-2 hover:bg-white/10 rounded">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
            </svg>
          </button>
          <router-link to="/" class="flex items-center gap-2">
            <!-- 如果有 logo 图片 -->
            <img
              v-if="settings.logo_url"
              :src="settings.logo_url"
              alt="Logo"
              class="w-8 h-8 object-contain"
            />
            <!-- 否则显示 SVG -->
            <div v-else class="w-8 h-8" v-html="settings.logo_svg || defaultLogoSvg"></div>
            <span class="font-serif text-xl">{{ settings.site_name || 'Daidy' }}</span>
          </router-link>
        </div>

        <div class="flex items-center gap-4">
          <router-link to="/" target="_blank" class="text-sm hover:bg-white/10 px-3 py-1.5 rounded flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
            </svg>
            查看网站
          </router-link>
          <button @click="handleLogout" class="text-sm hover:bg-white/10 px-3 py-1.5 rounded flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
            退出
          </button>
        </div>
      </div>
    </header>

    <div class="flex">
      <!-- Sidebar -->
      <aside
        :class="[
          'fixed md:static inset-y-0 left-0 z-40 w-64 bg-surface border-r border-border transform transition-transform duration-300 md:translate-x-0 pt-16 md:pt-0',
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        ]"
      >
        <nav class="p-4 space-y-1">
          <router-link
            to="/admin/products"
            class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-secondary/50 transition-colors"
            :class="$route.path === '/admin/products' ? 'bg-primary/10 text-primary' : 'text-text-secondary'"
            @click="closeSidebar"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
            </svg>
            产品管理
          </router-link>
          <router-link
            to="/admin/categories"
            class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-secondary/50 transition-colors"
            :class="$route.path === '/admin/categories' ? 'bg-primary/10 text-primary' : 'text-text-secondary'"
            @click="closeSidebar"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
            </svg>
            分类管理
          </router-link>
          <router-link
            to="/admin/banners"
            class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-secondary/50 transition-colors"
            :class="$route.path === '/admin/banners' ? 'bg-primary/10 text-primary' : 'text-text-secondary'"
            @click="closeSidebar"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
            </svg>
            Banner管理
          </router-link>
          <router-link
            to="/admin/new-products"
            class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-secondary/50 transition-colors"
            :class="$route.path === '/admin/new-products' ? 'bg-primary/10 text-primary' : 'text-text-secondary'"
            @click="closeSidebar"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            新品管理
          </router-link>
          <router-link
            to="/admin/videos"
            class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-secondary/50 transition-colors"
            :class="$route.path === '/admin/videos' ? 'bg-primary/10 text-primary' : 'text-text-secondary'"
            @click="closeSidebar"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
            </svg>
            视频管理
          </router-link>
          <router-link
            to="/admin/media"
            class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-secondary/50 transition-colors"
            :class="$route.path === '/admin/media' ? 'bg-primary/10 text-primary' : 'text-text-secondary'"
            @click="closeSidebar"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
            </svg>
            媒体库
          </router-link>
          <router-link
            to="/admin/settings"
            class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-secondary/50 transition-colors"
            :class="$route.path === '/admin/settings' ? 'bg-primary/10 text-primary' : 'text-text-secondary'"
            @click="closeSidebar"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
            系统设置
          </router-link>
        </nav>
      </aside>

      <!-- Overlay -->
      <div
        v-if="isSidebarOpen"
        @click="closeSidebar"
        class="fixed inset-0 bg-black/50 z-30 md:hidden"
      />

      <!-- Main Content -->
      <main class="flex-1 p-6 md:p-8 pt-20 md:pt-8">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const isSidebarOpen = ref(false)

const settings = ref({
  site_name: 'Daidy',
  logo_url: '',
  logo_svg: ''
})

const defaultLogoSvg = '<svg viewBox="0 0 32 32" fill="none"><circle cx="16" cy="16" r="14" stroke="currentColor" stroke-width="2"/><path d="M16 8 C12 12, 10 16, 16 24 C22 16, 20 12, 16 8" fill="currentColor"/></svg>'

async function fetchSettings() {
  try {
    const res = await axios.get('/api/settings')
    const data = res.data?.data || {}
    settings.value = {
      site_name: data.site_name || 'Daidy',
      logo_url: data.logo_url || '',
      logo_svg: data.logo_svg || defaultLogoSvg
    }
  } catch (e) {
    console.error('Failed to fetch settings:', e)
  }
}

function toggleSidebar() {
  isSidebarOpen.value = !isSidebarOpen.value
}

function closeSidebar() {
  isSidebarOpen.value = false
}

function handleLogout() {
  localStorage.removeItem('admin_token')
  router.push('/admin')
}

onMounted(() => {
  fetchSettings()
})
</script>

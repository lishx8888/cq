<template>
  <header
    :class="[
      'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
      isScrolled ? 'nav-scrolled' : 'bg-transparent'
    ]"
  >
    <nav class="container-custom h-[72px] flex items-center justify-between">
      <!-- Logo -->
      <router-link to="/" class="flex items-center gap-2 group">
        <!-- 如果有 logo 图片 -->
        <img
          v-if="settings.logo_url"
          :src="settings.logo_url"
          alt="Logo"
          class="w-8 h-8 object-contain"
        />
        <!-- 否则显示 SVG -->
        <div v-else class="w-8 h-8 relative" v-html="settings.logo_svg || defaultLogoSvg"></div>
        <span class="font-serif text-2xl font-medium tracking-wide text-primary">
          {{ settings.site_name || 'Daidy' }}
        </span>
      </router-link>

      <!-- Desktop Navigation -->
      <div class="hidden md:flex items-center gap-8">
        <router-link to="/" class="nav-link">首页</router-link>

        <!-- 产品列表 - 带分类下拉 -->
        <div
          class="relative"
          @mouseenter="showDropdown = true"
          @mouseleave="showDropdown = false"
        >
          <router-link to="/products" class="nav-link flex items-center gap-1">
            产品列表
            <svg class="w-3.5 h-3.5 transition-transform duration-200" :class="showDropdown ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </router-link>

          <!-- 下拉菜单 -->
          <transition name="dropdown">
            <div
              v-if="showDropdown && categories.length > 0"
              class="absolute top-full left-1/2 -translate-x-1/2 mt-2 w-44 bg-white rounded-xl shadow-lg border border-border overflow-hidden"
            >
              <!-- 全部产品 -->
              <router-link
                to="/products"
                class="dropdown-item"
                @click="showDropdown = false"
              >
                全部产品
              </router-link>
              <div class="h-px bg-border mx-3"></div>
              <!-- 分类列表 -->
              <router-link
                v-for="cat in categories"
                :key="cat.id"
                :to="`/products?category=${cat.id}`"
                class="dropdown-item"
                @click="showDropdown = false"
              >
                {{ cat.name }}
              </router-link>
            </div>
          </transition>
        </div>
      </div>

      <!-- Mobile Menu Button -->
      <button
        @click="toggleMobileMenu"
        class="md:hidden p-2 text-primary"
        aria-label="菜单"
      >
        <svg v-if="!isMobileMenuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
        </svg>
        <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
    </nav>

    <!-- Mobile Menu -->
    <transition name="slide">
      <div
        v-if="isMobileMenuOpen"
        class="md:hidden bg-white border-t border-border"
      >
        <div class="container-custom py-4 flex flex-col gap-4">
          <router-link
            to="/"
            class="py-2 text-lg text-primary hover:text-primary-light transition-colors"
            @click="closeMobileMenu"
          >
            首页
          </router-link>
          <div>
            <router-link
              to="/products"
              class="py-2 text-lg text-primary hover:text-primary-light transition-colors block"
              @click="closeMobileMenu"
            >
              产品列表
            </router-link>
            <!-- 移动端分类 -->
            <div class="pl-4 mt-1 flex flex-col gap-2" v-if="categories.length > 0">
              <router-link
                v-for="cat in categories"
                :key="cat.id"
                :to="`/products?category=${cat.id}`"
                class="py-1 text-base text-primary/70 hover:text-primary transition-colors"
                @click="closeMobileMenu"
              >
                — {{ cat.name }}
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

const isScrolled = ref(false)
const isMobileMenuOpen = ref(false)
const showDropdown = ref(false)
const categories = ref([])

const settings = ref({
  site_name: 'Daidy',
  logo_url: '',
  logo_svg: ''
})

const defaultLogoSvg = '<svg viewBox="0 0 32 32" fill="none"><circle cx="16" cy="16" r="14" stroke="#2D5A47" stroke-width="2"/><path d="M16 8 C12 12, 10 16, 16 24 C22 16, 20 12, 16 8" fill="#2D5A47"/></svg>'

async function fetchCategories() {
  try {
    const res = await axios.get('/api/categories')
    categories.value = res.data?.data || []
  } catch (e) {
    categories.value = []
  }
}

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

function handleScroll() {
  isScrolled.value = window.scrollY > 50
}

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

function closeMobileMenu() {
  isMobileMenuOpen.value = false
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  fetchCategories()
  fetchSettings()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.nav-scrolled {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--color-border);
}

.nav-link {
  @apply relative text-primary font-medium py-2;
}

.nav-link::after {
  content: '';
  @apply absolute bottom-0 left-1/2 w-0 h-0.5 bg-primary transition-all duration-300;
}

.nav-link:hover::after,
.nav-link.router-link-active::after {
  @apply w-full -translate-x-1/2;
}

.dropdown-item {
  @apply block px-4 py-2.5 text-sm text-primary hover:bg-green-50 hover:text-primary-light transition-colors cursor-pointer;
}

/* 下拉动画 */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}
.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-6px);
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>

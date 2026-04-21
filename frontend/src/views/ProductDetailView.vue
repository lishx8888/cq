<template>
  <div class="min-h-screen">
    <NavBar />

    <!-- Loading State -->
    <section v-if="productStore.loading" class="pt-32 pb-20">
      <div class="container-custom">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div class="aspect-square skeleton rounded-lg" />
          <div class="space-y-4">
            <div class="h-10 w-2/3 skeleton rounded" />
            <div class="h-6 w-1/3 skeleton rounded" />
            <div class="h-24 skeleton rounded mt-8" />
          </div>
        </div>
      </div>
    </section>

    <!-- Product Detail -->
    <section v-else-if="product" class="pt-32 pb-20">
      <div class="container-custom">
        <!-- Breadcrumb -->
        <nav class="flex items-center gap-2 text-sm text-text-secondary mb-8">
          <router-link to="/" class="hover:text-primary transition-colors">首页</router-link>
          <span>/</span>
          <router-link to="/products" class="hover:text-primary transition-colors">产品列表</router-link>
          <span>/</span>
          <span class="text-text-primary">{{ product.name }}</span>
        </nav>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <!-- Product Images -->
          <div>
            <div class="aspect-square bg-secondary/30 rounded-xl overflow-hidden mb-4">
              <img
                v-if="activeImage"
                :src="activeImage"
                :alt="product.name"
                class="w-full h-full object-cover"
              />
              <div v-else class="w-full h-full flex items-center justify-center">
                <svg class="w-24 h-24 text-border" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
              </div>
            </div>

            <!-- Thumbnail Gallery -->
            <div v-if="galleryList.length > 0" class="grid grid-cols-4 gap-3">
              <button
                v-for="(img, index) in galleryList"
                :key="index"
                @click="activeImage = img"
                :class="[
                  'aspect-square rounded-lg overflow-hidden transition-all',
                  activeImage === img
                    ? 'border-2 border-primary'
                    : 'border-2 border-transparent hover:border-primary/50'
                ]"
              >
                <img :src="img" :alt="`${product.name} - ${index + 1}`" class="w-full h-full object-cover" />
              </button>
            </div>
          </div>

          <!-- Product Info -->
          <div>
            <!-- Category Badge -->
            <span
              v-if="categoryName"
              class="inline-block px-4 py-1.5 bg-primary/10 text-primary text-sm font-medium rounded-full mb-4"
            >
              {{ categoryName }}
            </span>

            <h1 class="font-serif text-3xl lg:text-4xl mb-4">{{ product.name }}</h1>

            <!-- Specs -->
            <div v-if="product.specs" class="flex items-center gap-4 text-text-secondary mb-6">
              <span class="flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
                </svg>
                规格: {{ product.specs }}
              </span>
            </div>

            <!-- Short Description -->
            <p v-if="product.description" class="text-text-secondary text-lg mb-8">
              {{ product.description }}
            </p>

            <!-- Benefits -->
            <div v-if="benefitsList.length > 0" class="mb-8">
              <h2 class="font-medium text-xl mb-4 flex items-center gap-2">
                <svg class="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                核心功效
              </h2>
              <ul class="space-y-3">
                <li
                  v-for="(benefit, index) in benefitsList"
                  :key="index"
                  class="flex items-center gap-3"
                >
                  <span class="w-2 h-2 rounded-full bg-primary flex-shrink-0" />
                  <span>{{ benefit }}</span>
                </li>
              </ul>
            </div>

            <!-- Ingredients -->
            <div v-if="product.ingredients" class="mb-8 p-6 bg-secondary/30 rounded-xl">
              <h2 class="font-medium text-xl mb-3">主要成分</h2>
              <p class="text-text-secondary">{{ product.ingredients }}</p>
            </div>

            <!-- CTA -->
            <div class="flex flex-col sm:flex-row gap-4">
              <button
                v-if="isConsultEnabled()"
                @click="openConsult"
                class="flex-1 btn btn-primary flex items-center justify-center gap-2"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
                </svg>
                立即咨询
              </button>
              <router-link
                to="/products"
                class="flex-1 btn btn-secondary flex items-center justify-center gap-2"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
                </svg>
                返回列表
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Detail Images - 16:9, max 1660px, percentage width -->
      <div v-if="detailImages.length > 0" class="mt-12 flex flex-col gap-4 px-5 md:px-10">
        <div
          v-for="(img, idx) in detailImages"
          :key="idx"
          class="w-full mx-auto"
          style="max-width: 1660px; aspect-ratio: 16/9;"
        >
          <img
            :src="img"
            :alt="`${product.name} 详情图${idx + 1}`"
            class="w-full h-full object-cover rounded-lg"
          />
        </div>
      </div>
    </section>

    <!-- Not Found -->
    <section v-else class="pt-32 pb-20">
      <div class="container-custom text-center py-20">
        <svg class="w-20 h-20 mx-auto text-border mb-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <h3 class="text-xl font-medium mb-2">产品未找到</h3>
        <p class="text-text-secondary mb-6">抱歉，您访问的产品不存在</p>
        <router-link to="/products" class="btn btn-primary">
          返回产品列表
        </router-link>
      </div>
    </section>

    <!-- Floating Consultation Bar -->
    <transition name="slide-up">
      <div
        v-if="showFloatingBar && product && isConsultEnabled()"
        class="fixed bottom-0 left-0 right-0 bg-white border-t border-border p-4 shadow-lg z-50 md:hidden"
      >
        <button @click="openConsult" class="w-full btn btn-primary">
          想了解更多？立即咨询
        </button>
      </div>
    </transition>

    <Footer />

    <!-- Floating Navigation Sidebar -->
    <div class="fixed right-4 top-1/2 -translate-y-1/2 flex flex-col gap-3 z-40">
      <router-link
        to="/"
        class="w-12 h-12 rounded-full bg-white shadow-lg hover:shadow-xl flex items-center justify-center text-text-secondary hover:text-primary transition-all group"
        title="首页"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
        </svg>
      </router-link>
      <router-link
        to="/products"
        class="w-12 h-12 rounded-full bg-white shadow-lg hover:shadow-xl flex items-center justify-center text-text-secondary hover:text-primary transition-all group"
        title="分类"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/>
        </svg>
      </router-link>
      <router-link
        to="/#contact"
        class="w-12 h-12 rounded-full bg-white shadow-lg hover:shadow-xl flex items-center justify-center text-text-secondary hover:text-primary transition-all group"
        title="联系我们"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
        </svg>
      </router-link>
    </div>

    <!-- Consult Modal -->
    <ConsultModal :is-open="isConsultOpen" @close="isConsultOpen = false" />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import Footer from '@/components/Footer.vue'
import ConsultModal from '@/components/ConsultModal.vue'
import { useProductStore } from '@/stores/product'
import { categoryApi } from '@/api'
import { useSettings } from '@/composables/useSettings'

const route = useRoute()
const productStore = useProductStore()
const { fetchSettings, isConsultEnabled } = useSettings()

const isConsultOpen = ref(false)
const showFloatingBar = ref(false)
const categories = ref([])
const activeImage = ref('')

const product = computed(() => productStore.currentProduct)

// Computed properties (must be defined before watch)
const categoryName = computed(() => {
  if (!product.value?.category_id) return ''
  const category = categories.value.find(c => c.id === product.value.category_id)
  return category?.name || ''
})

const benefitsList = computed(() => {
  if (!product.value?.benefits) return []
  return product.value.benefits.split('|').filter(Boolean)
})

const galleryList = computed(() => {
  const mainImg = product.value?.image_url
  const g = product.value?.gallery
  let extra = []
  if (g) {
    if (Array.isArray(g)) extra = g
    else if (typeof g === 'string') {
      try { extra = JSON.parse(g) } catch { extra = [] }
    }
  }
  // 去重去空，且主图不在画廊里时才插入
  const extras = extra.filter(img => img && img !== mainImg)
  if (mainImg) {
    return [mainImg, ...extras]
  }
  return extras
})

const detailImages = computed(() => {
  const d = product.value?.detail_images
  if (!d) return []
  if (Array.isArray(d)) return d.filter(Boolean)
  if (typeof d === 'string') {
    try { return JSON.parse(d).filter(Boolean) } catch { return [] }
  }
  return []
})

async function fetchCategories() {
  try {
    const res = await categoryApi.getList()
    categories.value = res.data || []
  } catch (err) {
    console.error('Failed to fetch categories:', err)
  }
}

// Watch product and init activeImage
watch(product, (p) => {
  if (p?.image_url) {
    activeImage.value = p.image_url
  } else if (galleryList.value.length > 0) {
    activeImage.value = galleryList.value[0]
  }
}, { immediate: true })

watch(galleryList, (list) => {
  if (list.length > 0 && !activeImage.value) {
    activeImage.value = list[0]
  }
})

function openConsult() {
  isConsultOpen.value = true
}

let scrollTimeout = null
function handleScroll() {
  if (scrollTimeout) return
  scrollTimeout = setTimeout(() => {
    showFloatingBar.value = window.scrollY > 500
    scrollTimeout = null
  }, 50)
}

onMounted(async () => {
  await Promise.all([
    productStore.fetchProduct(route.params.id),
    fetchCategories(),
    fetchSettings()
  ])
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>

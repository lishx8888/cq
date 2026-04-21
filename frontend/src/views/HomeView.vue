<template>
  <div class="min-h-screen">
    <NavBar />
    
    <!-- Hero Banner Carousel -->
    <section class="relative h-[70vh] overflow-hidden">
      <div
        class="flex transition-transform duration-500 ease-out h-full"
        :style="{ transform: `translateX(-${currentSlide * 100}%)` }"
      >
        <div
          v-for="(banner, index) in banners"
          :key="index"
          class="w-full h-full flex-shrink-0 relative group"
        >
          <img
            :src="banner.image"
            :alt="banner.title"
            class="w-full h-full object-cover"
          />
          <div class="absolute inset-0 flex items-center justify-center">
            <div class="text-center text-white slide-up banner-text-container" style="width: 750px; max-width: 90%; height: 300px; background: rgba(0,0,0,0.15); border-radius: 16px; display: flex; flex-direction: column; align-items: center; justify-content: center; transition: background 0.3s ease;">
              <h1 class="font-serif text-4xl md:text-5xl lg:text-6xl mb-4">
                {{ banner.title }}
              </h1>
              <p class="text-lg md:text-xl opacity-90 mb-8">
                {{ banner.subtitle }}
              </p>
              <router-link
                to="/products"
                class="inline-block btn btn-primary"
              >
                探索产品
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Navigation Arrows -->
      <button
        @click="prevSlide"
        class="absolute left-4 top-1/2 -translate-y-1/2 w-12 h-12 rounded-full bg-white/20 backdrop-blur-sm hover:bg-white/40 transition-colors flex items-center justify-center text-white"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </button>
      <button
        @click="nextSlide"
        class="absolute right-4 top-1/2 -translate-y-1/2 w-12 h-12 rounded-full bg-white/20 backdrop-blur-sm hover:bg-white/40 transition-colors flex items-center justify-center text-white"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
        </svg>
      </button>

      <!-- Indicators -->
      <div class="absolute bottom-6 left-1/2 -translate-x-1/2 flex gap-2">
        <button
          v-for="(_, index) in banners"
          :key="index"
          @click="goToSlide(index)"
          :class="[
            'w-2 h-2 rounded-full transition-all duration-300',
            currentSlide === index ? 'bg-white w-8' : 'bg-white/50 hover:bg-white/70'
          ]"
        />
      </div>
    </section>

    <!-- Search Section -->
    <section class="py-12 bg-surface">
      <div class="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8">
        <div class="max-w-2xl mx-auto">
          <div class="relative group">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索产品..."
              @keyup.enter="handleSearch"
              class="w-full h-14 pl-14 pr-14 rounded-full border-2 border-primary/20 focus:border-primary focus:ring-4 focus:ring-primary/10 outline-none transition-all duration-300 text-base shadow-lg shadow-primary/5"
            />
            <div class="absolute left-5 top-1/2 -translate-y-1/2 text-primary/60 group-focus-within:text-primary transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
            </div>
            <button
              @click="handleSearch"
              class="absolute right-2 top-1/2 -translate-y-1/2 h-10 px-6 rounded-full bg-primary text-white font-medium hover:bg-primary/90 transition-colors flex items-center gap-2"
            >
              搜索
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Category Navigation -->
    <section class="section-spacing bg-surface">
      <div class="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="font-serif text-3xl text-center mb-12">产品分类</h2>
        
        <div class="flex flex-wrap justify-center gap-4">
          <router-link
            v-for="category in categories"
            :key="category.id"
            :to="`/products?category=${category.id}`"
            class="group flex flex-col items-center p-6 rounded-xl hover:bg-secondary/30 transition-colors"
          >
            <div class="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors">
              <span class="text-3xl">{{ category.icon }}</span>
            </div>
            <h3 class="font-medium text-center">{{ category.name }}</h3>
            <p class="text-sm text-text-secondary mt-1">{{ category.description }}</p>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Video Module -->
    <section class="section-spacing">
      <div class="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="font-serif text-3xl mb-4">产品视频</h2>
          <p class="text-text-secondary max-w-xl mx-auto">
            了解产品背后的故事与使用技巧
          </p>
        </div>

        <div v-if="homeVideos.length > 0" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          <div
            v-for="(video, index) in homeVideos"
            :key="video.id || index"
            class="relative rounded-xl overflow-hidden cursor-pointer group"
            style="aspect-ratio: 9/16;"
            @mouseenter="playVideo(index)"
            @mouseleave="pauseVideo(index)"
            @click="clickVideo(video, index)"
          >
            <!-- Poster Image (fallback: video first frame) -->
            <img
              v-show="!video.isPlaying"
              :src="video.posterUrl || video.cover_url || video.poster"
              :alt="video.title"
              class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
            />
            <!-- Video -->
            <video
              v-show="video.isPlaying"
              :ref="el => { if (el) { videoRefs[index] = el; el.addEventListener('loadeddata', () => captureVideoFrame(el, index)); } }"
              :src="video.video_url || video.url"
              class="w-full h-full object-cover"
              muted
              loop
              playsinline
              @loadeddata="captureVideoFrame($event.target, index)"
            />
            <!-- Overlay -->
            <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent" />
            <!-- Play Icon -->
            <div 
              v-show="!video.isPlaying"
              class="absolute inset-0 flex items-center justify-center"
            >
              <div class="w-14 h-14 rounded-full bg-white/30 backdrop-blur-sm flex items-center justify-center group-hover:bg-white/50 transition-colors">
                <svg class="w-6 h-6 text-white ml-1" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M8 5v14l11-7z"/>
                </svg>
              </div>
            </div>
            <!-- Title -->
            <div class="absolute bottom-0 left-0 right-0 p-4">
              <h3 class="text-white font-medium text-sm">{{ video.title }}</h3>
              <p v-if="video.description" class="text-white/70 text-xs mt-1 truncate">{{ video.description }}</p>
            </div>
            <!-- Product Link Indicator -->
            <div v-if="video.product_id" class="absolute top-2 right-2 px-2 py-1 bg-primary text-white text-xs rounded-full">
              查看产品
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-12 text-text-secondary">
          <svg class="w-16 h-16 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
          </svg>
          <p>暂无视频，请在后台添加</p>
        </div>
      </div>
    </section>

    <!-- New Arrivals -->
    <section class="section-spacing bg-surface">
      <div class="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between mb-12">
          <div class="text-center flex-1">
            <h2 class="font-serif text-3xl mb-4">新品上市</h2>
            <p class="text-text-secondary max-w-xl mx-auto">
              探索最新护肤科技，焕新肌肤活力
            </p>
          </div>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-4 gap-6">
          <ProductCard
            v-for="product in newProducts"
            :key="product.id"
            :product="product"
            :category-name="getCategoryName(product.category_id)"
            :show-consult="isConsultEnabled()"
            @click="goToProduct(product.id)"
            @consult="openConsult"
          />
        </div>

        <div class="text-center mt-12">
          <router-link to="/products" class="btn btn-secondary">
            查看全部产品
          </router-link>
        </div>
      </div>
    </section>

    <!-- Featured Products -->
    <section class="section-spacing">
      <div class="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="font-serif text-3xl mb-4">精选产品</h2>
          <p class="text-text-secondary max-w-xl mx-auto">
            严选天然成分，专注肌肤修护，为您带来纯净护肤体验
          </p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <ProductCard
            v-for="product in featuredProducts"
            :key="product.id"
            :product="product"
            :category-name="getCategoryName(product.category_id)"
            :show-consult="isConsultEnabled()"
            @click="goToProduct(product.id)"
            @consult="openConsult"
          />
        </div>

        <div class="text-center mt-12">
          <router-link to="/products" class="btn btn-secondary">
            查看全部产品
          </router-link>
        </div>
      </div>
    </section>

    <!-- Category Products Section -->
    <section class="section-spacing bg-surface">
      <div class="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="font-serif text-3xl mb-4">按分类浏览</h2>
          <p class="text-text-secondary max-w-xl mx-auto">
            发现每个品类中的明星产品
          </p>
        </div>

        <!-- Each Category: 1 row x 4 cols x 2 rows = 8 products -->
        <div v-for="cat in categories.slice(0, 6)" :key="cat.id" class="mb-12 last:mb-0">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-2xl font-serif flex items-center gap-2">
              <span class="text-2xl">{{ cat.icon }}</span>
              {{ cat.name }}
            </h3>
            <router-link 
              :to="`/products?category=${cat.id}`" 
              class="text-primary hover:underline text-sm font-medium"
            >
              查看全部 →
            </router-link>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <ProductCard
              v-for="product in getCategoryProducts(cat.id).slice(0, 8)"
              :key="product.id"
              :product="product"
              :category-name="cat.name"
              :show-consult="isConsultEnabled()"
              @click="goToProduct(product.id)"
              @consult="openConsult"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Brand Story -->
    <section class="section-spacing bg-primary text-white">
      <div class="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8">
        <div class="max-w-3xl mx-auto text-center">
          <span class="text-accent font-serif text-lg">Our Philosophy</span>
          <h2 class="font-serif text-4xl mt-4 mb-8">源自天然，专注肌肤本源</h2>
          <p class="text-white/80 text-lg leading-relaxed mb-8">
            Daidy 相信，真正的美丽源于肌肤的健康与平衡。我们从全球各地严选优质天然成分，
            结合先进科技与古老智慧，为您呈现纯净、高效的护肤产品。
            每一滴精华，都承载着对肌肤的尊重与呵护。
          </p>
          <div class="flex flex-wrap justify-center gap-8">
            <div class="text-center">
              <div class="font-serif text-4xl text-accent">98%</div>
              <div class="text-white/70 mt-1">天然成分</div>
            </div>
            <div class="text-center">
              <div class="font-serif text-4xl text-accent">0</div>
              <div class="text-white/70 mt-1">人工香精</div>
            </div>
            <div class="text-center">
              <div class="font-serif text-4xl text-accent">100%</div>
              <div class="text-white/70 mt-1">真诚承诺</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <Footer />

    <!-- Consult Modal -->
    <ConsultModal :is-open="isConsultOpen" @close="isConsultOpen = false" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import Footer from '@/components/Footer.vue'
import ProductCard from '@/components/ProductCard.vue'
import ConsultModal from '@/components/ConsultModal.vue'
import { useProductStore } from '@/stores/product'
import { categoryApi, bannerApi, productApi } from '@/api'
import { useSettings } from '@/composables/useSettings'

const router = useRouter()
const productStore = useProductStore()
const { fetchSettings, isConsultEnabled } = useSettings()

const searchQuery = ref('')
const currentSlide = ref(0)
const isConsultOpen = ref(false)
let autoplayTimer = null

const banners = ref([])
const categories = ref([])
const videoRefs = ref([])

// Videos from API
const homeVideos = ref([])
const videoPlayingState = ref({})

// Capture frame from video as poster (at 0.2s / ~5th frame)
function captureVideoFrame(video, index) {
  if (!video) return
  
  const videoItem = homeVideos.value[index]
  // Skip if already has a poster
  if (videoItem?.posterUrl) return
  
  try {
    // Seek to 0.2s (around 5th frame for 25fps video)
    video.currentTime = 0.2
    
    const onSeeked = () => {
      const canvas = document.createElement('canvas')
      canvas.width = video.videoWidth || 360
      canvas.height = video.videoHeight || 640
      const ctx = canvas.getContext('2d')
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
      const posterUrl = canvas.toDataURL('image/jpeg', 0.8)
      
      if (videoItem) {
        videoItem.posterUrl = posterUrl
      }
      video.removeEventListener('seeked', onSeeked)
    }
    
    video.addEventListener('seeked', onSeeked)
  } catch (e) {
    console.warn('Failed to capture video frame:', e)
  }
}

async function fetchVideos() {
  try {
    const res = await fetch('/api/videos')
    const data = await res.json()
    // Add isPlaying state to each video
    homeVideos.value = (data.data || []).map(v => ({
      ...v,
      isPlaying: false,
      posterUrl: v.cover_url || v.poster || null
    }))
  } catch (err) {
    console.error('Failed to fetch videos:', err)
  }
}

function playVideo(index) {
  const video = homeVideos.value[index]
  if (!video) return
  
  video.isPlaying = true
  videoPlayingState.value[index] = true
  nextTick(() => {
    const videoEl = videoRefs.value[index]
    if (videoEl) {
      videoEl.play().catch(() => {})
    }
  })
}

function pauseVideo(index) {
  const video = homeVideos.value[index]
  if (!video) return
  
  video.isPlaying = false
  videoPlayingState.value[index] = false
  nextTick(() => {
    const videoEl = videoRefs.value[index]
    if (videoEl) {
      videoEl.pause()
      videoEl.currentTime = 0
    }
  })
}

function clickVideo(video, index) {
  // Stop video first
  pauseVideo(index)
  
  // If video has linked product, go to product page
  if (video.product_id) {
    router.push(`/products/${video.product_id}`)
  }
}

async function fetchBanners() {
  try {
    const res = await bannerApi.getList()
    const data = res.data || []
    // Convert API format to component format
    banners.value = data.map(b => ({
      title: b.title || '',
      subtitle: b.subtitle || '',
      image: b.image || b.link || '',
      link: b.link || ''
    }))
  } catch (err) {
    console.error('Failed to fetch banners:', err)
    // Fallback banners if API fails
    banners.value = [{
      title: '纯净护肤，焕活肌肤',
      subtitle: '天然成分，科学配方，唤醒肌肤本真之美',
      image: 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=1920&q=80'
    }]
  }
}

async function fetchCategories() {
  try {
    const res = await categoryApi.getList()
    categories.value = res.data || []
  } catch (err) {
    console.error('Failed to fetch categories:', err)
  }
}

const featuredProducts = computed(() => productStore.products.slice(0, 8))

// Get products by category
function getCategoryProducts(categoryId) {
  return productStore.products.filter(p => p.category_id === categoryId)
}

// New arrivals - fetched from API (is_new = 1)
const newProducts = ref([])

async function fetchNewProducts() {
  try {
    const res = await productApi.getNew()
    newProducts.value = res.data || []
  } catch (err) {
    console.error('Failed to fetch new products:', err)
  }
}

function getCategoryName(categoryId) {
  const category = categories.value.find(c => c.id === categoryId)
  return category?.name || ''
}

function nextSlide() {
  currentSlide.value = (currentSlide.value + 1) % banners.value.length
}

function prevSlide() {
  currentSlide.value = (currentSlide.value - 1 + banners.value.length) % banners.value.length
}

function goToSlide(index) {
  currentSlide.value = index
}

function goToProduct(id) {
  router.push(`/products/${id}`)
}

function handleSearch() {
  if (searchQuery.value.trim()) {
    router.push(`/products?search=${encodeURIComponent(searchQuery.value.trim())}`)
  }
}

function openConsult() {
  isConsultOpen.value = true
}

function startAutoplay() {
  autoplayTimer = setInterval(() => {
    nextSlide()
  }, 5000)
}

function stopAutoplay() {
  if (autoplayTimer) {
    clearInterval(autoplayTimer)
  }
}

onMounted(async () => {
  await Promise.all([
    productStore.fetchProducts(),
    fetchCategories(),
    fetchBanners(),
    fetchNewProducts(),
    fetchVideos(),
    fetchSettings()
  ])
  startAutoplay()
})

onUnmounted(() => {
  stopAutoplay()
})
</script>

<style scoped>
.slide-up {
  animation: slideUp 0.6s ease-out forwards;
}

.group:hover .banner-text-container {
  background: transparent !important;
}
</style>

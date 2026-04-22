<template>
  <AdminLayout>
    <div>
      <!-- Header -->
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
        <div>
          <h1 class="text-2xl font-medium">产品视频管理</h1>
          <p class="text-text-secondary mt-1">管理首页视频展示（支持封面和排序）</p>
        </div>
        <button @click="openForm()" class="btn btn-primary flex items-center gap-2 self-start">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          新增视频
        </button>
      </div>

      <!-- Videos Grid -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
        <div
          v-for="(video, index) in videos"
          :key="video.id"
          class="bg-surface rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow"
        >
          <!-- Video Preview / Cover - 9:16 竖屏 -->
          <div class="relative bg-secondary/30 overflow-hidden w-full" style="aspect-ratio: 9/16;">
            <!-- Video Element -->
            <video
              v-if="video.video_url"
              :src="video.video_url"
              class="absolute inset-0 w-full h-full object-cover"
              muted
              preload="metadata"
              @mouseenter="$event.target.play()"
              @mouseleave="$event.target.pause(); $event.target.currentTime = 0"
            />
            <!-- Cover Image (fallback when no video) -->
            <img
              v-if="video.cover_url && !video.video_url"
              :src="video.cover_url"
              :alt="video.title"
              class="absolute inset-0 w-full h-full object-cover"
            />
            <!-- Placeholder -->
            <div v-if="!video.video_url && !video.cover_url" class="w-full h-full flex items-center justify-center text-border">
              <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
              </svg>
            </div>
            <!-- Sort Order Badge -->
            <span class="absolute top-2 left-2 px-2 py-1 bg-black/60 text-white text-xs rounded">
              #{{ index + 1 }}
            </span>
            <!-- Status Badge -->
            <div v-if="video.status !== 'enabled'" class="absolute inset-0 bg-black/50 flex items-center justify-center">
              <span class="text-white text-sm bg-red-500 px-2 py-1 rounded">已禁用</span>
            </div>
            <!-- Play Icon Overlay -->
            <div v-if="video.video_url" class="absolute inset-0 flex items-center justify-center bg-black/20 opacity-0 hover:opacity-100 transition-opacity">
              <div class="w-16 h-16 rounded-full bg-white/90 flex items-center justify-center">
                <svg class="w-8 h-8 text-primary ml-1" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M8 5v14l11-7z"/>
                </svg>
              </div>
            </div>
          </div>

          <div class="p-4">
            <h3 class="font-medium truncate">{{ video.title || '无标题' }}</h3>
            <p v-if="video.description" class="text-sm text-text-secondary truncate mt-1">{{ video.description }}</p>
            <div class="flex items-center gap-2 mt-4">
              <button
                @click="moveVideo(index, -1)"
                :disabled="index === 0"
                class="p-2 text-text-secondary hover:bg-secondary/50 rounded-lg transition-colors disabled:opacity-30"
                title="上移"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
                </svg>
              </button>
              <button
                @click="moveVideo(index, 1)"
                :disabled="index === videos.length - 1"
                class="p-2 text-text-secondary hover:bg-secondary/50 rounded-lg transition-colors disabled:opacity-30"
                title="下移"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>
              <button
                @click="openForm(video)"
                class="flex-1 px-3 py-2 text-sm border border-border rounded-lg hover:bg-secondary/50 transition-colors"
              >
                编辑
              </button>
              <button
                @click="confirmDelete(video)"
                class="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="videos.length === 0 && !loading" class="text-center py-16">
        <svg class="w-16 h-16 mx-auto text-border mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
        </svg>
        <p class="text-text-secondary">暂无视频，点击上方按钮添加</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-16">
        <div class="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
      </div>
    </div>

    <!-- Video Form Modal -->
    <teleport to="body">
      <transition name="modal">
        <div v-if="isFormOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
          <div @click.self="closeForm" class="absolute inset-0 bg-black/50" />
          <div class="relative bg-white rounded-xl shadow-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
            <div class="border-b border-border px-6 py-4 flex items-center justify-between sticky top-0 bg-white rounded-t-xl">
              <h2 class="text-lg font-medium">{{ editingVideo ? '编辑视频' : '新增视频' }}</h2>
              <button @click="closeForm" class="p-2 hover:bg-secondary/50 rounded">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>

            <form @submit.prevent="handleSubmit" class="p-6 space-y-5">
              <!-- Video & Cover Row -->
              <div class="flex gap-4">
                <!-- Video Upload -->
                <div class="flex-1">
                  <label class="block text-sm font-medium mb-2">视频文件</label>
                  <div
                    class="border-2 border-dashed border-border rounded-xl overflow-hidden transition-colors hover:border-primary"
                    style="aspect-ratio: 9/16; max-height: 320px;"
                  >
                    <div v-if="form.video_url" class="relative w-full h-full">
                      <video :src="form.video_url" class="w-full h-full object-cover" controls />
                      <button
                        type="button"
                        @click="form.video_url = ''"
                        class="absolute top-2 right-2 w-7 h-7 bg-black/50 hover:bg-black/70 text-white rounded-full flex items-center justify-center"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                      </button>
                    </div>
                    <div v-else class="w-full h-full flex flex-col items-center justify-center">
                      <input
                        ref="videoInput"
                        type="file"
                        accept="video/*"
                        @change="handleVideoSelect"
                        class="hidden"
                      />
                      <button
                        type="button"
                        @click="videoInput?.click()"
                        class="w-12 h-12 rounded-full bg-secondary/50 flex items-center justify-center mb-2 hover:bg-secondary transition-colors"
                        :disabled="uploadingVideo"
                      >
                        <svg v-if="!uploadingVideo" class="w-6 h-6 text-text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                        </svg>
                        <svg v-else class="w-6 h-6 text-primary animate-spin" fill="none" viewBox="0 0 24 24">
                          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                      </button>
                      <p v-if="!uploadingVideo" class="text-text-secondary text-xs">点击上传</p>
                      <p v-else class="text-primary text-xs">上传中...</p>
                    </div>
                  </div>
                  <!-- 手动输入视频链接 -->
                  <div class="mt-3">
                    <div class="flex gap-2">
                      <input
                        v-model="form.video_url"
                        type="text"
                        placeholder="输入视频链接（例如：https://example.com/video.mp4）"
                        class="flex-1 px-3 py-1.5 border border-border rounded-lg text-xs"
                      />
                      <button
                        type="button"
                        @click="form.video_url = ''"
                        class="px-3 py-1.5 bg-secondary text-text-secondary rounded-lg text-xs hover:bg-secondary/80"
                        :disabled="!form.video_url"
                      >
                        清除
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Cover Upload -->
                <div class="flex-1">
                  <label class="block text-sm font-medium mb-2">封面图片</label>
                  <div
                    class="border-2 border-dashed border-border rounded-xl overflow-hidden transition-colors hover:border-primary"
                    style="aspect-ratio: 9/16; max-height: 320px;"
                  >
                    <div v-if="form.cover_url" class="relative w-full h-full">
                      <img :src="form.cover_url" alt="Cover" class="w-full h-full object-cover" />
                      <button
                        type="button"
                        @click="form.cover_url = ''"
                        class="absolute top-2 right-2 w-7 h-7 bg-black/50 hover:bg-black/70 text-white rounded-full flex items-center justify-center"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                      </button>
                    </div>
                    <div v-else class="w-full h-full flex flex-col items-center justify-center">
                      <input
                        ref="coverInput"
                        type="file"
                        accept="image/*"
                        @change="handleCoverSelect"
                        class="hidden"
                      />
                      <button
                        type="button"
                        @click="coverInput?.click()"
                        class="w-12 h-12 rounded-full bg-secondary/50 flex items-center justify-center mb-2 hover:bg-secondary transition-colors"
                        :disabled="uploadingCover"
                      >
                        <svg v-if="!uploadingCover" class="w-6 h-6 text-text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                        </svg>
                        <svg v-else class="w-6 h-6 text-primary animate-spin" fill="none" viewBox="0 0 24 24">
                          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                      </button>
                      <p v-if="!uploadingCover" class="text-text-secondary text-xs">点击上传</p>
                      <p v-else class="text-primary text-xs">上传中...</p>
                    </div>
                  </div>
                  <!-- 手动输入封面链接 -->
                  <div class="mt-3">
                    <div class="flex gap-2">
                      <input
                        v-model="form.cover_url"
                        type="text"
                        placeholder="输入封面链接（例如：https://example.com/cover.jpg）"
                        class="flex-1 px-3 py-1.5 border border-border rounded-lg text-xs"
                      />
                      <button
                        type="button"
                        @click="form.cover_url = ''"
                        class="px-3 py-1.5 bg-secondary text-text-secondary rounded-lg text-xs hover:bg-secondary/80"
                        :disabled="!form.cover_url"
                      >
                        清除
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium mb-2">关联产品（可选）</label>
                <div class="relative">
                  <input
                    v-model="productSearch"
                    type="text"
                    placeholder="搜索产品..."
                    class="w-full px-4 py-3 rounded-lg border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
                    @focus="showProductDropdown = true"
                    @blur="hideProductDropdown"
                  />
                  <!-- Selected Product -->
                  <div v-if="selectedProduct" class="mt-2 p-3 bg-secondary/30 rounded-lg flex items-center justify-between">
                    <div class="flex items-center gap-2">
                      <img v-if="selectedProduct.image" :src="selectedProduct.image" class="w-10 h-10 rounded object-cover" />
                      <div>
                        <p class="text-sm font-medium">{{ selectedProduct.name }}</p>
                        <p class="text-xs text-text-secondary">¥{{ selectedProduct.price }}</p>
                      </div>
                    </div>
                    <button type="button" @click="clearProduct" class="p-1 hover:bg-secondary rounded">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                      </svg>
                    </button>
                  </div>
                  <!-- Dropdown -->
                  <div v-if="showProductDropdown && filteredProducts.length > 0" class="absolute z-10 w-full mt-1 bg-white rounded-lg border border-border shadow-lg max-h-60 overflow-y-auto">
                    <button
                      v-for="product in filteredProducts"
                      :key="product.id"
                      type="button"
                      class="w-full px-4 py-2 text-left hover:bg-secondary/50 flex items-center gap-3"
                      @mousedown.prevent="selectProduct(product)"
                    >
                      <img v-if="product.image" :src="product.image" class="w-8 h-8 rounded object-cover" />
                      <div class="flex-1">
                        <p class="text-sm">{{ product.name }}</p>
                        <p class="text-xs text-text-secondary">¥{{ product.price }}</p>
                      </div>
                    </button>
                  </div>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium mb-2">标题 *</label>
                <input
                  v-model="form.title"
                  type="text"
                  placeholder="请输入视频标题"
                  class="w-full px-4 py-3 rounded-lg border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
                  :class="{ 'border-red-400': submitted && !form.title }"
                  required
                />
                <p v-if="submitted && !form.title" class="text-red-500 text-sm mt-1">请输入标题</p>
              </div>

              <div>
                <label class="block text-sm font-medium mb-2">描述</label>
                <textarea
                  v-model="form.description"
                  rows="2"
                  placeholder="请输入视频描述（可选）"
                  class="w-full px-4 py-3 rounded-lg border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none resize-none"
                />
              </div>

              <div>
                <label class="block text-sm font-medium mb-2">排序</label>
                <input
                  v-model.number="form.sort_order"
                  type="number"
                  min="0"
                  placeholder="数字越小越靠前"
                  class="w-full px-4 py-3 rounded-lg border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
                />
              </div>

              <div>
                <label class="flex items-center gap-3 cursor-pointer">
                  <input
                    v-model="formStatus"
                    type="checkbox"
                    class="w-5 h-5 rounded border-border text-primary focus:ring-primary"
                  />
                  <span class="text-sm">启用此视频</span>
                </label>
              </div>

              <div class="flex gap-3 pt-2">
                <button type="button" @click="closeForm" class="flex-1 btn btn-secondary">
                  取消
                </button>
                <button type="submit" :disabled="submitting" class="flex-1 btn btn-primary disabled:opacity-50">
                  {{ submitting ? '保存中...' : '保存' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </transition>
    </teleport>

    <!-- Delete Confirmation Modal -->
    <teleport to="body">
      <transition name="modal">
        <div v-if="isDeleteModalOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
          <div @click.self="isDeleteModalOpen = false" class="absolute inset-0 bg-black/50" />
          <div class="relative bg-white rounded-xl shadow-2xl w-full max-w-md p-6">
            <div class="text-center">
              <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-red-100 flex items-center justify-center">
                <svg class="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                </svg>
              </div>
              <h3 class="text-lg font-medium mb-2">确认删除</h3>
              <p class="text-text-secondary mb-6">
                确定要删除视频 "<span class="font-medium">{{ deletingVideo?.title || '此视频' }}</span>" 吗？
              </p>
              <div class="flex gap-3">
                <button @click="isDeleteModalOpen = false" class="flex-1 btn btn-secondary">
                  取消
                </button>
                <button @click="handleDelete" :disabled="deleting" class="flex-1 bg-red-500 text-white hover:bg-red-600 btn disabled:opacity-50">
                  {{ deleting ? '删除中...' : '确认删除' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </teleport>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import AdminLayout from './AdminLayout.vue'
import axios from 'axios'

const videos = ref([])
const loading = ref(false)

// Form state
const isFormOpen = ref(false)
const editingVideo = ref(null)
const submitting = ref(false)
const submitted = ref(false)
const formStatus = ref(true)
const form = ref({
  title: '',
  description: '',
  video_url: '',
  cover_url: '',
  sort_order: 0,
  status: 'enabled',
  product_id: null
})

// Product search
const products = ref([])
const productSearch = ref('')
const showProductDropdown = ref(false)
const selectedProduct = ref(null)

async function fetchProducts() {
  try {
    const res = await api.get('/products')
    products.value = res.data.data || []
  } catch (err) {
    console.error('Failed to fetch products:', err)
  }
}

const filteredProducts = ref([])

// Watch for product search input
watch(productSearch, () => {
  filterProducts()
  showProductDropdown.value = true
})

function filterProducts() {
  if (!productSearch.value) {
    filteredProducts.value = products.value.slice(0, 10)
    return
  }
  const search = productSearch.value.toLowerCase()
  filteredProducts.value = products.value
    .filter(p => p.name?.toLowerCase().includes(search))
    .slice(0, 10)
}

function selectProduct(product) {
  selectedProduct.value = product
  form.value.product_id = product.id
  productSearch.value = product.name
  showProductDropdown.value = false
}

function clearProduct() {
  selectedProduct.value = null
  form.value.product_id = null
  productSearch.value = ''
}

function hideProductDropdown() {
  setTimeout(() => {
    showProductDropdown.value = false
  }, 200)
}

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('admin_token') || ''}`
  }
})

// Fetch videos from API
async function fetchVideos() {
  loading.value = true
  try {
    const res = await api.get('/videos/all')
    videos.value = res.data.data || []
  } catch (err) {
    console.error('Failed to fetch videos:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchVideos()
  fetchProducts()
})

function openForm(video = null) {
  submitted.value = false
  // Reset product selection
  selectedProduct.value = null
  productSearch.value = ''
  
  if (video) {
    editingVideo.value = video
    form.value = { 
      ...video,
      product_id: video.product_id || null
    }
    formStatus.value = video.status === 'enabled'
    // Set selected product if exists
    if (video.product_id) {
      const product = products.value.find(p => p.id === video.product_id)
      if (product) {
        selectedProduct.value = product
        productSearch.value = product.name
      }
    }
  } else {
    editingVideo.value = null
    form.value = {
      title: '',
      description: '',
      video_url: '',
      cover_url: '',
      sort_order: videos.value.length,
      status: 'enabled',
      product_id: null
    }
    formStatus.value = true
  }
  isFormOpen.value = true
}

function closeForm() {
  isFormOpen.value = false
  editingVideo.value = null
  submitting.value = false
  submitted.value = false
}

async function handleSubmit() {
  submitted.value = true
  if (!form.value.title) return

  submitting.value = true
  form.value.status = formStatus.value ? 'enabled' : 'disabled'
  try {
    if (editingVideo.value) {
      await api.put(`/videos/${editingVideo.value.id}`, form.value)
    } else {
      await api.post('/videos', form.value)
    }
    await fetchVideos()
    closeForm()
  } catch (err) {
    console.error('Failed to save video:', err)
    submitting.value = false
  }
}

// Video upload ref
const videoInput = ref(null)
const coverInput = ref(null)
const uploadingVideo = ref(false)
const uploadingCover = ref(false)

// Video upload handler
async function handleVideoSelect(event) {
  const file = event.target.files[0]
  if (!file) return

  // Validate file type
  if (!file.type.startsWith('video/')) {
    alert('请选择视频文件')
    return
  }

  // Validate file size (max 50MB)
  if (file.size > 50 * 1024 * 1024) {
    alert('视频大小不能超过50MB')
    return
  }

  // Check if logged in
  const token = localStorage.getItem('admin_token')
  if (!token) {
    alert('请先登录')
    return
  }

  uploadingVideo.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)
    // 不设置 Content-Type，让 axios 自动处理
    const res = await api.post('/upload/video', formData)
    form.value.video_url = res.data.url
  } catch (err) {
    console.error('Failed to upload video:', err)
    const errorMsg = err.response?.data?.message || err.message
    if (err.response?.status === 401) {
      alert('登录已过期，请重新登录')
    } else {
      alert('视频上传失败: ' + errorMsg)
    }
  } finally {
    uploadingVideo.value = false
  }
}

// Cover upload handler
async function handleCoverSelect(event) {
  const file = event.target.files[0]
  if (!file) return

  // Validate file type
  if (!file.type.startsWith('image/')) {
    alert('请选择图片文件')
    return
  }

  // Validate file size (max 5MB)
  if (file.size > 5 * 1024 * 1024) {
    alert('封面图片不能超过5MB')
    return
  }

  // Check if logged in
  const token = localStorage.getItem('admin_token')
  if (!token) {
    alert('请先登录')
    return
  }

  uploadingCover.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)
    // 不设置 Content-Type，让 axios 自动处理
    const res = await api.post('/upload/cover', formData)
    form.value.cover_url = res.data.url
  } catch (err) {
    console.error('Failed to upload cover:', err)
    const errorMsg = err.response?.data?.message || err.message
    if (err.response?.status === 401) {
      alert('登录已过期，请重新登录')
    } else {
      alert('封面上传失败: ' + errorMsg)
    }
  } finally {
    uploadingCover.value = false
  }
}

// Move video position
async function moveVideo(index, direction) {
  const newIndex = index + direction
  if (newIndex < 0 || newIndex >= videos.value.length) return

  // Swap in local array
  const temp = videos.value[index]
  videos.value[index] = videos.value[newIndex]
  videos.value[newIndex] = temp

  // Save new order
  try {
    const videoIds = videos.value.map(v => v.id)
    await api.put('/videos/reorder', { video_ids: videoIds })
  } catch (err) {
    console.error('Failed to reorder videos:', err)
    await fetchVideos() // Revert on error
  }
}

// Delete state
const isDeleteModalOpen = ref(false)
const deletingVideo = ref(null)
const deleting = ref(false)

function confirmDelete(video) {
  deletingVideo.value = video
  isDeleteModalOpen.value = true
}

async function handleDelete() {
  if (!deletingVideo.value) return
  deleting.value = true
  try {
    await api.delete(`/videos/${deletingVideo.value.id}`)
    await fetchVideos()
    isDeleteModalOpen.value = false
    deletingVideo.value = null
  } catch (err) {
    console.error('Failed to delete video:', err)
  } finally {
    deleting.value = false
  }
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>

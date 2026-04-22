<template>
  <AdminLayout>
    <div class="mb-8">
      <h1 class="text-2xl font-serif mb-2">媒体库</h1>
      <p class="text-text-secondary">管理所有上传的图片和视频</p>
    </div>

    <!-- Tabs and Batch Actions -->
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6 border-b border-border pb-2">
      <!-- Tabs -->
      <div class="flex gap-4">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          @click="activeTab = tab.key"
          :class="[
            'px-4 py-2 font-medium transition-colors border-b-2 -mb-px',
            activeTab === tab.key
              ? 'border-primary text-primary'
              : 'border-transparent text-text-secondary hover:text-text-primary'
          ]"
        >
          {{ tab.label }}
          <span class="ml-2 text-sm bg-secondary px-2 py-0.5 rounded-full">
            {{ tab.key === 'images' ? totalImages : totalVideos }}
          </span>
        </button>
      </div>
      
      <!-- Pagination -->
      <div v-if="(activeTab === 'images' && totalImages > itemsPerPage.images) || (activeTab === 'videos' && totalVideos > itemsPerPage.videos)" class="flex items-center gap-2">
        <button
          @click="currentPage = 1"
          :disabled="currentPage === 1"
          class="px-3 py-1 border border-border rounded hover:bg-secondary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          首页
        </button>
        <button
          @click="currentPage--"
          :disabled="currentPage === 1"
          class="px-3 py-1 border border-border rounded hover:bg-secondary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          上一页
        </button>
        <span class="px-3 py-1">
          {{ currentPage }} / {{ totalPages }}
        </span>
        <button
          @click="currentPage++"
          :disabled="currentPage === totalPages"
          class="px-3 py-1 border border-border rounded hover:bg-secondary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          下一页
        </button>
        <button
          @click="currentPage = totalPages"
          :disabled="currentPage === totalPages"
          class="px-3 py-1 border border-border rounded hover:bg-secondary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          末页
        </button>
      </div>
      
      <!-- Batch Actions -->
      <div class="flex flex-wrap items-center gap-2">
        <button
          v-if="(activeTab === 'images' && paginatedImages.length > 0) || (activeTab === 'videos' && paginatedVideos.length > 0)"
          @click="toggleSelectAll"
          class="px-4 py-2 bg-secondary text-text-primary text-sm rounded hover:bg-secondary/80 transition-colors"
        >
          {{ isSelectAll ? '取消全选' : '全选' }}
        </button>
        <span v-if="selectedItems.length > 0" class="text-sm text-text-secondary">已选择 {{ selectedItems.length }} 项</span>
        <button
          v-if="selectedItems.length > 0"
          @click="batchDelete"
          class="px-4 py-2 bg-red-500 text-white text-sm rounded hover:bg-red-600 transition-colors"
        >
          批量删除
        </button>
        <button
          v-if="selectedItems.length > 0"
          @click="clearSelection"
          class="px-4 py-2 bg-secondary text-text-primary text-sm rounded hover:bg-secondary/80 transition-colors"
        >
          取消选择
        </button>
      </div>
    </div>

    <!-- Images Grid -->
    <div v-if="activeTab === 'images'" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
      <div
        v-for="(img, index) in paginatedImages"
        :key="index"
        class="relative group rounded-lg overflow-hidden bg-secondary/30"
      >
        <!-- Checkbox -->
        <div class="absolute top-2 left-2 z-10">
          <input
            type="checkbox"
            :checked="selectedItems.includes(img.filename)"
            @change="toggleSelection(img.filename, 'image')"
            class="w-4 h-4 accent-primary"
          />
        </div>
        <div class="aspect-square">
          <img
            :src="img.url"
            :alt="img.filename"
            class="w-full h-full object-cover"
          />
        </div>
        <!-- Overlay -->
        <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center gap-2">
          <span class="text-white text-xs text-center px-2 truncate w-full">{{ img.filename }}</span>
          <div class="flex gap-2">
            <button
              @click="copyUrl(img.url)"
              class="px-3 py-1 bg-white/20 text-white text-xs rounded hover:bg-white/30"
            >
              复制链接
            </button>
            <button
              @click="deleteFile(img.filename, 'image')"
              class="px-3 py-1 bg-red-500/80 text-white text-xs rounded hover:bg-red-500"
            >
              删除
            </button>
          </div>
        </div>
      </div>
      <div v-if="paginatedImages.length === 0" class="col-span-full text-center py-12 text-text-secondary">
        暂无图片
      </div>
    </div>

    <!-- Videos Grid -->
    <div v-if="activeTab === 'videos'" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <div
        v-for="(video, index) in paginatedVideos"
        :key="index"
        class="relative group rounded-lg overflow-hidden bg-secondary/30"
      >
        <!-- Checkbox -->
        <div class="absolute top-2 left-2 z-10">
          <input
            type="checkbox"
            :checked="selectedItems.includes(video.filename)"
            @change="toggleSelection(video.filename, 'video')"
            class="w-4 h-4 accent-primary"
          />
        </div>
        <div class="aspect-video">
          <video
            :src="video.url"
            class="w-full h-full object-cover"
            muted
          />
        </div>
        <!-- Duration Badge -->
        <div class="absolute bottom-2 right-2 px-2 py-0.5 bg-black/70 text-white text-xs rounded">
          视频
        </div>
        <!-- Overlay -->
        <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center gap-2">
          <span class="text-white text-xs text-center px-2 truncate w-full">{{ video.filename }}</span>
          <div class="flex gap-2">
            <button
              @click="copyUrl(video.url)"
              class="px-3 py-1 bg-white/20 text-white text-xs rounded hover:bg-white/30"
            >
              复制链接
            </button>
            <button
              @click="deleteFile(video.filename, 'video')"
              class="px-3 py-1 bg-red-500/80 text-white text-xs rounded hover:bg-red-500"
            >
              删除
            </button>
          </div>
        </div>
      </div>
      <div v-if="paginatedVideos.length === 0" class="col-span-full text-center py-12 text-text-secondary">
        暂无视频
      </div>
    </div>



    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-8 h-8 border-4 border-primary/30 border-t-primary rounded-full animate-spin" />
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import AdminLayout from './AdminLayout.vue'

const tabs = [
  { key: 'images', label: '图片' },
  { key: 'videos', label: '视频' }
]

const activeTab = ref('images')
const loading = ref(false)
const images = ref([])
const videos = ref([])
const selectedItems = ref([])
const currentPage = ref(1)
const itemsPerPage = ref({
  images: 18,
  videos: 12
})

const API_BASE = '/api/media'

// 计算属性
const totalImages = computed(() => images.value.length)
const totalVideos = computed(() => videos.value.length)

const totalPages = computed(() => {
  if (activeTab.value === 'images') {
    return Math.ceil(totalImages.value / itemsPerPage.value.images)
  } else {
    return Math.ceil(totalVideos.value / itemsPerPage.value.videos)
  }
})

const paginatedImages = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value.images
  const end = start + itemsPerPage.value.images
  return images.value.slice(start, end)
})

const paginatedVideos = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value.videos
  const end = start + itemsPerPage.value.videos
  return videos.value.slice(start, end)
})

const isSelectAll = computed(() => {
  if (activeTab.value === 'images') {
    return paginatedImages.value.length > 0 && paginatedImages.value.every(img => selectedItems.value.includes(img.filename))
  } else {
    return paginatedVideos.value.length > 0 && paginatedVideos.value.every(video => selectedItems.value.includes(video.filename))
  }
})

async function fetchMedia() {
  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/list`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
      }
    })
    const data = await res.json()
    if (data.code === 200) {
      images.value = data.data.images || []
      videos.value = data.data.videos || []
      // Reset pagination and selection when fetching new data
      currentPage.value = 1
      selectedItems.value = []
    }
  } catch (err) {
    console.error('Failed to fetch media:', err)
  }
  loading.value = false
}

async function deleteFile(filename, type) {
  if (!confirm(`确定要删除 ${filename} 吗？`)) return
  
  try {
    const res = await fetch(`${API_BASE}/delete`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
      },
      body: JSON.stringify({ filename, type })
    })
    const data = await res.json()
    if (data.code === 200) {
      // Remove from list
      if (type === 'image') {
        images.value = images.value.filter(i => i.filename !== filename)
      } else {
        videos.value = videos.value.filter(v => v.filename !== filename)
      }
      // Remove from selection
      selectedItems.value = selectedItems.value.filter(item => item !== filename)
    } else {
      alert(data.message || '删除失败')
    }
  } catch (err) {
    console.error('Failed to delete file:', err)
    alert('删除失败')
  }
}

async function batchDelete() {
  if (!selectedItems.value.length) return
  
  if (!confirm(`确定要删除选中的 ${selectedItems.value.length} 项吗？`)) return
  
  try {
    const res = await fetch(`${API_BASE}/batch-delete`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
      },
      body: JSON.stringify({ filenames: selectedItems.value })
    })
    const data = await res.json()
    if (data.code === 200) {
      // Remove deleted items from lists
      images.value = images.value.filter(img => !selectedItems.value.includes(img.filename))
      videos.value = videos.value.filter(video => !selectedItems.value.includes(video.filename))
      // Clear selection
      selectedItems.value = []
      alert(`成功删除 ${data.deleted_count} 项`)
    } else {
      alert(data.message || '批量删除失败')
    }
  } catch (err) {
    console.error('Failed to batch delete files:', err)
    alert('批量删除失败')
  }
}

function toggleSelection(filename, type) {
  const index = selectedItems.value.indexOf(filename)
  if (index > -1) {
    selectedItems.value.splice(index, 1)
  } else {
    selectedItems.value.push(filename)
  }
}

function toggleSelectAll() {
  if (activeTab.value === 'images') {
    if (isSelectAll.value) {
      // 取消全选
      paginatedImages.value.forEach(img => {
        const index = selectedItems.value.indexOf(img.filename)
        if (index > -1) {
          selectedItems.value.splice(index, 1)
        }
      })
    } else {
      // 全选
      paginatedImages.value.forEach(img => {
        if (!selectedItems.value.includes(img.filename)) {
          selectedItems.value.push(img.filename)
        }
      })
    }
  } else {
    if (isSelectAll.value) {
      // 取消全选
      paginatedVideos.value.forEach(video => {
        const index = selectedItems.value.indexOf(video.filename)
        if (index > -1) {
          selectedItems.value.splice(index, 1)
        }
      })
    } else {
      // 全选
      paginatedVideos.value.forEach(video => {
        if (!selectedItems.value.includes(video.filename)) {
          selectedItems.value.push(video.filename)
        }
      })
    }
  }
}

function clearSelection() {
  selectedItems.value = []
}

function copyUrl(url) {
  navigator.clipboard.writeText(window.location.origin + url)
  alert('链接已复制')
}

// 监听标签切换，重置分页
watch(activeTab, () => {
  currentPage.value = 1
  selectedItems.value = []
})

onMounted(() => {
  fetchMedia()
})
</script>

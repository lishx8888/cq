<template>
  <AdminLayout>
    <div class="mb-8">
      <h1 class="text-2xl font-serif mb-2">媒体库</h1>
      <p class="text-text-secondary">管理所有上传的图片和视频</p>
    </div>

    <!-- Tabs -->
    <div class="flex gap-4 mb-6 border-b border-border">
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
          {{ tab.key === 'images' ? images.length : videos.length }}
        </span>
      </button>
    </div>

    <!-- Images Grid -->
    <div v-if="activeTab === 'images'" class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
      <div
        v-for="(img, index) in images"
        :key="index"
        class="relative group aspect-square rounded-lg overflow-hidden bg-secondary/30"
      >
        <img
          :src="img.url"
          :alt="img.filename"
          class="w-full h-full object-cover"
        />
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
      <div v-if="images.length === 0" class="col-span-full text-center py-12 text-text-secondary">
        暂无图片
      </div>
    </div>

    <!-- Videos Grid -->
    <div v-if="activeTab === 'videos'" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <div
        v-for="(video, index) in videos"
        :key="index"
        class="relative group rounded-lg overflow-hidden bg-secondary/30 aspect-video"
      >
        <video
          :src="video.url"
          class="w-full h-full object-cover"
          muted
        />
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
      <div v-if="videos.length === 0" class="col-span-full text-center py-12 text-text-secondary">
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
import { ref, onMounted } from 'vue'
import AdminLayout from './AdminLayout.vue'

const tabs = [
  { key: 'images', label: '图片' },
  { key: 'videos', label: '视频' }
]

const activeTab = ref('images')
const loading = ref(false)
const images = ref([])
const videos = ref([])

const API_BASE = '/api/media'

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
    } else {
      alert(data.message || '删除失败')
    }
  } catch (err) {
    console.error('Failed to delete file:', err)
    alert('删除失败')
  }
}

function copyUrl(url) {
  navigator.clipboard.writeText(window.location.origin + url)
  alert('链接已复制')
}

onMounted(() => {
  fetchMedia()
})
</script>

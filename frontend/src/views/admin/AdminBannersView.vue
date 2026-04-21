<template>
  <AdminLayout>
    <div>
      <!-- Header -->
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
        <div>
          <h1 class="text-2xl font-medium">Banner管理</h1>
          <p class="text-text-secondary mt-1">管理首页轮播图</p>
        </div>
        <button @click="openForm()" class="btn btn-primary flex items-center gap-2 self-start">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          新增Banner
        </button>
      </div>

      <!-- Banners Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="banner in banners"
          :key="banner.id"
          class="bg-surface rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow"
        >
          <div class="bg-secondary/30 relative aspect-video">
            <img
              v-if="banner.image"
              :src="banner.image"
              :alt="banner.title"
              class="w-full h-full object-cover"
            />
            <div v-else class="w-full h-full flex items-center justify-center text-border">
              <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
              </svg>
            </div>
            <div v-if="banner.status !== 'enabled'" class="absolute inset-0 bg-black/50 flex items-center justify-center">
              <span class="text-white text-sm bg-red-500 px-2 py-1 rounded">已禁用</span>
            </div>
          </div>
          <div class="p-4">
            <h3 class="font-medium truncate">{{ banner.title || '无标题' }}</h3>
            <p class="text-sm text-text-secondary truncate mt-1">{{ banner.subtitle || '无副标题' }}</p>
            <div class="flex items-center gap-2 mt-4">
              <button
                @click="openForm(banner)"
                class="flex-1 px-3 py-2 text-sm border border-border rounded-lg hover:bg-secondary/50 transition-colors"
              >
                编辑
              </button>
              <button
                @click="confirmDelete(banner)"
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
      <div v-if="banners.length === 0 && !loading" class="text-center py-16">
        <svg class="w-16 h-16 mx-auto text-border mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
        </svg>
        <p class="text-text-secondary">暂无Banner，点击上方按钮添加</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-16">
        <div class="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
      </div>
    </div>

    <!-- Banner Form Modal -->
    <teleport to="body">
      <transition name="modal">
        <div v-if="isFormOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
          <div @click.self="closeForm" class="absolute inset-0 bg-black/50" />
          <div class="relative bg-white rounded-xl shadow-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
            <div class="border-b border-border px-6 py-4 flex items-center justify-between sticky top-0 bg-white rounded-t-xl">
              <h2 class="text-lg font-medium">{{ editingBanner ? '编辑Banner' : '新增Banner' }}</h2>
              <button @click="closeForm" class="p-2 hover:bg-secondary/50 rounded">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>

            <form @submit.prevent="handleSubmit" class="p-6 space-y-5">
              <!-- Image Upload -->
              <div>
                <label class="block text-sm font-medium mb-2">Banner图片 *</label>
                <div
                  class="border-2 border-dashed border-border rounded-xl overflow-hidden transition-colors hover:border-primary"
                  :class="{ 'border-red-400': submitted && !form.image }"
                >
                  <div v-if="form.image" class="relative">
                    <img :src="form.image" alt="Preview" class="w-full object-cover aspect-video" />
                    <button
                      type="button"
                      @click="form.image = ''"
                      class="absolute top-2 right-2 w-8 h-8 bg-black/50 hover:bg-black/70 text-white rounded-full flex items-center justify-center"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                      </svg>
                    </button>
                  </div>
                  <div v-else class="p-8 text-center">
                    <input
                      ref="fileInput"
                      type="file"
                      accept="image/*"
                      @change="handleFileSelect"
                      class="hidden"
                    />
                    <button
                      type="button"
                      @click="$refs.fileInput.click()"
                      class="mx-auto w-16 h-16 rounded-full bg-secondary/50 flex items-center justify-center mb-4 hover:bg-secondary transition-colors"
                    >
                      <svg class="w-8 h-8 text-text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                      </svg>
                    </button>
                    <p class="text-text-secondary text-sm">点击上传图片</p>
                    <p class="text-text-secondary text-xs mt-1">推荐尺寸: 1920 x 1080 (16:9横版)</p>
                  </div>
                </div>
                <p v-if="submitted && !form.image" class="text-red-500 text-sm mt-1">请上传Banner图片</p>
              </div>

              <div>
                <label class="block text-sm font-medium mb-2">标题 *</label>
                <input
                  v-model="form.title"
                  type="text"
                  placeholder="请输入Banner标题"
                  class="w-full px-4 py-3 rounded-lg border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
                  :class="{ 'border-red-400': submitted && !form.title }"
                  required
                />
                <p v-if="submitted && !form.title" class="text-red-500 text-sm mt-1">请输入标题</p>
              </div>

              <div>
                <label class="block text-sm font-medium mb-2">副标题</label>
                <input
                  v-model="form.subtitle"
                  type="text"
                  placeholder="请输入副标题（可选）"
                  class="w-full px-4 py-3 rounded-lg border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
                />
              </div>

              <div>
                <label class="block text-sm font-medium mb-2">链接地址</label>
                <input
                  v-model="form.link"
                  type="text"
                  placeholder="点击Banner跳转的链接，如 /products"
                  class="w-full px-4 py-3 rounded-lg border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
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
                  <span class="text-sm">启用此Banner</span>
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
                确定要删除Banner "<span class="font-medium">{{ deletingBanner?.title || '此Banner' }}</span>" 吗？
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
import { ref, onMounted } from 'vue'
import AdminLayout from './AdminLayout.vue'
import { bannerApi } from '@/api'

const banners = ref([])
const loading = ref(false)

// Form state
const isFormOpen = ref(false)
const editingBanner = ref(null)
const submitting = ref(false)
const formStatus = ref(true)
const form = ref({
  title: '',
  subtitle: '',
  image: '',
  link: '',
  sort_order: 0,
  status: 'enabled'
})

// Fetch banners from API
async function fetchBanners() {
  loading.value = true
  try {
    const res = await bannerApi.getList()
    banners.value = res.data || []
  } catch (err) {
    console.error('Failed to fetch banners:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchBanners()
})

function openForm(banner = null) {
  if (banner) {
    editingBanner.value = banner
    form.value = { ...banner }
    formStatus.value = banner.status === 'enabled'
  } else {
    editingBanner.value = null
    form.value = {
      title: '',
      subtitle: '',
      image: '',
      link: '',
      sort_order: banners.value.length,
      status: 'enabled'
    }
    formStatus.value = true
  }
  isFormOpen.value = true
}

function closeForm() {
  isFormOpen.value = false
  editingBanner.value = null
  submitting.value = false
}

async function handleSubmit() {
  submitting.value = true
  form.value.status = formStatus.value ? 'enabled' : 'disabled'
  try {
    if (editingBanner.value) {
      await bannerApi.update(editingBanner.value.id, form.value)
    } else {
      await bannerApi.create(form.value)
    }
    await fetchBanners()
    closeForm()
  } catch (err) {
    console.error('Failed to save banner:', err)
    submitting.value = false
  }
}

// File upload handler
function handleFileSelect(event) {
  const file = event.target.files[0]
  if (!file) return

  // Validate file type
  if (!file.type.startsWith('image/')) {
    alert('请选择图片文件')
    return
  }

  // Validate file size (max 5MB)
  if (file.size > 5 * 1024 * 1024) {
    alert('图片大小不能超过5MB')
    return
  }

  // Convert to base64 for local storage
  const reader = new FileReader()
  reader.onload = (e) => {
    form.value.image = e.target.result
  }
  reader.readAsDataURL(file)
}

// Delete state
const isDeleteModalOpen = ref(false)
const deletingBanner = ref(null)
const deleting = ref(false)

function confirmDelete(banner) {
  deletingBanner.value = banner
  isDeleteModalOpen.value = true
}

async function handleDelete() {
  if (!deletingBanner.value) return
  deleting.value = true
  try {
    await bannerApi.delete(deletingBanner.value.id)
    await fetchBanners()
    isDeleteModalOpen.value = false
    deletingBanner.value = null
  } catch (err) {
    console.error('Failed to delete banner:', err)
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

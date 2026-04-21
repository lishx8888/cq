<template>
  <AdminLayout>
    <div class="mb-6">
      <h1 class="text-2xl font-serif">系统设置</h1>
      <p class="text-text-secondary mt-1">管理网站基本配置</p>
    </div>

    <div class="bg-surface rounded-xl p-6 max-w-2xl">
      <!-- Logo 设置 -->
      <div class="mb-8">
        <h2 class="text-lg font-medium mb-4">Logo 设置</h2>
        
        <!-- 当前 Logo 预览 -->
        <div class="mb-4 p-6 bg-background rounded-lg border border-border">
          <p class="text-sm text-text-secondary mb-4">当前 Logo 预览：</p>
          <div class="flex items-center gap-3">
            <div class="w-10 h-10" v-html="currentLogoSvg || defaultLogoSvg"></div>
            <span class="font-serif text-2xl text-primary">{{ settings.site_name || 'Daidy' }}</span>
          </div>
        </div>

        <!-- Logo 图片上传 -->
        <div class="mb-6">
          <label class="block text-sm font-medium mb-2">上传 Logo 图片</label>
          <div class="flex items-center gap-4">
            <input
              ref="logoInput"
              type="file"
              accept="image/*"
              @change="handleLogoSelect"
              class="hidden"
            />
            <button
              @click="$refs.logoInput.click()"
              class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors flex items-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
              </svg>
              选择图片
            </button>
            <span v-if="selectedLogo" class="text-sm text-text-secondary">
              {{ selectedLogo.name }}
            </span>
          </div>
          <p class="text-xs text-text-secondary mt-2">支持 PNG、JPG、GIF、WebP 格式，建议尺寸 200x200 像素</p>
        </div>

        <!-- 上传进度 -->
        <div v-if="uploading" class="mb-4">
          <div class="flex items-center gap-3">
            <div class="animate-spin w-5 h-5 border-2 border-primary border-t-transparent rounded-full"></div>
            <span class="text-sm">上传中...</span>
          </div>
        </div>

        <!-- 已有 Logo 显示 -->
        <div v-if="settings.logo_url" class="p-4 bg-background rounded-lg border border-border">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <img :src="settings.logo_url" alt="Logo" class="w-12 h-12 object-contain" />
              <div>
                <p class="text-sm font-medium">已上传 Logo 图片</p>
                <p class="text-xs text-text-secondary">{{ settings.logo_url }}</p>
              </div>
            </div>
            <button
              @click="useDefaultLogo"
              class="text-sm text-red-500 hover:text-red-600"
            >
              恢复默认
            </button>
          </div>
        </div>
      </div>

      <!-- 网站名称 -->
      <div class="mb-6">
        <label class="block text-sm font-medium mb-2">网站名称</label>
        <input
          v-model="siteName"
          type="text"
          placeholder="输入网站名称"
          class="w-full px-4 py-3 rounded-lg border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
        />
      </div>

      <!-- 功能模块设置 -->
      <div class="mb-8">
        <h2 class="text-lg font-medium mb-4">功能模块</h2>
        <div class="space-y-4">
          <!-- 咨询模块开关 -->
          <div class="flex items-center justify-between p-4 bg-background rounded-lg border border-border">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                <svg class="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
                </svg>
              </div>
              <div>
                <p class="font-medium text-sm">立即咨询</p>
                <p class="text-xs text-text-secondary">控制产品页和首页的「立即咨询」按钮与弹窗显示</p>
              </div>
            </div>
            <!-- Toggle Switch -->
            <button
              @click="toggleConsult"
              :class="[
                'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                consultEnabled ? 'bg-primary' : 'bg-gray-300'
              ]"
            >
              <span
                :class="[
                  'inline-block h-4 w-4 transform rounded-full bg-white transition-transform shadow',
                  consultEnabled ? 'translate-x-6' : 'translate-x-1'
                ]"
              />
            </button>
          </div>
        </div>
      </div>

      <!-- 保存按钮 -->
      <div class="flex justify-end gap-3">
        <button
          @click="resetForm"
          class="px-6 py-2.5 border border-border rounded-lg hover:bg-secondary/30 transition-colors"
        >
          重置
        </button>
        <button
          @click="saveSettings"
          :disabled="saving"
          class="px-6 py-2.5 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors disabled:opacity-50 flex items-center gap-2"
        >
          <div v-if="saving" class="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full"></div>
          {{ saving ? '保存中...' : '保存设置' }}
        </button>
      </div>
    </div>

    <!-- 图片裁切弹窗 -->
    <ImageCropper
      :visible="showCropper"
      :imageUrl="cropperImageUrl"
      @close="closeCropper"
      @crop="handleCropped"
    />
  </AdminLayout>
</template>

<script setup>
import AdminLayout from './AdminLayout.vue'
import ImageCropper from '@/components/ImageCropper.vue'
import { ref, computed, onMounted } from 'vue'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000'

// Simple toast function
function showToast(message, type = 'success') {
  const toast = document.createElement('div')
  toast.className = `fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg z-[9999] ${
    type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
  }`
  toast.textContent = message
  document.body.appendChild(toast)
  setTimeout(() => toast.remove(), 3000)
}

const settings = ref({
  site_name: '',
  logo_url: '',
  logo_svg: '',
  consult_enabled: '1'
})

const siteName = ref('')
const consultEnabled = ref(true)
const selectedLogo = ref(null)
const uploading = ref(false)
const saving = ref(false)

// Cropper state
const showCropper = ref(false)
const cropperImageUrl = ref('')

const defaultLogoSvg = '<svg viewBox="0 0 32 32" fill="none"><circle cx="16" cy="16" r="14" stroke="#2D5A47" stroke-width="2"/><path d="M16 8 C12 12, 10 16, 16 24 C22 16, 20 12, 16 8" fill="#2D5A47"/></svg>'

const currentLogoSvg = computed(() => {
  return settings.value.logo_svg || defaultLogoSvg
})

async function fetchSettings() {
  try {
    const res = await fetch(`${API_BASE}/api/settings`)
    const data = await res.json()
    settings.value = data.data || {}
    siteName.value = settings.value.site_name || ''
    consultEnabled.value = settings.value.consult_enabled !== '0'
  } catch (err) {
    console.error('Failed to fetch settings:', err)
  }
}

function handleLogoSelect(event) {
  const file = event.target.files[0]
  if (file) {
    // 创建本地预览 URL
    const reader = new FileReader()
    reader.onload = (e) => {
      cropperImageUrl.value = e.target.result
      showCropper.value = true
      selectedLogo.value = file
    }
    reader.readAsDataURL(file)
  }
  // 清空 input，允许重复选择同一文件
  event.target.value = ''
}

function closeCropper() {
  showCropper.value = false
  cropperImageUrl.value = ''
  selectedLogo.value = null
}

function handleCropped(croppedFile) {
  uploadLogo(croppedFile)
}

async function uploadLogo(file) {
  uploading.value = true
  showCropper.value = false
  
  try {
    const token = localStorage.getItem('admin_token')
    const formData = new FormData()
    formData.append('logo', file)
    
    const res = await fetch(`${API_BASE}/api/settings/logo`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    })
    
    const data = await res.json()
    
    if (res.ok) {
      settings.value.logo_url = data.url
      showToast('Logo 上传成功')
      selectedLogo.value = null
      cropperImageUrl.value = ''
    } else {
      showToast(data.message || '上传失败', 'error')
    }
  } catch (err) {
    console.error('Upload failed:', err)
    showToast('上传失败，请重试', 'error')
  } finally {
    uploading.value = false
  }
}

async function useDefaultLogo() {
  try {
    const token = localStorage.getItem('admin_token')
    const res = await fetch(`${API_BASE}/api/settings/logo_url`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ value: '' })
    })
    
    if (res.ok) {
      settings.value.logo_url = ''
      showToast('已恢复默认 Logo')
    }
  } catch (err) {
    console.error('Failed to reset logo:', err)
  }
}

async function saveSettings() {
  saving.value = true
  
  try {
    const token = localStorage.getItem('admin_token')
    
    const res = await fetch(`${API_BASE}/api/settings/site_name`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ value: siteName.value })
    })
    
    if (res.ok) {
      settings.value.site_name = siteName.value
      showToast('设置保存成功')
    } else {
      showToast('保存失败', 'error')
    }
  } catch (err) {
    console.error('Save failed:', err)
    showToast('保存失败，请重试', 'error')
  } finally {
    saving.value = false
  }
}

async function toggleConsult() {
  const newVal = consultEnabled.value ? '0' : '1'
  try {
    const token = localStorage.getItem('admin_token')
    const res = await fetch(`${API_BASE}/api/settings/consult_enabled`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ value: newVal })
    })
    if (res.ok) {
      consultEnabled.value = newVal === '1'
      showToast(consultEnabled.value ? '咨询模块已开启' : '咨询模块已关闭')
    } else {
      showToast('操作失败', 'error')
    }
  } catch (err) {
    console.error('Toggle consult failed:', err)
    showToast('操作失败', 'error')
  }
}

function resetForm() {
  siteName.value = settings.value.site_name || ''
  selectedLogo.value = null
}

onMounted(() => {
  fetchSettings()
})
</script>

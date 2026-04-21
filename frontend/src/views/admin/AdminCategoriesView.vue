<template>
  <AdminLayout>
    <div>
      <!-- Header -->
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
        <div>
          <h1 class="text-2xl font-medium">分类管理</h1>
          <p class="text-text-secondary mt-1">管理产品分类（拖拽调整顺序）</p>
        </div>
        <button @click="openForm()" class="btn btn-primary flex items-center gap-2 self-start">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          新增分类
        </button>
      </div>

      <!-- Drag Sort Tips -->
      <div class="bg-primary/5 border border-primary/20 rounded-lg p-4 mb-6 flex items-center gap-3">
        <svg class="w-5 h-5 text-primary flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <p class="text-sm text-text-secondary">
          拖动分类卡片左侧的 <span class="font-medium">☰</span> 图标可调整显示顺序，调整后点击<span class="font-medium text-primary"> 保存排序 </span>按钮生效
        </p>
      </div>

      <!-- Categories Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="(category, index) in categories"
          :key="category.id"
          class="bg-surface rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow cursor-move"
          draggable="true"
          @dragstart="onDragStart($event, index)"
          @dragover.prevent="onDragOver($event, index)"
          @dragend="onDragEnd"
          :class="{ 'ring-2 ring-primary ring-offset-2': dragIndex === index }"
        >
          <div class="flex items-start justify-between">
            <div class="flex items-center gap-4">
              <div class="flex items-center gap-2">
                <div class="w-8 h-8 rounded bg-secondary/50 flex items-center justify-center text-text-secondary cursor-grab active:cursor-grabbing">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M8 6h2v2H8V6zm6 0h2v2h-2V6zM8 11h2v2H8v-2zm6 0h2v2h-2v-2zm-6 5h2v2H8v-2zm6 0h2v2h-2v-2z"/>
                  </svg>
                </div>
                <div class="w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center text-2xl">
                  {{ category.icon || '📦' }}
                </div>
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <h3 class="font-medium">{{ category.name }}</h3>
                  <span class="text-xs bg-secondary/50 px-2 py-0.5 rounded-full">#{{ category.sort_order || 0 }}</span>
                </div>
                <p class="text-sm text-text-secondary">
                  {{ category.product_count || 0 }} 个产品
                </p>
              </div>
            </div>
            <div class="flex items-center gap-1">
              <button
                @click="openForm(category)"
                class="p-2 text-text-secondary hover:text-primary transition-colors"
                title="编辑"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                </svg>
              </button>
              <button
                @click="confirmDelete(category)"
                class="p-2 text-text-secondary hover:text-red-500 transition-colors"
                title="删除"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
              </button>
            </div>
          </div>
          <p v-if="category.description" class="text-sm text-text-secondary mt-4">
            {{ category.description }}
          </p>
        </div>
      </div>

      <!-- Save Sort Order Button -->
      <div v-if="sortChanged" class="fixed bottom-6 right-6 z-50">
        <button
          @click="saveSortOrder"
          :disabled="savingOrder"
          class="btn btn-primary shadow-lg flex items-center gap-2"
        >
          <svg v-if="savingOrder" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          {{ savingOrder ? '保存中...' : '保存排序' }}
        </button>
      </div>

      <!-- Empty State -->
      <div v-if="categories.length === 0" class="text-center py-16">
        <svg class="w-16 h-16 mx-auto text-border mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
        </svg>
        <p class="text-text-secondary">暂无分类，点击上方按钮添加</p>
      </div>
    </div>

    <!-- Category Form Modal -->
    <teleport to="body">
      <transition name="modal">
        <div v-if="isFormOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
          <div @click.self="closeForm" class="absolute inset-0 bg-black/50" />
          <div class="relative bg-white rounded-xl shadow-2xl w-full max-w-md">
            <div class="border-b border-border px-6 py-4 flex items-center justify-between">
              <h2 class="text-lg font-medium">{{ editingCategory ? '编辑分类' : '新增分类' }}</h2>
              <button @click="closeForm" class="p-2 hover:bg-secondary/50 rounded">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>

            <form @submit.prevent="handleSubmit" class="p-6 space-y-5">
              <div>
                <label class="block text-sm font-medium mb-2">分类名称 *</label>
                <input
                  v-model="form.name"
                  type="text"
                  placeholder="请输入分类名称"
                  class="w-full px-4 py-3 rounded-lg border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
                  required
                />
              </div>

              <div>
                <label class="block text-sm font-medium mb-2">图标</label>
                <div class="flex gap-3">
                  <div class="w-14 h-14 rounded-lg border-2 border-primary flex items-center justify-center text-2xl bg-secondary/30 flex-shrink-0">
                    {{ form.icon || '📦' }}
                  </div>
                  <div class="flex-1 text-sm text-text-secondary">
                    已选: {{ form.icon || '无' }}
                  </div>
                </div>
                <div class="mt-3 grid grid-cols-10 gap-1">
                  <button
                    v-for="icon in iconOptions"
                    :key="icon"
                    type="button"
                    @click="form.icon = icon"
                    :class="[
                      'w-10 h-10 rounded-lg flex items-center justify-center text-xl transition-all',
                      form.icon === icon 
                        ? 'bg-primary text-white ring-2 ring-primary/50' 
                        : 'bg-secondary/30 hover:bg-secondary/50'
                    ]"
                  >
                    {{ icon }}
                  </button>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium mb-2">描述</label>
                <input
                  v-model="form.description"
                  type="text"
                  placeholder="简短描述分类"
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
                <p class="text-xs text-text-secondary mt-1">设置分类在首页的显示顺序</p>
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
                确定要删除分类 "<span class="font-medium">{{ deletingCategory?.name }}</span>" 吗？
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
import { categoryApi } from '@/api'

const categories = ref([])
const loading = ref(false)

// Drag and sort
const dragIndex = ref(-1)
const sortChanged = ref(false)
const savingOrder = ref(false)

// Drag handlers
function onDragStart(event, index) {
  dragIndex.value = index
  event.dataTransfer.effectAllowed = 'move'
}

function onDragOver(event, index) {
  if (dragIndex.value === -1 || dragIndex.value === index) return
  
  const draggedItem = categories.value[dragIndex.value]
  categories.value.splice(dragIndex.value, 1)
  categories.value.splice(index, 0, draggedItem)
  dragIndex.value = index
  sortChanged.value = true
}

function onDragEnd() {
  dragIndex.value = -1
}

// Save new sort order
async function saveSortOrder() {
  savingOrder.value = true
  try {
    // Update sort_order for all categories based on their new position
    const updates = categories.value.map((cat, index) => ({
      id: cat.id,
      sort_order: index
    }))
    
    // Send update requests
    await Promise.all(
      updates.map(({ id, sort_order }) => 
        categoryApi.update(id, { sort_order })
      )
    )
    
    // Refresh categories
    await fetchCategories()
    sortChanged.value = false
  } catch (err) {
    console.error('Failed to save sort order:', err)
  } finally {
    savingOrder.value = false
  }
}

// 图标选项（100个）
const iconOptions = [
  // 护肤相关
  '🧴', '💧', '🧬', '🌿', '🌸', '✨', '☀️', '🌙', '💎', '🍃',
  '🧽', '💆', '🌺', '🦋', '🌻', '🪷', '🧖', '💄', '🎀', '🎁',
  // 自然元素
  '🌱', '🌲', '🌳', '🌴', '🌵', '🌷', '🌹', '🌼', '🌾', '🌰',
  '🍀', '🍁', '🍂', '🍄', '💐', '🌊', '🔥', '💨', '❄️', '☁️',
  // 水果
  '🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🫐', '🍈',
  '🍒', '🍑', '🍍', '🥝', '🥑', '🥥', '🍅', '🥕', '🌽', '🥦',
  // 美丽时尚
  '💅', '💇', '💈', '👑', '👒', '🎩', '🎓', '🧢', '👜', '👛',
  '👝', '🎒', '👞', '👟', '🥾', '🥿', '👠', '👡', '🩰', '👢',
  // 星星月亮
  '⭐', '🌟', '✨', '⚡', '🔥', '💥', '☄️', '☀️', '🌤️', '⛅',
  '🌥️', '☁️', '🌦️', '🌧️', '⛈️', '🌩️', '🌨️', '❄️', '🌬️', '💨',
  // 爱心
  '❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎', '💗',
  '💓', '💕', '💖', '💞', '💘', '💝', '💟', '♥️', '💌', '💋'
]

// Form state
const isFormOpen = ref(false)
const editingCategory = ref(null)
const submitting = ref(false)
const form = ref({
  name: '',
  icon: '',
  description: '',
  sort_order: 0
})

// Fetch categories from API
async function fetchCategories() {
  loading.value = true
  try {
    const res = await categoryApi.getList()
    categories.value = res.data || []
  } catch (err) {
    console.error('Failed to fetch categories:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCategories()
})

function openForm(category = null) {
  if (category) {
    editingCategory.value = category
    form.value = { ...category }
  } else {
    editingCategory.value = null
    form.value = {
      name: '',
      icon: '',
      description: '',
      sort_order: 0
    }
  }
  isFormOpen.value = true
}

function closeForm() {
  isFormOpen.value = false
  editingCategory.value = null
}

async function handleSubmit() {
  submitting.value = true
  try {
    if (editingCategory.value) {
      await categoryApi.update(editingCategory.value.id, form.value)
    } else {
      await categoryApi.create(form.value)
    }
    await fetchCategories()
    closeForm()
    sortChanged.value = false
  } catch (err) {
    console.error('Failed to save category:', err)
  } finally {
    submitting.value = false
  }
}

// Delete state
const isDeleteModalOpen = ref(false)
const deletingCategory = ref(null)
const deleting = ref(false)

function confirmDelete(category) {
  deletingCategory.value = category
  isDeleteModalOpen.value = true
}

async function handleDelete() {
  if (!deletingCategory.value) return
  deleting.value = true
  try {
    await categoryApi.delete(deletingCategory.value.id)
    await fetchCategories()
    isDeleteModalOpen.value = false
    deletingCategory.value = null
  } catch (err) {
    console.error('Failed to delete category:', err)
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

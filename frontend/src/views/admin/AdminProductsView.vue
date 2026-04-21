<template>
  <AdminLayout>
    <div>
      <!-- Header -->
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
        <div>
          <h1 class="text-2xl font-medium">产品管理</h1>
          <p class="text-text-secondary mt-1">管理您的产品列表</p>
        </div>
        <div class="flex items-center gap-3 self-start">
          <!-- 批量删除按钮，选中后显示 -->
          <button
            v-if="selectedIds.size > 0"
            @click="confirmBatchDelete"
            class="btn flex items-center gap-2 bg-red-50 text-red-600 border border-red-200 hover:bg-red-100 transition-colors px-4 py-2 rounded-lg text-sm font-medium"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
            删除选中 ({{ selectedIds.size }})
          </button>
          <button @click="openForm()" class="btn btn-primary flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            新增产品
          </button>
        </div>
      </div>

      <!-- Products Table -->
      <div class="bg-surface rounded-xl shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-secondary/30">
              <tr>
                <th class="px-4 py-4 w-10">
                  <input
                    type="checkbox"
                    :checked="isAllSelected"
                    :indeterminate="isIndeterminate"
                    @change="toggleSelectAll"
                    class="w-4 h-4 rounded border-border text-primary cursor-pointer accent-primary"
                  />
                </th>
                <th class="px-6 py-4 text-left text-sm font-medium text-text-secondary">产品</th>
                <th class="px-6 py-4 text-left text-sm font-medium text-text-secondary">分类</th>
                <th class="px-6 py-4 text-left text-sm font-medium text-text-secondary">规格</th>
                <th class="px-6 py-4 text-left text-sm font-medium text-text-secondary">状态</th>
                <th class="px-6 py-4 text-right text-sm font-medium text-text-secondary">操作</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-border">
              <tr v-for="product in paginatedProducts" :key="product.id" 
                :class="['hover:bg-secondary/20 transition-colors', selectedIds.has(product.id) ? 'bg-primary/5' : '']">
                <td class="px-4 py-4">
                  <input
                    type="checkbox"
                    :checked="selectedIds.has(product.id)"
                    @change="toggleSelect(product.id)"
                    class="w-4 h-4 rounded border-border cursor-pointer accent-primary"
                  />
                </td>
                <td class="px-6 py-4">
                  <div class="flex items-center gap-4">
                    <div class="w-12 h-12 rounded-lg bg-secondary/50 overflow-hidden flex-shrink-0">
                      <img v-if="product.image_url" :src="product.image_url" :alt="product.name" class="w-full h-full object-cover" />
                      <div v-else class="w-full h-full flex items-center justify-center">
                        <svg class="w-6 h-6 text-border" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                        </svg>
                      </div>
                    </div>
                    <div>
                      <p class="font-medium">{{ product.name }}</p>
                      <p class="text-sm text-text-secondary truncate max-w-xs">{{ product.description }}</p>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 text-text-secondary">
                  {{ getCategoryName(product.category_id) }}
                </td>
                <td class="px-6 py-4 text-text-secondary">
                  {{ product.specs || '-' }}
                </td>
                <td class="px-6 py-4">
                  <span
                    :class="[
                      'px-3 py-1 text-xs font-medium rounded-full',
                      product.status === 'enabled' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'
                    ]"
                  >
                    {{ product.status === 'enabled' ? '启用' : '禁用' }}
                  </span>
                </td>
                <td class="px-6 py-4 text-right">
                  <div class="flex items-center justify-end gap-2">
                    <button
                      @click="openForm(product)"
                      class="p-2 text-text-secondary hover:text-primary transition-colors"
                      title="编辑"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                      </svg>
                    </button>
                    <button
                      @click="confirmDelete(product)"
                      class="p-2 text-text-secondary hover:text-red-500 transition-colors"
                      title="删除"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Empty State -->
        <div v-if="totalProducts === 0 && !loading" class="text-center py-16">
          <svg class="w-16 h-16 mx-auto text-border mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
          </svg>
          <p class="text-text-secondary">暂无产品，点击上方按钮添加</p>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="px-6 py-4 bg-secondary/20 flex items-center justify-between">
          <p class="text-sm text-text-secondary">
            共 {{ totalProducts }} 条，第 {{ currentPage }} / {{ totalPages }} 页
          </p>
          <div class="flex items-center gap-2">
            <button
              @click="currentPage = 1"
              :disabled="currentPage === 1"
              class="px-3 py-1.5 text-sm rounded-lg border border-border hover:bg-surface disabled:opacity-50 disabled:cursor-not-allowed"
            >
              首页
            </button>
            <button
              @click="currentPage--"
              :disabled="currentPage === 1"
              class="px-3 py-1.5 text-sm rounded-lg border border-border hover:bg-surface disabled:opacity-50 disabled:cursor-not-allowed"
            >
              上一页
            </button>
            <div class="flex items-center gap-1">
              <button
                v-for="page in visiblePages"
                :key="page"
                @click="currentPage = page"
                :class="[
                  'w-9 h-9 text-sm rounded-lg border',
                  currentPage === page
                    ? 'bg-primary text-white border-primary'
                    : 'border-border hover:bg-surface'
                ]"
              >
                {{ page }}
              </button>
            </div>
            <button
              @click="currentPage++"
              :disabled="currentPage === totalPages"
              class="px-3 py-1.5 text-sm rounded-lg border border-border hover:bg-surface disabled:opacity-50 disabled:cursor-not-allowed"
            >
              下一页
            </button>
            <button
              @click="currentPage = totalPages"
              :disabled="currentPage === totalPages"
              class="px-3 py-1.5 text-sm rounded-lg border border-border hover:bg-surface disabled:opacity-50 disabled:cursor-not-allowed"
            >
              末页
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Product Form Modal -->
    <teleport to="body">
      <transition name="modal">
        <div v-if="isFormOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
          <div @click.self="closeForm" class="absolute inset-0 bg-black/50" />
          <div class="relative bg-white rounded-xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div class="sticky top-0 bg-white border-b border-border px-6 py-4 flex items-center justify-between">
              <h2 class="text-lg font-medium">{{ editingProduct ? '编辑产品' : '新增产品' }}</h2>
              <button @click="closeForm" class="p-2 hover:bg-secondary/50 rounded">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>

            <form @submit.prevent="handleSubmit" class="p-6 space-y-5">
              <div>
                <label class="block text-sm font-medium mb-2">产品名称 *</label>
                <input
                  v-model="form.name"
                  type="text"
                  placeholder="请输入产品名称"
                  class="w-full px-4 py-3 rounded-lg border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
                  required
                />
              </div>

              <div class="grid grid-cols-3 gap-4">
                <div>
                  <label class="block text-sm font-medium mb-2">产品分类 *</label>
                  <select
                    v-model="form.category_id"
                    class="w-full px-4 py-3 rounded-lg border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
                    required
                  >
                    <option value="">选择分类</option>
                    <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                      {{ cat.name }}
                    </option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium mb-2">规格</label>
                  <div class="flex gap-2">
                    <input
                      v-model="specsNumber"
                      type="number"
                      min="0"
                      placeholder="数量"
                      class="w-full min-w-[120px] px-4 py-3 rounded-lg border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
                    />
                    <div class="flex rounded-lg border border-border overflow-hidden shrink-0">
                      <button
                        type="button"
                        v-for="unit in ['g', 'ml', '颗', '瓶', '袋']"
                        :key="unit"
                        @click="specsUnit = unit"
                        :class="[
                          'px-4 py-3 text-sm font-medium transition-colors',
                          specsUnit === unit
                            ? 'bg-primary text-white'
                            : 'bg-white text-text-secondary hover:bg-secondary/30'
                        ]"
                      >
                        {{ unit }}
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium mb-2">产品图片 <span class="text-text-secondary text-xs font-normal">（最多5张，拖拽调整顺序，第1张为主图）</span></label>
                <div class="flex gap-3 flex-wrap">
                  <!-- 图片槽位：最多5个，支持拖拽 -->
                  <div
                    v-for="(slot, idx) in 5"
                    :key="idx"
                    class="relative cursor-move"
                    draggable="true"
                    @dragstart="onDragStart(idx)"
                    @dragover.prevent="onDragOver(idx)"
                    @drop="onDrop(idx)"
                    @dragend="onDragEnd"
                  >
                    <div
                      v-if="formImages[idx]"
                      class="w-28 h-28 rounded-lg overflow-hidden border-2 border-border relative group transition-all"
                      :class="{ 'border-primary ring-2 ring-primary/20': draggedIndex === idx }"
                    >
                      <img :src="formImages[idx]" class="w-full h-full object-cover" />
                      <div class="absolute inset-0 bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
                        <button type="button" @click.stop="removeImage(idx)" class="w-7 h-7 bg-red-500 text-white rounded-full flex items-center justify-center">
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                        </button>
                      </div>
                      <span v-if="idx === 0" class="absolute bottom-0 left-0 right-0 text-center text-xs bg-black/50 text-white py-0.5">主图</span>
                      <span class="absolute top-1 right-1 w-5 h-5 bg-black/50 text-white text-xs rounded-full flex items-center justify-center">{{ idx + 1 }}</span>
                    </div>
                    <div
                      v-else
                      class="w-28 h-28 rounded-lg border-2 border-dashed border-border hover:border-primary/50 transition-colors cursor-pointer flex flex-col items-center justify-center gap-1"
                      @click="triggerFileInput(idx)"
                    >
                      <svg class="w-8 h-8 text-border" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4v16m8-8H4"/></svg>
                      <span class="text-xs text-text-secondary">{{ idx === 0 ? '主图' : `附图${idx + 1}` }}</span>
                    </div>
                  </div>
                </div>
                <input ref="fileInput" type="file" accept="image/*" multiple class="hidden" @change="handleFileChange" />
              </div>

              <div>
                <label class="block text-sm font-medium mb-2">产品描述</label>
                <textarea
                  v-model="form.description"
                  rows="3"
                  placeholder="请输入产品描述"
                  class="w-full px-4 py-3 rounded-lg border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none resize-none"
                />
              </div>

              <div>
                <label class="block text-sm font-medium mb-2">详情图片 <span class="text-text-secondary text-xs font-normal">（最多4张，16:9 比例，最宽 1660px，自动压缩至800KB以内）</span></label>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div
                    v-for="(slot, idx) in 4"
                    :key="idx"
                    class="relative"
                  >
                    <!-- 已有图片 -->
                    <div
                      v-if="formDetailImages[idx]"
                      class="aspect-video rounded-lg overflow-hidden border-2 border-border relative group cursor-pointer"
                      @click="removeDetailImage(idx)"
                    >
                      <img :src="formDetailImages[idx]" class="w-full h-full object-cover" />
                      <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                        <span class="text-white text-sm">点击删除</span>
                      </div>
                      <span class="absolute top-1 left-1 px-2 py-0.5 bg-black/50 text-white text-xs rounded">{{ idx + 1 }}</span>
                    </div>
                    <!-- 上传按钮 -->
                    <div
                      v-else
                      class="aspect-video rounded-lg border-2 border-dashed border-border hover:border-primary/50 transition-colors cursor-pointer flex flex-col items-center justify-center gap-2 bg-secondary/20"
                      @click="triggerDetailFileInput(idx)"
                    >
                      <svg class="w-8 h-8 text-text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                      </svg>
                      <span class="text-xs text-text-secondary">{{ idx === 0 ? '上传第1张' : `图片${idx + 1}` }}</span>
                      <span class="text-xs text-text-secondary/60">16:9</span>
                    </div>
                  </div>
                </div>
                <input ref="detailFileInput" type="file" accept="image/*" multiple class="hidden" @change="handleDetailFileChange" />
              </div>

              <div>
                <label class="block text-sm font-medium mb-2">主要成分</label>
                <input
                  v-model="form.ingredients"
                  type="text"
                  placeholder="请输入主要成分，多个成分用逗号分隔"
                  class="w-full px-4 py-3 rounded-lg border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
                />
              </div>

              <div>
                <label class="block text-sm font-medium mb-2">核心功效</label>
                <input
                  v-model="form.benefits"
                  type="text"
                  placeholder="请输入核心功效，多个功效用竖线分隔，如: 保湿|美白|抗老"
                  class="w-full px-4 py-3 rounded-lg border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none"
                />
              </div>

              <div>
                <label class="block text-sm font-medium mb-2">状态</label>
                <div class="flex gap-4">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input
                      v-model="form.status"
                      type="radio"
                      value="enabled"
                      class="w-4 h-4 text-primary"
                    />
                    <span>启用</span>
                  </label>
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input
                      v-model="form.status"
                      type="radio"
                      value="disabled"
                      class="w-4 h-4 text-primary"
                    />
                    <span>禁用</span>
                  </label>
                </div>
              </div>

              <div class="flex gap-3 pt-4">
                <button type="button" @click="closeForm" class="flex-1 btn btn-secondary">
                  取消
                </button>
                <button type="submit" :disabled="submitting" class="flex-1 btn btn-primary disabled:opacity-50 flex items-center justify-center gap-2">
                  <svg v-if="submitting" class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
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
                确定要删除产品 "<span class="font-medium">{{ deletingProduct?.name }}</span>" 吗？此操作不可撤销。
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

    <!-- Batch Delete Confirmation Modal -->
    <teleport to="body">
      <transition name="modal">
        <div v-if="isBatchDeleteModalOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
          <div @click.self="isBatchDeleteModalOpen = false" class="absolute inset-0 bg-black/50" />
          <div class="relative bg-white rounded-xl shadow-2xl w-full max-w-md p-6">
            <div class="text-center">
              <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-red-100 flex items-center justify-center">
                <svg class="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                </svg>
              </div>
              <h3 class="text-lg font-medium mb-2">批量删除确认</h3>
              <p class="text-text-secondary mb-6">
                确定要删除选中的 <span class="font-medium text-red-500">{{ selectedIds.size }}</span> 个产品吗？此操作不可撤销。
              </p>
              <div class="flex gap-3">
                <button @click="isBatchDeleteModalOpen = false" class="flex-1 btn btn-secondary">
                  取消
                </button>
                <button @click="handleBatchDelete" :disabled="batchDeleting" class="flex-1 bg-red-500 text-white hover:bg-red-600 btn disabled:opacity-50">
                  {{ batchDeleting ? '删除中...' : `删除 ${selectedIds.size} 个` }}
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
import { ref, computed, onMounted, watch } from 'vue'
import AdminLayout from './AdminLayout.vue'
import { useProductStore } from '@/stores/product'
import { categoryApi, uploadApi } from '@/api'

const productStore = useProductStore()

const products = computed(() => productStore.products)
const loading = computed(() => productStore.loading)

const categories = ref([])

// Pagination
const currentPage = ref(1)
const pageSize = ref(10)

const totalProducts = computed(() => products.value.length)
const totalPages = computed(() => Math.ceil(totalProducts.value / pageSize.value))

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return products.value.slice(start, end)
})

const visiblePages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = currentPage.value
  let start = Math.max(1, current - 2)
  let end = Math.min(total, start + 5)
  if (end - start < 5) {
    start = Math.max(1, end - 5)
  }
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

async function fetchCategories() {
  try {
    const res = await categoryApi.getList()
    categories.value = res.data || []
  } catch (err) {
    console.error('Failed to fetch categories:', err)
  }
}

function getCategoryName(categoryId) {
  const category = categories.value.find(c => c.id === categoryId)
  return category?.name || '-'
}

// Form state
const isFormOpen = ref(false)
const editingProduct = ref(null)
const submitting = ref(false)
const form = ref({
  name: '',
  category_id: '',
  specs: '',
  image_url: '',
  description: '',
  detail_description: '',
  ingredients: '',
  benefits: '',
  status: 'enabled'
})
const fileInput = ref(null)
const specsNumber = ref('')
const specsUnit = ref('g')

// 数字/单位 → form.specs
watch([specsNumber, specsUnit], ([num, unit]) => {
  form.value.specs = num ? `${num}${unit}` : ''
})
const currentSlotIndex = ref(0) // 当前点击的图片槽位
const formImages = ref(['', '', '', '', '']) // 最多5张图
// 拖拽排序
const draggedIndex = ref(null)

// 详情图片
const detailFileInput = ref(null)
const currentDetailSlotIndex = ref(0)
const formDetailImages = ref(['', '', '', '']) // 最多4张详情图

function openForm(product = null) {
  if (product) {
    editingProduct.value = product
    form.value = { ...product }
    // 解析 specs → specsNumber + specsUnit
    const specsStr = product.specs || ''
    const match = specsStr.match(/^(\d+\.?\d*)(g|ml|颗|瓶|袋)$/i)
    if (match) {
      specsNumber.value = match[1]
      specsUnit.value = match[2]
    } else {
      specsNumber.value = specsStr.replace(/[^\d.]/g, '')
      if (specsStr.includes('ml')) specsUnit.value = 'ml'
      else if (specsStr.includes('颗')) specsUnit.value = '颗'
      else if (specsStr.includes('瓶')) specsUnit.value = '瓶'
      else if (specsStr.includes('袋')) specsUnit.value = '袋'
      else specsUnit.value = 'g'
    }
    // 解析 gallery 字段填充 formImages: [主图, 附图1, 附图2]
    let gallery = []
    if (product.gallery) {
      if (Array.isArray(product.gallery)) {
        gallery = product.gallery
      } else if (typeof product.gallery === 'string') {
        try { gallery = JSON.parse(product.gallery) } catch { gallery = [] }
      }
    }
    // 过滤掉无效图片（空值、base64 blob URL）
    const validImage = (url) => url && !url.startsWith('blob:')
    formImages.value = [
      validImage(product.image_url) ? product.image_url : '',
      ...gallery.slice(0, 4).map(g => validImage(g) ? g : '')
    ]
    // 详情图片
    let detailImages = []
    if (product.detail_images) {
      if (Array.isArray(product.detail_images)) {
        detailImages = product.detail_images
      } else if (typeof product.detail_images === 'string') {
        try { detailImages = JSON.parse(product.detail_images) } catch { detailImages = [] }
      }
    }
    formDetailImages.value = [
      validImage(detailImages[0]) ? detailImages[0] : '',
      validImage(detailImages[1]) ? detailImages[1] : '',
      validImage(detailImages[2]) ? detailImages[2] : '',
      validImage(detailImages[3]) ? detailImages[3] : ''
    ]
  } else {
    editingProduct.value = null
    specsNumber.value = ''
    specsUnit.value = 'g'
    form.value = {
      name: '',
      category_id: '',
      specs: '',
      image_url: '',
      description: '',
      detail_description: '',
      ingredients: '',
      benefits: '',
      status: 'enabled'
    }
    formImages.value = ['', '', '', '', '']
    formDetailImages.value = ['', '', '', '']
  }
  isFormOpen.value = true
}

function closeForm() {
  isFormOpen.value = false
  editingProduct.value = null
}

function triggerFileInput(idx) {
  currentSlotIndex.value = idx
  fileInput.value?.click()
}

async function handleFileChange(event) {
  const files = Array.from(event.target.files)
  if (!files.length) return

  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/bmp']
  const maxSlots = 5

  // 从当前点击槽位开始，依次填入
  let slotIdx = currentSlotIndex.value

  for (const file of files) {
    // 跳过已有图片的槽位，找下一个空槽（或当前槽直接覆盖）
    while (slotIdx < maxSlots && formImages.value[slotIdx] && slotIdx !== currentSlotIndex.value) {
      slotIdx++
    }
    if (slotIdx >= maxSlots) break

    if (!allowedTypes.includes(file.type)) {
      alert(`${file.name} 格式不支持，请选择 JPG、PNG、GIF 或 WebP`)
      slotIdx++
      continue
    }

    const idx = slotIdx
    // 本地预览
    const previewUrl = URL.createObjectURL(file)
    formImages.value[idx] = previewUrl
    if (idx === 0) form.value.image_url = previewUrl

    try {
      const res = await uploadApi.upload(file)
      const serverUrl = res.url || res.data?.url || (res.data && res.data.url)
      if (serverUrl) {
        formImages.value[idx] = serverUrl
        if (idx === 0) form.value.image_url = serverUrl
      }
    } catch (err) {
      console.error('Upload failed:', err)
      if (err.response?.status === 401) {
        alert('请先登录后再上传图片')
        localStorage.removeItem('admin_token')
        window.location.href = '/admin'
        break
      } else {
        alert('上传失败: ' + (err.response?.data?.message || err.message || '请重试'))
      }
    }

    slotIdx++
  }

  event.target.value = ''
}

function removeImage(idx) {
  formImages.value[idx] = ''
  if (idx === 0) form.value.image_url = ''
}

// 拖拽排序
function onDragStart(idx) {
  draggedIndex.value = idx
}
function onDragOver(idx) {
  // 可选：显示放置预览
}
function onDrop(idx) {
  if (draggedIndex.value === null || draggedIndex.value === idx) return
  const images = [...formImages.value]
  const [dragged] = images.splice(draggedIndex.value, 1)
  images.splice(idx, 0, dragged)
  formImages.value = images
  draggedIndex.value = null
}
function onDragEnd() {
  draggedIndex.value = null
}

// 详情图片上传
function triggerDetailFileInput(idx) {
  currentDetailSlotIndex.value = idx
  detailFileInput.value.click()
}

// 压缩图片到指定大小
function compressImage(file, maxWidth = 1660, maxHeight = 934, maxSizeKB = 800) {
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      const img = new Image()
      img.onload = () => {
        // 计算缩放后的尺寸
        let width = img.width
        let height = img.height
        if (width > maxWidth || height > maxHeight) {
          const ratio = Math.min(maxWidth / width, maxHeight / height)
          width = Math.round(width * ratio)
          height = Math.round(height * ratio)
        }

        const canvas = document.createElement('canvas')
        canvas.width = width
        canvas.height = height
        const ctx = canvas.getContext('2d')
        ctx.drawImage(img, 0, 0, width, height)

        // 逐步降低质量直到小于 maxSizeKB
        let quality = 0.9
        let dataUrl = canvas.toDataURL('image/jpeg', quality)

        while (dataUrl.length > maxSizeKB * 1024 * 1.37 && quality > 0.1) {
          quality -= 0.1
          dataUrl = canvas.toDataURL('image/jpeg', quality)
        }

        resolve(dataUrl)
      }
      img.src = e.target.result
    }
    reader.readAsDataURL(file)
  })
}

async function handleDetailFileChange(e) {
  const files = Array.from(e.target.files)
  if (!files.length) return

  const maxSlots = 4

  // 从当前点击槽位开始，依次找空槽填入
  let slotIdx = currentDetailSlotIndex.value

  for (const file of files) {
    // 找空槽（当前槽可直接覆盖，之后找空的）
    while (slotIdx < maxSlots && formDetailImages.value[slotIdx] && slotIdx !== currentDetailSlotIndex.value) {
      slotIdx++
    }
    if (slotIdx >= maxSlots) break

    const idx = slotIdx

    try {
      // 压缩预览
      const previewUrl = await compressImage(file, 1660, 934, 800)
      formDetailImages.value[idx] = previewUrl

      // 上传到服务器
      try {
        const res = await uploadApi.upload(file)
        const serverUrl = res.url || res.data?.url || (res.data && res.data.url)
        if (serverUrl) {
          formDetailImages.value[idx] = serverUrl
        }
      } catch (err) {
        console.error('Detail image upload failed:', err)
      }
    } catch (err) {
      console.error('图片处理失败:', err)
    }

    slotIdx++
  }

  e.target.value = ''
}

function removeDetailImage(idx) {
  formDetailImages.value[idx] = ''
}

async function handleSubmit() {
  let submitTimer = null
  submitTimer = setTimeout(() => { submitting.value = true }, 500)
  try {
    // 主图为第1张，gallery 存第2-5张（去重去空）
    const mainImage = formImages.value[0] || ''
    const extras = formImages.value.slice(1).filter(Boolean)
    form.value.image_url = mainImage
    form.value.gallery = JSON.stringify(extras)
    // 详情图片（过滤空值和 blob URL）
    const detailImages = formDetailImages.value.filter(url => url && !url.startsWith('blob:'))
    form.value.detail_images = JSON.stringify(detailImages)

    if (editingProduct.value) {
      await productStore.updateProduct(editingProduct.value.id, form.value)
    } else {
      await productStore.createProduct(form.value)
      currentPage.value = 1
    }
    closeForm()
  } catch (err) {
    console.error('Failed to save product:', err)
  } finally {
    clearTimeout(submitTimer)
    submitting.value = false
  }
}

// Delete state
const isDeleteModalOpen = ref(false)
const deletingProduct = ref(null)
const deleting = ref(false)

function confirmDelete(product) {
  deletingProduct.value = product
  isDeleteModalOpen.value = true
}

async function handleDelete() {
  if (!deletingProduct.value) return
  deleting.value = true
  try {
    await productStore.deleteProduct(deletingProduct.value.id)
    isDeleteModalOpen.value = false
    deletingProduct.value = null
    // Reset to first page if current page becomes empty
    if (paginatedProducts.value.length === 0 && currentPage.value > 1) {
      currentPage.value--
    }
  } catch (err) {
    console.error('Failed to delete product:', err)
  } finally {
    deleting.value = false
  }
}

// ---- 多选批量删除 ----
const selectedIds = ref(new Set())

const isAllSelected = computed(() =>
  paginatedProducts.value.length > 0 &&
  paginatedProducts.value.every(p => selectedIds.value.has(p.id))
)

const isIndeterminate = computed(() =>
  paginatedProducts.value.some(p => selectedIds.value.has(p.id)) && !isAllSelected.value
)

function toggleSelect(id) {
  const s = new Set(selectedIds.value)
  s.has(id) ? s.delete(id) : s.add(id)
  selectedIds.value = s
}

function toggleSelectAll(e) {
  const s = new Set(selectedIds.value)
  if (e.target.checked) {
    paginatedProducts.value.forEach(p => s.add(p.id))
  } else {
    paginatedProducts.value.forEach(p => s.delete(p.id))
  }
  selectedIds.value = s
}

const isBatchDeleteModalOpen = ref(false)
const batchDeleting = ref(false)

function confirmBatchDelete() {
  isBatchDeleteModalOpen.value = true
}

async function handleBatchDelete() {
  batchDeleting.value = true
  try {
    for (const id of selectedIds.value) {
      await productStore.deleteProduct(id)
    }
    selectedIds.value = new Set()
    isBatchDeleteModalOpen.value = false
    if (paginatedProducts.value.length === 0 && currentPage.value > 1) {
      currentPage.value--
    }
  } catch (err) {
    console.error('Batch delete failed:', err)
  } finally {
    batchDeleting.value = false
  }
}

onMounted(async () => {
  currentPage.value = 1
  await Promise.all([
    productStore.fetchProducts(),
    fetchCategories()
  ])
})
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

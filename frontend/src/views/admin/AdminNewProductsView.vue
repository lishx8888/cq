<template>
  <AdminLayout>
    <div>
      <!-- Header -->
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
        <div>
          <h1 class="text-2xl font-medium">首页新品管理</h1>
          <p class="text-text-secondary mt-1">设置首页"新品上市"模块显示的产品（最多4个）</p>
        </div>
        <button 
          @click="saveNewProducts" 
          :disabled="saving || newProductIds.length === 0"
          class="btn btn-primary flex items-center gap-2 self-start disabled:opacity-50"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          {{ saving ? '保存中...' : '保存设置' }}
        </button>
      </div>

      <!-- Selected Products -->
      <div class="mb-8">
        <h3 class="font-medium mb-4">已选新品（{{ newProductIds.length }}/4）</h3>
        <div v-if="newProductIds.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div
            v-for="product in selectedProducts"
            :key="product.id"
            class="bg-surface rounded-xl p-4 shadow-sm relative group"
          >
            <div class="w-20 h-20 rounded-lg overflow-hidden mb-3 bg-secondary/30 flex-shrink-0">
              <img
                v-if="product.image_url"
                :src="product.image_url"
                :alt="product.name"
                class="w-full h-full object-cover"
              />
              <div v-else class="w-full h-full flex items-center justify-center text-3xl">📦</div>
            </div>
            <h4 class="font-medium text-sm truncate">{{ product.name }}</h4>
            <p class="text-xs text-text-secondary mt-1">{{ getCategoryName(product.category_id) }}</p>
            <button
              @click="removeFromNew(product.id)"
              class="absolute top-2 right-2 w-8 h-8 rounded-full bg-red-500 text-white flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
            <div class="absolute top-2 left-2 px-2 py-1 bg-primary text-white text-xs rounded-full">
              新品
            </div>
          </div>
        </div>
        <div v-else class="bg-surface rounded-xl p-8 text-center">
          <svg class="w-12 h-12 mx-auto text-border mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
          </svg>
          <p class="text-text-secondary">暂未设置新品，请从下方选择</p>
        </div>
      </div>

      <!-- All Products -->
      <div>
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-medium">选择产品添加到首页新品</h3>
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索产品..."
              class="pl-10 pr-4 py-2 border border-border rounded-lg bg-surface focus:outline-none focus:ring-2 focus:ring-primary/50 w-64"
            />
            <svg class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </div>
        </div>
        
        <!-- Loading -->
        <div v-if="loading" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
          <div v-for="i in 10" :key="i" class="bg-surface rounded-xl overflow-hidden">
            <div class="aspect-square skeleton" />
            <div class="p-4">
              <div class="h-5 w-3/4 skeleton rounded mb-2" />
              <div class="h-4 w-1/2 skeleton rounded" />
            </div>
          </div>
        </div>

        <!-- Products Grid -->
        <div v-else-if="filteredProducts.length > 0" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
          <div
            v-for="product in filteredProducts"
            :key="product.id"
            :class="[
              'bg-surface rounded-xl p-3 shadow-sm cursor-pointer transition-all',
              newProductIds.includes(product.id) 
                ? 'ring-2 ring-primary' 
                : 'hover:shadow-md'
            ]"
            @click="toggleNewProduct(product)"
          >
            <div class="relative">
              <div class="w-20 h-20 rounded-lg overflow-hidden mb-3 bg-secondary/30 flex-shrink-0">
                <img
                  v-if="product.image_url"
                  :src="product.image_url"
                  :alt="product.name"
                  class="w-full h-full object-cover"
                />
                <div v-else class="w-full h-full flex items-center justify-center text-3xl">📦</div>
              </div>
              <!-- Selected indicator -->
              <div 
                v-if="newProductIds.includes(product.id)"
                class="absolute top-2 right-2 w-6 h-6 rounded-full bg-primary text-white flex items-center justify-center"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
              </div>
              <!-- Disabled indicator when max reached -->
              <div 
                v-else-if="newProductIds.length >= 4"
                class="absolute top-2 right-2 w-6 h-6 rounded-full bg-gray-400 text-white flex items-center justify-center opacity-50"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                </svg>
              </div>
            </div>
            <h4 class="font-medium text-sm truncate">{{ product.name }}</h4>
            <p class="text-xs text-text-secondary mt-1">{{ getCategoryName(product.category_id) }}</p>
          </div>
        </div>

        <!-- Empty Search Result -->
        <div v-else class="bg-surface rounded-xl p-8 text-center">
          <svg class="w-12 h-12 mx-auto text-border mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <p class="text-text-secondary">未找到匹配的产品</p>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AdminLayout from './AdminLayout.vue'
import { productApi, categoryApi } from '@/api'
import { useProductStore } from '@/stores/product'

const productStore = useProductStore()
const products = ref([])
const categories = ref([])
const newProductIds = ref([])
const loading = ref(false)
const saving = ref(false)
const searchQuery = ref('')

const selectedProducts = computed(() => {
  return newProductIds.value
    .map(id => products.value.find(p => p.id === id))
    .filter(Boolean)
})

// Filtered products based on search
const filteredProducts = computed(() => {
  if (!searchQuery.value.trim()) return products.value
  const query = searchQuery.value.toLowerCase().trim()
  return products.value.filter(p => 
    p.name.toLowerCase().includes(query)
  )
})


async function fetchData() {
  loading.value = true
  try {
    await productStore.fetchProducts()
    products.value = productStore.products
    
    // Fetch categories
    try {
      const res = await categoryApi.getList()
      categories.value = res.data || []
    } catch (err) {
      console.error('Failed to fetch categories:', err)
    }
    
    // Fetch current new products
    try {
      const res = await productApi.getNew()
      newProductIds.value = (res.data || []).map(p => p.id)
    } catch (err) {
      console.error('Failed to fetch new products:', err)
    }
  } finally {
    loading.value = false
  }
}

function getCategoryName(categoryId) {
  const category = categories.value.find(c => c.id === categoryId)
  return category?.name || ''
}

function toggleNewProduct(product) {
  const index = newProductIds.value.indexOf(product.id)
  if (index > -1) {
    // Remove
    newProductIds.value.splice(index, 1)
  } else {
    // Add (max 4)
    if (newProductIds.value.length < 4) {
      newProductIds.value.push(product.id)
    }
  }
}

function removeFromNew(productId) {
  const index = newProductIds.value.indexOf(productId)
  if (index > -1) {
    newProductIds.value.splice(index, 1)
  }
}

async function saveNewProducts() {
  if (newProductIds.value.length === 0) return
  
  saving.value = true
  try {
    await productApi.setNew(newProductIds.value)
    alert('设置成功！')
  } catch (err) {
    console.error('Failed to save new products:', err)
    alert('保存失败，请重试')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

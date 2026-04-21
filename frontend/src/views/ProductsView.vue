<template>
  <div class="min-h-screen">
    <NavBar />

    <!-- Page Header -->
    <section class="pt-32 pb-12 bg-surface">
      <div class="container-custom">
        <h1 class="font-serif text-4xl text-center">产品列表</h1>
        <p class="text-text-secondary text-center mt-4">
          发现适合您的护肤方案
        </p>
      </div>
    </section>

    <!-- Search & Filter -->
    <section class="sticky top-[72px] z-40 bg-background border-b border-border py-4">
      <div class="container-custom">
        <!-- Search Bar -->
        <div class="mb-4">
          <div class="relative max-w-md">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索产品..."
              class="w-full h-10 pl-10 pr-10 rounded-full border border-border focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-all text-sm"
            />
            <div class="absolute left-3 top-1/2 -translate-y-1/2 text-text-secondary">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
            </div>
            <button
              v-if="searchQuery"
              @click="searchQuery = ''"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-text-secondary hover:text-text-primary"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>
        
        <!-- Category Filter -->
        <div class="flex flex-wrap items-center gap-3">
          <button
            @click="selectedCategory = null"
            :class="[
              'px-5 py-2 rounded-full text-sm font-medium transition-all duration-300',
              selectedCategory === null
                ? 'bg-primary text-white'
                : 'bg-surface border border-border hover:border-primary hover:text-primary'
            ]"
          >
            全部产品
          </button>
          <button
            v-for="category in categories"
            :key="category.id"
            @click="selectedCategory = category.id"
            :class="[
              'px-5 py-2 rounded-full text-sm font-medium transition-all duration-300',
              selectedCategory === category.id
                ? 'bg-primary text-white'
                : 'bg-surface border border-border hover:border-primary hover:text-primary'
            ]"
          >
            {{ category.name }}
          </button>
        </div>
      </div>
    </section>

    <!-- Products Grid -->
    <section class="section-spacing">
      <div class="container-custom">
        <!-- Loading State -->
        <div v-if="productStore.loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div v-for="i in 8" :key="i" class="bg-surface rounded-lg overflow-hidden">
            <div class="aspect-square skeleton" />
            <div class="p-5">
              <div class="h-6 w-3/4 skeleton rounded mb-3" />
              <div class="h-4 w-1/2 skeleton rounded mb-4" />
              <div class="h-10 skeleton rounded" />
            </div>
          </div>
        </div>

        <!-- Products -->
        <div
          v-else-if="filteredProducts.length > 0"
          class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6"
        >
          <ProductCard
            v-for="product in filteredProducts"
            :key="product.id"
            :product="product"
            :category-name="getCategoryName(product.category_id)"
            :show-consult="isConsultEnabled()"
            @click="goToProduct(product.id)"
            @consult="openConsult"
          />
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-20">
          <svg class="w-20 h-20 mx-auto text-border mb-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
          </svg>
          <h3 class="text-xl font-medium mb-2">暂无产品</h3>
          <p class="text-text-secondary">该分类下暂无产品，敬请期待</p>
        </div>
      </div>
    </section>

    <Footer />

    <!-- Consult Modal -->
    <ConsultModal :is-open="isConsultOpen" @close="isConsultOpen = false" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import Footer from '@/components/Footer.vue'
import ProductCard from '@/components/ProductCard.vue'
import ConsultModal from '@/components/ConsultModal.vue'
import { useProductStore } from '@/stores/product'
import { categoryApi } from '@/api'
import { useSettings } from '@/composables/useSettings'

const router = useRouter()
const route = useRoute()
const productStore = useProductStore()
const { fetchSettings, isConsultEnabled } = useSettings()

const selectedCategory = ref(null)
const searchQuery = ref('')
const isConsultOpen = ref(false)

const categories = ref([])

async function fetchCategories() {
  try {
    const res = await categoryApi.getList()
    categories.value = res.data || []
  } catch (err) {
    console.error('Failed to fetch categories:', err)
  }
}

const filteredProducts = computed(() => {
  let result = productStore.products
  
  // Filter by category
  if (selectedCategory.value) {
    result = result.filter(
      product => product.category_id === selectedCategory.value
    )
  }
  
  // Filter by search query (fuzzy search)
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.trim().toLowerCase()
    result = result.filter(product => {
      const name = product.name.toLowerCase()
      const specs = (product.specs || '').toLowerCase()
      const categoryName = (categories.value.find(c => c.id === product.category_id)?.name || '').toLowerCase()
      
      // Exact match first
      if (name.includes(query) || specs.includes(query) || categoryName.includes(query)) {
        return true
      }
      
      // Fuzzy match: query characters all appear in order (non-contiguous)
      let queryIdx = 0
      const lowerName = name + specs + categoryName
      for (const char of lowerName) {
        if (queryIdx < query.length && char === query[queryIdx]) {
          queryIdx++
        }
      }
      return queryIdx === query.length
    })
  }
  
  return result
})

function getCategoryName(categoryId) {
  const category = categories.value.find(c => c.id === categoryId)
  return category?.name || ''
}

function goToProduct(id) {
  router.push(`/products/${id}`)
}

function openConsult() {
  isConsultOpen.value = true
}

// Handle category from query params
watch(
  () => route.query.category,
  (categoryId) => {
    if (categoryId) {
      selectedCategory.value = parseInt(categoryId)
    } else {
      selectedCategory.value = null
    }
  },
  { immediate: true }
)

// Handle search from query params
watch(
  () => route.query.search,
  (search) => {
    searchQuery.value = search ? decodeURIComponent(search) : ''
  },
  { immediate: true }
)

onMounted(async () => {
  await Promise.all([
    productStore.fetchProducts(),
    fetchCategories(),
    fetchSettings()
  ])
})
</script>

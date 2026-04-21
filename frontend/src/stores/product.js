import { defineStore } from 'pinia'
import { ref } from 'vue'
import { productApi, categoryApi } from '@/api'

export const useProductStore = defineStore('product', () => {
  const products = ref([])
  const categories = ref([])
  const currentProduct = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Get products with optional category filter
  async function fetchProducts(categoryId = null) {
    loading.value = true
    error.value = null
    try {
      const params = categoryId ? { category_id: categoryId } : {}
      const res = await productApi.getList(params)
      products.value = res.data || res
    } catch (err) {
      error.value = err.message
      console.error('Failed to fetch products:', err)
    } finally {
      loading.value = false
    }
  }

  // Get single product
  async function fetchProduct(id) {
    loading.value = true
    error.value = null
    try {
      const res = await productApi.getById(id)
      // res.data for {data: product} or res for direct product
      const product = res?.data ?? res
      currentProduct.value = product
    } catch (err) {
      error.value = err.message
      console.error('Failed to fetch product:', err)
    } finally {
      loading.value = false
    }
  }

  // Get categories
  async function fetchCategories() {
    try {
      const res = await categoryApi.getList()
      categories.value = res.data || res
    } catch (err) {
      console.error('Failed to fetch categories:', err)
    }
  }

  // Create product
  async function createProduct(data) {
    loading.value = true
    try {
      await productApi.create(data)
      await fetchProducts()
      return true
    } catch (err) {
      error.value = err.message
      return false
    } finally {
      loading.value = false
    }
  }

  // Update product
  async function updateProduct(id, data) {
    loading.value = true
    try {
      await productApi.update(id, data)
      await fetchProducts()
      return true
    } catch (err) {
      error.value = err.message
      return false
    } finally {
      loading.value = false
    }
  }

  // Delete product
  async function deleteProduct(id) {
    loading.value = true
    try {
      await productApi.delete(id)
      await fetchProducts()
      return true
    } catch (err) {
      error.value = err.message
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    products,
    categories,
    currentProduct,
    loading,
    error,
    fetchProducts,
    fetchProduct,
    fetchCategories,
    createProduct,
    updateProduct,
    deleteProduct
  }
})

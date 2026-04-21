import { defineStore } from 'pinia'
import { ref } from 'vue'
import { categoryApi } from '@/api'

export const useCategoryStore = defineStore('category', () => {
  const categories = ref([])
  const loading = ref(false)

  async function fetchCategories() {
    loading.value = true
    try {
      const res = await categoryApi.getList()
      categories.value = res.data || res
    } catch (err) {
      console.error('Failed to fetch categories:', err)
    } finally {
      loading.value = false
    }
  }

  async function createCategory(data) {
    try {
      await categoryApi.create(data)
      await fetchCategories()
      return true
    } catch (err) {
      console.error('Failed to create category:', err)
      return false
    }
  }

  async function updateCategory(id, data) {
    try {
      await categoryApi.update(id, data)
      await fetchCategories()
      return true
    } catch (err) {
      console.error('Failed to update category:', err)
      return false
    }
  }

  async function deleteCategory(id) {
    try {
      await categoryApi.delete(id)
      await fetchCategories()
      return true
    } catch (err) {
      console.error('Failed to delete category:', err)
      return false
    }
  }

  return {
    categories,
    loading,
    fetchCategories,
    createCategory,
    updateCategory,
    deleteCategory
  }
})

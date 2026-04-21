<template>
  <div
    class="bg-surface rounded-xl overflow-hidden card-hover cursor-pointer group transform transition-all duration-300 ease-out"
    :class="{ 'hover:-translate-y-2 hover:shadow-2xl': !disableHover }"
    @click="$emit('click')"
  >
    <!-- Product Image -->
    <div class="aspect-square bg-secondary/30 overflow-hidden relative">
      <img
        v-if="product.image_url"
        :src="product.image_url"
        :alt="product.name"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
      />
      <div v-else class="w-full h-full flex items-center justify-center">
        <svg class="w-16 h-16 text-border" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
        </svg>
      </div>
      
      <!-- Category Badge -->
      <span
        v-if="categoryName"
        class="absolute top-3 left-3 px-3 py-1 bg-white/90 backdrop-blur-sm text-xs font-medium text-primary rounded-full"
      >
        {{ categoryName }}
      </span>
      
      <!-- Quick View Overlay -->
      <div class="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-all duration-300 flex items-center justify-center opacity-0 group-hover:opacity-100">
        <span class="bg-white/95 backdrop-blur-sm text-primary px-5 py-2.5 rounded-full font-medium text-sm shadow-lg transform translate-y-4 group-hover:translate-y-0 transition-all duration-300">
          查看详情
        </span>
      </div>
    </div>

    <!-- Product Info -->
    <div class="p-5">
      <h3 class="font-medium text-lg text-text-primary mb-2 line-clamp-1 group-hover:text-primary transition-colors duration-300">
        {{ product.name }}
      </h3>
      
      <p v-if="product.specs" class="text-sm text-text-secondary mb-4">
        规格: {{ product.specs }}
      </p>

      <!-- CTA Button -->
      <button
        v-if="showConsult"
        @click.stop="$emit('consult')"
        class="w-full btn btn-secondary text-sm py-2.5"
      >
        立即咨询
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  product: {
    type: Object,
    required: true
  },
  categoryName: {
    type: String,
    default: ''
  },
  disableHover: {
    type: Boolean,
    default: false
  },
  showConsult: {
    type: Boolean,
    default: true
  }
})

defineEmits(['click', 'consult'])
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

<template>
  <div v-if="visible" class="fixed inset-0 bg-black/70 z-[9999] flex items-center justify-center p-4">
    <div class="bg-surface rounded-xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
      <!-- Header -->
      <div class="flex items-center justify-between p-4 border-b border-border">
        <h3 class="text-lg font-medium">裁切图片</h3>
        <button @click="close" class="p-2 hover:bg-secondary rounded-lg transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Cropper Area -->
      <div class="flex-1 overflow-hidden bg-background p-4">
        <div class="relative max-h-[50vh] mx-auto">
          <img ref="imageRef" :src="imageUrl" class="max-w-full max-h-[50vh] mx-auto" crossorigin="anonymous" />
        </div>
      </div>

      <!-- Aspect Ratio Options -->
      <div class="p-4 border-t border-border">
        <div class="flex items-center gap-4 mb-4">
          <span class="text-sm text-text-secondary">裁切比例：</span>
          <div class="flex gap-2">
            <button
              v-for="ratio in aspectRatios"
              :key="ratio.label"
              @click="setAspectRatio(ratio.value)"
              :class="[
                'px-3 py-1.5 rounded-lg text-sm transition-colors',
                currentAspectLabel === ratio.label 
                  ? 'bg-primary text-white' 
                  : 'bg-secondary hover:bg-secondary/80'
              ]"
            >
              {{ ratio.label }}
            </button>
          </div>
        </div>
        
        <!-- Zoom Controls -->
        <div class="flex items-center gap-4 mb-4">
          <span class="text-sm text-text-secondary">缩放：</span>
          <button @click="zoomOut" class="px-2 py-1 bg-secondary rounded hover:bg-secondary/80">-</button>
          <span class="text-sm w-12 text-center">{{ Math.round(zoom * 100) }}%</span>
          <button @click="zoomIn" class="px-2 py-1 bg-secondary rounded hover:bg-secondary/80">+</button>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex justify-end gap-3 p-4 border-t border-border">
        <button
          @click="close"
          class="px-6 py-2.5 border border-border rounded-lg hover:bg-secondary/30 transition-colors"
        >
          取消
        </button>
        <button
          @click="resetCropper"
          class="px-6 py-2.5 border border-border rounded-lg hover:bg-secondary/30 transition-colors"
        >
          重置
        </button>
        <button
          @click="confirmCrop"
          class="px-6 py-2.5 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors"
        >
          确认裁切
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onUnmounted, nextTick } from 'vue'
import Cropper from 'cropperjs'

const props = defineProps({
  visible: Boolean,
  imageUrl: String
})

const emit = defineEmits(['close', 'crop'])

const imageRef = ref(null)
let cropperInstance = null
const zoom = ref(1)
const currentAspectLabel = ref('1:1')

const aspectRatios = [
  { label: '1:1', value: 1 },
  { label: '4:3', value: 4/3 },
  { label: '16:9', value: 16/9 },
  { label: '自由', value: NaN }
]

function initCropper() {
  if (!imageRef.value) return
  
  // 销毁旧实例
  if (cropperInstance) {
    cropperInstance.destroy()
    cropperInstance = null
  }
  
  // 等待图片加载
  if (imageRef.value.complete && imageRef.value.naturalWidth > 0) {
    createCropperInstance()
  } else {
    imageRef.value.onload = createCropperInstance
  }
}

function createCropperInstance() {
  try {
    cropperInstance = new Cropper(imageRef.value, {
      aspectRatio: 1,
      viewMode: 1,
      dragMode: 'move',
      autoCropArea: 0.8,
      guides: true,
      center: true,
      highlight: false,
      cropBoxMovable: true,
      cropBoxResizable: true,
      toggleDragModeOnDblclick: false
    })
    console.log('Cropper created successfully')
  } catch (err) {
    console.error('Cropper creation failed:', err)
  }
}

function destroyCropper() {
  if (cropperInstance) {
    cropperInstance.destroy()
    cropperInstance = null
  }
}

function setAspectRatio(ratio) {
  const ratioInfo = aspectRatios.find(r => r.value === ratio)
  if (ratioInfo) {
    currentAspectLabel.value = ratioInfo.label
  }
  
  if (cropperInstance) {
    cropperInstance.setAspectRatio(ratio)
  }
}

function zoomIn() {
  if (cropperInstance) {
    cropperInstance.zoom(0.1)
    zoom.value = Math.min(3, zoom.value + 0.1)
  }
}

function zoomOut() {
  if (cropperInstance) {
    cropperInstance.zoom(-0.1)
    zoom.value = Math.max(0.5, zoom.value - 0.1)
  }
}

function resetCropper() {
  if (cropperInstance) {
    cropperInstance.reset()
    zoom.value = 1
  }
}

function confirmCrop() {
  if (!cropperInstance) {
    console.error('Cropper not initialized')
    return
  }
  
  try {
    const canvas = cropperInstance.getCroppedCanvas({
      maxWidth: 512,
      maxHeight: 512,
      imageSmoothingEnabled: true,
      imageSmoothingQuality: 'high'
    })
    
    canvas.toBlob((blob) => {
      const file = new File([blob], 'cropped-logo.png', { type: 'image/png' })
      emit('crop', file)
      close()
    }, 'image/png')
  } catch (err) {
    console.error('Crop failed:', err)
  }
}

function close() {
  destroyCropper()
  emit('close')
}

watch(() => props.visible, async (newVal) => {
  if (newVal) {
    zoom.value = 1
    currentAspectLabel.value = '1:1'
    await nextTick()
    setTimeout(initCropper, 100)
  } else {
    destroyCropper()
  }
})

watch(() => props.imageUrl, async () => {
  if (props.visible) {
    await nextTick()
    setTimeout(initCropper, 100)
  }
})

onUnmounted(() => {
  destroyCropper()
})
</script>

<style scoped>
/* Import cropperjs CSS */
:deep(.cropper-view-box),
:deep(.cropper-face) {
  border-radius: 0;
}

/* Cropper container styles */
:deep(.cropper-container) {
  font-family: inherit;
}

:deep(.cropper-modal) {
  background-color: rgba(0, 0, 0, 0.5);
}

:deep(.cropper-view-box) {
  outline: none;
  box-shadow: 0 0 0 1px #39f;
}

:deep(.cropper-line) {
  background-color: #39f;
}

:deep(.cropper-point) {
  background-color: #39f;
  width: 10px;
  height: 10px;
  opacity: 1;
}

:deep(.cropper-point.point-se) {
  width: 12px;
  height: 12px;
}

:deep(.cropper-dashed) {
  border-color: rgba(255, 255, 255, 0.5);
}

:deep(.cropper-center) {
  width: 12px;
  height: 12px;
}

:deep(.cropper-center::before),
:deep(.cropper-center::after) {
  background-color: rgba(255, 255, 255, 0.75);
}
</style>

<!-- 引入 cropperjs CSS -->
<style>
@import 'https://cdn.jsdelivr.net/npm/cropperjs@1.6.1/dist/cropper.min.css';
</style>

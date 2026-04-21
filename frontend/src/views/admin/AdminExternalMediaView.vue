<template>
  <AdminLayout>
    <div class="mb-8">
      <h1 class="text-2xl font-serif mb-2">外接图床</h1>
      <p class="text-text-secondary">管理外部图床的图片资源</p>
    </div>

    <!-- Iframe Container -->
    <div class="bg-surface rounded-lg border border-border overflow-hidden">
      <div class="bg-secondary/30 px-6 py-3 flex items-center justify-between border-b border-border">
        <div class="flex items-center gap-2">
          <svg class="w-5 h-5 text-text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/>
          </svg>
          <span class="font-medium">图床管理</span>
        </div>
        <a 
          href="https://pic.lishx.dpdns.org/admin-imgtc" 
          target="_blank" 
          class="text-sm text-primary hover:underline flex items-center gap-1"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
          </svg>
          在新窗口打开
        </a>
      </div>
      
      <!-- Iframe for External Media Bed -->
      <div class="h-[600px]">
        <iframe 
          :src="iframeUrl" 
          class="w-full h-full border-0" 
          title="外接图床管理"
          sandbox="allow-same-origin allow-scripts allow-forms"
        ></iframe>
      </div>
    </div>

    <!-- Login Info -->
    <div class="mt-4 bg-primary/5 border border-primary/20 rounded-lg p-4">
      <h3 class="font-medium text-primary mb-2">图床登录信息</h3>
      <div class="space-y-2 text-sm">
        <div class="flex items-center gap-2">
          <span class="text-text-secondary w-20">地址：</span>
          <span class="font-mono">{{ iframeUrl }}</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-text-secondary w-20">账号：</span>
          <span class="font-mono">admin</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-text-secondary w-20">密码：</span>
          <span class="font-mono">admin123</span>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import AdminLayout from './AdminLayout.vue'

const iframeUrl = 'https://pic.lishx.dpdns.org/admin-imgtc'
</script>
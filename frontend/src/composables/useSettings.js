import { ref } from 'vue'

// 全局单例缓存，避免多组件重复请求
const _settings = ref(null)
const _loaded = ref(false)
const _loading = ref(false)

export function useSettings() {
  async function fetchSettings() {
    if (_loaded.value) return
    if (_loading.value) {
      // 等待中，轮询等加载完
      await new Promise(resolve => {
        const timer = setInterval(() => {
          if (_loaded.value) { clearInterval(timer); resolve() }
        }, 50)
      })
      return
    }
    _loading.value = true
    try {
      const res = await fetch('/api/settings')
      const data = await res.json()
      _settings.value = data.data || {}
      _loaded.value = true
    } catch (e) {
      console.error('Failed to load settings:', e)
      _settings.value = {}
      _loaded.value = true
    } finally {
      _loading.value = false
    }
  }

  function isConsultEnabled() {
    if (!_settings.value) return true  // 未加载时默认显示
    return _settings.value.consult_enabled !== '0'
  }

  // 强制刷新（设置更新后调用）
  function invalidate() {
    _loaded.value = false
    _settings.value = null
  }

  return { fetchSettings, isConsultEnabled, settings: _settings, invalidate }
}

<template>
  <div :class="['elysian-layout', isDark ? 'dark' : 'light']">
    <aside :class="['elysian-sidebar', { collapsed: !sidebarOpen }]">
      <div class="sidebar-header">
        <button class="sidebar-toggle glass" @click="toggleSidebar" :aria-label="sidebarOpen ? '收起菜单' : '展开菜单'">
          <Icon :icon="sidebarOpen ? 'fluent:chevron-left-24-regular' : 'fluent:chevron-right-24-regular'" />
        </button>
      </div>
      <nav class="sidebar-nav">
        <button
          v-for="item in navs"
          :key="item.key"
          :class="['sidebar-btn glass', { active: current === item.key, 'icon-only': !sidebarOpen }]"
          @click="go(item.key)"
          :aria-label="item.label"
        >
          <Icon :icon="item.icon" class="sidebar-icon" />
          <span v-if="sidebarOpen" class="sidebar-label">{{ item.label }}</span>
        </button>
      </nav>
      <div class="sidebar-bottom">
        <button class="mode-toggle glass" @click="toggleDark" :aria-label="isDark ? '切换为亮色模式' : '切换为深色模式'">
          <Icon :icon="isDark ? 'fluent:weather-sunny-24-regular' : 'fluent:weather-moon-24-regular'" />
        </button>
      </div>
    </aside>
    <main class="elysian-content glass">
      <slot />
      <!-- 这里可以根据路由或状态切换不同内容页 -->
      <div v-if="current === 'home'" class="elysian-home-content">
        <img src="/Elysia.png" alt="elysia" class="elysian-hero-img" />
        <h1 class="elysian-title">Elysian-Realm</h1>
        <div class="elysian-desc">
          现代化、可视化的 LLM 微调与推理平台<br>
          支持 QLoRA、Optuna、ShareGPT 格式
        </div>
      </div>
      <!-- 其他内容页... -->
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { Icon } from '@iconify/vue'
const navs = [
  { key: 'home', icon: 'fluent:home-24-regular', label: '首页' },
  { key: 'train', icon: 'fluent:play-circle-24-regular', label: '训练' },
  { key: 'infer', icon: 'fluent:chat-24-regular', label: '推理' },
  { key: 'tune', icon: 'fluent:wand-24-regular', label: '调参' },
  { key: 'model', icon: 'fluent:database-24-regular', label: '模型管理' }
]
const current = ref('home')
const go = (key: string) => { current.value = key }
const sidebarOpen = ref(true)
const isMobile = ref(window.innerWidth <= 900)
const toggleSidebar = () => { sidebarOpen.value = !sidebarOpen.value }
const handleResize = () => { isMobile.value = window.innerWidth <= 900; if(isMobile.value) sidebarOpen.value = false }

// 深色模式检测与切换
const isDark = ref(window.matchMedia('(prefers-color-scheme: dark)').matches)
const onColorSchemeChange = (e: MediaQueryListEvent) => { isDark.value = e.matches }
const toggleDark = () => {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
  document.documentElement.classList.toggle('light', !isDark.value)
}
onMounted(() => {
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', onColorSchemeChange)
  document.documentElement.classList.toggle('dark', isDark.value)
  document.documentElement.classList.toggle('light', !isDark.value)
  window.addEventListener('resize', handleResize)
})
onUnmounted(() => {
  window.matchMedia('(prefers-color-scheme: dark)').removeEventListener('change', onColorSchemeChange)
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.elysian-layout {
  display: flex;
  min-height: 100vh;
  background: var(--bg-gradient);
  transition: background 0.3s;
}
.light { --bg-gradient: linear-gradient(135deg, #f6f8fc 0%, #e3f6fd 100%); }
.dark  { --bg-gradient: linear-gradient(135deg, #23272e 0%, #1a1d23 100%); }

.elysian-sidebar {
  width: 220px;
  min-width: 56px;
  background: var(--sidebar-bg);
  backdrop-filter: blur(16px) saturate(160%);
  -webkit-backdrop-filter: blur(16px) saturate(160%);
  border-radius: 0 16px 16px 0;
  box-shadow: 2px 0 16px 0 rgba(0,0,0,0.06);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 0;
  transition: width 0.2s, background 0.3s;
  z-index: 10;
  position: relative;
}
.elysian-sidebar.collapsed {
  width: 56px;
}
.light { --sidebar-bg: rgba(255,255,255,0.72); }
.dark  { --sidebar-bg: rgba(32,32,36,0.72); }

.sidebar-header {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 12px 0 8px 8px;
}
.sidebar-toggle.glass {
  font-size: 1.5rem;
  color: var(--sidebar-btn-color, #444);
  cursor: pointer;
  outline: none;
  border: none;
  background: var(--sidebar-btn-bg, rgba(255,255,255,0.38));
  border-radius: 12px;
  backdrop-filter: blur(12px) saturate(160%);
  -webkit-backdrop-filter: blur(12px) saturate(160%);
  box-shadow: 0 4px 12px 0 rgba(0,120,212,0.22), 0 2px 8px 0 rgba(0,0,0,0.08);
  padding: 8px 10px;
  margin-bottom: 8px;
  transition: background 0.18s, box-shadow 0.18s, color 0.18s, transform 0.18s;
}
.sidebar-toggle.glass:hover, .sidebar-toggle.glass:focus {
  background: var(--sidebar-btn-active-bg, #e3f6fd);
  color: var(--sidebar-btn-active-color, #0078d4);
  box-shadow: 0 8px 32px 0 rgba(0,120,212,0.32), 0 2px 8px 0 rgba(0,0,0,0.12);
  transform: translateY(-2px) scale(1.04);
}
.dark .sidebar-toggle.glass {
  background: rgba(32,32,36,0.62);
  color: #aad6ff;
  box-shadow: 0 4px 12px 0 rgba(0,180,255,0.32), 0 2px 8px 0 rgba(0,0,0,0.18);
}
.dark .sidebar-toggle.glass:hover, .dark .sidebar-toggle.glass:focus {
  background: #23272e;
  color: #fff;
  box-shadow: 0 8px 32px 0 rgba(0,180,255,0.42), 0 2px 8px 0 rgba(0,0,0,0.18);
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}
.sidebar-btn.glass {
  display: flex;
  align-items: center;
  width: 90%;
  margin-left: 5%;
  background: var(--sidebar-btn-bg, rgba(255,255,255,0.38));
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 12px 0 rgba(0,120,212,0.22), 0 2px 8px 0 rgba(0,0,0,0.08);
  font-size: 1.08rem;
  color: var(--sidebar-btn-color, #444);
  padding: 12px 12px;
  cursor: pointer;
  transition: background 0.18s, color 0.18s, box-shadow 0.18s, transform 0.18s;
  outline: none;
  backdrop-filter: blur(12px) saturate(160%);
  -webkit-backdrop-filter: blur(12px) saturate(160%);
  position: relative;
}
.sidebar-btn.icon-only {
  width: 40px;
  min-width: 40px;
  max-width: 40px;
  height: 40px;
  padding: 0;
  justify-content: center;
  margin-left: 8px;
}
.sidebar-btn.icon-only .sidebar-label {
  display: none;
}
.sidebar-btn.active, .sidebar-btn.glass:hover {
  background: var(--sidebar-btn-active-bg, #e3f6fd);
  color: var(--sidebar-btn-active-color, #0078d4);
  box-shadow: 0 8px 32px 0 rgba(0,120,212,0.32), 0 2px 8px 0 rgba(0,0,0,0.12);
  transform: translateY(-4px) scale(1.04);
  z-index: 1;
}
.dark .sidebar-btn.glass {
  background: rgba(32,32,36,0.62);
  color: #bbb;
  box-shadow: 0 4px 12px 0 rgba(0,180,255,0.32), 0 2px 8px 0 rgba(0,0,0,0.18);
}
.dark .sidebar-btn.active, .dark .sidebar-btn.glass:hover {
  background: rgba(40,80,180,0.18);
  color: #aad6ff;
  box-shadow: 0 8px 32px 0 rgba(0,180,255,0.42), 0 2px 8px 0 rgba(0,0,0,0.18);
}
.sidebar-icon {
  font-size: 1.4rem;
  margin-right: 12px;
}
.sidebar-btn.icon-only .sidebar-icon {
  margin-right: 0;
}
.sidebar-label {
  white-space: nowrap;
  transition: opacity 0.2s;
}
.elysian-sidebar.collapsed .sidebar-label {
  opacity: 0;
  width: 0;
  overflow: hidden;
}

.sidebar-bottom {
  position: absolute;
  left: 0;
  bottom: 12px;
  width: 100%;
  display: flex;
  justify-content: center;
}
.mode-toggle.glass {
  background: var(--sidebar-btn-bg, rgba(255,255,255,0.38));
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 12px 0 rgba(0,120,212,0.22), 0 2px 8px 0 rgba(0,0,0,0.08);
  font-size: 1.4rem;
  color: var(--sidebar-btn-color, #444);
  padding: 10px 12px;
  cursor: pointer;
  outline: none;
  backdrop-filter: blur(12px) saturate(160%);
  -webkit-backdrop-filter: blur(12px) saturate(160%);
  transition: background 0.18s, color 0.18s, box-shadow 0.18s;
}
.mode-toggle.glass:hover {
  background: var(--sidebar-btn-active-bg, #e3f6fd);
  color: var(--sidebar-btn-active-color, #0078d4);
  box-shadow: 0 8px 32px 0 rgba(0,120,212,0.32), 0 2px 8px 0 rgba(0,0,0,0.12);
}
.dark .mode-toggle.glass {
  background: rgba(32,32,36,0.62);
  color: #aad6ff;
  box-shadow: 0 4px 12px 0 rgba(0,180,255,0.32), 0 2px 8px 0 rgba(0,0,0,0.18);
}
.dark .mode-toggle.glass:hover {
  background: #23272e;
  color: #fff;
  box-shadow: 0 8px 32px 0 rgba(0,180,255,0.42), 0 2px 8px 0 rgba(0,0,0,0.18);
}

.elysian-content.glass {
  flex: 1;
  min-width: 0;
  padding: 48px 32px;
  background: var(--content-bg);
  backdrop-filter: blur(12px) saturate(160%);
  -webkit-backdrop-filter: blur(12px) saturate(160%);
  border-radius: 16px;
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.12);
  margin: 32px;
  transition: background 0.3s;
}
.light { --content-bg: rgba(255,255,255,0.82); }
.dark  { --content-bg: rgba(32,32,36,0.82); }

.elysian-home-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}
.elysian-hero-img {
  width: 220px;
  height: 280px;
  object-fit: contain;
  border-radius: 12px;
  box-shadow: 0 8px 32px 0 rgba(0,0,0,0.10);
}
.elysian-title {
  font-size: 2.2rem;
  font-weight: 800;
  color: #0078d4;
  margin: 0;
  text-align: center;
}
.dark .elysian-title { color: #aad6ff; }
.elysian-desc {
  font-size: 1.02rem;
  color: #666;
  line-height: 1.7;
  text-align: center;
}
.dark .elysian-desc { color: #bbb; }

@media (max-width: 900px) {
  .elysian-layout { flex-direction: column; }
  .elysian-sidebar { flex-direction: row; width: 100vw; min-width: 0; height: 56px; border-radius: 0 0 16px 16px; }
  .elysian-sidebar.collapsed { width: 56px; }
  .sidebar-header { padding: 8px 0 8px 8px; }
  .sidebar-nav { flex-direction: row; gap: 12px; width: auto; }
  .sidebar-btn.glass { flex-direction: column; padding: 6px 8px; border-radius: 12px; font-size: 0.98rem; margin-left: 0; width: 48px; }
  .sidebar-btn.icon-only { width: 40px; min-width: 40px; max-width: 40px; height: 40px; padding: 0; }
  .sidebar-icon { margin: 0 0 4px 0; }
  .sidebar-bottom { position: absolute; left: auto; right: 12px; bottom: 8px; }
  .elysian-content.glass { padding: 24px 8px; margin: 8px; border-radius: 12px; }
}
</style> 
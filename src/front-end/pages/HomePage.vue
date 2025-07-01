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
      <!-- 这里可以根据路由或状态切换不同内容页 -->
      <div v-if="current === 'home'" class="elysian-home-content">
        <img src="/Elysia.png" alt="elysia" class="elysian-hero-img" />
        <h1 class="elysian-title">Elysian-Realm</h1>
        <div class="elysian-desc">
          现代化、可视化的 LLM 微调与推理平台<br>
          支持 QLoRA、Optuna、ShareGPT 格式
        </div>
      </div>
      <TrainPage v-else-if="current === 'train'" />
      <InferPage v-else-if="current === 'infer'" />
      <TunePage v-else-if="current === 'tune'" />
      <ModelPage v-else-if="current === 'model'" />
      <!-- 其他内容页... -->
    </main>
  </div>
</template>

<script setup lang="ts">
import './HomePage.css'
import { ref, onMounted, onUnmounted } from 'vue'
import { Icon } from '@iconify/vue'
import TrainPage from './TrainPage.vue'
import InferPage from './InferPage.vue'
import TunePage from './TunePage.vue'
import ModelPage from './ModelPage.vue'

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
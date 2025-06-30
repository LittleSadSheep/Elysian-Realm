<template>
  <div id="app" :class="{ 'dark-theme': isDarkMode }">
    <!-- 导航栏 -->
    <nav class="navbar" v-if="currentRoute !== 'home'">
      <div class="nav-content">
        <div class="nav-left">
          <img src="/Elysia.png" alt="Logo" class="nav-logo" />
          <h1 class="nav-title">Elysian-Realm</h1>
        </div>
        
        <div class="nav-center">
          <button
            v-for="item in navigationItems"
            :key="item.key"
            class="nav-button"
            :class="{ active: currentRoute === item.key }"
            @click="navigateTo(item.key)"
          >
            <Icon :icon="item.icon" class="nav-icon" />
            <span class="nav-label">{{ item.label }}</span>
          </button>
        </div>
        
        <div class="nav-right">
          <button class="theme-toggle" @click="toggleTheme">
            <Icon :icon="isDarkMode ? 'fluent:weather-sunny-24-regular' : 'fluent:weather-moon-24-regular'" />
          </button>
        </div>
      </div>
    </nav>

    <!-- 首页欢迎界面 -->
    <div v-if="currentRoute === 'home'" class="welcome-screen">
      <div class="welcome-content">
        <div class="welcome-left">
          <div class="welcome-header">
            <img src="/Elysia.png" alt="Logo" class="welcome-logo" />
            <h1 class="welcome-title">Elysian-Realm</h1>
            <p class="welcome-subtitle">大模型微调平台</p>
          </div>
          
          <div class="welcome-description">
            <p>现代化、可视化的 LLM 微调与推理平台</p>
            <p>支持 QLoRA、Optuna、ShareGPT 格式</p>
            <p>采用 Microsoft Fluent 2 设计体系</p>
          </div>
          
          <div class="welcome-actions">
            <button
              v-for="item in navigationItems"
              :key="item.key"
              class="welcome-button"
              @click="navigateTo(item.key)"
            >
              <Icon :icon="item.icon" class="welcome-button-icon" />
              <span class="welcome-button-label">{{ item.label }}</span>
            </button>
          </div>
          
          <button class="theme-toggle-large" @click="toggleTheme">
            <Icon :icon="isDarkMode ? 'fluent:weather-sunny-24-regular' : 'fluent:weather-moon-24-regular'" />
          </button>
        </div>
        
        <div class="welcome-right">
          <div class="hero-image-container">
            <img src="/Elysia.png" alt="Hero" class="hero-image" />
          </div>
        </div>
      </div>
    </div>

    <!-- 页面内容 -->
    <main v-else class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Icon } from '@iconify/vue'

const router = useRouter()
const route = useRoute()

const isDarkMode = ref(false)

const navigationItems = [
  { key: 'home', icon: 'fluent:home-24-regular', label: '首页' },
  { key: 'train', icon: 'fluent:play-circle-24-regular', label: '训练' },
  { key: 'infer', icon: 'fluent:chat-24-regular', label: '推理' },
  { key: 'tune', icon: 'fluent:wand-24-regular', label: '调参' },
  { key: 'model', icon: 'fluent:database-24-regular', label: '模型管理' }
]

const currentRoute = computed(() => route.name as string)

const navigateTo = (routeName: string) => {
  router.push({ name: routeName })
}

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  document.documentElement.classList.toggle('dark-theme', isDarkMode.value)
}
</script>

<style scoped>
/* 基础变量 */
:root {
  --color-bg-primary: #ffffff;
  --color-bg-secondary: #f8f9fa;
  --color-bg-tertiary: #f1f3f4;
  --color-text-primary: #202124;
  --color-text-secondary: #5f6368;
  --color-border: #dadce0;
  --color-primary: #0078d4;
  --color-primary-hover: #106ebe;
  --color-accent: #0078d4;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
}

.dark-theme {
  --color-bg-primary: #1f1f1f;
  --color-bg-secondary: #2d2d30;
  --color-bg-tertiary: #3c3c3c;
  --color-text-primary: #ffffff;
  --color-text-secondary: #b0b0b0;
  --color-border: #404040;
  --color-primary: #60aaff;
  --color-primary-hover: #4cc2ff;
}

#app {
  min-height: 100vh;
  background: var(--color-bg-primary);
  color: var(--color-text-primary);
  transition: background-color 0.3s ease, color 0.3s ease;
}

/* 导航栏样式 */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--color-border);
  transition: all 0.3s ease;
}

.dark-theme .navbar {
  background: rgba(31, 31, 31, 0.8);
}

.nav-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-md) var(--spacing-xl);
  max-width: 1400px;
  margin: 0 auto;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.nav-logo {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
}

.nav-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.nav-center {
  display: flex;
  gap: var(--spacing-sm);
}

.nav-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  border: none;
  background: transparent;
  color: var(--color-text-secondary);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 64px;
}

.nav-button:hover {
  background: var(--color-bg-secondary);
  color: var(--color-text-primary);
}

.nav-button.active {
  background: var(--color-primary);
  color: white;
}

.nav-icon {
  font-size: 20px;
}

.nav-label {
  font-size: 12px;
  font-weight: 500;
}

.theme-toggle {
  width: 40px;
  height: 40px;
  border: none;
  background: var(--color-bg-secondary);
  color: var(--color-text-primary);
  border-radius: var(--radius-md);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.theme-toggle:hover {
  background: var(--color-bg-tertiary);
}

/* 欢迎界面样式 */
.welcome-screen {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl);
}

.welcome-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-2xl);
  max-width: 1200px;
  width: 100%;
  align-items: center;
}

.welcome-left {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
}

.welcome-header {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--spacing-md);
}

.welcome-logo {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-lg);
}

.welcome-title {
  font-size: 48px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0;
  line-height: 1.2;
}

.welcome-subtitle {
  font-size: 24px;
  color: var(--color-text-secondary);
  margin: 0;
  font-weight: 500;
}

.welcome-description {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.welcome-description p {
  font-size: 16px;
  color: var(--color-text-secondary);
  margin: 0;
  line-height: 1.6;
}

.welcome-actions {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-md);
  margin-top: var(--spacing-lg);
}

.welcome-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-lg);
  border: 1px solid var(--color-border);
  background: var(--color-bg-secondary);
  color: var(--color-text-primary);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
}

.welcome-button:hover {
  background: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.welcome-button-icon {
  font-size: 32px;
}

.welcome-button-label {
  font-size: 16px;
  font-weight: 600;
}

.theme-toggle-large {
  width: 56px;
  height: 56px;
  border: none;
  background: var(--color-bg-secondary);
  color: var(--color-text-primary);
  border-radius: var(--radius-lg);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  align-self: flex-start;
}

.theme-toggle-large:hover {
  background: var(--color-bg-tertiary);
}

.welcome-right {
  display: flex;
  justify-content: center;
  align-items: center;
}

.hero-image-container {
  position: relative;
  width: 400px;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  transition: transform 0.3s ease;
}

.hero-image:hover {
  transform: scale(1.05);
}

/* 主内容区域 */
.main-content {
  margin-top: 80px;
  padding: var(--spacing-xl);
  max-width: 1400px;
  margin-left: auto;
  margin-right: auto;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .welcome-content {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .welcome-actions {
    grid-template-columns: 1fr;
  }
  
  .nav-center {
    display: none;
  }
  
  .welcome-title {
    font-size: 36px;
  }
  
  .hero-image-container {
    width: 300px;
    height: 300px;
  }
}
</style> 
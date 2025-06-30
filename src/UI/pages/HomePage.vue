<template>
  <div class="fluent-home-root">
    <div class="fluent-home-main">
      <!-- 左侧内容 -->
      <div class="fluent-home-card glass">
        <div class="fluent-home-header">
          <img class="fluent-home-logo" src="/Elysia.png" alt="logo" />
          <div>
            <h1 class="fluent-home-title">Elysian-Realm</h1>
            <div class="fluent-home-subtitle">大模型微调平台</div>
          </div>
        </div>
        <div class="fluent-home-desc">
          现代化、可视化的 LLM 微调与推理平台<br>
          支持 QLoRA、Optuna、ShareGPT 格式<br>
          采用 Microsoft Fluent 2 设计体系
        </div>
        <div class="fluent-home-btns">
          <button
            v-for="item in navs"
            :key="item.key"
            class="fluent-btn"
            @click="go(item.key)"
            :title="item.label"
            :aria-label="item.label"
          >
            <Icon :icon="item.icon" class="btn-icon" />
            <span class="btn-label">{{ item.label }}</span>
          </button>
        </div>
      </div>
      <!-- 右侧角色图 -->
      <div class="fluent-home-hero glass">
        <img src="/Elysia.png" alt="elysia" class="fluent-home-hero-img" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const navs = [
  { key: 'home', icon: 'fluent:home-24-regular', label: '首页' },
  { key: 'train', icon: 'fluent:play-circle-24-regular', label: '训练' },
  { key: 'infer', icon: 'fluent:chat-24-regular', label: '推理' },
  { key: 'tune', icon: 'fluent:wand-24-regular', label: '调参' },
  { key: 'model', icon: 'fluent:database-24-regular', label: '模型管理' }
]
const go = (key: string) => {
  if (key !== 'home') router.push({ name: key })
}
</script>

<style scoped>
.fluent-home-root {
  min-height: 100vh;
  /* 多彩白（亮色）背景 */
  background: linear-gradient(135deg, #fffbe6 0%, #e3f6fd 30%, #f7e1ff 60%, #e6ffe6 100%),
              repeating-linear-gradient(120deg, #fff, #f0f0f0 20px, #f7e1ff 40px, #e3f6fd 60px);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.4s;
}
:root.dark .fluent-home-root {
  /* 多彩黑（深色）背景 */
  background: linear-gradient(135deg, #181c24 0%, #2a1a2e 30%, #1a2e2a 60%, #2e1a1a 100%),
              repeating-linear-gradient(120deg, #232427, #2a1a2e 20px, #1a2e2a 40px, #2e1a1a 60px);
}
.fluent-home-main {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 64px;
  width: 100%;
  max-width: 1200px;
  padding: 48px 0;
}
.fluent-home-card {
  min-width: 420px;
  max-width: 480px;
  padding: 40px 36px 32px 36px;
  border-radius: 32px;
  box-shadow: 0 8px 32px 0 rgba(0,0,0,0.14);
  background: rgba(255,255,255,0.72);
  -webkit-backdrop-filter: blur(32px) saturate(1.3);
  backdrop-filter: blur(32px) saturate(1.3);
  display: flex;
  flex-direction: column;
  gap: 32px;
  animation: fadeInUp 0.8s;
  transition: background 0.4s, box-shadow 0.3s;
  -webkit-user-select: none;
  user-select: none;
}
:root.dark .fluent-home-card {
  background: rgba(32,32,36,0.82);
  -webkit-backdrop-filter: blur(32px) saturate(1.3);
  backdrop-filter: blur(32px) saturate(1.3);
  box-shadow: 0 8px 32px 0 rgba(0,0,0,0.32);
}
.fluent-home-header {
  display: flex;
  align-items: center;
  gap: 18px;
}
.fluent-home-logo {
  width: 72px;
  height: 72px;
  border-radius: 20px;
  box-shadow: 0 2px 16px 0 rgba(0,0,0,0.12);
}
.fluent-home-title {
  font-size: 2.8rem;
  font-weight: 800;
  margin: 0;
  color: var(--fluent-title, #222);
  letter-spacing: 1px;
}
:root.dark .fluent-home-title {
  color: #fff;
}
.fluent-home-subtitle {
  font-size: 1.2rem;
  color: #0078d4;
  font-weight: 600;
  margin-top: 2px;
}
.fluent-home-desc {
  font-size: 1.08rem;
  color: var(--fluent-desc, #444);
  line-height: 1.7;
  margin-bottom: 8px;
}
:root.dark .fluent-home-desc {
  color: #e0e0e0;
}
.fluent-home-btns {
  display: flex;
  flex-direction: column;
  gap: 22px;
  margin-top: 12px;
}
.fluent-btn {
  display: flex;
  align-items: center;
  gap: 14px;
  justify-content: flex-start;
  background: linear-gradient(120deg, var(--fluent-btn-bg1, #f7faff) 60%, var(--fluent-btn-bg2, #e3e9f7) 100%);
  border: none;
  border-radius: 18px;
  box-shadow: 0 2px 16px 0 rgba(0,120,212,0.10);
  font-size: 1.18rem;
  font-weight: 600;
  color: var(--fluent-btn, #0078d4);
  padding: 20px 0 20px 18px;
  cursor: pointer;
  transition: background 0.22s, box-shadow 0.22s, color 0.22s, transform 0.18s;
  min-width: 180px;
  min-height: 54px;
  outline: none;
  -webkit-user-select: none;
  user-select: none;
  user-select: none;
}
:root.dark .fluent-btn {
  background: linear-gradient(120deg, #232427 60%, #18191c 100%);
  color: #aad6ff;
  box-shadow: 0 2px 16px 0 rgba(0,120,212,0.18);
}
.fluent-btn:hover {
  background: linear-gradient(120deg, var(--fluent-btn-bg2, #e3e9f7) 60%, var(--fluent-btn-bg1, #f7faff) 100%);
  color: var(--fluent-btn-hover, #005fa3);
  box-shadow: 0 8px 32px 0 rgba(0,120,212,0.18);
  transform: translateY(-2px) scale(1.03);
}
:root.dark .fluent-btn:hover {
  background: linear-gradient(120deg, #18191c 60%, #232427 100%);
  color: #fff;
}
.fluent-btn:active {
  filter: brightness(0.97);
  transform: scale(0.98);
}
.btn-icon {
  font-size: 1.7rem;
  display: flex;
  align-items: center;
}
.btn-label {
  flex: 1;
  text-align: left;
}
.fluent-home-hero {
  min-width: 360px;
  min-height: 420px;
  border-radius: 36px;
  background: rgba(255,255,255,0.32);
  -webkit-backdrop-filter: blur(36px) saturate(1.2);
  backdrop-filter: blur(36px) saturate(1.2);
  box-shadow: 0 8px 48px 0 rgba(0,0,0,0.18);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: float 3s ease-in-out infinite alternate;
  transition: background 0.4s, box-shadow 0.3s;
  -webkit-user-select: none;
  user-select: none;
}
:root.dark .fluent-home-hero {
  background: rgba(32,32,36,0.32);
  -webkit-backdrop-filter: blur(36px) saturate(1.2);
  backdrop-filter: blur(36px) saturate(1.2);
  box-shadow: 0 8px 48px 0 rgba(0,0,0,0.38);
}
.fluent-home-hero-img {
  width: 320px;
  height: 400px;
  object-fit: contain;
  border-radius: 32px;
  box-shadow: 0 8px 48px 0 rgba(0,0,0,0.18);
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(40px);}
  to { opacity: 1; transform: none;}
}
@keyframes float {
  0% { transform: translateY(0);}
  100% { transform: translateY(-18px);}
}
@media (max-width: 900px) {
  .fluent-home-main { flex-direction: column; gap: 32px; }
  .fluent-home-hero { min-width: 280px; min-height: 320px; }
  .fluent-home-hero-img { width: 220px; height: 260px; }
}
</style> 
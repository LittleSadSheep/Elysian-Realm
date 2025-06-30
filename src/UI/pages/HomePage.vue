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
          <button v-for="item in navs" :key="item.key" class="fluent-btn" @click="go(item.key)">
            <span class="icon"><Icon :icon="item.icon" /></span>
            <span>{{ item.label }}</span>
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
  background: linear-gradient(135deg, #e3e9f7 0%, #f7faff 40%, #f6f3ff 70%, #f9f6f3 100%);
  display: flex;
  align-items: center;
  justify-content: center;
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
  border-radius: 24px;
  box-shadow: 0 8px 32px 0 rgba(0,0,0,0.12);
  background: rgba(255,255,255,0.65);
  backdrop-filter: blur(24px) saturate(1.2);
  display: flex;
  flex-direction: column;
  gap: 32px;
  animation: fadeInUp 0.8s;
}
.fluent-home-header {
  display: flex;
  align-items: center;
  gap: 18px;
}
.fluent-home-logo {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.10);
}
.fluent-home-title {
  font-size: 2.6rem;
  font-weight: 800;
  margin: 0;
  color: #222;
  letter-spacing: 1px;
}
.fluent-home-subtitle {
  font-size: 1.2rem;
  color: #0078d4;
  font-weight: 600;
  margin-top: 2px;
}
.fluent-home-desc {
  font-size: 1.08rem;
  color: #444;
  line-height: 1.7;
  margin-bottom: 8px;
}
.fluent-home-btns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}
.fluent-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  justify-content: center;
  background: linear-gradient(120deg, #f7faff 60%, #e3e9f7 100%);
  border: none;
  border-radius: 16px;
  box-shadow: 0 2px 12px 0 rgba(0,120,212,0.08);
  font-size: 1.1rem;
  font-weight: 600;
  color: #0078d4;
  padding: 18px 0;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s, color 0.2s;
}
.fluent-btn:hover {
  background: linear-gradient(120deg, #e3e9f7 60%, #f7faff 100%);
  color: #005fa3;
  box-shadow: 0 8px 32px 0 rgba(0,120,212,0.18);
}
.fluent-btn .icon {
  font-size: 1.6rem;
  display: flex;
  align-items: center;
}
.fluent-home-hero {
  min-width: 360px;
  min-height: 420px;
  border-radius: 32px;
  background: rgba(255,255,255,0.32);
  box-shadow: 0 8px 48px 0 rgba(0,0,0,0.18);
  backdrop-filter: blur(32px) saturate(1.2);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: float 3s ease-in-out infinite alternate;
}
.fluent-home-hero-img {
  width: 320px;
  height: 400px;
  object-fit: contain;
  border-radius: 28px;
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
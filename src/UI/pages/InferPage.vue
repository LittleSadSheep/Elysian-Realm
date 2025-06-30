<template>
  <div class="fluent-infer-root">
    <div class="fluent-infer-main glass">
      <div class="fluent-infer-header">
        <h1>模型推理</h1>
        <div class="desc">加载模型，开始对话推理</div>
      </div>
      <div class="fluent-infer-chat glass">
        <div class="chat-messages">
          <div v-for="msg in chatMessages" :key="msg.id" :class="['chat-bubble', msg.role]">
            <span class="avatar"><Icon :icon="msg.role==='user'?'fluent:person-24-regular':'fluent:bot-24-regular'" /></span>
            <span class="bubble-content">{{ msg.content }}</span>
          </div>
        </div>
        <div class="chat-input-row">
          <textarea v-model="userInput" class="fluent-input" placeholder="输入您的问题..." @keydown.enter.prevent="sendMessage"></textarea>
          <button class="fluent-btn primary send-btn" @click="sendMessage" :disabled="!userInput.trim()"><Icon icon="fluent:send-24-regular" /></button>
        </div>
      </div>
      <div class="fluent-infer-settings glass">
        <div class="settings-row">
          <div class="form-group">
            <label>温度</label>
            <input type="range" v-model="settings.temperature" min="0" max="2" step="0.1" />
            <span class="range-value">{{ settings.temperature }}</span>
          </div>
          <div class="form-group">
            <label>最大长度</label>
            <input type="number" v-model="settings.maxLength" class="fluent-input" min="100" max="4096" />
          </div>
          <div class="form-group">
            <label>Top P</label>
            <input type="range" v-model="settings.topP" min="0" max="1" step="0.1" />
            <span class="range-value">{{ settings.topP }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Icon } from '@iconify/vue'

const chatMessages = ref([
  { id: 1, role: 'assistant', content: '你好！我是AI助手，有什么可以帮您？' }
])

const userInput = ref('')
const settings = ref({ temperature: 0.7, maxLength: 2048, topP: 0.9 })

const sendMessage = () => {
  if (!userInput.value.trim()) return
  chatMessages.value.push({ id: Date.now(), role: 'user', content: userInput.value })
  setTimeout(() => {
    chatMessages.value.push({ id: Date.now()+1, role: 'assistant', content: '这是AI的回复。' })
  }, 1000)
  userInput.value = ''
}
</script>

<style scoped>
.fluent-infer-root {
  min-height: 100vh;
  background: linear-gradient(135deg, #e3e9f7 0%, #f7faff 40%, #f6f3ff 70%, #f9f6f3 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}
.fluent-infer-main {
  width: 100%;
  max-width: 700px;
  margin: 48px auto;
  border-radius: 24px;
  box-shadow: 0 8px 32px 0 rgba(0,0,0,0.12);
  background: rgba(255,255,255,0.65);
  backdrop-filter: blur(24px) saturate(1.2);
  padding: 40px 36px 32px 36px;
  display: flex;
  flex-direction: column;
  gap: 32px;
  animation: fadeInUp 0.8s;
}
.fluent-infer-header h1 {
  font-size: 2.2rem;
  font-weight: 800;
  color: #222;
  margin-bottom: 8px;
}
.fluent-infer-header .desc {
  color: #0078d4;
  font-size: 1.1rem;
  font-weight: 600;
}
.fluent-infer-chat {
  border-radius: 20px;
  background: rgba(255,255,255,0.85);
  box-shadow: 0 4px 24px 0 rgba(0,120,212,0.10);
  padding: 24px 18px;
  margin-bottom: 18px;
}
.chat-messages {
  min-height: 180px;
  max-height: 320px;
  overflow-y: auto;
  margin-bottom: 18px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.chat-bubble {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  border-radius: 16px;
  background: #f7faff;
  box-shadow: 0 2px 8px 0 rgba(0,120,212,0.06);
  padding: 10px 16px;
  max-width: 80%;
  font-size: 1.05rem;
  animation: fadeInUp 0.4s;
}
.chat-bubble.user {
  align-self: flex-end;
  background: linear-gradient(120deg, #e3e9f7 60%, #f7faff 100%);
  color: #0078d4;
}
.chat-bubble.assistant {
  align-self: flex-start;
  background: #fff;
  color: #222;
}
.avatar {
  font-size: 1.4rem;
  margin-right: 4px;
}
.bubble-content {
  word-break: break-all;
}
.chat-input-row {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}
.fluent-input {
  border-radius: 12px;
  border: none;
  background: rgba(255,255,255,0.85);
  box-shadow: 0 2px 8px 0 rgba(0,120,212,0.06);
  padding: 10px 14px;
  font-size: 1rem;
  color: #222;
  transition: box-shadow 0.2s, border 0.2s;
  outline: none;
  flex: 1;
  min-height: 48px;
  resize: vertical;
}
.fluent-input:focus {
  box-shadow: 0 0 0 2px #0078d4;
}
.send-btn {
  min-width: 48px;
  min-height: 48px;
  border-radius: 16px;
  background: linear-gradient(120deg, #0078d4 60%, #60aaff 100%);
  color: #fff;
  border: none;
  box-shadow: 0 2px 12px 0 rgba(0,120,212,0.08);
  font-size: 1.3rem;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;
}
.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.send-btn:hover {
  background: linear-gradient(120deg, #005fa3 60%, #60aaff 100%);
}
.fluent-infer-settings {
  border-radius: 20px;
  background: rgba(255,255,255,0.85);
  box-shadow: 0 4px 24px 0 rgba(0,120,212,0.10);
  padding: 18px 18px;
}
.settings-row {
  display: flex;
  gap: 24px;
}
.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.range-value {
  font-size: 0.98rem;
  color: #0078d4;
  margin-left: 8px;
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(40px);}
  to { opacity: 1; transform: none;}
}
@media (max-width: 900px) {
  .fluent-infer-main { padding: 24px 8px; }
  .settings-row { flex-direction: column; gap: 8px; }
}
</style> 
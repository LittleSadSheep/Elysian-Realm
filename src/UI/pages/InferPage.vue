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
import './InferPage.css'
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
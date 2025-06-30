<template>
  <div class="infer-page fade-in">
    <div class="container">
      <!-- 页面标题 -->
      <div class="page-header">
        <h1 class="page-title">模型推理</h1>
        <p class="page-description">加载模型，开始对话推理</p>
      </div>

      <!-- 模型选择 -->
      <div class="model-selection card">
        <h2 class="section-title">模型选择</h2>
        <div class="model-grid grid grid-3">
          <div 
            v-for="model in availableModels" 
            :key="model.id"
            class="model-card"
            :class="{ active: selectedModel?.id === model.id }"
            @click="selectModel(model)"
          >
            <div class="model-icon">
              <Icon :icon="model.icon" />
            </div>
            <div class="model-info">
              <h3 class="model-name">{{ model.name }}</h3>
              <p class="model-size">{{ model.size }}</p>
            </div>
            <div class="model-status" :class="model.status">
              {{ model.status === 'loaded' ? '已加载' : '未加载' }}
            </div>
          </div>
        </div>
      </div>

      <!-- 对话界面 -->
      <div class="chat-interface card">
        <div class="chat-header">
          <h2 class="section-title">对话</h2>
          <div class="chat-controls">
            <button class="button secondary" @click="clearChat">
              <Icon icon="fluent:delete-24-regular" />
              清空对话
            </button>
            <button class="button secondary" @click="exportChat">
              <Icon icon="fluent:download-24-regular" />
              导出对话
            </button>
          </div>
        </div>

        <div class="chat-messages" ref="chatContainer">
          <div 
            v-for="message in chatMessages" 
            :key="message.id"
            class="message"
            :class="message.role"
          >
            <div class="message-avatar">
              <Icon :icon="message.role === 'user' ? 'fluent:person-24-regular' : 'fluent:bot-24-regular'" />
            </div>
            <div class="message-content">
              <div class="message-text">{{ message.content }}</div>
              <div class="message-time">{{ formatTime(message.timestamp) }}</div>
            </div>
          </div>
          
          <div v-if="isGenerating" class="message assistant">
            <div class="message-avatar">
              <Icon icon="fluent:bot-24-regular" />
            </div>
            <div class="message-content">
              <div class="message-text">
                <span class="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </span>
              </div>
            </div>
          </div>
        </div>

        <div class="chat-input">
          <div class="input-group">
            <textarea 
              class="textarea"
              v-model="userInput"
              placeholder="输入您的问题..."
              @keydown.enter.prevent="sendMessage"
              :disabled="!selectedModel || isGenerating"
            ></textarea>
            <button 
              class="button primary send-button"
              @click="sendMessage"
              :disabled="!userInput.trim() || !selectedModel || isGenerating"
            >
              <Icon icon="fluent:send-24-regular" />
            </button>
          </div>
        </div>
      </div>

      <!-- 参数设置 -->
      <div class="inference-settings card">
        <h2 class="section-title">推理参数</h2>
        <div class="settings-grid grid grid-3">
          <div class="form-group">
            <label class="form-label">温度 (Temperature)</label>
            <input 
              type="range" 
              class="range-input" 
              v-model="settings.temperature" 
              min="0" 
              max="2" 
              step="0.1"
            />
            <span class="range-value">{{ settings.temperature }}</span>
          </div>

          <div class="form-group">
            <label class="form-label">最大长度</label>
            <input 
              type="number" 
              class="input" 
              v-model="settings.maxLength" 
              min="100" 
              max="4096"
            />
          </div>

          <div class="form-group">
            <label class="form-label">Top P</label>
            <input 
              type="range" 
              class="range-input" 
              v-model="settings.topP" 
              min="0" 
              max="1" 
              step="0.1"
            />
            <span class="range-value">{{ settings.topP }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { Icon } from '@iconify/vue'

// 可用模型
const availableModels = ref([
  {
    id: 1,
    name: 'Llama2-7B-Chat',
    size: '7B',
    icon: 'fluent:brain-circuit-24-regular',
    status: 'loaded'
  },
  {
    id: 2,
    name: 'Qwen-7B-Chat',
    size: '7B',
    icon: 'fluent:brain-circuit-24-regular',
    status: 'unloaded'
  },
  {
    id: 3,
    name: 'ChatGLM3-6B',
    size: '6B',
    icon: 'fluent:brain-circuit-24-regular',
    status: 'unloaded'
  }
])

// 选中的模型
const selectedModel = ref(availableModels.value[0])

// 推理设置
const settings = ref({
  temperature: 0.7,
  maxLength: 2048,
  topP: 0.9
})

// 对话消息
const chatMessages = ref([
  {
    id: 1,
    role: 'assistant',
    content: '你好！我是 Elysian-Realm 的AI助手，有什么可以帮助您的吗？',
    timestamp: new Date()
  }
])

// 用户输入
const userInput = ref('')
const isGenerating = ref(false)
const chatContainer = ref<HTMLElement>()

// 选择模型
const selectModel = (model: any) => {
  selectedModel.value = model
  console.log('选择模型:', model.name)
}

// 发送消息
const sendMessage = async () => {
  if (!userInput.value.trim() || !selectedModel.value || isGenerating.value) return

  const userMessage = {
    id: Date.now(),
    role: 'user' as const,
    content: userInput.value,
    timestamp: new Date()
  }

  chatMessages.value.push(userMessage)
  const message = userInput.value
  userInput.value = ''
  isGenerating.value = true

  // 滚动到底部
  await nextTick()
  scrollToBottom()

  // 模拟AI回复
  setTimeout(() => {
    const assistantMessage = {
      id: Date.now() + 1,
      role: 'assistant' as const,
      content: `这是对"${message}"的回复。我正在使用 ${selectedModel.value?.name} 模型为您生成回答。`,
      timestamp: new Date()
    }
    chatMessages.value.push(assistantMessage)
    isGenerating.value = false
    
    nextTick(() => {
      scrollToBottom()
    })
  }, 2000)
}

// 清空对话
const clearChat = () => {
  chatMessages.value = [{
    id: Date.now(),
    role: 'assistant',
    content: '对话已清空。有什么可以帮助您的吗？',
    timestamp: new Date()
  }]
}

// 导出对话
const exportChat = () => {
  const chatText = chatMessages.value
    .map(msg => `${msg.role === 'user' ? '用户' : 'AI'}: ${msg.content}`)
    .join('\n\n')
  
  const blob = new Blob([chatText], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `chat-${new Date().toISOString().slice(0, 10)}.txt`
  a.click()
  URL.revokeObjectURL(url)
}

// 滚动到底部
const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

// 格式化时间
const formatTime = (date: Date) => {
  return date.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
.infer-page {
  padding: var(--spacing-xl) 0;
}

.page-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

.page-description {
  font-size: 16px;
  color: var(--color-text-secondary);
}

.model-selection {
  margin-bottom: var(--spacing-xl);
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-lg);
}

.model-grid {
  margin-bottom: var(--spacing-lg);
}

.model-card {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.2s ease;
}

.model-card:hover {
  border-color: var(--color-primary);
  background: var(--color-bg-secondary);
}

.model-card.active {
  border-color: var(--color-primary);
  background: var(--color-primary);
  color: white;
}

.model-icon {
  font-size: 24px;
  color: var(--color-primary);
}

.model-card.active .model-icon {
  color: white;
}

.model-info {
  flex: 1;
}

.model-name {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: var(--spacing-xs);
}

.model-size {
  font-size: 14px;
  color: var(--color-text-secondary);
}

.model-card.active .model-size {
  color: rgba(255, 255, 255, 0.8);
}

.model-status {
  font-size: 12px;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-sm);
  background: var(--color-bg-tertiary);
}

.model-status.loaded {
  background: #107c10;
  color: white;
}

.model-status.unloaded {
  background: var(--color-text-secondary);
  color: white;
}

.chat-interface {
  margin-bottom: var(--spacing-xl);
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.chat-controls {
  display: flex;
  gap: var(--spacing-sm);
}

.chat-messages {
  height: 400px;
  overflow-y: auto;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
  background: var(--color-bg-primary);
}

.message {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message.user .message-avatar {
  background: var(--color-primary);
  color: white;
}

.message-content {
  flex: 1;
}

.message-text {
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: var(--spacing-xs);
}

.message-time {
  font-size: 12px;
  color: var(--color-text-secondary);
}

.chat-input {
  margin-bottom: var(--spacing-lg);
}

.input-group {
  display: flex;
  gap: var(--spacing-sm);
}

.input-group .textarea {
  flex: 1;
  resize: none;
  min-height: 60px;
}

.send-button {
  width: 48px;
  height: 48px;
  padding: 0;
}

.typing-indicator {
  display: flex;
  gap: 4px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-text-secondary);
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

@keyframes typing {
  0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
  40% { transform: scale(1); opacity: 1; }
}

.inference-settings {
  margin-bottom: var(--spacing-xl);
}

.settings-grid {
  margin-bottom: var(--spacing-lg);
}

.form-group {
  margin-bottom: var(--spacing-md);
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

.range-input {
  width: 100%;
  margin-bottom: var(--spacing-xs);
}

.range-value {
  font-size: 12px;
  color: var(--color-text-secondary);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .model-grid,
  .settings-grid {
    grid-template-columns: 1fr;
  }
  
  .chat-header {
    flex-direction: column;
    gap: var(--spacing-md);
    align-items: flex-start;
  }
  
  .chat-controls {
    width: 100%;
    justify-content: space-between;
  }
  
  .input-group {
    flex-direction: column;
  }
  
  .send-button {
    width: 100%;
    height: 40px;
  }
}
</style> 
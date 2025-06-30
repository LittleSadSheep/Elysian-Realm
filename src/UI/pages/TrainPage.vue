<template>
  <div class="train-page fade-in">
    <div class="container">
      <!-- 页面标题 -->
      <div class="page-header">
        <h1 class="page-title">模型训练</h1>
        <p class="page-description">配置训练参数，开始模型微调过程</p>
      </div>

      <!-- 训练配置表单 -->
      <div class="train-config card">
        <h2 class="section-title">训练配置</h2>
        <div class="config-grid grid grid-2">
          <div class="form-group">
            <label class="form-label">基础模型</label>
            <select class="select" v-model="config.baseModel">
              <option value="llama2-7b">Llama2-7B</option>
              <option value="llama2-13b">Llama2-13B</option>
              <option value="qwen-7b">Qwen-7B</option>
              <option value="chatglm3-6b">ChatGLM3-6B</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">微调方法</label>
            <select class="select" v-model="config.finetuneMethod">
              <option value="qlora">QLoRA</option>
              <option value="lora">LoRA</option>
              <option value="full">全参数微调</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">学习率</label>
            <input type="number" class="input" v-model="config.learningRate" step="0.0001" min="0.0001" max="0.1" />
          </div>

          <div class="form-group">
            <label class="form-label">批次大小</label>
            <input type="number" class="input" v-model="config.batchSize" min="1" max="32" />
          </div>

          <div class="form-group">
            <label class="form-label">训练轮数</label>
            <input type="number" class="input" v-model="config.epochs" min="1" max="100" />
          </div>

          <div class="form-group">
            <label class="form-label">最大序列长度</label>
            <input type="number" class="input" v-model="config.maxLength" min="512" max="4096" />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">训练数据路径</label>
          <div class="file-input-group">
            <input type="text" class="input" v-model="config.dataPath" placeholder="选择训练数据文件或目录" readonly />
            <button class="button secondary" @click="selectDataPath">浏览</button>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">输出目录</label>
          <div class="file-input-group">
            <input type="text" class="input" v-model="config.outputPath" placeholder="选择模型输出目录" readonly />
            <button class="button secondary" @click="selectOutputPath">浏览</button>
          </div>
        </div>
      </div>

      <!-- 高级配置 -->
      <div class="advanced-config card">
        <h2 class="section-title">高级配置</h2>
        <div class="config-grid grid grid-2">
          <div class="form-group">
            <label class="form-label">LoRA Rank</label>
            <input type="number" class="input" v-model="config.loraRank" min="8" max="256" />
          </div>

          <div class="form-group">
            <label class="form-label">LoRA Alpha</label>
            <input type="number" class="input" v-model="config.loraAlpha" min="8" max="256" />
          </div>

          <div class="form-group">
            <label class="form-label">权重衰减</label>
            <input type="number" class="input" v-model="config.weightDecay" step="0.01" min="0" max="1" />
          </div>

          <div class="form-group">
            <label class="form-label">梯度累积步数</label>
            <input type="number" class="input" v-model="config.gradientAccumulation" min="1" max="16" />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">训练目标</label>
          <textarea class="textarea" v-model="config.promptTemplate" placeholder="输入训练提示模板，例如：### 指令：{instruction}\n### 回答：{response}"></textarea>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <button class="button secondary" @click="validateConfig">验证配置</button>
        <button class="button primary" @click="startTraining" :disabled="!isConfigValid || isTraining">
          <Icon icon="fluent:play-24-regular" v-if="!isTraining" />
          <Icon icon="fluent:stop-24-regular" v-else />
          {{ isTraining ? '停止训练' : '开始训练' }}
        </button>
      </div>

      <!-- 训练状态 -->
      <div v-if="isTraining" class="training-status card">
        <h2 class="section-title">训练状态</h2>
        <div class="status-grid grid grid-3">
          <div class="status-item">
            <div class="status-label">当前轮数</div>
            <div class="status-value">{{ trainingStatus.currentEpoch }}/{{ config.epochs }}</div>
          </div>
          <div class="status-item">
            <div class="status-label">损失值</div>
            <div class="status-value">{{ trainingStatus.loss.toFixed(4) }}</div>
          </div>
          <div class="status-item">
            <div class="status-label">训练时间</div>
            <div class="status-value">{{ formatTime(trainingStatus.elapsedTime) }}</div>
          </div>
        </div>
        
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: `${trainingStatus.progress}%` }"></div>
        </div>
        
        <div class="training-log">
          <h3>训练日志</h3>
          <div class="log-content">
            <div v-for="log in trainingLogs" :key="log.id" class="log-entry">
              <span class="log-time">{{ log.time }}</span>
              <span class="log-message">{{ log.message }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Icon } from '@iconify/vue'

// 训练配置
const config = ref({
  baseModel: 'llama2-7b',
  finetuneMethod: 'qlora',
  learningRate: 0.0002,
  batchSize: 4,
  epochs: 3,
  maxLength: 2048,
  dataPath: '',
  outputPath: '',
  loraRank: 64,
  loraAlpha: 16,
  weightDecay: 0.01,
  gradientAccumulation: 4,
  promptTemplate: '### 指令：{instruction}\n### 回答：{response}'
})

// 训练状态
const isTraining = ref(false)
const isConfigValid = ref(false)
const trainingStatus = ref({
  currentEpoch: 0,
  loss: 0,
  elapsedTime: 0,
  progress: 0
})

const trainingLogs = ref([
  { id: 1, time: '12:00:00', message: '开始训练...' },
  { id: 2, time: '12:00:05', message: '加载模型完成' },
  { id: 3, time: '12:00:10', message: '开始第1轮训练' }
])

// 选择文件路径
const selectDataPath = () => {
  // TODO: 实现文件选择逻辑
  console.log('选择数据路径')
}

const selectOutputPath = () => {
  // TODO: 实现文件选择逻辑
  console.log('选择输出路径')
}

// 验证配置
const validateConfig = () => {
  // TODO: 实现配置验证逻辑
  isConfigValid.value = true
  console.log('配置验证通过')
}

// 开始训练
const startTraining = () => {
  if (isTraining.value) {
    isTraining.value = false
    console.log('停止训练')
  } else {
    isTraining.value = true
    console.log('开始训练')
    // TODO: 实现训练逻辑
  }
}

// 格式化时间
const formatTime = (seconds: number) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}
</script>

<style scoped>
.train-page {
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

.train-config,
.advanced-config {
  margin-bottom: var(--spacing-xl);
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-lg);
}

.config-grid {
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

.file-input-group {
  display: flex;
  gap: var(--spacing-sm);
}

.file-input-group .input {
  flex: 1;
}

.action-buttons {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  margin-bottom: var(--spacing-xl);
}

.training-status {
  margin-bottom: var(--spacing-xl);
}

.status-grid {
  margin-bottom: var(--spacing-lg);
}

.status-item {
  text-align: center;
}

.status-label {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-xs);
}

.status-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: var(--color-bg-tertiary);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: var(--spacing-lg);
}

.progress-fill {
  height: 100%;
  background: var(--color-primary);
  transition: width 0.3s ease;
}

.training-log h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
}

.log-content {
  max-height: 200px;
  overflow-y: auto;
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
}

.log-entry {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-sm);
  font-size: 12px;
  font-family: 'Consolas', 'Monaco', monospace;
}

.log-time {
  color: var(--color-text-secondary);
  min-width: 80px;
}

.log-message {
  color: var(--color-text-primary);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .config-grid {
    grid-template-columns: 1fr;
  }
  
  .status-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .file-input-group {
    flex-direction: column;
  }
}
</style> 
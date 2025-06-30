<template>
  <div class="tune-page fade-in">
    <div class="container">
      <!-- 页面标题 -->
      <div class="page-header">
        <h1 class="page-title">参数调优</h1>
        <p class="page-description">基于 Optuna 的超参数优化，自动寻找最佳训练配置</p>
      </div>

      <!-- 优化配置 -->
      <div class="optimization-config card">
        <h2 class="section-title">优化配置</h2>
        <div class="config-grid grid grid-2">
          <div class="form-group">
            <label class="form-label">优化目标</label>
            <select class="select" v-model="config.objective">
              <option value="loss">最小化损失</option>
              <option value="accuracy">最大化准确率</option>
              <option value="f1">最大化F1分数</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">试验次数</label>
            <input type="number" class="input" v-model="config.nTrials" min="10" max="1000" />
          </div>

          <div class="form-group">
            <label class="form-label">超时时间 (分钟)</label>
            <input type="number" class="input" v-model="config.timeout" min="10" max="1440" />
          </div>

          <div class="form-group">
            <label class="form-label">并行试验数</label>
            <input type="number" class="input" v-model="config.nJobs" min="1" max="8" />
          </div>
        </div>
      </div>

      <!-- 超参数空间 -->
      <div class="hyperparameter-space card">
        <h2 class="section-title">超参数空间</h2>
        <div class="params-grid grid grid-2">
          <div class="param-group">
            <h3 class="param-title">学习率</h3>
            <div class="param-range">
              <label>最小值</label>
              <input type="number" class="input" v-model="params.learningRate.min" step="0.0001" />
            </div>
            <div class="param-range">
              <label>最大值</label>
              <input type="number" class="input" v-model="params.learningRate.max" step="0.0001" />
            </div>
          </div>

          <div class="param-group">
            <h3 class="param-title">批次大小</h3>
            <div class="param-options">
              <label v-for="size in [1, 2, 4, 8, 16, 32]" :key="size" class="checkbox-label">
                <input type="checkbox" v-model="params.batchSize" :value="size" />
                {{ size }}
              </label>
            </div>
          </div>

          <div class="param-group">
            <h3 class="param-title">LoRA Rank</h3>
            <div class="param-range">
              <label>最小值</label>
              <input type="number" class="input" v-model="params.loraRank.min" min="8" max="256" />
            </div>
            <div class="param-range">
              <label>最大值</label>
              <input type="number" class="input" v-model="params.loraRank.max" min="8" max="256" />
            </div>
          </div>

          <div class="param-group">
            <h3 class="param-title">权重衰减</h3>
            <div class="param-range">
              <label>最小值</label>
              <input type="number" class="input" v-model="params.weightDecay.min" step="0.001" min="0" max="1" />
            </div>
            <div class="param-range">
              <label>最大值</label>
              <input type="number" class="input" v-model="params.weightDecay.max" step="0.001" min="0" max="1" />
            </div>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <button class="button secondary" @click="validateConfig">验证配置</button>
        <button class="button primary" @click="startOptimization" :disabled="!isConfigValid || isOptimizing">
          <Icon icon="fluent:play-24-regular" v-if="!isOptimizing" />
          <Icon icon="fluent:stop-24-regular" v-else />
          {{ isOptimizing ? '停止优化' : '开始优化' }}
        </button>
      </div>

      <!-- 优化进度 -->
      <div v-if="isOptimizing" class="optimization-progress card">
        <h2 class="section-title">优化进度</h2>
        <div class="progress-stats grid grid-4">
          <div class="stat-item">
            <div class="stat-label">当前试验</div>
            <div class="stat-value">{{ optimizationStatus.currentTrial }}/{{ config.nTrials }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">最佳分数</div>
            <div class="stat-value">{{ optimizationStatus.bestScore.toFixed(4) }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">运行时间</div>
            <div class="stat-value">{{ formatTime(optimizationStatus.elapsedTime) }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">剩余时间</div>
            <div class="stat-value">{{ formatTime(optimizationStatus.remainingTime) }}</div>
          </div>
        </div>

        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: `${optimizationStatus.progress}%` }"></div>
        </div>

        <div class="optimization-log">
          <h3>优化日志</h3>
          <div class="log-content">
            <div v-for="log in optimizationLogs" :key="log.id" class="log-entry">
              <span class="log-time">{{ log.time }}</span>
              <span class="log-trial">试验 #{{ log.trial }}</span>
              <span class="log-score">分数: {{ log.score.toFixed(4) }}</span>
              <span class="log-message">{{ log.message }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 最佳结果 -->
      <div v-if="bestResult" class="best-result card">
        <h2 class="section-title">最佳结果</h2>
        <div class="result-summary">
          <div class="result-score">
            <span class="score-label">最佳分数</span>
            <span class="score-value">{{ bestResult.score.toFixed(4) }}</span>
          </div>
          <div class="result-params">
            <h3>最佳参数</h3>
            <div class="params-list">
              <div v-for="(value, key) in bestResult.params" :key="key" class="param-item">
                <span class="param-name">{{ key }}</span>
                <span class="param-value">{{ value }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="result-actions">
          <button class="button secondary" @click="exportResult">导出结果</button>
          <button class="button primary" @click="applyResult">应用参数</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Icon } from '@iconify/vue'

// 优化配置
const config = ref({
  objective: 'loss',
  nTrials: 100,
  timeout: 60,
  nJobs: 1
})

// 超参数空间
const params = ref({
  learningRate: { min: 0.0001, max: 0.01 },
  batchSize: [4, 8, 16],
  loraRank: { min: 16, max: 128 },
  weightDecay: { min: 0.001, max: 0.1 }
})

// 优化状态
const isOptimizing = ref(false)
const isConfigValid = ref(false)
const optimizationStatus = ref({
  currentTrial: 0,
  bestScore: 0,
  elapsedTime: 0,
  remainingTime: 0,
  progress: 0
})

const optimizationLogs = ref([
  { id: 1, time: '12:00:00', trial: 1, score: 0.2345, message: '开始第1次试验' },
  { id: 2, time: '12:00:30', trial: 2, score: 0.1987, message: '第2次试验完成，发现更好的参数' },
  { id: 3, time: '12:01:00', trial: 3, score: 0.2456, message: '第3次试验完成' }
])

const bestResult = ref({
  score: 0.1987,
  params: {
    learningRate: 0.0005,
    batchSize: 8,
    loraRank: 64,
    weightDecay: 0.01
  }
})

// 验证配置
const validateConfig = () => {
  // TODO: 实现配置验证逻辑
  isConfigValid.value = true
  console.log('配置验证通过')
}

// 开始优化
const startOptimization = () => {
  if (isOptimizing.value) {
    isOptimizing.value = false
    console.log('停止优化')
  } else {
    isOptimizing.value = true
    console.log('开始优化')
    // TODO: 实现优化逻辑
  }
}

// 导出结果
const exportResult = () => {
  const resultData = {
    config: config.value,
    params: params.value,
    bestResult: bestResult.value,
    timestamp: new Date().toISOString()
  }
  
  const blob = new Blob([JSON.stringify(resultData, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `optimization-result-${new Date().toISOString().slice(0, 10)}.json`
  a.click()
  URL.revokeObjectURL(url)
}

// 应用参数
const applyResult = () => {
  console.log('应用最佳参数:', bestResult.value.params)
  // TODO: 实现参数应用逻辑
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
.tune-page {
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

.optimization-config,
.hyperparameter-space {
  margin-bottom: var(--spacing-xl);
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-lg);
}

.config-grid,
.params-grid {
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

.param-group {
  margin-bottom: var(--spacing-lg);
}

.param-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
}

.param-range {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-sm);
}

.param-range label {
  font-size: 14px;
  color: var(--color-text-secondary);
  min-width: 60px;
}

.param-range .input {
  flex: 1;
}

.param-options {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: 14px;
  color: var(--color-text-primary);
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 16px;
  height: 16px;
}

.action-buttons {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  margin-bottom: var(--spacing-xl);
}

.optimization-progress {
  margin-bottom: var(--spacing-xl);
}

.progress-stats {
  margin-bottom: var(--spacing-lg);
}

.stat-item {
  text-align: center;
}

.stat-label {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-xs);
}

.stat-value {
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

.optimization-log h3 {
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

.log-trial {
  color: var(--color-primary);
  min-width: 60px;
}

.log-score {
  color: var(--color-text-secondary);
  min-width: 80px;
}

.log-message {
  color: var(--color-text-primary);
  flex: 1;
}

.best-result {
  margin-bottom: var(--spacing-xl);
}

.result-summary {
  margin-bottom: var(--spacing-lg);
}

.result-score {
  text-align: center;
  margin-bottom: var(--spacing-lg);
}

.score-label {
  display: block;
  font-size: 14px;
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-sm);
}

.score-value {
  font-size: 48px;
  font-weight: 700;
  color: var(--color-primary);
}

.result-params h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
}

.params-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-sm);
}

.param-item {
  display: flex;
  justify-content: space-between;
  padding: var(--spacing-sm);
  background: var(--color-bg-secondary);
  border-radius: var(--radius-sm);
}

.param-name {
  font-size: 14px;
  color: var(--color-text-secondary);
}

.param-value {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.result-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .config-grid,
  .params-grid {
    grid-template-columns: 1fr;
  }
  
  .progress-stats {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .params-list {
    grid-template-columns: 1fr;
  }
  
  .action-buttons,
  .result-actions {
    flex-direction: column;
  }
  
  .param-range {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .param-range .input {
    width: 100%;
  }
}
</style> 
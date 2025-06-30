<template>
  <div class="fluent-tune-root">
    <div class="fluent-tune-main glass">
      <div class="fluent-tune-header">
        <h1>超参数调优</h1>
        <div class="desc">自动搜索最佳训练参数，提升模型效果</div>
      </div>
      <form class="fluent-tune-form">
        <div class="form-row">
          <div class="form-group">
            <label>搜索算法</label>
            <select v-model="config.searchAlgo" class="fluent-input">
              <option value="optuna">Optuna</option>
              <option value="grid">网格搜索</option>
              <option value="random">随机搜索</option>
            </select>
          </div>
          <div class="form-group">
            <label>最大试验数</label>
            <input type="number" v-model="config.maxTrials" class="fluent-input" min="1" max="100" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>学习率范围</label>
            <input type="text" v-model="config.lrRange" class="fluent-input" placeholder="如 0.0001-0.01" />
          </div>
          <div class="form-group">
            <label>批次大小范围</label>
            <input type="text" v-model="config.bsRange" class="fluent-input" placeholder="如 2-16" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>目标指标</label>
            <select v-model="config.metric" class="fluent-input">
              <option value="loss">损失值</option>
              <option value="accuracy">准确率</option>
              <option value="f1">F1分数</option>
            </select>
          </div>
          <div class="form-group">
            <label>优化方向</label>
            <select v-model="config.direction" class="fluent-input">
              <option value="minimize">最小化</option>
              <option value="maximize">最大化</option>
            </select>
          </div>
        </div>
        <div class="form-actions">
          <button type="button" class="fluent-btn secondary" @click="validateConfig">验证配置</button>
          <button type="button" class="fluent-btn primary" @click="startTuning" :disabled="!isConfigValid || isTuning">
            <Icon icon="fluent:wand-24-regular" v-if="!isTuning" />
            <Icon icon="fluent:stop-24-regular" v-else />
            {{ isTuning ? '停止调优' : '开始调优' }}
          </button>
        </div>
      </form>
      <div v-if="isTuning" class="fluent-tune-status glass">
        <div class="status-row">
          <div>当前试验：{{ tuneStatus.currentTrial }}/{{ config.maxTrials }}</div>
          <div>最佳指标：{{ tuneStatus.bestMetric }}</div>
          <div>已用时间：{{ formatTime(tuneStatus.elapsedTime) }}</div>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: `${tuneStatus.progress}%` }"></div>
        </div>
        <div class="tune-log">
          <h3>调优日志</h3>
          <div class="log-content">
            <div v-for="log in tuneLogs" :key="log.id" class="log-entry">
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
import { ref } from 'vue'
import { Icon } from '@iconify/vue'

// 优化配置
const config = ref({
  searchAlgo: 'optuna',
  maxTrials: 10,
  lrRange: '0.0001-0.01',
  bsRange: '2-16',
  metric: 'loss',
  direction: 'minimize'
})

// 优化状态
const isTuning = ref(false)
const isConfigValid = ref(false)
const tuneStatus = ref({ currentTrial: 0, bestMetric: 0.1234, elapsedTime: 0, progress: 0 })
const tuneLogs = ref([{ id: 1, time: '12:00:00', message: '开始调优...' }])

// 验证配置
const validateConfig = () => {
  // TODO: 实现配置验证逻辑
  isConfigValid.value = true
  console.log('配置验证通过')
}

// 开始优化
const startTuning = () => {
  if (isTuning.value) {
    isTuning.value = false
    console.log('停止优化')
  } else {
    isTuning.value = true
    console.log('开始优化')
    // TODO: 实现优化逻辑
  }
}

// 格式化时间
const formatTime = (s: number) => `${Math.floor(s/3600).toString().padStart(2,'0')}:${Math.floor((s%3600)/60).toString().padStart(2,'0')}:${(s%60).toString().padStart(2,'0')}`
</script>

<style scoped>
.fluent-tune-root {
  min-height: 100vh;
  background: linear-gradient(135deg, #e3e9f700 0%, #f7faff00 40%, #f6f3ff00 70%rgba(249, 246, 243, 0)f3 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}
.fluent-tune-main {
  width: 100%;
  max-width: 800px;
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
.fluent-tune-header h1 {
  font-size: 2.2rem;
  font-weight: 800;
  color: #222;
  margin-bottom: 8px;
}
.fluent-tune-header .desc {
  color: #0078d4;
  font-size: 1.1rem;
  font-weight: 600;
}
.fluent-tune-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.form-row {
  display: flex;
  gap: 18px;
}
.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
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
}
.fluent-input:focus {
  box-shadow: 0 0 0 2px #0078d4;
}
.form-actions {
  display: flex;
  gap: 18px;
  justify-content: flex-end;
  margin-top: 8px;
}
.fluent-btn {
  border: none;
  border-radius: 16px;
  box-shadow: 0 2px 12px 0 rgba(0,120,212,0.08);
  font-size: 1.1rem;
  font-weight: 600;
  padding: 12px 32px;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s, color 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}
.fluent-btn.primary {
  background: linear-gradient(120deg, #0078d4 60%, #60aaff 100%);
  color: #fff;
}
.fluent-btn.primary:hover {
  background: linear-gradient(120deg, #005fa3 60%, #60aaff 100%);
}
.fluent-btn.secondary {
  background: #f7faff;
  color: #0078d4;
}
.fluent-btn.secondary:hover {
  background: #e3e9f7;
  color: #005fa3;
}
.fluent-tune-status {
  margin-top: 24px;
  border-radius: 20px;
  background: rgba(255,255,255,0.85);
  box-shadow: 0 4px 24px 0 rgba(0,120,212,0.10);
  padding: 24px 18px;
  animation: fadeInUp 0.6s;
}
.status-row {
  display: flex;
  gap: 32px;
  font-size: 1.1rem;
  color: #0078d4;
  font-weight: 600;
  margin-bottom: 12px;
}
.progress-bar {
  width: 100%;
  height: 8px;
  background: #e3e9f7;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 18px;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #0078d4 0%, #60aaff 100%);
  transition: width 0.3s;
}
.tune-log h3 {
  font-size: 1.1rem;
  color: #222;
  margin-bottom: 8px;
}
.log-content {
  max-height: 120px;
  overflow-y: auto;
  background: #f7faff;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 0.98rem;
}
.log-entry {
  display: flex;
  gap: 18px;
  margin-bottom: 4px;
  color: #444;
}
.log-time {
  color: #0078d4;
  min-width: 70px;
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(40px);}
  to { opacity: 1; transform: none;}
}
@media (max-width: 900px) {
  .fluent-tune-main { padding: 24px 8px; }
  .form-row { flex-direction: column; gap: 8px; }
}
</style> 
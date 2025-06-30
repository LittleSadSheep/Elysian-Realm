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
import './TunePage.css'
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
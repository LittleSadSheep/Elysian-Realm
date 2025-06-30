<template>
  <div class="fluent-train-root">
    <div class="fluent-train-main glass">
      <div class="fluent-train-header">
        <h1>模型训练</h1>
        <div class="desc">配置训练参数，开始模型微调过程</div>
      </div>
      <form class="fluent-train-form">
        <div class="form-row">
          <div class="form-group">
            <label>基础模型</label>
            <select v-model="config.baseModel" class="fluent-input">
              <option value="llama2-7b">Llama2-7B</option>
              <option value="llama2-13b">Llama2-13B</option>
              <option value="qwen-7b">Qwen-7B</option>
              <option value="chatglm3-6b">ChatGLM3-6B</option>
            </select>
          </div>
          <div class="form-group">
            <label>微调方法</label>
            <select v-model="config.finetuneMethod" class="fluent-input">
              <option value="qlora">QLoRA</option>
              <option value="lora">LoRA</option>
              <option value="full">全参数微调</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>学习率</label>
            <input type="number" v-model="config.learningRate" class="fluent-input" step="0.0001" min="0.0001" max="0.1" />
          </div>
          <div class="form-group">
            <label>批次大小</label>
            <input type="number" v-model="config.batchSize" class="fluent-input" min="1" max="32" />
          </div>
          <div class="form-group">
            <label>训练轮数</label>
            <input type="number" v-model="config.epochs" class="fluent-input" min="1" max="100" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>训练数据路径</label>
            <input type="text" v-model="config.dataPath" class="fluent-input" placeholder="选择训练数据文件或目录" readonly />
          </div>
          <div class="form-group">
            <label>输出目录</label>
            <input type="text" v-model="config.outputPath" class="fluent-input" placeholder="选择模型输出目录" readonly />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>LoRA Rank</label>
            <input type="number" v-model="config.loraRank" class="fluent-input" min="8" max="256" />
          </div>
          <div class="form-group">
            <label>LoRA Alpha</label>
            <input type="number" v-model="config.loraAlpha" class="fluent-input" min="8" max="256" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>训练目标</label>
            <textarea v-model="config.promptTemplate" class="fluent-input" rows="2" placeholder="输入训练提示模板"></textarea>
          </div>
        </div>
        <div class="form-actions">
          <button type="button" class="fluent-btn secondary" @click="validateConfig">验证配置</button>
          <button type="button" class="fluent-btn primary" @click="startTraining" :disabled="!isConfigValid || isTraining">
            <Icon icon="fluent:play-24-regular" v-if="!isTraining" />
            <Icon icon="fluent:stop-24-regular" v-else />
            {{ isTraining ? '停止训练' : '开始训练' }}
          </button>
        </div>
      </form>
      <div v-if="isTraining" class="fluent-train-status glass">
        <div class="status-row">
          <div>当前轮数：{{ trainingStatus.currentEpoch }}/{{ config.epochs }}</div>
          <div>损失值：{{ trainingStatus.loss.toFixed(4) }}</div>
          <div>训练时间：{{ formatTime(trainingStatus.elapsedTime) }}</div>
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
import { ref } from 'vue'
import { Icon } from '@iconify/vue'

// 训练配置
const config = ref({
  baseModel: 'llama2-7b',
  finetuneMethod: 'qlora',
  learningRate: 0.0002,
  batchSize: 4,
  epochs: 3,
  dataPath: '',
  outputPath: '',
  loraRank: 64,
  loraAlpha: 16,
  promptTemplate: '### 指令：{instruction}\n### 回答：{response}'
})

// 训练状态
const isTraining = ref(false)
const isConfigValid = ref(false)
const trainingStatus = ref({ currentEpoch: 0, loss: 0, elapsedTime: 0, progress: 0 })
const trainingLogs = ref([{ id: 1, time: '12:00:00', message: '开始训练...' }])

// 验证配置
const validateConfig = () => {
  isConfigValid.value = true
}

// 开始训练
const startTraining = () => {
  isTraining.value = !isTraining.value
}

// 格式化时间
const formatTime = (s: number) => `${Math.floor(s/3600).toString().padStart(2,'0')}:${Math.floor((s%3600)/60).toString().padStart(2,'0')}:${(s%60).toString().padStart(2,'0')}`
</script>

<style scoped>
.fluent-train-root {
  min-height: 100vh;
  background: linear-gradient(135deg, #e3e9f7 0%, #f7faff 40%, #f6f3ff 70%, #f9f6f3 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}
.fluent-train-main {
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
.fluent-train-header h1 {
  font-size: 2.2rem;
  font-weight: 800;
  color: #222;
  margin-bottom: 8px;
}
.fluent-train-header .desc {
  color: #0078d4;
  font-size: 1.1rem;
  font-weight: 600;
}
.fluent-train-form {
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
textarea.fluent-input {
  min-height: 48px;
  resize: vertical;
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
.fluent-train-status {
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
.training-log h3 {
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
  .fluent-train-main { padding: 24px 8px; }
  .form-row { flex-direction: column; gap: 8px; }
}
</style> 
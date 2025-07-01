<template>
    <div class="fluent-train-main glass">
      <div class="fluent-train-header">
        <h1>模型训练</h1>
        <div class="desc">配置训练参数，开始模型微调过程</div>
        <br>
        <p style="text-indent:2em">
          这是描述这是描述这是描述这是描述这是描述这是<br>
          这是描述这是描述这是描述这是描述这是描述这是描述
          这是描述这是描述这是描述这是描述这是描述这是描述
          这是描述这是描述这是描述这是描述这是描述这是描述
          这是描述这是描述这是描述这是描述这是描述这是描述
          这是描述这是描述这是描述这是描述这是描述这是描述
          这是描述这是描述这是描述这是描述这是描述这是描述
          这是描述这是描述这是描述这是描述这是描述这是描述
          这是描述这是描述这是描述这是描述这是描述这是描述
          这是描述这是描述这是描述这是描述这是描述这是描述
          这是描述这是描述这是描述这是描述这是描述这是描述
          这是描述这是描述这是描述这是描述这是描述这是描述
          这是描述这是描述这是描述这是描述这是描述这是描述
          这是描述这是描述这是描述这是描述这是描述这是描述
          这是描述这是描述这是描述这是描述这是描述这是描述
          这是描述这是描述这是描述这是描述这是描述这是描述
          这是描述这是描述这是描述这是描述这是描述这是描述
          这是描述这是描述这是描述这是描述这是描述这是描述
          这是描述这是描述这是描述这是描述
        </p>
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
</template>

<script setup lang="ts">
import './TrainPage.css'
import { ref, Text } from 'vue'
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
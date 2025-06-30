<template>
  <div class="model-page fade-in">
    <div class="container">
      <!-- 页面标题 -->
      <div class="page-header">
        <h1 class="page-title">模型管理</h1>
        <p class="page-description">统一的模型存储和管理，支持多种格式转换和版本控制</p>
      </div>

      <!-- 模型列表 -->
      <div class="model-list card">
        <div class="list-header">
          <h2 class="section-title">模型列表</h2>
          <div class="list-controls">
            <button class="button secondary" @click="refreshModels">
              <Icon icon="fluent:refresh-24-regular" />
              刷新
            </button>
            <button class="button primary" @click="importModel">
              <Icon icon="fluent:add-24-regular" />
              导入模型
            </button>
          </div>
        </div>

        <div class="models-grid grid grid-3">
          <div 
            v-for="model in models" 
            :key="model.id"
            class="model-item"
            :class="{ active: selectedModel?.id === model.id }"
            @click="selectModel(model)"
          >
            <div class="model-header">
              <div class="model-icon">
                <Icon :icon="model.icon" />
              </div>
              <div class="model-status" :class="model.status">
                {{ model.status === 'loaded' ? '已加载' : '未加载' }}
              </div>
            </div>
            
            <div class="model-info">
              <h3 class="model-name">{{ model.name }}</h3>
              <p class="model-version">{{ model.version }}</p>
              <p class="model-size">{{ formatSize(model.size) }}</p>
              <p class="model-format">{{ model.format }}</p>
            </div>
            
            <div class="model-actions">
              <button class="action-btn" @click.stop="loadModel(model)" :disabled="model.status === 'loaded'">
                <Icon icon="fluent:play-24-regular" />
              </button>
              <button class="action-btn" @click.stop="convertModel(model)">
                <Icon icon="fluent:arrow-swap-24-regular" />
              </button>
              <button class="action-btn" @click.stop="deleteModel(model)">
                <Icon icon="fluent:delete-24-regular" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 模型详情 -->
      <div v-if="selectedModel" class="model-details card">
        <h2 class="section-title">模型详情</h2>
        <div class="details-grid grid grid-2">
          <div class="detail-group">
            <h3>基本信息</h3>
            <div class="detail-item">
              <span class="detail-label">名称</span>
              <span class="detail-value">{{ selectedModel.name }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">版本</span>
              <span class="detail-value">{{ selectedModel.version }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">大小</span>
              <span class="detail-value">{{ formatSize(selectedModel.size) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">格式</span>
              <span class="detail-value">{{ selectedModel.format }}</span>
            </div>
          </div>
          
          <div class="detail-group">
            <h3>训练信息</h3>
            <div class="detail-item">
              <span class="detail-label">基础模型</span>
              <span class="detail-value">{{ selectedModel.baseModel }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">微调方法</span>
              <span class="detail-value">{{ selectedModel.finetuneMethod }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">训练轮数</span>
              <span class="detail-value">{{ selectedModel.epochs }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">创建时间</span>
              <span class="detail-value">{{ formatDate(selectedModel.createdAt) }}</span>
            </div>
          </div>
        </div>
        
        <div class="detail-actions">
          <button class="button secondary" @click="exportModel">导出模型</button>
          <button class="button secondary" @click="shareModel">分享模型</button>
          <button class="button primary" @click="useModel">使用模型</button>
        </div>
      </div>

      <!-- 转换对话框 -->
      <div v-if="showConvertDialog" class="convert-dialog">
        <div class="dialog-content card">
          <h3>模型格式转换</h3>
          <div class="convert-form">
            <div class="form-group">
              <label class="form-label">目标格式</label>
              <select class="select" v-model="convertConfig.targetFormat">
                <option value="gguf">GGUF</option>
                <option value="safetensors">SafeTensors</option>
                <option value="pytorch">PyTorch</option>
                <option value="onnx">ONNX</option>
              </select>
            </div>
            
            <div class="form-group">
              <label class="form-label">量化级别</label>
              <select class="select" v-model="convertConfig.quantization">
                <option value="none">无量化</option>
                <option value="q4_0">Q4_0</option>
                <option value="q4_1">Q4_1</option>
                <option value="q5_0">Q5_0</option>
                <option value="q5_1">Q5_1</option>
                <option value="q8_0">Q8_0</option>
              </select>
            </div>
            
            <div class="dialog-actions">
              <button class="button secondary" @click="cancelConvert">取消</button>
              <button class="button primary" @click="startConvert">开始转换</button>
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

// 模型列表
const models = ref([
  {
    id: 1,
    name: 'Llama2-7B-Chat',
    version: 'v1.0',
    size: 13743895347, // 13.7GB
    format: 'GGUF',
    status: 'loaded',
    icon: 'fluent:brain-circuit-24-regular',
    baseModel: 'Llama2-7B',
    finetuneMethod: 'QLoRA',
    epochs: 3,
    createdAt: new Date('2024-01-15')
  },
  {
    id: 2,
    name: 'Qwen-7B-Chat',
    version: 'v2.1',
    size: 14566133760, // 14.5GB
    format: 'SafeTensors',
    status: 'unloaded',
    icon: 'fluent:brain-circuit-24-regular',
    baseModel: 'Qwen-7B',
    finetuneMethod: 'LoRA',
    epochs: 5,
    createdAt: new Date('2024-01-20')
  },
  {
    id: 3,
    name: 'ChatGLM3-6B',
    version: 'v1.2',
    size: 12079595520, // 12GB
    format: 'PyTorch',
    status: 'unloaded',
    icon: 'fluent:brain-circuit-24-regular',
    baseModel: 'ChatGLM3-6B',
    finetuneMethod: '全参数',
    epochs: 2,
    createdAt: new Date('2024-01-25')
  }
])

// 选中的模型
const selectedModel = ref(models.value[0])

// 转换对话框
const showConvertDialog = ref(false)
const convertConfig = ref({
  targetFormat: 'gguf',
  quantization: 'q4_0'
})

// 选择模型
const selectModel = (model: any) => {
  selectedModel.value = model
}

// 加载模型
const loadModel = (model: any) => {
  model.status = 'loaded'
  console.log('加载模型:', model.name)
}

// 转换模型
const convertModel = (model: any) => {
  selectedModel.value = model
  showConvertDialog.value = true
}

// 删除模型
const deleteModel = (model: any) => {
  if (confirm(`确定要删除模型 "${model.name}" 吗？`)) {
    const index = models.value.findIndex(m => m.id === model.id)
    if (index > -1) {
      models.value.splice(index, 1)
      if (selectedModel.value?.id === model.id) {
        selectedModel.value = models.value[0] || null
      }
    }
  }
}

// 刷新模型列表
const refreshModels = () => {
  console.log('刷新模型列表')
  // TODO: 实现刷新逻辑
}

// 导入模型
const importModel = () => {
  console.log('导入模型')
  // TODO: 实现导入逻辑
}

// 导出模型
const exportModel = () => {
  console.log('导出模型:', selectedModel.value?.name)
  // TODO: 实现导出逻辑
}

// 分享模型
const shareModel = () => {
  console.log('分享模型:', selectedModel.value?.name)
  // TODO: 实现分享逻辑
}

// 使用模型
const useModel = () => {
  console.log('使用模型:', selectedModel.value?.name)
  // TODO: 实现使用逻辑
}

// 取消转换
const cancelConvert = () => {
  showConvertDialog.value = false
}

// 开始转换
const startConvert = () => {
  console.log('开始转换:', convertConfig.value)
  showConvertDialog.value = false
  // TODO: 实现转换逻辑
}

// 格式化文件大小
const formatSize = (bytes: number) => {
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  if (bytes === 0) return '0 B'
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`
}

// 格式化日期
const formatDate = (date: Date) => {
  return date.toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.model-page {
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

.model-list {
  margin-bottom: var(--spacing-xl);
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.list-controls {
  display: flex;
  gap: var(--spacing-sm);
}

.models-grid {
  margin-bottom: var(--spacing-lg);
}

.model-item {
  border: 2px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  cursor: pointer;
  transition: all 0.2s ease;
}

.model-item:hover {
  border-color: var(--color-primary);
  background: var(--color-bg-secondary);
}

.model-item.active {
  border-color: var(--color-primary);
  background: var(--color-primary);
  color: white;
}

.model-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.model-icon {
  font-size: 24px;
  color: var(--color-primary);
}

.model-item.active .model-icon {
  color: white;
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

.model-info {
  margin-bottom: var(--spacing-md);
}

.model-name {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: var(--spacing-xs);
}

.model-version,
.model-size,
.model-format {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-xs);
}

.model-item.active .model-version,
.model-item.active .model-size,
.model-item.active .model-format {
  color: rgba(255, 255, 255, 0.8);
}

.model-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.action-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: var(--color-bg-tertiary);
  color: var(--color-text-primary);
  border-radius: var(--radius-sm);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: var(--color-primary);
  color: white;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.model-details {
  margin-bottom: var(--spacing-xl);
}

.details-grid {
  margin-bottom: var(--spacing-lg);
}

.detail-group h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: var(--spacing-sm) 0;
  border-bottom: 1px solid var(--color-border);
}

.detail-label {
  font-size: 14px;
  color: var(--color-text-secondary);
}

.detail-value {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
}

.detail-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
}

.convert-dialog {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog-content {
  max-width: 400px;
  width: 90%;
}

.dialog-content h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-lg);
}

.convert-form {
  margin-bottom: var(--spacing-lg);
}

.dialog-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: flex-end;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .models-grid {
    grid-template-columns: 1fr;
  }
  
  .details-grid {
    grid-template-columns: 1fr;
  }
  
  .list-header {
    flex-direction: column;
    gap: var(--spacing-md);
    align-items: flex-start;
  }
  
  .list-controls {
    width: 100%;
    justify-content: space-between;
  }
  
  .detail-actions {
    flex-direction: column;
  }
  
  .model-actions {
    justify-content: center;
  }
}
</style> 
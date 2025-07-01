<template>
  <div class="fluent-model-root">
    <div class="fluent-model-main glass">
      <div class="fluent-model-header">
        <h1>模型管理</h1>
        <div class="desc">管理本地与已训练模型，支持导入、导出、删除等操作</div>
      </div>
      <div class="fluent-model-actions">
        <button class="fluent-btn primary" @click="importModel"><Icon icon="fluent:folder-add-24-regular" /> 导入模型</button>
        <button class="fluent-btn secondary" @click="exportSelected" :disabled="!selected.length"><Icon icon="fluent:arrow-export-24-regular" /> 导出</button>
        <button class="fluent-btn secondary" @click="deleteSelected" :disabled="!selected.length"><Icon icon="fluent:delete-24-regular" /> 删除</button>
      </div>
      <div class="fluent-model-table glass">
        <table>
          <thead>
            <tr>
              <th><input type="checkbox" @change="toggleAll" :checked="allSelected" /></th>
              <th>模型名称</th>
              <th>大小</th>
              <th>类型</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="model in models" :key="model.id">
              <td><input type="checkbox" v-model="selected" :value="model.id" /></td>
              <td>{{ model.name }}</td>
              <td>{{ model.size }}</td>
              <td>{{ model.type }}</td>
              <td>
                <span :class="['status-dot', model.status]">●</span>
                {{ model.status === 'ready' ? '可用' : '未加载' }}
              </td>
              <td>
                <button class="fluent-btn secondary mini" @click="exportModel(model)"><Icon icon="fluent:arrow-export-24-regular" /></button>
                <button class="fluent-btn secondary mini" @click="deleteModel(model)"><Icon icon="fluent:delete-24-regular" /></button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import './ModelPage.css'
import { ref, computed } from 'vue'
import { Icon } from '@iconify/vue'

const models = ref([
  { id: 1, name: 'Llama2-7B', size: '7B', type: '基础', status: 'ready' },
  { id: 2, name: 'Qwen-7B', size: '7B', type: '微调', status: 'ready' },
  { id: 3, name: 'ChatGLM3-6B', size: '6B', type: '基础', status: 'unloaded' }
])

const selected = ref<number[]>([])
const allSelected = computed(() => selected.value.length === models.value.length)
const toggleAll = (e: Event) => {
  const checked = (e.target as HTMLInputElement).checked
  selected.value = checked ? models.value.map(m => m.id) : []
}

const importModel = () => {}
const exportSelected = () => {}
const deleteSelected = () => {}
const exportModel = (model: any) => {}
const deleteModel = (model: any) => {}
</script>
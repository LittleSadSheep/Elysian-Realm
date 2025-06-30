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

<style scoped>
.fluent-model-root {
  min-height: 100vh;
  background: linear-gradient(135deg, #e3e9f7 0%, #f7faff 40%, #f6f3ff 70%, #f9f6f3 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}
.fluent-model-main {
  width: 100%;
  max-width: 900px;
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
.fluent-model-header h1 {
  font-size: 2.2rem;
  font-weight: 800;
  color: #222;
  margin-bottom: 8px;
}
.fluent-model-header .desc {
  color: #0078d4;
  font-size: 1.1rem;
  font-weight: 600;
}
.fluent-model-actions {
  display: flex;
  gap: 18px;
  margin-bottom: 8px;
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
.fluent-btn.mini {
  padding: 6px 10px;
  font-size: 1rem;
  border-radius: 10px;
}
.fluent-model-table {
  border-radius: 20px;
  background: rgba(255,255,255,0.85);
  box-shadow: 0 4px 24px 0 rgba(0,120,212,0.10);
  padding: 18px 18px;
  overflow-x: auto;
}
table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 1.05rem;
  background: transparent;
}
th, td {
  padding: 12px 10px;
  text-align: left;
}
th {
  color: #0078d4;
  font-weight: 700;
  background: transparent;
}
tbody tr {
  border-radius: 12px;
  background: #f7faff;
  box-shadow: 0 2px 8px 0 rgba(0,120,212,0.06);
  transition: box-shadow 0.2s;
}
tbody tr:hover {
  box-shadow: 0 8px 32px 0 rgba(0,120,212,0.12);
}
.status-dot {
  font-size: 1.2em;
  margin-right: 6px;
}
.status-dot.ready {
  color: #0078d4;
}
.status-dot.unloaded {
  color: #aaa;
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(40px);}
  to { opacity: 1; transform: none;}
}
@media (max-width: 900px) {
  .fluent-model-main { padding: 24px 8px; }
  th, td { padding: 8px 4px; }
}
</style> 
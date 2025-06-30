# Elysian-Realm UI

现代化、可视化的 LLM 微调与推理平台的前端界面，采用 Microsoft Fluent 2 设计体系。

## 技术栈

- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **设计系统**: Microsoft Fluent 2
- **图标库**: Iconify
- **桌面应用**: Tauri
- **路由**: Vue Router

## 项目结构

```
src/UI/
├── src/
│   ├── components/          # 通用组件
│   ├── pages/              # 页面组件
│   │   ├── HomePage.vue    # 首页
│   │   ├── TrainPage.vue   # 模型训练
│   │   ├── InferPage.vue   # 模型推理
│   │   ├── TunePage.vue    # 参数调优
│   │   └── ModelPage.vue   # 模型管理
│   ├── styles/
│   │   └── global.css      # 全局样式
│   ├── App.vue             # 主应用组件
│   └── main.ts             # 应用入口
├── index.html              # HTML模板
├── package.json            # 项目配置
├── vite.config.ts          # Vite配置
└── tsconfig.json           # TypeScript配置
```

## 功能特性

### 🎨 设计系统
- 采用 Microsoft Fluent 2 设计规范
- 支持深色/浅色主题切换
- 响应式设计，支持移动端适配
- 流畅的动画和过渡效果

### 🚀 核心功能
- **模型训练**: 支持 QLoRA、LoRA 等微调方法
- **模型推理**: 实时对话界面，支持多种模型格式
- **参数调优**: 基于 Optuna 的超参数优化
- **模型管理**: 统一的模型存储和管理

### 💻 用户体验
- 直观的导航界面
- 实时状态监控
- 可视化配置界面
- 优雅的交互反馈

## 开发指南

### 安装依赖
```bash
npm install
```

### 启动开发服务器
```bash
npm run dev
```

### 构建生产版本
```bash
npm run build
```

### Tauri 开发
```bash
npm run tauri dev
```

### Tauri 构建
```bash
npm run tauri build
```

## 设计规范

### 颜色系统
- **主色调**: #0078d4 (Fluent Blue)
- **背景色**: 浅色主题 #fafafa，深色主题 #1a1a1a
- **文本色**: 浅色主题 #323130，深色主题 #ffffff

### 间距系统
- **xs**: 4px
- **sm**: 8px
- **md**: 16px
- **lg**: 24px
- **xl**: 32px
- **2xl**: 48px

### 圆角系统
- **sm**: 4px
- **md**: 8px
- **lg**: 12px
- **xl**: 16px

## 组件库

项目使用自定义组件库，基于 Fluent 2 设计规范：

- **Button**: 按钮组件，支持多种样式
- **Input**: 输入框组件
- **Select**: 选择器组件
- **Card**: 卡片容器组件
- **Icon**: 图标组件（基于 Iconify）

## 主题系统

支持深色和浅色主题切换，通过 CSS 变量实现：

```css
:root {
  --color-bg-primary: #ffffff;
  --color-text-primary: #323130;
  /* ... 其他变量 */
}

.dark-theme {
  --color-bg-primary: #1a1a1a;
  --color-text-primary: #ffffff;
  /* ... 深色主题变量 */
}
```

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

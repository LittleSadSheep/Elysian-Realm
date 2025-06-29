# Elysian-Realm UI (Tarui + Vite + TypeScript)

- UI 框架：Tarui (React/TypeScript)
- 构建工具：Vite
- 设计语言：Microsoft Fluent2
- 图标库：Iconify

## 设计原则
- 现代、简洁、流畅，遵循 Fluent2 设计体系
- 丰富的动效与交互反馈
- 响应式布局，适配桌面与移动端
- 主题色彩与组件风格与微软生态一致

## 主要页面
- 首页（模式选择、项目简介、状态展示）
- 训练参数配置页（支持 Optuna/手动切换，参数分组，动效切换）
- 推理页（输入/输出区，历史记录，模型选择）
- 调参页（Optuna实验进度、结果可视化）
- 日志与模型管理页

## 组件建议
- Fluent2 Button、Input、Switch、Tabs、Dialog、ProgressBar、Tooltip、Card、List、Dropdown 等
- Iconify 图标集成
- 动效：切换、悬浮、加载、进度、弹窗等

## 目录结构建议
```
src/UI/
  ├─ assets/         # 静态资源、图标
  ├─ components/     # 通用组件（Button、Input、Card等）
  ├─ pages/          # 各功能页面
  ├─ App.tsx        # 入口
  ├─ main.tsx       # Vite入口
  └─ vite.config.ts # Vite配置
```

## 参考
- Fluent2: https://fluent2.microsoft.design/
- Iconify: https://iconify.design/
- Tarui: https://github.com/innocces/tarui
- Vite: https://vitejs.dev/

---

后续将优先完成 UI 主要页面和动效设计，后端 API 接入可后补。

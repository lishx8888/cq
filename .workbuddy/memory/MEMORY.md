# Daidy 项目记忆

## 项目概况
- **项目**: Daidy 护肤电商
- **技术栈**: Vue3 + Flask + SQLite
- **路径**: h:/cq/frontend（前端）, h:/cq/backend:5000（后端）

## 用户偏好
- 中文交流
- 喜欢简洁、分步骤的指令
- 习惯附带截图和短命令
- 喜欢让 AI 直接执行命令

## 功能更新记录

### 2026-04-18
- **Banner 图片尺寸改回 16:9**: AdminBannersView.vue 中将 `aspect-ratio: 9/16` 改为 `aspect-video`
- **后台分类排序管理**: AdminCategoriesView.vue 添加拖拽排序功能
  - 卡片左侧添加拖拽手柄
  - 显示排序编号 #sort_order
  - 拖拽后显示"保存排序"按钮
  - 编辑表单中添加 sort_order 字段输入
  - 后端已按 sort_order 排序（models.py 第25行已有字段）

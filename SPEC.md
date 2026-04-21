# 护肤产品展示独立站 — 规格说明书

## 1. Concept & Vision

一个清新、自然、专业的高端护肤产品展示网站。设计灵感来自北欧极简主义与日式侘寂美学的结合——大量留白、柔和的自然色调、克制的动画，营造出宁静、信赖、高端的品牌氛围。用户在浏览时仿佛置身于一间光线充足的护肤品概念店，感受到产品背后传递的纯净与专业。

---

## 2. Design Language

### 2.1 美学方向
**北欧日式融合风** — 参考 Aesop、Glossier 的品牌调性，强调"少即是多"的克制美学。

### 2.2 色彩系统

| 用途 | 色值 | 说明 |
|------|------|------|
| Primary | `#2D5A47` | 深森林绿，主品牌色 |
| Primary Light | `#4A7C66` | 浅森林绿，hover状态 |
| Secondary | `#E8DDD4` | 暖米色，背景点缀 |
| Accent | `#C4A77D` | 玫瑰金色，强调与CTA |
| Background | `#FAFAF8` | 近白色，主背景 |
| Surface | `#FFFFFF` | 纯白，卡片背景 |
| Text Primary | `#1A1A1A` | 近黑色，主文字 |
| Text Secondary | `#6B6B6B` | 灰色，次要文字 |
| Border | `#E5E5E3` | 浅灰，边框线 |

### 2.3 字体系统

- **标题字体**: `Cormorant Garamond` (Google Fonts) — 优雅的衬线体，用于大标题和品牌名
- **正文字体**: `Noto Sans SC` (Google Fonts) — 清晰的中文无衬线体
- **英文辅助**: `Cormorant Garamond` — 用于英文标签和装饰

**字号层级**:
- 品牌Logo: 28px / font-weight: 600
- H1 (页面标题): 48px / font-weight: 500
- H2 (区块标题): 32px / font-weight: 500
- H3 (卡片标题): 20px / font-weight: 500
- Body: 16px / font-weight: 400 / line-height: 1.8
- Caption: 14px / font-weight: 400

### 2.4 空间系统

- 基础单位: 8px
- 页面最大宽度: 1200px
- 卡片间距: 24px
- 区块垂直间距: 80px (桌面) / 48px (移动端)
- 容器内边距: 40px (桌面) / 20px (移动端)

### 2.5 动效哲学

**"如微风拂过"** — 动效应该是轻盈、自然的，不抢夺用户注意力。

| 动效类型 | 参数 | 说明 |
|----------|------|------|
| 页面进入 | opacity 0→1, translateY 20px→0, 600ms, ease-out | 元素渐入效果 |
| 卡片悬浮 | translateY -4px, box-shadow 增强, 300ms ease | 轻微上浮感 |
| 按钮悬停 | background-color 渐变, 200ms ease | 色彩平滑过渡 |
| 导航固定 | 滚动50px后触发, 背景添加毛玻璃效果 | 导航融入感 |

### 2.6 视觉资产

- **图标库**: Lucide Icons (线条风格，与品牌调性一致)
- **产品图片**: 统一使用 1:1 比例的方形象限图，背景 `#F5F5F3`
- **装饰元素**: 细线条装饰、柔和的几何图形（如细圆圈、细线条）
- **无图片占位**: 柔和渐变背景 `#E8DDD4 → #F5F5F3`

---

## 3. Layout & Structure

### 3.1 整体架构

```
┌─────────────────────────────────────────────────────────┐
│  顶部导航栏 (固定, 毛玻璃效果)                            │
├─────────────────────────────────────────────────────────┤
│  首页                                                    │
│  ├─ Hero Banner 轮播 (全宽, 视差效果)                      │
│  ├─ 产品分类入口 (横向卡片)                               │
│  ├─ 精选产品展示 (2x4 网格)                               │
│  └─ 品牌理念区                                           │
├─────────────────────────────────────────────────────────┤
│  产品列表页                                              │
│  ├─ 页面标题                                             │
│  ├─ 分类筛选栏                                           │
│  └─ 产品网格 (响应式 2-4 列)                             │
├─────────────────────────────────────────────────────────┤
│  产品详情页                                              │
│  ├─ 产品主图 (左侧) + 信息 (右侧)                         │
│  ├─ 核心功效区                                           │
│  └─ 咨询引导区                                           │
├─────────────────────────────────────────────────────────┤
│  底部 Footer (品牌信息、联系方式)                          │
└─────────────────────────────────────────────────────────┘
```

### 3.2 响应式断点

- 桌面端: ≥1024px (4列产品网格)
- 平板端: 768px - 1023px (3列网格)
- 移动端: <768px (2列网格, 汉堡菜单)

### 3.3 页面节奏

- **首页 Hero**: 100vh 全屏，大气开场
- **分类入口**: 紧凑排列，视觉引导
- **精选产品**: 适中密度，留白呼吸
- **品牌理念**: 大留白，文字聚焦
- **详情页**: 宽松排版，信息清晰

---

## 4. Features & Interactions

### 4.1 导航栏

**行为**:
- 页面滚动超过 50px 时，导航栏添加 `backdrop-filter: blur(12px)` 和底部边框
- Logo 左侧，导航链接右侧
- "首页" / "产品列表" 两个主导航
- 移动端显示汉堡菜单按钮，点击展开侧边抽屉

**悬停状态**:
- 链接下方出现 2px 高度的下划线动画 (从中心向两端展开)

### 4.2 Banner 轮播

**行为**:
- 自动轮播，间隔 5 秒
- 支持左右箭头手动切换
- 底部指示点，点击可跳转
- 触摸滑动支持 (移动端)
- 无限循环

**视觉**:
- 每张 Banner 占据视口宽度，高度 70vh
- 图片使用 `object-fit: cover`
- 叠加半透明遮罩 (`rgba(0,0,0,0.2)`)，确保文字可读

### 4.3 产品分类入口

**展示**:
- 横向滚动 (移动端) / 弹性布局 (桌面端)
- 每个分类: 图标/图片 + 分类名称
- 最多显示 6 个分类

**交互**:
- 悬停: 轻微放大 (scale 1.05)，添加阴影
- 点击: 跳转至产品列表页并自动筛选该分类

### 4.4 产品卡片

**内容**:
- 产品主图 (1:1)
- 产品名称
- 简短描述 (可选)
- 咨询按钮

**状态**:
- Default: 白色背景，轻微阴影
- Hover: 上浮 4px，阴影加深，图片轻微放大 1.05
- 点击"咨询": 弹出微信/客服咨询提示

### 4.5 产品详情页

**布局**:
- 左侧 50%: 产品主图 + 缩略图列表
- 右侧 50%: 产品名称、规格、成分、功效说明

**功效展示**:
- 使用图标 + 文字的列表形式
- 重要功效可加粗或使用品牌色

**咨询引导**:
- 页面底部固定悬浮栏: "想了解更多？立即咨询"
- 点击弹出联系方式 (微信/二维码/电话号码)

### 4.6 后台管理系统

**登录页**:
- 简洁的登录表单: 用户名 + 密码
- "记住登录状态" 复选框

**产品管理**:
- 产品列表表格: ID、名称、分类、状态、操作
- 新增/编辑产品表单:
  - 产品名称 (必填)
  - 产品分类 (下拉选择)
  - 产品图片 (上传组件，支持拖拽)
  - 产品规格
  - 成分说明
  - 功效描述 (富文本)
  - 状态 (启用/禁用)
- 删除确认弹窗

**分类管理**:
- 简单的分类增删改
- 关联产品数量显示

---

## 5. Component Inventory

### 5.1 Button 按钮

| 类型 | 默认样式 | Hover | Active | Disabled |
|------|---------|-------|--------|----------|
| Primary | 森林绿背景, 白色文字, 圆角 4px | 浅森林绿, 轻微上浮 | 深森林绿 | 灰色, 50% 透明度 |
| Secondary | 透明背景, 森林绿边框 | 浅绿色背景填充 | 深绿色背景 | 灰色边框/文字 |
| Ghost | 无边框, 森林绿文字 | 添加浅绿背景 | 文字加深 | 灰色文字 |

### 5.2 Input 输入框

- 默认: 浅灰边框 `#E5E5E3`, 圆角 4px
- Focus: 森林绿边框, 轻微阴影
- Error: 红色边框, 错误提示文字
- 高度: 48px (桌面) / 44px (移动端)

### 5.3 Card 卡片

- 白色背景, 圆角 8px
- 阴影: `0 2px 8px rgba(0,0,0,0.06)`
- Hover 阴影: `0 8px 24px rgba(0,0,0,0.1)`

### 5.4 Modal 弹窗

- 居中显示, 最大宽度 500px
- 半透明黑色遮罩 `rgba(0,0,0,0.5)`
- 进入动画: scale 0.95→1, opacity 0→1, 200ms
- 右上角关闭按钮

### 5.5 Navigation 导航

- 固定顶部, 高度 72px
- 过渡效果: 滚动后添加背景模糊和边框

### 5.6 Loading 加载

- 使用品牌色的 CSS 动画圆环
- 尺寸: 32px (内嵌) / 48px (全屏)

---

## 6. Technical Approach

### 6.1 技术栈

**前端**:
- Vue 3 (Composition API + `<script setup>`)
- Vite (构建工具)
- Vue Router (路由管理)
- Pinia (状态管理)
- Axios (HTTP 请求)
- Tailwind CSS (工具类样式) + 自定义 CSS 变量

**后端**:
- Python Flask (轻量级 API 服务)
- SQLite (数据存储)
- Flask-CORS (跨域支持)

**目录结构**:
```
skincare-site/
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── assets/          # 静态资源
│   │   ├── components/      # 公共组件
│   │   ├── views/           # 页面视图
│   │   ├── stores/          # Pinia stores
│   │   ├── router/          # 路由配置
│   │   ├── api/             # API 接口
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── backend/                  # 后端项目
│   ├── app.py               # Flask 主应用
│   ├── models.py            # 数据模型
│   ├── routes/              # 路由模块
│   └── requirements.txt
└── SPEC.md
```

### 6.2 API 设计

**产品接口**:

| Method | Endpoint | 说明 |
|--------|----------|------|
| GET | `/api/products` | 获取产品列表 (支持分类筛选) |
| GET | `/api/products/:id` | 获取产品详情 |
| POST | `/api/products` | 创建产品 |
| PUT | `/api/products/:id` | 更新产品 |
| DELETE | `/api/products/:id` | 删除产品 |

**分类接口**:

| Method | Endpoint | 说明 |
|--------|----------|------|
| GET | `/api/categories` | 获取分类列表 |
| POST | `/api/categories` | 创建分类 |
| PUT | `/api/categories/:id` | 更新分类 |
| DELETE | `/api/categories/:id` | 删除分类 |

**管理接口**:

| Method | Endpoint | 说明 |
|--------|----------|------|
| POST | `/api/admin/login` | 管理员登录 |
| GET | `/api/admin/stats` | 获取统计数据 |

### 6.3 数据模型

**Product 产品**:
```json
{
  "id": "integer",
  "name": "string",
  "category_id": "integer",
  "image_url": "string",
  "gallery": ["string"],
  "specs": "string",
  "ingredients": "string",
  "benefits": "string",
  "description": "string",
  "status": "enum(enabled, disabled)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Category 分类**:
```json
{
  "id": "integer",
  "name": "string",
  "icon": "string",
  "sort_order": "integer",
  "created_at": "datetime"
}
```

**Admin 管理员**:
```json
{
  "id": "integer",
  "username": "string",
  "password_hash": "string",
  "created_at": "datetime"
}
```

### 6.4 前端路由

| Path | Component | 说明 |
|------|-----------|------|
| `/` | HomeView | 首页 |
| `/products` | ProductsView | 产品列表 |
| `/products/:id` | ProductDetailView | 产品详情 |
| `/admin` | AdminLoginView | 管理员登录 |
| `/admin/products` | AdminProductsView | 产品管理 |
| `/admin/categories` | AdminCategoriesView | 分类管理 |

---

## 7. Mock Data

### 7.1 产品分类 (初始数据)

1. 洁面系列 - 温和清洁
2. 精华液 - 高效修护
3. 面霜乳液 - 深层保湿
4. 防晒护理 - 防护隔离
5. 面膜专区 - 密集滋养
6. 套装礼盒 - 精致礼遇

### 7.2 示例产品数据

```json
[
  {
    "name": "玫瑰精粹洁面乳",
    "category": "洁面系列",
    "specs": "120ml",
    "ingredients": "玫瑰花水、氨基酸表活、玻尿酸",
    "benefits": "温和清洁|补水保湿|舒缓肌肤",
    "description": "蕴含大马士革玫瑰精粹，温和洁净同时锁住肌肤水分"
  },
  {
    "name": "维C焕亮精华液",
    "category": "精华液",
    "specs": "30ml",
    "ingredients": "10%活性维C、烟酰胺、传明酸",
    "benefits": "提亮肤色|淡化色斑|抗氧化",
    "description": "高浓度维C精华，多维改善暗沉肤色"
  }
]
```

---

## 8. Success Criteria

- [ ] 首页 Banner 轮播功能正常，自动/手动切换流畅
- [ ] 产品分类导航跳转正确
- [ ] 产品列表页筛选功能正常
- [ ] 产品详情页信息展示完整
- [ ] 咨询引导弹窗正常触发
- [ ] 后台管理系统可正常登录
- [ ] 产品增删改查功能完整
- [ ] 响应式布局在移动端显示正常
- [ ] 动画效果流畅，无明显卡顿
- [ ] 所有 API 接口返回正确数据

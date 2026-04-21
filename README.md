# PURE LAB 护肤产品展示独立站

一个专注于产品展示的高端护肤产品独立网站，包含完整的前台展示和后台管理系统。

## 功能特点

### 前台展示
- **首页**: Banner 轮播、分类入口、精选产品、品牌故事
- **产品列表**: 分类筛选、产品卡片展示
- **产品详情**: 产品信息、功效说明、在线咨询引导

### 后台管理
- **产品管理**: 产品的增删改查
- **分类管理**: 产品分类的增删改查
- **管理员登录**: 安全的 JWT 认证

## 技术栈

### 前端
- Vue 3 (Composition API)
- Vite (构建工具)
- Vue Router (路由管理)
- Pinia (状态管理)
- Tailwind CSS (样式框架)
- Axios (HTTP 请求)

### 后端
- Python Flask
- SQLite (数据库)
- Flask-JWT-Extended (认证)
- Flask-CORS (跨域支持)

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 18+
- npm 或 yarn

### 安装与运行

#### Windows 用户
双击运行 `start.bat` 或在终端中执行:
```bash
.\start.bat
```

#### 手动启动

**1. 安装后端依赖**
```bash
cd backend
pip install -r requirements.txt
```

**2. 安装前端依赖**
```bash
cd frontend
npm install
```

**3. 启动后端服务**
```bash
cd backend
python app.py
```

**4. 启动前端服务** (新开终端)
```bash
cd frontend
npm run dev
```

## 访问地址

| 服务 | 地址 |
|------|------|
| 前台网站 | http://localhost:5173 |
| 后台管理 | http://localhost:5173/admin |
| API 接口 | http://localhost:5000/api |

## 管理员账号

- **用户名**: admin
- **密码**: admin123

## 项目结构

```
skincare-site/
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── api/            # API 请求封装
│   │   ├── assets/         # 静态资源
│   │   ├── components/     # 公共组件
│   │   ├── stores/         # Pinia 状态管理
│   │   ├── router/         # 路由配置
│   │   └── views/          # 页面视图
│   ├── public/
│   └── package.json
├── backend/                  # 后端项目
│   ├── app.py              # Flask 主应用
│   ├── models.py           # 数据库模型
│   └── requirements.txt
├── SPEC.md                   # 项目规格说明
└── README.md
```

## 设计理念

网站采用北欧日式融合风格，强调"少即是多"的克制美学:
- 大量留白，营造宁静氛围
- 柔和的自然色调，传递纯净感
- 克制的动画效果，不抢夺注意力
- 响应式设计，适配多端设备

## 品牌色彩

| 用途 | 色值 |
|------|------|
| 主品牌色 | #2D5A47 (森林绿) |
| 强调色 | #C4A77D (玫瑰金) |
| 背景色 | #FAFAF8 (近白) |
| 点缀色 | #E8DDD4 (暖米色) |

## License

MIT License

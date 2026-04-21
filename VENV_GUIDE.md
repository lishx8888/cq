# 虚拟环境使用指南

## 为什么使用虚拟环境？

使用虚拟环境（venv）是 Python 项目的最佳实践，具有以下优势：

### 1. 依赖隔离
- 避免与系统 Python 包冲突
- 不同项目可以使用不同版本的依赖包
- 防止全局环境污染

### 2. 版本管理
- 精确控制每个项目的依赖版本
- 避免版本兼容性问题
- 便于团队协作

### 3. 环境清洁
- 系统环境保持干净
- 便于卸载和重建
- 减少依赖冲突

### 4. 易于部署
- 可以轻松复制整个虚拟环境
- 便于 Docker 容器化
- 支持自动化部署

### 5. 权限安全
- 不需要 sudo 权限安装包
- 用户级别的包管理
- 更好的安全性

## 快速开始

### 方法一：使用启动脚本（推荐）

```bash
# 赋予执行权限
chmod +x start.sh

# 运行启动脚本（自动创建和管理虚拟环境）
./start.sh
```

### 方法二：手动管理虚拟环境

#### 1. 创建虚拟环境

```bash
# 使用虚拟环境管理工具
chmod +x venv_manager.sh
./venv_manager.sh create

# 或手动创建
python3 -m venv venv
```

#### 2. 激活虚拟环境

```bash
# 使用管理工具
./venv_manager.sh activate

# 或手动激活
source venv/bin/activate
```

#### 3. 安装依赖

```bash
# 激活虚拟环境后
cd backend
pip install -r requirements.txt
```

#### 4. 启动服务

```bash
# 后端（在虚拟环境中）
cd backend
python app.py

# 前端（新开终端）
cd frontend
npm run dev
```

#### 5. 退出虚拟环境

```bash
deactivate
```

## 虚拟环境管理工具

项目提供了 `venv_manager.sh` 脚本来管理虚拟环境：

### 命令列表

```bash
# 创建虚拟环境
./venv_manager.sh create

# 激活虚拟环境
./venv_manager.sh activate

# 查看虚拟环境状态
./venv_manager.sh status

# 删除虚拟环境
./venv_manager.sh delete

# 更新依赖
./venv_manager.sh update

# 导出依赖列表
./venv_manager.sh export
```

## 虚拟环境目录结构

```
venv/
├── bin/              # 可执行文件
│   ├── activate      # 激活脚本
│   ├── python        # Python 解释器
│   └── pip           # 包管理器
├── lib/              # 库文件
│   └── python3.x/    # Python 版本
│       └── site-packages/  # 安装的包
└── pyvenv.cfg        # 虚拟环境配置
```

## 常见问题

### 1. 虚拟环境创建失败

**问题**：`python3 -m venv venv` 命令失败

**解决方案**：
```bash
# 确保安装了 python3-venv
sudo apt-get install python3-venv  # Ubuntu/Debian
sudo yum install python3-venv      # CentOS/RHEL
```

### 2. 激活虚拟环境后 Python 版本不对

**问题**：激活后 Python 版本不是预期的版本

**解决方案**：
```bash
# 删除虚拟环境重新创建
rm -rf venv
python3.8 -m venv venv  # 指定 Python 版本
```

### 3. 依赖安装失败

**问题**：`pip install` 失败

**解决方案**：
```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 4. 虚拟环境占用空间过大

**问题**：虚拟环境占用大量磁盘空间

**解决方案**：
```bash
# 清理缓存
pip cache purge

# 删除不必要的包
pip uninstall <package-name>

# 重建虚拟环境（只保留必要的包）
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 生产环境部署

### 1. 导出依赖列表

```bash
source venv/bin/activate
pip freeze > requirements.txt
```

### 2. 在生产环境重建

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. 使用 Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 最佳实践

1. **始终使用虚拟环境**：不要在系统环境中安装项目依赖
2. **提交 requirements.txt**：确保团队使用相同的依赖版本
3. **定期更新依赖**：保持依赖包的安全性和性能
4. **使用版本控制**：将虚拟环境配置纳入版本控制
5. **文档化环境**：记录虚拟环境的创建和使用方法

## 与系统环境对比

| 特性 | 虚拟环境 | 系统环境 |
|------|---------|---------|
| 依赖隔离 | ✅ | ❌ |
| 版本控制 | ✅ | ❌ |
| 权限要求 | 低 | 高 |
| 环境清洁 | ✅ | ❌ |
| 部署便利性 | ✅ | ❌ |
| 学习成本 | 低 | 低 |

## 总结

使用虚拟环境是 Python 开发的最佳实践，能够显著提高项目的可维护性和可移植性。本项目已经集成了虚拟环境支持，建议您在开发和部署过程中始终使用虚拟环境。
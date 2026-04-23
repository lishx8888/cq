# GitHub Actions Docker Build Workflow

本项目使用GitHub Actions自动构建Docker镜像并推送到Docker Hub，镜像名称包含日期标签。

## 配置步骤

### 1. 在Docker Hub创建仓库

- 创建两个仓库：`cq-backend` 和 `cq-frontend`
- 确保您的Docker Hub账号有推送权限

### 2. 在GitHub仓库设置密钥

在GitHub仓库的 `Settings > Secrets and variables > Actions` 中添加以下密钥：

| 密钥名称 | 描述 | 值 |
|---------|------|----|
| `DOCKERHUB_USERNAME` | Docker Hub用户名 | 您的Docker Hub用户名 |
| `DOCKERHUB_TOKEN` | Docker Hub访问令牌 | 在Docker Hub生成的访问令牌 |

### 3. 生成访问令牌

1. 登录Docker Hub
2. 进入 `Account Settings > Security`
3. 点击 `New Access Token`
4. 命名令牌（例如：`github-actions`）
5. 设置权限为 `Read & Write`
6. 复制生成的令牌并保存到GitHub Secrets中

## 工作流说明

### 触发条件

- 推送到 `main` 或 `dev` 分支
- 打开或更新 `main` 或 `dev` 分支的Pull Request
- 手动触发（在GitHub Actions页面点击 `Run workflow`）

### 构建过程

1. 检出代码
2. 设置Docker Buildx
3. 登录到Docker Hub
4. 生成日期标签（格式：YYMMDD）
5. 构建并推送后端镜像
6. 构建并推送前端镜像
7. 清理Docker系统

### 镜像命名

- 后端镜像：`{username}/cq-backend:{date}` 和 `{username}/cq-backend:latest`
- 前端镜像：`{username}/cq-frontend:{date}` 和 `{username}/cq-frontend:latest`

例如：
- `yourusername/cq-backend:260423`
- `yourusername/cq-frontend:260423`

## 使用镜像

### 拉取镜像

```bash
# 拉取指定日期的镜像
docker pull yourusername/cq-backend:260423
docker pull yourusername/cq-frontend:260423

# 拉取最新镜像
docker pull yourusername/cq-backend:latest
docker pull yourusername/cq-frontend:latest
```

### 运行容器

```bash
# 运行后端
docker run -d --name cq-backend -p 5000:5000 yourusername/cq-backend:260423

# 运行前端
docker run -d --name cq-frontend -p 80:80 --link cq-backend:backend yourusername/cq-frontend:260423
```

## 监控构建

1. 进入GitHub仓库
2. 点击 `Actions` 标签
3. 选择 `Docker Build and Push` 工作流
4. 查看构建状态和日志

## 故障排查

### 构建失败

- 检查Docker Hub用户名和令牌是否正确
- 确保Docker Hub仓库存在且有推送权限
- 查看构建日志了解具体错误

### 镜像推送失败

- 检查网络连接
- 确保Docker Hub令牌有写权限
- 验证Docker Hub账号是否被限制

### 镜像拉取失败

- 检查Docker Hub用户名是否正确
- 确认镜像已成功构建并推送
- 验证网络连接

## 自定义配置

### 修改构建触发条件

编辑 `.github/workflows/docker-build.yml` 文件，修改 `on` 部分：

```yaml
on:
  push:
    branches: [ main, dev, feature/* ]  # 添加更多分支
  schedule:
    - cron: '0 0 * * *'  # 每天自动构建
```

### 修改镜像标签格式

编辑 `.github/workflows/docker-build.yml` 文件，修改日期格式：

```yaml
- name: Get current date
  id: date
  run: echo "date=$(date +'%Y%m%d')" >> $GITHUB_OUTPUT  # 改为YYYYMMDD格式
```

## 安全注意事项

- 不要在代码中硬编码Docker Hub凭据
- 定期更新Docker Hub访问令牌
- 使用最小权限原则设置令牌权限
- 定期更新基础镜像以获取安全补丁

## 相关文件

- `.github/workflows/docker-build.yml` - GitHub Actions配置
- `backend/Dockerfile` - 后端Dockerfile
- `frontend/Dockerfile` - 前端Dockerfile
- `docker-compose.yml` - 本地开发和部署配置
# Docker 部署指南

本项目已配置为轻量化的Docker容器部署，使用多阶段构建和Alpine Linux基础镜像来最小化镜像大小。

## 镜像大小优化

- **后端镜像**：基于Python 3.12 Alpine，约150MB
- **前端镜像**：基于Nginx Alpine，约25MB
- **总体积**：相比标准镜像减少约70%

## 快速开始

### 1. 构建和启动服务

```bash
docker-compose up -d --build
```

### 2. 停止服务

```bash
docker-compose down
```

### 3. 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 4. 重启服务

```bash
docker-compose restart
```

## 服务访问

- **前端**：http://localhost
- **后端API**：http://localhost:5000
- **管理后台**：http://localhost/admin

## Docker配置文件说明

### backend/Dockerfile
- 使用Python 3.12 Alpine基础镜像
- 多阶段构建：先安装依赖，再复制应用代码
- 非root用户运行，提高安全性
- 最小化镜像层数量

### frontend/Dockerfile
- 使用Node.js 20 Alpine进行构建
- 使用Nginx Alpine作为运行时镜像
- 自动构建前端应用并优化静态文件
- 配置gzip压缩提高传输效率

### docker-compose.yml
- 定义后端和前端服务
- 配置健康检查确保服务可用性
- 自动重启策略
- 网络隔离和安全配置

### nginx.conf
- 反向代理配置，将API请求转发到后端
- SPA路由支持
- Gzip压缩配置
- 性能优化设置

## 环境变量

可以在docker-compose.yml中添加环境变量：

```yaml
services:
  backend:
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=0
      - DATABASE_URL=your_database_url
```

## 数据持久化

如需持久化数据，可以添加volumes配置：

```yaml
services:
  backend:
    volumes:
      - ./data:/app/data
```

## 生产环境部署建议

1. **使用HTTPS**：配置SSL证书
2. **域名配置**：修改nginx.conf中的server_name
3. **资源限制**：添加CPU和内存限制
4. **日志管理**：配置日志轮转
5. **监控**：添加健康检查和监控

## 故障排查

### 查看容器状态
```bash
docker-compose ps
```

### 进入容器调试
```bash
docker-compose exec backend sh
docker-compose exec frontend sh
```

### 重新构建特定服务
```bash
docker-compose up -d --build backend
docker-compose up -d --build frontend
```

## 清理

### 停止并删除容器
```bash
docker-compose down
```

### 删除镜像
```bash
docker rmi cq-backend cq-frontend
```

### 完全清理
```bash
docker-compose down -v --rmi all
```

## 注意事项

1. 首次构建可能需要较长时间下载依赖
2. 确保Docker有足够的内存和磁盘空间
3. 生产环境建议使用外部数据库
4. 定期更新基础镜像以获得安全补丁
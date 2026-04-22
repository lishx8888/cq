#!/bin/bash

echo "正在停止 PURE LAB 服务..."

# 停止后端服务
if [ -f "backend.pid" ]; then
    BACKEND_PID=$(cat backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        # 先尝试软终止
        kill $BACKEND_PID 2>/dev/null
        sleep 2
        # 检查是否还在运行，若在运行则强制终止
        if kill -0 $BACKEND_PID 2>/dev/null; then
            kill -9 $BACKEND_PID 2>/dev/null
            echo "后端服务已强制停止 (PID: $BACKEND_PID)"
        else
            echo "后端服务已停止 (PID: $BACKEND_PID)"
        fi
        rm backend.pid
    else
        echo "后端服务已不存在，清理PID文件"
        rm backend.pid
    fi
else
    echo "未找到后端服务PID文件"
    # 尝试通过进程名停止
    pkill -f "python3.*app\.py" 2>/dev/null
    pkill -f "python.*app\.py" 2>/dev/null
    pkill -f "/.*python.*app\.py" 2>/dev/null
    sleep 1
    # 强制终止剩余进程
    pkill -9 -f "python3.*app\.py" 2>/dev/null
    pkill -9 -f "python.*app\.py" 2>/dev/null
    pkill -9 -f "/.*python.*app\.py" 2>/dev/null
    echo "后端服务已停止 (通过进程名)"
fi

# 停止前端服务
if [ -f "frontend.pid" ]; then
    FRONTEND_PID=$(cat frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        # 先尝试软终止
        kill $FRONTEND_PID 2>/dev/null
        sleep 2
        # 检查是否还在运行，若在运行则强制终止
        if kill -0 $FRONTEND_PID 2>/dev/null; then
            kill -9 $FRONTEND_PID 2>/dev/null
            echo "前端服务已强制停止 (PID: $FRONTEND_PID)"
        else
            echo "前端服务已停止 (PID: $FRONTEND_PID)"
        fi
        rm frontend.pid
    else
        echo "前端服务已不存在，清理PID文件"
        rm frontend.pid
    fi
else
    echo "未找到前端服务PID文件"
    # 尝试通过进程名停止
    pkill -f "npm run dev" 2>/dev/null
    sleep 1
    # 强制终止剩余进程
    pkill -9 -f "npm run dev" 2>/dev/null
    pkill -9 -f "node"
    echo "前端服务已停止 (通过进程名)"
fi

# 清理临时文件
echo "清理临时文件..."
# 清理npm缓存
npm cache clean --force 2>/dev/null
# 清理Python缓存
find . -name "__pycache__" -type d -exec rm -rf {} \; 2>/dev/null
find . -name "*.pyc" -type f -exec rm -f {} \; 2>/dev/null

# 检查是否还有相关进程在运行
echo "检查是否还有相关进程在运行..."
BACKEND_PROCESSES=$(ps aux | grep -E "python.*app\.py" | grep -v grep | wc -l)
BACKEND_PROCESSES_WITH_PATH=$(ps aux | grep -E "/.*python.*app\.py" | grep -v grep | wc -l)
TOTAL_BACKEND_PROCESSES=$((BACKEND_PROCESSES + BACKEND_PROCESSES_WITH_PATH))
FRONTEND_PROCESSES=$(ps aux | grep -E "node|npm" | grep -v grep | wc -l)

if [ $TOTAL_BACKEND_PROCESSES -gt 0 ]; then
    echo "警告: 仍有 $TOTAL_BACKEND_PROCESSES 个后端进程在运行"
    ps aux | grep -E "python.*app\.py|/.*python.*app\.py" | grep -v grep
    # 再次尝试强制终止
    echo "再次尝试强制终止后端进程..."
    pkill -9 -f "python.*app\.py" 2>/dev/null
    pkill -9 -f "/.*python.*app\.py" 2>/dev/null
    sleep 1
    # 再次检查
    FINAL_BACKEND_PROCESSES=$(ps aux | grep -E "python.*app\.py|/.*python.*app\.py" | grep -v grep | wc -l)
    if [ $FINAL_BACKEND_PROCESSES -gt 0 ]; then
        echo "错误: 无法完全终止后端进程"
        ps aux | grep -E "python.*app\.py|/.*python.*app\.py" | grep -v grep
    else
        echo "后端进程已全部终止"
    fi
elif [ $FRONTEND_PROCESSES -gt 0 ]; then
    echo "警告: 仍有 $FRONTEND_PROCESSES 个前端进程在运行"
    ps aux | grep -E "node|npm" | grep -v grep
    # 再次尝试强制终止
    echo "再次尝试强制终止前端进程..."
    pkill -9 -f "node" 2>/dev/null
    pkill -9 -f "npm" 2>/dev/null
    sleep 1
    # 再次检查
    FINAL_FRONTEND_PROCESSES=$(ps aux | grep -E "node|npm" | grep -v grep | wc -l)
    if [ $FINAL_FRONTEND_PROCESSES -gt 0 ]; then
        echo "错误: 无法完全终止前端进程"
        ps aux | grep -E "node|npm" | grep -v grep
    else
        echo "前端进程已全部终止"
    fi
else
    echo "所有服务已完全停止"
fi

echo "停止操作完成"

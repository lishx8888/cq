#!/bin/bash

echo "正在停止 PURE LAB 服务..."

# Stop backend service using PID file
if [ -f "backend.pid" ]; then
    BACKEND_PID=$(cat backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "后端服务已停止 (PID: $BACKEND_PID)"
            rm backend.pid
        else
            echo "后端服务停止失败"
        fi
    else
        echo "后端服务已不存在，清理PID文件"
        rm backend.pid
    fi
else
    echo "未找到后端服务PID文件"
    # Fallback: try to kill by process name
    pkill -f "python3 app.py" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "后端服务已停止 (通过进程名)"
    else
        echo "未找到运行中的后端服务"
    fi
fi

# Stop frontend service using PID file
if [ -f "frontend.pid" ]; then
    FRONTEND_PID=$(cat frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "前端服务已停止 (PID: $FRONTEND_PID)"
            rm frontend.pid
        else
            echo "前端服务停止失败"
        fi
    else
        echo "前端服务已不存在，清理PID文件"
        rm frontend.pid
    fi
else
    echo "未找到前端服务PID文件"
    # Fallback: try to kill by process name
    pkill -f "npm run dev" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "前端服务已停止 (通过进程名)"
    else
        echo "未找到运行中的前端服务"
    fi
fi

echo "所有服务已停止"

#!/bin/bash

echo "正在停止 PURE LAB 服务..."

# Kill backend processes
pkill -f "python3 app.py" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "后端服务已停止"
else
    echo "未找到运行中的后端服务"
fi

# Kill frontend processes
pkill -f "npm run dev" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "前端服务已停止"
else
    echo "未找到运行中的前端服务"
fi

echo "所有服务已停止"
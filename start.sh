#!/bin/bash

echo "========================================"
echo "  PURE LAB 护肤产品展示网站 - 启动脚本"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到 Python3，请先安装 Python 3.8+"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "[错误] 未检测到 Node.js，请先安装 Node.js 18+"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "[错误] 未检测到 npm，请先安装 npm"
    exit 1
fi

# Virtual environment setup
VENV_DIR="venv"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "[1/4] 创建虚拟环境..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "[错误] 虚拟环境创建失败"
        exit 1
    fi
    echo "虚拟环境创建成功"
else
    echo "[1/4] 使用现有虚拟环境"
fi

# Activate virtual environment
echo "激活虚拟环境..."
source "$VENV_DIR/bin/activate"

echo ""
echo "[2/4] 安装后端依赖..."
cd backend
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[错误] 后端依赖安装失败"
    deactivate
    exit 1
fi
cd ..

echo ""
echo "[3/4] 安装前端依赖..."
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "[错误] 前端依赖安装失败"
    deactivate
    exit 1
fi
cd ..

echo ""
echo "[4/4] 启动服务..."
echo ""
echo "后端服务: http://localhost:5000"
echo "前端服务: http://localhost:5173"
echo "管理后台: http://localhost:5173/admin"
echo ""
echo "管理员账号: admin"
echo "管理员密码: admin123"
echo ""

# Start backend in background (using virtual environment)
cd backend
VENV_PYTHON="../venv/bin/python"
$VENV_PYTHON app.py &
BACKEND_PID=$!
echo "后端服务已启动 (PID: $BACKEND_PID, 使用虚拟环境: $VENV_PYTHON)"
cd ..

# Wait for backend to start
sleep 3

# Start frontend in background
cd frontend
npm run dev &
FRONTEND_PID=$!
echo "前端服务已启动 (PID: $FRONTEND_PID)"
cd ..

echo ""
echo "========================================"
echo "服务已启动！"
echo "========================================"
echo "按 Ctrl+C 停止所有服务"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "正在停止服务..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    deactivate 2>/dev/null
    echo "服务已停止"
    exit 0
}

# Trap SIGINT and SIGTERM
trap cleanup SIGINT SIGTERM

# Wait for processes
wait
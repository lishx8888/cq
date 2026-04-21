@echo off
echo ================================================
echo   PURE LAB 护肤产品展示网站 - 启动脚本
echo ================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

:: Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Node.js，请先安装 Node.js 18+
    pause
    exit /b 1
)

echo [1/3] 安装后端依赖...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [错误] 后端依赖安装失败
    pause
    exit /b 1
)
cd ..

echo.
echo [2/3] 安装前端依赖...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo [错误] 前端依赖安装失败
    pause
    exit /b 1
)
cd ..

echo.
echo [3/3] 启动服务...
echo.
echo 后端服务: http://localhost:5000
echo 前端服务: http://localhost:5173
echo 管理后台: http://localhost:5173/admin
echo.
echo 管理员账号: admin
echo 管理员密码: admin123
echo.

:: Start backend in new window
start cmd /k "cd backend && python app.py"

:: Wait a bit for backend to start
timeout /t 3 /nobreak >nul

:: Start frontend
cd frontend && npm run dev

pause

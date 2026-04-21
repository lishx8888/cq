#!/bin/bash

echo "========================================"
echo "  PURE LAB 虚拟环境管理工具"
echo "========================================"
echo ""

VENV_DIR="venv"

# Function to create virtual environment
create_venv() {
    echo "创建虚拟环境..."
    if [ -d "$VENV_DIR" ]; then
        echo "虚拟环境已存在，是否删除并重建？ (y/n)"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            rm -rf "$VENV_DIR"
            echo "已删除旧虚拟环境"
        else
            echo "取消创建"
            return 1
        fi
    fi
    
    python3 -m venv "$VENV_DIR"
    if [ $? -eq 0 ]; then
        echo "虚拟环境创建成功"
        source "$VENV_DIR/bin/activate"
        echo "安装后端依赖..."
        cd backend
        pip install -r requirements.txt
        cd ..
        echo "依赖安装完成"
        deactivate
    else
        echo "虚拟环境创建失败"
        return 1
    fi
}

# Function to activate virtual environment
activate_venv() {
    if [ -d "$VENV_DIR" ]; then
        echo "激活虚拟环境..."
        source "$VENV_DIR/bin/activate"
        echo "虚拟环境已激活"
        echo "当前 Python 路径: $(which python)"
        echo "要退出虚拟环境，请输入: deactivate"
    else
        echo "虚拟环境不存在，请先创建虚拟环境"
        return 1
    fi
}

# Function to check virtual environment status
check_status() {
    if [ -d "$VENV_DIR" ]; then
        echo "虚拟环境状态: 已存在"
        echo "虚拟环境路径: $(pwd)/$VENV_DIR"
        if [ -f "$VENV_DIR/bin/python" ]; then
            echo "Python 版本: $($VENV_DIR/bin/python --version)"
        fi
        if [ -f "$VENV_DIR/bin/pip" ]; then
            echo "Pip 版本: $($VENV_DIR/bin/pip --version)"
        fi
        echo ""
        echo "已安装的包:"
        source "$VENV_DIR/bin/activate"
        pip list
        deactivate
    else
        echo "虚拟环境状态: 不存在"
    fi
}

# Function to delete virtual environment
delete_venv() {
    if [ -d "$VENV_DIR" ]; then
        echo "确定要删除虚拟环境吗？ (y/n)"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            rm -rf "$VENV_DIR"
            echo "虚拟环境已删除"
        else
            echo "取消删除"
        fi
    else
        echo "虚拟环境不存在"
    fi
}

# Function to update dependencies
update_deps() {
    if [ -d "$VENV_DIR" ]; then
        echo "更新依赖..."
        source "$VENV_DIR/bin/activate"
        cd backend
        pip install --upgrade -r requirements.txt
        cd ..
        deactivate
        echo "依赖更新完成"
    else
        echo "虚拟环境不存在，请先创建虚拟环境"
        return 1
    fi
}

# Function to export requirements
export_req() {
    if [ -d "$VENV_DIR" ]; then
        echo "导出依赖列表..."
        source "$VENV_DIR/bin/activate"
        pip freeze > requirements_export.txt
        deactivate
        echo "依赖列表已导出到 requirements_export.txt"
    else
        echo "虚拟环境不存在"
        return 1
    fi
}

# Menu
case "${1:-}" in
    "create")
        create_venv
        ;;
    "activate")
        activate_venv
        ;;
    "status")
        check_status
        ;;
    "delete")
        delete_venv
        ;;
    "update")
        update_deps
        ;;
    "export")
        export_req
        ;;
    *)
        echo "用法: $0 {create|activate|status|delete|update|export}"
        echo ""
        echo "命令说明:"
        echo "  create   - 创建虚拟环境并安装依赖"
        echo "  activate - 激活虚拟环境"
        echo "  status   - 查看虚拟环境状态"
        echo "  delete   - 删除虚拟环境"
        echo "  update   - 更新依赖"
        echo "  export   - 导出依赖列表"
        ;;
esac
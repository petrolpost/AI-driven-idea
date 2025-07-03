# AI决策框架项目 Makefile
# 提供便捷的开发和部署命令

.PHONY: help install install-dev install-full sync clean format lint test test-cov dev start build publish info

# 默认目标
help:
	@echo "AI决策框架项目 - 可用命令:"
	@echo ""
	@echo "安装和环境:"
	@echo "  install      - 安装基础依赖"
	@echo "  install-dev  - 安装开发依赖"
	@echo "  install-full - 安装完整功能依赖"
	@echo "  sync         - 同步依赖到最新版本"
	@echo "  clean        - 清理缓存和临时文件"
	@echo ""
	@echo "代码质量:"
	@echo "  format       - 格式化代码"
	@echo "  lint         - 代码检查"
	@echo "  test         - 运行测试"
	@echo "  test-cov     - 运行测试并生成覆盖率报告"
	@echo ""
	@echo "开发和部署:"
	@echo "  dev          - 启动开发服务器"
	@echo "  start        - 启动生产服务器"
	@echo "  build        - 构建项目"
	@echo "  publish      - 发布项目"
	@echo "  info         - 显示项目信息"
	@echo ""

# 安装基础依赖
install:
	@echo "📦 安装基础依赖..."
	uv sync

# 安装开发依赖
install-dev:
	@echo "🛠️ 安装开发依赖..."
	uv sync --extra dev

# 安装完整功能依赖
install-full:
	@echo "🚀 安装完整功能依赖..."
	uv sync --extra full

# 同步依赖
sync:
	@echo "🔄 同步依赖到最新版本..."
	uv sync --upgrade

# 清理缓存和临时文件
clean:
	@echo "🧹 清理缓存和临时文件..."
	uv cache clean
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# 格式化代码
format:
	@echo "✨ 格式化代码..."
	uv run black .
	uv run ruff check --fix .

# 代码检查
lint:
	@echo "🔍 代码检查..."
	uv run ruff check .
	uv run mypy .

# 运行测试
test:
	@echo "🧪 运行测试..."
	uv run pytest tests/ -v

# 运行测试并生成覆盖率报告
test-cov:
	@echo "📊 运行测试并生成覆盖率报告..."
	uv run pytest tests/ --cov=ai_decision_framework --cov-report=html --cov-report=term
	@echo "📈 覆盖率报告已生成到 htmlcov/index.html"

# 启动开发服务器
dev:
	@echo "🚀 启动开发服务器..."
	uv run python run.py --host localhost --port 8000

# 启动生产服务器
start:
	@echo "🌐 启动生产服务器..."
	uv run python run.py --host 0.0.0.0 --port 8000 --workers 4

# 构建项目
build:
	@echo "🔨 构建项目..."
	uv build

# 发布项目
publish:
	@echo "📤 发布项目..."
	uv publish

# 显示项目信息
info:
	@echo "ℹ️ 项目信息:"
	uv run python run.py --info

# 初始化开发环境
init-dev: install-dev
	@echo "🎯 初始化开发环境..."
	uv run pre-commit install
	@echo "✅ 开发环境初始化完成!"

# 检查项目健康状态
check: format lint test
	@echo "✅ 项目健康检查完成!"

# 快速启动（安装依赖并启动开发服务器）
quick-start: install-dev dev

# 部署准备（检查、测试、构建）
deploy-prep: check build
	@echo "🚀 部署准备完成!"
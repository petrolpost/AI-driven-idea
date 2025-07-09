#!/usr/bin/env python3
"""
AI决策框架快速启动脚本

使用方法:
    python run.py              # 启动开发服务器
    python run.py --prod       # 启动生产服务器
    python run.py --help       # 查看帮助信息
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

def check_requirements():
    """检查依赖是否安装"""
    try:
        import fastapi
        import uvicorn
        import pydantic
        print("✅ 核心依赖检查通过")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def check_env_file():
    """检查环境配置文件"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("⚠️  未找到 .env 文件")
            print("请复制 .env.example 为 .env 并配置相应参数")
            
            # 询问是否自动创建
            response = input("是否自动创建基础 .env 文件? (y/n): ")
            if response.lower() in ['y', 'yes', '是']:
                env_example.rename(env_file)
                print("✅ 已创建 .env 文件，请根据需要修改配置")
                return True
            else:
                return False
        else:
            print("❌ 未找到环境配置文件")
            return False
    else:
        print("✅ 环境配置文件检查通过")
        return True

def create_directories():
    """创建必要的目录"""
    directories = [
        "logs",
        "static",
        "assets/css",
        "assets/js",
        "assets/images"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ 目录结构检查完成")

def run_development_server(host="localhost", port=8000):
    """启动开发服务器"""
    print(f"🚀 启动开发服务器: http://{host}:{port}")
    print("按 Ctrl+C 停止服务器")
    print("-" * 50)
    
    try:
        import uvicorn
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

def run_production_server(host="0.0.0.0", port=8000, workers=4):
    """启动生产服务器"""
    print(f"🚀 启动生产服务器: http://{host}:{port}")
    print(f"工作进程数: {workers}")
    print("-" * 50)
    
    try:
        import uvicorn
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            workers=workers,
            log_level="warning"
        )
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

def install_dependencies():
    """安装项目依赖"""
    print("📦 安装项目依赖...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✅ 依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False
    except FileNotFoundError:
        print("❌ 未找到 requirements.txt 文件")
        return False

def show_project_info():
    """显示项目信息"""
    print("="*60)
    print("🤖 AI决策框架 - AI工作流vs智能体决策支持系统")
    print("="*60)
    print("📁 项目结构:")
    print("  ├── main.py              # 主应用文件")
    print("  ├── index.html           # 前端评分界面")
    print("  ├── requirements.txt     # 项目依赖")
    print("  ├── .env.example         # 环境配置模板")
    print("  ├── README.md            # 项目说明")
    print("  ├── docs/                # 文档目录")
    print("  │   ├── decision-framework.md")
    print("  │   └── case-studies.md")
    print("  └── examples/            # 示例代码")
    print("      ├── workflow-example.md")
    print("      ├── agent-example.md")
    print("      └── hybrid-example.md")
    print()
    print("🌐 访问地址:")
    print("  - 主页: http://localhost:8000")
    print("  - API文档: http://localhost:8000/docs")
    print("  - 健康检查: http://localhost:8000/health")
    print("  - 统计信息: http://localhost:8000/stats")
    print()

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="AI决策框架启动脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python run.py                    # 启动开发服务器
  python run.py --prod             # 启动生产服务器
  python run.py --install          # 安装依赖
  python run.py --host 0.0.0.0     # 指定主机地址
  python run.py --port 9000        # 指定端口
        """
    )
    
    parser.add_argument("--prod", action="store_true", 
                       help="启动生产服务器")
    parser.add_argument("--install", action="store_true", 
                       help="安装项目依赖")
    parser.add_argument("--host", default="localhost", 
                       help="服务器主机地址 (默认: localhost)")
    parser.add_argument("--port", type=int, default=8000, 
                       help="服务器端口 (默认: 8000)")
    parser.add_argument("--workers", type=int, default=4, 
                       help="生产服务器工作进程数 (默认: 4)")
    parser.add_argument("--info", action="store_true", 
                       help="显示项目信息")
    
    args = parser.parse_args()
    
    # 显示项目信息
    if args.info:
        show_project_info()
        return
    
    # 安装依赖
    if args.install:
        if install_dependencies():
            print("\n🎉 依赖安装完成，现在可以启动服务器了")
            print("运行: python run.py")
        return
    
    # 显示项目信息
    show_project_info()
    
    # 检查环境
    print("🔍 环境检查...")
    
    if not check_requirements():
        print("\n💡 提示: 运行 'python run.py --install' 安装依赖")
        sys.exit(1)
    
    if not check_env_file():
        sys.exit(1)
    
    create_directories()
    
    print("\n" + "="*50)
    
    # 启动服务器
    if args.prod:
        run_production_server(args.host, args.port, args.workers)
    else:
        run_development_server(args.host, args.port)

if __name__ == "__main__":
    main()
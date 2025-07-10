#!/usr/bin/env python3
"""
数据库迁移脚本：添加source_url字段到projects表

这个脚本会安全地为现有的projects表添加source_url字段。
如果字段已存在，脚本会跳过添加操作。
"""

import sqlite3
import os
from pathlib import Path

def get_database_path():
    """获取数据库文件路径"""
    current_dir = Path(__file__).parent
    db_path = current_dir / "navigator.db"
    return str(db_path)

def check_column_exists(cursor, table_name, column_name):
    """检查表中是否存在指定列"""
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]
    return column_name in column_names

def add_source_url_column():
    """添加source_url字段到projects表"""
    db_path = get_database_path()
    
    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}")
        print("请先启动应用程序以创建数据库。")
        return False
    
    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查projects表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects'")
        if not cursor.fetchone():
            print("projects表不存在，无需迁移。")
            conn.close()
            return True
        
        # 检查source_url字段是否已存在
        if check_column_exists(cursor, 'projects', 'source_url'):
            print("source_url字段已存在，无需添加。")
            conn.close()
            return True
        
        # 添加source_url字段
        print("正在添加source_url字段到projects表...")
        cursor.execute("ALTER TABLE projects ADD COLUMN source_url TEXT")
        
        # 提交更改
        conn.commit()
        print("✅ 成功添加source_url字段！")
        
        # 验证字段已添加
        if check_column_exists(cursor, 'projects', 'source_url'):
            print("✅ 字段添加验证成功！")
        else:
            print("❌ 字段添加验证失败！")
            return False
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ 数据库操作失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 迁移过程中发生错误: {e}")
        return False

def main():
    """主函数"""
    print("=== 数据库迁移：添加source_url字段 ===")
    print()
    
    success = add_source_url_column()
    
    print()
    if success:
        print("🎉 迁移完成！现在可以重新启动应用程序。")
    else:
        print("💥 迁移失败！请检查错误信息并重试。")
    
    return success

if __name__ == "__main__":
    main()
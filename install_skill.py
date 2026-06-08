#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
安装脚本：将 newsmth-career-search skill 复制到 OpenClaw 的 skills 目录
"""

import os
import shutil
import sys


def install_skill():
    """安装 skill 到 OpenClaw 目录"""
    # 源目录（当前项目目录）
    source_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 目标目录（OpenClaw skills 目录）
    target_dir = r"C:\Users\tchu\.openclaw\workspace\skills\newsmth-career-search"
    
    print(f"源目录: {source_dir}")
    print(f"目标目录: {target_dir}")
    
    # 检查源文件是否存在
    required_files = ['SKILL.md', 'search_newsmth.py', 'requirements.txt']
    for file in required_files:
        file_path = os.path.join(source_dir, file)
        if not os.path.exists(file_path):
            print(f"错误：缺少必要文件 {file}")
            sys.exit(1)
    
    # 如果目标目录已存在，先删除
    if os.path.exists(target_dir):
        print(f"目标目录已存在，正在删除...")
        shutil.rmtree(target_dir)
    
    # 创建目标目录
    os.makedirs(target_dir, exist_ok=True)
    
    # 复制文件
    files_to_copy = [
        'SKILL.md',
        'search_newsmth.py',
        'requirements.txt',
        '.gitignore',
        'mock_career_upgrade.html',
        'test_mock.py'
    ]
    
    copied_files = []
    for file in files_to_copy:
        source_file = os.path.join(source_dir, file)
        if os.path.exists(source_file):
            target_file = os.path.join(target_dir, file)
            shutil.copy2(source_file, target_file)
            copied_files.append(file)
            print(f"  复制: {file}")
    
    print(f"\n成功复制 {len(copied_files)} 个文件")
    
    # 验证安装
    print("\n验证安装...")
    skill_md_path = os.path.join(target_dir, 'SKILL.md')
    if os.path.exists(skill_md_path):
        print(f"  SKILL.md 存在")
        # 读取 skill 名称
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if first_line == '---':
                # 读取 YAML front matter
                lines = []
                for line in f:
                    if line.strip() == '---':
                        break
                    lines.append(line.strip())
                for line in lines:
                    if line.startswith('name:'):
                        skill_name = line.split(':', 1)[1].strip()
                        print(f"  Skill 名称: {skill_name}")
                        break
    
    script_path = os.path.join(target_dir, 'search_newsmth.py')
    if os.path.exists(script_path):
        print(f"  search_newsmth.py 存在")
    
    print(f"\n安装完成！")
    print(f"Skill 路径: {target_dir}")
    print(f"\n使用方法:")
    print(f"  1. 安装依赖: cd \"{target_dir}\" && pip install -r requirements.txt")
    print(f"  2. 搜索招聘: python search_newsmth.py \"Python\" --board career")
    print(f"  3. 获取新闻: python search_newsmth.py --board working --max-posts 10")
    print(f"  4. 总结新闻: python search_newsmth.py --board working --summarize")


if __name__ == "__main__":
    install_skill()

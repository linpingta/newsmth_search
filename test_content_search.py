#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
内容搜索测试脚本
用于本地测试帖子内容搜索功能
"""

import sys
import os
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Optional


def get_post_content_text(html: str) -> Optional[str]:
    """获取帖子的纯文本内容"""
    soup = BeautifulSoup(html, 'lxml')
    
    # 查找帖子内容区域
    content_div = soup.find('div', class_='b-content')
    if content_div:
        # 提取所有文本，去除多余空白
        text = content_div.get_text(separator='\n', strip=True)
        # 清理文本
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return '\n'.join(lines)
    
    # 如果找不到 b-content，尝试其他选择器
    article = soup.find('article') or soup.find('div', class_='article')
    if article:
        return article.get_text(separator='\n', strip=True)
    
    return None


def search_content_in_post(html: str, keyword: str) -> bool:
    """检查帖子内容是否包含关键字"""
    content = get_post_content_text(html)
    if content:
        return keyword.lower() in content.lower()
    return False


def main():
    """主函数"""
    mock_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mock_post_content.html')
    
    if not os.path.exists(mock_file):
        print(f"错误：找不到 mock 文件 {mock_file}", file=sys.stderr)
        sys.exit(1)
    
    with open(mock_file, 'r', encoding='utf-8') as f:
        mock_html = f.read()
    
    print("=" * 60)
    print("Mock 内容搜索测试")
    print("=" * 60)
    
    # 测试 1: 提取帖子内容
    print("\n【测试 1】提取帖子内容")
    print("-" * 40)
    content = get_post_content_text(mock_html)
    if content:
        print("成功提取内容，前 300 字符：")
        print(content[:300])
        print("...")
    else:
        print("无法提取内容")
    
    # 测试 2: 搜索关键字 "Python"
    print("\n【测试 2】搜索关键字: Python")
    print("-" * 40)
    found = search_content_in_post(mock_html, "Python")
    print(f"结果: {'找到' if found else '未找到'}")
    
    # 测试 3: 搜索关键字 "Django"
    print("\n【测试 3】搜索关键字: Django")
    print("-" * 40)
    found = search_content_in_post(mock_html, "Django")
    print(f"结果: {'找到' if found else '未找到'}")
    
    # 测试 4: 搜索关键字 "北京"
    print("\n【测试 4】搜索关键字: 北京")
    print("-" * 40)
    found = search_content_in_post(mock_html, "北京")
    print(f"结果: {'找到' if found else '未找到'}")
    
    # 测试 5: 搜索关键字 "不存在的关键字"
    print("\n【测试 5】搜索关键字: 不存在的关键字")
    print("-" * 40)
    found = search_content_in_post(mock_html, "不存在的关键字")
    print(f"结果: {'找到' if found else '未找到'}")
    
    # 测试 6: 搜索关键字 "量化交易"
    print("\n【测试 6】搜索关键字: 量化交易")
    print("-" * 40)
    found = search_content_in_post(mock_html, "量化交易")
    print(f"结果: {'找到' if found else '未找到'}")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

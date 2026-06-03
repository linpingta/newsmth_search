#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mock 数据测试脚本
用于本地测试搜索逻辑，无需联网
"""

import sys
import os
from bs4 import BeautifulSoup
import re
from typing import List, Dict

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def parse_board_page(html: str, keyword: str, board_name: str) -> List[Dict]:
    """解析板块页面，搜索关键字"""
    results = []
    soup = BeautifulSoup(html, 'lxml')
    
    title_cells = soup.find_all('td', class_='title_9')
    
    for cell in title_cells:
        # 找到所有包含 /nForum/article/ 的链接，取第二个（标题链接）
        links = cell.find_all('a', href=re.compile(r'/nForum/article/'))
        # 第一个链接是"新窗口打开"图标，第二个才是标题链接
        link = links[1] if len(links) > 1 else (links[0] if links else None)
        if link:
            title = link.get_text(strip=True)
            href = link.get('href', '')
            full_url = f"https://www.newsmth.net{href}" if href.startswith('/') else href
            
            if title and keyword.lower() in title.lower():
                row = link.find_parent('tr')
                publish_time = ''
                if row:
                    time_cell = row.find('td', class_='title_10')
                    if time_cell:
                        publish_time = time_cell.get_text(strip=True)
                
                results.append({
                    'title': title,
                    'board': board_name,
                    'publish_time': publish_time,
                    'url': full_url,
                    'summary': '',
                })
    
    return results


def parse_latest_posts(html: str, board_name: str, max_posts: int = 10) -> List[Dict]:
    """解析板块页面，获取最新帖子"""
    results = []
    soup = BeautifulSoup(html, 'lxml')
    
    title_cells = soup.find_all('td', class_='title_9')
    
    skip_titles = ['欢迎关注水木职版官方号', '审核通过WorkingLife版治版方针', '状态主题发帖时间']
    
    for cell in title_cells:
        if len(results) >= max_posts:
            break
        
        links = cell.find_all('a', href=re.compile(r'/nForum/article/'))
        link = links[1] if len(links) > 1 else (links[0] if links else None)
        if link:
            title = link.get_text(strip=True)
            href = link.get('href', '')
            full_url = f"https://www.newsmth.net{href}" if href.startswith('/') else href
            
            if title and len(title) > 3 and title not in skip_titles:
                row = link.find_parent('tr')
                publish_time = ''
                if row:
                    time_cell = row.find('td', class_='title_10')
                    if time_cell:
                        publish_time = time_cell.get_text(strip=True)
                
                results.append({
                    'title': title,
                    'board': board_name,
                    'publish_time': publish_time,
                    'url': full_url,
                    'summary': '',
                })
    
    return results


def format_career_results(results: List[Dict]) -> str:
    """格式化招聘搜索结果"""
    if not results:
        return "未找到相关招聘信息。"
    
    output = []
    output.append(f"在 Career_Upgrade 板块找到 {len(results)} 条相关招聘信息：\n")
    
    for i, result in enumerate(results, 1):
        output.append(f"{i}. {result['title']}")
        if result.get('publish_time'):
            output.append(f"   发布时间：{result['publish_time']}")
        output.append(f"   板块：{result['board']}")
        output.append(f"   链接：{result['url']}")
        output.append("")
    
    return "\n".join(output)


def main():
    """主函数"""
    mock_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mock_career_upgrade.html')
    
    if not os.path.exists(mock_file):
        print(f"错误：找不到 mock 文件 {mock_file}", file=sys.stderr)
        sys.exit(1)
    
    with open(mock_file, 'r', encoding='utf-8') as f:
        mock_html = f.read()
    
    print("=" * 60)
    print("Mock 数据测试 - 搜索招聘信息")
    print("=" * 60)
    
    # 测试 1: 搜索 "Python"
    print("\n【测试 1】搜索关键字: Python")
    print("-" * 40)
    results = parse_board_page(mock_html, "Python", "Career_Upgrade")
    print(format_career_results(results))
    
    # 测试 2: 搜索 "Java"
    print("\n【测试 2】搜索关键字: Java")
    print("-" * 40)
    results = parse_board_page(mock_html, "Java", "Career_Upgrade")
    print(format_career_results(results))
    
    # 测试 3: 搜索 "前端"
    print("\n【测试 3】搜索关键字: 前端")
    print("-" * 40)
    results = parse_board_page(mock_html, "前端", "Career_Upgrade")
    print(format_career_results(results))
    
    # 测试 4: 搜索 "招聘"（通用关键字）
    print("\n【测试 4】搜索关键字: 招聘")
    print("-" * 40)
    results = parse_board_page(mock_html, "招聘", "Career_Upgrade")
    print(format_career_results(results))
    
    # 测试 5: 获取所有帖子（不搜索关键字）
    print("\n【测试 5】获取所有最新帖子")
    print("-" * 40)
    results = parse_latest_posts(mock_html, "Career_Upgrade", max_posts=10)
    print(f"共获取 {len(results)} 条帖子：\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']}")
        print(f"   发布时间：{result['publish_time']}")
        print(f"   链接：{result['url']}")
        print("")
    
    print("=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

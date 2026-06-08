#!/usr/bin/env python3
"""
水木社区职场搜索工具
- Career_Upgrade: 招聘信息搜索
- WorkingLife: 职场新闻/动态搜索和总结
"""

import requests
from bs4 import BeautifulSoup
import re
import sys
import json
from urllib.parse import urljoin, urlparse, parse_qs
from typing import List, Dict, Optional
import time
import argparse


class NewsmthSearcher:
    """水木社区板块搜索器"""
    
    BASE_URL = "https://www.newsmth.net"
    
    BOARDS = {
        "career": {
            "name": "Career_Upgrade",
            "url": "https://www.newsmth.net/nForum/board/Career_Upgrade",
            "description": "职场招聘板块"
        },
        "working": {
            "name": "WorkingLife",
            "url": "https://www.newsmth.net/nForum/board/WorkingLife",
            "description": "职场生活板块"
        }
    }
    
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def search_career(self, keyword: str, max_pages: int = 3, search_content: bool = False, max_content_posts: int = 10) -> List[Dict]:
        """搜索Career_Upgrade板块的招聘信息
        
        Args:
            keyword: 搜索关键字
            max_pages: 搜索的板块页数
            search_content: 是否搜索帖子内容（而不仅是标题）
            max_content_posts: 最多检查内容的帖子数量
        """
        if search_content:
            return self._search_board_content("career", keyword, max_pages, max_content_posts)
        return self._search_board("career", keyword, max_pages)
    
    def search_working(self, max_posts: int = 10) -> List[Dict]:
        """获取WorkingLife板块的最新帖子"""
        return self._get_latest_posts("working", max_posts)
    
    def _search_board(self, board_key: str, keyword: str, max_pages: int = 3) -> List[Dict]:
        """搜索指定板块的帖子（仅标题）"""
        board = self.BOARDS[board_key]
        results = []
        
        for page in range(1, max_pages + 1):
            try:
                board_url = f"{board['url']}?p={page}"
                response = self.session.get(board_url, timeout=20)
                
                if response.status_code == 200:
                    page_results = self._parse_board_page(response.text, keyword, board["name"])
                    results.extend(page_results)
                    
                    if not page_results:
                        break
                
                time.sleep(1.5)
                
            except requests.RequestException as e:
                print(f"获取第{page}页出错: {e}", file=sys.stderr)
                time.sleep(2)
                continue
        
        return results
    
    def _search_board_content(self, board_key: str, keyword: str, max_pages: int = 3, max_posts: int = 10) -> List[Dict]:
        """搜索指定板块的帖子（包括内容）
        
        先搜索标题，如果标题不匹配，再获取帖子内容检查
        """
        board = self.BOARDS[board_key]
        results = []
        posts_checked = 0
        
        for page in range(1, max_pages + 1):
            try:
                board_url = f"{board['url']}?p={page}"
                response = self.session.get(board_url, timeout=20)
                
                if response.status_code == 200:
                    # 先获取所有帖子
                    posts = self._parse_latest_posts(response.text, board["name"], max_posts=100)
                    
                    for post in posts:
                        if posts_checked >= max_posts:
                            break
                        
                        posts_checked += 1
                        
                        # 1. 先检查标题
                        if keyword.lower() in post['title'].lower():
                            results.append(post)
                            continue
                        
                        # 2. 标题不匹配，获取内容检查
                        print(f"  检查帖子内容: {post['title'][:30]}...", file=sys.stderr)
                        content = self._get_post_content_text(post['url'])
                        
                        if content and keyword.lower() in content.lower():
                            post['summary'] = content[:200] + "..." if len(content) > 200 else content
                            results.append(post)
                        
                        time.sleep(1)  # 避免请求过快
                    
                    if posts_checked >= max_posts:
                        break
                
                time.sleep(1.5)
                
            except requests.RequestException as e:
                print(f"获取第{page}页出错: {e}", file=sys.stderr)
                time.sleep(2)
                continue
        
        return results
    
    def _get_post_content_text(self, url: str) -> Optional[str]:
        """获取帖子的纯文本内容"""
        try:
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                
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
        
        except requests.RequestException as e:
            print(f"获取帖子内容出错: {e}", file=sys.stderr)
        
        return None
    
    def _get_latest_posts(self, board_key: str, max_posts: int = 10) -> List[Dict]:
        """获取指定板块的最新帖子"""
        board = self.BOARDS[board_key]
        results = []
        
        try:
            response = self.session.get(board["url"], timeout=20)
            
            if response.status_code == 200:
                results = self._parse_latest_posts(response.text, board["name"], max_posts)
        
        except requests.RequestException as e:
            print(f"获取板块出错: {e}", file=sys.stderr)
        
        return results
    
    def _parse_board_page(self, html: str, keyword: str, board_name: str) -> List[Dict]:
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
                full_url = f"{self.BASE_URL}{href}" if href.startswith('/') else href
                
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
    
    def _parse_latest_posts(self, html: str, board_name: str, max_posts: int = 10) -> List[Dict]:
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
                full_url = f"{self.BASE_URL}{href}" if href.startswith('/') else href
                
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
    
    def get_post_content(self, board: str, post_id: str) -> Optional[str]:
        """获取帖子内容"""
        try:
            url = f"{self.BASE_URL}/nForum/article/{board}/{post_id}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                content = soup.get_text()
                return content[:2000]
        
        except requests.RequestException as e:
            print(f"获取帖子内容出错: {e}", file=sys.stderr)
        
        return None
    
    def format_career_results(self, results: List[Dict]) -> str:
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
            if result.get('summary'):
                output.append(f"   内容摘要：{result['summary']}")
            if result.get('url'):
                output.append(f"   链接：{result['url']}")
            output.append("")
        
        return "\n".join(output)
    
    def format_working_results(self, results: List[Dict]) -> str:
        """格式化职场新闻结果"""
        if not results:
            return "未获取到职场新闻。"
        
        output = []
        output.append(f"WorkingLife 板块最新 {len(results)} 条职场动态：\n")
        
        for i, result in enumerate(results, 1):
            output.append(f"{i}. {result['title']}")
            if result.get('publish_time'):
                output.append(f"   发布时间：{result['publish_time']}")
            output.append("")
        
        return "\n".join(output)


def summarize_posts(searcher: NewsmthSearcher, posts: List[Dict]) -> str:
    """总结帖子内容"""
    if not posts:
        return "没有可总结的内容。"
    
    summary = []
    summary.append("职场新闻总结：\n")
    
    for i, post in enumerate(posts[:5], 1):
        title = post.get('title', '')
        summary.append(f"{i}. {title}")
    
    summary.append(f"\n共获取 {len(posts)} 条职场动态。")
    summary.append("热门话题包括职场压力、求职面试、行业动态等。")
    
    return "\n".join(summary)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='水木社区职场搜索工具')
    parser.add_argument('keyword', nargs='?', default='', help='搜索关键字')
    parser.add_argument('--board', choices=['career', 'working'], default='career', help='搜索板块 (默认: career)')
    parser.add_argument('--max-pages', type=int, default=3, help='最大搜索页数 (默认: 3)')
    parser.add_argument('--max-posts', type=int, default=10, help='最大帖子数 (默认: 10)')
    parser.add_argument('--json', action='store_true', help='以JSON格式输出')
    parser.add_argument('--summarize', action='store_true', help='总结职场新闻')
    parser.add_argument('--post-id', type=str, help='获取指定帖子内容')
    parser.add_argument('--search-content', action='store_true', help='搜索帖子内容（而不仅是标题）')
    parser.add_argument('--max-content-posts', type=int, default=10, help='内容搜索时最多检查的帖子数 (默认: 10)')
    
    args = parser.parse_args()
    
    searcher = NewsmthSearcher()
    
    if args.post_id:
        content = searcher.get_post_content(args.board, args.post_id)
        if content:
            print(content)
        else:
            print("无法获取帖子内容", file=sys.stderr)
            sys.exit(1)
    
    elif args.board == 'career':
        if not args.keyword:
            print("请提供搜索关键字", file=sys.stderr)
            sys.exit(1)
        
        results = searcher.search_career(
            args.keyword, 
            args.max_pages, 
            search_content=args.search_content,
            max_content_posts=args.max_content_posts
        )
        
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(searcher.format_career_results(results))
    
    elif args.board == 'working':
        results = searcher.search_working(args.max_posts)
        
        if args.summarize:
            print(summarize_posts(searcher, results))
        elif args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(searcher.format_working_results(results))


if __name__ == '__main__':
    main()

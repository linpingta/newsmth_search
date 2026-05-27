#!/usr/bin/env python3
"""
水木社区职场招聘板块搜索工具
搜索 newsmth.net Job 板块的招聘信息
"""

import requests
from bs4 import BeautifulSoup
import re
import sys
import json
from urllib.parse import urljoin
from typing import List, Dict, Optional
import time


class NewsmthJobSearcher:
    """水木社区Job板块搜索器"""
    
    BASE_URL = "https://www.newsmth.net"
    JOB_BOARD_URL = "https://www.newsmth.net/nForum/board/Job"
    SEARCH_URL = "https://www.newsmth.net/nForum/search"
    
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
    
    def search_by_keyword(self, keyword: str, max_pages: int = 3) -> List[Dict]:
        """
        根据关键字搜索Job板块帖子
        
        Args:
            keyword: 搜索关键字
            max_pages: 最大搜索页数
            
        Returns:
            搜索结果列表
        """
        results = []
        
        try:
            # 方法1: 使用水木社区的搜索功能
            search_params = {
                "kw": keyword,
                "board": "Job",
                "p": 1,
            }
            
            response = self.session.get(
                self.SEARCH_URL,
                params=search_params,
                timeout=10,
                allow_redirects=True
            )
            
            if response.status_code == 200:
                results = self._parse_search_results(response.text)
            
            # 如果搜索结果不理想，尝试直接浏览Job板块
            if not results:
                results = self._browse_job_board(keyword, max_pages)
                
        except requests.RequestException as e:
            print(f"搜索出错: {e}", file=sys.stderr)
            # 尝试直接浏览板块
            results = self._browse_job_board(keyword, max_pages)
        
        return results
    
    def _parse_search_results(self, html: str) -> List[Dict]:
        """解析搜索结果页面"""
        results = []
        soup = BeautifulSoup(html, 'lxml')
        
        # 查找帖子列表
        post_items = soup.find_all('li', class_=re.compile(r'.*post.*|.*topic.*|.*thread.*'))
        
        if not post_items:
            # 尝试其他可能的选择器
            post_items = soup.find_all('tr', class_=re.compile(r('.*')))
        
        for item in post_items:
            try:
                result = self._extract_post_info(item)
                if result:
                    results.append(result)
            except Exception:
                continue
        
        return results
    
    def _browse_job_board(self, keyword: str, max_pages: int = 3) -> List[Dict]:
        """直接浏览Job板块并搜索关键字"""
        results = []
        
        for page in range(1, max_pages + 1):
            try:
                board_url = f"{self.JOB_BOARD_URL}?p={page}"
                response = self.session.get(board_url, timeout=10)
                
                if response.status_code == 200:
                    page_results = self._parse_board_page(response.text, keyword)
                    results.extend(page_results)
                    
                    # 如果当前页没有结果，可能后续页也没有
                    if not page_results:
                        break
                
                # 礼貌延迟
                time.sleep(1)
                
            except requests.RequestException as e:
                print(f"获取第{page}页出错: {e}", file=sys.stderr)
                break
        
        return results
    
    def _parse_board_page(self, html: str, keyword: str) -> List[Dict]:
        """解析板块页面"""
        results = []
        soup = BeautifulSoup(html, 'lxml')
        
        # 水木社区帖子列表通常在 table 或 div 中
        # 查找所有可能的帖子链接
        links = soup.find_all('a', href=re.compile(r'/nForum/article/'))
        
        for link in links:
            title = link.get_text(strip=True)
            
            # 检查标题是否包含关键字
            if keyword.lower() in title.lower():
                href = link.get('href', '')
                full_url = urljoin(self.BASE_URL, href)
                
                # 提取帖子ID
                post_id = self._extract_post_id(href)
                
                results.append({
                    'title': title,
                    'url': full_url,
                    'post_id': post_id,
                    'board': 'Job',
                    'summary': '',
                    'publish_time': '',
                })
        
        return results
    
    def _extract_post_info(self, element) -> Optional[Dict]:
        """从帖子元素中提取信息"""
        try:
            title_elem = element.find('a', href=re.compile(r'/nForum/article/'))
            if not title_elem:
                return None
            
            title = title_elem.get_text(strip=True)
            href = title_elem.get('href', '')
            full_url = urljoin(self.BASE_URL, href)
            post_id = self._extract_post_id(href)
            
            # 尝试提取时间和摘要
            time_elem = element.find(class_=re.compile(r'.*time.*|.*date.*'))
            publish_time = time_elem.get_text(strip=True) if time_elem else ''
            
            summary_elem = element.find(class_=re.compile(r('.*summary.*|.*content.*|.*abstract.*')))
            summary = summary_elem.get_text(strip=True)[:200] if summary_elem else ''
            
            return {
                'title': title,
                'url': full_url,
                'post_id': post_id,
                'board': 'Job',
                'summary': summary,
                'publish_time': publish_time,
            }
        except Exception:
            return None
    
    def _extract_post_id(self, href: str) -> str:
        """从URL中提取帖子ID"""
        match = re.search(r'article/(\w+)/(\d+)', href)
        if match:
            return match.group(2)
        return ''
    
    def get_post_detail(self, post_url: str) -> Optional[Dict]:
        """获取帖子详情"""
        try:
            response = self.session.get(post_url, timeout=10)
            if response.status_code == 200:
                return self._parse_post_detail(response.text)
        except requests.RequestException as e:
            print(f"获取帖子详情出错: {e}", file=sys.stderr)
        return None
    
    def _parse_post_detail(self, html: str) -> Optional[Dict]:
        """解析帖子详情页面"""
        soup = BeautifulSoup(html, 'lxml')
        
        # 提取标题
        title_elem = soup.find('title')
        title = title_elem.get_text(strip=True) if title_elem else ''
        
        # 提取内容
        content_elem = soup.find('div', class_=re.compile(r'.*content.*|.*post.*'))
        content = content_elem.get_text(strip=True)[:500] if content_elem else ''
        
        # 提取时间
        time_elem = soup.find(class_=re.compile(r('.*time.*|.*date.*')))
        publish_time = time_elem.get_text(strip=True) if time_elem else ''
        
        return {
            'title': title,
            'content': content,
            'publish_time': publish_time,
        }
    
    def format_results(self, results: List[Dict]) -> str:
        """格式化搜索结果"""
        if not results:
            return "未找到相关招聘信息。"
        
        output = []
        output.append(f"找到 {len(results)} 条相关招聘信息：\n")
        
        for i, result in enumerate(results, 1):
            output.append(f"{i}. {result['title']}")
            if result.get('publish_time'):
                output.append(f"   发布时间：{result['publish_time']}")
            output.append(f"   链接：{result['url']}")
            if result.get('summary'):
                output.append(f"   摘要：{result['summary'][:150]}...")
            output.append("")
        
        return "\n".join(output)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='水木社区Job板块搜索工具')
    parser.add_argument('keyword', help='搜索关键字')
    parser.add_argument('--max-pages', type=int, default=3, help='最大搜索页数 (默认: 3)')
    parser.add_argument('--json', action='store_true', help='以JSON格式输出')
    parser.add_argument('--detail', type=str, help='获取指定帖子URL的详情')
    
    args = parser.parse_args()
    
    searcher = NewsmthJobSearcher()
    
    if args.detail:
        # 获取帖子详情
        detail = searcher.get_post_detail(args.detail)
        if detail:
            if args.json:
                print(json.dumps(detail, ensure_ascii=False, indent=2))
            else:
                print(f"标题：{detail['title']}")
                print(f"发布时间：{detail['publish_time']}")
                print(f"\n内容：\n{detail['content']}")
        else:
            print("无法获取帖子详情", file=sys.stderr)
            sys.exit(1)
    else:
        # 搜索帖子
        results = searcher.search_by_keyword(args.keyword, args.max_pages)
        
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(searcher.format_results(results))


if __name__ == '__main__':
    main()

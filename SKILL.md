---
name: newsmth-job-search
description: Search job postings on newsmth.net (水木社区) Job board by keyword. Returns job titles, links, publish times, and summaries.
---

# 水木社区职场招聘搜索

This skill searches the Job board on 水木社区 (newsmth.net) for job postings matching a keyword.

## When to Use

- User wants to search for job postings on 水木社区
- User mentions newsmth, 水木社区, 水木, or Job board
- User wants to find recruitment information in Chinese tech community

## Prerequisites

Install Python dependencies before first use:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Search

```bash
python search_newsmth.py "关键字"
```

Example:
```bash
python search_newsmth.py "Python开发"
```

### Search with More Pages

```bash
python search_newsmth.py "Java" --max-pages 5
```

### JSON Output

```bash
python search_newsmth.py "前端" --json
```

### Get Post Detail

```bash
python search_newsmth.py "" --detail "https://www.newsmth.net/nForum/article/Job/123456"
```

## Output Format

Default output:
```
找到 5 条相关招聘信息：

1. Python开发工程师 - 某互联网公司
   发布时间：2024-01-15
   链接：https://www.newsmth.net/nForum/article/Job/123456
   摘要：本公司招聘Python开发工程师，要求...

2. ...
```

JSON output:
```json
[
  {
    "title": "Python开发工程师",
    "url": "https://www.newsmth.net/nForum/article/Job/123456",
    "post_id": "123456",
    "board": "Job",
    "summary": "本公司招聘...",
    "publish_time": "2024-01-15"
  }
]
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| keyword | Search keyword (required) | - |
| --max-pages | Maximum pages to search | 3 |
| --json | Output in JSON format | false |
| --detail | Get detail of a specific post URL | - |

## Notes

- Searches only the main Job board (Job)
- Results include title, link, publish time, and summary
- Be respectful to the server (1 second delay between page requests)
- Requires internet connection to access newsmth.net

---
name: newsmth-career-search
description: Search job postings on newsmth.net Career_Upgrade board and fetch latest workplace news from WorkingLife board. Supports keyword search, post reading, and news summarization.
---

# 水木社区职场搜索

This skill searches 水木社区 (newsmth.net) for:
1. **Job postings** in Career_Upgrade board by keyword
2. **Workplace news** from WorkingLife board with summarization

## When to Use

- User wants to search for job postings on 水木社区 Career_Upgrade board
- User wants to get latest workplace news from WorkingLife board
- User mentions newsmth, 水木社区, 水木, Career_Upgrade, WorkingLife
- User wants to search recruitment info or summarize workplace discussions

## Prerequisites

Install Python dependencies before first use:

```bash
pip install -r requirements.txt
```

## Usage

### 搜索招聘信息 (Career_Upgrade)

Search job postings by keyword (title only):

```bash
python search_newsmth.py "Python开发" --board career
```

Search with more pages:

```bash
python search_newsmth.py "Java" --board career --max-pages 5
```

Search in post content (not just title):

```bash
python search_newsmth.py "Python" --board career --search-content --max-content-posts 10
```

JSON output:

```bash
python search_newsmth.py "前端" --board career --json
```

### 获取职场新闻 (WorkingLife)

Get latest workplace news:

```bash
python search_newsmth.py --board working --max-posts 10
```

Summarize workplace news:

```bash
python search_newsmth.py --board working --summarize
```

JSON output:

```bash
python search_newsmth.py --board working --json
```

### 获取帖子内容

Get specific post content:

```bash
python search_newsmth.py --board career --post-id 123456
```

## Output Format

### Career Search Results

```
在 Career_Upgrade 板块找到 5 条相关招聘信息：

1. Python开发工程师 - 某互联网公司
   发布时间：2024-01-15
   板块：Career_Upgrade

2. ...
```

### WorkingLife News

```
WorkingLife 板块最新 10 条职场动态：

1. 我决定存款达到100万就辞职
   发布时间：2026-05-29

2. 每天上班都很挣扎
   发布时间：2026-05-28

3. ...
```

### Summarized News

```
职场新闻总结：

1. 我决定存款达到100万就辞职
2. 每天上班都很挣扎
3. 告诉大家一个好消息，现在已经触底了
4. 所谓"中产"，只不过是幻觉罢了
5. 已经开始挣大钱了

共获取 10 条职场动态。
热门话题包括职场压力、求职面试、行业动态等。
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| keyword | Search keyword (for career board) | - |
| --board | Board to search: career or working | career |
| --max-pages | Maximum pages to search (career) | 3 |
| --max-posts | Maximum posts to fetch (working) | 10 |
| --search-content | Search in post content, not just title | false |
| --max-content-posts | Maximum posts to check content | 10 |
| --json | Output in JSON format | false |
| --summarize | Summarize workplace news | false |
| --post-id | Get specific post content | - |

## Boards

| Board | URL | Description |
|-------|-----|-------------|
| Career_Upgrade | https://www.newsmth.net/nForum/#!board/Career_Upgrade | 职场招聘板块 |
| WorkingLife | https://www.newsmth.net/nForum/#!board/WorkingLife | 职场生活板块 |

## Notes

- Career_Upgrade uses pagination: `?p=2`, `?p=3`, etc.
- WorkingLife provides latest workplace discussions
- Be respectful to the server (1 second delay between page requests)
- Requires internet connection to access newsmth.net

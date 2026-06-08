# 水木社区职场搜索 (newsmth-career-search)

一个用于搜索水木社区 (newsmth.net) 职场板块招聘信息和职场动态的 Python 工具。

## 功能

- **搜索招聘信息**：在 `Career_Upgrade` 板块按关键字搜索招聘帖（支持标题搜索和内容搜索）
- **获取职场动态**：获取 `WorkingLife` 板块最新帖子
- **帖子内容获取**：获取指定帖子的详细内容
- **新闻总结**：对职场动态进行简单总结
- **JSON 输出**：支持结构化 JSON 输出，方便二次处理

## 安装

```bash
pip install -r requirements.txt
```

依赖：
- requests >= 2.28.0
- beautifulsoup4 >= 4.12.0
- lxml >= 4.9.0

## 用法

### 搜索招聘信息

```bash
# 标题搜索（默认）
python search_newsmth.py "Python开发" --board career

# 搜索更多页数
python search_newsmth.py "Java" --board career --max-pages 5

# 搜索帖子内容（不仅标题）
python search_newsmth.py "Python" --board career --search-content --max-content-posts 10

# JSON 输出
python search_newsmth.py "前端" --board career --json
```

### 获取职场动态

```bash
# 获取最新帖子
python search_newsmth.py --board working --max-posts 10

# 总结职场新闻
python search_newsmth.py --board working --summarize

# JSON 输出
python search_newsmth.py --board working --json
```

### 获取帖子内容

```bash
python search_newsmth.py --board career --post-id 123456
```

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `keyword` | 搜索关键字（career 板块必填） | - |
| `--board` | 搜索板块：`career` 或 `working` | `career` |
| `--max-pages` | 最大搜索页数（career） | 3 |
| `--max-posts` | 最大帖子数（working） | 10 |
| `--search-content` | 搜索帖子内容（不仅标题） | false |
| `--max-content-posts` | 内容搜索时最多检查的帖子数 | 10 |
| `--json` | JSON 格式输出 | false |
| `--summarize` | 总结职场新闻 | false |
| `--post-id` | 获取指定帖子内容 | - |

## 项目结构

```
.
├── search_newsmth.py       # 主程序
├── requirements.txt        # Python 依赖
├── SKILL.md                # OpenClaw Skill 定义
├── install_skill.py        # Skill 安装脚本
├── test_mock.py            # Mock 数据测试（无需联网）
├── test_content_search.py  # 内容搜索测试
├── mock_career_upgrade.html  # 招聘板块 Mock 数据
├── mock_post_content.html    # 帖子内容 Mock 数据
└── .gitignore
```

## 测试

项目包含离线测试脚本，使用 Mock HTML 数据，无需联网即可运行：

```bash
# 测试标题搜索逻辑
python test_mock.py

# 测试内容搜索逻辑
python test_content_search.py
```

## 作为 OpenClaw Skill 使用

本项目同时是一个 OpenClaw Skill，可安装到 OpenClaw 的 skills 目录：

```bash
python install_skill.py
```

安装后可通过 OpenClaw 直接调用。

## 注意事项

- 请求之间设有 1 秒延迟，请尊重目标服务器
- 需要网络连接访问 newsmth.net
- 水木社区页面结构变化可能导致解析失效

## License

MIT

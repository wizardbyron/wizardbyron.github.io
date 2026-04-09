# 导出博客到微信公众号

## 功能说明

将 Hugo 博客的 Markdown 内容转换为微信公众号编辑器可用的格式，支持：

- 标准 Markdown 格式转换
- 代码块高亮
- 表格转换
- 图片处理
- 一键复制到剪贴板

## 使用方式

### 交互式转换（推荐）

```bash
python3 .opencode/skills/export_to_wechat/export_to_wechat.py
```

会自动列出最近的博客文章供选择。

### 转换指定文件

```bash
# 生成含样式的 HTML（浏览器预览）
python3 .opencode/skills/export_to_wechat/export_to_wechat.py content/blog/2026-04-09-启动-reset-计划/index.md

# 复制纯 HTML 到剪贴板（直接粘贴到微信）
python3 .opencode/skills/export_to_wechat/export_to_wechat.py content/blog/2026-04-09-启动-reset-计划/index.md --clipboard

# 指定作者和来源
python3 .opencode/skills/export_to_wechat/export_to_wechat.py content/blog/xxx/index.md -a "作者名" -s "https://example.com"
```

## 输出格式

### 1. 预览 HTML（含样式）

生成 `.html` 文件，可用浏览器打开预览效果：
- 完整的响应式样式
- 代码高亮
- 适合发布前检查

### 2. 纯 HTML（粘贴到微信）

复制到剪贴板的内容：
- 无 `<head>` 和 `<body>` 标签
- 微信编辑器可直接粘贴
- 需手动上传图片

## 微信公众号限制

微信编辑器有以下限制，脚本会自动处理：

| 功能 | 支持情况 | 处理方式 |
|------|----------|----------|
| 标题 | h1-h3 | 转换为对应级别 |
| 粗体/斜体 | ✅ | `<strong>`/`<em>` |
| 列表 | ✅ | `<ul>`/`<ol>` |
| 代码块 | ✅ | `<pre><code>` |
| 表格 | ✅ | `<table>` |
| 图片 | ⚠️ | 需手动上传到微信 |

### 图片处理

1. 生成 HTML 时图片会保留原路径
2. 粘贴到微信后：
   - 点击图片占位符
   - 选择「图片」→ 上传本地图片
   - 微信会自动处理

## 故障排除

### 粘贴后格式错乱

1. 使用「复制纯 HTML」模式
2. 在微信编辑器中选择「清除格式」后再粘贴
3. 或者粘贴到「代码」模式下

### 代码块显示异常

微信不完全支持代码高亮，建议：
1. 使用等宽字体
2. 减少代码块长度
3. 重要代码使用截图

### 表格显示问题

微信对复杂表格支持有限，建议：
1. 简化表格结构
2. 或将表格转为列表形式

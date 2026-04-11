---
name: export-to-wechat
description: 将 Hugo 博客的 Markdown 内容转换为微信公众号可用的 HTML 格式，使用与微信公众号一致的样式，自动在浏览器中打开预览。
---

## 功能说明

将 Hugo 博客的 Markdown 内容转换为微信公众号可用的格式，使用与微信公众号一致的样式。

## 使用方式

### 交互式选择（推荐）

```bash
python3 .opencode/skills/export-to-wechat/export_to_wechat.py
```

### 命令行指定文件

```bash
python3 .opencode/skills/export-to-wechat/export_to_wechat.py content/blog/xxx/index.md

# 不自动打开浏览器
python3 .opencode/skills/export-to-wechat/export_to_wechat.py file.md --no-open

# 指定作者和来源
python3 .opencode/skills/export-to-wechat/export_to_wechat.py file.md -a "作者" -s "https://example.com"
```

## 发布步骤

1. **运行脚本** - 自动在浏览器中打开预览
2. **全选内容** - 在浏览器中按 `Cmd+A` (Mac) 或 `Ctrl+A` (Windows)
3. **复制内容** - 按 `Cmd+C` 或 `Ctrl+C`
4. **粘贴到微信** - 打开微信公众号后台，按 `Cmd+V` 或 `Ctrl+V` 粘贴
5. **上传图片** - 手动上传文章中的图片

## 样式说明

导出的 HTML 使用与微信公众号一致的样式：

- **字体**：苹方 / 微软雅黑 / Helvetica
- **正文颜色**：#595959 (深灰色)
- **行高**：1.8em
- **标题**：带底部边框分隔
- **强调**：青色 (#47acaf) 斜体
- **代码**：浅灰背景 + 红色文字

## 格式支持情况

| 功能 | 支持 | 说明 |
|------|------|------|
| 标题 (h1-h3) | ✅ | 带边框分隔 |
| 粗体 | ✅ | 青色强调 |
| 斜体 | ✅ | 青色斜体 |
| 无序列表 | ✅ | 标准圆点 |
| 有序列表 | ✅ | 1. 2. 3. |
| 代码块 | ✅ | 等宽字体 + 浅灰背景 |
| 行内代码 | ✅ | 红色高亮 |
| 表格 | ✅ | 斑马纹样式 |
| 图片 | ⚠️ | 需手动上传 |
| 链接 | ✅ | 蓝色可点击 |

## 图片处理

微信编辑器不支持 HTML 图片直接显示：

1. 复制内容后，图片位置会显示为占位符
2. 点击占位符 → 选择「图片」→ 上传本地图片
3. 建议提前准备好所有图片

## 故障排除

### 粘贴后格式丢失

确保在浏览器中：
1. 全选 (Cmd+A) 选中所有内容
2. 确认选中了包括"使用说明"以上的所有内容
3. 复制 (Cmd+C) 后再粘贴

### 微信编辑器格式错乱

1. 在微信编辑器中点击「清除格式」
2. 重新粘贴内容
3. 使用编辑器的格式化工具调整

### 代码块显示异常

微信不完全支持代码高亮：
1. 代码块会显示为等宽字体 + 浅灰背景
2. 建议复杂代码使用截图

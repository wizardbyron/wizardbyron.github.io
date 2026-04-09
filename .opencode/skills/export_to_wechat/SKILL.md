# 导出博客到微信公众号

## 功能说明

将 Hugo 博客的 Markdown 内容转换为微信公众号可用的格式，生成带完整样式的 HTML 预览文件。

## 使用方式

### 交互式选择（推荐）

```bash
python3 .opencode/skills/export_to_wechat/export_to_wechat.py
```

### 命令行指定文件

```bash
python3 .opencode/skills/export_to_wechat/export_to_wechat.py content/blog/xxx/index.md

# 不自动打开浏览器
python3 .opencode/skills/export_to_wechat/export_to_wechat.py file.md --no-open

# 指定作者和来源
python3 .opencode/skills/export_to_wechat/export_to_wechat.py file.md -a "作者" -s "https://example.com"
```

## 发布步骤（浏览器复制法）

这是最可靠的方式，格式保留最完整：

1. **运行脚本** - 自动在浏览器中打开预览
2. **全选内容** - 在浏览器中按 `Cmd+A`
3. **复制内容** - 按 `Cmd+C`
4. **粘贴到微信** - 打开微信公众号后台，按 `Cmd+V` 粘贴
5. **上传图片** - 手动上传文章中的图片

## 生成的文件

脚本会生成一个 HTML 预览文件，例如：
```
content/blog/xxx/index_wechat_preview.html
```

文件包含：
- 完整的微信样式（字体、行高、颜色等）
- 标题居中显示
- 使用说明提示

## 格式支持情况

| 功能 | 支持 | 说明 |
|------|------|------|
| 标题 (h1-h3) | ✅ | 自动转换 |
| 粗体/斜体 | ✅ | 格式保留 |
| 无序列表 | ✅ | • 符号 |
| 有序列表 | ✅ | 1. 2. 3. |
| 代码块 | ✅ | 等宽字体 |
| 表格 | ✅ | 简单表格效果最好 |
| 图片 | ⚠️ | 需手动上传 |
| 链接 | ✅ | 可点击 |

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
1. 代码块会显示为等宽字体
2. 建议复杂代码使用截图
3. 或使用引用格式展示

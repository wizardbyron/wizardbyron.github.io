# 导出备忘录到博客

## 功能说明

将苹果备忘录（Notes.app）中「草稿」文件夹的内容导出为 Hugo 博客格式，生成符合本博客规范的 Markdown 文件。

**原理**：通过 AppleScript 访问备忘录应用获取解密后的内容，无需直接读取加密的 SQLite 数据库。

## 使用方式

在 OpenCode 中执行：

```
python3 .opencode/skills/export_notes_to_blog/export_notes.py
```

或在 OpenCode 对话中直接说：
> "导出备忘录到博客"

## 常用命令

```bash
# 交互式导出（推荐）
python3 .opencode/skills/export_notes_to_blog/export_notes.py

# 仅列出备忘录，不导出
python3 .opencode/skills/export_notes_to_blog/export_notes.py --list

# 预览模式
python3 .opencode/skills/export_notes_to_blog/export_notes.py --dry-run
```

## 导出流程

脚本会执行以下操作：

1. **连接备忘录** - 通过 AppleScript 访问 Notes.app
2. **筛选内容** - 查找「草稿」文件夹中的所有备忘录
3. **显示列表** - 列出所有可导出的备忘录
4. **选择导出** - 可选择导出全部或指定序号
5. **格式转换** - 纯文本 → 基本 Markdown
6. **生成文件** - 按 `content/blog/YYYY-MM-DD-title/index.md` 结构创建文件

## 输出格式

每篇导出的备忘录会生成：

```
content/blog/2026-04-09-备忘录标题/
└── index.md          # 博客正文（带 frontmatter）
```

### Frontmatter 格式

```yaml
---
title: "备忘录原始标题"
date: 2026-04-09
draft: false
tags:
- 
---
```

## 注意事项

1. **日期**：统一使用导出日期，而非备忘录创建日期
2. **标签**：导出的文章标签为空，需手动添加
3. **图片**：当前版本暂不支持图片导出（AppleScript 限制）
4. **格式**：纯文本转换，可能需要手动调整格式

## 故障排除

### 无法访问备忘录
```
❌ AppleScript 执行失败
```
→ 确保在 macOS 上运行，且备忘录应用正常

### 找不到备忘录
```
⚠️ 未找到备忘录
```
→ 检查备忘录中确实存在名为"草稿"的文件夹

### 权限问题
备忘录应用需要辅助功能权限：
1. 打开 **系统设置** → **隐私与安全性** → **隐私**
2. 找到 **辅助功能**
3. 确保您的终端应用已添加并启用

## 技术细节

- **访问方式**：AppleScript（osascript）
- **内容获取**：Notes.app body 属性（解密后内容）
- **格式转换**：内置纯文本 → Markdown 转换器
- **无需额外依赖**：仅使用 Python 标准库

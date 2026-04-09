# 从备忘录导入 (import_from_notes)

## 功能说明

从苹果备忘录（Notes.app）的「草稿」文件夹导入内容，自动转换为 Hugo 博客格式的 Markdown 文件。

## 前置要求

### macOS 环境

确保在 macOS 上运行，并授予终端访问备忘录的权限（如有提示）。

## 使用方式

### 交互式导入（推荐）

```bash
python3 .opencode/skills/import_from_notes/import_from_notes.py
```

### 命令行导入

```bash
# 列出备忘录
python3 .opencode/skills/import_from_notes/import_from_notes.py --list

# 导入第1篇
python3 .opencode/skills/import_from_notes/import_from_notes.py --import 1

# 导入全部
python3 .opencode/skills/import_from_notes/import_from_notes.py
# 输入 'a'
```

## 导入流程

1. **连接备忘录** - 通过 AppleScript 访问 Notes.app
2. **筛选内容** - 查找「草稿」文件夹中的所有备忘录
3. **显示列表** - 列出所有可导入的备忘录
4. **选择导入** - 可选择导入全部或指定序号
5. **格式转换** - HTML → Markdown
6. **生成文件** - 按 `content/blog/YYYY-MM-DD-title/index.md` 结构创建文件

## 输出格式

每篇导入的备忘录会生成：

```
content/blog/YYYY-MM-DD-标题/index.md
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

## 支持的格式

- 标题 (h1, h2)
- 无序列表 (-)
- 有序列表 (1. 2. 3.)
- 表格
- 粗体、斜体
- 链接

## 注意事项

1. **文件夹名称**：必须存在名为「草稿」的备忘录文件夹
2. **日期**：统一使用导入日期
3. **标签**：导入的文章标签为空，需手动添加
4. **图片**：当前版本暂不支持图片导出

## 故障排除

### 无法访问备忘录

确保在 macOS 上运行，且备忘录应用正常工作。

### 找不到备忘录

检查备忘录中确实存在名为"草稿"的文件夹，且文件夹中有备忘录。

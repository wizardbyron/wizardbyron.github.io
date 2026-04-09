# 导出博客到微信公众号

## 功能说明

将 Hugo 博客的 Markdown 内容转换为微信公众号可用的格式，支持：

- 标准 Markdown 格式转换
- 代码块高亮
- 表格转换
- 多种复制模式

## 使用方式

### 交互式转换（推荐）

```bash
python3 .opencode/skills/export_to_wechat/export_to_wechat.py
```

### 命令行转换

```bash
# 复制富文本到剪贴板（推荐）- 直接粘贴到微信编辑器
python3 .opencode/skills/export_to_wechat/export_to_wechat.py content/blog/xxx/index.md -r

# 复制 HTML 到剪贴板 - 在微信代码模式粘贴
python3 .opencode/skills/export_to_wechat/export_to_wechat.py content/blog/xxx/index.md -c

# 生成预览 HTML 文件
python3 .opencode/skills/export_to_wechat/export_to_wechat.py content/blog/xxx/index.md -p

# 指定作者和来源
python3 .opencode/skills/export_to_wechat/export_to_wechat.py file.md -a "作者" -s "https://example.com"
```

## 复制模式说明

| 模式 | 命令 | 使用方法 | 优缺点 |
|------|------|----------|--------|
| **富文本** | `-r` | 直接 Ctrl+V 粘贴 | ✅ 最方便，可能丢失部分格式 |
| **HTML** | `-c` | 微信编辑器 → 代码模式 → Ctrl+V | ✅ 格式完整，需切换模式 |
| **预览文件** | `-p` | 浏览器打开预览 | ✅ 可检查效果，适合发布前 |
| **纯文本** | `-t` | 粘贴后手动格式化 | 格式丢失最少 |

## 微信公众号使用步骤

### 方式一：富文本模式（推荐）

1. 运行 `python3 export_to_wechat.py file.md -r`
2. 打开微信公众号后台
3. 在编辑器中直接 **Ctrl+V** 粘贴
4. 手动上传图片

### 方式二：HTML 模式

1. 运行 `python3 export_to_wechat.py file.md -c`
2. 打开微信公众号后台
3. 点击编辑器右上角 **「< >」代码图标**
4. **Ctrl+V** 粘贴 HTML 代码
5. 点击确定，自动转换为富文本

## 格式支持情况

| 功能 | 支持 | 说明 |
|------|------|------|
| 标题 (h1-h3) | ✅ | 自动转换 |
| 粗体/斜体 | ✅ | 使用 Ctrl+B/I |
| 无序列表 | ✅ | • 符号 |
| 有序列表 | ✅ | 1. 2. 3. |
| 代码块 | ✅ | 等宽字体显示 |
| 表格 | ✅ | 简单表格效果最好 |
| 图片 | ⚠️ | 需手动上传 |
| 链接 | ✅ | 可点击 |

## 图片处理

微信编辑器不支持 HTML 中的图片直接显示：

1. 复制内容后，图片位置会显示为占位符
2. 点击占位符，选择「图片」→ 上传本地图片
3. 建议提前准备好图片，或使用微信图床

## 故障排除

### 粘贴后格式错乱

1. 使用 **HTML 模式**（`-c`）
2. 在微信代码模式下粘贴
3. 或粘贴后点击「清除格式」再重新格式化

### 代码块显示异常

微信不完全支持代码高亮：
1. 代码块会显示为等宽字体
2. 建议使用截图展示复杂代码
3. 或使用代码块引用格式

### 表格显示问题

微信对复杂表格支持有限：
1. 简化表格结构（少于 4 列）
2. 或将表格转为列表形式

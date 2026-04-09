#!/usr/bin/env python3
"""
Markdown to WeChat Article Converter
将 Markdown 博客内容转换为微信公众号可用的格式
"""

import os
import sys
import re
import argparse
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime

# 尝试导入 markdown 库，如果没有则使用正则表达式
try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

TEMPLATE_DIR = Path(__file__).parent


def copy_html_as_rtf_to_clipboard(html_content):
    """将 HTML 内容复制到剪贴板（微信编辑器粘贴方式）"""
    # 生成带样式的 HTML
    styled_html = f'''<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; font-size: 16px; line-height: 1.8; padding: 20px; max-width: 100%; word-wrap: break-word;">
{html_content}
</div>'''
    
    try:
        # 使用 pbcopy 复制
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(input=styled_html.encode('utf-8'))
        return True
    except Exception as e:
        print(f"⚠️ 复制失败: {e}")
        return False


def generate_rtf_from_html(html_content):
    """将 HTML 转换为 RTF 格式"""
    # 简单的 RTF 生成器
    rtf_lines = []
    rtf_lines.append(r'{\rtf1\ansi\deff0')
    rtf_lines.append(r'{\fonttbl{\f0 Helvetica;}}')
    rtf_lines.append(r'\f0\fs24')
    
    lines = html_content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            rtf_lines.append(r'\par')
            continue
        
        # 处理标签
        if line.startswith('<h1'):
            content = extract_tag_content(line, 'h1')
            rtf_lines.append(r'\fs36\b ' + escape_rtf(content) + r'\b0\par')
        elif line.startswith('<h2'):
            content = extract_tag_content(line, 'h2')
            rtf_lines.append(r'\fs28\b ' + escape_rtf(content) + r'\b0\par')
        elif line.startswith('<h3'):
            content = extract_tag_content(line, 'h3')
            rtf_lines.append(r'\fs24\b ' + escape_rtf(content) + r'\b0\par')
        elif line.startswith('<p>'):
            content = extract_tag_content(line, 'p')
            content = process_inline_tags(content)
            rtf_lines.append(escape_rtf(content) + r'\par')
        elif line.startswith('<li>'):
            content = extract_tag_content(line, 'li')
            content = process_inline_tags(content)
            rtf_lines.append(r'\bullet ' + escape_rtf(content) + r'\par')
        elif line.startswith('<ol'):
            continue  # 列表开始
        elif line.startswith('</ol'):
            continue  # 列表结束
        elif line.startswith('<pre>'):
            content = extract_tag_content(line, 'pre')
            rtf_lines.append(r'{\f1\fs20 ' + escape_rtf(content) + r'}\par')
        else:
            # 处理剩余的 HTML 标签
            content = re.sub(r'<[^>]+>', '', line)
            if content.strip():
                rtf_lines.append(escape_rtf(content) + r'\par')
    
    rtf_lines.append('}')
    return '\n'.join(rtf_lines)


def extract_tag_content(text, tag):
    """提取 HTML 标签内容"""
    pattern = f'<{tag}[^>]*>(.*?)</{tag}>'
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1) if match else text


def process_inline_tags(text):
    """处理行内标签"""
    # 移除所有行内标签但保留内容
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<strong>(.*?)</strong>', r'\1', text)
    text = re.sub(r'<b>(.*?)</b>', r'\1', text)
    text = re.sub(r'<em>(.*?)</em>', r'\1', text)
    text = re.sub(r'<i>(.*?)</i>', r'\1', text)
    text = re.sub(r'<code>(.*?)</code>', r'\1', text)
    text = re.sub(r'<[^>]+>', '', text)
    return text


def escape_rtf(text):
    """转义 RTF 特殊字符"""
    text = text.replace('\\', '\\\\')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    text = text.replace('\n', r'\par ')
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    return text


def copy_html_to_clipboard(html_content):
    """复制 HTML 到剪贴板（微信编辑器粘贴）"""
    # 使用 pbcopy 复制纯 HTML
    try:
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(input=html_content.encode('utf-8'))
        return True
    except Exception as e:
        print(f"⚠️ 复制失败: {e}")
        return False


def copy_plain_text_to_clipboard(markdown_text):
    """复制为纯文本（微信编辑器可接受的格式）"""
    # 转换 Markdown 到纯文本（保留基本格式）
    plain_lines = []
    lines = markdown_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            plain_lines.append('')
            continue
        
        # 标题转换
        if line.startswith('# '):
            plain_lines.append(line[2:])
            plain_lines.append('=' * len(line[2:]))
        elif line.startswith('## '):
            plain_lines.append(line[3:])
            plain_lines.append('-' * len(line[3:]))
        elif line.startswith('### '):
            plain_lines.append(line[4:])
        # 列表
        elif line.startswith('- ') or line.startswith('* '):
            plain_lines.append('• ' + line[2:])
        elif re.match(r'^\d+\.\s', line):
            plain_lines.append(line)
        # 代码
        elif line.startswith('```'):
            continue
        else:
            # 移除 Markdown 格式
            line = re.sub(r'\*\*(.+?)\*\*', r'\1', line)
            line = re.sub(r'\*(.+?)\*', r'\1', line)
            line = re.sub(r'`(.+?)`', r'\1', line)
            plain_lines.append(line)
    
    plain_text = '\n'.join(plain_lines)
    
    try:
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(input=plain_text.encode('utf-8'))
        return True
    except Exception as e:
        print(f"⚠️ 复制失败: {e}")
        return False


def markdown_to_html(markdown_text):
    """将 Markdown 转换为 HTML"""
    if not markdown_text:
        return ""
    
    # 尝试使用 markdown 库
    if HAS_MARKDOWN:
        md = markdown.Markdown(extensions=[
            'tables',
            'fenced_code',
            'codehilite',
            'nl2br',
            'sane_lists'
        ])
        html = md.convert(markdown_text)
        return html
    
    # 降级：使用正则表达式转换
    return regex_markdown_to_html(markdown_text)


def regex_markdown_to_html(text):
    """使用正则表达式将 Markdown 转换为 HTML"""
    lines = text.split('\n')
    html_parts = []
    in_code_block = False
    in_list = False
    in_ordered_list = False
    
    for line in lines:
        # 代码块
        if line.strip().startswith('```'):
            if not in_code_block:
                html_parts.append('<pre><code>')
                in_code_block = True
            else:
                html_parts.append('</code></pre>')
                in_code_block = False
            continue
        
        if in_code_block:
            html_parts.append(line.replace('<', '&lt;').replace('>', '&gt;'))
            continue
        
        # 标题
        if line.startswith('# '):
            html_parts.append(f'<h2>{escape_html(line[2:])}</h2>')
            continue
        elif line.startswith('## '):
            html_parts.append(f'<h3>{escape_html(line[3:])}</h3>')
            continue
        elif line.startswith('### '):
            html_parts.append(f'<h4>{escape_html(line[4:])}</h4>')
            continue
        
        # 无序列表
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            if not in_list:
                html_parts.append('<ul>')
                in_list = True
            content = line.strip()[2:]
            html_parts.append(f'<li>{process_inline(content)}</li>')
            continue
        elif line.strip() and line.strip()[0].isdigit() and '. ' in line:
            if not in_ordered_list:
                html_parts.append('<ol>')
                in_ordered_list = True
            content = re.sub(r'^\d+\.\s*', '', line.strip())
            html_parts.append(f'<li>{process_inline(content)}</li>')
            continue
        
        # 关闭列表
        if in_list:
            html_parts.append('</ul>')
            in_list = False
        if in_ordered_list:
            html_parts.append('</ol>')
            in_ordered_list = False
        
        # 引用
        if line.startswith('>'):
            html_parts.append(f'<blockquote>{escape_html(line[1:].strip())}</blockquote>')
            continue
        
        # 分隔线
        if line.strip() in ['---', '***', '___']:
            html_parts.append('<hr/>')
            continue
        
        # 空行
        if not line.strip():
            continue
        
        # 段落
        html_parts.append(f'<p>{process_inline(line)}</p>')
    
    # 关闭未关闭的标签
    if in_list:
        html_parts.append('</ul>')
    if in_ordered_list:
        html_parts.append('</ol>')
    
    return '\n'.join(html_parts)


def escape_html(text):
    """转义 HTML 特殊字符"""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    return text


def process_inline(text):
    """处理行内格式"""
    # 粗体 **text**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # 斜体 *text* 或 _text_
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
    # 行内代码 `code`
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    # 图片 ![alt](url)
    text = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', r'<img src="\2" alt="\1" style="max-width:100%;"/>', text)
    # 链接 [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
    return text


def generate_wechat_html(title, html_content, author="", source_url=""):
    """生成微信公众号可用的 HTML"""
    
    # 如果有 markdown 库，使用更好的转换
    if HAS_MARKDOWN:
        from markdown.extensions.tables import TableExtension
        from markdown.extensions.fenced_code import FencedCodeExtension
        
        md = markdown.Markdown(extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.nl2br',
        ])
        
        # 处理表格
        html_content = md.convert(html_content)
    
    wechat_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{escape_html(title)}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Symbol";
            font-size: 16px;
            line-height: 1.8;
            color: #333;
            padding: 20px;
            max-width: 100%;
            word-wrap: break-word;
        }}
        h1 {{ font-size: 1.5em; text-align: center; margin-bottom: 1em; }}
        h2 {{ font-size: 1.3em; margin-top: 1.5em; border-bottom: 1px solid #eee; padding-bottom: 0.3em; }}
        h3 {{ font-size: 1.1em; margin-top: 1.2em; }}
        h4 {{ font-size: 1em; margin-top: 1em; }}
        p {{ margin: 1em 0; text-align: justify; }}
        img {{ max-width: 100%; height: auto; display: block; margin: 1em auto; }}
        pre {{ 
            background-color: #f6f8fa; 
            padding: 16px; 
            overflow-x: auto; 
            border-radius: 6px;
            font-size: 14px;
            line-height: 1.45;
        }}
        code {{
            background-color: #f6f8fa;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: "SF Mono", Consolas, Monaco, monospace;
            font-size: 0.9em;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            margin: 1em 0;
            padding-left: 1em;
            color: #666;
        }}
        ul, ol {{
            padding-left: 1.5em;
            margin: 1em 0;
        }}
        li {{ margin: 0.5em 0; }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{ background-color: #f6f8fa; }}
        a {{ color: #576b95; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        hr {{
            border: none;
            border-top: 1px solid #eee;
            margin: 2em 0;
        }}
        .meta {{
            text-align: center;
            color: #999;
            font-size: 0.9em;
            margin-bottom: 2em;
            padding-bottom: 1em;
            border-bottom: 1px solid #eee;
        }}
    </style>
</head>
<body>
    <h1>{escape_html(title)}</h1>
    <div class="meta">
        {f'作者：{escape_html(author)}' if author else ''}
        {f'｜ 来源：<a href="{escape_html(source_url)}">{escape_html(source_url)}</a>' if source_url else ''}
    </div>
    {html_content}
</body>
</html>'''
    
    return wechat_html


def read_blog_file(file_path):
    """读取博客文件并提取标题和内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 frontmatter
    frontmatter = {}
    body_content = content
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body_content = parts[2].strip()
            
            # 解析 frontmatter
            for line in fm_text.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip().strip('"').strip("'")
    
    return frontmatter, body_content.strip()


def convert_blog_to_wechat(blog_path, output_path=None, author="", source_url=""):
    """转换博客为微信格式"""
    
    if not os.path.exists(blog_path):
        print(f"❌ 文件不存在: {blog_path}")
        return False
    
    # 读取博客
    frontmatter, body = read_blog_file(blog_path)
    
    title = frontmatter.get('title', '无标题')
    if not author:
        author = frontmatter.get('author', '')
    if not source_url:
        source_url = frontmatter.get('url', '')
    
    # 转换 Markdown 到 HTML
    html_content = markdown_to_html(body)
    
    # 生成微信 HTML
    wechat_html = generate_wechat_html(title, html_content, author, source_url)
    
    # 保存
    if not output_path:
        output_path = blog_path.replace('.md', '_wechat.html')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(wechat_html)
    
    print(f"✅ 转换完成: {output_path}")
    return True


def copy_to_clipboard(text):
    """复制文本到剪贴板"""
    try:
        subprocess.run(['pbcopy'], input=text.encode('utf-8'), check=True)
        return True
    except Exception as e:
        print(f"⚠️ 复制到剪贴板失败: {e}")
        return False


def convert_blog_to_plain_html(blog_path, copy=True, mode='html'):
    """转换博客为纯 HTML（不含样式，用于直接粘贴到微信）"""
    
    if not os.path.exists(blog_path):
        print(f"❌ 文件不存在: {blog_path}")
        return None
    
    # 读取博客
    frontmatter, body = read_blog_file(blog_path)
    title = frontmatter.get('title', '无标题')
    
    # 转换
    html_content = markdown_to_html(body)
    
    # 生成纯 HTML（无 head 和 body）
    plain_html = f'''<h1 style="text-align:center;">{escape_html(title)}</h1>
{html_content}'''
    
    if copy:
        if mode == 'html':
            if copy_to_clipboard(plain_html):
                print("✅ HTML 内容已复制到剪贴板")
                print("   微信编辑器：使用 Ctrl+V 粘贴，或在代码模式下粘贴")
        elif mode == 'rtf':
            if copy_html_as_rtf_to_clipboard(plain_html):
                print("✅ 富文本内容已复制到剪贴板")
                print("   微信编辑器：直接 Ctrl+V 粘贴（推荐）")
        elif mode == 'text':
            if copy_plain_text_to_clipboard(body):
                print("✅ 纯文本内容已复制到剪贴板")
                print("   微信编辑器：粘贴后使用编辑器格式化")
    
    return plain_html


def convert_blog_to_rtf(blog_path, copy=True):
    """转换博客为 RTF 格式（支持富文本粘贴到微信）"""
    
    if not os.path.exists(blog_path):
        print(f"❌ 文件不存在: {blog_path}")
        return None
    
    # 读取博客
    frontmatter, body = read_blog_file(blog_path)
    title = frontmatter.get('title', '无标题')
    
    # 转换为 HTML
    html_content = markdown_to_html(body)
    
    # 添加标题
    full_html = f'<h1>{escape_html(title)}</h1>\n{html_content}'
    
    if copy:
        if copy_html_as_rtf_to_clipboard(full_html):
            print("✅ 富文本内容已复制到剪贴板")
            print("   可以直接粘贴到微信公众号编辑器（保留格式）")
    
    return full_html


def interactive_convert():
    """交互式转换"""
    print("📝 Markdown to WeChat Converter")
    print("=" * 50)
    
    # 查找博客文件
    blog_dir = Path("content/blog")
    if not blog_dir.exists():
        print("❌ 找不到 content/blog 目录")
        return
    
    # 获取最新的博客
    blog_files = sorted(blog_dir.glob("*/index.md"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    if not blog_files:
        print("❌ 没有找到博客文章")
        return
    
    print(f"\n找到 {len(blog_files)} 篇博客:\n")
    for i, f in enumerate(blog_files[:10], 1):
        frontmatter, _ = read_blog_file(f)
        title = frontmatter.get('title', f.parent.name)
        date = frontmatter.get('date', '')
        print(f"  {i}. [{date}] {title}")
    
    print(f"\n请输入要转换的文章序号 (1-{min(10, len(blog_files))}) [默认 1]:")
    choice = input().strip() or "1"
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(blog_files):
            blog_path = str(blog_files[idx])
        else:
            print("❌ 无效的选择")
            return
    except ValueError:
        print("❌ 请输入有效数字")
        return
    
    print("\n选择输出格式:")
    print("  1. HTML 文件（含样式，可浏览器预览）")
    print("  2. 纯 HTML（保存到文件）")
    print("  3. 复制到剪贴板 - HTML（微信代码模式粘贴）")
    print("  4. 复制到剪贴板 - RTF（微信直接粘贴，保留格式）")
    print("  5. 复制到剪贴板 - 纯文本")
    
    format_choice = input("\n请输入选择 (1-5) [默认 4]: ").strip() or "4"
    
    if format_choice == "1":
        output_path = blog_path.replace('.md', '_wechat.html')
        author = input("作者 (可选): ").strip()
        source = input("来源 URL (可选): ").strip()
        convert_blog_to_wechat(blog_path, output_path, author, source)
    elif format_choice == "2":
        plain_html = convert_blog_to_plain_html(blog_path, copy=False)
        output_path = blog_path.replace('.md', '_plain.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(plain_html)
        print(f"✅ 已保存到: {output_path}")
    elif format_choice == "3":
        convert_blog_to_plain_html(blog_path, copy=True, mode='html')
    elif format_choice == "4":
        convert_blog_to_plain_html(blog_path, copy=True, mode='rtf')
    else:
        convert_blog_to_plain_html(blog_path, copy=True, mode='text')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="将 Markdown 博客转换为微信公众号可用的格式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 export_to_wechat.py                                    # 交互式转换
  python3 export_to_wechat.py content/blog/xxx/index.md         # 生成预览 HTML
  python3 export_to_wechat.py file.md -c                         # 复制 HTML 到剪贴板
  python3 export_to_wechat.py file.md -r                         # 复制 RTF（富文本）到剪贴板
  python3 export_to_wechat.py file.md -t                         # 复制纯文本到剪贴板
        """
    )
    parser.add_argument('file', nargs='?', help='博客文件路径')
    parser.add_argument('--clipboard', '-c', action='store_true', help='复制 HTML 到剪贴板（微信代码模式）')
    parser.add_argument('--rtf', '-r', action='store_true', help='复制 RTF 富文本到剪贴板（微信直接粘贴，推荐）')
    parser.add_argument('--text', '-t', action='store_true', help='复制纯文本到剪贴板')
    parser.add_argument('--preview', '-p', action='store_true', help='生成预览 HTML 文件')
    parser.add_argument('--author', '-a', default='', help='作者名')
    parser.add_argument('--source', '-s', default='', help='来源 URL')
    
    args = parser.parse_args()
    
    if args.file:
        if args.rtf:
            convert_blog_to_plain_html(args.file, copy=True, mode='rtf')
        elif args.text:
            convert_blog_to_plain_html(args.file, copy=True, mode='text')
        elif args.clipboard:
            convert_blog_to_plain_html(args.file, copy=True, mode='html')
        elif args.preview:
            convert_blog_to_wechat(args.file, author=args.author, source_url=args.source)
        else:
            # 默认生成预览
            convert_blog_to_wechat(args.file, author=args.author, source_url=args.source)
    else:
        interactive_convert()

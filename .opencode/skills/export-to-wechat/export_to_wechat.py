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
from pathlib import Path
from datetime import datetime

TEMPLATE_DIR = Path(__file__).parent


def markdown_to_html(markdown_text):
    """将 Markdown 转换为 HTML"""
    if not markdown_text:
        return ""
    
    lines = markdown_text.split('\n')
    html_parts = []
    in_code_block = False
    in_list = False
    in_ordered_list = False
    in_table = False
    table_rows = []
    
    def process_table_row(row, is_header=False):
        """处理表格行"""
        cells = []
        # 分割单元格，处理 | | 的情况
        parts = row.strip().strip('|').split('|')
        for cell in parts:
            cell = cell.strip()
            if cell:  # 跳过空单元格
                if is_header:
                    cells.append(f'<th>{process_inline(cell)}</th>')
                else:
                    cells.append(f'<td>{process_inline(cell)}</td>')
        return cells
    
    def build_table(rows):
        """构建表格 HTML"""
        if not rows:
            return ''
        html = ['<table>']
        # 第一行是表头
        html.append('<thead><tr>')
        html.append(''.join(rows[0]))
        html.append('</tr></thead>')
        # 其余是数据行
        if len(rows) > 1:
            html.append('<tbody>')
            for row in rows[1:]:
                html.append('<tr>')
                html.append(''.join(row))
                html.append('</tr>')
            html.append('</tbody>')
        html.append('</table>')
        return ''.join(html)
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 代码块
        if line.strip().startswith('```'):
            if not in_code_block:
                # 关闭可能打开的列表
                if in_list:
                    html_parts.append('</ul>')
                    in_list = False
                if in_ordered_list:
                    html_parts.append('</ol>')
                    in_ordered_list = False
                # 关闭可能打开的表格
                if in_table:
                    html_parts.append(build_table(table_rows))
                    table_rows = []
                    in_table = False
                html_parts.append('<pre><code>')
                in_code_block = True
            else:
                html_parts.append('</code></pre>')
                in_code_block = False
            i += 1
            continue
        
        if in_code_block:
            html_parts.append(line.replace('<', '&lt;').replace('>', '&gt;'))
            i += 1
            continue
        
        # 检测表格
        if line.strip().startswith('|') and '|' in line.strip()[1:]:
            # 关闭可能打开的列表
            if in_list:
                html_parts.append('</ul>')
                in_list = False
            if in_ordered_list:
                html_parts.append('</ol>')
                in_ordered_list = False
            
            # 检查是否是分隔行 (|---|---|)
            if re.match(r'^\|[\s\-:|]+\|$', line.strip()):
                # 分隔行，跳过但标记表头结束
                i += 1
                continue
            
            # 添加行到表格
            in_table = True
            cells = process_table_row(line, is_header=(len(table_rows) == 0))
            table_rows.append(cells)
            i += 1
            continue
        
        # 处理累积的表格
        if in_table and table_rows:
            html_parts.append(build_table(table_rows))
            table_rows = []
            in_table = False
        
        # 标题
        if line.startswith('# '):
            html_parts.append(f'<h2>{escape_html(line[2:])}</h2>')
        elif line.startswith('## '):
            html_parts.append(f'<h3>{escape_html(line[3:])}</h3>')
        elif line.startswith('### '):
            html_parts.append(f'<h4>{escape_html(line[4:])}</h4>')
        # 无序列表
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            if not in_list:
                html_parts.append('<ul>')
                in_list = True
            content = line.strip()[2:]
            html_parts.append(f'<li>{process_inline(content)}</li>')
        # 有序列表
        elif line.strip() and re.match(r'^\d+\.\s', line.strip()):
            if not in_ordered_list:
                html_parts.append('<ol>')
                in_ordered_list = True
            content = re.sub(r'^\d+\.\s*', '', line.strip())
            html_parts.append(f'<li>{process_inline(content)}</li>')
        # 引用
        elif line.startswith('>'):
            html_parts.append(f'<blockquote>{escape_html(line[1:].strip())}</blockquote>')
        # 分隔线
        elif line.strip() in ['---', '***', '___']:
            html_parts.append('<hr/>')
        # 空行
        elif not line.strip():
            pass  # 忽略空行
        # 段落
        else:
            html_parts.append(f'<p>{process_inline(line)}</p>')
        
        # 关闭列表（如果下一行不是列表项）
        if in_list or in_ordered_list:
            next_i = i + 1
            next_is_list = False
            if next_i < len(lines):
                next_line = lines[next_i].strip()
                if next_line.startswith('- ') or next_line.startswith('* ') or re.match(r'^\d+\.\s', next_line):
                    next_is_list = True
            
            if not next_is_list and (in_list or in_ordered_list):
                if in_list:
                    html_parts.append('</ul>')
                    in_list = False
                if in_ordered_list:
                    html_parts.append('</ol>')
                    in_ordered_list = False
        
        i += 1
    
    # 关闭未关闭的标签
    if in_list:
        html_parts.append('</ul>')
    if in_ordered_list:
        html_parts.append('</ol>')
    if in_table and table_rows:
        html_parts.append(build_table(table_rows))
    
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
    # 粗体 - 使用微信公众号强调色
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color:#47acaf;font-weight:bold;">\1</strong>', text)
    # 斜体 - 使用微信公众号强调色
    text = re.sub(r'\*(.+?)\*', r'<em style="color:#47acaf;font-style:italic;">\1</em>', text)
    text = re.sub(r'_(.+?)_', r'<em style="color:#47acaf;font-style:italic;">\1</em>', text)
    # 行内代码
    text = re.sub(r'`(.+?)`', r'<code style="background-color:#f5f5f5;padding:2px 4px;border-radius:3px;font-family:Consolas,monospace;font-size:0.9em;">\1</code>', text)
    # 图片
    text = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', r'<img src="\2" alt="\1" style="max-width:100%;height:auto;display:block;margin:1em auto;"/>', text)
    # 链接
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" style="color:#576b95;text-decoration:none;">\1</a>', text)
    return text


def generate_preview_html(title, html_content, author="", source_url=""):
    """生成带完整样式的预览 HTML - 仿微信公众号样式"""
    
    wechat_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
    <title>{escape_html(title)}</title>
    <style>
        body {{
            font-family: "PingFang SC", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif;
            font-size: 16px;
            line-height: 1.8;
            color: #333;
            max-width: 677px;
            margin: 0 auto;
            padding: 20px;
            background: #fff;
            -webkit-text-size-adjust: 100% !important;
        }}
        h1 {{ 
            font-size: 1.5em; 
            text-align: center; 
            margin-bottom: 1em;
            font-weight: normal;
        }}
        h2 {{ 
            font-size: 1.3em; 
            margin: 30px 0 15px; 
            padding-bottom: 8px;
            border-bottom: 2px solid #595959;
            color: #595959;
            font-weight: bold;
        }}
        h3 {{ 
            font-size: 1.1em; 
            margin: 20px 0 10px;
            color: #595959;
            font-weight: bold;
        }}
        h4 {{ 
            font-size: 1em; 
            margin: 15px 0 8px;
            color: #595959;
            font-weight: bold;
        }}
        p {{ 
            color: #595959; 
            margin: 8px 0;
            text-align: justify;
            line-height: 1.8em;
            font-size: 16px;
        }}
        img {{ 
            max-width: 100%; 
            height: auto; 
            display: block; 
            margin: 1em auto;
            border-radius: 4px;
        }}
        pre {{ 
            background-color: #f8f8f8; 
            padding: 16px; 
            overflow-x: auto; 
            border-radius: 4px;
            font-size: 14px;
            line-height: 1.5em;
            margin: 1em 0;
            border: 1px solid #e0e0e0;
        }}
        code {{
            background-color: #f5f5f5;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: Consolas, Monaco, "Courier New", monospace;
            font-size: 0.9em;
            color: #c7254e;
        }}
        pre code {{ 
            background-color: transparent; 
            padding: 0; 
            border-radius: 0;
            color: #333;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            margin: 1em 0;
            padding: 8px 16px;
            background-color: #f9f9f9;
            color: #666;
        }}
        ul, ol {{ 
            padding-left: 1.5em; 
            margin: 1em 0;
            color: #595959;
        }}
        li {{ 
            margin: 0.5em 0;
            line-height: 1.8em;
        }}
        table {{ 
            border-collapse: collapse; 
            width: 100%; 
            margin: 1em 0; 
            overflow-x: auto;
            display: block;
        }}
        th, td {{ 
            border: 1px solid #ddd; 
            padding: 10px 12px; 
            text-align: left; 
            font-size: 14px;
            color: #595959;
        }}
        th {{ 
            background-color: #f8f8f8; 
            font-weight: bold;
        }}
        tr:nth-child(even) {{ background-color: #fafafa; }}
        a {{ 
            color: #576b95;
            text-decoration: none;
        }}
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
        .section-separator {{
            text-align: center;
            color: #ccc;
            margin: 2em 0;
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
    <hr/>
    <p style="text-align:center;color:#ccc;font-size:12px;">═══════════════════════════════</p>
    <p style="text-align:center;color:#999;font-size:14px;">📋 使用说明</p>
    <p style="text-align:center;color:#595959;font-size:13px;">1. 选中上方所有内容 (Cmd+A / Ctrl+A)</p>
    <p style="text-align:center;color:#595959;font-size:13px;">2. 复制 (Cmd+C / Ctrl+C)</p>
    <p style="text-align:center;color:#595959;font-size:13px;">3. 打开微信公众号后台，粘贴 (Cmd+V / Ctrl+V)</p>
</body>
</html>'''
    
    return wechat_html


def read_blog_file(file_path):
    """读取博客文件并提取标题和内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    frontmatter = {}
    body_content = content
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body_content = parts[2].strip()
            
            for line in fm_text.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip().strip('"').strip("'")
    
    return frontmatter, body_content.strip()


def open_in_browser(html_path):
    """在浏览器中打开 HTML 文件"""
    try:
        subprocess.run(['open', html_path], check=True)
        return True
    except Exception as e:
        print(f"⚠️ 无法打开浏览器: {e}")
        return False


def convert_blog_to_wechat(blog_path, output_path=None, author="", source_url="", auto_open=True):
    """转换博客为微信预览格式"""
    
    if not os.path.exists(blog_path):
        print(f"❌ 文件不存在: {blog_path}")
        return False
    
    frontmatter, body = read_blog_file(blog_path)
    
    title = frontmatter.get('title', '无标题')
    if not author:
        author = frontmatter.get('author', '')
    if not source_url:
        source_url = frontmatter.get('url', '')
    
    html_content = markdown_to_html(body)
    wechat_html = generate_preview_html(title, html_content, author, source_url)
    
    if not output_path:
        output_path = blog_path.replace('.md', '_wechat_preview.html')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(wechat_html)
    
    print(f"✅ 预览文件已生成: {output_path}")
    
    if auto_open:
        print("📖 在浏览器中打开...")
        open_in_browser(output_path)
        print("\n📋 微信公众号发布步骤:")
        print("   1. 选中浏览器中的所有内容 (Cmd+A)")
        print("   2. 复制 (Cmd+C)")
        print("   3. 打开微信公众号后台，粘贴 (Cmd+V)")
        print("   4. 手动上传图片")
    
    return True


def interactive_convert():
    """交互式转换"""
    print("📝 Markdown to WeChat Converter")
    print("=" * 50)
    
    blog_dir = Path("content/blog")
    if not blog_dir.exists():
        print("❌ 找不到 content/blog 目录")
        return
    
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
    
    print(f"\n📖 正在生成预览文件...")
    convert_blog_to_wechat(blog_path)


def skill_handler(args=None):
    """技能调用入口"""
    if args:
        file_path = args.get('file')
        if file_path:
            convert_blog_to_wechat(
                file_path,
                author=args.get('author', ''),
                source_url=args.get('source', ''),
                auto_open=not args.get('no_open', False)
            )
        else:
            interactive_convert()
    else:
        interactive_convert()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="将 Markdown 博客转换为微信公众号可用的格式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 export_to_wechat.py                          # 交互式选择
  python3 export_to_wechat.py content/blog/xxx/index.md # 生成预览并打开浏览器
  python3 export_to_wechat.py file.md --no-open        # 只生成预览文件
        """
    )
    parser.add_argument('file', nargs='?', help='博客文件路径')
    parser.add_argument('--no-open', action='store_true', help='只生成文件，不打开浏览器')
    parser.add_argument('--author', '-a', default='', help='作者名')
    parser.add_argument('--source', '-s', default='', help='来源 URL')
    
    args = parser.parse_args()
    
    if args.file:
        convert_blog_to_wechat(
            args.file, 
            author=args.author, 
            source_url=args.source,
            auto_open=not args.no_open
        )
    else:
        interactive_convert()

#!/usr/bin/env python3
"""
Import from Apple Notes
从苹果备忘录导入内容并转换为 Hugo 博客格式
"""

import os
import sys
import re
import argparse
import subprocess
from pathlib import Path
from datetime import datetime


def run_applescript(script, timeout=120):
    """运行 AppleScript 并返回结果"""
    try:
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode != 0:
            return None, result.stderr
        return result.stdout, None
    except subprocess.TimeoutExpired:
        return None, "AppleScript 执行超时"
    except FileNotFoundError:
        return None, "未找到 osascript，请确保在 macOS 上运行"
    except Exception as e:
        return None, str(e)


def get_notes_list():
    """获取备忘录列表"""
    script = '''
    tell application "Notes"
        set resultText to ""
        set counter to 0
        
        try
            set allFolders to every folder
            
            repeat with aFolder in allFolders
                if name of aFolder is "草稿" then
                    set folderNotes to every note of aFolder
                    
                    repeat with n from 1 to (count of folderNotes)
                        set aNote to item n of folderNotes
                        set counter to counter + 1
                        set noteTitle to name of aNote
                        set resultText to resultText & counter & ". " & noteTitle & return
                    end repeat
                    
                    exit repeat
                end if
            end repeat
        on error e
            return "ERROR:" & e
        end try
        
        if counter is 0 then
            return "EMPTY"
        else
            return resultText
        end if
    end tell
    '''
    
    output, error = run_applescript(script)
    if error:
        return [], error
    
    if "EMPTY" in output or not output.strip():
        return [], None
    
    return output.strip().split('\n'), None


def get_note_content(note_index):
    """获取指定备忘录的完整内容"""
    newline_placeholder = "§§§NEWLINE§§§"
    script = '''
    tell application "Notes"
        set idx to 0
        
        try
            set allFolders to every folder
            
            repeat with aFolder in allFolders
                if name of aFolder is "草稿" then
                    set folderNotes to every note of aFolder
                    
                    repeat with aNote in folderNotes
                        set idx to idx + 1
                        if idx is ''' + str(note_index) + ''' then
                            set noteTitle to name of aNote
                            set noteBody to body of aNote
                            return "TITLE:" & noteTitle & "''' + newline_placeholder + '''BODY:''' + newline_placeholder + '''" & noteBody
                        end if
                    end repeat
                    
                    exit repeat
                end if
            end repeat
        on error e
            return "ERROR:" & e
        end try
        
        return "NOTFOUND"
    end tell
    '''
    
    output, error = run_applescript(script)
    if error:
        return None, None, error
    
    if "NOTFOUND" in output:
        return None, None, "未找到指定的备忘录"
    
    # 解析输出
    newline_placeholder = "§§§NEWLINE§§§"
    output = output.replace(newline_placeholder, "\n")
    
    parts = output.split("\nBODY:\n", 1)
    if len(parts) < 2:
        parts = output.split("BODY:\n", 1)
    
    if len(parts) < 2:
        return None, None, "解析失败"
    
    title = parts[0].replace("TITLE:", "").strip()
    body = parts[1].strip()
    
    return title, body, None


def merge_consecutive_headings(text, tag):
    """合并连续的同级别 HTML 标题为一个（Apple Notes 会把标题拆成多个标签）"""
    pattern = r'(<{tag}[^>]*>.*?</{tag}>\s*)+'.format(tag=tag)
    
    def replacer(match):
        chunk = match.group(0)
        inner_pattern = r'<{tag}[^>]*>(.*?)</{tag}>'.format(tag=tag)
        parts = re.findall(inner_pattern, chunk, flags=re.IGNORECASE | re.DOTALL)
        merged = ' '.join(strip_basic_tags(p) for p in parts if strip_basic_tags(p).strip())
        if merged.strip():
            return '<{tag}>{merged}</{tag}>'.format(tag=tag, merged=merged)
        return ''
    
    text = re.sub(pattern, replacer, text, flags=re.IGNORECASE | re.DOTALL)
    return text


def html_to_markdown(text):
    """将 HTML 转换为 Markdown"""
    if not text:
        return ""
    
    if '<' not in text or '>' not in text:
        return text
    
    # 合并连续的同级别标题（Apple Notes 特有问题）
    text = merge_consecutive_headings(text, 'h1')
    text = merge_consecutive_headings(text, 'h2')
    
    # 清理 Notes 特有标签
    text = re.sub(r'</?font[^>]*>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'</?span[^>]*>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'</?div[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    
    # 处理 h1 标题（移除，因为 frontmatter 已包含标题）
    text = re.sub(r'<h1[^>]*>.*?</h1>', '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 处理 h2 标题
    def convert_h2(match):
        content = match.group(1)
        content = strip_basic_tags(content)
        if content and content.strip():
            return f'\n\n## {content}\n\n'
        return ''
    text = re.sub(r'<h2[^>]*>(.*?)</h2>', convert_h2, text, flags=re.IGNORECASE | re.DOTALL)
    
    # 处理 p 标签
    text = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 处理列表
    text = re.sub(r'<li[^>]*>(.*?)</li>', r'\n- \1', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 清理表格
    text = re.sub(r'</?table[^>]*>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'</?tbody[^>]*>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'</?tr[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</?td[^>]*>', ' | ', text, flags=re.IGNORECASE)
    text = re.sub(r'</?th[^>]*>', '| ', text, flags=re.IGNORECASE)
    text = re.sub(r'</?thead[^>]*>', '| ', text, flags=re.IGNORECASE)
    
    # 移除剩余标签
    text = re.sub(r'<[^>]+>', '', text)
    
    # 解码 HTML 实体
    for _ in range(3):
        old_text = text
        text = decode_html_entities(text)
        if text == old_text:
            break
    
    # 清理空白：段落之间保留一个空行，列表项之间不留空行
    lines = text.split('\n')
    result_lines = []
    prev_was_empty = True
    
    for line in lines:
        stripped = line.strip()
        
        if stripped and re.match(r'^[\|\-\s:]+$', stripped) and not stripped.startswith('- '):
            continue
        
        if stripped:
            # 列表项紧跟上一个列表项（不留空行）
            if stripped.startswith('- ') and result_lines and result_lines[-1] == '':
                prev_is_list = len(result_lines) >= 2 and result_lines[-2].startswith('- ')
                if prev_is_list:
                    result_lines.pop()  # 移除列表间的空行
            
            result_lines.append(stripped)
            prev_was_empty = False
        elif not prev_was_empty:
            result_lines.append('')
            prev_was_empty = True
    
    while result_lines and result_lines[-1] == '':
        result_lines.pop()
    
    result = '\n'.join(result_lines)
    
    # 重新编号有序列表
    lines = result.split('\n')
    fixed_lines = []
    in_list = False
    list_counter = 0
    for line in lines:
        if line.startswith('- '):
            in_list = True
            list_counter = 0
            fixed_lines.append(line)
        elif re.match(r'^\d+\.\s', line) and in_list:
            list_counter += 1
            fixed_lines.append(f'{list_counter}.' + line[line.index('.'):])
        else:
            in_list = False
            fixed_lines.append(line)
    
    result = '\n'.join(fixed_lines)
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    return result.strip()


def strip_basic_tags(text):
    """基本清理 HTML 标签"""
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    return decode_html_entities(text).strip()


def decode_html_entities(text):
    """解码 HTML 实体"""
    entities = {
        '&nbsp;': ' ', '&nbsp': ' ',
        '&lt;': '<', '&lt': '<',
        '&gt;': '>', '&gt': '>',
        '&amp;': '&', '&amp': '&',
        '&quot;': '"', '&quot': '"',
        '&#39;': "'", '&#39': "'",
        '&apos;': "'", '&apos': "'",
        '&mdash;': '—', '&mdash': '—',
        '&ndash;': '–', '&ndash': '–',
        '&hellip;': '…', '&hellip': '…',
        '&copy;': '©', '&copy': '©',
        '&reg;': '®', '&reg': '®',
        '&trade;': '™', '&trade': '™',
    }
    for entity, char in entities.items():
        text = text.replace(entity, char)
    text = re.sub(r'&#(\d+);?', lambda m: chr(int(m.group(1))), text)
    text = re.sub(r'&#x([0-9a-fA-F]+);?', lambda m: chr(int(m.group(1), 16)), text)
    return text


def export_note(note_index, output_path=None, slug=None):
    """导出单个备忘录"""
    title, body, error = get_note_content(note_index)
    
    if error:
        print(f"❌ {error}")
        return False
    
    markdown_content = html_to_markdown(body)
    
    export_date = datetime.now().strftime('%Y-%m-%d')
    frontmatter = f'''---
title: "{title}"
date: {export_date}
draft: false
tags:
- 
---

'''
    
    if not output_path:
        if slug:
            safe_slug = re.sub(r'[^\w\s-]', '', slug.lower())
            safe_slug = re.sub(r'[-\s]+', '-', safe_slug).strip('-')
        else:
            safe_slug = re.sub(r'[^\w\s-]', '', title.lower())
            safe_slug = re.sub(r'[-\s]+', '-', safe_slug).strip('-')
        output_path = f"content/blog/{export_date}-{safe_slug}/index.md"
    
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter + markdown_content)
    
    print(f"✅ 已导出: {output_path}")
    return True


def list_notes():
    """列出所有备忘录"""
    print("📝 草稿文件夹中的备忘录:")
    print("=" * 50)
    
    notes_list, error = get_notes_list()
    
    if error:
        print(f"❌ 获取备忘录失败: {error}")
        return
    
    if not notes_list:
        print("⚠️  没有找到备忘录")
        print("请确保备忘录中存在名为「草稿」的文件夹，并且里面有内容")
        return
    
    for note in notes_list:
        print(f"  {note}")
    
    print(f"\n共 {len(notes_list)} 篇备忘录")


def interactive_export():
    """交互式导出"""
    print("📝 从备忘录导入")
    print("=" * 50)
    
    notes_list, error = get_notes_list()
    
    if error:
        print(f"❌ {error}")
        return
    
    if not notes_list:
        print("⚠️  没有找到备忘录")
        return
    
    print("\n📋 可导入的备忘录:")
    for note in notes_list:
        print(f"  {note}")
    
    print("\n请输入要导入的序号 (多个用逗号分隔，如 1,3,5)，或输入 'a' 导入全部:")
    choice = input().strip()
    
    if not choice:
        return
    
    if choice.lower() == 'a':
        for i in range(1, len(notes_list) + 1):
            export_note(i)
    elif ',' in choice:
        indices = [int(x.strip()) for x in choice.split(',')]
        for idx in indices:
            if 1 <= idx <= len(notes_list):
                export_note(idx)
            else:
                print(f"⚠️  序号 {idx} 无效")
    else:
        try:
            idx = int(choice)
            if 1 <= idx <= len(notes_list):
                export_note(idx)
            else:
                print("❌ 无效的序号")
        except ValueError:
            print("❌ 请输入有效数字")


def skill_handler(args=None):
    """技能调用入口"""
    if args:
        if args.get('list'):
            list_notes()
        elif args.get('import'):
            export_note(int(args['import']))
        else:
            interactive_export()
    else:
        interactive_export()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="从苹果备忘录导入内容到博客",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 import_from_notes.py              # 交互式导入
  python3 import_from_notes.py --list       # 列出备忘录
  python3 import_from_notes.py --import 2   # 导入第2篇
        """
    )
    parser.add_argument('--list', '-l', action='store_true', help='列出备忘录')
    parser.add_argument('--import', '-i', dest='note_index', type=int, metavar='N', help='导入第N篇备忘录')
    parser.add_argument('--slug', '-s', dest='slug', type=str, metavar='SLUG', help='英文目录名（如 ai-restart-life）')
    
    args = parser.parse_args()
    
    if args.list:
        list_notes()
    elif args.note_index:
        export_note(args.note_index, slug=args.slug)
    else:
        interactive_export()

#!/usr/bin/env python3
"""
Apple Notes to Markdown Exporter
使用 AppleScript 直接从备忘录应用导出内容为 Markdown
"""

import os
import sys
import re
import argparse
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent


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


def escape_applescript(text):
    """转义 AppleScript 特殊字符"""
    if not text:
        return ""
    text = text.replace('\\', '\\\\')
    text = text.replace('"', '\\"')
    text = text.replace('\r', '\\r')
    text = text.replace('\n', '\\n')
    text = text.replace('\t', '\\t')
    return text


def get_notes_list():
    """获取草稿文件夹中的备忘录列表"""
    script = '''
    tell application "Notes"
        set noteList to {}
        
        repeat with aNote in notes
            set noteContainer to container of aNote
            set containerName to name of noteContainer
            
            if containerName is "草稿" then
                set noteTitle to name of aNote
                set noteBody to body of aNote
                set noteModDate to modification date of aNote
                
                -- 将日期转换为文本
                set dateStr to (text returned of (do shell script "date -j -f '%a %b %d %H:%M:%S %Y' + '%Y-%m-%d' date \"$(date -j -f \"%a %b %d %H:%M:%S %Y %z\" '\" & (time string of noteModDate) & \" +0000\" 2>/dev/null || date '+%Y-%m-%d')\""))
                
                set end of noteList to noteTitle & "|||DATE|||»" & noteModDate & "|||SEPARATOR|||»" & noteBody
            end if
        end repeat
        
        -- 返回备忘录数量和列表
        set noteCount to count of noteList
        return "COUNT:" & noteCount & "|||NOTES|||" & (noteList as text)
    end tell
    '''
    
    output, error = run_applescript(script)
    if error:
        print(f"❌ AppleScript 执行失败: {error}")
        return []
    
    return parse_notes_output(output)


def get_notes_list_simple():
    """简化版本 - 获取备忘录列表"""
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
        return None, error
    
    if "EMPTY" in output:
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
    
    return parse_single_note(output)


def parse_notes_output(output):
    """解析备忘录列表输出"""
    if not output or "COUNT:0" in output:
        return []
    
    notes = []
    parts = output.split("|||NOTES|||")
    if len(parts) < 2:
        return []
    
    count_part = parts[0].replace("COUNT:", "").strip()
    notes_text = parts[1]
    
    # 分割每个备忘录
    note_items = re.split(r'§§§', notes_text)
    for item in note_items:
        if "|||SEPARATOR|||»" in item:
            parts = item.split("|||SEPARATOR|||»")
            if len(parts) >= 2:
                title_with_date = parts[0]
                body = "|||SEPARATOR|||»".join(parts[1:])
                
                # 分离标题和日期
                if "|||DATE|||»" in title_with_date:
                    date_parts = title_with_date.split("|||DATE|||»")
                    title = date_parts[0] if date_parts else "无标题"
                    # 日期处理
                    try:
                        mod_date = datetime.strptime(date_parts[1][:19], "%Y-%m-%d %H:%M:%S")
                    except:
                        mod_date = datetime.now()
                else:
                    title = title_with_date
                    mod_date = datetime.now()
                
                notes.append({
                    'title': title,
                    'body': body,
                    'date': mod_date
                })
    
    return notes


def parse_single_note(output):
    """解析单个备忘录内容"""
    if not output or "NOTFOUND" in output:
        return None, None, "未找到"
    
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


def html_to_markdown(text):
    """将 HTML 转换为 Markdown"""
    if not text:
        return ""
    
    # 如果没有 HTML 标签，直接返回
    if '<' not in text or '>' not in text:
        return text
    
    # 先清理 Notes 特有的标签
    # 移除 font 标签但保留内容
    text = re.sub(r'</?font[^>]*>', '', text, flags=re.IGNORECASE)
    
    # 移除 span 标签但保留内容
    text = re.sub(r'</?span[^>]*>', '', text, flags=re.IGNORECASE)
    
    # 移除 div 标签但保留内容
    text = re.sub(r'</?div[^>]*>', '\n', text, flags=re.IGNORECASE)
    
    # 处理换行
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    
    # 处理 h1 标题 - Notes 可能用多个 h1 表示标题
    h1_pattern = r'<h1[^>]*>(.*?)</h1>'
    h1_matches = re.findall(h1_pattern, text, flags=re.IGNORECASE | re.DOTALL)
    if h1_matches:
        # 合并多个 h1 内容作为标题
        title_parts = [strip_basic_tags(m) for m in h1_matches if strip_basic_tags(m).strip()]
        if title_parts:
            combined_title = ''.join(title_parts)
            text = re.sub(h1_pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
            # 清理开头可能的空白
            text = text.strip()
    
    # 处理 h2 标题 - 忽略空的或只有空白的内容
    def convert_h2(match):
        content = match.group(1)
        content = strip_basic_tags(content)
        if content and content.strip():
            return f'\n## {content}\n'
        return ''
    text = re.sub(r'<h2[^>]*>(.*?)</h2>', convert_h2, text, flags=re.IGNORECASE | re.DOTALL)
    
    # 处理 h3-h6 标题
    text = re.sub(r'<h([3-6])[^>]*>(.*?)</h\1>', lambda m: f'\n{"#" * int(m.group(1))} {m.group(2)}\n', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 处理 p 标签
    text = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 处理无序列表项
    text = re.sub(r'<li[^>]*>(.*?)</li>', r'\n- \1', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 处理有序列表项
    text = re.sub(r'<li[^>]*>(\d+)\.\s*(.*?)</li>', r'\n1. \2', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 移除 table 相关标签
    text = re.sub(r'</?table[^>]*>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'</?tbody[^>]*>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'</?tr[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</?td[^>]*>', ' | ', text, flags=re.IGNORECASE)
    text = re.sub(r'</?th[^>]*>', '| ', text, flags=re.IGNORECASE)
    text = re.sub(r'</?thead[^>]*>', '| ', text, flags=re.IGNORECASE)
    
    # 移除所有剩余的 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)
    
    # 多次解码以处理嵌套实体
    for _ in range(3):
        old_text = text
        text = decode_html_entities(text)
        if text == old_text:
            break
    
    # 清理空白
    lines = text.split('\n')
    result_lines = []
    for line in lines:
        line = line.strip()
        # 跳过只包含分隔符的行
        if line and not re.match(r'^[\|\-\s:]+$', line):
            result_lines.append(line)
    
    result = '\n'.join(result_lines)
    
    # 重新处理列表编号
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
            # 重新编号
            list_counter += 1
            fixed_lines.append(f'{list_counter}.' + line[line.index('.'):])
        else:
            in_list = False
            fixed_lines.append(line)
    
    result = '\n'.join(fixed_lines)
    
    # 清理多余空行
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    # 移除开头可能的重复标题
    lines = result.split('\n')
    if len(lines) > 1 and lines[0].strip() in [lines[i].strip() for i in range(1, min(5, len(lines)))]:
        # 找到重复的行并移除
        first_line = lines[0].strip()
        cleaned = [lines[0]]  # 保留第一行作为标题
        seen_title = False
        for line in lines[1:]:
            if line.strip() == first_line and not seen_title:
                seen_title = True
                continue
            cleaned.append(line)
        result = '\n'.join(cleaned)
    
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
        '&nbsp;': ' ',
        '&nbsp': ' ',
        '&lt;': '<',
        '&lt': '<',
        '&gt;': '>',
        '&gt': '>',
        '&amp;': '&',
        '&amp': '&',
        '&quot;': '"',
        '&quot': '"',
        '&#39;': "'",
        '&#39': "'",
        '&apos;': "'",
        '&apos': "'",
        '&mdash;': '—',
        '&mdash': '—',
        '&ndash;': '–',
        '&ndash': '–',
        '&hellip;': '…',
        '&hellip': '…',
        '&copy;': '©',
        '&copy': '©',
        '&reg;': '®',
        '&reg': '®',
        '&trade;': '™',
        '&trade': '™',
    }
    for entity, char in entities.items():
        text = text.replace(entity, char)
    # 处理数字实体
    text = re.sub(r'&#(\d+);?', lambda m: chr(int(m.group(1))), text)
    text = re.sub(r'&#x([0-9a-fA-F]+);?', lambda m: chr(int(m.group(1), 16)), text)
    return text


def strip_html_tags(text):
    """移除 HTML 标签，保留内容"""
    if not text:
        return ""
    
    # 先处理自闭合标签
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    
    # 处理列表标签
    text = re.sub(r'</?ul[^>]*>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'</?ol[^>]*>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'</?li[^>]*>', '\n- ', text, flags=re.IGNORECASE)
    
    # 移除所有剩余标签
    text = re.sub(r'<[^>]+>', '', text)
    
    # 解码 HTML 实体
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&amp;', '&')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    
    # 清理空白
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def export_note_to_markdown(note_index, output_path=None):
    """导出单个备忘录为 Markdown"""
    
    title, body, error = get_note_content(note_index)
    
    if error:
        print(f"❌ {error}")
        return False
    
    # 转换为 Markdown
    markdown_content = html_to_markdown(body)
    
    # 生成 frontmatter
    export_date = datetime.now().strftime('%Y-%m-%d')
    frontmatter = f'''---
title: "{title}"
date: {export_date}
draft: false
tags:
- 
---

'''
    
    # 如果没有标题行，添加标题
    if not markdown_content.startswith('#'):
        full_content = frontmatter + '# ' + title + '\n\n' + markdown_content
    else:
        full_content = frontmatter + markdown_content
    
    # 保存文件
    if not output_path:
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        output_path = f"content/blog/{export_date}-{slug}/index.md"
    
    # 创建目录
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"✅ 已导出: {output_path}")
    return True


def list_notes():
    """列出所有备忘录"""
    print("📝 草稿文件夹中的备忘录:")
    print("=" * 50)
    
    notes_list, error = get_notes_list_simple()
    
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
    print("📝 Apple Notes 导出工具")
    print("=" * 50)
    
    # 获取列表
    notes_list, error = get_notes_list_simple()
    
    if error:
        print(f"❌ {error}")
        return
    
    if not notes_list:
        print("⚠️  没有找到备忘录")
        return
    
    print("\n📋 可导出的备忘录:")
    for note in notes_list:
        print(f"  {note}")
    
    print("\n请输入要导出的序号 (多个用逗号分隔，如 1,3,5)，或输入 'a' 导出全部:")
    choice = input().strip()
    
    if not choice:
        return
    
    if choice.lower() == 'a':
        # 导出全部
        for i in range(1, len(notes_list) + 1):
            export_note_to_markdown(i)
    elif ',' in choice:
        # 导出多个
        indices = [int(x.strip()) for x in choice.split(',')]
        for idx in indices:
            if 1 <= idx <= len(notes_list):
                export_note_to_markdown(idx)
            else:
                print(f"⚠️  序号 {idx} 无效")
    else:
        # 导出单个
        try:
            idx = int(choice)
            if 1 <= idx <= len(notes_list):
                export_note_to_markdown(idx)
            else:
                print(f"❌ 无效的序号")
        except ValueError:
            print("❌ 请输入有效数字")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="使用 AppleScript 从备忘录导出内容为 Markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 export_notes_applescript.py           # 交互式导出
  python3 export_notes_applescript.py --list    # 列出备忘录
  python3 export_notes_applescript.py --export 2 # 导出第2篇
        """
    )
    parser.add_argument('--list', '-l', action='store_true', help='列出备忘录')
    parser.add_argument('--export', '-e', type=int, metavar='N', help='导出第N篇备忘录')
    
    args = parser.parse_args()
    
    if args.list:
        list_notes()
    elif args.export:
        export_note_to_markdown(args.export)
    else:
        interactive_export()

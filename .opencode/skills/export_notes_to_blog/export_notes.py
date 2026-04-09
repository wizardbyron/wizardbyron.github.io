#!/usr/bin/env python3
"""
Apple Notes to Hugo Blog Exporter
使用 AppleScript 导出苹果备忘录中"草稿"文件夹的内容为 Hugo 博客格式
"""

import os
import sys
import shutil
import subprocess
import re
import argparse
from pathlib import Path
from datetime import datetime

# 配置
BLOG_CONTENT_DIR = "content/blog"
TEMP_DIR = "/tmp/notes_export"
SCRIPT_DIR = Path(__file__).parent


def ensure_temp_dir():
    """确保临时目录存在"""
    os.makedirs(TEMP_DIR, exist_ok=True)


def run_applescript(script):
    """运行 AppleScript 并返回结果"""
    try:
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode != 0:
            print(f"❌ AppleScript 执行失败: {result.stderr}")
            return None
        return result.stdout
    except subprocess.TimeoutExpired:
        print("❌ AppleScript 执行超时")
        return None
    except FileNotFoundError:
        print("❌ 未找到 osascript，请确保在 macOS 上运行")
        return None
    except Exception as e:
        print(f"❌ 执行 AppleScript 时出错: {e}")
        return None


def get_notes_from_draft_folder():
    """通过 AppleScript 获取草稿文件夹中的所有备忘录"""
    
    # AppleScript 获取备忘录列表
    script = '''
    tell application "Notes"
        -- 获取所有备忘录的标题和内容
        set noteList to {}
        
        -- 遍历所有备忘录，查找草稿文件夹
        repeat with aNote in notes
            set noteContainer to container of aNote
            set containerName to name of noteContainer
            
            -- 检查是否在草稿文件夹
            if containerName is "草稿" then
                set noteTitle to name of aNote
                set noteBody to body of aNote
                
                -- 将标题和内容添加到列表
                set end of noteList to noteTitle & "|||SEPARATOR|||»" & noteBody
            end if
        end repeat
        
        -- 返回备忘录数量
        set noteCount to count of noteList
        
        -- 如果有备忘录，返回第一个备忘录测试
        if noteCount > 0 then
            return "COUNT:" & noteCount & "|||NOTES|||" & (item 1 of noteList)
        else
            return "COUNT:0"
        end if
    end tell
    '''
    
    result = run_applescript(script)
    if not result:
        return []
    
    # 解析结果
    if "COUNT:0" in result:
        return []
    
    # 提取备忘录数量
    parts = result.split("|||NOTES|||")
    if len(parts) < 2:
        return []
    
    count_part = parts[0].replace("COUNT:", "").strip()
    try:
        note_count = int(count_part)
    except ValueError:
        return []
    
    # 获取所有备忘录
    all_notes_script = '''
    tell application "Notes"
        set noteList to {}
        
        repeat with aNote in notes
            set noteContainer to container of aNote
            set containerName to name of noteContainer
            
            if containerName is "草稿" then
                set noteTitle to name of aNote
                set noteBody to body of aNote
                set end of noteList to noteTitle & "|||SEPARATOR|||»" & noteBody
            end if
        end repeat
        
        -- 返回备忘录总数
        set noteCount to count of noteList
        
        -- 构建返回字符串
        set output to "COUNT:" & noteCount & "|||NOTES|||"
        repeat with i from 1 to noteCount
            set output to output & (item i of noteList)
            if i < noteCount then
                set output to output & "|||NOTE|||"
            end if
        end repeat
        
        return output
    end tell
    '''
    
    result = run_applescript(all_notes_script)
    if not result:
        return []
    
    # 解析所有备忘录
    parts = result.split("|||NOTES|||")
    if len(parts) < 2:
        return []
    
    count_part = parts[0].replace("COUNT:", "").strip()
    try:
        note_count = int(count_part)
    except ValueError:
        return []
    
    notes = []
    if note_count > 0:
        note_parts = parts[1].split("|||NOTE|||")
        for note_text in note_parts:
            if "|||SEPARATOR|||»" in note_text:
                idx = note_text.index("|||SEPARATOR|||»")
                title = note_text[:idx]
                body = note_text[idx + len("|||SEPARATOR|||»"):]
                notes.append({
                    'title': title,
                    'body': body
                })
    
    return notes


def text_to_markdown(text):
    """将 HTML 文本转换为 Markdown"""
    if not text:
        return ""
    
    # 检查是否是 HTML
    is_html = '<' in text and '>' in text
    
    if is_html:
        # 清理 HTML 结构（移除外层 div wrapper）
        text = text.strip()
        if text.startswith('<div>') and text.endswith('</div>'):
            # 尝试提取内部内容
            text = re.sub(r'^<div>(.*)</div>$', r'\1', text, flags=re.DOTALL)
        
        # 使用 pandoc 转换 HTML 到 Markdown
        temp_html = f"{TEMP_DIR}/temp_note.html"
        with open(temp_html, 'w', encoding='utf-8') as f:
            f.write(text)
        
        try:
            # 使用 markdown 选项避免扩展语法
            result = subprocess.run(
                ['pandoc', '-f', 'html', '-t', 'markdown-raw_html', '--wrap=none', temp_html],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0 and result.stdout:
                output = result.stdout.strip()
                # 清理 pandoc 生成的额外块语法
                output = re.sub(r'^:::.*?\n', '', output, flags=re.MULTILINE)
                output = re.sub(r'^:::\s*$', '', output, flags=re.MULTILINE)
                output = re.sub(r'\n:::.*', '', output)
                # 清理 LaTeX 换行符
                output = re.sub(r'\\\n', '\n', output)
                output = re.sub(r'\\$', '', output, flags=re.MULTILINE)
                os.remove(temp_html)
                return output.strip()
        except Exception:
            pass
        finally:
            if os.path.exists(temp_html):
                os.remove(temp_html)
    
    # 降级处理：基本文本清理
    text = re.sub(r'<[^>]+>', '', text)  # 移除 HTML 标签
    text = re.sub(r'\n{3,}', '\n\n', text)  # 规范化换行
    return text.strip()


def export_notes_to_blog():
    """主导出函数"""
    print("📝 苹果备忘录导出工具 (AppleScript 模式)")
    print("=" * 50)
    
    ensure_temp_dir()
    
    # 获取备忘录
    print("🔍 查找'草稿'文件夹中的备忘录...")
    notes = get_notes_from_draft_folder()
    
    if not notes:
        print("⚠️  未找到备忘录，请检查：")
        print("   1. 备忘录中是否存在名为'草稿'的文件夹")
        print("   2. '草稿'文件夹中是否有备忘录")
        print("   3. 备忘录应用是否正常运行")
        sys.exit(0)
    
    print(f"✅ 找到 {len(notes)} 篇备忘录:")
    print()
    
    # 显示备忘录列表
    for i, note in enumerate(notes, 1):
        title = note['title'] or "无标题"
        body_preview = note['body'][:50] + "..." if len(note['body']) > 50 else note['body']
        print(f"  {i}. {title}")
        if body_preview:
            print(f"     📄 {body_preview}")
    print()
    
    # 选择导出模式
    print("请选择导出模式:")
    print("  1. 导出所有备忘录")
    print("  2. 指定序号导出")
    
    choice = input("\n请输入选择 (1/2) [默认 1]: ").strip() or "1"
    
    notes_to_export = []
    
    if choice == "2":
        indices = input("请输入要导出的序号 (用逗号分隔，如 1,3,5): ").strip()
        try:
            indices = [int(i.strip()) for i in indices.split(',')]
            notes_to_export = [notes[i-1] for i in indices if 1 <= i <= len(notes)]
        except ValueError:
            print("❌ 输入格式错误")
            sys.exit(1)
    else:
        notes_to_export = notes
    
    # 导出每个备忘录
    export_date = datetime.now().strftime('%Y-%m-%d')
    exported_count = 0
    
    print(f"\n🚀 开始导出到 {BLOG_CONTENT_DIR}/...")
    print()
    
    for note in notes_to_export:
        title = note['title'] or "无标题"
        
        # 生成博客目录名
        slug = create_slug(title)
        blog_dir = Path(BLOG_CONTENT_DIR) / f"{export_date}-{slug}"
        
        # 处理重名
        counter = 1
        while blog_dir.exists():
            blog_dir = Path(BLOG_CONTENT_DIR) / f"{export_date}-{slug}-{counter}"
            counter += 1
        
        blog_dir.mkdir(parents=True, exist_ok=True)
        
        # 转换为 Markdown
        markdown_content = text_to_markdown(note['body'])
        
        # 生成带 frontmatter 的文件
        frontmatter = f'''---
title: "{title}"
date: {export_date}
draft: false
tags:
- 
---

'''
        
        index_path = blog_dir / "index.md"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
            f.write(markdown_content)
        
        exported_count += 1
        print(f"  ✅ 已导出: {title}")
    
    print()
    print("=" * 50)
    print(f"🎉 导出完成! 共导出 {exported_count} 篇备忘录")
    print(f"📁 文件位置: {BLOG_CONTENT_DIR}/")


def create_slug(title):
    """从标题创建 URL 友好的 slug"""
    if not title:
        title = "untitled"
    
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    slug = slug.strip('-')
    
    return slug or "untitled"


def list_notes():
    """仅列出备忘录，不导出"""
    notes = get_notes_from_draft_folder()
    
    if not notes:
        print("⚠️  未找到备忘录")
        return
    
    print(f"📝 '草稿'文件夹中共 {len(notes)} 篇备忘录:\n")
    for i, note in enumerate(notes, 1):
        title = note['title'] or "无标题"
        body_len = len(note['body'])
        print(f"  {i}. {title}")
        print(f"     📄 {body_len} 字符")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="苹果备忘录导出工具 - 将备忘录导出为 Hugo 博客格式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 export_notes.py              # 交互式导出
  python3 export_notes.py --list       # 仅列出备忘录
  python3 export_notes.py --dry-run   # 预览模式
        """
    )
    parser.add_argument('--list', action='store_true',
                        help='仅列出备忘录，不导出')
    parser.add_argument('--dry-run', action='store_true',
                        help='预览模式，显示将要导出的内容')
    
    args = parser.parse_args()
    
    if args.list:
        print("🔍 列出备忘录...\n")
        list_notes()
    elif args.dry_run:
        print("🔍 预览模式\n")
        list_notes()
        print("💡 运行不带参数的命令开始导出")
    else:
        export_notes_to_blog()

#!/usr/bin/env python3
"""
Create Trade Plan
创建交易计划博客文章
"""

import os
import re
import argparse
from pathlib import Path
from datetime import datetime


def create_trade_plan(title, slug=None, stock_code=None, date=None):
    """创建交易计划文章"""
    project_root = Path(__file__).resolve().parents[3]
    archetype_path = project_root / "archetypes" / "trade-plan.md"
    
    if not archetype_path.exists():
        print("❌ 找不到模板文件: archetypes/trade-plan.md")
        return False
    
    with open(archetype_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    if date:
        export_date = date
    else:
        export_date = datetime.now().strftime('%Y-%m-%d')
    
    if slug:
        safe_slug = re.sub(r'[^\w\s-]', '', slug.lower())
        safe_slug = re.sub(r'[-\s]+', '-', safe_slug).strip('-')
    else:
        safe_slug = re.sub(r'[^\w\s-]', '', title.lower())
        safe_slug = re.sub(r'[-\s]+', '-', safe_slug).strip('-')
    
    dir_name = f"{export_date}-{safe_slug}"
    output_dir = project_root / "content" / "blog" / dir_name
    output_path = output_dir / "index.md"
    
    if output_path.exists():
        print(f"⚠️  文件已存在: {output_path}")
        overwrite = input("是否覆盖？(y/N): ").strip().lower()
        if overwrite != 'y':
            print("已取消")
            return False
    
    content = template.replace('{{ replace .Name "-" " " | title }}', title)
    content = content.replace('{{ .Date }}', export_date)
    
    if stock_code:
        content = content.replace(
            '## 声明',
            f'## 声明\n\n本文是根据我自己的交易系统在**{title}（{stock_code}）**的一次交易复盘。'
        )
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已创建交易计划: {output_path}")
    print(f"   目录: content/blog/{dir_name}/")
    print(f"   状态: 草稿 (draft: true)")
    return True


def skill_handler(args=None):
    """技能调用入口"""
    if args:
        create_trade_plan(
            title=args.get('title', '未命名交易计划'),
            slug=args.get('slug'),
            stock_code=args.get('stock_code'),
            date=args.get('date')
        )
    else:
        interactive_create()


def interactive_create():
    """交互式创建"""
    print("📝 创建交易计划")
    print("=" * 50)
    
    title = input("文章标题: ").strip()
    if not title:
        print("❌ 标题不能为空")
        return
    
    stock_code = input("股票代码 (如 SZ.002163，可选): ").strip() or None
    slug = input("英文目录名 (如 trade-review-sz002163，可选): ").strip() or None
    date = input(f"日期 (默认今天 {datetime.now().strftime('%Y-%m-%d')}): ").strip() or None
    
    create_trade_plan(title=title, slug=slug, stock_code=stock_code, date=date)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="创建交易计划博客文章",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 create_trade_plan.py -t "海南发展交易复盘" -c "SZ.002163" -s trade-review-sz002163
  python3 create_trade_plan.py --interactive
        """
    )
    parser.add_argument('-t', '--title', type=str, help='文章标题')
    parser.add_argument('-c', '--code', dest='stock_code', type=str, help='股票代码（如 SZ.002163）')
    parser.add_argument('-s', '--slug', type=str, help='英文目录名')
    parser.add_argument('-d', '--date', type=str, help='日期 (YYYY-MM-DD)')
    parser.add_argument('-i', '--interactive', action='store_true', help='交互式创建')
    
    args = parser.parse_args()
    
    if args.interactive or not args.title:
        interactive_create()
    else:
        create_trade_plan(
            title=args.title,
            slug=args.slug,
            stock_code=args.stock_code,
            date=args.date
        )

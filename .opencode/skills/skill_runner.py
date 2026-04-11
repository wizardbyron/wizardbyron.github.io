#!/usr/bin/env python3
"""
opencode 技能入口模块
处理 skill 工具的调用
"""
import sys
import json
from pathlib import Path

SKILLS_DIR = Path(__file__).parent
sys.path.insert(0, str(SKILLS_DIR / "import-from-notes"))
sys.path.insert(0, str(SKILLS_DIR / "export-to-wechat"))
sys.path.insert(0, str(SKILLS_DIR / "create-trade-plan"))

def handle_skill(skill_name, args=None):
    """处理技能调用"""
    if skill_name == "import-from-notes":
        from import_from_notes import skill_handler
        skill_handler(args)
    elif skill_name == "export-to-wechat":
        from export_to_wechat import skill_handler
        skill_handler(args)
    elif skill_name == "create-trade-plan":
        from create_trade_plan import skill_handler
        skill_handler(args)
    else:
        print(f"未知技能: {skill_name}")
        print("可用技能: import-from-notes, export-to-wechat, create-trade-plan")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 skill_runner.py <skill_name> [args_json]")
        print("示例: python3 skill_runner.py import-from-notes")
        sys.exit(1)
    
    skill_name = sys.argv[1]
    args = None
    
    if len(sys.argv) > 2:
        try:
            args = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            print(f"无效的 JSON 参数: {sys.argv[2]}")
            sys.exit(1)
    
    handle_skill(skill_name, args)

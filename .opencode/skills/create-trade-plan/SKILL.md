---
name: create-trade-plan
description: 基于模板快速创建交易计划博客文章，包含分析、入场、持有、离场、复盘五个部分，支持指定股票代码和英文目录名。
---

## 功能说明

基于模板快速创建交易计划博客文章，包含分析、入场、持有、离场、复盘五个部分。

## 使用方式

### 交互式创建（推荐）

```bash
python3 .opencode/skills/create-trade-plan/create_trade_plan.py
```

### 命令行创建

```bash
# 指定标题和股票代码
python3 .opencode/skills/create-trade-plan/create_trade_plan.py -t "海南发展交易复盘" -c "SZ.002163" -s trade-review-sz002163

# 指定日期
python3 .opencode/skills/create-trade-plan/create_trade_plan.py -t "标题" -d 2026-04-15
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `-t` / `--title` | 文章标题 | "海南发展交易复盘" |
| `-c` / `--code` | 股票代码 | "SZ.002163" |
| `-s` / `--slug` | 英文目录名 | "trade-review-sz002163" |
| `-d` / `--date` | 日期 | "2026-04-15" |
| `-i` / `--interactive` | 交互式创建 | |

## 模板文件

模板位置：`archetypes/trade-plan.md`

## 文章结构

1. **分析** - 宏观背景、选股逻辑、关键价位、交易周期判断
2. **入场** - 仓位计划、条件单设置、止损条件
3. **持有** - 止盈条件（上移止损）、每日跟踪表格
4. **离场** - 离场原因、条件单执行、收益统计
5. **复盘** - 做的好的、做的不好的、反思与改进

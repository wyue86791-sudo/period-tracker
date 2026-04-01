---
name: period-tracker
description: "Period cycle tracker and predictor. Record periods by saying '月经来了', 'period started', 'my period came'. Analyze cycles by saying '查月经', 'period analysis', 'predict period'. Also supports '大姨妈来了', '例假来了', '生理期来了', '周期分析', '预测月经', '下次月经'. Manages menstrual cycle records with smart prediction."
license: MIT
compatibility: "Requires Python 3.9+. No third-party dependencies. Works on macOS, Linux, Windows."
metadata:
  author: wyue86791-sudo
  version: "1.0.0"
  display_name: "掌管月经的神"
  language: "zh-CN"
  category: "health"
---

# 🩸 掌管月经的神 — 月经周期记录 & 分析预测

一个本地化的月经周期记录、分析与预测工具。数据完全本地存储，保护隐私。

## 数据存储

数据文件存储在 Skill 目录下的 `data/records.json`。
脚本路径: `${CLAUDE_SKILL_DIR}/scripts/period.py`

> **跨平台路径**: 脚本会自动检测所在目录，数据文件存储在脚本同级的 `../data/` 目录下。无需手动配置路径。

## 指令映射

根据用户消息匹配操作：

| 用户说 | 操作 |
|--------|------|
| 月经来了 / 大姨妈来了 / 例假来了 / 生理期来了 / period started | `record`（记录当前时间） |
| 20260305月经来了 / 260305月经来了 | `record 20260305`（从消息中提取纯数字日期） |
| 月经来了 + 具体日期（如"月经3月28号来的"） | `record <日期>` |
| 查月经 / 月经分析 / 查大姨妈 / 周期分析 / 预测月经 / period analysis | `analyze` |
| 删除月经记录 / 撤销上次记录 | `delete` |
| 月经记录列表 / 查看所有记录 | `list` |

### 日期提取规则

当用户消息中包含数字+「月经来了」时，提取前面的数字作为日期传入 record 命令：
- `20260305月经来了` → `record "20260305"`
- `260305月经来了` → `record "260305"`
- `0305月经来了` → `record "03-05"`（补当年）

脚本支持的日期格式：`20260401`、`260401`、`2026-04-01`、`04-01`、`4月1日`

## 执行方式

```bash
# 记录（当前时间）
python3 ${CLAUDE_SKILL_DIR}/scripts/period.py record

# 记录（指定时间）
python3 ${CLAUDE_SKILL_DIR}/scripts/period.py record "2026-04-01"

# 分析预测
python3 ${CLAUDE_SKILL_DIR}/scripts/period.py analyze

# 删除最近一条
python3 ${CLAUDE_SKILL_DIR}/scripts/period.py delete

# 列出所有
python3 ${CLAUDE_SKILL_DIR}/scripts/period.py list
```

## 回复规则

- **记录时**：执行脚本后，用温和友好的语气告知已记录，附上脚本输出的周期信息
- **分析时**：执行脚本后，将文本输出原样转发给用户，保留所有数据和 emoji
- **隐私**：此为高度隐私数据，绝不在任何非用户直接对话的场合提及或泄露

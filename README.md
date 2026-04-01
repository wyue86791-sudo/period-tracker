# 🩸 掌管月经的神

> 一个 WorkBuddy Skill —— 用自然语言记录月经、分析周期、预测下一次。

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![WorkBuddy](https://img.shields.io/badge/WorkBuddy-Skill-blueviolet)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ 功能亮点

- 📝 **一句话记录** — 说"月经来了"即刻记录，支持补记历史日期
- 📊 **智能分析** — 自动统计周期规律，展示提前/推迟趋势
- 🔮 **加权预测** — 基于近期数据加权计算下次月经时间
- 📱 **微信友好** — 精简文字报告，一屏看完
- 🔒 **本地隐私** — 数据存在本机，绝不上传

## 📋 使用方式

在 WorkBuddy 对话中直接说：

| 你说 | 效果 |
|------|------|
| `月经来了` | 记录今天 |
| `20260305月经来了` | 补记 2026年3月5日 |
| `月经3月28号来的` | 补记 3月28日 |
| `查月经` / `月经分析` | 查看周期分析报告 |
| `删除月经记录` | 删除最近一条 |
| `月经记录列表` | 查看所有记录 |

## 📊 分析报告示例

```
🩸 周期报告（12次记录）

25.04.01
25.04.30  29天 🟢
25.05.28  28天 -1天
25.06.26  29天 🟢
25.07.25  29天 🟢
25.08.22  28天 🟢
25.09.20  29天 🟢
25.10.17  27天 -2天
25.11.16  30天 +2天
25.12.13  27天 -2天
26.01.12  30天 +2天
26.02.10  29天 🟢

📊 平均周期29天 | 27~30天 | ✨很规律

🔮 下次预测 26.03.11（03.10~03.12）还有1天
```

**符号说明**：🟢 正常 | `+N天` 推迟 | `-N天` 提前

## 🚀 安装

### 方式一：手动安装

将本仓库克隆到 WorkBuddy 的 skills 目录：

```bash
git clone https://github.com/YOUR_USERNAME/period-tracker.git ~/.workbuddy/skills/period-tracker
```

### 方式二：WorkBuddy 导入

1. 打开 WorkBuddy → 设置 → Skills 管理
2. 点击「从 Git 仓库导入」
3. 粘贴本仓库地址

### 方式三：ZIP 安装

下载 Release 中的 zip 文件，解压到 `~/.workbuddy/skills/period-tracker/`

## 📁 文件结构

```
period-tracker/
├── SKILL.md          # Skill 定义（WorkBuddy 读取）
├── README.md         # 说明文档
├── scripts/
│   └── period.py     # 核心脚本
└── data/             # 数据目录（自动创建）
    └── records.json  # 记录文件（.gitignore 忽略）
```

## ⚙️ 技术细节

- **语言**: Python 3.9+（无第三方依赖）
- **数据格式**: JSON
- **日期支持**: `YYYYMMDD`、`YYMMDD`、`YYYY-MM-DD`、`MM-DD`、`M月D日`
- **预测算法**: 加权移动平均（近期权重更高）
- **防重复**: 3天内重复记录自动忽略

## 📜 License

MIT License — 随便用，开心就好 🌸

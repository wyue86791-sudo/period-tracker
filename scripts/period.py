#!/usr/bin/env python3
"""月经周期记录与分析预测工具"""

import json
import os
import sys
from datetime import datetime, timedelta

# 跨平台路径：自动检测脚本所在目录，数据存在同级 ../data/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(SKILL_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "records.json")


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_records():
    """加载所有记录，返回按时间排序的列表"""
    ensure_data_dir()
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    # 按时间排序
    data.sort(key=lambda x: x["start"])
    return data


def save_records(records):
    ensure_data_dir()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def cmd_record(time_str=None):
    """记录月经开始时间。无参数则用当前时间，有参数则解析指定时间"""
    records = load_records()

    if time_str:
        # 支持多种格式
        dt = None
        for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d", "%Y%m%d", "%m-%d", "%m月%d日"):
            try:
                dt = datetime.strptime(time_str, fmt)
                if dt.year == 1900:  # 只有月日，补上今年
                    dt = dt.replace(year=datetime.now().year)
                break
            except ValueError:
                continue

        # 尝试纯数字格式：6位(YYMMDD) 或 8位(YYYYMMDD)
        if dt is None and time_str.isdigit():
            if len(time_str) == 8:
                try:
                    dt = datetime.strptime(time_str, "%Y%m%d")
                except ValueError:
                    pass
            elif len(time_str) == 6:
                try:
                    dt = datetime(2000 + int(time_str[:2]), int(time_str[2:4]), int(time_str[4:6]))
                except (ValueError, OverflowError):
                    pass

        if dt is None:
            print(f"❌ 无法解析时间: {time_str}")
            print("支持格式: 20260401, 260401, 2026-04-01, 04-01, 4月1日")
            sys.exit(1)
    else:
        dt = datetime.now()

    # 检查是否与最近一次记录太近（3天内视为重复）
    if records:
        last = datetime.fromisoformat(records[-1]["start"])
        diff = abs((dt - last).days)
        if diff < 3:
            print(f"⚠️ 距上次记录仅 {diff} 天（{last.strftime('%Y-%m-%d')}），已忽略重复记录。")
            print(f"如确需记录，请先用 delete 命令删除上次记录。")
            sys.exit(0)

    record = {
        "start": dt.isoformat(timespec="minutes"),
        "recorded_at": datetime.now().isoformat(timespec="minutes"),
    }
    records.append(record)
    save_records(records)

    print(f"✅ 已记录月经开始时间: {dt.strftime('%Y年%m月%d日 %H:%M')}")
    if len(records) >= 2:
        prev = datetime.fromisoformat(records[-2]["start"])
        cycle = (dt - prev).days
        print(f"📊 本次周期: {cycle} 天")


def cmd_analyze():
    """分析最近12次记录并预测下次时间（微信友好精简版）"""
    records = load_records()

    if not records:
        print("📭 暂无记录，发「月经来了」开始记录")
        sys.exit(0)

    # 取最近12次
    recent = records[-12:]
    total = len(recent)

    lines = []
    lines.append(f"🩸 周期报告（{total}次记录）")
    lines.append("")

    # --- 记录列表 & 周期计算 ---
    cycles = []
    for i, rec in enumerate(recent):
        dt = datetime.fromisoformat(rec["start"])
        date_short = dt.strftime("%y.%m.%d")

        if i == 0:
            lines.append(f"{date_short}")
        else:
            prev_dt = datetime.fromisoformat(recent[i - 1]["start"])
            cycle = (dt - prev_dt).days
            cycles.append(cycle)

            # 与平均周期比较
            if len(cycles) >= 2:
                avg_so_far = sum(cycles[:-1]) / len(cycles[:-1])
                diff = cycle - avg_so_far
                if abs(diff) < 1:
                    mark = "🟢"
                elif diff > 0:
                    mark = f"+{abs(diff):.0f}天"
                else:
                    mark = f"-{abs(diff):.0f}天"
            else:
                mark = "🟢"

            lines.append(f"{date_short}  {cycle}天 {mark}")

    # --- 统计 & 预测 ---
    if cycles:
        avg_cycle = sum(cycles) / len(cycles)
        min_cycle = min(cycles)
        max_cycle = max(cycles)
        variance = sum((c - avg_cycle) ** 2 for c in cycles) / len(cycles)
        std_dev = variance ** 0.5

        if std_dev <= 2:
            reg = "✨很规律"
        elif std_dev <= 4:
            reg = "👍较规律"
        elif std_dev <= 7:
            reg = "📊有波动"
        else:
            reg = "⚠️波动大"

        lines.append("")
        lines.append(f"📊 平均周期{avg_cycle:.0f}天 | {min_cycle}~{max_cycle}天 | {reg}")

        # 预测
        last_dt = datetime.fromisoformat(recent[-1]["start"])
        if len(cycles) >= 3:
            weights = list(range(1, len(cycles) + 1))
            weighted_avg = sum(c * w for c, w in zip(cycles, weights)) / sum(weights)
        else:
            weighted_avg = avg_cycle

        predicted_dt = last_dt + timedelta(days=round(weighted_avg))
        early_dt = last_dt + timedelta(days=round(weighted_avg - std_dev))
        late_dt = last_dt + timedelta(days=round(weighted_avg + std_dev))

        today = datetime.now()
        days_until = (predicted_dt - today).days

        lines.append("")
        if days_until > 0:
            countdown = f"还有{days_until}天"
        elif days_until == 0:
            countdown = "就是今天❗"
        else:
            countdown = f"超出{abs(days_until)}天⏰"

        lines.append(f"🔮 下次预测 {predicted_dt.strftime('%y.%m.%d')}（{early_dt.strftime('%m.%d')}~{late_dt.strftime('%m.%d')}）{countdown}")
    else:
        lines.append("")
        lines.append("📌 至少2次记录才能分析")

    print("\n".join(lines))


def cmd_delete():
    """删除最近一条记录"""
    records = load_records()
    if not records:
        print("📭 无记录可删除。")
        sys.exit(0)

    removed = records.pop()
    save_records(records)
    dt = datetime.fromisoformat(removed["start"])
    print(f"🗑️ 已删除最近一条记录: {dt.strftime('%Y年%m月%d日 %H:%M')}")
    print(f"📊 剩余 {len(records)} 条记录。")


def cmd_list():
    """列出所有记录"""
    records = load_records()
    if not records:
        print("📭 暂无记录。")
        sys.exit(0)

    print(f"📋 全部月经记录（共 {len(records)} 条）:\n")
    for i, rec in enumerate(records, 1):
        dt = datetime.fromisoformat(rec["start"])
        print(f"  {i:>3}. {dt.strftime('%Y-%m-%d %H:%M')}")


def main():
    if len(sys.argv) < 2:
        print("用法: period.py <command> [args]")
        print("命令:")
        print("  record [时间]  - 记录月经开始（默认当前时间）")
        print("  analyze        - 分析周期并预测")
        print("  delete         - 删除最近一条记录")
        print("  list           - 列出所有记录")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "record":
        time_str = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
        cmd_record(time_str)
    elif cmd == "analyze":
        cmd_analyze()
    elif cmd == "delete":
        cmd_delete()
    elif cmd == "list":
        cmd_list()
    else:
        print(f"❌ 未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Trend Tracker
跨日复盘趋势追踪，识别长期模式
"""

import os
import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict


class TrendTracker:
    """趋势追踪器"""

    def __init__(self, review_dir: str = "./skills/daily-review/review_history"):
        self.review_dir = review_dir

    def get_recent_reports(self, days: int = 7) -> List[Dict]:
        """获取最近 N 天的复盘报告"""
        reports = []

        for f in os.listdir(self.review_dir):
            if f.endswith(".yaml") and f.startswith("review_"):
                date_str = f.split("_")[1]
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    if (datetime.now() - date).days <= days:
                        reports.append({
                            "date": date_str,
                            "file": f,
                            "path": os.path.join(self.review_dir, f)
                        })
                except:
                    continue

        reports.sort(key=lambda x: x["date"], reverse=True)
        return reports

    def extract_metrics(self, report_path: str) -> Dict:
        """从报告中提取关键指标"""
        # 简化版：实际使用时会解析 YAML
        metrics = {
            "completion_rate": 0.0,
            "total_work_hours": 0.0,
            "meeting_hours": 0.0,
            "deep_work_hours": 0.0,
            "ok_count": 0,
            "problem_count": 0,
            "emotional_intensity": 0.0,
        }

        # 读取文件内容，用正则提取
        try:
            with open(report_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 提取完成度
            match = re.search(r"completion_rate:\s*([\d.]+)", content)
            if match:
                metrics["completion_rate"] = float(match.group(1))

            # 提取工作时长
            match = re.search(r"total_work_hours:\s*([\d.]+)", content)
            if match:
                metrics["total_work_hours"] = float(match.group(1))

            # 提取会议时长
            match = re.search(r"meeting_hours:\s*([\d.]+)", content)
            if match:
                metrics["meeting_hours"] = float(match.group(1))

            # 提取深度工作时长
            match = re.search(r"deep_work_hours:\s*([\d.]+)", content)
            if match:
                metrics["deep_work_hours"] = float(match.group(1))

            # 统计 OK 和问题数量（Markdown 中）
            md_path = report_path.replace(".yaml", ".md")
            if os.path.exists(md_path):
                with open(md_path, "r", encoding="utf-8") as f:
                    md_content = f.read()

                metrics["ok_count"] = len(re.findall(r"## 02 ✅", md_content))
                metrics["problem_count"] = len(re.findall(r"## 03 ❌", md_content))

        except Exception as e:
            print(f"Error extracting metrics from {report_path}: {e}")

        return metrics

    def calculate_trends(self, days: int = 7) -> Dict:
        """计算趋势"""
        reports = self.get_recent_reports(days)

        if len(reports) < 2:
            return {
                "status": "insufficient_data",
                "message": f"需要至少 2 天数据才能分析趋势，当前只有 {len(reports)} 天",
                "reports_count": len(reports)
            }

        # 提取所有指标
        all_metrics = []
        for report in reports:
            metrics = self.extract_metrics(report["path"])
            metrics["date"] = report["date"]
            all_metrics.append(metrics)

        # 计算趋势
        trends = {
            "status": "success",
            "period": f"{days} 天",
            "reports_count": len(reports),
            "date_range": f"{reports[-1]['date']} ~ {reports[0]['date']}",

            "improvements": [],
            "declines": [],
            "patterns": [],
            "averages": {},
            "trend_lines": {}
        }

        # 计算平均值
        for key in ["completion_rate", "total_work_hours", "meeting_hours", 
                    "deep_work_hours", "ok_count", "problem_count"]:
            values = [m.get(key, 0) for m in all_metrics if key in m]
            if values:
                trends["averages"][key] = sum(values) / len(values)
                trends["trend_lines"][key] = values

        # 识别趋势（简化版：比较首尾）
        if len(all_metrics) >= 2:
            first = all_metrics[-1]  # 最早
            last = all_metrics[0]    # 最近

            # 完成度趋势
            if last.get("completion_rate", 0) > first.get("completion_rate", 0) + 0.1:
                trends["improvements"].append(
                    f"计划完成度提升：{first.get('completion_rate', 0):.0%} → {last.get('completion_rate', 0):.0%}"
                )
            elif last.get("completion_rate", 0) < first.get("completion_rate", 0) - 0.1:
                trends["declines"].append(
                    f"计划完成度下降：{first.get('completion_rate', 0):.0%} → {last.get('completion_rate', 0):.0%}"
                )

            # 深度工作趋势
            if last.get("deep_work_hours", 0) > first.get("deep_work_hours", 0) + 0.5:
                trends["improvements"].append(
                    f"深度工作时长增加：{first.get('deep_work_hours', 0):.1f}h → {last.get('deep_work_hours', 0):.1f}h"
                )
            elif last.get("deep_work_hours", 0) < first.get("deep_work_hours", 0) - 0.5:
                trends["declines"].append(
                    f"深度工作时长减少：{first.get('deep_work_hours', 0):.1f}h → {last.get('deep_work_hours', 0):.1f}h"
                )

            # 会议时间趋势
            if last.get("meeting_hours", 0) > first.get("meeting_hours", 0) + 0.5:
                trends["declines"].append(
                    f"会议时间增加：{first.get('meeting_hours', 0):.1f}h → {last.get('meeting_hours', 0):.1f}h"
                )
            elif last.get("meeting_hours", 0) < first.get("meeting_hours", 0) - 0.5:
                trends["improvements"].append(
                    f"会议时间减少：{first.get('meeting_hours', 0):.1f}h → {last.get('meeting_hours', 0):.1f}h"
                )

        # 识别重复模式（简化版：检查连续低完成度）
        low_completion_days = [
            m["date"] for m in all_metrics 
            if m.get("completion_rate", 1.0) < 0.7
        ]
        if len(low_completion_days) >= 3:
            trends["patterns"].append(
                f"连续 {len(low_completion_days)} 天计划完成度低于 70%：{', '.join(low_completion_days)}"
            )

        # 高会议天数
        high_meeting_days = [
            m["date"] for m in all_metrics 
            if m.get("meeting_hours", 0) > 3.0
        ]
        if len(high_meeting_days) >= 3:
            trends["patterns"].append(
                f"连续 {len(high_meeting_days)} 天会议时间超过 3 小时：{', '.join(high_meeting_days)}"
            )

        return trends

    def generate_trend_report(self, days: int = 7) -> str:
        """生成趋势报告"""
        trends = self.calculate_trends(days)

        if trends["status"] == "insufficient_data":
            return f"""# 📈 趋势报告

> {trends["message"]}

建议连续记录至少 2 天复盘，才能看到趋势。
"""

        md = f"""# 📈 趋势报告 — 最近 {trends["period"]}

> 数据范围：{trends["date_range"]}  
> 复盘天数：{trends["reports_count"]} 天

---

## 平均指标

| 指标 | 平均值 |
|------|--------|
"""

        for key, value in trends["averages"].items():
            label = {
                "completion_rate": "计划完成度",
                "total_work_hours": "总工作时长",
                "meeting_hours": "会议时长",
                "deep_work_hours": "深度工作时长",
                "ok_count": "OK 事项数",
                "problem_count": "问题事项数"
            }.get(key, key)

            if key == "completion_rate":
                md += f"| {label} | {value:.0%} |
"
            else:
                md += f"| {label} | {value:.1f} |
"

        md += """
---

## 📈 进步指标

"""
        if trends["improvements"]:
            for item in trends["improvements"]:
                md += f"- ✅ {item}
"
        else:
            md += "- 暂无显著进步指标
"

        md += """
---

## 📉 退步指标

"""
        if trends["declines"]:
            for item in trends["declines"]:
                md += f"- ❌ {item}
"
        else:
            md += "- 暂无显著退步指标
"

        md += """
---

## 🔄 重复模式

"""
        if trends["patterns"]:
            for item in trends["patterns"]:
                md += f"- ⚠️ {item}
"
        else:
            md += "- 暂无识别出的重复模式
"

        md += """
---

*趋势报告由 Daily Review Skill 生成*
"""

        return md


def main():
    """CLI 入口"""
    tracker = TrendTracker()
    print("Trend Tracker v1.0.0")

    reports = tracker.get_recent_reports(30)
    print(f"Found {len(reports)} reports in the last 30 days")

    if len(reports) >= 2:
        print("
Generating trend report...")
        report = tracker.generate_trend_report(7)
        print(report[:500] + "...")
    else:
        print("Need at least 2 reports to generate trend analysis.")


if __name__ == "__main__":
    main()

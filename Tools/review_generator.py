#!/usr/bin/env python3
"""
Daily Review Generator
生成结构化复盘报告，支持 Markdown 和 YAML 双格式输出
"""

import os
import re
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class ReviewReport:
    """复盘报告数据结构"""
    date: str
    data_sources: List[Dict[str, Any]]
    timeline: List[Dict[str, str]]
    work_items: List[Dict[str, Any]]
    communication_events: List[Dict[str, Any]]
    decisions: List[Dict[str, Any]]
    emotional_signals: List[Dict[str, Any]]
    plan_deviation: List[Dict[str, Any]]
    information_gaps: List[str]

    # 复盘结论
    ok_list: List[Dict[str, str]]
    problem_list: List[Dict[str, str]]
    third_person_view: List[Dict[str, str]]
    root_cause: List[Dict[str, str]]
    tomorrow_suggestions: List[Dict[str, str]]
    trend: Optional[Dict[str, Any]]

    # 元数据
    completion_rate: float
    total_work_hours: float
    meeting_hours: float
    deep_work_hours: float
    version: str = "1.0.0"


class ReviewGenerator:
    """复盘报告生成器"""

    def __init__(self, output_dir: str = "./skills/daily-review/review_history"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_report_id(self, date: str) -> str:
        """生成报告唯一 ID"""
        return f"review_{date}_{hashlib.md5(date.encode()).hexdigest()[:6]}"

    def save_report(self, report: ReviewReport) -> str:
        """保存复盘报告到文件"""
        report_id = self.generate_report_id(report.date)

        # Markdown 格式
        md_path = os.path.join(self.output_dir, f"{report_id}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(self._to_markdown(report))

        # YAML 格式（结构化数据）
        yaml_path = os.path.join(self.output_dir, f"{report_id}.yaml")
        with open(yaml_path, "w", encoding="utf-8") as f:
            f.write(self._to_yaml(report))

        return report_id

    def load_report(self, date: str) -> Optional[ReviewReport]:
        """加载指定日期的复盘报告"""
        report_id = self.generate_report_id(date)
        yaml_path = os.path.join(self.output_dir, f"{report_id}.yaml")

        if not os.path.exists(yaml_path):
            return None

        # 简化版：实际使用时会解析 YAML
        return None

    def list_reports(self, days: int = 30) -> List[str]:
        """列出最近 N 天的复盘报告"""
        reports = []
        for f in os.listdir(self.output_dir):
            if f.endswith(".md") and f.startswith("review_"):
                # 提取日期
                date_str = f.split("_")[1]
                reports.append(date_str)

        reports.sort(reverse=True)
        return reports[:days]

    def _to_markdown(self, report: ReviewReport) -> str:
        """转换为 Markdown 格式"""
        md = f"""# 🪞 每日复盘报告 — {report.date}

> 生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M")}
> 数据来源：{len(report.data_sources)} 类素材
> 计划完成度：{report.completion_rate:.0%}

---

## 01 今日事实（What Happened）

### 时间线摘要
"""

        # 时间线
        for event in report.timeline[:10]:  # 只显示前10条
            md += f"- **{event.get('time', '??:??')}** — {event.get('event', '未知事件')}  
"
            md += f"  [来源：{event.get('source', '未知')}]
"

        md += f"""
### 关键指标
| 指标 | 数值 |
|------|------|
| 总工作时长 | {report.total_work_hours:.1f}h |
| 会议时长 | {report.meeting_hours:.1f}h |
| 深度工作时长 | {report.deep_work_hours:.1f}h |
| 计划完成度 | {report.completion_rate:.0%} |

---

## 02 ✅ OK 清单（What Went Well）

"""

        for i, item in enumerate(report.ok_list, 1):
            md += f"""### {i}. {item.get('behavior', '未命名')}

{item.get('evidence', '无证据')}

**为什么好**：{item.get('why_good', '未说明')}

---
"""

        md += """## 03 ❌ 问题清单（What Went Wrong）

"""

        for i, item in enumerate(report.problem_list, 1):
            md += f"""### {i}. {item.get('behavior', '未命名')}

{item.get('evidence', '无证据')}

**影响**：{item.get('impact', '未说明')}

**建议**：{item.get('suggestion', '未建议')}

---
"""

        md += """## 04 🪞 第三方视角评判（The Mirror）

"""

        for i, item in enumerate(report.third_person_view, 1):
            md += f"""> **观察 {i}**：{item.get('observation', '未观察')}
>
> **解读**：{item.get('interpretation', '未解读')}
>
> **建议**：{item.get('suggestion', '未建议')}

"""

        md += """---

## 05 🔍 根因分析（Root Cause）

"""

        for i, item in enumerate(report.root_cause, 1):
            md += f"""### {i}. {item.get('problem', '未命名问题')}

- **表面原因**：{item.get('surface', '未分析')}
- **深层原因**：{item.get('deep', '未分析')}
- **系统性原因**：{item.get('systemic', '未分析')}

"""

        md += """---

## 06 🎯 明日建议（Actionable）

"""

        for i, item in enumerate(report.tomorrow_suggestions, 1):
            priority = item.get('priority', '中')
            emoji = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(priority, "⚪")
            md += f"""### {emoji} 优先级 {i}（{priority}）

**行动**：{item.get('action', '未指定')}

**时间**：{item.get('time', '未指定')}

**成功标准**：{item.get('success_criteria', '未指定')}

"""

        md += """---

## 07 📈 长期趋势（Trend）

"""

        if report.trend:
            md += f"""### 进步指标
"""
            for item in report.trend.get('improvements', []):
                md += f"- {item}
"

            md += f"""
### 退步指标
"""
            for item in report.trend.get('declines', []):
                md += f"- {item}
"

            md += f"""
### 重复模式
"""
            for item in report.trend.get('patterns', []):
                md += f"- {item}
"
        else:
            md += "> 💡 这是你的第一次复盘。建议连续记录 7 天，才能识别出你的行为模式。
"

        md += """
---

*复盘报告由 Daily Review Skill 生成 | 版本 1.0.0*
"""

        return md

    def _to_yaml(self, report: ReviewReport) -> str:
        """转换为 YAML 格式（简化版）"""
        # 实际使用时会用 pyyaml
        return f"""# 结构化数据 — {report.date}
report:
  date: {report.date}
  version: {report.version}
  metrics:
    completion_rate: {report.completion_rate}
    total_work_hours: {report.total_work_hours}
    meeting_hours: {report.meeting_hours}
    deep_work_hours: {report.deep_work_hours}
  data_sources:
""" + "
".join([f"    - type: {s.get('type', 'unknown')}" for s in report.data_sources])


def main():
    """CLI 入口"""
    generator = ReviewGenerator()
    print("Daily Review Generator v1.0.0")
    print(f"Output directory: {generator.output_dir}")
    print(f"Existing reports: {len(generator.list_reports())}")


if __name__ == "__main__":
    main()

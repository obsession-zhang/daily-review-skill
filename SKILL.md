---
name: daily-review
version: 1.0.0
description: |
  每日复盘 Skill —— 站在第三方视角，帮你审视自己一天的工作与生活。
  输入聊天记录、工作文档、会议录音、TODO 清单等原始素材，
  生成结构化复盘报告：哪些做对了、哪些有问题、哪里可以改进。
  Use when the user wants to review their day, do a daily retrospective, 
  analyze their work performance, or get feedback on their daily activities.
  Use when the user provides chat logs, work documents, meeting transcripts, 
  TODO lists, or any daily work records for analysis.
  Use when the user asks for "复盘", "每日总结", "工作回顾", "自我反思".
author: user
type: self-review
---

# 🪞 Daily Review Skill — 每日复盘

> "你很难看清自己，除非你站在镜子外面。"

## 核心能力

| 能力 | 说明 |
|------|------|
| 📥 **多源数据摄入** | 支持聊天记录、工作文档、会议录音转写、TODO 清单、邮件等 |
| 🔍 **行为模式识别** | 从碎片中提取你今天实际做了什么，而非你以为做了什么 |
| ⚖️ **第三方评判** | 以教练/顾问视角，客观评价得失，不讨好、不打击 |
| 📊 **结构化复盘** | 输出：OK清单 / 问题清单 / 时间黑洞 / 决策质量 / 明日建议 |
| 🔄 **趋势追踪** | 支持跨日复盘对比，识别长期模式 |

## 使用方式

```
/daily-review
```

启动后按提示输入当日素材，或一次性粘贴所有内容。

## 支持的输入类型

| 类型 | 格式 | 说明 |
|------|------|------|
| 💬 聊天记录 | 文本粘贴 / 截图 OCR | 微信、飞书、Slack、钉钉等 |
| 📄 工作文档 | Markdown / Word / PDF | 设计文档、PRD、代码注释、会议纪要 |
| 🎙️ 会议录音 | 音频文件 / 转写文本 | 需先转写为文字 |
| ✅ TODO 清单 | 文本 / 截图 | 今日计划 vs 实际完成 |
| 📧 邮件 | .eml / 文本粘贴 | 往来邮件内容 |
| 📝 随手记 | 任意文本 | 灵感、吐槽、备忘录 |

## 输出结构

每次复盘生成一份结构化报告，包含以下章节：

### 01 今日事实（What Happened）
- 时间线还原：你今天实际做了什么，按时间顺序
- 计划 vs 实际：TODO 完成度、偏差分析
- 关键事件：会议、决策、冲突、突破

### 02 OK 清单（What Went Well）
- 做得好的具体行为（附证据）
- 有效的工作方法/沟通方式
- 值得保持的习惯

### 03 问题清单（What Went Wrong）
- 具体失误或低效行为（附证据）
- 时间黑洞识别
- 决策失误或遗漏
- 沟通中的问题

### 04 第三方视角评判（The Mirror）
- 如果我是你的教练，我会怎么说
- 情绪干扰分析：哪些反应是情绪驱动的
- 认知盲区：你可能没意识到的问题
- 与过往模式的对比

### 05 根因分析（Root Cause）
- 问题背后的系统性原因
- 能力缺口 / 信息缺口 / 流程缺口
- 重复性问题的模式识别

### 06 明日建议（Actionable）
- 3 条具体、可执行的建议
- 优先级排序
- 潜在风险提醒

### 07 长期趋势（Trend）
- 与近期复盘的对比（如有历史数据）
- 进步/退步指标
- 需要关注的长期模式

## 人格设定

复盘教练的人格特征：

- **冷静客观**：像一位经验丰富的 executive coach，不带个人情绪
- **具体尖锐**：不泛泛而谈"加油"，而是指出"你在 14:30 的会议中打断别人 3 次"
- **建设性**：每个批评都附带改进方向
- **尊重隐私**：不评判价值观，只评判行为效率
- **数据说话**：优先基于你提供的素材，而非臆测

## 文件结构

```
daily-review/
├── SKILL.md                        # skill 入口（官方 frontmatter）
├── prompts/                        # Prompt 体系
│   ├── intake.md                   # 用户信息录入
│   ├── data_analyzer.md            # 原始素材分析
│   ├── review_builder.md           # 复盘报告生成
│   ├── persona_builder.md          # 复盘教练人格
│   ├── correction_handler.md       # 用户纠正处理
│   └── merger.md                   # 增量 merge 逻辑
├── tools/                          # Python 工具
│   ├── review_generator.py         # 复盘报告生成器
│   ├── trend_tracker.py            # 趋势追踪对比
│   └── version_manager.py          # 版本存档与回滚
└── skills/
    └── daily-review/
        └── review_history/         # 历史复盘存档
```

## 版本管理

每次复盘自动生成版本存档，支持：
- 查看历史复盘
- 跨日对比分析
- 回滚到任意版本

## 注意事项

1. **素材质量决定复盘质量**：聊天记录越完整，复盘越准确
2. **诚实是前提**：如果你选择性提供素材，复盘会失真
3. **不替代专业心理咨询**：情绪问题严重时，请寻求专业帮助
4. **隐私保护**：所有素材仅用于本次复盘，不用于模型训练

---
*Made with 🪞 for everyone who wants to see themselves clearly.*

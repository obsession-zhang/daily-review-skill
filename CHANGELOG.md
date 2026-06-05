# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-05

### Added
- Initial release of Daily Review Skill
- Multi-source data intake: chat logs, work documents, meeting transcripts, TODO lists, emails, notes
- 7-section structured review report: Facts, OK List, Problem List, Third-Person View, Root Cause, Actionable Suggestions, Trend
- Third-person perspective review by Executive Coach persona (Mirror)
- Trend tracking across multiple days
- Version management with archive and rollback
- Incremental data merge (append mode)
- User correction handling with learning mechanism
- Support for Claude Code, Hermes, OpenClaw, Codex hosts
- One-line install script (`install.sh`)
- Example input and output for product manager scenario
- GitHub Actions for Pages deployment and release
- Issue templates for bug reports and feature requests

### Features
- Evidence-based feedback: every critique comes with source reference
- SMART actionable suggestions
- Privacy protection: all data used only for current review session
- Pattern recognition: identifies recurring issues across days
- Emotional signal detection from text analysis
- Plan deviation analysis (planned vs actual)
- Decision quality assessment
- Communication event analysis

## [Unreleased]

### Planned
- [ ] Web UI for easier material input
- [ ] Audio transcription integration
- [ ] Weekly/Monthly aggregated reports
- [ ] Custom persona configuration
- [ ] Integration with calendar APIs
- [ ] Slack/Discord bot mode
- [ ] Multi-language support (English, Japanese)

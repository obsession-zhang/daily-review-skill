#!/usr/bin/env bash
# Daily Review Skill 安装脚本
# 支持 Claude Code / Hermes / OpenClaw / Codex

set -e

SKILL_NAME="daily-review"
REPO_URL="https://github.com/obsession-zhang/daily-review-skill"

echo "🪞 Installing Daily Review Skill..."

# 检测宿主
if [ -d "$HOME/.claude" ]; then
    TARGET="$HOME/.claude/skills/$SKILL_NAME"
    HOST="Claude Code"
elif [ -d "$HOME/.openclaw" ]; then
    TARGET="$HOME/.openclaw/workspace/skills/$SKILL_NAME"
    HOST="OpenClaw"
elif [ -d "$HOME/.codex" ]; then
    TARGET="$HOME/.codex/skills/$SKILL_NAME"
    HOST="Codex"
elif [ -d "$HOME/.hermes" ]; then
    TARGET="$HOME/.hermes/skills/$SKILL_NAME"
    HOST="Hermes"
else
    echo "❌ Could not detect Agent host. Please manually specify the skills directory."
    echo "   Claude Code: ~/.claude/skills/$SKILL_NAME"
    echo "   OpenClaw:    ~/.openclaw/workspace/skills/$SKILL_NAME"
    echo "   Codex:       ~/.codex/skills/$SKILL_NAME"
    echo "   Hermes:      ~/.hermes/skills/$SKILL_NAME"
    exit 1
fi

echo "   Detected host: $HOST"
echo "   Target: $TARGET"

# 克隆仓库
if [ -d "$TARGET" ]; then
    echo "⚠️  Skill already exists at $TARGET"
    read -p "   Overwrite? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$TARGET"
    else
        echo "   Installation cancelled."
        exit 0
    fi
fi

echo "   Cloning from $REPO_URL..."
git clone "$REPO_URL" "$TARGET"

echo ""
echo "✅ Daily Review Skill installed successfully!"
echo ""
echo "   Usage:"
echo "     /daily-review              # Start a review"
echo "     /daily-review --append     # Append new data"
echo "     /daily-review --trend 7    # View 7-day trend"
echo "     /daily-review --history    # View history"
echo ""
echo "   Next step: Paste your daily materials and get your first review!"

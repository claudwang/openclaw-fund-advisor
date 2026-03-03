#!/bin/bash
# OpenClaw 基金投资顾问 Skill 一键安装脚本

echo "🎯 开始安装 OpenClaw 基金投资顾问 Skill..."
echo ""

# 检查 OpenClaw 安装目录
if [ ! -d "$HOME/.openclaw/skills" ]; then
    echo "❌ OpenClaw 未安装或找不到 skills 目录"
    echo "请先安装 OpenClaw"
    exit 1
fi

# 克隆 Skill
cd "$SKILLS_DIR"
SKILL_DIR="fund-advisor"

if [ -d "$SKILL_DIR" ]; then
    echo "⚠️  Skill 已存在，正在更新..."
    cd "$SKILL_DIR"
    git pull origin main
else
    echo "📥 正在克隆 Skill..."
    git clone https://github.com/claudwang/openclaw-fund-advisor.git "$SKILL_DIR"
fi

echo ""
echo "✅ 安装完成！"
echo ""
echo "📝 使用方法："
echo "1. 编辑持仓文件："
echo "   nano $SKILL_DIR/references/portfolio.md"
echo ""
echo "2. 运行分析："
echo "   cd $SKILL_DIR"
echo "   python3 scripts/fund_recommender.py  # 市场场分析 & 基金推荐"
echo "   python3 scripts/fund_monitor.py     # 组合策略报告"
echo "   python3 scripts/stock_report.py     # A股板块日报"
echo ""
echo "🎮 重启 OpenClaw 使 Skill 生效"

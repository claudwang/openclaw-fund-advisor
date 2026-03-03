---
name: fund-advisor
description: Chinese fund investment advisor with daily analysis, recommendations, and portfolio management. Provides automatic monitoring, buying/selling suggestions, and market reports for Chinese mutual funds and ETFs.
---

# Chinese Fund Investment Advisor

This skill provides comprehensive investment advisory services for Chinese mutual funds and ETFs, including daily market analysis, fund recommendations, and portfolio management.

## Quick Start

### Generate Daily Market Analysis & Recommendations

To get today's fund recommendations and market analysis:

```bash
python3 scripts/fund_recommender.py
```

This script:
- Analyzes market sentiment (positive/neutral/negative)
- Identifies hot investment themes (AI, consumption, new energy, etc.)
- Shows top 10 sector gains
- Recommends top 5 buying funds with detailed analysis:
  - Trend assessment (strong rally/rising/consolidation bullish)
  - Daily average gain
  - Win rate (up days percentage)
  - Recent 5-day performance
  - Maximum drawdown
  - Sector investment logic
- Provides scoring system (0-100 points)
- Includes risk warnings

### Monitor Portfolio & Get Strategy Report

To analyze user's fund portfolio and get action suggestions:

```bash
python3 scripts/fund_monitor.py
```

This script reads `references/portfolio.md` and generates:
- Total portfolio value
- Per-fund performance tracking
- Action suggestions:
  - **Profit taking**: When yield > 15%, suggest selling 50% to lock profits
  - **Replenishment**: When loss 10%-20%, suggest adding 2000-5000 yuan
  - **Stop loss**: When loss > 20%, alert user

### Generate A-Share Sector Report

To get daily A-share sector performance:

```bash
python3 scripts/stock_report.py
```

## User Portfolio Management

The portfolio is stored in `references/portfolio.md`. Format:

```markdown
# 基金持仓

## 持仓明细

- **基金名称 (代码)**: 持仓金额 | 收益率: XX%
```

Example:

```markdown
# 基金持仓

## 持仓明细

- **中欧数字经济混合C (010937)**: 119,042.15 元 | 收益率: +19.03%
- **招商中证香港科技ETF联接C (018110)**: 84,871.40 元 | 收益率: -15.13%
- **广发纳斯达克100ETF联接C (006479)**: 22,030.52 元 | 收益率: +22.40%
```

## Automated Daily Reports via Cron

This skill works with OpenClaw's cron system to send automatic daily reports:

### Example Cron Configuration

```json
{
  "name": "Market Analysis & Fund Recommendations",
  "enabled": true,
  "schedule": {"kind": "cron", "expr": "0 9 * * 1-5", "tz": "Asia/Shanghai"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run python3 scripts/fund_recommender.py to generate market analysis and fund recommendations, then read the output and send to user.",
    "timeoutSeconds": 60
  }
}
```

```json
{
  "name": "Portfolio Strategy Report",
  "enabled": true,
  "schedule": {"kind": "cron", "expr": "0 15 * * 1-5", "tz": "Asia/Shanghai"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run python3 scripts/fund_monitor.py to analyze portfolio and generate strategy suggestions.",
    "timeoutSeconds": 60
  }
}
```

**Note**: Use `sessionTarget: "isolated"` with `payload.kind: "agentTurn"` for script execution. `systemEvent` only injects text and cannot execute scripts.

## Data Sources

All scripts use East Money APIs (eastmoney.com) to fetch:
- Real-time fund net values
- Historical price data
- Sector performance
- Market sentiment

## When to Use This Skill

Use this skill when:
- User asks for fund investment advice
- User wants to monitor their fund portfolio
- User needs daily market analysis
- User requests buying/selling suggestions for their holdings
- User wants sector performance reports

## Risk Warning

This skill provides analysis based on historical data and market trends. 
All investment suggestions are for reference only and do not constitute investment advice. 
Users should make independent decisions based on their own risk tolerance and financial situation.

Historical performance does not guarantee future returns.

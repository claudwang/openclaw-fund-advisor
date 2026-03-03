#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""基金监控和策略提醒脚本"""
import json
import sys
import requests
from datetime import datetime
import re

def get_fund_nav(fund_code):
    """获取基金净值"""
    url = f'https://fundgz.1234567.com.cn/js/{fund_code}.js'
    try:
        response = requests.get(url, timeout=10)
        text = response.text.strip()
        # 解析 JSON 数据：jsonpgz({"fundcode":"010937","name":"中欧数字经济混合C","jzrq":"2026-02-21","dwjz":"1.4334","gsz":"1.4490","gszzl":"1.08"});
        if text.startswith('jsonpgz(') and text.endswith(');'):
            json_str = text[7:-2]
            data = json.loads(json_str)
            return {
                'code': data.get('fundcode'),
                'name': data.get('name'),
                'date': data.get('jzrq'),
                'net_value': float(str(data.get('dwjz', 0) or 0)),
                'estimated_value': float(str(data.get('gsz', 0) or 0)),
                'change_percent': data.get('gszzl', '0')
            }
    except Exception as e:
        print(f"获取基金 {fund_code} 数据失败: {e}", file=sys.stderr)
    return None

def get_portfolio():
    """获取持仓基金列表"""
    return {
        '015790': {'name': '永赢高端装备智选混合C', 'amount': 141060.03, 'return_rate': -5.96},
        '010937': {'name': '中欧数字经济混合C', 'amount': 119042.15, 'return_rate': 19.03},
        '004263': {'name': '德邦稳盈增长灵活配置混合C', 'amount': 92819.55, 'return_rate': -7.18},
        '018110': {'name': '招商中证香港科技ETF联接C', 'amount': 84871.40, 'return_rate': -15.13},
        '016134': {'name': '博时中证卫星产业指数C', 'amount': 46843.57, 'return_rate': -6.31},
        '006479': {'name': '广发纳斯达克100ETF联接C', 'amount': 22030.52, 'return_rate': 22.40}
    }

def analyze_strategy(funds, portfolio):
    """分析交易策略"""
    signals = []
    
    for code, fund_info in portfolio.items():
        return_rate = fund_info.get('return_rate', 0)
        name = fund_info.get('name', '')
        
        # 止盈信号
        if return_rate > 15:
            signals.append({
                'type': 'SELL',
                'code': code,
                'name': name,
                'reason': f'收益已达 {return_rate:.2f}%，建议止盈',
                'action': f'考虑卖出 50% 持仓锁定利润'
            })
        
        # 补仓信号（亏损超过 10% 但未到止损线）
        if return_rate < -10 and return_rate > -20:
            signals.append({
                'type': 'BUY',
                'code': code,
                'name': name,
                'reason': f'亏损 {return_rate:.2f}%，低于成本补仓机会',
                'action': '建议补仓 2000-5000 元'
            })
        
        # 止损信号
        if return_rate < -20:
            signals.append({
                'type': 'STOP_LOSS',
                'code': code,
                'name': name,
                'reason': f'亏损已达 {return_rate:.2f}%，超过止损线',
                'action': '建议止损或观察'
            })
    
    return signals

def main():
    portfolio = get_portfolio()
    
    # 分析策略
    signals = analyze_strategy({}, portfolio)
    
    # 构建消息
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    message = f"📊 基金策略报告 ({now})\n\n"
    
    # 持仓概览
    message += "💼 持仓概览:\n"
    total_amount = sum(f['amount'] for f in portfolio.values())
    message += f"  总持仓: ¥{total_amount:,.2f}\n"
    message += f"  基金数量: {len(portfolio)} 只\n\n"
    
    # 基金详情
    message += "📋 持仓明细:\n"
    for code, info in portfolio.items():
        emoji = "✅" if info['return_rate'] >= 0 else "❌"
        message += f"  {emoji} {info['name']} ({code})\n"
        message += f"     持仓: ¥{info['amount']:,.2f} | 收益: {info['return_rate']:+.2f}%\n"
    
    message += "\n"
    
    # 信号部分
    if signals:
        message += "🎯 操作建议:\n\n"
        for signal in signals:
            if signal['type'] == 'SELL':
                emoji = '📈'
            elif signal['type'] == 'BUY':
                emoji = '📉'
            else:
                emoji = '⚠️'
            
            message += f"{emoji} {signal['name']} ({signal['code']})\n"
            message += f"   理由: {signal['reason']}\n"
            message += f"   建议: {signal['action']}\n\n"
    else:
        message += "✅ 当前无操作建议，持仓状态正常\n\n"
    
    message += "💡 回复 '确认' 或指令来确认操作"
    
    # 保存消息
    output_file = "/tmp/fund_monitor_message.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(message)
    
    print(f"监控消息已保存到: {output_file}")

if __name__ == '__main__':
    main()

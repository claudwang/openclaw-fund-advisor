#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
import requests
from datetime import datetime
import re

def safe_float(value):
    """安全转换为浮点数"""
    try:
        if value is None or value == '-' or value == '':
            return 0.0
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def fetch_sector_data():
    """获取板块数据"""
    url = 'https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=5&po=1&np=1&ut=bd1d9ddb040897&fltt=2&invt=2&fid=f3&fs=m:90+t:2&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('data') and data['data'].get('diff'):
            sectors = []
            for item in data['data']['diff']:
                sectors.append({
                    'name': item.get('f14', ''),
                    'change': safe_float(item.get('f3', 0)),
                    'open': safe_float(item.get('f16', 0)),
                    'high': safe_float(item.get('f17', 0)),
                    'low': safe_float(item.get('f18', 0)),
                    'amount': safe_float(item.get('f4', 0))
                })
            # 按涨幅排序
            sectors.sort(key=lambda x: x['change'], reverse=True)
            return sectors[:5]
        return []
    except Exception as e:
        print(f"获取板块数据失败: {e}", file=sys.stderr)
        return []

def fetch_index_data():
    """获取指数数据"""
    try:
        response = requests.get('https://hq.sinajs.cn/list=sh000001,sz399001,sz399006', timeout=10)
        text = response.text
        
        sh000001 = re.search(r'sh000001="([^"]+)"', text)
        sz399001 = re.search(r'sz399001="([^"]+)"', text)
        sz399006 = re.search(r'sz399006="([^"]+)"', text)
        
        indices = {}
        if sh000001:
            data = sh000001.group(1).split(',')
            indices['上证'] = float(data[2]) if len(data) > 2 else 0
        if sz399001:
            data = sz399001.group(1).split(',')
            indices['深证'] = float(data[2]) if len(data) > 2 else 0
        if sz399006:
            data = sz399006.group(1).split(',')
            indices['创业板'] = float(data[2]) if len(data) > 2 else 0
            
        return indices
    except Exception as e:
        print(f"获取指数数据失败: {e}", file=sys.stderr)
        return {}

def format_change(value):
    """格式化涨跌幅"""
    prefix = '+' if value >= 0 else ''
    return f"{prefix}{value:.2f}%"

def main():
    # 获取数据
    indices = fetch_index_data()
    sectors = fetch_sector_data()
    
    # 构建消息
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    message = f"📊 A股板块涨幅日报 ({now})\n\n"
    
    # 指数部分
    if indices:
        message += "📈 指数表现:\n"
        for name, change in indices.items():
            color = "🔴" if change >= 0 else "🟢"
            message += f"  {color} {name}: {format_change(change)}\n"
        message += "\n"
    
    # 板块部分
    message += "🏆 今日涨幅前五板块:\n"
    for i, sector in enumerate(sectors, 1):
        emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i-1]
        message += f"{emoji} {sector['name']}: {format_change(sector['change'])}\n"
        open_val = float(sector['open']) if sector['open'] else 0
        high_val = float(sector.get('high', 0)) if sector.get('high', 0) else 0
        low_val = float(sector.get('low', 0)) if sector.get('low', 0) else 0
        message += f"   开盘: {open_val:.2f} | 最高: {high_val:.2f} | 最低: {low_val:.2f}\n"
    
    message += "\n"
    message += "🌐 查看详情: https://claudwang.github.io/stock-dashboard/\n"
    message += "\n💡 数据来源: 东方财富网 · 仅供参考，不构成投资建议"
    
    # 保存到文件
    output_file = "/tmp/stock_report_message.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(message)
    
    print(f"消息已保存到: {output_file}")

if __name__ == '__main__':
    main()

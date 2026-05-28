#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_content.py — 2019血疫纪元 网站内容更新程序 (v3)

用法：
  python generate_content.py          # 重新生成 content.js
  python generate_content.py --check  # 仅检查，不写入

Part 结构：
  Part 1: 血疫爆发
  Part 2: 暗影反击
  Part 3: 净域残响
  Part 4: 根系蔓延
"""

import os
import sys
import json
import argparse
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(SCRIPT_DIR, '..')
OUTPUT = os.path.join(SCRIPT_DIR, 'content.js')

PARTS = [
    {'id': 1, 'title': '血疫爆发', 'subtitle': 'The Outbreak', 'desc': '从盖亚之巢启动到X市全面封锁，一场以博览会为伪装的基因武器袭击。'},
    {'id': 2, 'title': '暗影反击', 'subtitle': 'The Counterattack', 'desc': '档案员的逃亡与反击，季风的暗中调查，圣女计划的政治博弈。'},
    {'id': 3, 'title': '净域残响', 'subtitle': 'Residual Signal', 'desc': '真相广播后的重建，内鬼揭露，菌丝复燃，母亲的低语。'},
    {'id': 4, 'title': '根系蔓延', 'subtitle': 'The Spreading Root', 'desc': '全球17城市菌丝危机，Nodus Primus的布道，两个物种的对话。'},
]

ITEMS = [
    # ═══ PART 1: 血疫爆发 ═══
    {'part': 1, 'id': 'setting-b3',     'title': '核心世界观设定',         'section': '世界观',   'type': 'setting', 'file': '幸福里社区3号楼/设定.md'},
    {'part': 1, 'id': 'polaris-intro',  'title': '北极星集团介绍',         'section': '世界观',   'type': 'doc',     'file': '北极星集团介绍.md'},
    {'part': 1, 'id': 'eternity-intro', 'title': '永生树集团介绍',         'section': '世界观',   'type': 'doc',     'file': '永生树集团介绍.md'},
    {'part': 1, 'id': 'polaris-report', 'title': '北极星集团背景审查报告', 'section': '世界观',   'type': 'doc',     'file': '一些报告/北极星集团背景审查报告.md'},
    {'part': 1, 'id': 'origin-01', 'title': '第一章：项目启动',   'section': '起源篇', 'type': 'story', 'file': '起源/01-项目启动.md'},
    {'part': 1, 'id': 'origin-02', 'title': '第二章：泄露事件',   'section': '起源篇', 'type': 'story', 'file': '起源/02-泄露事件.md'},
    {'part': 1, 'id': 'origin-03', 'title': '第三章：彼岸实验室', 'section': '起源篇', 'type': 'story', 'file': '起源/03-彼岸实验室.md'},
    {'part': 1, 'id': 'hotel-ts',  'title': '关键24小时时间轴', 'section': '酒店孤岛', 'type': 'doc',   'file': '酒店孤岛/时间戳.md'},
    {'part': 1, 'id': 'hotel-p1',  'title': 'P1 - 北极星坠落',  'section': '酒店孤岛', 'type': 'story', 'file': '酒店孤岛/P1-北极星坠落.md'},
    {'part': 1, 'id': 'hotel-p2',  'title': 'P2 - 沉默的证据',  'section': '酒店孤岛', 'type': 'story', 'file': '酒店孤岛/P2-沉默的证据.md'},
    {'part': 1, 'id': 'hotel-p3',  'title': 'P3 - 推广品',      'section': '酒店孤岛', 'type': 'story', 'file': '酒店孤岛/P3-推广品 (Promotional Material).md'},
    {'part': 1, 'id': 'b3-hive',     'title': '蜂巢之神',         'section': '幸福里社区3号楼', 'type': 'story', 'file': '幸福里社区3号楼/第一幕 神祇陨落/01_蜂巢之神.md'},
    {'part': 1, 'id': 'b3-survivor', 'title': '档案幸存者',       'section': '幸福里社区3号楼', 'type': 'story', 'file': '幸福里社区3号楼/第一幕 神祇陨落/02_档案幸存者.md'},
    {'part': 1, 'id': 'b3-ghost',    'title': '幽灵的低语',       'section': '幸福里社区3号楼', 'type': 'story', 'file': '幸福里社区3号楼/第二幕 幽灵低语/03_幽灵的低语.md'},
    {'part': 1, 'id': 'b3-escape',   'title': '移动硬盘逃亡计划', 'section': '幸福里社区3号楼', 'type': 'story', 'file': '幸福里社区3号楼/4-移动硬盘逃亡计划.md'},
    {'part': 1, 'id': 'entry-citizen', 'title': '一个市民的视角',     'section': '入城记', 'type': 'story', 'file': '入城记/一个市民的视角.md'},
    {'part': 1, 'id': 'entry-driver',  'title': '一个货车司机的视角', 'section': '入城记', 'type': 'story', 'file': '入城记/一个货车司机的视角.md'},
    {'part': 1, 'id': 'side-manna',  'title': '番外：甘露 (Manna)',          'section': '番外', 'type': 'story', 'file': '番外/番外：甘露 (Manna).md'},
    {'part': 1, 'id': 'side-body',   'title': '番外二：圣体 (The Holy Body)', 'section': '番外', 'type': 'story', 'file': '番外/番外二：圣体 (The Holy Body).md'},
    {'part': 1, 'id': 'side-body2',  'title': '圣体二 (The Holy Body II)',    'section': '番外', 'type': 'story', 'file': '番外/圣体二 (The Holy Body Ⅱ).md'},
    {'part': 1, 'id': 'side-repose', 'title': '番外三：安息 (Repose)',        'section': '番外', 'type': 'story', 'file': '番外/番外三：安息 (Repose).md'},
    {'part': 1, 'id': 'radio-bridge',  'title': '关于大桥事故', 'section': '电台', 'type': 'radio', 'file': '电台/关于大桥事故.md'},
    {'part': 1, 'id': 'radio-traffic', 'title': '交通节目',     'section': '电台', 'type': 'radio', 'file': '电台/交通节目.md'},
    {'part': 1, 'id': 'news-shangbao', 'title': 'X市商报 2019.09.10', 'section': '新闻档案', 'type': 'news', 'date': '2019年9月10日',   'file': '一组商报新闻/《X市商报》 - 2019年9月10日 - 经济版头条.md'},
    {'part': 1, 'id': 'news-chenbao',  'title': 'X市晨报 2019.11.19', 'section': '新闻档案', 'type': 'news', 'date': '2019年11月19日',  'file': '一组晨报新闻/《X市晨报》 - 2019年11月19日 - 第A3版：城市动态.md'},
    {'part': 1, 'id': 'news-wanbao',   'title': 'X市晚报 2019.11.25', 'section': '新闻档案', 'type': 'news', 'date': '2019年11月25日',  'file': '一组晚报新闻/《X市晚报》 - 2019年11月25日 - 头版.md'},
    {'part': 1, 'id': 'diary-wang',  'title': '老王的日记',       'section': '其他', 'type': 'diary', 'file': '老王的日记.md'},
    {'part': 1, 'id': 'notice-01',   'title': '一则最高紧急通知', 'section': '其他', 'type': 'doc',   'file': '一则最高紧急通知.md'},
    {'part': 1, 'id': 'bluedust-ad', 'title': '蓝色星尘 广告',    'section': '其他', 'type': 'ad',    'file': '蓝色星尘/广告.md'},

    # ═══ PART 2: 暗影反击 ═══
    {'part': 2, 'id': 'p2-prologue', 'title': '现在可公开的情报', 'section': '序章', 'type': 'doc', 'file': 'Part2/序章/00-现在可公开的情报.md'},
    {'part': 2, 'id': 'p2-ch1-01', 'title': '城北公园',       'section': '第一章·幸存者', 'type': 'story', 'file': 'Part2/第一章/01-城北公园.md'},
    {'part': 2, 'id': 'p2-ch1-02', 'title': '记忆的重量',     'section': '第一章·幸存者', 'type': 'story', 'file': 'Part2/第一章/02-记忆的重量.md'},
    {'part': 2, 'id': 'p2-ch1-03', 'title': '幽灵的技能',     'section': '第一章·幸存者', 'type': 'story', 'file': 'Part2/第一章/03-幽灵的技能.md'},
    {'part': 2, 'id': 'p2-ch1-04', 'title': '回收队',         'section': '第一章·幸存者', 'type': 'story', 'file': 'Part2/第一章/04-回收队.md'},
    {'part': 2, 'id': 'p2-ch2-01', 'title': '苏醒',           'section': '第二章·觉醒', 'type': 'story', 'file': 'Part2/第二章/01-苏醒.md'},
    {'part': 2, 'id': 'p2-ch2-02', 'title': '白色的房间',     'section': '第二章·觉醒', 'type': 'story', 'file': 'Part2/第二章/02-白色的房间.md'},
    {'part': 2, 'id': 'p2-ch2-03', 'title': '走廊的另一端',   'section': '第二章·觉醒', 'type': 'story', 'file': 'Part2/第二章/03-走廊的另一端.md'},
    {'part': 2, 'id': 'p2-ch2-04', 'title': '碎片与真相',     'section': '第二章·觉醒', 'type': 'story', 'file': 'Part2/第二章/04-碎片与真相.md'},
    {'part': 2, 'id': 'p2-ch3-01', 'title': '记忆的代价',     'section': '第三章·代价', 'type': 'story', 'file': 'Part2/第三章/01-记忆的代价.md'},
    {'part': 2, 'id': 'p2-ch3-02', 'title': '最后的画',       'section': '第三章·代价', 'type': 'story', 'file': 'Part2/第三章/02-最后的画.md'},
    {'part': 2, 'id': 'p2-ch3-03', 'title': '老孙的石头',     'section': '第三章·代价', 'type': 'story', 'file': 'Part2/第三章/03-老孙的石头.md'},
    {'part': 2, 'id': 'p2-ch3-04', 'title': '告别的季节',     'section': '第三章·代价', 'type': 'story', 'file': 'Part2/第三章/04-告别的季节.md'},
    {'part': 2, 'id': 'p2-ch4-01', 'title': '季风的计划',     'section': '第四章·反击', 'type': 'story', 'file': 'Part2/第四章/01-季风的计划.md'},
    {'part': 2, 'id': 'p2-ch4-02', 'title': '逃离',           'section': '第四章·反击', 'type': 'story', 'file': 'Part2/第四章/02-逃离.md'},
    {'part': 2, 'id': 'p2-ch4-03', 'title': '地下网络',       'section': '第四章·反击', 'type': 'story', 'file': 'Part2/第四章/03-地下网络.md'},
    {'part': 2, 'id': 'p2-ch4-04', 'title': '回家',           'section': '第四章·反击', 'type': 'story', 'file': 'Part2/第四章/04-回家.md'},
    {'part': 2, 'id': 'p2-ch5-01', 'title': '真相广播',       'section': '第五章·真相', 'type': 'story', 'file': 'Part2/第五章/01-真相广播.md'},
    {'part': 2, 'id': 'p2-ch5-02', 'title': '周先生',         'section': '第五章·真相', 'type': 'story', 'file': 'Part2/第五章/02-周先生.md'},
    {'part': 2, 'id': 'p2-ch5-03', 'title': '回家',           'section': '第五章·真相', 'type': 'story', 'file': 'Part2/第五章/03-回家.md'},
    {'part': 2, 'id': 'p2-ch5-04', 'title': '画比手机好',     'section': '第五章·真相', 'type': 'story', 'file': 'Part2/第五章/04-画比手机好.md'},
    {'part': 2, 'id': 'p2-side-01', 'title': '陈医生的日记',   'section': '番外·暗影', 'type': 'diary', 'file': 'Part2/番外/01-陈医生的日记.md'},
    {'part': 2, 'id': 'p2-side-02', 'title': '最后的通道',     'section': '番外·暗影', 'type': 'story', 'file': 'Part2/番外/02-最后的通道.md'},
    {'part': 2, 'id': 'p2-side-03', 'title': '清洁工',         'section': '番外·暗影', 'type': 'story', 'file': 'Part2/番外/03-清洁工.md'},
    {'part': 2, 'id': 'p2-side-04', 'title': '灰色的人',       'section': '番外·暗影', 'type': 'story', 'file': 'Part2/番外/04-灰色的人.md'},
    {'part': 2, 'id': 'p2-side-05', 'title': '流浪汉',         'section': '番外·暗影', 'type': 'story', 'file': 'Part2/番外/05-流浪汉.md'},
    {'part': 2, 'id': 'p2-side-06', 'title': '季风',           'section': '番外·暗影', 'type': 'story', 'file': 'Part2/番外/06-季风.md'},

    # ═══ PART 3: 净域残响 ═══
    {'part': 3, 'id': 'p3-prologue-01', 'title': '调查委员会成立',     'section': '序章·残响', 'type': 'doc', 'file': 'Part3/序章/00-调查委员会成立.md'},
    {'part': 3, 'id': 'p3-prologue-02', 'title': 'X市感染区现状报告', 'section': '序章·残响', 'type': 'doc', 'file': 'Part3/序章/01-X市感染区现状报告.md'},
    {'part': 3, 'id': 'p3-ch1-01', 'title': '幸福里的新居民', 'section': '第一章·余波', 'type': 'story', 'file': 'Part3/第一章/01-幸福里的新居民.md'},
    {'part': 3, 'id': 'p3-ch1-02', 'title': '空壳病房',       'section': '第一章·余波', 'type': 'story', 'file': 'Part3/第一章/02-空壳病房.md'},
    {'part': 3, 'id': 'p3-ch1-03', 'title': '回收队的幽灵',   'section': '第一章·余波', 'type': 'story', 'file': 'Part3/第一章/03-回收队的幽灵.md'},
    {'part': 3, 'id': 'p3-ch1-04', 'title': '地下电台',       'section': '第一章·余波', 'type': 'story', 'file': 'Part3/第一章/04-地下电台.md'},
    {'part': 3, 'id': 'p3-ch2-01', 'title': '档案员在听',     'section': '第二章·裂隙', 'type': 'story', 'file': 'Part3/第二章/01-档案员在听.md'},
    {'part': 3, 'id': 'p3-ch2-02', 'title': '韩风的实验室',   'section': '第二章·裂隙', 'type': 'story', 'file': 'Part3/第二章/02-韩风的实验室.md'},
    {'part': 3, 'id': 'p3-ch2-03', 'title': '嫌疑名单',       'section': '第二章·裂隙', 'type': 'doc',   'file': 'Part3/第二章/03-嫌疑名单.md'},
    {'part': 3, 'id': 'p3-ch2-04', 'title': '蓝色残渣',       'section': '第二章·裂隙', 'type': 'story', 'file': 'Part3/第二章/04-蓝色残渣.md'},
    {'part': 3, 'id': 'p3-ch3-01', 'title': '第十一局',       'section': '第三章·内鬼', 'type': 'story', 'file': 'Part3/第三章/01-第十一局.md'},
    {'part': 3, 'id': 'p3-ch3-02', 'title': '被篡改的档案',   'section': '第三章·内鬼', 'type': 'doc',   'file': 'Part3/第三章/02-被篡改的档案.md'},
    {'part': 3, 'id': 'p3-ch3-03', 'title': '旧日影像',       'section': '第三章·内鬼', 'type': 'story', 'file': 'Part3/第三章/03-旧日影像.md'},
    {'part': 3, 'id': 'p3-ch3-04', 'title': '面罩之下',       'section': '第三章·内鬼', 'type': 'story', 'file': 'Part3/第三章/04-面罩之下.md'},
    {'part': 3, 'id': 'p3-ch4-01', 'title': '地下的震动',     'section': '第四章·复燃', 'type': 'story', 'file': 'Part3/第四章/01-地下的震动.md'},
    {'part': 3, 'id': 'p3-ch4-02', 'title': '白色花朵',       'section': '第四章·复燃', 'type': 'story', 'file': 'Part3/第四章/02-白色花朵.md'},
    {'part': 3, 'id': 'p3-ch4-03', 'title': '净化协议2.0',    'section': '第四章·复燃', 'type': 'story', 'file': 'Part3/第四章/03-净化协议2.0.md'},
    {'part': 3, 'id': 'p3-ch4-04', 'title': '母亲的低语',     'section': '第四章·复燃', 'type': 'story', 'file': 'Part3/第四章/04-母亲的低语.md'},
    {'part': 3, 'id': 'p3-ch5-01', 'title': '第二次广播',     'section': '第五章·新生', 'type': 'story', 'file': 'Part3/第五章/01-第二次广播.md'},
    {'part': 3, 'id': 'p3-ch5-02', 'title': '周先生的信',     'section': '第五章·新生', 'type': 'story', 'file': 'Part3/第五章/02-周先生的信.md'},
    {'part': 3, 'id': 'p3-ch5-03', 'title': '告别旧城',       'section': '第五章·新生', 'type': 'story', 'file': 'Part3/第五章/03-告别旧城.md'},
    {'part': 3, 'id': 'p3-ch5-04', 'title': '城市醒来',       'section': '第五章·新生', 'type': 'story', 'file': 'Part3/第五章/04-城市醒来.md'},
    {'part': 3, 'id': 'p3-side-01', 'title': '老赵的十年',   'section': '番外·净域', 'type': 'story', 'file': 'Part3/番外/01-老赵的十年.md'},
    {'part': 3, 'id': 'p3-side-02', 'title': '女儿的来信',   'section': '番外·净域', 'type': 'story', 'file': 'Part3/番外/02-女儿的来信.md'},
    {'part': 3, 'id': 'p3-side-03', 'title': '外卖骑手日记', 'section': '番外·净域', 'type': 'diary', 'file': 'Part3/番外/03-外卖骑手日记.md'},
    {'part': 3, 'id': 'p3-side-04', 'title': '韩风的笔记',   'section': '番外·净域', 'type': 'doc',   'file': 'Part3/番外/04-韩风的笔记.md'},

    # ═══ PART 4: 根系蔓延 ═══
    {'part': 4, 'id': 'p4-prologue-01', 'title': '全球菌丝监测网络异常报告', 'section': '序章·沉睡的根', 'type': 'doc',  'file': 'Part4/序章/00-全球菌丝监测网络异常报告.md'},
    {'part': 4, 'id': 'p4-prologue-02', 'title': '柏林地铁事件',           'section': '序章·沉睡的根', 'type': 'news', 'file': 'Part4/序章/01-柏林地铁事件.md'},
    {'part': 4, 'id': 'p4-ch1-01', 'title': '幸福里的两年后', 'section': '第一章·裂土', 'type': 'story', 'file': 'Part4/第一章/01-幸福里的两年后.md'},
    {'part': 4, 'id': 'p4-ch1-02', 'title': '地下50米',       'section': '第一章·裂土', 'type': 'story', 'file': 'Part4/第一章/02-地下50米.md'},
    {'part': 4, 'id': 'p4-ch1-03', 'title': 'K-8的噩梦',     'section': '第一章·裂土', 'type': 'story', 'file': 'Part4/第一章/03-K-8的噩梦.md'},
    {'part': 4, 'id': 'p4-ch1-04', 'title': '来自柏林的电话', 'section': '第一章·裂土', 'type': 'story', 'file': 'Part4/第一章/04-来自柏林的电话.md'},
    {'part': 4, 'id': 'p4-ch2-01', 'title': 'Nodus Primus的布道', 'section': '第二章·新芽', 'type': 'story', 'file': 'Part4/第二章/01-Nodus Primus的布道.md'},
    {'part': 4, 'id': 'p4-ch2-02', 'title': '圣女再现',           'section': '第二章·新芽', 'type': 'story', 'file': 'Part4/第二章/02-圣女再现.md'},
    {'part': 4, 'id': 'p4-ch2-03', 'title': '第三种人',           'section': '第二章·新芽', 'type': 'doc',   'file': 'Part4/第二章/03-第三种人.md'},
    {'part': 4, 'id': 'p4-ch2-04', 'title': '周小雨的画',         'section': '第二章·新芽', 'type': 'story', 'file': 'Part4/第二章/04-周小雨的画.md'},
    {'part': 4, 'id': 'p4-ch3-01', 'title': '全球同步',     'section': '第三章·连根', 'type': 'doc',   'file': 'Part4/第三章/01-全球同步.md'},
    {'part': 4, 'id': 'p4-ch3-02', 'title': 'X市的震动',    'section': '第三章·连根', 'type': 'story', 'file': 'Part4/第三章/02-X市的震动.md'},
    {'part': 4, 'id': 'p4-ch3-03', 'title': '桥梁的选择',   'section': '第三章·连根', 'type': 'story', 'file': 'Part4/第三章/03-桥梁的选择.md'},
    {'part': 4, 'id': 'p4-ch3-04', 'title': '季风的赌注',   'section': '第三章·连根', 'type': 'story', 'file': 'Part4/第三章/04-季风的赌注.md'},
    {'part': 4, 'id': 'p4-ch4-01', 'title': '母亲回来了',   'section': '第四章·觉醒', 'type': 'story', 'file': 'Part4/第四章/01-母亲回来了.md'},
    {'part': 4, 'id': 'p4-ch4-02', 'title': '防空洞深处',   'section': '第四章·觉醒', 'type': 'story', 'file': 'Part4/第四章/02-防空洞深处.md'},
    {'part': 4, 'id': 'p4-ch4-03', 'title': '第19.3号协议', 'section': '第四章·觉醒', 'type': 'doc',   'file': 'Part4/第四章/03-第19.3号协议.md'},
    {'part': 4, 'id': 'p4-ch4-04', 'title': '甘露的代价',   'section': '第四章·觉醒', 'type': 'story', 'file': 'Part4/第四章/04-甘露的代价.md'},
    {'part': 4, 'id': 'p4-ch5-01', 'title': '第二次净化',   'section': '第五章·分水岭', 'type': 'story', 'file': 'Part4/第五章/01-第二次净化.md'},
    {'part': 4, 'id': 'p4-ch5-02', 'title': 'K-8的回答',    'section': '第五章·分水岭', 'type': 'story', 'file': 'Part4/第五章/02-K-8的回答.md'},
    {'part': 4, 'id': 'p4-ch5-03', 'title': '根与枝',       'section': '第五章·分水岭', 'type': 'story', 'file': 'Part4/第五章/03-根与枝.md'},
    {'part': 4, 'id': 'p4-ch5-04', 'title': '新世界的黎明', 'section': '第五章·分水岭', 'type': 'story', 'file': 'Part4/第五章/04-新世界的黎明.md'},
    {'part': 4, 'id': 'p4-side-01', 'title': 'Mueller的日记',     'section': '番外·根系', 'type': 'diary', 'file': 'Part4/番外/01-Mueller的日记.md'},
    {'part': 4, 'id': 'p4-side-02', 'title': '空壳患者的梦',     'section': '番外·根系', 'type': 'story', 'file': 'Part4/番外/02-空壳患者的梦.md'},
    {'part': 4, 'id': 'p4-side-03', 'title': '全球节点通讯录',   'section': '番外·根系', 'type': 'doc',   'file': 'Part4/番外/03-全球节点通讯录.md'},
    {'part': 4, 'id': 'p4-side-04', 'title': '李明给儿子的信',   'section': '番外·根系', 'type': 'story', 'file': 'Part4/番外/04-李明给儿子的信.md'},
]

SECTIONS_ORDER = {
    1: ['世界观', '起源篇', '酒店孤岛', '幸福里社区3号楼', '入城记', '电台', '新闻档案', '其他', '番外'],
    2: ['序章', '第一章·幸存者', '第二章·觉醒', '第三章·代价', '第四章·反击', '第五章·真相', '番外·暗影'],
    3: ['序章·残响', '第一章·余波', '第二章·裂隙', '第三章·内鬼', '第四章·复燃', '第五章·新生', '番外·净域'],
    4: ['序章·沉睡的根', '第一章·裂土', '第二章·新芽', '第三章·连根', '第四章·觉醒', '第五章·分水岭', '番外·根系'],
}

DEFAULT_OPEN = {'起源篇', '序章', '序章·残响', '序章·沉睡的根'}


def read_content(item):
    if item.get('file') is None:
        return None
    fpath = os.path.join(ROOT, item['file'])
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"  [WARN] {item['file']}", file=sys.stderr)
        return ''
    except Exception as e:
        print(f"  [ERROR] {item['file']}: {e}", file=sys.stderr)
        return ''


def generate(check_only=False):
    print(f"源目录: {ROOT}")
    print(f"输出:   {OUTPUT}")
    pc = {p: sum(1 for i in ITEMS if i['part']==p) for p in [1,2,3,4]}
    print(f"条目数: {len(ITEMS)} (P1:{pc[1]} P2:{pc[2]} P3:{pc[3]} P4:{pc[4]})")
    print()

    ok, warn, placeholder = 0, 0, 0
    for item in ITEMS:
        content = read_content(item)
        item['content'] = content
        if content is None:
            item['empty'] = True
            item['content'] = ''
            placeholder += 1
            print(f"  [占位] {item['title']}")
        elif content:
            ok += 1
            print(f"  OK  {item.get('file','?')} ({len(content)} chars)")
        else:
            warn += 1

    print(f"\n读取完成: {ok} 成功, {warn} 失败, {placeholder} 占位")

    if check_only:
        print("检查完成（未写入文件）")
        return

    def build_sections(items, order):
        si = {}
        for item in items:
            sec = item['section']
            if sec not in si:
                si[sec] = []
            si[sec].append(item)
        result = []
        for sec in order:
            if sec not in si:
                continue
            result.append({
                'title': sec,
                'open': sec in DEFAULT_OPEN,
                'items': [{'id': i['id'], 'title': i['title'], 'type': i['type'], 'empty': i.get('empty', False)} for i in si[sec]]
            })
        return result

    js = []
    js.append(f'// Auto-generated by generate_content.py v3 — {len(ITEMS)} pieces')
    js.append(f'// Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    js.append('')
    js.append('const PARTS = ' + json.dumps(PARTS, ensure_ascii=False, indent=2) + ';')
    js.append('')
    js.append('const CONTENT_SECTIONS = {')
    for p in [1, 2, 3, 4]:
        pi = [i for i in ITEMS if i['part'] == p]
        comma = ',' if p < 4 else ''
        js.append(f'  {p}: ' + json.dumps(build_sections(pi, SECTIONS_ORDER[p]), ensure_ascii=False, indent=4) + comma)
    js.append('};')
    js.append('')
    js.append('const CONTENT_DATA = [')
    for item in ITEMS:
        js.append('  {')
        js.append(f'    id: {json.dumps(item["id"], ensure_ascii=False)},')
        js.append(f'    title: {json.dumps(item["title"], ensure_ascii=False)},')
        js.append(f'    section: {json.dumps(item["section"], ensure_ascii=False)},')
        js.append(f'    type: {json.dumps(item["type"], ensure_ascii=False)},')
        js.append(f'    part: {item["part"]},')
        if item.get('chapter'):
            js.append(f'    chapter: {json.dumps(item["chapter"], ensure_ascii=False)},')
        if item.get('date'):
            js.append(f'    date: {json.dumps(item["date"], ensure_ascii=False)},')
        if item.get('empty'):
            js.append('    empty: true,')
        js.append(f'    content: {json.dumps(item["content"], ensure_ascii=False)}')
        js.append('  },')
    js.append('];')

    output = '\n'.join(js)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(output)

    size_kb = os.path.getsize(OUTPUT) / 1024
    print(f"\n生成完成: {OUTPUT} ({size_kb:.1f} KB)")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='2019血疫纪元 内容更新程序 v3')
    parser.add_argument('--check', action='store_true', help='仅检查，不写入')
    args = parser.parse_args()
    generate(check_only=args.check)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_content.py — 2019血疫纪元 网站内容更新程序 (v2)

用法：
  python generate_content.py          # 重新生成 content.js
  python generate_content.py --check  # 仅检查，不写入

添加新内容：
  1. 在对应目录下创建 .md 文件
  2. 在下方 ITEMS 列表中添加条目
  3. 运行本脚本

Part 结构：
  Part 1: 血疫爆发 — 已完成的全部内容
  Part 2: 暗影反击 — 调查、生存与反击（章节框架已就位）
"""

import os
import sys
import json
import argparse
from datetime import datetime

# ===== 路径 =====
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(SCRIPT_DIR, '..')
OUTPUT = os.path.join(SCRIPT_DIR, 'content.js')

# ===== Part 元数据 =====
PARTS = [
    {'id': 1, 'title': '血疫爆发', 'subtitle': 'The Outbreak', 'desc': '从盖亚之巢启动到X市全面封锁，一场以博览会为伪装的基因武器袭击。'},
    {'id': 2, 'title': '暗影反击', 'subtitle': 'The Counterattack', 'desc': '档案员的逃亡与反击，季风的暗中调查，圣女计划的政治博弈。'},
]

# ===== 内容条目 =====
# part: 所属部分 (1 或 2)
# id:   唯一标识符
# title: 显示标题
# section: 所属分区（侧边栏分组）
# type: story/doc/news/radio/diary/setting/ad/bbs
# file: 相对于 ROOT 的文件路径（None 表示占位）
# chapter: Part 2 的章节编号（如 "第一章"）

ITEMS = [
    # ═══════════════════════════════════════════════════
    #  PART 1: 血疫爆发
    # ═══════════════════════════════════════════════════

    # ── 世界观 ──
    {'part': 1, 'id': 'setting-b3',     'title': '核心世界观设定',         'section': '世界观',   'type': 'setting', 'file': '幸福里社区3号楼/设定.md'},
    {'part': 1, 'id': 'polaris-intro',  'title': '北极星集团介绍',         'section': '世界观',   'type': 'doc',     'file': '北极星集团介绍.md'},
    {'part': 1, 'id': 'eternity-intro', 'title': '永生树集团介绍',         'section': '世界观',   'type': 'doc',     'file': '永生树集团介绍.md'},
    {'part': 1, 'id': 'polaris-report', 'title': '北极星集团背景审查报告', 'section': '世界观',   'type': 'doc',     'file': '一些报告/北极星集团背景审查报告.md'},

    # ── 起源篇 ──
    {'part': 1, 'id': 'origin-01', 'title': '第一章：项目启动',   'section': '起源篇', 'type': 'story', 'file': '起源/01-项目启动.md'},
    {'part': 1, 'id': 'origin-02', 'title': '第二章：泄露事件',   'section': '起源篇', 'type': 'story', 'file': '起源/02-泄露事件.md'},
    {'part': 1, 'id': 'origin-03', 'title': '第三章：彼岸实验室', 'section': '起源篇', 'type': 'story', 'file': '起源/03-彼岸实验室.md'},

    # ── 酒店孤岛 ──
    {'part': 1, 'id': 'hotel-ts',  'title': '关键24小时时间轴', 'section': '酒店孤岛', 'type': 'doc',   'file': '酒店孤岛/时间戳.md'},
    {'part': 1, 'id': 'hotel-p1',  'title': 'P1 - 北极星坠落',  'section': '酒店孤岛', 'type': 'story', 'file': '酒店孤岛/P1-北极星坠落.md'},
    {'part': 1, 'id': 'hotel-p2',  'title': 'P2 - 沉默的证据',  'section': '酒店孤岛', 'type': 'story', 'file': '酒店孤岛/P2-沉默的证据.md'},
    {'part': 1, 'id': 'hotel-p3',  'title': 'P3 - 推广品',      'section': '酒店孤岛', 'type': 'story', 'file': '酒店孤岛/P3-推广品 (Promotional Material).md'},

    # ── 幸福里社区3号楼 ──
    {'part': 1, 'id': 'b3-hive',     'title': '蜂巢之神',         'section': '幸福里社区3号楼', 'type': 'story', 'file': '幸福里社区3号楼/第一幕 神祇陨落/01_蜂巢之神.md'},
    {'part': 1, 'id': 'b3-survivor', 'title': '档案幸存者',       'section': '幸福里社区3号楼', 'type': 'story', 'file': '幸福里社区3号楼/第一幕 神祇陨落/02_档案幸存者.md'},
    {'part': 1, 'id': 'b3-ghost',    'title': '幽灵的低语',       'section': '幸福里社区3号楼', 'type': 'story', 'file': '幸福里社区3号楼/第二幕 幽灵低语/03_幽灵的低语.md'},
    {'part': 1, 'id': 'b3-escape',   'title': '移动硬盘逃亡计划', 'section': '幸福里社区3号楼', 'type': 'story', 'file': '幸福里社区3号楼/4-移动硬盘逃亡计划.md'},

    # ── 入城记 ──
    {'part': 1, 'id': 'entry-citizen', 'title': '一个市民的视角',     'section': '入城记', 'type': 'story', 'file': '入城记/一个市民的视角.md'},
    {'part': 1, 'id': 'entry-driver',  'title': '一个货车司机的视角', 'section': '入城记', 'type': 'story', 'file': '入城记/一个货车司机的视角.md'},

    # ── 番外 ──
    {'part': 1, 'id': 'side-manna',  'title': '番外：甘露 (Manna)',          'section': '番外', 'type': 'story', 'file': '番外/番外：甘露 (Manna).md'},
    {'part': 1, 'id': 'side-body',   'title': '番外二：圣体 (The Holy Body)', 'section': '番外', 'type': 'story', 'file': '番外/番外二：圣体 (The Holy Body).md'},
    {'part': 1, 'id': 'side-body2',  'title': '圣体二 (The Holy Body II)',    'section': '番外', 'type': 'story', 'file': '番外/圣体二 (The Holy Body Ⅱ).md'},
    {'part': 1, 'id': 'side-repose', 'title': '番外三：安息 (Repose)',        'section': '番外', 'type': 'story', 'file': '番外/番外三：安息 (Repose).md'},

    # ── 电台 ──
    {'part': 1, 'id': 'radio-bridge',  'title': '关于大桥事故', 'section': '电台', 'type': 'radio', 'file': '电台/关于大桥事故.md'},
    {'part': 1, 'id': 'radio-traffic', 'title': '交通节目',     'section': '电台', 'type': 'radio', 'file': '电台/交通节目.md'},

    # ── 新闻档案 ──
    {'part': 1, 'id': 'news-shangbao', 'title': 'X市商报 2019.09.10', 'section': '新闻档案', 'type': 'news', 'date': '2019年9月10日',   'file': '一组商报新闻/《X市商报》 - 2019年9月10日 - 经济版头条.md'},
    {'part': 1, 'id': 'news-chenbao',  'title': 'X市晨报 2019.11.19', 'section': '新闻档案', 'type': 'news', 'date': '2019年11月19日',  'file': '一组晨报新闻/《X市晨报》 - 2019年11月19日 - 第A3版：城市动态.md'},
    {'part': 1, 'id': 'news-wanbao',   'title': 'X市晚报 2019.11.25', 'section': '新闻档案', 'type': 'news', 'date': '2019年11月25日',  'file': '一组晚报新闻/《X市晚报》 - 2019年11月25日 - 头版.md'},

    # ── 其他 ──
    {'part': 1, 'id': 'diary-wang',  'title': '老王的日记',       'section': '其他', 'type': 'diary', 'file': '老王的日记.md'},
    {'part': 1, 'id': 'notice-01',   'title': '一则最高紧急通知', 'section': '其他', 'type': 'doc',   'file': '一则最高紧急通知.md'},
    {'part': 1, 'id': 'bluedust-ad', 'title': '蓝色星尘 广告',    'section': '其他', 'type': 'ad',    'file': '蓝色星尘/广告.md'},

    # ═══════════════════════════════════════════════════
    #  PART 2: 暗影反击
    #  章节框架 — file=None 为占位，写好后填入路径
    # ═══════════════════════════════════════════════════

    # ── 第一章：幸存者 ──
    {'part': 2, 'id': 'p2-ch1-01', 'title': '城北公园',       'section': '第一章·幸存者', 'type': 'story', 'chapter': '第一章', 'file': 'Part2/第一章/01-城北公园.md'},
    {'part': 2, 'id': 'p2-ch1-02', 'title': '记忆的重量',     'section': '第一章·幸存者', 'type': 'story', 'chapter': '第一章', 'file': 'Part2/第一章/02-记忆的重量.md'},
    {'part': 2, 'id': 'p2-ch1-03', 'title': '幽灵的技能',     'section': '第一章·幸存者', 'type': 'story', 'chapter': '第一章', 'file': 'Part2/第一章/03-幽灵的技能.md'},
    {'part': 2, 'id': 'p2-ch1-04', 'title': '回收队',         'section': '第一章·幸存者', 'type': 'story', 'chapter': '第一章', 'file': None},

    # ── 第二章：暗网 ──
    {'part': 2, 'id': 'p2-ch2-01', 'title': '地下防空洞',     'section': '第二章·暗网', 'type': 'story', 'chapter': '第二章', 'file': None},
    {'part': 2, 'id': 'p2-ch2-02', 'title': '季风的眼线',     'section': '第二章·暗网', 'type': 'story', 'chapter': '第二章', 'file': None},
    {'part': 2, 'id': 'p2-ch2-03', 'title': '蓝色星尘的源头', 'section': '第二章·暗网', 'type': 'story', 'chapter': '第二章', 'file': None},
    {'part': 2, 'id': 'p2-ch2-04', 'title': '数据交易',       'section': '第二章·暗网', 'type': 'story', 'chapter': '第二章', 'file': None},

    # ── 第三章：圣女 ──
    {'part': 2, 'id': 'p2-ch3-01', 'title': '安全屋的日与夜', 'section': '第三章·圣女', 'type': 'story', 'chapter': '第三章', 'file': None},
    {'part': 2, 'id': 'p2-ch3-02', 'title': '甘露的代价',     'section': '第三章·圣女', 'type': 'story', 'chapter': '第三章', 'file': None},
    {'part': 2, 'id': 'p2-ch3-03', 'title': '第七工作组',     'section': '第三章·圣女', 'type': 'story', 'chapter': '第三章', 'file': None},
    {'part': 2, 'id': 'p2-ch3-04', 'title': '叛逃者',         'section': '第三章·圣女', 'type': 'story', 'chapter': '第三章', 'file': None},

    # ── 第四章：真相 ──
    {'part': 2, 'id': 'p2-ch4-01', 'title': '档案员的广播',   'section': '第四章·真相', 'type': 'story', 'chapter': '第四章', 'file': None},
    {'part': 2, 'id': 'p2-ch4-02', 'title': '137个名字',      'section': '第四章·真相', 'type': 'story', 'chapter': '第四章', 'file': None},
    {'part': 2, 'id': 'p2-ch4-03', 'title': '永生树的回应',   'section': '第四章·真相', 'type': 'story', 'chapter': '第四章', 'file': None},
    {'part': 2, 'id': 'p2-ch4-04', 'title': '盖亚的低语',     'section': '第四章·真相', 'type': 'story', 'chapter': '第四章', 'file': None},

    # ── 第五章：反击 ──
    {'part': 2, 'id': 'p2-ch5-01', 'title': '集结',           'section': '第五章·反击', 'type': 'story', 'chapter': '第五章', 'file': None},
    {'part': 2, 'id': 'p2-ch5-02', 'title': '渗透',           'section': '第五章·反击', 'type': 'story', 'chapter': '第五章', 'file': None},
    {'part': 2, 'id': 'p2-ch5-03', 'title': '母体的心脏',     'section': '第五章·反击', 'type': 'story', 'chapter': '第五章', 'file': None},
    {'part': 2, 'id': 'p2-ch5-04', 'title': '新的纪元',       'section': '第五章·反击', 'type': 'story', 'chapter': '第五章', 'file': None},

    # ── Part 2 番外 ──
    {'part': 2, 'id': 'p2-side-01', 'title': '番外四：园丁 (The Gardener)',  'section': '番外·续', 'type': 'story', 'file': None},
    {'part': 2, 'id': 'p2-side-02', 'title': '番外五：第一节点 (Nodus Primus)', 'section': '番外·续', 'type': 'story', 'file': None},
]

# ── 侧边栏分区顺序 ──
SECTIONS_ORDER_P1 = ['世界观', '起源篇', '酒店孤岛', '幸福里社区3号楼', '入城记', '电台', '新闻档案', '其他', '番外']
SECTIONS_ORDER_P2 = ['第一章·幸存者', '第二章·暗网', '第三章·圣女', '第四章·真相', '第五章·反击', '番外·续']

DEFAULT_OPEN = {'起源篇', '第一章·幸存者'}


def read_content(item):
    """读取单个 Markdown 文件"""
    if item.get('file') is None:
        return None  # 占位条目
    fpath = os.path.join(ROOT, item['file'])
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"  [WARN] 文件不存在: {item['file']}", file=sys.stderr)
        return ''
    except Exception as e:
        print(f"  [ERROR] {item['file']}: {e}", file=sys.stderr)
        return ''


def generate(check_only=False):
    """生成 content.js"""
    print(f"源目录: {ROOT}")
    print(f"输出:   {OUTPUT}")
    print(f"条目数: {len(ITEMS)} (Part 1: {sum(1 for i in ITEMS if i['part']==1)}, Part 2: {sum(1 for i in ITEMS if i['part']==2)})")
    print()

    # 读取内容
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
            print(f"  OK  {item.get('file', '?')} ({len(content)} chars)")
        else:
            warn += 1

    print(f"\n读取完成: {ok} 成功, {warn} 失败, {placeholder} 占位")

    if check_only:
        print("检查完成（未写入文件）")
        return

    # 按 Part + 分区组织
    def build_sections(items, order):
        section_items = {}
        for item in items:
            sec = item['section']
            if sec not in section_items:
                section_items[sec] = []
            section_items[sec].append(item)
        result = []
        for sec in order:
            if sec not in section_items:
                continue
            result.append({
                'title': sec,
                'open': sec in DEFAULT_OPEN,
                'items': [{'id': i['id'], 'title': i['title'], 'type': i['type'], 'empty': i.get('empty', False)} for i in section_items[sec]]
            })
        return result

    p1_items = [i for i in ITEMS if i['part'] == 1]
    p2_items = [i for i in ITEMS if i['part'] == 2]

    # 生成 JS
    js = []
    js.append(f'// Auto-generated by generate_content.py v2 — {len(ITEMS)} pieces')
    js.append(f'// Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    js.append('')

    # Parts metadata
    js.append('const PARTS = ' + json.dumps(PARTS, ensure_ascii=False, indent=2) + ';')
    js.append('')

    # Sections
    js.append('const CONTENT_SECTIONS = {')
    js.append('  1: ' + json.dumps(build_sections(p1_items, SECTIONS_ORDER_P1), ensure_ascii=False, indent=4) + ',')
    js.append('  2: ' + json.dumps(build_sections(p2_items, SECTIONS_ORDER_P2), ensure_ascii=False, indent=4))
    js.append('};')
    js.append('')

    # Content data
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
    parser = argparse.ArgumentParser(description='2019血疫纪元 内容更新程序 v2')
    parser.add_argument('--check', action='store_true', help='仅检查，不写入')
    args = parser.parse_args()
    generate(check_only=args.check)

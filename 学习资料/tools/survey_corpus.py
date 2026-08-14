# -*- coding: utf-8 -*-
"""盘点紫微斗数语料库：统计每个 PDF 的页数与文字可提取性。"""
import os
import sys
import pymupdf

ROOTS = [
    r"E:\52.王亭之紫微斗数6本全集",
]

def survey(root, max_depth=1):
    """只扫 root 根层 + 一层子目录，避开八字/风水等非紫微内容时按名称过滤。"""
    rows = []
    for dirpath, dirnames, filenames in os.walk(root):
        depth = os.path.relpath(dirpath, root).count(os.sep)
        if os.path.relpath(dirpath, root) != '.':
            depth += 1
        # 排除隐藏目录
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        for fn in sorted(filenames):
            if not fn.lower().endswith('.pdf'):
                continue
            p = os.path.join(dirpath, fn)
            try:
                doc = pymupdf.open(p)
                pages = doc.page_count
                # 抽样检测文字：取前3页、中间1页、最后1页
                sample_idx = sorted(set([0, pages // 2, pages - 1, min(2, pages - 1)]))
                total_chars = 0
                for i in sample_idx:
                    try:
                        total_chars += len(doc[i].get_text().strip())
                    except Exception:
                        pass
                avg = total_chars / max(1, len(sample_idx))
                kind = "文字版" if avg > 80 else ("疑似扫描" if avg > 10 else "纯扫描/图片")
                doc.close()
            except Exception as e:
                pages, avg, kind = -1, 0, f"读取失败:{type(e).__name__}"
            rel = os.path.relpath(p, root)
            rows.append((rel, pages, round(avg), kind))
    return rows

if __name__ == '__main__':
    for root in ROOTS:
        print(f"=== ROOT: {root} ===")
        for rel, pages, avg, kind in survey(root):
            # 只看紫微相关：路径含“紫微/斗数/紫薇/王亭之/中州”或在根层
            name = rel.replace('\\', '/')
            top = name.split('/')[0]
            ziwei_related = any(k in name for k in ('紫微', '紫薇', '斗数', '斗數', '王亭之', '中州', '斗shu'))
            in_root = '/' not in name
            if not (ziwei_related or in_root):
                continue
            print(f"{pages:>5}页 | {kind:<8} | 样本均{avg:>4}字 | {name}")

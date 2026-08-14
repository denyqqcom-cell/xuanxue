# -*- coding: utf-8 -*-
"""把文字版 PDF 抽取为 Markdown 文本，供后续阅读学习。"""
import os
import pymupdf

BASE = r"E:\52.王亭之紫微斗数6本全集"
OUT = os.path.join(BASE, "紫微", ".学习工作区", "提取文本")
os.makedirs(OUT, exist_ok=True)

BOOKS = [
    r"斗數全書.pdf",
    r"紫微入門(1).pdf",
]

def extract(rel):
    src = os.path.join(BASE, rel)
    name = os.path.splitext(os.path.basename(rel))[0]
    dst = os.path.join(OUT, name + ".md")
    doc = pymupdf.open(src)
    parts = [f"# {name}\n\n> 来源：{rel}，共 {doc.page_count} 页\n"]
    for i, page in enumerate(doc):
        t = page.get_text().strip()
        parts.append(f"\n## 第{i+1}页\n\n{t if t else '（本页无可提取文字）'}\n")
    doc.close()
    with open(dst, 'w', encoding='utf-8') as f:
        f.write("\n".join(parts))
    print(f"OK {dst} ({os.path.getsize(dst)//1024}KB)")

for b in BOOKS:
    extract(b)

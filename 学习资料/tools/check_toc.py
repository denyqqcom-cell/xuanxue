# -*- coding: utf-8 -*-
"""检查六本全集扫描版前12页是否存在可提取文字（如目录）。"""
import os
import pymupdf

BASE = r"E:\52.王亭之紫微斗数6本全集"
vols = [
    ("一", r"紫微斗数全集（一）王亭之编著  254P.pdf"),
    ("二", r"紫微斗数全集（二）王亭之编著  280P.pdf"),
    ("三", r"紫微斗数全集（三）王亭之编著  404P.pdf"),
    ("四", r"紫微斗数全集（四）王亭之编著  428P.pdf"),
    ("五", r"紫微斗数全集（五）王亭之编著  212P.pdf"),
    ("六", r"紫微斗数全集（六）王亭之编著  300P.pdf"),
]

for tag, rel in vols:
    p = os.path.join(BASE, rel)
    doc = pymupdf.open(p)
    print(f"\n===== 全集（{tag}）共{doc.page_count}页 =====")
    found_any = False
    for i in range(min(12, doc.page_count)):
        t = doc[i].get_text().strip()
        if len(t) > 20:
            found_any = True
            print(f"--- 第{i+1}页 ({len(t)}字) ---")
            print(t[:500])
    if not found_any:
        print("前12页均无可提取文字，目录需 OCR")
    doc.close()

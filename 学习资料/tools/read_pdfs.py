# -*- coding: utf-8 -*-
import pdfplumber
import json

def read_pdf_content(pdf_path, start_page=0, end_page=30):
    """读取PDF指定页码范围的内容"""
    results = {}
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        results['total_pages'] = total_pages
        results['pages'] = []
        
        end = min(end_page, total_pages)
        for i in range(start_page, end):
            text = pdf.pages[i].extract_text()
            if text:
                results['pages'].append({
                    'page_num': i + 1,
                    'content': text
                })
    
    return results

# 读取《金函玉镜》上册 - 目录和基础理论部分
print("=" * 60)
print("《金函玉镜奇门遁甲秘笈全书》上册")
print("=" * 60)

pdf_path1 = "F:/奇门遁甲/《金函玉镜奇门遁甲秘笈全书(上)》诸葛亮.pdf"
result1 = read_pdf_content(pdf_path1, 0, 25)
print(f"总页数: {result1['total_pages']}")

for page in result1['pages'][:15]:
    print(f"\n--- 第{page['page_num']}页 ---")
    content = page['content'].replace('\n', '\n')
    print(content[:800] if len(content) > 800 else content)

# 读取《金函玉镜》下册 - 格局和解盘部分
print("\n\n" + "=" * 60)
print("《金函玉镜奇门遁甲秘笈全书》下册")
print("=" * 60)

pdf_path2 = "F:/奇门遁甲/《金函玉镜奇门遁甲秘笈全书(下)》诸葛亮.pdf"
result2 = read_pdf_content(pdf_path2, 0, 25)
print(f"总页数: {result2['total_pages']}")

for page in result2['pages'][:15]:
    print(f"\n--- 第{page['page_num']}页 ---")
    print(page['content'][:600])

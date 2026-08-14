# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pdfplumber
import os

pdf_dir = "F:/奇门遁甲"
pdf_files = [
    "《金函玉镜奇门遁甲秘笈全书(上)》诸葛亮.pdf",
    "《金函玉镜奇门遁甲秘笈全书(下)》诸葛亮.pdf",
    "《甲遁真授秘录》上册 繁体竖版 术数丛书珍本 (清)薛凤祚著 .pdf",
    "《甲遁真授秘录》下册 繁体竖版 术数丛书珍本 (清)薛凤祚著 .pdf",
    "《笺元遁甲句解烟波钓叟歌》繁体竖版 (宋)趙普撰 明刊本 台湾国家图书馆藏.pdf",
    "《奇门遁甲白话精解》奇行+着.pdf",
    "《奇门遁甲吉凶占断教程》.pdf",
    "《奇门遁甲新述》费秉勋著 时代文艺出版社1991.pdf",
    "《奇门遁甲应用学》佚名.pdf",
    "《奇门遁甲预测学》佚名.pdf",
    "《奇门遁甲最新实例解析》.pdf",
    "《奇门精粹：奇门遁甲典籍大全》.pdf",
    "《图解奇门遁甲大全(第2部)：阳遁540局祥解》.pdf",
    "《图解奇门遁甲大全(第3部)：阴遁540局祥解》.pdf",
    "《图解遁甲演义》上部 吉凶占断  .pdf",
    "《图解遁甲演义》下部 遁甲1080局  .pdf",
]

print("PDF文本提取能力检查")
print("=" * 70)

for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_dir, pdf_file)
    if not os.path.exists(pdf_path):
        print(f"\n[不存在] {pdf_file}")
        continue

    try:
        with pdfplumber.open(pdf_path) as pdf:
            text_len = 0
            images_count = 0
            sample_text = ""

            for i, page in enumerate(pdf.pages[:3]):
                text = page.extract_text() or ""
                text_len += len(text)
                images_count += len(page.images)
                if not sample_text and text:
                    sample_text = text[:150]

            if text_len > 0:
                print(f"\n[有文字] {pdf_file}")
                print(f"  页数: {len(pdf.pages)}, 前3页文字数: {text_len}, 图像数: {images_count}")
                if sample_text:
                    print(f"  样本: {sample_text}...")
            else:
                print(f"\n[扫描版] {pdf_file}")
                print(f"  页数: {len(pdf.pages)}, 图像数: {images_count}")

    except Exception as e:
        print(f"\n[错误] {pdf_file}: {e}")

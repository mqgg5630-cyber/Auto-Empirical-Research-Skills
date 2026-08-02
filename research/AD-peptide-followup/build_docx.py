#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 Markdown 源文件生成格式化 .docx 报告（python-docx）。
支持：标题(1-4)、表格、引用块(>)、无序列表(-)、有序列表(1.)、**粗体**、*斜体*、[文本](链接) 超链接、中文字体。

用法: python3 build_docx.py <input.md> <output.docx>
"""
import re
import sys
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.opc.constants import RELATIONSHIP_TYPE as RT

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def set_run_fonts(run, size=None, bold=None, italic=None, east="宋体", ascii_f="Calibri"):
    run.font.name = ascii_f
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), ascii_f)
    rFonts.set(qn('w:hAnsi'), ascii_f)
    rFonts.set(qn('w:eastAsia'), east)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic


def add_hyperlink(paragraph, url, text, size=9.5):
    part = paragraph.part
    r_id = part.relate_to(url, RT.HYPERLINK, is_external=True)
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)
    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), 'Calibri')
    rFonts.set(qn('w:hAnsi'), 'Calibri')
    rFonts.set(qn('w:eastAsia'), '宋体')
    rPr.append(rFonts)
    sz = OxmlElement('w:sz'); sz.set(qn('w:val'), str(int(size * 2))); rPr.append(sz)
    c = OxmlElement('w:color'); c.set(qn('w:val'), '0563C1'); rPr.append(c)
    u = OxmlElement('w:u'); u.set(qn('w:val'), 'single'); rPr.append(u)
    new_run.append(rPr)
    t = OxmlElement('w:t')
    t.set(qn('xml:space'), 'preserve')
    t.text = text
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def add_text_with_links(paragraph, text, bold=False, italic=False, size=10.5):
    """处理 [text](url) 链接，其余为普通文本。"""
    pos = 0
    for m in LINK_RE.finditer(text):
        if m.start() > pos:
            r = paragraph.add_run(text[pos:m.start()])
            set_run_fonts(r, size=size, bold=bold, italic=italic)
        add_hyperlink(paragraph, m.group(2), m.group(1), size=size)
        pos = m.end()
    if pos < len(text):
        r = paragraph.add_run(text[pos:])
        set_run_fonts(r, size=size, bold=bold, italic=italic)


def add_inline(paragraph, text, size=10.5):
    """解析 **粗体** 与 *斜体*（不嵌套），含链接。"""
    segs = text.split('**')
    for i, seg in enumerate(segs):
        bold = (i % 2 == 1)
        subs = seg.split('*')
        for j, sp in enumerate(subs):
            italic = (j % 2 == 1)
            add_text_with_links(paragraph, sp, bold=bold, italic=italic, size=size)


def add_callout(doc, text, size=10.5):
    """引用块：浅灰底 + 左侧竖线。"""
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single'); left.set(qn('w:sz'), '18')
    left.set(qn('w:space'), '4'); left.set(qn('w:color'), '2E74B5')
    pBdr.append(left)
    pPr.append(pBdr)
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), 'F2F7FB')
    pPr.append(shd)
    p.paragraph_format.left_indent = Cm(0.4)
    p.paragraph_format.space_after = Pt(6)
    add_inline(p, text, size=size)
    return p


def add_table(doc, rows):
    """rows: list[list[str]]，首行为表头。"""
    n_cols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=n_cols)
    table.style = 'Table Grid'
    table.autofit = True
    for i, row in enumerate(rows):
        for j in range(n_cols):
            cell_text = row[j] if j < len(row) else ''
            cell = table.cell(i, j)
            # 清空默认段落，重新填充
            para = cell.paragraphs[0]
            for run in list(para.runs):
                run._element.getparent().remove(run._element)
            add_inline(para, cell_text, size=9)
            if i == 0:
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                # 表头底纹
                tcPr = cell._tc.get_or_add_tcPr()
                shd = OxmlElement('w:shd')
                shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), 'DEEAF6')
                tcPr.append(shd)
    # 段后间距
    sp = doc.add_paragraph()
    sp.paragraph_format.space_after = Pt(2)
    r = sp.add_run('')
    r.font.size = Pt(2)
    return table


def parse_md(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
    return lines


def build(md_path, docx_path):
    lines = parse_md(md_path)
    doc = Document()

    # 默认样式
    normal = doc.styles['Normal']
    normal.font.name = 'Calibri'
    normal.font.size = Pt(10.5)
    normal._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

    # 页边距
    for sec in doc.sections:
        sec.left_margin = Cm(2.2)
        sec.right_margin = Cm(2.2)
        sec.top_margin = Cm(2.2)
        sec.bottom_margin = Cm(2.2)

    i = 0
    first_h1 = True
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue

        # 表格块
        if line.startswith('|'):
            block = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                block.append(lines[i].strip())
                i += 1
            # 去掉分隔行 (|---|)
            data_rows = [r for r in block if not re.match(r'^\|[\s:\-|]+\|$', r)]
            rows = []
            for r in data_rows:
                cells = [c.strip() for c in r.strip().strip('|').split('|')]
                rows.append(cells)
            if rows:
                add_table(doc, rows)
            continue

        if line.startswith('#### '):
            h = doc.add_heading('', level=4)
            add_inline(h, line[5:], size=11)
            i += 1
            continue
        if line.startswith('### '):
            h = doc.add_heading('', level=3)
            add_inline(h, line[4:], size=12.5)
            i += 1
            continue
        if line.startswith('## '):
            h = doc.add_heading('', level=2)
            add_inline(h, line[3:], size=14)
            i += 1
            continue
        if line.startswith('# '):
            if first_h1:
                h = doc.add_heading('', level=0)
                first_h1 = False
            else:
                h = doc.add_heading('', level=1)
            add_inline(h, line[2:], size=17 if not first_h1 else 20)
            i += 1
            continue

        if line.startswith('> '):
            add_callout(doc, line[2:])
            i += 1
            continue

        if line.startswith('- '):
            p = doc.add_paragraph(style='List Bullet')
            add_inline(p, line[2:])
            i += 1
            continue

        m = re.match(r'^(\d+)\.\s+(.*)$', line)
        if m:
            p = doc.add_paragraph(style='List Bullet')
            add_inline(p, m.group(1) + '. ' + m.group(2))
            i += 1
            continue

        # 普通段落
        p = doc.add_paragraph()
        add_inline(p, line)
        i += 1

    # 文档属性
    cp = doc.core_properties
    cp.title = 'AChE/AD 相关候选肽后续机制研究——文献证据基础与实施方案'
    cp.author = 'Auto-Empirical-Research-Skills (AERS)'
    cp.subject = 'Cu/Fe-ROS-脂质过氧化-神经毒性；Aβ/tau/ApoE4/ferritin/transferrin 定位；计算结构生物学方法学；12 肽 Go/No-Go 方案'
    cp.keywords = 'AChE, PAS, Aβ42, tau, ApoE4, ferritin, transferrin, Cu, Fe, Zn, ROS, AlphaFold3, MD, MM/GBSA, QM/MM, iPSC'

    doc.save(docx_path)
    print(f'OK -> {docx_path}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    build(sys.argv[1], sys.argv[2])

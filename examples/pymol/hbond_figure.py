#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyMOL 配体-受体氢键出图（可审计版）
===================================

解决 AI 生成 PyMOL 脚本时最常见的三类翻车：

1. **误读 cmd.distance() 的返回值**
   它返回的是 *平均距离*，不是氢键条数。脚本里写 `if cmd.distance(...) == 0:`
   永远判断不出「没找到氢键」，于是退化成把周围残基全画出来。

2. **两个选择集重叠**
   `dist(name, "ligand", "protein")` 里如果 protein 把 ligand 也包含进去了
   （常见于同一个 PDB 文件里肽和受体在一个对象中），画出来的会是蛋白自身
   骨架 i/i+1 的氢键（典型特征：1.6-1.8 Å 的 H···O），与配体无关。

3. **选择器用错**
   肽配体是 polymer 不是 organic，`select ligand, organic` 会得到 0 个原子；
   小分子配体则相反。选完必须打印原子数验证。

本脚本的做法是：自己枚举供体/受体原子对，用 **chain/resi/name 构造的选择字符串**
（而不是内部 index）逐对画距离，然后**回读每条线重新测量一遍**做交叉校验，
最后打印一张可以直接贴进论文补充材料的氢键表。找不到就明确报错，绝不静默降级。

用法
----
    # 自检（不需要任何输入文件，内部构造测试复合物）
    python hbond_figure.py --selftest

    # 真实体系
    python hbond_figure.py --complex complex.pdb \
        --ligand-sel "chain B" --receptor-sel "chain A" \
        --out figure.png --cutoff 3.5

    # 配体与受体分属两个文件
    python hbond_figure.py --receptor rec.pdb --ligand pep.pdb --out figure.png

环境
----
    conda install -c conda-forge pymol-open-source
"""

from __future__ import annotations

import argparse
import hashlib
import math
import os
import sys

SCRIPT_VERSION = "1.1.0"

# 物理常量：重原子之间的氢键几何下限。
# N···O 氢键典型 2.6-3.2 Å；C-C 共价键才 1.54 Å。
# 任何小于此值的"重原子氢键"都是几何错误或空间冲突，不是氢键。
MIN_HEAVY_DIST = 2.20
MAX_HEAVY_DIST = 3.60


def script_fingerprint() -> str:
    """返回本文件的 SHA256 前 12 位。

    用途：确认 Agent 跑的确实是这个文件而不是它自己改写的版本。
    只要有人动过一个字节，指纹就会变。
    """
    try:
        return hashlib.sha256(
            open(__file__, "rb").read()).hexdigest()[:12]
    except Exception:
        return "unknown"

try:
    from pymol import cmd
except ModuleNotFoundError:
    sys.stderr.write(
        "未检测到 PyMOL。请先安装：\n"
        "    conda create -n pymol python=3.11 -y\n"
        "    conda activate pymol\n"
        "    conda install -c conda-forge pymol-open-source -y\n"
    )
    raise


# ---------------------------------------------------------------- 基础工具

def _atoms(sel: str) -> list[dict]:
    """取选择集内原子的标识与坐标。用 chain/resi/name 作为稳定标识，
    不使用 index —— PyMOL 内部 index 在不同调用间语义不一致。"""
    out: list[dict] = []
    cmd.iterate_state(
        1, sel,
        "out.append(dict(model=model, chain=chain, segi=segi, resi=resi, "
        "resn=resn, name=name, elem=elem, x=x, y=y, z=z))",
        space={"out": out, "dict": dict},
    )
    return out


def _sel_of(a: dict) -> str:
    """由原子标识构造唯一选择字符串。"""
    chain = a["chain"] if a["chain"] else "''"
    return (f"({a['model']} and chain {chain} and resi {a['resi']} "
            f"and name {a['name']})")


def _dist(a: dict, b: dict) -> float:
    return math.dist((a["x"], a["y"], a["z"]), (b["x"], b["y"], b["z"]))


def _angle(a: dict, b: dict, c: dict) -> float:
    """返回 a-b-c 的夹角（度）。"""
    v1 = (a["x"] - b["x"], a["y"] - b["y"], a["z"] - b["z"])
    v2 = (c["x"] - b["x"], c["y"] - b["y"], c["z"] - b["z"])
    n1 = math.sqrt(sum(t * t for t in v1))
    n2 = math.sqrt(sum(t * t for t in v2))
    if n1 == 0 or n2 == 0:
        return 0.0
    cosv = max(-1.0, min(1.0, sum(p * q for p, q in zip(v1, v2)) / (n1 * n2)))
    return math.degrees(math.acos(cosv))


# ---------------------------------------------------------------- 诊断

def diagnose(lig_sel: str, rec_sel: str) -> dict:
    """出图之前先体检。三项任何一项不过，后面画出来的都是假的。"""
    n_lig = cmd.count_atoms(lig_sel)
    n_rec = cmd.count_atoms(rec_sel)
    n_overlap = cmd.count_atoms(f"({lig_sel}) and ({rec_sel})")
    n_h_lig = cmd.count_atoms(f"({lig_sel}) and hydro")
    n_h_rec = cmd.count_atoms(f"({rec_sel}) and hydro")

    print("\n[诊断] 选择集体检")
    print(f"  配体原子数        : {n_lig}")
    print(f"  受体原子数        : {n_rec}")
    print(f"  两者重叠原子数    : {n_overlap}", end="")
    print("   ← 必须为 0，否则画出来的是蛋白自身氢键" if n_overlap else "   ✓")
    print(f"  配体氢原子        : {n_h_lig}")
    print(f"  受体氢原子        : {n_h_rec}")

    problems = []
    if n_lig == 0:
        problems.append(
            f"配体选择 '{lig_sel}' 匹配到 0 个原子。"
            "肽配体要用 chain/resi 选，不能用 organic；小分子才用 organic。")
    if n_rec == 0:
        problems.append(f"受体选择 '{rec_sel}' 匹配到 0 个原子。")
    if n_overlap:
        problems.append(
            f"配体与受体选择集重叠 {n_overlap} 个原子 —— "
            "这正是画出 1.6-1.8 Å 蛋白内部氢键的原因。"
            "受体应写成 '(polymer) and not (配体选择)'。")
    return {"n_lig": n_lig, "n_rec": n_rec, "n_overlap": n_overlap,
            "n_h_lig": n_h_lig, "n_h_rec": n_h_rec, "problems": problems}


# ---------------------------------------------------------------- 氢键检测

def find_hbonds(lig_sel: str, rec_sel: str, cutoff: float = 3.5,
                min_angle: float = 120.0) -> list[dict]:
    """枚举配体与受体之间的氢键。

    判据：重原子供体-受体距离 <= cutoff；若存在显式氢，另要求
    D-H···A 夹角 >= min_angle。返回按距离排序的列表。
    """
    lig_pol = _atoms(f"({lig_sel}) and (donor or acceptor)")
    rec_pol = _atoms(f"({rec_sel}) and (donor or acceptor)")
    lig_don = {id(a) for a in lig_pol}  # 占位，实际用下面的标志集合

    donors_l = _atoms(f"({lig_sel}) and donor")
    donors_r = _atoms(f"({rec_sel}) and donor")
    accept_l = _atoms(f"({lig_sel}) and acceptor")
    accept_r = _atoms(f"({rec_sel}) and acceptor")

    def key(a):
        return (a["model"], a["chain"], a["resi"], a["name"])

    donor_keys = {key(a) for a in donors_l} | {key(a) for a in donors_r}
    accept_keys = {key(a) for a in accept_l} | {key(a) for a in accept_r}

    hbonds: list[dict] = []
    clashes: list[dict] = []
    for a in lig_pol:
        ka = key(a)
        for b in rec_pol:
            kb = key(b)
            d = _dist(a, b)
            if d > cutoff:
                continue
            if d < MIN_HEAVY_DIST:
                # 重原子距离小于 2.2 Å 不可能是氢键，是空间冲突（对接位姿有问题）
                clashes.append({"lig": a, "rec": b, "dist": d})
                continue
            # 必须一方是供体、另一方是受体
            pair_ok = (ka in donor_keys and kb in accept_keys) or \
                      (kb in donor_keys and ka in accept_keys)
            if not pair_ok:
                continue

            donor, acceptor = (a, b) if ka in donor_keys else (b, a)
            ang = None
            # 有显式氢时做角度筛选
            hs = _atoms(f"(neighbor {_sel_of(donor)}) and hydro")
            if hs:
                ang = max(_angle(donor, h, acceptor) for h in hs)
                if ang < min_angle:
                    continue
            hbonds.append({
                "lig": a, "rec": b, "donor": donor, "acceptor": acceptor,
                "dist": d, "angle": ang,
            })

    hbonds.sort(key=lambda x: x["dist"])
    if clashes:
        clashes.sort(key=lambda x: x["dist"])
        print(f"\n[警告] 检出 {len(clashes)} 对重原子距离 < {MIN_HEAVY_DIST} Å 的接触，"
              f"最短 {clashes[0]['dist']:.2f} Å")
        print("       这不是氢键，是空间冲突 —— 对接位姿本身有原子重叠，请回去检查对接")
        for c in clashes[:5]:
            l, r = c["lig"], c["rec"]
            print(f"       {l['resn']}{l['resi']}/{l['name']} ··· "
                  f"{r['resn']}{r['resi']}/{r['name']}  {c['dist']:.2f} Å")
    return hbonds


def verify_geometry(hbonds: list[dict], cutoff: float) -> list[dict]:
    """回读校验：用 PyMOL 自己再测一遍每一对原子。

    为什么必须做这一步 —— 如果对象上挂了 TTT 显示矩阵
    （例如脚本里用过 cmd.translate(..., object=...)，它只改显示不改坐标），
    iterate_state 拿到的坐标和 PyMOL 实际几何就会不一致，
    算出来的"氢键"全是假的。这里以 PyMOL 实测为准。
    """
    fixed, drift = [], 0
    for hb in hbonds:
        s1, s2 = _sel_of(hb["lig"]), _sel_of(hb["rec"])
        try:
            real = cmd.get_distance(s1, s2)
        except Exception:
            continue
        if abs(real - hb["dist"]) >= 0.05:
            drift += 1
            hb["dist"] = real
        if real <= cutoff:
            fixed.append(hb)
    if drift:
        print(f"\n[校验] {drift} 条与实测不符，已按 PyMOL 实测几何重新筛选 "
              f"（常见原因：对象上挂了显示矩阵）")
    fixed.sort(key=lambda x: x["dist"])
    return fixed


def draw_hbonds(hbonds: list[dict], name: str = "hbonds") -> int:
    """逐对绘制距离。用 chain/resi/name 构造选择，不用内部 index。"""
    for obj in cmd.get_names("objects"):
        if obj.startswith("__hb_"):
            cmd.delete(obj)
    drawn = 0
    for k, hb in enumerate(hbonds):
        cmd.distance(f"__hb_{k}", _sel_of(hb["lig"]), _sel_of(hb["rec"]))
        drawn += 1
    parts = [f"__hb_{k}" for k in range(len(hbonds))]
    if parts:
        cmd.group(name, " ".join(parts))
    return drawn


def report(hbonds: list[dict]) -> None:
    print(f"\n[结果] 共检出 {len(hbonds)} 条配体-受体氢键")
    if not hbonds:
        print("  ⚠ 一条都没有。可能原因：")
        print("    1) 选择集写错（见上方诊断）")
        print("    2) 体系本身就没有氢键接触 —— 放大 cutoff 到 3.8 再看")
        print("    3) 结构里缺极性氢 → 先跑 cmd.h_add('donors or acceptors')")
        return
    print(f"\n  {'#':<3}{'配体原子':<24}{'受体残基/原子':<24}{'d(Å)':>7}{'角度(°)':>9}")
    print("  " + "-" * 66)
    for i, hb in enumerate(hbonds, 1):
        l, r = hb["lig"], hb["rec"]
        ls = f"{l['resn']}{l['resi']}/{l['name']}"
        rs = f"{r['chain']}/{r['resn']}{r['resi']}/{r['name']}"
        ang = f"{hb['angle']:.0f}" if hb["angle"] is not None else "n/a"
        print(f"  {i:<3}{ls:<24}{rs:<24}{hb['dist']:>7.2f}{ang:>9}")
    ds = [hb["dist"] for hb in hbonds]
    print(f"\n  [物理自检] 距离范围 {min(ds):.2f} – {max(ds):.2f} Å "
          f"（合理区间 {MIN_HEAVY_DIST}–{MAX_HEAVY_DIST}）"
          f"{'  ✓' if min(ds) >= MIN_HEAVY_DIST else '  ✗ 有小于下限的值，结果不可信'}")
    resid = sorted({(hb["rec"]["chain"], hb["rec"]["resi"], hb["rec"]["resn"])
                    for hb in hbonds}, key=lambda t: int(t[1]) if t[1].lstrip('-').isdigit() else 0)
    print(f"\n  参与成键的受体残基（{len(resid)} 个）："
          + ", ".join(f"{r[2]}{r[1]}" for r in resid))


# ---------------------------------------------------------------- 出图

def style_figure(lig_sel: str, rec_sel: str, hbonds: list[dict],
                 cartoon_transparency: float = 0.75) -> None:
    """只显示参与氢键的残基，画面立刻干净。"""
    cmd.hide("everything")
    cmd.show("cartoon", rec_sel)
    cmd.color("palegreen", rec_sel)
    cmd.set("cartoon_transparency", cartoon_transparency)

    cmd.show("sticks", f"({lig_sel}) and not (hydro and elem H and neighbor elem C)")
    cmd.color("cyan", f"({lig_sel}) and elem C")
    cmd.util.cnc(lig_sel)
    cmd.set("stick_radius", 0.16, lig_sel)

    if hbonds:
        parts = " or ".join(_sel_of(hb["rec"]) for hb in hbonds)
        cmd.select("hb_residues", f"byres ({parts})")
        cmd.show("sticks", "hb_residues and not (hydro and neighbor elem C)")
        cmd.color("green", "hb_residues and elem C")
        cmd.set("stick_radius", 0.14, "hb_residues")

    # 非极性氢一律隐藏
    cmd.hide("everything", "hydro and (neighbor elem C)")

    # 关键：上面的 hide("everything") 会把 distance 对象一起藏掉，
    # 必须显式把 dashes / labels 重新打开 —— 这是"氢键线画了却看不见"的第四个原因。
    for obj in cmd.get_names("objects"):
        if obj.startswith("__hb_"):
            cmd.enable(obj)
            cmd.show("dashes", obj)
            cmd.show("labels", obj)
            cmd.color("yellow", obj)
            cmd.set("dash_gap", 0.25, obj)
            cmd.set("dash_length", 0.30, obj)
            cmd.set("dash_width", 5.0, obj)
            cmd.set("dash_radius", 0.09, obj)
            cmd.set("dash_color", "yellow", obj)
            cmd.set("label_size", 18, obj)
            cmd.set("label_distance_digits", 2, obj)
            cmd.set("label_color", "black", obj)

    cmd.bg_color("white")
    cmd.set("ray_opaque_background", 1)
    cmd.set("antialias", 2)
    cmd.set("ambient_occlusion_mode", 1)
    cmd.set("specular", 0.15)
    focus = "hb_residues or (%s)" % lig_sel if hbonds else lig_sel
    cmd.orient(focus)
    cmd.zoom(focus, 4.0)


# ---------------------------------------------------------------- 主流程

def run(complex_path=None, receptor_path=None, ligand_path=None,
        lig_sel="chain B", rec_sel=None, cutoff=3.5, out="hbond_figure.png",
        add_h=True, width=2000, height=1500, selftest=False) -> int:
    print(f"hbond_figure.py v{SCRIPT_VERSION}  指纹 {script_fingerprint()}")
    print("（若 Agent 声称跑了本脚本但输出里没有这一行，说明它跑的是别的代码）")
    cmd.reinitialize()
    cmd.feedback("disable", "all", "everything")

    if selftest:
        print("[自检] 用 cmd.fab 构造测试复合物（不需要外部文件）")
        cmd.fab("AEAAAKEAAAKAEAAAKA", "receptor", ss=1)
        cmd.fab("FSDLWKLL", "peptide", ss=1)
        cmd.translate([3.5, 6.0, 0.0], selection="peptide", camera=0)
        lig_sel, rec_sel = "peptide", "receptor"
    elif complex_path:
        cmd.load(complex_path, "complex")
        if rec_sel is None:
            rec_sel = f"(complex and polymer) and not ({lig_sel})"
    elif receptor_path and ligand_path:
        cmd.load(receptor_path, "receptor")
        cmd.load(ligand_path, "ligand")
        lig_sel, rec_sel = "ligand", "receptor"
    else:
        print("需要 --complex 或 (--receptor 且 --ligand)，或 --selftest", file=sys.stderr)
        return 2

    if add_h:
        # 只补极性氢，比 h_add all 干净得多
        cmd.h_add("donors or acceptors")

    diag = diagnose(lig_sel, rec_sel)
    if diag["problems"]:
        print("\n[阻断] 发现以下问题，先修好再出图：")
        for p in diag["problems"]:
            print("  ✗ " + p)
        return 1

    hbonds = find_hbonds(lig_sel, rec_sel, cutoff=cutoff)
    if not hbonds and cutoff < 3.8:
        print(f"\n[重试] cutoff={cutoff} 未找到，放大到 3.8 再试一次")
        hbonds = find_hbonds(lig_sel, rec_sel, cutoff=3.8)

    hbonds = verify_geometry(hbonds, cutoff if hbonds else 3.8)
    drawn = draw_hbonds(hbonds)
    report(hbonds)
    if hbonds:
        print(f"\n[校验] {drawn}/{len(hbonds)} 条已绘制，全部通过 PyMOL 实测复核 ✓")

    style_figure(lig_sel, rec_sel, hbonds)
    out = os.path.abspath(out)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    cmd.ray(width, height)
    cmd.png(out, dpi=300)
    print(f"\n[输出] {out}")
    print(f"[输出] 会话 {out.rsplit('.', 1)[0]}.pse（可用 PyMOL 打开手工微调）")
    cmd.save(out.rsplit(".", 1)[0] + ".pse")
    return 0 if hbonds else 3


def main() -> int:
    ap = argparse.ArgumentParser(description="PyMOL 配体-受体氢键出图（可审计）")
    ap.add_argument("--complex", dest="complex_path")
    ap.add_argument("--receptor", dest="receptor_path")
    ap.add_argument("--ligand", dest="ligand_path")
    ap.add_argument("--ligand-sel", default="chain B",
                    help="配体选择表达式；肽用 chain/resi，小分子用 organic")
    ap.add_argument("--receptor-sel", default=None,
                    help="留空则自动取 polymer 减去配体，保证两者不重叠")
    ap.add_argument("--cutoff", type=float, default=3.5)
    ap.add_argument("--out", default="hbond_figure.png")
    ap.add_argument("--no-addh", action="store_true")
    ap.add_argument("--width", type=int, default=2000)
    ap.add_argument("--height", type=int, default=1500)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--version", action="store_true", help="打印版本与文件指纹后退出")
    a = ap.parse_args()
    if a.version:
        print(f"hbond_figure.py v{SCRIPT_VERSION}  指纹 {script_fingerprint()}")
        return 0
    return run(complex_path=a.complex_path, receptor_path=a.receptor_path,
               ligand_path=a.ligand_path, lig_sel=a.ligand_sel,
               rec_sel=a.receptor_sel, cutoff=a.cutoff, out=a.out,
               add_h=not a.no_addh, width=a.width, height=a.height,
               selftest=a.selftest)


if __name__ == "__main__":
    raise SystemExit(main())

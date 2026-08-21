#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dump_contacts.py —— 从当前 PyMOL 会话里导出真实的极性接触列表
================================================================

用途：你在 GUI 里手动做出来的 `lig_polar_conts` 是**基准真值**，
但 PyMOL 只画线不给列表。这个脚本把已经存在的距离对象里的
原子配对抠出来，打印成表并存成 CSV。

这样你就有了一份可以用来核对任何自动化脚本的标准答案。

两种用法
--------

**用法 A：在已经打开的 PyMOL 图形界面里**（推荐，读的是你亲手确认过的结果）

    在 PyMOL 窗口下方那个写着 "PyMOL>" 的输入框里敲：

        run E:/0mcp-agv/pymol/dump_contacts.py

    注意：`run` 是 PyMOL 的内部命令，**不是 PowerShell 命令**。
    在 PowerShell 里敲会报 "无法将 run 项识别为 cmdlet"。

**用法 B：在 PowerShell 里独立运行**（自动加载、拆分、计算、导表）

    python dump_contacts.py --complex E:/path/complex.pdb --ligand-sel "chain B"

    这会新开一个无头会话，把复合物拆成 lig / pro 两个对象，
    执行与 GUI 完全相同的 dist ... mode=2，然后导表。

输出
----
    终端打印一张表：配体原子 / 受体原子 / H···A / D···A
    同目录生成 contacts_dump.csv

可选参数（在 PyMOL 里改这两个变量后重新 run）
    DIST_OBJECT = "lig_polar_conts"   # 要读哪个距离对象；留空则读全部
    OUT_CSV     = "contacts_dump.csv"
"""

import os
import sys

from pymol import cmd

try:
    from chempy import cpv
except ImportError:  # 极老版本兜底
    import math

    class cpv:  # type: ignore
        @staticmethod
        def distance(a, b):
            return math.dist(a, b)


DIST_OBJECT = "lig_polar_conts"   # 改成你的距离对象名；留空字符串则导出全部
OUT_CSV = "contacts_dump.csv"


def _measurement_objects(name: str = "") -> list[str]:
    try:
        objs = cmd.get_names_of_type("object:measurement")
    except Exception:
        objs = [o for o in cmd.get_names("objects")
                if cmd.get_type(o) == "object:measurement"]
    if name:
        return [o for o in objs if o == name] or objs
    return objs


def _raw_pairs(dist_name: str, state: int = 1):
    """把距离对象的虚线端点坐标反查回原子。"""
    xyz2idx: dict = {}
    cmd.iterate_state(state, "all", "xyz2idx[x, y, z] = (model, index)",
                      space={"xyz2idx": xyz2idx})
    out = []
    for obj in cmd.get_session(dist_name, 1, 1, 0, 0)["names"]:
        try:
            points = obj[5][2][state - 1][1]
        except Exception:
            continue
        if not points:
            continue
        for i in range(0, len(points), 6):
            p1 = tuple(points[i:i + 3])
            p2 = tuple(points[i + 3:i + 6])
            if p1 in xyz2idx and p2 in xyz2idx:
                out.append((xyz2idx[p1], xyz2idx[p2], cpv.distance(p1, p2)))
    return out


def _atom(model: str, idx: int):
    m = cmd.get_model(f"{model} and index {idx}")
    return m.atom[0] if m.atom else None


def _heavy(model: str, idx: int):
    """氢换成它连接的重原子；本来就是重原子则原样返回。"""
    a = _atom(model, idx)
    if a is None or a.symbol != "H":
        return a
    nb = cmd.get_model(f"(neighbor ({model} and index {idx})) and not hydro")
    return nb.atom[0] if nb.atom else a


def dump(dist_object: str = DIST_OBJECT, out_csv: str = OUT_CSV) -> None:
    objs = _measurement_objects(dist_object)
    if not objs:
        print("当前会话里没有距离对象。两种解决办法：\n")
        print("  A) 如果你已经在 PyMOL 图形界面里做好了 polar contacts：")
        print("     请在 PyMOL 窗口下方的 \"PyMOL>\" 输入框里敲（不是 PowerShell）：")
        print("         run E:/0mcp-agv/pymol/dump_contacts.py\n")
        print("  B) 想在 PowerShell 里一步到位（自动加载+拆分+计算）：")
        print("         python dump_contacts.py --complex 你的complex.pdb "
              "--ligand-sel \"chain B\"")
        return

    print("=" * 78)
    print("当前会话对象：", ", ".join(cmd.get_names("objects")))
    print("读取的距离对象：", ", ".join(objs))
    print("=" * 78)

    rows = []
    for name in objs:
        pairs = _raw_pairs(name)
        for (m1, i1), (m2, i2), d_raw in pairs:
            a1, a2 = _atom(m1, i1), _atom(m2, i2)
            h1, h2 = _heavy(m1, i1), _heavy(m2, i2)
            if not all((a1, a2, h1, h2)):
                continue
            d_heavy = cpv.distance(h1.coord, h2.coord)
            rows.append({
                "dist_obj": name,
                "atom1": f"{a1.model}/{a1.chain}/{a1.resn}{a1.resi}/{a1.name}",
                "atom2": f"{a2.model}/{a2.chain}/{a2.resn}{a2.resi}/{a2.name}",
                "heavy1": f"{h1.model}/{h1.chain}/{h1.resn}{h1.resi}/{h1.name}",
                "heavy2": f"{h2.model}/{h2.chain}/{h2.resn}{h2.resi}/{h2.name}",
                "d_drawn": round(d_raw, 2),
                "d_heavy": round(d_heavy, 2),
                "intra": a1.model == a2.model,
            })

    if not rows:
        print("距离对象存在但没能反查到原子配对。"
              "常见原因：距离对象是在结构被修改前生成的，"
              "请重新执行一次 dist 命令后再 run 本脚本。")
        return

    rows.sort(key=lambda r: r["d_heavy"])
    inter = [r for r in rows if not r["intra"]]
    intra = [r for r in rows if r["intra"]]

    print(f"\n共 {len(rows)} 条接触：分子间 {len(inter)} 条，分子内 {len(intra)} 条\n")
    print(f"  {'#':<3}{'原子1（画线端点）':<32}{'原子2（画线端点）':<32}"
          f"{'画的':>7}{'D···A':>8}")
    print("  " + "-" * 80)
    for i, r in enumerate(inter, 1):
        print(f"  {i:<3}{r['atom1']:<32}{r['atom2']:<32}"
              f"{r['d_drawn']:>7.2f}{r['d_heavy']:>8.2f}")

    if intra:
        print(f"\n  以下 {len(intra)} 条是**同一对象内部**的接触"
              f"（肽自身的 α 螺旋骨架氢键），不属于配体-受体相互作用：")
        for r in intra[:10]:
            print(f"      {r['atom1']:<32}{r['atom2']:<32}"
                  f"{r['d_drawn']:>7.2f}{r['d_heavy']:>8.2f}")

    # 参与残基
    resid = []
    for r in inter:
        for h in (r["heavy1"], r["heavy2"]):
            parts = h.split("/")
            resid.append((parts[0], parts[1], parts[2]))
    uniq = sorted(set(resid))
    print(f"\n  涉及的残基（{len(uniq)} 个）：")
    for obj in sorted({u[0] for u in uniq}):
        names = [u[2] for u in uniq if u[0] == obj]
        print(f"      {obj}: " + ", ".join(sorted(set(names))))

    # 写 CSV
    try:
        import csv
        path = os.path.abspath(out_csv)
        with open(path, "w", newline="", encoding="utf-8-sig") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"\n  已写出 CSV：{path}")
    except Exception as exc:
        print(f"\n  写 CSV 失败：{exc}")

    print("\n把上面这张表贴出来，就是核对任何自动化脚本的标准答案。")
    print("=" * 78)


def build_and_dump(complex_path: str, lig_sel: str = "chain B",
                   out_csv: str = OUT_CSV) -> None:
    """独立模式：加载复合物 → 拆成 lig/pro → 执行与 GUI 相同的 dist → 导表。"""
    if not os.path.exists(complex_path):
        print(f"找不到文件：{complex_path}")
        return
    cmd.reinitialize()
    cmd.feedback("disable", "all", "everything")
    cmd.load(complex_path, "__src")
    n_all = cmd.count_atoms("__src")
    cmd.create("lig", f"(__src) and ({lig_sel})")
    cmd.create("pro", f"(__src) and polymer and not ({lig_sel})")
    cmd.delete("__src")
    cmd.sort()
    n_lig, n_pro = cmd.count_atoms("lig"), cmd.count_atoms("pro")
    print(f"[加载] {complex_path}  共 {n_all} 原子")
    print(f"[拆分] lig = {n_lig} 原子（{lig_sel}） / pro = {n_pro} 原子")
    if n_lig == 0:
        print("配体选择匹配到 0 个原子 —— 检查 --ligand-sel。"
              "肽配体用 chain/resi，不要用 organic。")
        return
    # 与 GUI 的 Action → find → polar contacts 完全一致的命令
    cmd.dist("lig_polar_conts", "lig", "pro",
             quiet=1, mode=2, label=0, reset=1)
    dump(out_csv=out_csv)


# ---- 入口 ----
if __name__ == "__main__" or "--complex" in sys.argv:
    if "--complex" in sys.argv:
        i = sys.argv.index("--complex")
        path = sys.argv[i + 1] if i + 1 < len(sys.argv) else ""
        lig = "chain B"
        if "--ligand-sel" in sys.argv:
            j = sys.argv.index("--ligand-sel")
            lig = sys.argv[j + 1] if j + 1 < len(sys.argv) else lig
        out = OUT_CSV
        if "--out-csv" in sys.argv:
            k = sys.argv.index("--out-csv")
            out = sys.argv[k + 1] if k + 1 < len(sys.argv) else out
        build_and_dump(path, lig, out)
    else:
        dump()
else:
    # 通过 PyMOL 的 run 命令加载时走这里
    dump()

# 也可以在 PyMOL 命令行里直接调用：dump_contacts
cmd.extend("dump_contacts", dump)

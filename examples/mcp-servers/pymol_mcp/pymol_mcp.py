#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyMOL MCP Server
=================
Wraps the PyMOL molecular graphics system (available via the `pymol` Python
package) as an MCP service.  The server runs in the `docking` conda
environment and exposes a small set of useful operations:

* ``load_pdb(file_path)`` – Load a structure from a PDB file.
* ``save_image(output_path, width=800, height=600, ray=False)`` – Render the
  current view to a PNG image.
* ``align_structures(target_path, mobile_path)`` – Align two structures using
  PyMOL's ``align`` command.
* ``set_view(view_matrix)`` – Apply a view matrix (list of 16 floats).
* ``get_view()`` – Return the current view matrix.
* ``render_movie(pdb_list, output_path, fps=30)`` – Generate a simple MP4 movie
  by loading each structure in sequence.
* ``reset()`` – Reset the PyMOL session to a clean state.

The implementation follows the same pattern as the official ``orange3_mcp``
server: lazy-load PyMOL, provide a ``_selftest`` routine, and register the tools
with ``FastMCP``.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Any, List

# FastMCP SDK – compatible with MCP <2
try:
    from mcp.server.fastmcp import FastMCP
except ModuleNotFoundError as exc:  # pragma: no cover
    sys.stderr.write(
        "无法导入 mcp.server.fastmcp。\n"
        "原因：MCP Python SDK 2.0（2026-07-28 发布）把该模块迁移到了 mcp.server.mcpserver。\n"
        "解决：pip install \"mcp>=1.28,<2\"，或用 uvx --with \"mcp<2\" 启动。\n"
        f"原始错误：{exc}\n"
    )

mcp = FastMCP("pymol")

# --------------------------------------------------------------------------
# Helper – lazy import of PyMOL
# --------------------------------------------------------------------------

def _pymol() -> Any:
    """Import PyMOL lazily.  If the import fails, raise a clear error with
    installation hints.
    """
    try:
        import pymol
        from pymol import cmd
        return cmd
    except Exception as exc:
        hint = (
            "PyMOL 未在当前 conda 环境中安装。请在 `docking` 环境里执行：\n"
            "    conda install -n docking -c conda-forge pymol-open-source\n"
            "或使用官方安装脚本。"
        )
        raise RuntimeError(hint) from exc


# --------------------------------------------------------------------------
# Utility response helpers – mimic orange3 style
# --------------------------------------------------------------------------

def _ok(**payload: Any) -> dict:
    out = {"ok": True}
    out.update(payload)
    return out


def _err(msg: str, **extra: Any) -> dict:
    out = {"ok": False, "error": msg}
    out.update(extra)
    return out


# --------------------------------------------------------------------------
# MCP tools implementation
# --------------------------------------------------------------------------

@mcp.tool()
def load_pdb(file_path: str) -> dict:
    """Load a PDB file into the current PyMOL session.
    Returns the absolute path that was loaded.
    """
    if not os.path.isfile(file_path):
        return _err(f"找不到文件：{file_path}")
    try:
        cmd = _pymol()
        cmd.load(file_path, "loaded")
        return _ok(path=os.path.abspath(file_path))
    except Exception as exc:
        return _err(f"加载失败 {type(exc).__name__}: {exc}")


@mcp.tool()
def save_image(output_path: str, width: int = 800, height: int = 600, ray: bool = False) -> dict:
    """Render the current view to a PNG image.
    ``ray`` – whether to use ray tracing (slow but high quality).
    """
    try:
        cmd = _pymol()
        # Ensure the directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        cmd.png(output_path, width=width, height=height, ray=ray)
        return _ok(image=os.path.abspath(output_path))
    except Exception as exc:
        return _err(f"保存图片失败 {type(exc).__name__}: {exc}")


@mcp.tool()
def align_structures(target_path: str, mobile_path: str) -> dict:
    """Align ``mobile_path`` onto ``target_path`` using PyMOL's ``align``.
    Returns RMSD and the name of the aligned object.
    """
    if not os.path.isfile(target_path) or not os.path.isfile(mobile_path):
        return _err("目标或移动文件不存在")
    try:
        cmd = _pymol()
        cmd.delete("all")
        cmd.load(target_path, "target")
        cmd.load(mobile_path, "mobile")
        rms = cmd.align("mobile", "target")
        return _ok(rms=rms, aligned_object="mobile")
    except Exception as exc:
        return _err(f"对齐失败 {type(exc).__name__}: {exc}")


@mcp.tool()
def set_view(view_matrix: List[float]) -> dict:
    """Set the camera view matrix (list of 16 floats)."""
    if len(view_matrix) != 16:
        return _err("view_matrix 必须包含 16 个浮点数")
    try:
        cmd = _pymol()
        cmd.set_view(view_matrix)
        return _ok()
    except Exception as exc:
        return _err(f"设置视图失败 {type(exc).__name__}: {exc}")


@mcp.tool()
def get_view() -> dict:
    """Return the current view matrix as a list of 16 floats."""
    try:
        cmd = _pymol()
        vm = cmd.get_view()
        return _ok(view_matrix=vm)
    except Exception as exc:
        return _err(f"获取视图失败 {type(exc).__name__}: {exc}")


@mcp.tool()
def render_movie(pdb_list: List[str], output_path: str, fps: int = 30) -> dict:
    """Create a simple MP4 movie by loading each PDB in ``pdb_list`` sequentially.
    The generated movie is saved to ``output_path``.
    """
    if not pdb_list:
        return _err("pdb_list 不能为空")
    for p in pdb_list:
        if not os.path.isfile(p):
            return _err(f"文件不存在：{p}")
    try:
        cmd = _pymol()
        cmd.delete("all")
        # Ensure output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        # Use PyMOL's mplay and mset to create a movie
        cmd.mstop()
        cmd.mdelete()
        cmd.mset(f"1 x {len(pdb_list)}")
        for i, p in enumerate(pdb_list, start=1):
            cmd.load(p, f"obj{i}")
            cmd.frame(i)
            cmd.show_as("cartoon", f"obj{i}")
            cmd.hide("everything", "all")
            cmd.show("cartoon", f"obj{i}")
        cmd.mpng(output_path, mode=0, width=800, height=600)
        # Convert frames to MP4 using ffmpeg if available
        ffmpeg = "ffmpeg"
        if subprocess.run([ffmpeg, "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
            # PyMOL writes frames as PNGs with pattern "movie001.png" etc.
            pattern = os.path.join(os.path.dirname(output_path), "movie%03d.png")
            cmd.mpng(pattern, mode=0, width=800, height=600)
            subprocess.run([
                ffmpeg, "-y", "-framerate", str(fps), "-i", pattern,
                "-c:v", "libx264", "-pix_fmt", "yuv420p", output_path
            ], check=True)
            # Clean up intermediate PNGs
            for f in os.listdir(os.path.dirname(output_path)):
                if f.startswith("movie") and f.endswith(".png"):
                    os.remove(os.path.join(os.path.dirname(output_path), f))
        else:
            # ffmpeg not available – just keep the PNG sequence.
            pass
        return _ok(movie=os.path.abspath(output_path))
    except Exception as exc:
        return _err(f"渲染电影失败 {type(exc).__name__}: {exc}")


@mcp.tool()
def split_complex_pdb(complex_path: str, output_dir: str = "", ligand_chain: str = "B", receptor_chain: str = "A") -> dict:
    """Physically splits a docked complex PDB into lig.pdb (ligand) and pro.pdb (receptor).

    Args:
        complex_path: Path to complex PDB file
        output_dir: Destination folder (defaults to complex directory)
        ligand_chain: Ligand chain ID (default 'B')
        receptor_chain: Receptor chain ID (default 'A')
    """
    if not os.path.isfile(complex_path):
        return _err(f"找不到复合物文件：{complex_path}")
    try:
        cmd = _pymol()
        if not output_dir:
            output_dir = os.path.dirname(os.path.abspath(complex_path))
        os.makedirs(output_dir, exist_ok=True)

        lig_pdb = os.path.join(output_dir, "lig.pdb")
        pro_pdb = os.path.join(output_dir, "pro.pdb")

        cmd.reinitialize()
        cmd.load(complex_path, "complex_tmp")

        lig_atoms = cmd.count_atoms(f"complex_tmp and chain {ligand_chain}")
        pro_atoms = cmd.count_atoms(f"complex_tmp and chain {receptor_chain}")

        if lig_atoms == 0 or pro_atoms == 0:
            return _err(f"链选择错误: chain {ligand_chain}={lig_atoms}原子, chain {receptor_chain}={pro_atoms}原子")

        cmd.save(lig_pdb, f"complex_tmp and chain {ligand_chain}")
        cmd.save(pro_pdb, f"complex_tmp and chain {receptor_chain}")

        return _ok(
            lig_pdb=os.path.abspath(lig_pdb),
            pro_pdb=os.path.abspath(pro_pdb),
            lig_atoms=lig_atoms,
            pro_atoms=pro_atoms
        )
    except Exception as exc:
        return _err(f"拆分复合物失败 {type(exc).__name__}: {exc}")


@mcp.tool()
def render_sci_docking_composite(
    complex_path: str,
    output_png: str = "",
    output_pse: str = "",
    ligand_chain: str = "B",
    receptor_chain: str = "A"
) -> dict:
    """Generate an SCI publication-ready dual-panel docking interaction composite figure.

    Features:
    - Left Panel: Global receptor overview + precise pixel-mask bounding box around ligand
    - Right Panel: High-clarity binding site + native polar contacts (yellow dashed lines)
                   + Cyan sticks for interacting receptor residues + floating bold halo labels
    - Exports high-resolution PNG (1850x1000) and interactive PyMOL .pse session file.
    """
    if not os.path.isfile(complex_path):
        return _err(f"找不到复合物文件：{complex_path}")

    try:
        import math
        from PIL import Image, ImageDraw
        cmd = _pymol()

        base_dir = os.path.dirname(os.path.abspath(complex_path))
        base_name = os.path.splitext(os.path.basename(complex_path))[0].replace("_complex", "")

        if not output_png:
            output_png = os.path.join(base_dir, f"{base_name}_sci.png")
        if not output_pse:
            output_pse = os.path.join(base_dir, f"{base_name}.pse")

        os.makedirs(os.path.dirname(os.path.abspath(output_png)), exist_ok=True)
        os.makedirs(os.path.dirname(os.path.abspath(output_pse)), exist_ok=True)

        # 1. Physical Split
        temp_dir = os.path.join(base_dir, f"_{base_name}_temp")
        os.makedirs(temp_dir, exist_ok=True)
        lig_pdb = os.path.join(temp_dir, "lig.pdb")
        pro_pdb = os.path.join(temp_dir, "pro.pdb")

        cmd.reinitialize()
        cmd.load(complex_path, "complex_tmp")
        cmd.save(lig_pdb, f"complex_tmp and chain {ligand_chain}")
        cmd.save(pro_pdb, f"complex_tmp and chain {receptor_chain}")

        overview_temp = os.path.join(temp_dir, "ov.png")
        mask_temp = os.path.join(temp_dir, "mk.png")
        detail_temp = os.path.join(temp_dir, "dt.png")

        # 2. Render Left Panel
        cmd.reinitialize()
        cmd.viewport(900, 900)
        cmd.load(pro_pdb, "pro")
        cmd.load(lig_pdb, "lig")
        cmd.hide("everything")
        cmd.show_as("cartoon", "pro")
        cmd.color("forest", "pro")
        cmd.show("sticks", "lig")
        cmd.color("red", "lig")
        cmd.set("stick_radius", 0.28, "lig")
        cmd.orient("pro")
        cmd.zoom("pro", buffer=2.0)

        cmd.bg_color("white")
        cmd.set("ray_opaque_background", 1)
        cmd.set("antialias", 2)
        cmd.set("ray_shadow", 1)
        cmd.set("ray_shadow_decay_factor", 0.15)
        cmd.set("ambient_occlusion_mode", 1)
        cmd.set("ambient_occlusion_scale", 12.0)
        cmd.set("ambient_occlusion_smooth", 10)
        cmd.set("specular", 0.25)
        cmd.set("ortho", 1)

        cmd.ray(900, 900)
        cmd.png(overview_temp)

        # Mask
        cmd.hide("everything", "pro")
        cmd.bg_color("black")
        cmd.color("white", "lig")
        cmd.ray(900, 900)
        cmd.png(mask_temp)

        mask_img = Image.open(mask_temp).convert("L")
        bbox = mask_img.getbbox()
        if bbox is None:
            min_px, min_py, max_px, max_py = 400, 400, 500, 500
        else:
            pad = 25
            min_px = max(10, bbox[0] - pad)
            min_py = max(10, bbox[1] - pad)
            max_px = min(890, bbox[2] + pad)
            max_py = min(890, bbox[3] + pad)

        # 3. Render Right Panel
        cmd.reinitialize()
        cmd.viewport(900, 900)
        cmd.load(pro_pdb, "pro")
        cmd.load(lig_pdb, "lig")
        cmd.hide("everything")

        cmd.show_as("cartoon", "pro")
        cmd.color("forest", "pro")
        cmd.set("cartoon_transparency", 0.45)

        cmd.show("sticks", "lig")
        cmd.color("red", "lig")
        cmd.set("stick_radius", 0.25, "lig")

        cmd.distance("lig_polar_conts", "lig", "pro", mode=2)
        cmd.enable("lig_polar_conts")
        cmd.color("yellow", "lig_polar_conts")
        cmd.set("dash_gap", 0.25, "lig_polar_conts")
        cmd.set("dash_width", 4.5, "lig_polar_conts")
        cmd.set("dash_radius", 0.07, "lig_polar_conts")
        cmd.set("label_color", "black", "lig_polar_conts")
        cmd.set("label_font_id", 7, "lig_polar_conts")
        cmd.set("label_size", 16, "lig_polar_conts")

        # Extract exact residues from distance coordinates
        session_data = cmd.get_session("lig_polar_conts", 1, 1, 0, 0)
        points = session_data["names"][0][5][2][0][1]

        xyz2atom = {}
        cmd.iterate_state(1, "all", "xyz2atom[(round(x, 3), round(y, 3), round(z, 3))] = (model, resn, resi, name)", space={"xyz2atom": xyz2atom})

        rec_res_keys = set()
        hbonds_info = []
        for i in range(0, len(points), 6):
            p1 = (round(points[i], 3), round(points[i+1], 3), round(points[i+2], 3))
            p2 = (round(points[i+3], 3), round(points[i+4], 3), round(points[i+5], 3))
            dist = math.dist(p1, p2)

            a1 = xyz2atom.get(p1, ("?", "?", "?", "?"))
            a2 = xyz2atom.get(p2, ("?", "?", "?", "?"))
            lig_a = a1 if a1[0] == 'lig' else a2
            pro_a = a2 if a1[0] == 'lig' else a1

            if pro_a[0] == 'pro':
                rec_res_keys.add(str(pro_a[2]))
            hbonds_info.append({
                "ligand_atom": f"{lig_a[1]}{lig_a[2]}:{lig_a[3]}",
                "receptor_atom": f"{pro_a[1]}{pro_a[2]}:{pro_a[3]}",
                "distance": round(dist, 2)
            })

        rec_resi_list = sorted(rec_res_keys, key=lambda x: int(x) if x.isdigit() else x)

        if rec_resi_list:
            resi_sel = "+".join(rec_resi_list)
            cmd.select("res", f"pro and resi {resi_sel}")
            cmd.show("sticks", "res")
            cmd.color("cyan", "res")
            cmd.set("stick_radius", 0.22, "res")

            cmd.label("res and name CA", '"%s-%s" % (resn.upper(), resi)')
            cmd.set("label_font_id", 7)
            cmd.set("label_size", 20)
            cmd.set("label_color", "black")
            cmd.set("label_outline_color", "white")
            cmd.set("float_labels", 1)
            cmd.set("label_shadow_mode", 0)
            cmd.set("label_position", [1.0, 1.0, 2.5])

        cmd.orient("lig")
        cmd.zoom("res or lig" if rec_resi_list else "lig", buffer=3.2)
        cmd.turn("x", 15)
        cmd.turn("y", 10)

        cmd.bg_color("white")
        cmd.set("ray_opaque_background", 1)
        cmd.set("antialias", 2)
        cmd.set("ray_shadow", 1)
        cmd.set("ray_shadow_decay_factor", 0.15)
        cmd.set("ambient_occlusion_mode", 1)
        cmd.set("ambient_occlusion_scale", 12.0)
        cmd.set("ambient_occlusion_smooth", 10)
        cmd.set("specular", 0.25)
        cmd.set("ortho", 1)

        cmd.ray(900, 900)
        cmd.png(detail_temp)
        cmd.save(output_pse)

        # 4. Compose
        canvas = Image.new("RGB", (1850, 1000), "white")
        img_ov = Image.open(overview_temp)
        img_dt = Image.open(detail_temp)
        canvas.paste(img_ov, (50, 50))
        canvas.paste(img_dt, (900, 50))

        draw = ImageDraw.Draw(canvas)
        purple_color = (127, 63, 152)

        box_coords = [int(50 + min_px), int(50 + min_py), int(50 + max_px), int(50 + max_py)]
        _draw_dashed_rect(draw, box_coords, purple_color, width=3)
        _draw_dashed_rect(draw, [900, 50, 1800, 950], purple_color, width=3)
        _draw_dashed_line(draw, (box_coords[2], box_coords[1]), (900, 50), purple_color, width=3)
        _draw_dashed_line(draw, (box_coords[2], box_coords[3]), (900, 950), purple_color, width=3)

        canvas.save(output_png)

        # Cleanup temp files
        for f in [overview_temp, mask_temp, detail_temp, lig_pdb, pro_pdb]:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except Exception:
                    pass
        if os.path.exists(temp_dir):
            try:
                os.rmdir(temp_dir)
            except Exception:
                pass

        return _ok(
            figure_path=os.path.abspath(output_png),
            session_path=os.path.abspath(output_pse),
            interacting_residues=rec_resi_list,
            hydrogen_bonds=hbonds_info
        )
    except Exception as exc:
        return _err(f"生成 SCI 对接图失败 {type(exc).__name__}: {exc}")


def _draw_dashed_rect(draw, coords, color, dash_len=8, gap_len=6, width=3):
    x0, y0, x1, y1 = coords
    for x in range(x0, x1, dash_len + gap_len):
        draw.line([x, y0, min(x + dash_len, x1), y0], fill=color, width=width)
        draw.line([x, y1, min(x + dash_len, x1), y1], fill=color, width=width)
    for y in range(y0, y1, dash_len + gap_len):
        draw.line([x0, y, x0, min(y + dash_len, y1)], fill=color, width=width)
        draw.line([x1, y, x1, min(y + dash_len, y1)], fill=color, width=width)


def _draw_dashed_line(draw, start, end, color, dash_len=8, gap_len=6, width=2):
    import math
    x0, y0 = start
    x1, y1 = end
    dx, dy = x1 - x0, y1 - y0
    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    ux, uy = dx / dist, dy / dist
    curr_dist = 0
    while curr_dist < dist:
        sx = x0 + ux * curr_dist
        sy = y0 + uy * curr_dist
        curr_dist = min(curr_dist + dash_len, dist)
        ex = x0 + ux * curr_dist
        ey = y0 + uy * curr_dist
        draw.line([sx, sy, ex, ey], fill=color, width=width)
        curr_dist += gap_len


@mcp.tool()
def reset() -> dict:
    """Reset the PyMOL session - delete all objects and clear settings."""
    try:
        cmd = _pymol()
        cmd.reinitialize()
        return _ok()
    except Exception as exc:
        return _err(f"重置失败 {type(exc).__name__}: {exc}")


# --------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------

def _selftest() -> int:
    print("=== PyMOL MCP Server Self-test ===")
    print(f"Python      : {sys.executable}")
    print(f"Python Version: {sys.version.split()[0]}")
    try:
        import mcp as _m
        print(f"mcp Version   : {getattr(_m, '__version__', 'unknown')}")
    except Exception as exc:
        print(f"mcp import failed: {exc}")
    try:
        cmd = _pymol()
        print("PyMOL import success OK")
    except Exception as exc:
        print(f"PyMOL import failed: {exc}")
        return 1

    # List registered tools
    names = sorted(
        n for n, v in globals().items()
        if callable(v) and getattr(v, "__module__", None) == __name__ and not n.startswith("_")
    )
    print("\nRegistered MCP Tools:")
    for n in names:
        if n in {"main"}:
            continue
        doc = (globals()[n].__doc__ or "").strip().splitlines()
        print(f"  - {n:20s} {doc[0] if doc else ''}")
    print("\nSelf-test completed.")
    return 0


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="PyMOL MCP Server")
    ap.add_argument("--selftest", action="store_true", help="只做自检而不启动服务器")
    args = ap.parse_args()
    if args.selftest:
        return _selftest()
    mcp.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())

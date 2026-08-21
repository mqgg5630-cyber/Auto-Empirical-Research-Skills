---
name: pymol-docking-viz
description: Professional SCI-grade molecular docking visualization and dual-object polar contact analysis using PyMOL. Supports physical PDB splitting (lig.pdb + pro.pdb), native mode=2 polar contact measurement, cyan stick residue highlighting, and floating bold halo labels.
---

# PyMOL Molecular Docking Visualization Skill

## Overview
This skill implements the **Golden Standard Workflow** for publication-quality SCI molecular docking visualization and hydrogen bond interaction analysis.

---

## Core Architecture & Guidelines

### 1. Dual-Object Architecture (Never keep as single object)
Always split the complex into two distinct physical files or PyMOL objects:
- **`pro` (Receptor)**: Chain A (shown as `forest` green cartoon with `cartoon_transparency 0.45-0.50`).
- **`lig` (Ligand)**: Chain B (shown as `red` sticks, `stick_radius 0.25-0.28`).

> Why this matters: PyMOL's `find → polar contacts → within selection` measures the
> ligand against **itself**, which for a helical peptide yields a pile of i→i+4
> backbone hydrogen bonds that look like "the peptide bonding to itself".
> Splitting into two objects makes intramolecular contacts structurally impossible.

### 2. Native Polar Contact Detection (`mode=2`)
PyMOL's native `mode=2` calculates geometrically accurate hydrogen bonds and salt bridges with strict angle/donor-acceptor validation:
```python
cmd.distance('lig_polar_conts', 'lig', 'pro', mode=2)
cmd.color('yellow', 'lig_polar_conts')
cmd.set('dash_gap', 0.25, 'lig_polar_conts')
cmd.set('dash_width', 4.5, 'lig_polar_conts')
cmd.set('dash_radius', 0.07, 'lig_polar_conts')
```

> Never test the return value of `cmd.distance()` to decide whether contacts were
> found — it returns the **mean distance**, not a count.

### 3. Programmatic Interacting Residue Extraction
Extract only the exact receptor residue numbers connected to the distance object endpoints:
```python
session = cmd.get_session('lig_polar_conts', 1, 1, 0, 0)
points = session["names"][0][5][2][0][1]
# Map endpoints to atom residue numbers
```

> When explicit hydrogens are present, these endpoint distances are **H···A**
> (typically 1.6–2.5 Å). Journals report **D···A** heavy-atom distances
> (typically 2.6–3.2 Å). Convert the hydrogen endpoint to its bonded heavy atom
> before writing numbers into a manuscript. Any heavy-atom pair below 2.2 Å is a
> steric clash, not a hydrogen bond.

### 4. Highlighting & Label Styling
- **Cyan Sticks for interacting residues**:
  ```python
  cmd.select('res', f'pro and resi {"+".join(rec_resi_list)}')
  cmd.show('sticks', 'res')
  cmd.color('cyan', 'res')
  cmd.set('stick_radius', 0.22, 'res')
  ```
- **High-visibility Floating Labels (No Occlusion / No Clipping)**:
  ```python
  cmd.label('res and name CA', '"%s-%s" % (resn.upper(), resi)')
  cmd.set('label_font_id', 7)             # Helvetica Bold
  cmd.set('label_size', 20)               # Large readable size
  cmd.set('label_color', 'black')         # Deep black text
  cmd.set('label_outline_color', 'white') # White halo outline
  cmd.set('float_labels', 1)              # Always on top of 3D geometry
  cmd.set('label_shadow_mode', 0)
  ```

> `cmd.hide('everything')` also hides distance objects. If dashes disappear after
> styling, re-enable them explicitly with `cmd.show('dashes', obj)`.

### 5. Dual-Panel SCI Composite Layout
- **Left Panel (Overview)**: Full receptor in solid cartoon + Red ligand + Exact pixel-mask bounding box.
- **Right Panel (Detail)**: Binding site focused with `buffer 3.2-3.6` (prevents border clipping), semi-transparent receptor, yellow dashed lines, and cyan residue sticks.
- **Connecting Lines**: Purple dashed lines (`#7F3F98`, width 3) linking the left bounding box to the right panel.

---

## MCP Server Tools Available

When `pymol_mcp` is running, call:
1. `split_complex_pdb(complex_path, output_dir)`: Physically splits into `lig.pdb` and `pro.pdb`.
2. `render_sci_docking_composite(complex_path, output_png, output_pse)`: Generates full dual-panel image and interactive `.pse` session.
3. `load_pdb`, `save_image`, `align_structures`, `set_view`, `get_view`, `reset`.

Server implementation: `examples/mcp-servers/pymol_mcp/pymol_mcp.py` in this repository.

## Verification Requirements

Before accepting any generated figure:

1. Run `python pymol_mcp.py --selftest` and confirm PyMOL imports and all tools are listed.
2. Check the returned `hydrogen_bonds` list — a 7-residue peptide interface should
   have roughly 3–10 contacts, not 40+.
3. Reject any reported distance below 2.2 Å between heavy atoms.
4. Confirm every yellow dash in the figure connects the ligand to the receptor,
   not two receptor residues to each other.

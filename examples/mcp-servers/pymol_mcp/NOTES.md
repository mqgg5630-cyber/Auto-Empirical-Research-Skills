# pymol_mcp.py 代码审阅记录

对照 `skills/77-research-software-to-mcp` 的规范做的检查。**当前版本功能可用**，
以下是建议改进项，按严重程度排序。

## 检查器输出

```
$ python check_mcp_server.py pymol_mcp.py
  [ERROR] E3:193  subprocess.run 缺少 timeout 参数
  [ERROR] E3:189  subprocess.run 缺少 timeout 参数
  [WARN]  W4      缺少 *_info 环境自检工具
合计：2 个 ERROR，1 个 WARN
```

## 1. 导入失败时未 re-raise（实测复现）

```python
except ModuleNotFoundError as exc:
    sys.stderr.write("无法导入 mcp.server.fastmcp ...")
    # 缺 raise
mcp = FastMCP("pymol")     # ← NameError: name 'FastMCP' is not defined
```

实测：mcp 未安装时，精心写的提示信息会被后面的 `NameError` 淹没，
客户端只看到一行 traceback。

建议在 `sys.stderr.write(...)` 之后补一行 `raise`。

## 2. subprocess 无 timeout（第 189、193 行）

`render_movie` 里两处 `subprocess.run` 都没有 `timeout`。
ffmpeg 编码卡住会让整个 MCP 调用永久挂起，客户端只能超时断连。

建议：`subprocess.run([...], timeout=600, check=True)`，
并把 `FileNotFoundError`（ffmpeg 不存在）单独捕获。

## 3. 缺少 `pymol_info` 工具

排障时 Agent 无从下手。建议补一个返回 PyMOL 版本、解释器路径、
Pillow/ffmpeg 是否可用的工具。

## 4. `render_sci_docking_composite` 里的两个脆弱点

```python
session_data = cmd.get_session("lig_polar_conts", 1, 1, 0, 0)
points = session_data["names"][0][5][2][0][1]
```

- 硬编码 `names[0]`：假设距离对象排在第一个。会话里有其他对象时会取错。
  建议遍历 `names` 并按名字匹配。
- `points` 可能为 `None`（一条接触都没有时），当前会抛 `TypeError`
  被外层 except 吞掉，返回一句笼统的错误。建议显式判断并返回
  "未检出极性接触" 这样可执行的信息。

## 5. 受体选择建议

`split_complex_pdb` 用 `chain A` 指定受体。如果受体本身是多链复合物
（A/C/D 等），只会导出 A 链。更稳的写法：

```python
cmd.save(pro_pdb, f"complex_tmp and polymer and not chain {ligand_chain}")
```

## 6. 数值口径提醒

`hydrogen_bonds` 里返回的 `distance` 是**虚线端点距离**。结构带显式氢时
这是 H···A（典型 1.6–2.5 Å），而论文报告的是 D···A 重原子距离
（典型 2.6–3.2 Å）。写进稿件前需要把氢换算回所连的重原子。
参见 `examples/pymol/dump_contacts.py` 的实现。

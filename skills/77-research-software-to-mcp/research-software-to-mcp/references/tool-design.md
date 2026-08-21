# 工具设计规范

## 命名

- 用 `动词_名词`：`load_table`、`cross_validate`、`export_result`
- 同一服务器内保持统一前缀风格，便于 Agent 在几十个工具里定位
- 避免 `get_data` 这类含义空泛的名字

## docstring 就是接口契约

Agent 判断「什么时候调用哪个工具」的唯一依据就是 docstring。必须写清：

1. 这个工具做什么（第一行，会显示在工具列表里）
2. 每个参数的含义、单位、允许取值
3. 返回什么

```python
@mcp.tool()
def cluster_sequences(fasta_path: str, identity: float = 0.4,
                      output_path: str = "") -> dict:
    """用 CD-HIT 对蛋白序列做同源冗余去除，返回代表序列与簇归属。

    fasta_path:  输入 FASTA 的绝对路径
    identity:    相似度阈值，0.4-1.0；0.4 严格（跨簇差异大），0.9 宽松
    output_path: 代表序列输出路径；留空则只返回统计不写文件
    """
```

## 返回结构化数据

```python
# 好
return {"ok": True, "n_clusters": 812, "n_input": 5031, "reduction": 0.839}

# 差
return "聚类完成，从 5031 条序列中得到 812 个簇，压缩率 83.9%"
```

结构化返回让 Agent 能直接取字段做后续判断；散文需要它二次解析，容易出错。

统一用两个辅助函数保持形状一致：

```python
def _ok(**payload):  return {"ok": True, **payload}
def _err(msg, **kw): return {"ok": False, "error": msg, **kw}
```

## 用注册表约束选项

不要让 Agent 猜类名。把合法取值写成模块级字典，并在参数校验失败时把清单返回给它：

```python
CLASSIFIERS = {
    "logistic": ("Orange.classification", "LogisticRegressionLearner"),
    "random_forest": ("Orange.classification", "RandomForestLearner"),
}

if name not in CLASSIFIERS:
    return _err(f"未知学习器 '{name}'，可选：{sorted(CLASSIFIERS)}")
```

## 错误信息要可执行

Agent 拿到错误后要能自我修正，所以错误信息必须说明「下一步该怎么做」：

```python
# 好
"未检测到 Orange3。请在本服务器所用的 Python 环境执行 pip install Orange3，"
"并确认 mcp_config.json 的 command 指向该环境的 python.exe"

# 差
"ImportError"
```

## 粒度：一个工具一件事

反面教材：

```python
@mcp.tool()
def run(command: str) -> str:   # ❌ 命令注入 + Agent 用不明白
    return subprocess.run(command, shell=True, capture_output=True).stdout
```

正面：把常用操作拆成 5–8 个语义明确的工具。工具太少 Agent 会滥用万能接口，
太多（超过 20 个）又会稀释它的注意力。

## 必备的 info 工具

每个服务器都应该有一个：

```python
@mcp.tool()
def xxx_info() -> dict:
    """检查环境：返回软件版本、解释器路径、可用能力清单。排查问题时先调这个。"""
```

它是排障的第一站，也能让 Agent 在动手前确认环境就绪。

## 分页与截断

返回可能很大的结果（表格行、序列、日志）时提供 `limit` / `offset`，
并在返回里标注 `truncated: true`。不要一次把上万行塞进上下文。

## 读写分离

只读工具和写文件工具分开。写工具的输出路径必须由调用方显式给出，
不要有「默认写到当前目录」这种行为。

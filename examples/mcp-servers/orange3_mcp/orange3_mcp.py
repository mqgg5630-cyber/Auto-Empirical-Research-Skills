#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orange3 MCP Server
==================

把 Orange3（https://orangedatamining.com）的 Python API 包装成 MCP 工具，
让 Antigravity / Claude Code / VS Code 里的 Agent 可以直接调用 Orange 做
数据加载、描述统计、特征打分、交叉验证建模和预测导出。

设计原则
--------
1. **懒加载**：Orange 只在真正用到时才 import，因此即使没装 Orange，
   MCP 服务器本身也能启动并给出清晰的安装提示（而不是直接崩溃）。
2. **只读优先**：默认不写任何文件；需要落盘的工具必须显式传出路径。
3. **结构化返回**：所有工具返回 dict（会被序列化成 JSON），便于 Agent 解析，
   而不是返回一大段人类可读文本。
4. **锁定 mcp<2**：MCP Python SDK 2.0 移除了 mcp.server.fastmcp，
   启动命令必须写 `uvx --with "mcp<2" ...` 或在环境里装 mcp>=1.28,<2。

启动
----
    python orange3_mcp.py                 # 以 stdio 方式启动 MCP 服务器
    python orange3_mcp.py --selftest      # 不启动服务器，只自检环境与工具清单

在 Antigravity 中注册（~/.gemini/config/mcp_config.json）
--------------------------------------------------------
    {
      "mcpServers": {
        "orange3": {
          "command": "C:/Users/你/miniconda3/envs/orange/python.exe",
          "args": ["E:/mcp-servers/orange3_mcp/orange3_mcp.py"]
        }
      }
    }

注意 command 要指向**装了 Orange3 的那个 Python 解释器**（通常是一个专用 conda 环境），
并且必须是绝对路径。
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Any

try:
    from mcp.server.fastmcp import FastMCP
except ModuleNotFoundError as exc:  # pragma: no cover
    sys.stderr.write(
        "无法导入 mcp.server.fastmcp。\n"
        "原因：MCP Python SDK 2.0（2026-07-28 发布）把该模块迁移到了 mcp.server.mcpserver。\n"
        '解决：pip install "mcp>=1.28,<2"，或用 uvx --with "mcp<2" 启动。\n'
        f"原始错误：{exc}\n"
    )
    raise

mcp = FastMCP("orange3")

# --------------------------------------------------------------------------
# 内部工具
# --------------------------------------------------------------------------

_INSTALL_HINT = (
    "未检测到 Orange3。请在本 MCP 服务器所用的 Python 环境里安装：\n"
    "    conda create -n orange python=3.11 -y\n"
    "    conda activate orange\n"
    "    pip install Orange3\n"
    "然后把 mcp_config.json 里的 command 指向该环境的 python.exe。"
)


def _orange():
    """懒加载 Orange，未安装时抛出带安装指引的异常。"""
    try:
        import Orange  # noqa: F401
    except ModuleNotFoundError as exc:
        raise RuntimeError(_INSTALL_HINT) from exc
    return sys.modules["Orange"]


def _err(msg: str, **extra: Any) -> dict:
    out = {"ok": False, "error": msg}
    out.update(extra)
    return out


def _ok(**payload: Any) -> dict:
    out = {"ok": True}
    out.update(payload)
    return out


# 允许 Agent 按名字选择学习器，避免它凭空猜类名
CLASSIFIERS = {
    "logistic": ("Orange.classification", "LogisticRegressionLearner"),
    "random_forest": ("Orange.classification", "RandomForestLearner"),
    "tree": ("Orange.classification", "TreeLearner"),
    "knn": ("Orange.classification", "KNNLearner"),
    "svm": ("Orange.classification", "SVMLearner"),
    "naive_bayes": ("Orange.classification", "NaiveBayesLearner"),
    "gradient_boosting": ("Orange.classification", "GBLearner"),
    "neural_network": ("Orange.classification", "NNClassificationLearner"),
}

REGRESSORS = {
    "linear": ("Orange.regression", "LinearRegressionLearner"),
    "ridge": ("Orange.regression", "RidgeRegressionLearner"),
    "random_forest": ("Orange.regression", "RandomForestRegressionLearner"),
    "tree": ("Orange.regression", "TreeLearner"),
    "svm": ("Orange.regression", "SVRLearner"),
    "knn": ("Orange.regression", "KNNRegressionLearner"),
}

SCORERS = {
    "info_gain": "InfoGain",
    "gain_ratio": "GainRatio",
    "gini": "Gini",
    "relieff": "ReliefF",
    "fcbf": "FCBF",
    "chi2": "Chi2",
    "anova": "ANOVA",
}


def _build_learner(name: str, task: str, params: dict | None):
    import importlib

    registry = CLASSIFIERS if task == "classification" else REGRESSORS
    if name not in registry:
        raise ValueError(
            f"未知的学习器 '{name}'（task={task}）。可选：{sorted(registry)}"
        )
    module_name, cls_name = registry[name]
    module = importlib.import_module(module_name)
    cls = getattr(module, cls_name)
    learner = cls(**(params or {}))
    learner.name = name
    return learner


def _load(path: str):
    Orange = _orange()
    if not os.path.exists(path) and not path.endswith((".tab", ".csv", ".xlsx")):
        # 允许直接用 Orange 自带数据集名，如 "iris" / "titanic" / "heart_disease"
        return Orange.data.Table(path)
    if not os.path.exists(path):
        raise FileNotFoundError(f"找不到文件：{path}")
    return Orange.data.Table(path)


def _domain_summary(table) -> dict:
    d = table.domain
    return {
        "n_rows": len(table),
        "n_features": len(d.attributes),
        "features": [
            {"name": v.name, "type": type(v).__name__} for v in d.attributes
        ][:200],
        "class_var": (
            {
                "name": d.class_var.name,
                "type": type(d.class_var).__name__,
                "values": list(getattr(d.class_var, "values", []) or []),
            }
            if d.class_var is not None
            else None
        ),
        "metas": [v.name for v in d.metas],
    }


# --------------------------------------------------------------------------
# MCP 工具
# --------------------------------------------------------------------------


@mcp.tool()
def orange_info() -> dict:
    """检查 Orange3 环境：返回版本号、Python 解释器路径、可用的学习器与打分方法清单。
    排查问题时先调用这个。"""
    info: dict[str, Any] = {
        "python": sys.executable,
        "python_version": sys.version.split()[0],
        "classifiers": sorted(CLASSIFIERS),
        "regressors": sorted(REGRESSORS),
        "feature_scorers": sorted(SCORERS),
    }
    try:
        Orange = _orange()
        info["orange_version"] = getattr(Orange, "__version__", "unknown")
        info["orange_installed"] = True
    except RuntimeError as exc:
        info["orange_installed"] = False
        info["hint"] = str(exc)
        return _err("Orange3 未安装", **info)
    return _ok(**info)


@mcp.tool()
def load_table(path: str) -> dict:
    """加载数据表并返回结构摘要（行数、特征名与类型、目标变量、meta 列）。

    path 可以是 .tab / .csv / .xlsx 文件路径，也可以是 Orange 自带数据集名
    （如 iris、titanic、heart_disease、housing）。
    """
    try:
        table = _load(path)
    except Exception as exc:
        return _err(str(exc))
    return _ok(source=path, **_domain_summary(table))


@mcp.tool()
def describe_data(path: str, max_features: int = 50) -> dict:
    """对数据做描述统计：连续变量给 min/max/mean/std/缺失率，离散变量给各取值频数。"""
    try:
        table = _load(path)
        Orange = _orange()
        import numpy as np
    except Exception as exc:
        return _err(str(exc))

    stats = []
    for i, var in enumerate(table.domain.attributes[:max_features]):
        col = table.X[:, i]
        missing = float(np.isnan(col).mean()) if col.dtype.kind == "f" else 0.0
        if var.is_continuous:
            valid = col[~np.isnan(col)]
            stats.append(
                {
                    "name": var.name,
                    "kind": "continuous",
                    "min": float(np.min(valid)) if valid.size else None,
                    "max": float(np.max(valid)) if valid.size else None,
                    "mean": float(np.mean(valid)) if valid.size else None,
                    "std": float(np.std(valid)) if valid.size else None,
                    "missing_rate": round(missing, 4),
                }
            )
        else:
            valid = col[~np.isnan(col)].astype(int)
            counts = {
                var.values[v]: int((valid == v).sum())
                for v in range(len(var.values))
            }
            stats.append(
                {
                    "name": var.name,
                    "kind": "discrete",
                    "counts": counts,
                    "missing_rate": round(missing, 4),
                }
            )

    target = None
    if table.domain.class_var is not None and table.domain.class_var.is_discrete:
        import numpy as np

        y = table.Y[~np.isnan(table.Y)].astype(int)
        target = {
            table.domain.class_var.values[v]: int((y == v).sum())
            for v in range(len(table.domain.class_var.values))
        }

    return _ok(
        source=path,
        n_rows=len(table),
        n_features=len(table.domain.attributes),
        feature_stats=stats,
        class_distribution=target,
        truncated=len(table.domain.attributes) > max_features,
    )


@mcp.tool()
def feature_scores(path: str, method: str = "info_gain", top_n: int = 20) -> dict:
    """用信息增益等方法给特征打分排序，用于特征筛选。

    method 可选：info_gain、gain_ratio、gini、relieff、fcbf、chi2、anova。
    """
    if method not in SCORERS:
        return _err(f"未知的打分方法 '{method}'，可选：{sorted(SCORERS)}")
    try:
        table = _load(path)
        Orange = _orange()
        scorer_cls = getattr(Orange.preprocess.score, SCORERS[method])
        scorer = scorer_cls()
        scores = [(var.name, float(scorer(table, var))) for var in table.domain.attributes]
    except Exception as exc:
        return _err(f"{type(exc).__name__}: {exc}")

    scores.sort(key=lambda x: x[1], reverse=True)
    return _ok(
        source=path,
        method=method,
        top_features=[{"name": n, "score": round(s, 6)} for n, s in scores[:top_n]],
        n_scored=len(scores),
    )


@mcp.tool()
def cross_validate(
    path: str,
    learners: list[str] | None = None,
    task: str = "classification",
    k: int = 5,
    random_state: int = 42,
    learner_params: dict | None = None,
) -> dict:
    """对一个或多个学习器做 k 折交叉验证并返回指标对比。

    分类返回 CA / AUC / F1 / Precision / Recall / MCC；回归返回 RMSE / MAE / R2。
    learners 例：["logistic", "random_forest", "svm"]；不传则用一组默认基线。
    """
    if task not in ("classification", "regression"):
        return _err("task 只能是 classification 或 regression")
    if learners is None:
        learners = (
            ["logistic", "random_forest", "tree"]
            if task == "classification"
            else ["linear", "random_forest"]
        )
    try:
        table = _load(path)
        Orange = _orange()
        built = [_build_learner(n, task, (learner_params or {}).get(n)) for n in learners]
        cv = Orange.evaluation.CrossValidation(k=k, random_state=random_state)
        res = cv(table, built)
    except Exception as exc:
        return _err(f"{type(exc).__name__}: {exc}")

    ev = Orange.evaluation
    rows = []
    try:
        if task == "classification":
            metrics = {
                "CA": ev.CA(res),
                "AUC": ev.AUC(res),
                "F1": ev.F1(res, average="macro"),
                "Precision": ev.Precision(res, average="macro"),
                "Recall": ev.Recall(res, average="macro"),
            }
            try:
                metrics["MCC"] = ev.MatthewsCorrCoefficient(res)
            except Exception:
                pass
        else:
            metrics = {"RMSE": ev.RMSE(res), "MAE": ev.MAE(res), "R2": ev.R2(res)}
        for i, name in enumerate(learners):
            rows.append(
                {"learner": name, **{m: round(float(v[i]), 4) for m, v in metrics.items()}}
            )
    except Exception as exc:
        return _err(f"指标计算失败 {type(exc).__name__}: {exc}")

    return _ok(source=path, task=task, k=k, random_state=random_state, results=rows)


@mcp.tool()
def train_and_predict(
    train_path: str,
    test_path: str,
    learner: str = "random_forest",
    task: str = "classification",
    output_csv: str | None = None,
    learner_params: dict | None = None,
) -> dict:
    """在训练集上拟合模型，对测试集预测，可选把预测结果写成 CSV。

    output_csv 为 None 时只返回前 20 条预测的预览，不写任何文件。
    """
    try:
        train = _load(train_path)
        test = _load(test_path)
        model = _build_learner(learner, task, learner_params)(train)
        preds = model(test)
    except Exception as exc:
        return _err(f"{type(exc).__name__}: {exc}")

    class_var = train.domain.class_var
    if task == "classification" and class_var is not None:
        labels = [class_var.values[int(p)] for p in preds]
    else:
        labels = [float(p) for p in preds]

    written = None
    if output_csv:
        try:
            import csv

            os.makedirs(os.path.dirname(os.path.abspath(output_csv)), exist_ok=True)
            with open(output_csv, "w", newline="", encoding="utf-8") as fh:
                w = csv.writer(fh)
                w.writerow(["index", "prediction"])
                for i, lab in enumerate(labels):
                    w.writerow([i, lab])
            written = os.path.abspath(output_csv)
        except Exception as exc:
            return _err(f"写文件失败 {type(exc).__name__}: {exc}")

    return _ok(
        learner=learner,
        task=task,
        n_train=len(train),
        n_test=len(test),
        preview=labels[:20],
        output_csv=written,
    )


@mcp.tool()
def open_workflow_in_gui(ows_path: str, orange_python: str | None = None) -> dict:
    """在 Orange 图形界面中打开一个 .ows 工作流文件（非阻塞启动）。

    说明：Orange 的 .ows 工作流没有官方的无头批处理执行接口，
    因此这里只负责把它在 GUI 里打开，供你人工查看/运行。
    需要可脚本化的分析请用 cross_validate / train_and_predict。
    """
    if not os.path.exists(ows_path):
        return _err(f"找不到工作流文件：{ows_path}")
    exe = orange_python or sys.executable
    try:
        subprocess.Popen(
            [exe, "-m", "Orange.canvas", ows_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception as exc:
        return _err(f"启动失败 {type(exc).__name__}: {exc}")
    return _ok(
        opened=os.path.abspath(ows_path),
        note="已在后台启动 Orange 画布；.ows 无官方无头执行接口，需人工在 GUI 中运行。",
    )


# --------------------------------------------------------------------------
# 自检
# --------------------------------------------------------------------------


def _selftest() -> int:
    print("=== Orange3 MCP Server 自检 ===")
    print(f"Python      : {sys.executable}")
    print(f"Python 版本 : {sys.version.split()[0]}")
    try:
        import mcp as _m

        print(f"mcp 版本    : {getattr(_m, '__version__', 'unknown')}")
    except Exception as exc:
        print(f"mcp         : 导入失败 {exc}")
    try:
        Orange = _orange()
        print(f"Orange3     : {getattr(Orange, '__version__', 'unknown')}  ✓")
        try:
            t = Orange.data.Table("iris")
            print(f"内置数据集  : iris 加载成功（{len(t)} 行）✓")
        except Exception as exc:
            print(f"内置数据集  : 加载失败 {exc}")
    except RuntimeError as exc:
        print("Orange3     : 未安装  ✗")
        print(exc)
    names = sorted(
        n
        for n, v in globals().items()
        if callable(v) and getattr(v, "__module__", None) == __name__ and not n.startswith("_")
    )
    print("\n已注册的 MCP 工具：")
    for n in names:
        if n in {"main"}:
            continue
        doc = (globals()[n].__doc__ or "").strip().splitlines()
        print(f"  - {n:22s} {doc[0] if doc else ''}")
    print("\n自检完成。若 Orange3 显示未安装，请见上方安装提示。")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Orange3 MCP Server")
    ap.add_argument("--selftest", action="store_true", help="只做环境自检，不启动服务器")
    args = ap.parse_args()
    if args.selftest:
        return _selftest()
    mcp.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

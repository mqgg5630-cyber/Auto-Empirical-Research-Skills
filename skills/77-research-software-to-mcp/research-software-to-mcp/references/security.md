# 安全清单

MCP 客户端**不会**替你沙箱化服务器。Anthropic 官方 `build-mcpb` skill 里写得
很直白：manifest 没有 permissions 块，进程以完整用户权限运行，
路径校验和 spawn 白名单是作者的责任。科研数据常涉及保密协议与个人信息，
这一节不是可选项。

## 1. 子进程

```python
subprocess.run([exe, *args], shell=False, timeout=300, capture_output=True)
```

- `shell=False` + argv 数组，杜绝命令注入
- 必须设 `timeout`
- 可执行文件用 `shutil.which()` 解析或写死绝对路径，不要接受调用方传入任意 exe

## 2. 路径校验

Agent 传来的路径可能包含 `../`。凡是要读写的路径都做规范化并限定在允许目录内：

```python
def _safe_path(user_path: str, root: str) -> str:
    full = os.path.realpath(os.path.join(root, user_path))
    if not full.startswith(os.path.realpath(root) + os.sep):
        raise ValueError(f"路径越界：{user_path}")
    return full
```

## 3. 写操作

- 输出路径必须显式传入
- 不默认覆盖已存在文件，或至少在返回里明确告知覆盖了什么
- 删除类操作：要么不提供，要么要求一个 `confirm=True` 参数

## 4. 密钥

- 从环境变量读，不要写死在源码里
- 不要 print / log / 返回密钥值
- 报错信息里做脱敏（DSN 里的密码尤其容易泄漏进日志）

## 5. 提示注入

网页、PDF、issue 里可能藏有针对 AI 的指令。风险来自「能读外部内容」+
「能写本地」两类工具的组合。

- 抓取类与写盘/数据库类不要给同一个 Agent 会话
- 保持工具调用需人工确认，别无脑点 Always Allow
- 反重力可用权限策略精确放行：`mcp(server/tool)` 而不是 `mcp(*)`

## 6. 数据库

- 只读连接或只读账号
- DBHub 新版的只读写在 `dbhub.toml` 的 `[[tools]]` 段（`--readonly` 参数已废弃）
- 含个人隐私的微观数据优先本地库 + 脱敏视图，敏感字段不暴露给 MCP

## 7. 依赖

- `mcp>=1.28,<2`，理由见 RESOURCES.md
- 第三方 MCP 服务器安装前过一遍源码，尤其是会写文件、发网络请求的部分
- 注册表内（github.com/mcp）的条目经过审核，社区项目自行评估

## 8. 学术场景补充

- 未发表的数据与代码：让 Agent 操作 GitHub 前先确认仓库为 private
- 所有进论文的数字必须人工重跑脚本确认，不能直接采信 Agent 的报告
- 期刊多要求披露 AI 使用情况，建议保留工具调用日志

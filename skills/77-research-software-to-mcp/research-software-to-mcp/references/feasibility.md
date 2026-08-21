# 可行性判断：五条集成路径

按 A → E 顺序检查，命中第一条就停。

## A. Python API（最优）

**判据**：`pip install X` 后能 `import X`，且有脚本化接口（不只是 GUI 入口）。

**做法**：函数内部懒加载，直接调库。

```python
def _lib():
    try:
        import Orange
    except ModuleNotFoundError as exc:
        raise RuntimeError(INSTALL_HINT) from exc
    return sys.modules["Orange"]
```

**坑**：
- 有些包 import 时会拉起 Qt（Orange、napari）。在无显示环境要设 `QT_QPA_PLATFORM=offscreen`。
- 版本 API 变动频繁的库，在 `*_info` 工具里返回版本号，方便排查。

## B. 命令行 CLI

**判据**：装完有可执行文件，且支持非交互批处理参数。

**做法**：`subprocess.run(argv_list, shell=False, timeout=..., capture_output=True)`。

```python
proc = subprocess.run([exe, "-i", inp, "-o", outp, "-c", str(threshold)],
                      capture_output=True, text=True, timeout=600, shell=False)
```

**坑**：
- 绝不用 `shell=True`。参数来自 Agent，等于把命令注入的口子敞开。
- 长任务（GROMACS、大规模比对）必须设 timeout，或改成「提交 + 轮询状态」两个工具。
- stdout 可能极大，截断后再返回（例如末尾 8000 字符）。
- 退出码非 0 时把 stderr 一并返回，Agent 需要它来自我修正。

## C. 本地 REST

**判据**：软件自带 HTTP 服务（Cytoscape CyREST 1234、ChimeraX remotecontrol）。

**做法**：`requests` 调用，MCP 工具只做参数校验和结果整形。

**坑**：
- 端口被占用或服务未启动时给出清晰提示，别让 Agent 看到裸的 ConnectionError。
- 这类服务通常无鉴权且监听 localhost，不要暴露到公网。

## D. COM 自动化（仅 Windows）

**判据**：软件注册了 COM 接口（Origin、SPSS、Office、MATLAB）。

**做法**：`pywin32` 的 `win32com.client.Dispatch("Origin.Application")`。

**坑**：
- 需要软件已安装且注册；不同版本的 ProgID 可能不同。
- COM 对象要显式释放，否则会留下僵尸进程。
- 只在 Windows 可用，README 里必须写明平台限制。

## E. 纯 GUI，无任何接口

**不要封装。** 截图 + 点击的 UI 自动化：

- 软件一更新布局就全废
- 分辨率、缩放、主题都会影响
- 调试成本远高于人工操作

正确回应是告诉用户「这个软件没有可脚本化接口，建议保持手工操作」，
而不是硬做一个三天后就坏掉的东西。

## 判断示例

| 软件 | 检查 | 结论 |
|---|---|---|
| Orange3 | `pip install Orange3; python -c "import Orange"` 成功 | A |
| CD-HIT | `cd-hit -h` 有输出 | B |
| Cytoscape | `curl http://localhost:1234/v1/version` 返回 JSON | C |
| Origin | `python -c "import OriginExt"` 成功且已装 Origin | D |
| 某老旧商业分析软件 | 三项都失败 | E，劝退 |

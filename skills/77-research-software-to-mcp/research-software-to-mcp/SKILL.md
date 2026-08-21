---
name: research-software-to-mcp
description: Use when the user wants to expose a research or office application (Orange3, ImageJ, CD-HIT, BLAST+, Cytoscape, Origin, PyMOL, GROMACS, a lab-internal CLI, etc.) to an AI agent as an MCP server — covering feasibility triage, tool design, implementation, real-data verification, and client registration for Antigravity / Claude Code / VS Code.
---

# Research Software → MCP

Wrap an existing scientific or office application as a Model Context Protocol
server so an agent can drive it directly, instead of the agent guessing at
shell commands or the user copy-pasting between a GUI and the chat window.

The deliverable of this skill is always the same three things: a working
server file, a real-data verification transcript, and a client config snippet.
A server that has not been run against real data is not done.

## Required workflow

### Phase 1 — Feasibility triage (do this before writing any code)

1. Identify which integration path the target software offers. Check in this
   order and stop at the first hit:

   | Path | Evidence | Difficulty |
   |---|---|---|
   | A. Python API | `pip install X` then `import X` works | lowest |
   | B. Command line | ships an executable with batch/headless flags | low |
   | C. Local REST | exposes an HTTP port (CyREST, ChimeraX remotecontrol) | low |
   | D. COM automation | Windows only, drivable via `pywin32` | medium |
   | E. GUI only | none of the above | do not wrap |

2. If the answer is E, say so plainly and stop. GUI/screenshot automation is
   brittle, breaks on every software update, and costs more to maintain than
   the manual workflow it replaces. Recommend the manual path instead.

3. Search for an existing server before building one. Check `github.com/mcp`,
   the target project's own repository, and `references/RESOURCES.md` in this
   skill. Do not rebuild `excel-mcp-server`, `office-word-mcp-server`,
   `mcp-stata`, or `zotero-mcp`.

4. Read `references/feasibility.md` for path-specific gotchas.

### Phase 2 — Tool design (get approval before implementing)

5. Draft 5–8 tools and present them to the user as a table of
   name / purpose / parameters / return shape / read-or-write. Wait for
   confirmation. Designing on paper is far cheaper than rewriting code.

6. Apply these design rules:
   - One tool does one thing. Never expose a generic `run_anything(command)` —
     it is both a command-injection hole and something agents use incorrectly.
   - Always include an `*_info` tool that reports version, interpreter path,
     and available capabilities. It is the first thing to call when debugging.
   - The docstring is the entire interface contract the agent sees. State the
     purpose, every parameter's meaning, and the units or allowed values.
   - Return `dict`, not prose. Structured output is parsed far more reliably.
   - Enumerate valid choices in a module-level registry (learners, formats,
     methods) so the agent selects from a list instead of guessing class names.

7. Read `references/tool-design.md` before writing the table.

### Phase 3 — Implementation

8. Copy `scripts/template_mcp.py` as the starting skeleton. Then:
   - Pin the SDK: `mcp>=1.28,<2`. SDK 2.0 removed `mcp.server.fastmcp`, so an
     unbounded requirement breaks the server without warning.
   - Import the target library lazily inside functions, so a missing install
     produces a readable hint instead of a dead process.
   - `subprocess` must use `shell=False`, an argv list, and an explicit
     `timeout`.
   - Any tool that writes must take an explicit output path. Never overwrite
     by default, never write into the current directory implicitly.
   - Provide a `--selftest` flag that checks the environment and lists tools
     without starting the server.

9. Read `references/security.md`. Path validation and spawn allowlisting are
   the author's responsibility — no MCP client sandboxes this for you.

### Phase 4 — Verification (mandatory, not optional)

10. Run `python <server>.py --selftest` and paste the output.
11. Call **every** tool against real data and paste the actual returned values.
    Claiming "this should work" without a transcript fails this skill.
12. Run `scripts/check_mcp_server.py <server>.py` to lint the conventions
    above (SDK pin, lazy import, shell=False, timeout, selftest, docstrings).
13. Optionally exercise the wire protocol with
    `npx @modelcontextprotocol/inspector python <server>.py`.

### Phase 5 — Registration and handoff

14. Emit the client config snippet for the user's client. The formats differ:

    - Antigravity: `~/.gemini/config/mcp_config.json`, top key `mcpServers`,
      remote servers use `serverUrl`
    - Claude Code / Claude Desktop: top key `mcpServers`
    - VS Code: `.vscode/mcp.json`, top key `servers`, remote uses `type`+`url`

15. `command` must be the absolute path to the interpreter that has the target
    software installed — typically a dedicated conda environment, not `base`.
    Agent IDEs frequently do not inherit the shell `PATH`.

16. Write a short README covering install, selftest, registration, and the
    three most likely failure modes.

## Environment isolation

Give each wrapped application its own environment. Dependency conflicts
between scientific packages are the norm, not the exception.

```bash
conda create -n orange python=3.11 -y
conda activate orange
pip install Orange3 "mcp>=1.28,<2"
where python          # Windows — this absolute path goes in the config
```

## Anti-patterns

Do not do any of the following:

- Wrap software that has no programmatic interface.
- Expose a shell passthrough tool.
- Let the `mcp` dependency float above 2.0.
- Import the heavy target library at module top level.
- Report success without a real-data transcript.
- Point `command` at `python` and hope `PATH` resolves it.
- Rebuild a server that already exists and is maintained upstream.

## Reference files

- `references/feasibility.md` — the five integration paths, with worked
  examples per path and a per-software lookup table
- `references/tool-design.md` — naming, docstrings, return shapes, registries,
  error messages, pagination
- `references/security.md` — path traversal, subprocess hardening, secrets,
  prompt-injection exposure, read/write separation
- `references/client-setup.md` — Antigravity / Claude Code / VS Code config
  formats and the differences between them
- `references/RESOURCES.md` — upstream skills, SDKs, scaffolding tools,
  registries and further reading

## Scripts

- `scripts/template_mcp.py` — annotated skeleton covering all four integration
  paths; run with `--selftest`
- `scripts/check_mcp_server.py` — static conventions linter; exits non-zero on
  violations so it can be wired into CI

# Subagent Patterns — Shared Module
> Imported by all skills. Defines how to decompose and parallelize work.

---

## 1. When to Use Subagents

Use a subagent when:
- A task is self-contained with clear inputs and outputs.
- A task can run independently from other ongoing tasks.
- A task is complex enough to benefit from isolated context.

Do NOT use a subagent when:
- The task is trivial (<5 min equivalent effort).
- The task requires continuous back-and-forth with the user.

---

## 2. Parallel Execution Pattern

```
Orchestrator
├── Subagent A  →  output-a.md
├── Subagent B  →  output-b.md
└── Subagent C  →  output-c.md
         ↓
Orchestrator merges → final-artifact.md
```

- Orchestrator defines task boundaries and assigns inputs before spawning.
- Each subagent is given: task description, input files, output file path, and completion criteria.
- Orchestrator waits for all subagents, then validates and merges.

---

## 3. Sequential Execution Pattern

Use when output of step N is input to step N+1.
Always save intermediate outputs to files — never pass large content inline between steps.

---

## 4. Error Handling

- If a subagent fails or produces incomplete output: log the failure, retry once, then escalate to user.
- Never silently skip a failed subagent task.
- Partial results must be clearly marked as INCOMPLETE in the output file.

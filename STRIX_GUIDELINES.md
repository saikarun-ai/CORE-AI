# STRIX Security Guidelines for Secure AI Agent Development

This document defines the strict **STRIX guidelines** enforced across the CORE-AI platform. It ensures that any AI agent, code generator, and external tool operates within safe, secure, and predictable boundaries to prevent security and privacy breaches during research-to-prototype transitions.

---

## 1. Principles of Secure AI Systems

### Principle A: Least Privilege Execution
AI agents should never execute in administrative or root contexts. All dynamic code execution must take place in custom, locked-down sandboxes.

### Principle B: Input Validation & Sanitization
LLM inputs must be checked for potential prompt injections, and generated code must be treated as untrusted user input before execution.

### Principle C: Constant Human Auditing (Human-In-The-Loop)
No automated agent should commit code, update databases, or execute commands without human verification at critical milestones.

---

## 2. Guidelines for Sandboxed Execution

When executing generated code in CORE-AI, the following sandboxing parameters must be enforced:
1. **Isolated Namespace**: Strip out global access to the standard libraries (e.g., `os`, `sys`, `subprocess`) unless strictly necessary and safe.
2. **Resource Constraints**:
   - Limit execution timeout (default: 10 seconds).
   - Prevent unbounded memory usage or CPU cycles.
3. **Data Protection**: Ensure filesystem boundaries are strictly controlled. The agent must never read/write arbitrary paths on the host machine.

---

## 3. Vulnerability Scanning & Mitigation Checklist

Our automated Strix Security Scanner checks code against several critical vulnerabilities:

### 1. Command Injection
- **Check**: Look for calls like `os.system(...)`, `subprocess.Popen(..., shell=True)`, `eval(...)`, or `exec(...)`.
- **Remediation**: Use structured API calls or array-based argument tokens (e.g., `subprocess.run(["echo", "hello"])`) rather than starting a full subshell.

### 2. Path Traversal
- **Check**: Identify occurrences of `../`, `..\\`, or absolute paths in file operation APIs.
- **Remediation**: Pass absolute base paths and validate that parsed absolute paths begin strictly with the allowed working directory prefix.

### 3. Hardcoded Secrets
- **Check**: Scan for static API keys, passwords, database URLs, and bearer tokens.
- **Remediation**: Store configurations in environment variables and access them dynamically via standard utility libraries.

### 4. Insecure Deserialization
- **Check**: Detect the use of libraries like `pickle.loads` or `yaml.unsafe_load`.
- **Remediation**: Use standard, secure, schema-enforced serialization protocols such as JSON or Protocol Buffers.

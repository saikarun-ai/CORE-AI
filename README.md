# CORE-AI: Research-Grade Assistant with Human-In-The-Loop Evaluation & Strix Security Guidelines

Welcome to **CORE-AI**, a state-of-the-art, research-grade assistant designed to bridge the gap between human-judged research papers and secure, production-ready implementation. Inspired by frameworks like Collabuild, CORE-AI processes scientific research through an automated but highly supervised 9-stage pipeline, ensuring that human critical opinion acts as the catalyst and ultimate judge of the system's outputs.

Furthermore, CORE-AI enforces the strict **Strix Security Guidelines** directly inside its architecture—providing sandboxed code execution, input/output validation, and automated vulnerability scanning/pentesting before code is ever promoted.

---

## High-Level Architecture

CORE-AI is organized as a multi-agent cooperative pipeline operating across 9 distinct stages. To satisfy the requirement that human judgment remains paramount, the pipeline includes **Human-In-The-Loop (HITL) checkpoints** at three vital milestones:

1. **Milestone 1 (Paper Ingestion & Synthesis)**: After digesting the research paper, the human reviews the synthesized goals, concepts, and requirements.
2. **Milestone 2 (System Design & Module Architecture)**: Before writing code, the human approves the designed APIs, modules, and schemas.
3. **Milestone 3 (Code Generation & Security Audit)**: After code generation and automated Strix security auditing, the human must explicitly approve the code and security report.

```
       +-------------------------------------------------------+
       |                  Human Research Paper                 |
       +---------------------------+---------------------------+
                                   |
                                   v
       +---------------------------+---------------------------+
       |   Stage 1: Paper Ingestion & Objectives Synthesis     |
       +---------------------------+---------------------------+
                                   |
                                   v
       +---------------------------+---------------------------+
       | [HITL #1] Human Evaluation: Approve/Refine Synthesis  |
       +---------------------------+---------------------------+
                                   |
                                   v
       +---------------------------+---------------------------+
       |   Stage 2: Literature & Concept Contextualization     |
       +---------------------------+---------------------------+
                                   |
                                   v
       +---------------------------+---------------------------+
       |   Stage 3: SRS & Feature Requirements Generation      |
       +---------------------------+---------------------------+
                                   |
                                   v
       +---------------------------+---------------------------+
       |   Stage 4: High-Level System Architecture Design      |
       +---------------------------+---------------------------+
                                   |
                                   v
       +---------------------------+---------------------------+
       |   Stage 5: Detailed Component & Module Design         |
       +---------------------------+---------------------------+
                                   |
                                   v
       +---------------------------+---------------------------+
       | [HITL #2] Human Evaluation: Approve/Refine Design     |
       +---------------------------+---------------------------+
                                   |
                                   v
       +---------------------------+---------------------------+
       |   Stage 6: Code Generation & Component Assembly       |
       +---------------------------+---------------------------+
                                   |
                                   v
       +---------------------------+---------------------------+
       |   Stage 7: Isolated Sandboxed Execution & Diagnostics |
       +---------------------------+---------------------------+
                                   |
                                   v
       +---------------------------+---------------------------+
       |   Stage 8: Strix Security Scanning & Vulnerability PoC|
       +---------------------------+---------------------------+
                                   |
                                   v
       +---------------------------+---------------------------+
       |   Stage 9: Comprehensive Review & Packaging           |
       +---------------------------+---------------------------+
                                   |
                                   v
       +---------------------------+---------------------------+
       | [HITL #3] Human Evaluation: Approve Final Output/Code  |
       +---------------------------+---------------------------+
```

---

## Core Security: The Strix Framework

Rather than treating security as a post-development afterthought, CORE-AI embeds safety into the development process using **Strix Principles**:
- **Sandboxed Execution**: Generated code is run inside restricted, resource-constrained environments (using simulated process isolation, filesystem virtualization, and standard stream redirection) to prevent malicious or accidental system compromises.
- **Automated Pentesting (Strix Audit)**: Code is scanned for critical security risks (e.g., Code Injection, Command Injection, Insecure Deserialization, Path Traversal, and Hardcoded Secrets) and produces an interactive security report.
- **Input/Output Sanitization**: All prompts sent to the LLM and code outputs fetched are strictly validated and parsed to avoid prompt injection and code poisoning.

---

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd CORE-AI
   ```

2. **Run Tests**:
   Ensure everything is operating correctly:
   ```bash
   python -m unittest discover tests
   ```

3. **Run CLI**:
   Begin an interactive session to process a research paper:
   ```bash
   python -m core_ai.cli --paper path/to/research_paper.txt --interactive
   ```

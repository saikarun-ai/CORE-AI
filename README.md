# CORE-AI: Cloud-Ready Research-Grade Assistant with Human-In-The-Loop Evaluation & Strix Security Guidelines

Welcome to **CORE-AI**, a state-of-the-art, research-grade assistant designed to bridge the gap between human-judged research papers and secure, production-ready implementation. CORE-AI processes scientific research through an automated but highly supervised 9-stage pipeline, ensuring that human critical opinion acts as the catalyst and ultimate judge of the system's outputs.

Now available as a **Cloud Platform**, CORE-AI supports multi-tenant, cloud-native deployments with an integrated, lightweight REST API, web polling interface, and centralized Strix security governance.

---

## High-Level Cloud Architecture

CORE-AI is organized as a multi-agent cooperative pipeline operating across 9 distinct stages. To satisfy the requirement that human judgment remains paramount, the pipeline includes **Human-In-The-Loop (HITL) checkpoints** at three vital milestones.

In the Cloud version, these checkpoints are managed via centralized REST API endpoints (`/api/milestones`), allowing human evaluators to query active milestones and submit approval or feedback from any web dashboard.

```
                  +-----------------------------------+
                  |      Web Client / API Consumer    |
                  +---+---------------------------^---+
                      |                           |
            POST /api/pipeline             GET /api/milestones
                      |                           |
                      v                           +
       +--------------+---------------------------+-----------+
       |                  CORE-AI Cloud Service               |
       +------------------------------------------------------+
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

## Core Security: The Cloud Strix Framework

Rather than treating security as a post-development afterthought, CORE-AI embeds safety into the cloud development process using **Strix Principles**:
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

3. **Start the Cloud API Server**:
   Start the cloud-native REST service:
   ```bash
   python -m core_ai.api --port 8080
   ```

4. **Run CLI**:
   Begin an interactive session to process a research paper:
   ```bash
   python -m core_ai.cli --paper path/to/research_paper.txt --interactive
   ```

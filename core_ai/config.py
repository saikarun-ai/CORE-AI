"""
Configuration settings for the CORE-AI system.
"""

import os

# Maximum number of iterations for the agent loops
MAX_AGENT_ITERATIONS = int(os.environ.get("CORE_AI_MAX_ITERATIONS", "300"))

# Security settings
SANDBOX_TIMEOUT_SECONDS = float(os.environ.get("CORE_AI_TIMEOUT", "10.0"))
MAX_MEMORY_MB = int(os.environ.get("CORE_AI_MAX_MEMORY", "256"))

# Pre-defined security vulnerability patterns for the Strix Scanner (Regex/Substring)
VULNERABILITY_PATTERNS = {
    "command_injection": [
        "subprocess.Popen(..., shell=True)",
        "os.system(",
        "eval(",
        "exec(",
    ],
    "path_traversal": [
        "../",
        "..\\",
        "open(filepath",
    ],
    "hardcoded_secrets": [
        "api_key =",
        "secret =",
        "password =",
        "token =",
    ],
    "insecure_deserialization": [
        "pickle.loads",
        "yaml.unsafe_load",
    ],
}

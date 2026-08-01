"""
Implements Strix-inspired security guidelines, static auditing, and vulnerability scanning for AI-generated code.
"""

from typing import Dict, Any, List
from core_ai.config import VULNERABILITY_PATTERNS

class StrixSecurityScanner:
    """
    Simulates a Strix Security agent. It performs static code analysis
    and identifies security flaws inside generated code.
    """
    def __init__(self, patterns: Dict[str, List[str]] = VULNERABILITY_PATTERNS):
        self.patterns = patterns

    def scan(self, code: str) -> Dict[str, Any]:
        """
        Scans code for common AI agent vulnerabilities.
        Returns a detailed security report dictionary.
        """
        findings = []
        is_secure = True

        for category, triggers in self.patterns.items():
            for trigger in triggers:
                if trigger in code:
                    is_secure = False
                    findings.append({
                        "category": category,
                        "vulnerability": f"Detected unsafe usage of: {trigger}",
                        "severity": self._get_severity(category),
                        "remediation": self._get_remediation(category)
                    })

        return {
            "is_secure": is_secure,
            "vulnerability_count": len(findings),
            "findings": findings
        }

    def _get_severity(self, category: str) -> str:
        if category in ["command_injection", "insecure_deserialization"]:
            return "CRITICAL"
        elif category in ["path_traversal"]:
            return "HIGH"
        elif category in ["hardcoded_secrets"]:
            return "MEDIUM"
        return "LOW"

    def _get_remediation(self, category: str) -> str:
        remediations = {
            "command_injection": "Avoid executing shell commands using 'shell=True' or 'os.system'. Use structured APIs or subprocesses with tokenized argument arrays.",
            "path_traversal": "Sanitize all file paths. Strictly use os.path.basename or resolve files within a safe, absolute root directory.",
            "hardcoded_secrets": "Use environment variables or a configuration manager. Never hardcode sensitive tokens or passwords directly in code repositories.",
            "insecure_deserialization": "Never use pickle or unsafe yaml loading libraries on untrusted input data. Prefer JSON-based deserializers."
        }
        return remediations.get(category, "Review security policies and refactor code.")

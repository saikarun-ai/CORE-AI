import unittest
from core_ai.sandbox import SandboxEnvironment
from core_ai.security import StrixSecurityScanner

class TestSandboxAndSecurity(unittest.TestCase):
    def test_sandbox_secure_execution(self):
        sandbox = SandboxEnvironment()

        # Test basic addition and return
        code = "result = 1 + 2\nprint('Result is:', result)"
        execution_result = sandbox.execute(code)

        self.assertTrue(execution_result["success"])
        self.assertIn("Result is: 3", execution_result["stdout"])
        self.assertEqual(execution_result["stderr"], "")

    def test_sandbox_malicious_code_restriction(self):
        sandbox = SandboxEnvironment()

        # Code trying to import disallowed libraries
        code = "import os\nos.system('echo dangerous')"
        execution_result = sandbox.execute(code)

        self.assertFalse(execution_result["success"])
        self.assertIn("ImportError", execution_result["stderr"]) # '__import__ not found' when importing in restricted builtins

    def test_strix_security_scanner_clean_code(self):
        scanner = StrixSecurityScanner()
        clean_code = "def safe_function():\n    return 'Hello World'"

        report = scanner.scan(clean_code)
        self.assertTrue(report["is_secure"])
        self.assertEqual(report["vulnerability_count"], 0)
        self.assertEqual(len(report["findings"]), 0)

    def test_strix_security_scanner_vulnerabilities(self):
        scanner = StrixSecurityScanner()

        # Unsafe code with command injection and hardcoded secret
        unsafe_code = (
            "def test():\n"
            "    api_key = 'super-secret-key-123'\n"
            "    os.system('rm -rf /')\n"
        )

        report = scanner.scan(unsafe_code)
        self.assertFalse(report["is_secure"])
        self.assertEqual(report["vulnerability_count"], 2)

        categories = [finding["category"] for finding in report["findings"]]
        self.assertIn("command_injection", categories)
        self.assertIn("hardcoded_secrets", categories)


if __name__ == "__main__":
    unittest.main()

import unittest
import sys
from unittest.mock import patch
import io
from core_ai.cli import cli_interactive_hitl_callback

class TestCOREAICLI(unittest.TestCase):
    @patch('builtins.input', side_effect=['y'])
    def test_cli_interactive_hitl_callback_approval(self, mock_input):
        # Redirect stdout to avoid messing with test logs
        with patch('sys.stdout', new=io.StringIO()):
            approved = cli_interactive_hitl_callback("Synthesis Milestone", 1, {"synthesis": "Test objective"})
            self.assertTrue(approved)

    @patch('builtins.input', side_effect=['n'])
    def test_cli_interactive_hitl_callback_rejection(self, mock_input):
        with patch('sys.stdout', new=io.StringIO()):
            approved = cli_interactive_hitl_callback("Synthesis Milestone", 1, {"synthesis": "Test objective"})
            self.assertFalse(approved)

    @patch('builtins.input', side_effect=['Use better model parameters', 'y'])
    def test_cli_interactive_hitl_callback_feedback_and_approval(self, mock_input):
        with patch('sys.stdout', new=io.StringIO()):
            approved = cli_interactive_hitl_callback("Design Milestone", 5, {"module_design": {"modules": [], "apis": {}}})
            self.assertTrue(approved)


if __name__ == "__main__":
    unittest.main()

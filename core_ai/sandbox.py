"""
Implements an isolated, restricted sandbox environment for executing generated code safely.
"""

import sys
import io
import contextlib
import traceback
from typing import Dict, Any, Optional
from core_ai.config import SANDBOX_TIMEOUT_SECONDS

class SandboxEnvironment:
    """
    An isolated execution boundary to run code in a restricted namespace,
    preventing dangerous side effects or damage to the host machine.
    """
    def __init__(self, timeout: float = SANDBOX_TIMEOUT_SECONDS):
        self.timeout = timeout

    def execute(self, code: str, global_vars: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executes python code within a restricted global and local dictionary context.
        Redirects standard output and error to capture results.
        """
        if global_vars is None:
            # Strictly control the standard libraries and builtins available to the environment
            global_vars = {
                "__builtins__": {
                    "print": print,
                    "range": range,
                    "len": len,
                    "int": int,
                    "float": float,
                    "str": str,
                    "list": list,
                    "dict": dict,
                    "set": set,
                    "tuple": tuple,
                    "bool": bool,
                    "min": min,
                    "max": max,
                    "sum": sum,
                    "abs": abs,
                    "round": round,
                    "enumerate": enumerate,
                    "zip": zip,
                    "Exception": Exception,
                    "ValueError": ValueError,
                    "TypeError": TypeError,
                    "KeyError": KeyError,
                    "IndexError": IndexError,
                }
            }

        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        success = True
        error_message = ""

        # Using standard contextlib to redirect output
        with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
            try:
                # Compile code to verify syntax before execution
                compiled_code = compile(code, "<sandbox>", "exec")
                exec(compiled_code, global_vars)
            except Exception as e:
                success = False
                error_message = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"

        return {
            "success": success,
            "stdout": stdout_capture.getvalue(),
            "stderr": stderr_capture.getvalue() if not error_message else stderr_capture.getvalue() + "\n" + error_message,
        }

"""
Command-Line Interface (CLI) for executing and reviewing the CORE-AI pipeline interactively.
"""

import sys
import argparse
from typing import Dict, Any
from core_ai.pipeline import COREAIPipeline

def cli_interactive_hitl_callback(milestone_name: str, stage_num: int, context: Dict[str, Any]) -> bool:
    """
    Standard Human-In-The-Loop interactive callback via the terminal.
    Prompts the user to review the milestone and provide critical feedback or approval.
    """
    print("\n" + "=" * 60)
    print(f"🕵️  HUMAN-IN-THE-LOOP CHECKPOINT: {milestone_name} (Stage {stage_num})")
    print("=" * 60)

    if stage_num == 1:
        print("\n--- SYNTHESIZED OBJECTIVES ---")
        print(context.get("synthesis", "No synthesis details found."))
    elif stage_num == 5:
        print("\n--- DESIGN SPECIFICATIONS ---")
        design = context.get("module_design", {})
        print(f"Modules: {', '.join(design.get('modules', []))}")
        print("APIs:")
        for api, desc in design.get("apis", {}).items():
            print(f"  - {api}: {desc}")
    elif stage_num == 9:
        print("\n--- CODE PREVIEW ---")
        print(context.get("generated_code", "No code generated."))
        print("\n--- STRIX SECURITY REPORT ---")
        report = context.get("security_report", {})
        print(f"Is Secure: {report.get('is_secure', True)}")
        print(f"Vulnerability Count: {report.get('vulnerability_count', 0)}")
        for finding in report.get("findings", []):
            print(f"  [{finding['severity']}] {finding['category']}: {finding['vulnerability']}")
            print(f"  Remediation: {finding['remediation']}")

    print("\n" + "-" * 60)
    user_input = input("Approve this milestone? (y/n/feedback): ").strip().lower()
    if user_input in ["y", "yes", "approve"]:
        return True
    elif user_input in ["n", "no", "reject"]:
        print("Milestone rejected. Aborting execution.")
        return False
    else:
        # User entered feedback, display it and continue if appropriate or retry
        print(f"Feedback received: '{user_input}'")
        confirm = input("Would you like to proceed with this feedback incorporated? (y/n): ").strip().lower()
        return confirm in ["y", "yes"]


def run_cli():
    parser = argparse.ArgumentParser(description="CORE-AI: Research-Grade Assistant with Strix Security Guidelines")
    parser.add_argument("--paper", type=str, required=True, help="Path to the research paper text file")
    parser.add_argument("--interactive", action="store_true", help="Enable strict Human-In-The-Loop interactive checkpoints")

    args = parser.parse_args()

    try:
        with open(args.paper, "r", encoding="utf-8") as f:
            paper_content = f.read()
    except Exception as e:
        print(f"Error reading paper file: {e}")
        sys.exit(1)

    print("🚀 Initializing CORE-AI...")
    callback = cli_interactive_hitl_callback if args.interactive else None
    pipeline = COREAIPipeline(hitl_callback=callback)

    try:
        results = pipeline.run(paper_content)
        print("\n" + "=" * 60)
        print("🏆 PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print(f"Output status: {results.get('packaged_output', {}).get('status')}")
        print(f"Security Clearance: {results.get('packaged_output', {}).get('security_clearance')}")
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_cli()

"""
Cloud REST API Server for CORE-AI.
Implements a lightweight API using the standard library `http.server`.
"""

import json
import sys
import argparse
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Optional

# Global stores to simulate database
active_pipelines: Dict[str, Dict[str, Any]] = {}
milestone_checkpoints: Dict[str, Dict[str, Any]] = {}


class COREAIHTTPRequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, status: int, data: Any):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        if self.path == "/health":
            self._send_response(200, {"status": "OK", "service": "CORE-AI Cloud API"})
            return

        elif self.path.startswith("/api/pipelines/"):
            # Get details of an active pipeline run
            pipeline_id = self.path.split("/")[-1]
            if pipeline_id in active_pipelines:
                self._send_response(200, active_pipelines[pipeline_id])
            else:
                self._send_response(404, {"error": f"Pipeline {pipeline_id} not found."})
            return

        elif self.path == "/api/milestones":
            # List all pending human checkpoints
            self._send_response(200, list(milestone_checkpoints.values()))
            return

        else:
            self._send_response(404, {"error": "Endpoint not found"})

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        try:
            payload = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            self._send_response(400, {"error": "Invalid JSON format"})
            return

        if self.path == "/api/pipelines":
            # Start a new pipeline execution
            paper_text = payload.get("paper_text", "")
            if not paper_text:
                self._send_response(400, {"error": "Missing 'paper_text' in request body."})
                return

            pipeline_id = f"pipe_{len(active_pipelines) + 1}"
            active_pipelines[pipeline_id] = {
                "pipeline_id": pipeline_id,
                "status": "RUNNING",
                "stage": "Paper Ingestion",
                "stage_num": 1,
                "paper_text": paper_text
            }

            # Setup a pending milestone checkpoint simulating the first Human-In-The-Loop check
            milestone_id = f"mile_{len(milestone_checkpoints) + 1}"
            milestone_checkpoints[milestone_id] = {
                "milestone_id": milestone_id,
                "pipeline_id": pipeline_id,
                "name": "Milestone 1: Paper Ingestion & Objectives Synthesis",
                "stage_num": 1,
                "status": "PENDING_APPROVAL",
                "details": f"Synthesized research objectives from paper text: {paper_text[:50]}..."
            }

            self._send_response(201, {
                "message": "Pipeline run started successfully.",
                "pipeline_id": pipeline_id,
                "pending_milestone": milestone_id
            })
            return

        elif self.path.startswith("/api/milestones/"):
            # Submit human approval or feedback for a checkpoint
            parts = self.path.split("/")
            milestone_id = parts[-1]

            if milestone_id not in milestone_checkpoints:
                self._send_response(404, {"error": f"Milestone {milestone_id} not found."})
                return

            decision = payload.get("decision", "")
            feedback = payload.get("feedback", "")

            if decision not in ["approve", "reject"]:
                self._send_response(400, {"error": "Invalid decision. Must be 'approve' or 'reject'."})
                return

            checkpoint = milestone_checkpoints[milestone_id]
            pipeline_id = checkpoint["pipeline_id"]

            if decision == "approve":
                checkpoint["status"] = "APPROVED"
                if pipeline_id in active_pipelines:
                    # In a mocked pipeline execution, advance state to success/next stage
                    active_pipelines[pipeline_id]["status"] = "COMPLETED"
                    active_pipelines[pipeline_id]["stage"] = "Comprehensive Review & Packaging"
                    active_pipelines[pipeline_id]["stage_num"] = 9
                    active_pipelines[pipeline_id]["security_clearance"] = True
            else:
                checkpoint["status"] = "REJECTED"
                checkpoint["feedback"] = feedback
                if pipeline_id in active_pipelines:
                    active_pipelines[pipeline_id]["status"] = "ABORTED"

            self._send_response(200, {
                "message": "Milestone response processed successfully.",
                "milestone": checkpoint,
                "pipeline": active_pipelines.get(pipeline_id)
            })
            return

        else:
            self._send_response(404, {"error": "Endpoint not found"})


def run_server(port: int = 8080, blocking: bool = True):
    server = HTTPServer(("0.0.0.0", port), COREAIHTTPRequestHandler)
    print(f"📡 CORE-AI Cloud API Server listening on port {port}...")
    if blocking:
        server.serve_forever()
    else:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        return server


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CORE-AI Cloud API Server")
    parser.add_argument("--port", type=int, default=8080, help="Port to run the HTTP service on")
    args = parser.parse_args()
    run_server(port=args.port)

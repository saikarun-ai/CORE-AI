import unittest
import urllib.request
import urllib.error
import json
import time
from core_ai.api import run_server, active_pipelines, milestone_checkpoints

class TestCOREAICloudAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the lightweight HTTP server on a non-standard test port
        cls.port = 18080
        cls.server = run_server(port=cls.port, blocking=False)
        cls.base_url = f"http://127.0.0.1:{cls.port}"
        # Wait a tiny moment for server socket to bind
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        # Shutdown HTTP server safely
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        # Clear database states between test runs
        active_pipelines.clear()
        milestone_checkpoints.clear()

    def test_health_endpoint(self):
        req = urllib.request.Request(f"{self.base_url}/health", method="GET")
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))
            self.assertEqual(data["status"], "OK")
            self.assertEqual(data["service"], "CORE-AI Cloud API")

    def test_pipeline_creation_and_checkpoints(self):
        # 1. Create a pipeline
        create_payload = json.dumps({"paper_text": "Evaluating Secure Microkernels under Strix Rules."}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/pipelines",
            data=create_payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 201)
            resp_data = json.loads(response.read().decode("utf-8"))
            self.assertIn("pipeline_id", resp_data)
            self.assertIn("pending_milestone", resp_data)
            pipeline_id = resp_data["pipeline_id"]
            milestone_id = resp_data["pending_milestone"]

        # 2. Query pipeline status
        req = urllib.request.Request(f"{self.base_url}/api/pipelines/{pipeline_id}", method="GET")
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            pipe_details = json.loads(response.read().decode("utf-8"))
            self.assertEqual(pipe_details["status"], "RUNNING")

        # 3. Query milestone list
        req = urllib.request.Request(f"{self.base_url}/api/milestones", method="GET")
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            milestones = json.loads(response.read().decode("utf-8"))
            self.assertEqual(len(milestones), 1)
            self.assertEqual(milestones[0]["milestone_id"], milestone_id)

        # 4. Approve the milestone
        approve_payload = json.dumps({"decision": "approve"}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/milestones/{milestone_id}",
            data=approve_payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            decision_resp = json.loads(response.read().decode("utf-8"))
            self.assertEqual(decision_resp["milestone"]["status"], "APPROVED")
            self.assertEqual(decision_resp["pipeline"]["status"], "COMPLETED")

    def test_pipeline_rejection(self):
        # 1. Create a pipeline
        create_payload = json.dumps({"paper_text": "An unsafe framework design."}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/pipelines",
            data=create_payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req) as response:
            resp_data = json.loads(response.read().decode("utf-8"))
            milestone_id = resp_data["pending_milestone"]

        # 2. Reject the milestone with feedback
        reject_payload = json.dumps({
            "decision": "reject",
            "feedback": "Lacks proper isolation design."
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/milestones/{milestone_id}",
            data=reject_payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            decision_resp = json.loads(response.read().decode("utf-8"))
            self.assertEqual(decision_resp["milestone"]["status"], "REJECTED")
            self.assertEqual(decision_resp["milestone"]["feedback"], "Lacks proper isolation design.")
            self.assertEqual(decision_resp["pipeline"]["status"], "ABORTED")


if __name__ == "__main__":
    unittest.main()

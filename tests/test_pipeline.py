import unittest
from core_ai.pipeline import COREAIPipeline

class TestCOREAIPipeline(unittest.TestCase):
    def test_pipeline_successful_run(self):
        # A simple test that executes all 9 stages with auto-approval
        pipeline = COREAIPipeline(hitl_callback=lambda name, num, ctx: True)
        results = pipeline.run("Test research paper about AI security and automation.")

        self.assertIn("synthesis", results)
        self.assertIn("contextualized_concepts", results)
        self.assertIn("srs", results)
        self.assertIn("architecture", results)
        self.assertIn("module_design", results)
        self.assertIn("generated_code", results)
        self.assertIn("sandbox_execution_result", results)
        self.assertIn("security_report", results)
        self.assertIn("packaged_output", results)

        # Verify package output details
        packaged_output = results["packaged_output"]
        self.assertEqual(packaged_output["app_name"], "CORE-AI Research Prototype")
        self.assertEqual(packaged_output["status"], "Ready for deployment")

    def test_pipeline_rejection_milestone1(self):
        # Human rejects at milestone 1
        def reject_milestone_1(name, stage_num, context):
            if stage_num == 1:
                return False
            return True

        pipeline = COREAIPipeline(hitl_callback=reject_milestone_1)
        with self.assertRaises(ValueError) as context:
            pipeline.run("Test paper content")
        self.assertIn("Milestone 1", str(context.exception))

    def test_pipeline_rejection_milestone2(self):
        # Human rejects at milestone 2 (detailed design)
        def reject_milestone_2(name, stage_num, context):
            if stage_num == 5:
                return False
            return True

        pipeline = COREAIPipeline(hitl_callback=reject_milestone_2)
        with self.assertRaises(ValueError) as context:
            pipeline.run("Test paper content")
        self.assertIn("Milestone 2", str(context.exception))

    def test_pipeline_rejection_milestone3(self):
        # Human rejects at milestone 3 (final packaging)
        def reject_milestone_3(name, stage_num, context):
            if stage_num == 9:
                return False
            return True

        pipeline = COREAIPipeline(hitl_callback=reject_milestone_3)
        with self.assertRaises(ValueError) as context:
            pipeline.run("Test paper content")
        self.assertIn("Milestone 3", str(context.exception))


if __name__ == "__main__":
    unittest.main()

"""Research records retain source bytes, links, and execution failures."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import research as sa


class ResearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="researchweave-records-")
        self.root = Path(self.temp.name)
        self.study = self.root / "study"
        sa.initialize(argparse.Namespace(study=str(self.study), question="Synthetic calibration", label="synthetic"))

    def test_previous_name_study_remains_readable(self):
        meta = sa.read_json(self.study / "study.json")
        self.assertEqual(meta["format"], "researchweave.study.v1")
        meta["format"] = "zhangluo.study.v1"
        sa.atomic_json(self.study / "study.json", meta)
        self.assertEqual(sa.study_path(self.study), self.study.resolve())
        self.assertEqual(sa.status(argparse.Namespace(study=str(self.study)))["counts"], {})

    def tearDown(self):
        self.temp.cleanup()

    def test_snapshot_and_parent_links_survive_source_changes(self):
        source = self.root / "measurements.csv"
        original = b"x,y\n1,3\n2,5\n"
        source.write_bytes(original)
        evidence = sa.save_record(self.study, {"kind": "evidence", "content": {
            "claim": "Synthetic values", "source": str(source), "evidence_type": "synthetic"}}, [source])
        source.write_text("changed", encoding="utf-8")
        saved = evidence["artifacts"][0]
        self.assertEqual((self.study / saved["path"]).read_bytes(), original)
        self.assertEqual(saved["sha256"], hashlib.sha256(original).hexdigest())
        hypothesis = sa.save_record(self.study, {"kind": "hypothesis", "content": {
            "statement": "There may be a linear relationship", "predictions": ["Predict new values"],
            "evidence_ids": [evidence["id"]]}, "parent_ids": [evidence["id"]]})
        recovered = sa.status(argparse.Namespace(study=str(self.study)))
        self.assertEqual(recovered["counts"], {"evidence": 1, "hypothesis": 1})
        self.assertIn(hypothesis["id"], [r["id"] for r in recovered["records"]])
        report = sa.report(argparse.Namespace(study=str(self.study)))
        self.assertTrue(Path(report["report"]).is_file())

    def test_invalid_links_and_reinitialization_do_not_change_records(self):
        with self.assertRaisesRegex(ValueError, "missing or wrong-kind"):
            sa.save_record(self.study, {"kind": "result", "content": {"summary": "invalid", "analysis_id": "absent"}})
        self.assertEqual(sa.records(self.study), [])
        with self.assertRaisesRegex(ValueError, "new or empty"):
            sa.initialize(argparse.Namespace(study=str(self.study), question="Different", label="real"))
        self.assertEqual(sa.read_json(self.study / "study.json")["question"], "Synthetic calibration")

    def test_execution_failure_is_saved_with_input_and_analysis(self):
        analysis = sa.save_record(self.study, {"kind": "analysis", "content": {
            "question": "Can this program run?", "inputs": ["input.json"], "method": "Run once",
            "comparison": "Expected return value", "success_criteria": "Valid JSON", "independent_unit": "Synthetic row",
            "hypothesis_ids": []}})
        code = self.root / "candidate.py"
        code.write_text("def run(data):\n    raise ValueError('failed')\n", encoding="utf-8")
        data = self.root / "input.json"
        data.write_text("[1,2]", encoding="utf-8")
        with patch("era_sandbox.DockerSandbox") as runner:
            runner.return_value.run.return_value = (None, False)
            runner.return_value.last_error = "candidate_failed"
            runner.return_value.image = "test-image"
            response = sa.run(argparse.Namespace(study=str(self.study), code=str(code), input=str(data),
                                                 function="run", analysis_id=analysis["id"], timeout=30))
        self.assertFalse(response["success"])
        self.assertEqual(response["record"]["content"]["run_status"], "failed")
        entries = sa.records(self.study)
        code_entry = next(r for r in entries if r["kind"] == "code")
        self.assertEqual(len(code_entry["artifacts"]), 2)
        self.assertEqual(response["record"]["content"]["code_id"], code_entry["id"])


if __name__ == "__main__":
    unittest.main()

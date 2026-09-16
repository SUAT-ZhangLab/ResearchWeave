"""Meaningful checks for stepwise ERA persistence, scoring, and Docker execution.

Run ordinary checks with unittest. Set ZHANGLUO_DOCKER_TESTS=1 to include
an actual WSL Docker run using the installed zhangluo-era image.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import era


def result(score=0.0, output=None, error=None):
    return {"score": score, "metric_value": -score if score is not None else None,
            "error": error, "output": output}


class SessionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="zhangluo-era-tests-")
        self.root = Path(self.temporary.name)
        self.session = self.root / "session"
        self.spec_path = self.root / "input.json"
        self.baseline = self.root / "baseline.py"
        self.baseline.write_text("def predict(xs):\n    return [0 for x in xs]\n", encoding="utf-8")
        self.spec = {"problem": "Fit y from the provided training examples.",
                     "development": {"input": [1, 2], "target": [3, 5]},
                     "final": {"input": [4], "target": [9]}, "iterations": 3}
        self.write_spec()

    def tearDown(self):
        self.temporary.cleanup()

    def write_spec(self):
        self.spec_path.write_text(json.dumps(self.spec), encoding="utf-8")

    def init(self, score=-4.0):
        with patch.object(era, "_evaluate", return_value=result(score)):
            return era.initialize(self.session, self.spec_path, self.baseline)

    def submit(self, program, score):
        path = self.root / "candidate.py"
        path.write_text(program, encoding="utf-8")
        request = era.ask(self.session)
        with patch.object(era, "_evaluate", return_value=result(score, error="candidate_failed" if score is None else None)):
            return era.tell(self.session, path, request["request_id"])

    def test_ask_is_persistent_and_rejects_stale_tell(self):
        self.init()
        first = era.ask(self.session)
        self.assertEqual(first, era.ask(self.session))
        self.assertNotIn("development", first)
        self.assertNotIn("final", first)
        with patch.object(era, "_evaluate") as evaluate:
            with self.assertRaisesRegex(era.SessionError, "Stale"):
                era.tell(self.session, self.baseline, "old-request")
            evaluate.assert_not_called()
        self.assertEqual(era.ask(self.session)["request_id"], first["request_id"])
        with patch.object(era, "_evaluate", return_value=result(-3)):
            response = era.tell(self.session, self.baseline, first["request_id"])
        self.assertEqual(response["candidate"]["parent_index"], 0)
        with self.assertRaisesRegex(era.SessionError, "Stale"):
            era.tell(self.session, self.baseline, first["request_id"])

    def test_split_search_matches_upstream_parent_selection(self):
        self.spec["iterations"] = 5
        self.write_spec()
        self.init(score=0)
        programs = ["candidate-one", "candidate-two", "candidate-three", "candidate-four", "candidate-five"]
        scores = [-1.0, 3.0, 2.0, 4.0, -2.0]
        base_program = self.baseline.read_text(encoding="utf-8")
        upstream_parents = []
        next_index = 0
        def generate(problem, parent, score):
            nonlocal next_index
            upstream_parents.append(parent.program)
            generated = era.futs.Solution(programs[next_index])
            next_index += 1
            return generated
        upstream_best, upstream_score = era.futs.search(
            era.futs.Problem("test"), era.futs.Solution(base_program), 0.0,
            generate, lambda problem, candidate: scores[programs.index(candidate.program)], 5)
        actual_parents = []
        for program, score in zip(programs, scores):
            actual_parents.append(era.ask(self.session)["parent_code"])
            self.submit(program, score)
        self.assertEqual(actual_parents, upstream_parents)
        summary = era.status(self.session)
        self.assertEqual(summary["best"]["score"], upstream_score)
        self.assertEqual((self.session / summary["best"]["code"]).read_text(), upstream_best.program)
        with self.assertRaisesRegex(era.SessionError, "budget"):
            era.ask(self.session)

    def test_failure_is_recorded_as_null_and_restored_as_negative_infinity(self):
        self.init()
        response = self.submit("bad candidate", None)
        record = response["candidate"]
        self.assertIsNone(record["score"])
        state = json.loads((self.session / "state.json").read_text(encoding="utf-8"))
        self.assertEqual(era._nodes(self.session, state)[1].score, float("-inf"))
        self.assertNotIn("Infinity", (self.session / "state.json").read_text())
        self.assertEqual(record["sha256"], hashlib.sha256(b"bad candidate").hexdigest())
        self.assertEqual(state["candidates"][0]["num_visits"], 1)
        self.assertEqual(state["candidates"][1]["num_visits"], 1)
        self.assertEqual(era.ask(self.session)["parent_index"], 0)

    def test_failed_baseline_cannot_start_search(self):
        with patch.object(era, "_evaluate", return_value=result(None, error="candidate_failed")):
            with self.assertRaisesRegex(era.SessionError, "Baseline failed"):
                era.initialize(self.session, self.spec_path, self.baseline)
        self.assertEqual(era.status(self.session)["phase"], "initial_failed")
        with self.assertRaises(era.SessionError):
            era.ask(self.session)

    def test_final_runs_once_and_finalized_session_cannot_continue(self):
        self.init()
        self.submit("winner", 0.0)
        with patch.object(era, "_evaluate", return_value=result(-2, [7])) as evaluate:
            first = era.finalize(self.session)
            second = era.finalize(self.session)
            self.assertEqual(first, second)
            evaluate.assert_called_once()
            self.assertEqual(evaluate.call_args.args[0], "winner")
            self.assertEqual(evaluate.call_args.args[2], self.spec["final"])
        self.assertEqual(first["final_evaluation"]["metric_value"], 2)
        self.assertEqual(json.loads((self.session / "final_output.json").read_text()), [7])
        with self.assertRaises(era.SessionError):
            era.ask(self.session)
        with self.assertRaises(era.SessionError):
            era.tell(self.session, self.baseline, "anything")

    def test_final_interruption_does_not_repeat_evaluation(self):
        self.init()
        with patch.object(era, "_evaluate", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                era.finalize(self.session)
        self.assertEqual(era.status(self.session)["phase"], "finalizing")
        with patch.object(era, "_evaluate") as evaluate:
            with self.assertRaisesRegex(era.SessionError, "not be repeated"):
                era.finalize(self.session)
            evaluate.assert_not_called()

    def test_no_final_dataset_is_reported_without_execution(self):
        del self.spec["final"]
        self.write_spec()
        self.init()
        with patch.object(era, "_evaluate") as evaluate:
            summary = era.finalize(self.session)
            evaluate.assert_not_called()
        self.assertFalse(summary["final_evaluation"]["evaluated"])
        self.assertIsNone(summary["final_evaluation"]["score"])

    def test_lock_prevents_mutation_and_pending_request_prevents_finalize(self):
        self.init()
        with era._locked(self.session):
            with self.assertRaisesRegex(era.SessionError, "busy"):
                era.ask(self.session)
        self.assertFalse((self.session / ".write.lock").exists())
        era.ask(self.session)
        with self.assertRaisesRegex(era.SessionError, "pending"):
            era.finalize(self.session)

    def test_metrics_check_actual_output_shape_and_values(self):
        score, value = era._score([1, 3], [1, 5], "rmse")
        self.assertAlmostEqual(score, -2 ** 0.5)
        self.assertAlmostEqual(value, 2 ** 0.5)
        self.assertEqual(era._score(["a", "b", "a"], ["a", "b", "b"], "accuracy"), (2 / 3, 2 / 3))
        for output in ([True, 1], [float("nan"), 1], [1], {"x": 1}):
            with self.assertRaises(era.SessionError):
                era._score(output, [1, 2], "rmse")
        with self.assertRaises(era.SessionError):
            era._score([[1]], [1], "accuracy")

    def test_only_input_is_sent_to_container(self):
        spec = era._validate_spec(self.spec)
        with patch.object(era, "DockerSandbox") as sandbox_type:
            sandbox = sandbox_type.return_value
            sandbox.run.return_value = ([3, 5], True)
            evaluation = era._evaluate("code", spec, spec["development"])
            sandbox.run.assert_called_once_with("code", "predict", [1, 2], 60)
        self.assertEqual(evaluation["score"], 0)

    def test_changed_scored_candidate_is_rejected_by_search_and_finalization(self):
        self.init()
        saved_state = json.loads((self.session / "state.json").read_text(encoding="utf-8"))
        (self.session / "candidate_000.py").write_text("def predict(xs): return [999 for x in xs]\n", encoding="utf-8")
        with patch.object(era, "_evaluate") as evaluate:
            for command in (era.ask, era.status, era.finalize):
                with self.subTest(command=command.__name__):
                    with self.assertRaisesRegex(era.SessionError, "candidate_000.py.*changed"):
                        command(self.session)
            with self.assertRaisesRegex(era.SessionError, "candidate_000.py.*changed"):
                era._nodes(self.session, saved_state)
            evaluate.assert_not_called()

    def test_changed_spec_is_rejected_before_scoring(self):
        self.init()
        request = era.ask(self.session)
        saved_spec = json.loads((self.session / "spec.json").read_text(encoding="utf-8"))
        saved_spec["development"]["target"] = [999, 999]
        (self.session / "spec.json").write_text(json.dumps(saved_spec), encoding="utf-8")
        with patch.object(era, "_evaluate") as evaluate:
            for command in (era.ask, era.status, era.finalize):
                with self.subTest(command=command.__name__):
                    with self.assertRaisesRegex(era.SessionError, "spec.json changed"):
                        command(self.session)
            with self.assertRaisesRegex(era.SessionError, "spec.json changed"):
                era.tell(self.session, self.baseline, request["request_id"])
            evaluate.assert_not_called()

    def test_spec_hash_uses_json_content_not_whitespace_or_key_order(self):
        self.init()
        path = self.session / "spec.json"
        spec = json.loads(path.read_text(encoding="utf-8"))
        reordered = dict(reversed(list(spec.items())))
        path.write_text(json.dumps(reordered, indent=7), encoding="utf-8")
        self.assertEqual(era.status(self.session)["phase"], "active")
        self.assertEqual(era.ask(self.session)["parent_index"], 0)

    def test_legacy_session_without_spec_hash_requires_new_session(self):
        self.init()
        path = self.session / "state.json"
        state = json.loads(path.read_text(encoding="utf-8"))
        del state["spec_hash"]
        path.write_text(json.dumps(state), encoding="utf-8")
        with self.assertRaisesRegex(era.SessionError, "no spec_hash.*Start a new session"):
            era.status(self.session)

    def test_existing_session_and_invalid_spec_are_rejected(self):
        self.init()
        with self.assertRaisesRegex(era.SessionError, "already"):
            era.initialize(self.session, self.spec_path, self.baseline)
        for key, value in (("iterations", True), ("iterations", 21), ("timeout_seconds", 0), ("metric", "pvalue")):
            with self.subTest(key=key, value=value):
                with self.assertRaises(era.SessionError):
                    era._validate_spec({**self.spec, key: value})


@unittest.skipUnless(os.environ.get("ZHANGLUO_DOCKER_TESTS") == "1", "set ZHANGLUO_DOCKER_TESTS=1 for actual Docker execution")
class DockerIntegrationTest(unittest.TestCase):
    def test_complete_stepwise_run_in_actual_docker(self):
        with tempfile.TemporaryDirectory(prefix="zhangluo-era-docker-") as directory:
            root = Path(directory)
            spec = root / "spec.json"
            baseline = root / "baseline.py"
            candidate = root / "candidate.py"
            session = root / "run"
            spec.write_text(json.dumps({"problem": "Synthetic example y=2*x+1; this is a software check.",
                "development": {"input": [-2, 0, 3], "target": [-3, 1, 7]},
                "final": {"input": [-7, 4], "target": [-13, 9]},
                "iterations": 1, "timeout_seconds": 30}), encoding="utf-8")
            baseline.write_text("def predict(xs):\n    return [0.0 for x in xs]\n", encoding="utf-8")
            candidate.write_text("def predict(xs):\n    return [2*x+1 for x in xs]\n", encoding="utf-8")
            initial = era.initialize(session, spec, baseline)
            self.assertLess(initial["best"]["score"], 0)
            request = era.ask(session)
            told = era.tell(session, candidate, request["request_id"])
            self.assertEqual(told["candidate"]["score"], 0)
            complete = era.finalize(session)
            self.assertEqual(complete["phase"], "finalized")
            self.assertEqual(complete["final_evaluation"]["metric_value"], 0)
            self.assertEqual(complete, era.finalize(session))


if __name__ == "__main__":
    unittest.main(verbosity=2)

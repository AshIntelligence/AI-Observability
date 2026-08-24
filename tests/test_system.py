import unittest

from main import GatePolicy, WEIGHTS, evaluate, evaluate_window


class MautamTests(unittest.TestCase):
    def test_healthy_snapshot_ships(self):
        result = evaluate({k: .9 for k in WEIGHTS})
        self.assertEqual(result.decision, "SHIP")
        self.assertEqual(result.gate_failures, ())

    def test_trust_gate_stops_release(self):
        sample = {k: .9 for k in WEIGHTS}
        sample["trust_controls"] = .4
        result = evaluate(sample)
        self.assertEqual(result.decision, "STOP")
        self.assertIn("trust-controls-below-gate", result.gate_failures)

    def test_window_exposes_direction(self):
        rows = [
            {k: .65 for k in WEIGHTS},
            {k: .75 for k in WEIGHTS},
            {k: .90 for k in WEIGHTS},
        ]
        result = evaluate_window(rows)
        self.assertEqual(result["trend"], "IMPROVING")
        self.assertEqual(result["sample_count"], 3)

    def test_policy_is_configurable(self):
        policy = GatePolicy(min_trust=.8, min_availability=.8)
        sample = {k: .9 for k in WEIGHTS}
        sample["availability_health"] = .75
        self.assertEqual(evaluate(sample, policy).decision, "STOP")


if __name__ == "__main__":
    unittest.main()

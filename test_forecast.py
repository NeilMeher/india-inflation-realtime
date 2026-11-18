import json
import unittest
import forecast


class ForecastTests(unittest.TestCase):
    def test_month_boundary(self):
        self.assertEqual(forecast.month_end("2024-02"), "2024-02-29")

    def test_no_future_in_safe_features(self):
        data = json.loads((forecast.ROOT / "data.json").read_text())
        records, scores = forecast.evaluate(data)
        self.assertEqual(len(records), 8)
        self.assertTrue(all(row["latest_visible"] < row["origin"][:7] for row in records))
        self.assertEqual(scores["leaked_persistence"], 0)
        self.assertGreater(scores["persistence"], scores["leaked_persistence"])

    def test_ar_constant_history(self):
        self.assertEqual(forecast.forecast_ar([3.0] * 6, 4.0), 3)

"""Walk-forward CPI nowcasts indexed by the public release date."""
import calendar
import csv
import html
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def month_end(month):
    year, number = map(int, month.split("-"))
    return f"{month}-{calendar.monthrange(year, number)[1]:02}"


def available(rows, origin):
    return [row for row in rows if row["release"] <= origin]


def forecast_ar(history, lag):
    predictor, outcome = history[:-1], history[1:]
    mean_x, mean_y = statistics.mean(predictor), statistics.mean(outcome)
    variance = sum((x - mean_x)**2 for x in predictor)
    slope = sum((x - mean_x) * (y - mean_y) for x, y in zip(predictor, outcome)) / variance if variance else 0
    return mean_y + slope * (lag - mean_x)


def evaluate(rows):
    predictions = []
    for target in rows:
        origin = month_end(target["month"])
        known = available(rows, origin)
        if len(known) < 5:
            continue
        track = [row["value"] for row in known]
        unsafe_lag = [row["value"] for row in rows if row["month"] <= target["month"]][-1]
        predictions.append(dict(origin=origin, latest_visible=known[-1]["month"], actual=target["value"],
                                persistence=track[-1], autoregression=forecast_ar(track, track[-1]),
                                leaked_persistence=unsafe_lag, leaked_ar=forecast_ar(track, unsafe_lag)))
    keys = ("persistence", "autoregression", "leaked_persistence", "leaked_ar")
    scores = {key: statistics.mean(abs(r[key] - r["actual"]) for r in predictions) for key in keys}
    return predictions, scores


def run():
    rows = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    predictions, scores = evaluate(rows)
    with (ROOT / "backtest.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(predictions[0]))
        writer.writeheader()
        writer.writerows(predictions)
    (ROOT / "metrics.json").write_text(json.dumps(scores, indent=2) + "\n", encoding="utf-8")
    table = "\n".join(f'<tr><td>{r["month"]}</td><td>{r["release"]}</td>'
                       f'<td>{r["value"]:.2f}%</td><td><a href="{html.escape(r["source"])}">Release</a></td></tr>'
                       for r in rows)
    page = """<!doctype html><html lang=en><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>India CPI release timeline</title><style>body{font:1rem/1.6 system-ui;color:#17394d;max-width:55rem;margin:4rem auto;padding:0 1rem;background:#f5f8fb}
table{border-collapse:collapse;width:100%;background:white}td,th{border-bottom:1px solid #d4dde5;padding:.65rem;text-align:left}</style>
<h1>India CPI release timeline</h1><p>First released all-India combined annual inflation.</p>
<table><thead><tr><th>Observation month</th><th>Publication date</th><th>Inflation</th><th>Evidence</th></tr></thead><tbody>"""
    (ROOT / "timeline.html").write_text(page + table + "</tbody></table></html>", encoding="utf-8")
    print(json.dumps(scores, indent=2))


if __name__ == "__main__":
    run()

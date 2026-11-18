# India Inflation in Real Time

How much does using publication dates change apparent forecast performance?

Across eight walk-forward origins, mean absolute error was 0.629 percentage points for persistence and 0.637 for AR(1). The deliberately leaked versions scored 0.000 and 0.170. The leaked persistence run copies the outcome because the faulty merge treats publication as contemporaneous.

## Run locally

Use Python 3.11 or later. Run `python -m unittest -v` and `python forecast.py`. Open `timeline.html` after generating it. The 13 releases cover December 2024 through December 2025. Each month has its original MoSPI publication date, value and source link in `data.json`. No third-party dependencies or keys are required.

The main decision is to join on release date and keep a fixed first-release target. The archive does not reconstruct subsequent revisions, and eight origins give weak evidence on relative forecasting skill. Explain the difference between an observation date and a release date, and identify the exact path through which the outcome enters the contaminated lag.

Neil Meher specified the project and its requirements. Codex assembled and checked the release register and authored the analysis code. Neil's independent data review is pending.

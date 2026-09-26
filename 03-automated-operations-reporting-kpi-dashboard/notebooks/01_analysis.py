"""
Weekly Operations KPI Report
Dataset: appliance call center call log, Jan-Mar 2015 (5,000 calls, 9 agents, 5 departments)

Goal: turn a raw call log into the same weekly KPI report a manager would ask
for: volume, abandonment, first-contact resolution, speed of answer, handle
time, and satisfaction, trended week over week and broken out by department
and agent, the way a workforce/operations coordinator's weekly report works.
"""
import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "call_center_raw.csv")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

pd.set_option("display.width", 140)

# ---------------------------------------------------------------
# 1. Load & clean
# ---------------------------------------------------------------
df = pd.read_csv(DATA_PATH, encoding="latin1")

df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%y")
df["week_start"] = (df["Date"] - pd.to_timedelta(df["Date"].dt.weekday, unit="D"))
df["week_label"] = df["week_start"].dt.strftime("%b %d")

df["answered"] = df["Answered (Y/N)"] == "Y"
df["resolved"] = df["Resolved"] == "Y"

def to_seconds(t):
    if pd.isna(t):
        return None
    h, m, s = str(t).split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)

df["talk_seconds"] = df["AvgTalkDuration"].apply(to_seconds)

print(f"Rows: {len(df):,}  |  Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
print(f"Agents: {df['Agent'].nunique()}  |  Departments: {df['Department'].nunique()}")

# ---------------------------------------------------------------
# 2. Weekly KPI trend (the core "weekly report" table)
# ---------------------------------------------------------------
weekly = df.groupby("week_label").agg(
    week_start=("week_start", "min"),
    calls=("Call Id", "count"),
    answered=("answered", "sum"),
).reset_index()
weekly = weekly.sort_values("week_start")

answered_df = df[df["answered"]]
weekly_answered = answered_df.groupby("week_label").agg(
    resolved=("resolved", "sum"),
    answered_calls=("answered", "sum"),
    avg_speed_of_answer=("Speed of Answer", "mean"),
    avg_handle_time=("talk_seconds", "mean"),
    avg_satisfaction=("Satisfaction rating", "mean"),
).reset_index()

weekly = weekly.merge(weekly_answered, on="week_label", how="left")
weekly["answer_rate"] = weekly["answered"] / weekly["calls"]
weekly["abandonment_rate"] = 1 - weekly["answer_rate"]
weekly["fcr_rate"] = weekly["resolved"] / weekly["answered_calls"]
weekly = weekly.sort_values("week_start").reset_index(drop=True)

print("\n--- Weekly KPI trend ---")
print(weekly[["week_label", "calls", "answer_rate", "fcr_rate", "avg_speed_of_answer",
              "avg_handle_time", "avg_satisfaction"]].round(3))

# Week-over-week change for the headline tiles (last full week vs prior)
latest = weekly.iloc[-1]
prior = weekly.iloc[-2]
print(f"\nLatest week ({latest['week_label']}) vs prior week ({prior['week_label']}):")
print(f"  Calls: {latest['calls']} vs {prior['calls']}")
print(f"  Answer rate: {latest['answer_rate']:.1%} vs {prior['answer_rate']:.1%}")
print(f"  FCR rate: {latest['fcr_rate']:.1%} vs {prior['fcr_rate']:.1%}")
print(f"  Avg satisfaction: {latest['avg_satisfaction']:.2f} vs {prior['avg_satisfaction']:.2f}")

# ---------------------------------------------------------------
# 3. Department breakdown
# ---------------------------------------------------------------
dept = df.groupby("Department").agg(
    calls=("Call Id", "count"),
    answer_rate=("answered", "mean"),
).reset_index()
dept_answered = answered_df.groupby("Department").agg(
    fcr_rate=("resolved", "mean"),
    avg_satisfaction=("Satisfaction rating", "mean"),
    avg_handle_time=("talk_seconds", "mean"),
).reset_index()
dept = dept.merge(dept_answered, on="Department", how="left").sort_values("calls", ascending=False)

print("\n--- By department ---")
print(dept.round(3))

# ---------------------------------------------------------------
# 4. Agent performance
# ---------------------------------------------------------------
agent = df.groupby("Agent").agg(
    calls=("Call Id", "count"),
    answer_rate=("answered", "mean"),
).reset_index()
agent_answered = answered_df.groupby("Agent").agg(
    fcr_rate=("resolved", "mean"),
    avg_satisfaction=("Satisfaction rating", "mean"),
    avg_handle_time=("talk_seconds", "mean"),
).reset_index()
agent = agent.merge(agent_answered, on="Agent", how="left").sort_values("avg_satisfaction", ascending=False)

print("\n--- By agent ---")
print(agent.round(3))

# ---------------------------------------------------------------
# 5. Satisfaction distribution (top-box / bottom-box)
# ---------------------------------------------------------------
sat_counts = answered_df["Satisfaction rating"].value_counts().sort_index()
top_box = answered_df["Satisfaction rating"].isin([4, 5]).mean()
bottom_box = answered_df["Satisfaction rating"].isin([1, 2]).mean()
print(f"\nTop-box satisfaction (4-5): {top_box:.1%}  |  Bottom-box (1-2): {bottom_box:.1%}")

# ---------------------------------------------------------------
# 6. Export for the dashboard
# ---------------------------------------------------------------
weekly.round(4).to_csv(os.path.join(OUT_DIR, "weekly_kpis.csv"), index=False)
dept.round(4).to_csv(os.path.join(OUT_DIR, "department_kpis.csv"), index=False)
agent.round(4).to_csv(os.path.join(OUT_DIR, "agent_kpis.csv"), index=False)
sat_counts.to_csv(os.path.join(OUT_DIR, "satisfaction_distribution.csv"))

print("\nDone. Summary tables written to outputs/.")

"""
Operational Bottleneck & Late-Delivery Risk Analysis
Dataset: DataCo Smart Supply Chain (2015-2018), ~180k order line items.

Goal: find where the order fulfillment process breaks down (which regions,
shipping modes, departments, and time periods drive late deliveries) and
quantify the business cost, then recommend fixes.
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "DataCoSupplyChainDataset.csv")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

pd.set_option("display.width", 140)

# ---------------------------------------------------------------
# 1. Load & clean
# ---------------------------------------------------------------
df = pd.read_csv(DATA_PATH, encoding="latin1")

# Drop PII / not needed for operations analysis
pii_cols = [c for c in df.columns if any(k in c for k in
            ["Email", "Password", "Fname", "Lname", "Street", "Customer Id",
             "Customer Zipcode", "Order Zipcode", "Product Image", "Product Description"])]
df = df.drop(columns=pii_cols)

df["order date (DateOrders)"] = pd.to_datetime(df["order date (DateOrders)"])
df["shipping date (DateOrders)"] = pd.to_datetime(df["shipping date (DateOrders)"])
df["order_month"] = df["order date (DateOrders)"].dt.to_period("M").astype(str)

df["shipping_delay_days"] = df["Days for shipping (real)"] - df["Days for shipment (scheduled)"]
df["is_late"] = df["Late_delivery_risk"] == 1

print(f"Rows: {len(df):,}  |  Date range: {df['order date (DateOrders)'].min().date()} to {df['order date (DateOrders)'].max().date()}")
print(f"Overall late delivery rate: {df['is_late'].mean():.1%}")

# ---------------------------------------------------------------
# 2. Where are the bottlenecks?
# ---------------------------------------------------------------

# By shipping mode
by_mode = df.groupby("Shipping Mode").agg(
    orders=("is_late", "size"),
    late_rate=("is_late", "mean"),
    avg_delay=("shipping_delay_days", "mean"),
).sort_values("late_rate", ascending=False)
print("\n--- Late delivery rate by Shipping Mode ---")
print(by_mode)

# By region
by_region = df.groupby("Order Region").agg(
    orders=("is_late", "size"),
    late_rate=("is_late", "mean"),
    lost_sales=("Sales", lambda s: s[df.loc[s.index, "is_late"]].sum()),
).sort_values("late_rate", ascending=False)
print("\n--- Late delivery rate by Region (top 10) ---")
print(by_region.head(10))

# By department
by_dept = df.groupby("Department Name").agg(
    orders=("is_late", "size"),
    late_rate=("is_late", "mean"),
).sort_values("late_rate", ascending=False)
print("\n--- Late delivery rate by Department ---")
print(by_dept)

# Trend over time
by_month = df.groupby("order_month").agg(
    orders=("is_late", "size"),
    late_rate=("is_late", "mean"),
)

# Business impact: profit lost to late-delivery orders that were also
# unprofitable, and total sales exposed to late delivery
total_sales = df["Sales"].sum()
late_sales = df.loc[df["is_late"], "Sales"].sum()
late_negative_profit_orders = df[(df["is_late"]) & (df["Order Profit Per Order"] < 0)]
print(f"\nSales exposed to late delivery: ${late_sales:,.0f} ({late_sales/total_sales:.1%} of total sales)")
print(f"Late orders that were ALSO unprofitable: {len(late_negative_profit_orders):,} "
      f"(lost ${-late_negative_profit_orders['Order Profit Per Order'].sum():,.0f})")

# Worst combination: region x shipping mode
pivot = df.pivot_table(index="Order Region", columns="Shipping Mode",
                        values="is_late", aggfunc="mean")

# ---------------------------------------------------------------
# 3. Charts
# ---------------------------------------------------------------
plt.rcParams["figure.autolayout"] = True

# Chart 1: late rate by shipping mode
fig, ax = plt.subplots(figsize=(7, 4.5))
by_mode["late_rate"].sort_values().plot(kind="barh", ax=ax, color="#3b6ea5")
ax.set_xlabel("Late delivery rate")
ax.set_title("Late Delivery Rate by Shipping Mode")
ax.xaxis.set_major_formatter(lambda x, _: f"{x:.0%}")
fig.savefig(os.path.join(OUT_DIR, "01_late_rate_by_shipping_mode.png"), dpi=150)
plt.close(fig)

# Chart 2: late rate trend over time
fig, ax = plt.subplots(figsize=(9, 4.5))
by_month["late_rate"].plot(ax=ax, color="#c0392b", marker="o", markersize=3)
ax.set_ylabel("Late delivery rate")
ax.set_title("Late Delivery Rate Over Time")
ax.yaxis.set_major_formatter(lambda x, _: f"{x:.0%}")
fig.savefig(os.path.join(OUT_DIR, "02_late_rate_trend.png"), dpi=150)
plt.close(fig)

# Chart 3: heatmap-style pivot (region x shipping mode)
fig, ax = plt.subplots(figsize=(8, 8))
im = ax.imshow(pivot.values, cmap="Reds", aspect="auto", vmin=0, vmax=1)
ax.set_xticks(range(len(pivot.columns)))
ax.set_xticklabels(pivot.columns, rotation=45, ha="right")
ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels(pivot.index)
ax.set_title("Late Delivery Rate: Region x Shipping Mode")
fig.colorbar(im, ax=ax, label="Late delivery rate")
fig.savefig(os.path.join(OUT_DIR, "03_region_shipping_heatmap.png"), dpi=150)
plt.close(fig)

# Chart 4: late rate by department
fig, ax = plt.subplots(figsize=(7, 4.5))
by_dept["late_rate"].sort_values().plot(kind="barh", ax=ax, color="#3b6ea5")
ax.set_xlabel("Late delivery rate")
ax.set_title("Late Delivery Rate by Department")
ax.xaxis.set_major_formatter(lambda x, _: f"{x:.0%}")
fig.savefig(os.path.join(OUT_DIR, "04_late_rate_by_department.png"), dpi=150)
plt.close(fig)

# ---------------------------------------------------------------
# 4. Export summary tables for the dashboard / README
# ---------------------------------------------------------------
by_mode.to_csv(os.path.join(OUT_DIR, "summary_by_shipping_mode.csv"))
by_region.to_csv(os.path.join(OUT_DIR, "summary_by_region.csv"))
by_dept.to_csv(os.path.join(OUT_DIR, "summary_by_department.csv"))
by_month.to_csv(os.path.join(OUT_DIR, "summary_by_month.csv"))
pivot.to_csv(os.path.join(OUT_DIR, "summary_region_shipping_pivot.csv"))

# Cleaned dataset for Power BI / Tableau
keep_cols = ["order date (DateOrders)", "shipping date (DateOrders)", "order_month",
             "Order Region", "Order Country", "Order State", "Order City",
             "Market", "Department Name", "Category Name", "Shipping Mode",
             "Days for shipping (real)", "Days for shipment (scheduled)",
             "shipping_delay_days", "Late_delivery_risk", "Delivery Status",
             "Order Status", "Sales", "Order Item Quantity", "Order Profit Per Order",
             "Order Item Profit Ratio", "Customer Segment"]
df[keep_cols].to_csv(os.path.join(OUT_DIR, "cleaned_orders_for_bi_tool.csv"), index=False)

print("\nDone. Charts + summary tables written to outputs/.")

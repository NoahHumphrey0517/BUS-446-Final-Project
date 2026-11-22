# ------------------------------------------------------------
# BUS 446 Final Project
# The Changing Age of First-Time Homebuyers in the U.S., 2000-2025
#
# This script:
#   1. Loads the data from the Excel file
#   2. Cleans it and checks for problems
#   3. Calculates summary statistics and the age gap
#   4. Runs a simple linear regression (Year -> Average first-time buyer age)
#   5. Saves the charts to the 2_Visualizations folder
#
# How to run (from the main project folder):
#   python 1_Data_and_Method/src/analysis.py
# ------------------------------------------------------------

import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# ---------- File locations ----------
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA_FILE = os.path.join(PROJECT, "1_Data_and_Method", "data", "raw",
                         "First-Time-Homebuyer-Age-Statistics-yearly_data.xlsx")
CLEAN_FOLDER = os.path.join(PROJECT, "1_Data_and_Method", "data", "processed")
RESULTS_FOLDER = os.path.join(PROJECT, "1_Data_and_Method", "results")
CHART_FOLDER = os.path.join(PROJECT, "2_Visualizations")

for folder in [CLEAN_FOLDER, RESULTS_FOLDER, CHART_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# ---------- Step 1: Load the data ----------
# The data is on the sheet "Chart 1".
# Average ages are in columns C-E and median ages are in columns H-J.
# The data starts on row 6 of the sheet (we skip the 5 title rows).
raw = pd.read_excel(DATA_FILE, sheet_name="Chart 1", header=None, skiprows=5)

df = pd.DataFrame({
    "year": raw[2],
    "avg_first_time": raw[3],
    "avg_repeat": raw[4],
    "median_first_time": raw[8],
    "median_repeat": raw[9],
})

# ---------- Step 2: Clean and check the data ----------
df = df.dropna()                     # remove any empty rows
df = df.astype(float)                # make sure every column is a number
df["year"] = df["year"].astype(int)
df = df.sort_values("year").reset_index(drop=True)

print("Number of years:", len(df))                      # should be 26
print("First and last year:", df["year"].min(), "-", df["year"].max())
print("Missing values:", df.isna().sum().sum())          # should be 0
print("Duplicate years:", df["year"].duplicated().sum()) # should be 0

# ---------- Step 3: Summary statistics ----------
# Age gap = how much older repeat buyers are than first-time buyers
df["avg_gap"] = df["avg_repeat"] - df["avg_first_time"]
df["median_gap"] = df["median_repeat"] - df["median_first_time"]

df.round(2).to_csv(os.path.join(CLEAN_FOLDER, "homebuyer_age_clean.csv"), index=False)

summary = df.drop(columns="year").describe().round(2)
summary.to_csv(os.path.join(RESULTS_FOLDER, "summary_statistics.csv"))
print("\nSummary statistics:\n", summary.to_string())

# Average for three time periods
def period(start, end):
    return df[(df["year"] >= start) & (df["year"] <= end)].drop(columns="year").mean()

periods = pd.DataFrame({
    "2000-2007": period(2000, 2007),
    "2008-2015": period(2008, 2015),
    "2016-2025": period(2016, 2025),
}).T.round(2)
periods.to_csv(os.path.join(RESULTS_FOLDER, "period_averages.csv"))
print("\nPeriod averages:\n", periods.to_string())

# ---------- Step 4: Simple linear regression ----------
# X = year, Y = average age of first-time buyers
reg = stats.linregress(df["year"], df["avg_first_time"])

results_text = f"""Simple Linear Regression
X = Year, Y = Average age of first-time homebuyers (2000-2025, n = {len(df)})

Equation:   Age = {reg.intercept:.2f} + ({reg.slope:.4f} x Year)
Slope:      {reg.slope:.4f} years per year  (about {reg.slope * 10:.2f} years per decade)
R-squared:  {reg.rvalue ** 2:.3f}
p-value:    {reg.pvalue:.6f}

Interpretation: Each year is associated with first-time buyers being about
{abs(reg.slope):.2f} years younger on average. Year explains about
{reg.rvalue ** 2 * 100:.0f}% of the year-to-year variation in average first-time buyer age.
Because p < 0.05, the relationship is statistically significant.
"""
with open(os.path.join(RESULTS_FOLDER, "regression_results.txt"), "w") as f:
    f.write(results_text)
print("\n" + results_text)

# ---------- Step 5: Charts ----------
BLUE = "#2a78d6"     # first-time buyers
ORANGE = "#eb6834"   # repeat buyers
SOURCE = "Source: New York Fed Consumer Credit Panel / Equifax"

plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.alpha": 0.3, "figure.dpi": 150})
years = df["year"]
first = df.iloc[0]
last = df.iloc[-1]


def save(fig, name):
    fig.text(0.01, 0.01, SOURCE, fontsize=8, color="gray")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig(os.path.join(CHART_FOLDER, name), bbox_inches="tight")
    plt.close(fig)


# Chart 1: Average age of first-time buyers
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(years, df["avg_first_time"], color=BLUE, marker="o", linewidth=2)
ax.axvspan(2007.9, 2009.5, color="gray", alpha=0.15)
ax.text(2008.7, 38.1, "Great\nRecession", ha="center", fontsize=9, color="dimgray")
for yr in [2000, 2010, 2025]:
    value = df.loc[df["year"] == yr, "avg_first_time"].values[0]
    offset = -18 if yr == 2010 else 10   # put the 2010 label below the point
    ax.annotate(f"{value:.1f}", (yr, value), textcoords="offset points", xytext=(0, offset),
                ha="center", fontweight="bold")
ax.set_ylim(35, 38.6)
ax.set_title("Average Age of First-Time Homebuyers, 2000-2025", fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Average age (years)")
save(fig, "1_avg_first_time_buyer_age.png")

# Chart 2: First-time vs repeat buyers (average age)
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(years, df["avg_repeat"], color=ORANGE, marker="o", linewidth=2, label="Repeat buyers")
ax.plot(years, df["avg_first_time"], color=BLUE, marker="o", linewidth=2, label="First-time buyers")
for col in ["avg_repeat", "avg_first_time"]:
    ax.annotate(f"{first[col]:.1f}", (2000, first[col]), textcoords="offset points", xytext=(0, 10), ha="center")
    ax.annotate(f"{last[col]:.1f}", (2025, last[col]), textcoords="offset points", xytext=(0, 10), ha="center")
ax.set_ylim(33, 51)
ax.set_title("Average Age: First-Time vs. Repeat Homebuyers", fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Average age (years)")
ax.legend(loc="center left")
save(fig, "2_first_time_vs_repeat_average.png")

# Chart 3: First-time vs repeat buyers (median age)
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(years, df["median_repeat"], color=ORANGE, marker="o", linewidth=2, label="Repeat buyers")
ax.plot(years, df["median_first_time"], color=BLUE, marker="o", linewidth=2, label="First-time buyers")
for col in ["median_repeat", "median_first_time"]:
    ax.annotate(f"{first[col]:.0f}", (2000, first[col]), textcoords="offset points", xytext=(0, 10), ha="center")
    ax.annotate(f"{last[col]:.0f}", (2025, last[col]), textcoords="offset points", xytext=(0, 10), ha="center")
ax.set_ylim(30, 50)
ax.set_title("Median Age: First-Time vs. Repeat Homebuyers", fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Median age (years)")
ax.legend(loc="center left")
save(fig, "3_first_time_vs_repeat_median.png")

# Chart 4: Average vs median for first-time buyers
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(years, df["avg_first_time"], color=BLUE, marker="o", linewidth=2, label="Average (mean)")
ax.plot(years, df["median_first_time"], color=BLUE, linestyle="--", marker="s", linewidth=1.5,
        label="Median")
ax.set_ylim(30, 40)
ax.set_title("First-Time Buyers: Average Age vs. Median Age", fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Age (years)")
ax.legend(loc="upper right")
ax.text(2000, 30.6, "The average is always higher than the median, meaning some older\n"
        "first-time buyers pull the average up.", fontsize=9.5, color="dimgray")
save(fig, "4_average_vs_median_first_time.png")

# Chart 5: Age gap
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.bar(years, df["avg_gap"], color=ORANGE)
for yr in [2000, 2010, 2025]:
    value = df.loc[df["year"] == yr, "avg_gap"].values[0]
    ax.text(yr, value + 0.2, f"{value:.1f}", ha="center", fontweight="bold")
ax.set_ylim(0, 14)
ax.set_title("Age Gap: Repeat Buyers Minus First-Time Buyers (Average Age)", fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Gap (years)")
save(fig, "5_age_gap.png")

# Chart 6: Regression scatter plot with trend line
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.scatter(years, df["avg_first_time"], color=BLUE, label="Actual average age")
ax.plot(years, reg.intercept + reg.slope * years, color="black", linewidth=2, label="Regression line")
ax.text(2013.2, 37.6, f"Age = {reg.intercept:.2f} + ({reg.slope:.4f} x Year)\n"
        f"R² = {reg.rvalue ** 2:.2f},  p < 0.001", fontsize=10,
        bbox=dict(facecolor="white", edgecolor="lightgray"))
ax.set_title("Regression: Year vs. Average Age of First-Time Buyers", fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Average age (years)")
ax.legend(loc="lower left")
save(fig, "6_regression.png")

print("Charts saved to", CHART_FOLDER)

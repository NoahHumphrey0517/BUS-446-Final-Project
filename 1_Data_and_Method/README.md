# 1 · Data and Method

## Folder Contents

| File / Folder | Description |
|---|---|
| `data/raw/First-Time-Homebuyer-Age-Statistics-yearly_data.xlsx` | Original dataset (unchanged) |
| `data/processed/homebuyer_age_clean.csv` | Cleaned data with the age gap columns added |
| `src/analysis.py` | Python code for cleaning, statistics, regression and charts |
| `results/summary_statistics.csv` | Mean, min, max, etc. for each variable |
| `results/period_averages.csv` | Averages for 2000–2007, 2008–2015 and 2016–2025 |
| `results/regression_results.txt` | Regression equation, R² and p-value |
| `Project_Task_Plan.docx` | Our original project plan |

## Data Source

- **Dataset:** First-Time Homebuyer Age Statistics – Yearly Data
- **Original source:** New York Fed Consumer Credit Panel / Equifax
- **Published by:** Edward J. Pinto, Joseph S. Tracy and Donghoon Lee, *Median First-Time Homebuyer Age at 34 Years in 2025, Little Changed from 2024*, American Enterprise Institute (2025)
- **Coverage:** United States, yearly, 2000–2025 (26 years)

## How to Access the Data

1. **In this repository:** the original Excel file is in the `data/raw/` folder.
2. **From the source:** go to the AEI report page and download the data:
   https://www.aei.org/research-products/report/median-first-time-homebuyer-age-at-34-years-in-2025-little-changed-from-2024/pdf/

In the Excel file, the data is on the **"Chart 1"** sheet. Average ages are in columns C–E and median ages are in columns H–J.

## Variables

| Variable | Description |
|---|---|
| `year` | Year (2000–2025) |
| `avg_first_time` | Average age of first-time buyers |
| `avg_repeat` | Average age of repeat buyers |
| `median_first_time` | Median age of first-time buyers |
| `median_repeat` | Median age of repeat buyers |
| `avg_gap` | Repeat average minus first-time average |
| `median_gap` | Repeat median minus first-time median |

## Method

1. **Clean the data:** load the Excel file, keep the needed columns, and check for missing values and duplicate years. All 26 years were complete.
2. **Descriptive statistics:** calculate the mean, minimum and maximum, the age gap, and averages for three time periods.
3. **Visualize:** create line charts, a bar chart and a scatter plot (saved in `2_Visualizations`).
4. **Regression:** run a simple linear regression with X = year and Y = average first-time buyer age.

## Regression Result

**Age = 191.36 − 0.0769 × Year**, with R² = 0.58 and p < 0.001.

On average, first-time buyers got about 0.08 years (about one month) younger each year. The result is statistically significant. These numbers can also be checked in Excel using `=SLOPE()`, `=INTERCEPT()` and `=RSQ()`.

## How to Run

From the main project folder:

```bash
pip install -r requirements.txt
python 1_Data_and_Method/src/analysis.py
```

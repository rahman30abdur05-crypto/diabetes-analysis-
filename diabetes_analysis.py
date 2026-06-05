# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
#
#
# # ── Load the dataset ──────────────────────────────────────────
# df = pd.read_csv("diabetes.csv")
#
# # ── First look at the data ────────────────────────────────────
# print("=" * 50)
# print("SHAPE (rows, columns):")
# print(df.shape)
#
# print("\nFIRST 5 ROWS:")
# print(df.head())
#
# print("\nCOLUMN NAMES:")
# print(df.columns.tolist())
#
# print("\nBASIC STATISTICS:")
# print(df.describe())
#
# print("\nMISSING VALUES:")
# print(df.isnull().sum())





import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ── Load the dataset ──────────────────────────────────────────
df = pd.read_csv("diabetes.csv")

# ── First look at the data ────────────────────────────────────
print("=" * 50)
print("SHAPE (rows, columns):")
print(df.shape)

print("\nFIRST 5 ROWS:")
print(df.head())

print("\nCOLUMN NAMES:")
print(df.columns.tolist())

print("\nBASIC STATISTICS:")
print(df.describe())

print("\nMISSING VALUES:")
print(df.isnull().sum())

# ── Data Cleaning ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("DATA CLEANING")
print("=" * 50)

# These columns CANNOT be zero medically
cols_with_zeros = ["Glucose", "BloodPressure",
                   "SkinThickness", "Insulin", "BMI"]

# Count zeros in each column
print("\nZero values (hidden missing data):")
for col in cols_with_zeros:
    zero_count = (df[col] == 0).sum()
    percentage = (zero_count / len(df)) * 100
    print(f"  {col:<25}: {zero_count} zeros ({percentage:.1f}%)")

# Replace 0s with NaN
df[cols_with_zeros] = df[cols_with_zeros].replace(0, np.nan)

# Fill missing values with median
df[cols_with_zeros] = df[cols_with_zeros].fillna(
    df[cols_with_zeros].median()
)

print("\n✅ Zeros replaced with median values")
print("\nAfter cleaning — Missing Values:")
print(df.isnull().sum())

print("\nAfter cleaning — New Statistics:")
print(df[["Glucose", "BloodPressure", "BMI"]].describe().round(2))



# ── VISUALIZATION ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("GENERATING CHARTS...")
print("=" * 50)

# Set style for all charts
sns.set_style("whitegrid")
sns.set_palette("husl")

# ── Chart 1: Diabetes Distribution ────────────────────────────
plt.figure(figsize=(15, 10))

plt.subplot(2, 3, 1)
outcome_counts = df["Outcome"].value_counts()
plt.pie(outcome_counts,
        labels=["No Diabetes", "Diabetes"],
        autopct="%1.1f%%",
        colors=["#2ecc71", "#e74c3c"],
        startangle=90)
plt.title("Diabetes Distribution", fontsize=13, fontweight="bold")

# ── Chart 2: Glucose Distribution ─────────────────────────────
plt.subplot(2, 3, 2)
df[df["Outcome"] == 0]["Glucose"].hist(alpha=0.6,
                                        color="#2ecc71",
                                        label="No Diabetes",
                                        bins=20)
df[df["Outcome"] == 1]["Glucose"].hist(alpha=0.6,
                                        color="#e74c3c",
                                        label="Diabetes",
                                        bins=20)
plt.xlabel("Glucose Level")
plt.ylabel("Number of Patients")
plt.title("Glucose by Diabetes Status", fontsize=13, fontweight="bold")
plt.legend()

# ── Chart 3: BMI Distribution ─────────────────────────────────
plt.subplot(2, 3, 3)
df[df["Outcome"] == 0]["BMI"].hist(alpha=0.6,
                                    color="#2ecc71",
                                    label="No Diabetes",
                                    bins=20)
df[df["Outcome"] == 1]["BMI"].hist(alpha=0.6,
                                    color="#e74c3c",
                                    label="Diabetes",
                                    bins=20)
plt.xlabel("BMI")
plt.ylabel("Number of Patients")
plt.title("BMI by Diabetes Status", fontsize=13, fontweight="bold")
plt.legend()

# ── Chart 4: Age Distribution ──────────────────────────────────
plt.subplot(2, 3, 4)
df[df["Outcome"] == 0]["Age"].hist(alpha=0.6,
                                    color="#2ecc71",
                                    label="No Diabetes",
                                    bins=20)
df[df["Outcome"] == 1]["Age"].hist(alpha=0.6,
                                    color="#e74c3c",
                                    label="Diabetes",
                                    bins=20)
plt.xlabel("Age")
plt.ylabel("Number of Patients")
plt.title("Age by Diabetes Status", fontsize=13, fontweight="bold")
plt.legend()

# ── Chart 5: Glucose vs BMI Scatter ───────────────────────────
plt.subplot(2, 3, 5)
colors = df["Outcome"].map({0: "#2ecc71", 1: "#e74c3c"})
plt.scatter(df["BMI"], df["Glucose"],
            c=colors, alpha=0.5, s=20)
plt.xlabel("BMI")
plt.ylabel("Glucose Level")
plt.title("BMI vs Glucose", fontsize=13, fontweight="bold")

# ── Chart 6: Average values by Outcome ────────────────────────
plt.subplot(2, 3, 6)
avg_by_outcome = df.groupby("Outcome")[
    ["Glucose", "BMI", "Age", "BloodPressure"]
].mean()
avg_by_outcome.T.plot(kind="bar",
                      ax=plt.gca(),
                      color=["#2ecc71", "#e74c3c"])
plt.title("Avg Values: Diabetic vs Non-Diabetic",
          fontsize=13, fontweight="bold")
plt.xticks(rotation=30)
plt.legend(["No Diabetes", "Diabetes"])

plt.tight_layout()
plt.savefig("diabetes_charts.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n✅ Charts saved as diabetes_charts.png")






# ── CORRELATION ANALYSIS ──────────────────────────────────────
print("\n" + "=" * 50)
print("CORRELATION ANALYSIS")
print("=" * 50)

# How strongly each factor relates to diabetes
correlation = df.corr()["Outcome"].sort_values(ascending=False)
print("\nCorrelation with Diabetes (Outcome):")
print(correlation.round(3))

# ── Heatmap ───────────────────────────────────────────────────
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr().round(2),
            annot=True,
            cmap="RdYlGn",
            center=0,
            fmt=".2f",
            linewidths=0.5)
plt.title("Correlation Heatmap — All Features",
          fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("correlation_heatmap.png", dpi=150, bbox_inches="tight")
plt.show()
print("✅ Heatmap saved as correlation_heatmap.png")

# ── Risk Factor Summary ───────────────────────────────────────
print("\n" + "=" * 50)
print("RISK FACTOR SUMMARY")
print("=" * 50)

diabetic     = df[df["Outcome"] == 1]
non_diabetic = df[df["Outcome"] == 0]

factors = ["Glucose", "BMI", "Age",
           "BloodPressure", "Insulin"]

print(f"\n{'Factor':<25} {'Non-Diabetic':>14} "
      f"{'Diabetic':>12} {'Difference':>12}")
print("-" * 65)

for factor in factors:
    avg_no  = non_diabetic[factor].mean()
    avg_yes = diabetic[factor].mean()
    diff    = ((avg_yes - avg_no) / avg_no) * 100
    print(f"{factor:<25} {avg_no:>14.1f} "
          f"{avg_yes:>12.1f} {diff:>+11.1f}%")




# ── FINAL MEDICAL REPORT ──────────────────────────────────────
print("\n" + "=" * 55)
print("   📋 DIABETES RISK ANALYSIS REPORT")
print("=" * 55)

total     = len(df)
diabetic  = df[df["Outcome"] == 1]
non_diab  = df[df["Outcome"] == 0]

print(f"""
DATASET OVERVIEW:
  Total Patients     : {total}
  Diabetic           : {len(diabetic)} ({len(diabetic)/total*100:.1f}%)
  Non-Diabetic       : {len(non_diab)} ({len(non_diab)/total*100:.1f}%)

AVERAGE VALUES COMPARISON:
  {'Factor':<28} {'Non-Diabetic':>13} {'Diabetic':>10}
  {'-'*53}""")

factors = ["Glucose", "BMI", "Age", "BloodPressure", "Insulin"]
for f in factors:
    avg_no  = non_diab[f].mean()
    avg_yes = diabetic[f].mean()
    diff    = ((avg_yes - avg_no) / avg_no) * 100
    arrow   = "🔺" if diff > 0 else "🔻"
    print(f"  {f:<28} {avg_no:>13.1f} {avg_yes:>10.1f}  "
          f"{arrow}{abs(diff):.1f}%")

print(f"""
HIGH RISK PATIENTS:
  Glucose > 140      : {len(df[df['Glucose'] > 140])} patients
  BMI > 35           : {len(df[df['BMI'] > 35])} patients
  Age > 50           : {len(df[df['Age'] > 50])} patients
  All 3 risk factors : {len(df[(df['Glucose']>140) &
                               (df['BMI']>35) &
                               (df['Age']>50)])} patients

KEY FINDINGS:
  1. Glucose is the strongest diabetes predictor (r=0.49)
  2. Diabetic patients have 27% higher glucose on average
  3. BMI is 2nd strongest predictor (r=0.31)
  4. Risk increases significantly after age 35
  5. 48.7% of insulin data was missing — data quality issue

CLINICAL CONCLUSION:
  High glucose + High BMI + Older age =
  Highest risk combination for diabetes
  in this Pima Indian female population.
""")
print("=" * 55)
print("✅ Analysis Complete!")
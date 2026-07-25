# %%
import pandas as pd

df = pd.read_csv(r"C:\Users\DELL\OneDrive\Documents\healthcare_system\dataset\dataset.csv")

diseases = sorted(df["Disease"].unique())

print("\nTotal Diseases:", len(diseases))
print("-" * 50)

for disease in diseases:
    print(disease)
# %%

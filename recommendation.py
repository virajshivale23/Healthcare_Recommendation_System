# %%

import pandas as pd

# Load CSV files
description_df = pd.read_csv("dataset/symptom_Description.csv")
precaution_df = pd.read_csv("dataset/symptom_precaution.csv")
medicine_df = pd.read_csv("dataset/medicine_recommendation.csv")


def get_description(disease):
    row = description_df[description_df["Disease"] == disease]

    if not row.empty:
        return row["Description"].values[0]

    return "Description not available."


def get_precautions(disease):
    row = precaution_df[precaution_df["Disease"] == disease]

    if not row.empty:
        return [
            row["Precaution_1"].values[0],
            row["Precaution_2"].values[0],
            row["Precaution_3"].values[0],
            row["Precaution_4"].values[0]
        ]

    return []


def get_medicine_details(disease):
    row = medicine_df[medicine_df["Disease"] == disease]

    if row.empty:
        return {
            "Medicine": "Consult Doctor",
            "Diet": "Balanced Diet",
            "Exercise": "Light Exercise",
            "Doctor": "General Physician"
        }

    return {
        "Medicine": row["Medicine"].values[0],
        "Diet": row["Diet"].values[0],
        "Exercise": row["Exercise"].values[0],
        "Doctor": row["Doctor"].values[0]
    }
# %%

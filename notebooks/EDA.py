# %%
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)

plt.style.use("ggplot")
# %%
df = pd.read_csv(r"C:\Users\DELL\OneDrive\Documents\healthcare_system\dataset\dataset.csv")

df.head()
# %%
print("Rows :", df.shape[0])
print("Columns :", df.shape[1])
# %%
df.columns
# %%
# DATASET INFORMATION
df.info()
# %%
# MISSING VALUES
df.isnull().sum()
# %%
# duplicate records 
print("Duplicate Rows :", df.duplicated().sum())
# %%
df.drop_duplicates(inplace=True)

df.reset_index(drop=True, inplace=True)

# %%
# NUMBER OF DISEASES 
df["Disease"].nunique()
# displaying names 
sorted(df["Disease"].unique())

# %%
# DISEASE DISTRIBUTION
df["Disease"].value_counts()

# %%
# PLoTTING DISEASE DISTRIBUTION
plt.figure(figsize=(12,10))

df["Disease"].value_counts().plot(kind="bar")

plt.title("Disease Distribution")

plt.xlabel("Disease")

plt.ylabel("Count")

plt.xticks(rotation=90)

plt.show()
# %%
# CHECKING MISSING SYMPTOMS
symptom_columns = [col for col in df.columns if "Symptom" in col]

df[symptom_columns].isnull().sum()

# %%
# COUNTING UNIQUE SYMPTOMS
symptoms = []

for col in symptom_columns:
    symptoms.extend(df[col].dropna().tolist())

len(set(symptoms))

# %%
# TOP 20 MOST FREQUENT SYMPTOMS

from collections import Counter

counter = Counter(symptoms)

top20 = counter.most_common(20)

top20
# %%
# VISUALIZING TOP SYMPTOMS 
top_df = pd.DataFrame(top20, columns=["Symptom","Count"])

plt.figure(figsize=(12,6))

sns.barplot(data=top_df,
            x="Count",
            y="Symptom")

plt.title("Top 20 Most Common Symptoms")

plt.show()
# %%

# STORING SYMPTOMS COLUMNS 
symptom_columns = [col for col in df.columns if col.startswith("Symptom")]

symptom_columns

# %%
# FINFDING ALL UNIQUE SYMPTOMS 
all_symptoms = []

for col in symptom_columns:
    all_symptoms.extend(df[col].dropna().unique())

all_symptoms = sorted(list(set(all_symptoms)))

print("Total Unique Symptoms:", len(all_symptoms))

# %%
# CREATING BINARY FEATURE MATRIX 
X = pd.DataFrame(
    data=0,
    index=df.index,
    columns=all_symptoms
)

X.head()

# %%
# FILL BINARY MATRIX 
for index, row in df.iterrows():

    for symptom in symptom_columns:

        if pd.notna(row[symptom]):

            X.loc[index, row[symptom]] = 1

# %%
#  VERIFYING MATRIX 
X.head()

# %%
# CREATING TARGET VARIABLES 
y = df["Disease"]

y.head()
# %%
# ENCODFING DISEASE LABELS
from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()

y_encoded = encoder.fit_transform(y)

y_encoded[:10]
# %%
# SAVING DISEASE MAPPING 
disease_mapping = pd.DataFrame({
    "Disease": encoder.classes_,
    "Encoded": range(len(encoder.classes_))
})

disease_mapping
# %%
# TRAIN TEST SPLIT 

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)
# %%
# VEERIFYING SHAPES 
print("Training Shape :", X_train.shape)
print("Testing Shape  :", X_test.shape)
print("Training Labels:", y_train.shape)
print("Testing Labels :", y_test.shape)
# %%
# IMPORTING ML LIBARIRIES
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# %%
# TRAINNG LOGISTIC REGRESSION 
lr = LogisticRegression(max_iter=1000)

lr.fit(X_train, y_train)

lr_pred = lr.predict(X_test)

print("Logistic Regression Accuracy:",
      accuracy_score(y_test, lr_pred))
# %%
# TRAINING DECISION TREE CLASSIFIER
dt = DecisionTreeClassifier(random_state=42)

dt.fit(X_train, y_train)

dt_pred = dt.predict(X_test)

print("Decision Tree Accuracy:",
      accuracy_score(y_test, dt_pred))
# %%
# Training Random Forest Classifier
rf = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

rf.fit(X_train, y_train)

rf_pred = rf.predict(X_test)

print("Random Forest Accuracy:",
      accuracy_score(y_test, rf_pred))
# %%
# Training Gaussian Naive Bayes Classifier
nb = GaussianNB()

nb.fit(X_train, y_train)

nb_pred = nb.predict(X_test)

print("Naive Bayes Accuracy:",
      accuracy_score(y_test, nb_pred))
# %%

# comparing all models
results = {
    "Logistic Regression":
        accuracy_score(y_test, lr_pred),

    "Decision Tree":
        accuracy_score(y_test, dt_pred),

    "Random Forest":
        accuracy_score(y_test, rf_pred),

    "Naive Bayes":
        accuracy_score(y_test, nb_pred)
}

results_df = pd.DataFrame(
    results.items(),
    columns=["Model", "Accuracy"]
)

results_df.sort_values(
    by="Accuracy",
    ascending=False
)
# %%
# classsification report 
print(classification_report(
    y_test,
    rf_pred,
    target_names=encoder.classes_
))
# %%
# CONFUSION MATRIX
import matplotlib.pyplot as plt
import seaborn as sns

cm = confusion_matrix(y_test, rf_pred)

plt.figure(figsize=(12,10))

sns.heatmap(
    cm,
    cmap="Blues",
    annot=False
)

plt.title("Random Forest Confusion Matrix")

plt.xlabel("Predicted")

plt.ylabel("Actual")

plt.show()
# %%
# FEATURE IMPORTANCE 
feature_importance = pd.DataFrame({
    "Symptom": X.columns,
    "Importance": rf.feature_importances_
})

feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)

feature_importance.head(20)
# %%
# PLOTTING TOP 20 IMP SYMPTOIMS 
plt.figure(figsize=(10,8))

sns.barplot(
    data=feature_importance.head(20),
    x="Importance",
    y="Symptom"
)

plt.title("Top 20 Important Symptoms")

plt.show()
# %%
# saving the best model
import joblib
import os

os.makedirs("models", exist_ok=True)

joblib.dump(rf, "models/disease_prediction_model.pkl")
joblib.dump(encoder, "models/label_encoder.pkl")

print("✅ Model Saved Successfully!")
# %%
import joblib

joblib.dump(list(X.columns), "models/symptom_columns.pkl")
# %%

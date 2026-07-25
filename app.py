
from flask import Flask, render_template, request
import pandas as pd
import joblib

from recommendation import (
    get_description,
    get_precautions,
    get_medicine_details
)

app = Flask(__name__)

# Load model
model = joblib.load("models/disease_prediction_model.pkl")
encoder = joblib.load("models/label_encoder.pkl")
symptom_columns = joblib.load("models/symptom_columns.pkl")


@app.route("/")
def home():
    return render_template(
        "index.html",
        symptoms=symptom_columns
    )


@app.route("/predict", methods=["POST"])
def predict():

    selected_symptoms = request.form.getlist("symptoms")

    # Create input vector
    input_data = [0] * len(symptom_columns)

    for symptom in selected_symptoms:
        if symptom in symptom_columns:
            index = symptom_columns.index(symptom)
            input_data[index] = 1

    prediction = model.predict([input_data])[0]
    disease = encoder.inverse_transform([prediction])[0]

    description = get_description(disease)
    precautions = get_precautions(disease)
    details = get_medicine_details(disease)

    return render_template(
        "result.html",
        disease=disease,
        description=description,
        precautions=precautions,
        medicine=details["Medicine"],
        diet=details["Diet"],
        exercise=details["Exercise"],
        doctor=details["Doctor"]
    )


if __name__ == "__main__":
    app.run(debug=True)
# %%

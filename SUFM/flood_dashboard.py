
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load the trained Random Forest model
model = joblib.load("flood_model.pkl")

# Load dataset
dataset_path = "manhole_flood_dataset.csv"
df = pd.read_csv(dataset_path)

# Streamlit app layout
st.title("🌊 Smart Urban Flood Management - Prediction Dashboard")
st.sidebar.title("💡 Input Features")

# Sidebar inputs for real-time predictions
debris_level = st.sidebar.slider("Debris Level", min_value=0, max_value=200, value=50)
water_level = st.sidebar.slider("Water Level (cm)", min_value=0, max_value=500, value=120)
methane = st.sidebar.slider("Methane Level (ppm)", min_value=0, max_value=100, value=30)
h2s = st.sidebar.slider("H2S Level (ppm)", min_value=0, max_value=100, value=20)
co = st.sidebar.slider("CO Level (ppm)", min_value=0, max_value=100, value=40)

# Store inputs in a DataFrame
input_data = pd.DataFrame([[debris_level, water_level, methane, h2s, co]],
                          columns=['debris_level', 'water_level', 'methane', 'h2s', 'co'])

# Make Prediction
prediction = model.predict(input_data)[0]
probability = model.predict_proba(input_data)[0][1]

# Display the Prediction Result
st.subheader("🚀 Prediction Result")
if prediction == 1:
    st.error(f"🌊 Flood Risk Detected! Probability: {probability*100:.2f}%")
else:
    st.success(f"✅ No Flood Risk. Probability: {(1-probability)*100:.2f}%")

# Display Dataset
st.subheader("📊 Dataset Preview")
st.write(df.head())

# Model evaluation
X = df.drop('flood_status', axis=1)
y = df['flood_status']
y_pred = model.predict(X)
accuracy = accuracy_score(y, y_pred)
st.write(f"✅ Model Accuracy: {accuracy:.2f}")

# Classification report
st.subheader("📄 Classification Report")
st.text(classification_report(y, y_pred))

# Confusion Matrix
st.subheader("🔍 Confusion Matrix")
conf_matrix = confusion_matrix(y, y_pred)

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues",
            xticklabels=["No Flood", "Flood"],
            yticklabels=["No Flood", "Flood"])
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
st.pyplot(fig)

# Feature Importance
st.subheader("📈 Feature Importance")
feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
}).sort_values(by="Importance", ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=feature_importance, palette='viridis')
plt.title("Feature Importance in Flood Prediction")
st.pyplot(fig)

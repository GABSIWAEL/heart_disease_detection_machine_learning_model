import pickle
from pathlib import Path

import streamlit as st


FEATURE_NAMES = (
	"age",
	"sex",
	"cp",
	"trestbps",
	"chol",
	"fbs",
	"restecg",
	"thalach",
	"exang",
	"oldpeak",
	"slope",
	"ca",
	"thal",
)


@st.cache_resource
def load_model():
	model_path = (
		Path(__file__).resolve().parents[1]
		/ "Our_Trained_Model"
		/ "heart_disease_model.sav"
	)
	with model_path.open("rb") as model_file:
		return pickle.load(model_file)


st.set_page_config(page_title="Heart Disease Prediction", page_icon="Heart", layout="wide")
st.title("Heart Disease Prediction")
st.write(
	"Enter the patient's measurements to get a prediction from the trained model. "
	"Categorical inputs use the numeric codes from the training dataset."
)

try:
	model = load_model()
except FileNotFoundError:
	st.error("The trained model was not found. Check the Our_Trained_Model folder.")
	st.stop()
except Exception as error:
	st.error(f"The trained model could not be loaded: {error}")
	st.stop()

with st.form("prediction_form"):
	first_column, second_column, third_column = st.columns(3)

	with first_column:
		age = st.number_input("Age", min_value=1, max_value=120, value=45, step=1)
		sex = st.selectbox("Sex", options=[0, 1], format_func=lambda value: "Female" if value == 0 else "Male")
		cp = st.selectbox("Chest pain type (cp)", options=[0, 1, 2, 3])
		trestbps = st.number_input(
			"Resting blood pressure (trestbps)",
			min_value=0,
			max_value=300,
			value=120,
			step=1,
		)

	with second_column:
		chol = st.number_input(
			"Serum cholesterol (chol)", min_value=0, max_value=1000, value=200, step=1
		)
		fbs = st.selectbox(
			"Fasting blood sugar > 120 mg/dl (fbs)",
			options=[0, 1],
			format_func=lambda value: "No" if value == 0 else "Yes",
		)
		restecg = st.selectbox("Resting ECG result (restecg)", options=[0, 1, 2])
		thalach = st.number_input(
			"Maximum heart rate (thalach)", min_value=0, max_value=300, value=150, step=1
		)
		exang = st.selectbox(
			"Exercise-induced angina (exang)",
			options=[0, 1],
			format_func=lambda value: "No" if value == 0 else "Yes",
		)

	with third_column:
		oldpeak = st.number_input(
			"ST depression (oldpeak)",
			min_value=0.0,
			max_value=10.0,
			value=0.0,
			step=0.1,
			format="%.1f",
		)
		slope = st.selectbox("Slope of peak exercise ST segment (slope)", options=[0, 1, 2])
		ca = st.selectbox("Number of major vessels (ca)", options=[0, 1, 2, 3, 4])
		thal = st.selectbox("Thalassemia result (thal)", options=[0, 1, 2, 3])

	submitted = st.form_submit_button("Predict")

if submitted:
	input_by_feature = {
		"age": age,
		"sex": sex,
		"cp": cp,
		"trestbps": trestbps,
		"chol": chol,
		"fbs": fbs,
		"restecg": restecg,
		"thalach": thalach,
		"exang": exang,
		"oldpeak": oldpeak,
		"slope": slope,
		"ca": ca,
		"thal": thal,
	}
	input_values = [input_by_feature[name] for name in FEATURE_NAMES]
	prediction = int(model.predict([input_values])[0])

	if prediction == 1:
		st.error("The model detected a signal associated with heart disease.")
	else:
		st.success("The model did not detect a signal associated with heart disease.")

st.caption(
	"For educational purposes only. This prediction is not a diagnosis and should not "
	"replace advice from a qualified healthcare professional."
)

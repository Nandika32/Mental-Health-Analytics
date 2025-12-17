from sklearn.linear_model import LogisticRegression
import numpy as np
import streamlit as st
import pandas as pd

# ------------------------------
# PAGE CONFIGURATION
# ------------------------------
st.set_page_config(
    page_title="Mental Health Survey",
    page_icon="🧠",
    layout="centered"
)

# ------------------------------
# CUSTOM CSS (UI BEAUTIFICATION)
# ------------------------------
st.markdown("""
    <style>

/* ---------- Global smoothness ---------- */
* {
    transition: background-color 0.25s ease, color 0.25s ease;
}

/* ---------- Title ---------- */
.big-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #6EA8FE, #B197FC);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}

.subtitle {
    text-align: center;
    font-size: 17px;
    color: var(--text-color);
    opacity: 0.75;
    margin-bottom: 30px;
}

/* ---------- Card / Question Box ---------- */
.question-box {
    background-color: var(--secondary-background-color);
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 18px;
    border: 1px solid rgba(120,120,120,0.25);
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    color: var(--text-color);
}

/* ---------- Section headers ---------- */
.section-title {
    font-size: 24px;
    font-weight: 700;
    margin-top: 35px;
    margin-bottom: 15px;
    color: var(--text-color);
}

/* ---------- Buttons ---------- */
.stButton > button {
    width: 100%;
    border-radius: 14px;
    height: 3.2em;
    font-size: 17px;
    font-weight: 600;
    background: linear-gradient(90deg, #6EA8FE, #B197FC);
    color: white;
    border: none;
}

.stButton > button:hover {
    opacity: 0.9;
}

/* ---------- Sliders ---------- */
.stSlider > div {
    padding-top: 5px;
}

/* ---------- Success box ---------- */
.stAlert {
    border-radius: 14px;
}

/* ---------- Remove harsh Streamlit padding ---------- */
.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------
# PAGE TITLE
# ------------------------------
st.markdown("<div class='big-title'>🧠 Mental Health Awareness Survey</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Your honest responses help improve mental health insights.</div>", unsafe_allow_html=True)

st.write("---")

# ------------------------------
# SURVEY QUESTIONS
# ------------------------------

st.markdown("<div class='section-title'>Personal Details</div>", unsafe_allow_html=True)
name = st.text_input("Your Name")
age = st.number_input("Age", min_value=10, max_value=80, step=1)
gender = st.selectbox("Gender", ["Female", "Male", "Non-binary", "Prefer not to say"])

st.write("---")

st.markdown("### Psychological Questions")

def ask_question(text):
    st.markdown(f"<div class='question-box'>{text}</div>", unsafe_allow_html=True)
    return st.slider("Select intensity:", 1, 5, 3, key=text)
    st.caption("1 = Very low   •   3 = Moderate   •   5 = Very high")


q1 = ask_question("1. How often do you feel stressed?")
q2 = ask_question("2. Do you feel overwhelmed by daily tasks?")
q3 = ask_question("3. How often do you feel anxious or worried?")
q4 = ask_question("4. Do you have trouble sleeping?")
q5 = ask_question("5. Do you feel socially isolated or lonely?")

st.write("---")

# ------------------------------
# SCORING SYSTEM
# ------------------------------
score = q1 + q2 + q3 + q4 + q5

if score <= 10:
    level = "🟢 Low Stress — You're doing okay!"
elif score <= 17:
    level = "🟡 Moderate Stress — Pay attention to your mental health."
else:
    level = "🔴 High Stress — You may need rest or support."
# --- Simple ML Model (Educational Purpose) ---

# Training data (dummy but structured)
X_train = np.array([
    [1,1,1,1,1],
    [2,2,2,2,2],
    [3,3,3,3,3],
    [4,4,4,4,4],
    [5,5,5,5,5]
])

y_train = ["Low", "Low", "Moderate", "High", "High"]

model = LogisticRegression()
model.fit(X_train, y_train)

prediction = model.predict([[q1, q2, q3, q4, q5]])[0]

# ------------------------------
# SAVE & SHOW RESULT
# ------------------------------
if st.button("Submit Survey"):
    data = {
        "Name": name,
        "Age": age,
        "Gender": gender,
        "Stress Score": score,
        "Stress Level": level
    }

    df = pd.DataFrame([data])

    import os
    file_path = "mental_health_responses.csv"

    if not os.path.exists(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode="a", index=False, header=False)

    st.success("🎉 Survey submitted successfully!")
    st.subheader("Your Mental Health Result:")
    st.info(f"**{level}**")
    st.subheader("🤖 ML-Based Stress Prediction")
    st.info(f"Predicted Stress Level: **{prediction}**")
st.write("---")
st.warning(
    "⚠️ **Disclaimer**: This tool is for educational and awareness purposes only. "
    "It does NOT provide medical advice or diagnosis. "
    "If you are experiencing distress, please consult a qualified mental health professional."
)

import streamlit as st
import numpy as np
import pandas as pd
import os
import pickle

model = pickle.load(open("model.pkl", "rb"))
from streamlit_lottie import st_lottie
import requests

def load_lottie(url):
    return requests.get(url).json()
    
st.set_page_config(
    page_title="Diabetes Risk Prediction",
    page_icon="🩺",
    layout="wide"
)

# ----------------------------
# SESSION INIT
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

# ----------------------------
# CSS (KEEP YOUR STYLE)
# ----------------------------
st.markdown("""
<style>
body {
    background-color: #f4f6f9;
}
.hero {
    padding: 40px;
    border-radius: 15px;
    background: linear-gradient(90deg, #0f2027, #203a43, #2c5364);
    color: white;
    text-align: center;
    margin-bottom: 30px;
}
.card {
    background: white;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
}
.stButton>button {
    background-color: #1f77b4;
    color: white;
    height: 50px;
    width: 100%;
    border-radius: 10px;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# LOGIN SCREEN
# ----------------------------
def login():
    st.markdown("""
    <div class="hero">
        <h1>🧠 Diabetes AI Platform</h1>
        <p>Secure Login</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)

   user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if os.path.exists("users.csv"):
            users = pd.read_csv("users.csv")

            if ((users["username"] == user) & (users["password"] == pwd)).any():
                st.session_state.page = "home"
                st.session_state.user = user
            else:
                st.error("Invalid credentials")
        else:
            st.error("No users found")

    if st.button("Create New Account"):
        st.session_state.page = "signup"

        st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# HOME SCREEN
# ----------------------------
def home():
    st.markdown("""
    <div class="hero">
        <h1>🩺 Diabetes Risk Prediction System</h1>
        <p>AI-powered health risk assessment tool</p>
    </div>
    """, unsafe_allow_html=True)

    # ✅ ADD LOTTIE HERE
    lottie = load_lottie("https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json")
    st_lottie(lottie, height=200)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Welcome to the System")
    st.write("""
    This system helps predict diabetes risk using AI.
    Click below to start prediction.
    """)

    if st.button("🚀 Start Prediction"):
        st.session_state.page = "predict"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# PREDICTION LOGIC
# ----------------------------
# def calculate_risk(age, glucose, bp, insulin, skin, bmi):
    # score = 0
    # if glucose > 140:
        # score += 30
    # if bmi > 30:
        # score += 20
    # if age > 45:
        # score += 15
    # if bp > 90:
        # score += 15
    # if insulin > 150:
        # score += 10
    # if skin > 35:
        # score += 10
    # return min(score, 100)

# ----------------------------
# PREDICT SCREEN (YOUR UI)
# ----------------------------
def predict():
    st.markdown("""
    <div class="hero">
        <h1>🩺 Diabetes Risk Prediction</h1>
        <p>Enter patient details</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    # ---------------- INPUT SECTION ----------------
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        with c1:
            age = st.number_input("Age", 1, 120)
            glucose = st.number_input("Glucose", 0.0, 300.0)
            bp = st.number_input("Blood Pressure", 0.0, 200.0)

        with c2:
            insulin = st.number_input("Insulin", 0.0, 900.0)
            skin = st.number_input("Skin Thickness", 0.0, 100.0)
            bmi = st.number_input("BMI", 0.0, 60.0)

        # ✅ BUTTON DEFINED HERE
        predict_btn = st.button("Predict Risk")

        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- RESULT SECTION ----------------
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        if predict_btn:
            with st.spinner("🧠 AI is analyzing patient data..."):
                import time
                time.sleep(2)

            # ✅ ML MODEL INPUT FORMAT (IMPORTANT ORDER)
            input_data = np.array([[0, glucose, bp, skin, insulin, bmi, 0, age]])

            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][1]

            risk = int(probability * 100)

            # UI Output
            st.progress(risk / 100)
            st.metric("Risk Score", f"{risk}%")

            # Save history
            new_data = pd.DataFrame([[age, glucose, bp, insulin, skin, bmi, risk]],
                columns=["Age","Glucose","BP","Insulin","Skin","BMI","Risk"])

            if os.path.exists("history.csv"):
                new_data.to_csv("history.csv", mode='a', header=False, index=False)
            else:
                new_data.to_csv("history.csv", index=False)

            # Result
            if prediction == 1:
                st.error("⚠ High Risk of Diabetes")
            else:
                st.success("✅ Low Risk")

        else:
            st.info("Enter details and click Predict")

        st.markdown('</div>', unsafe_allow_html=True)
        
    # st.markdown("""
    # <div class="hero">
        # <h1>🩺 Diabetes Risk Prediction</h1>
        # <p>Enter patient details</p>
    # </div>
    # """, unsafe_allow_html=True)

    # col1, col2 = st.columns([2, 1])

    # with col1:
        # st.markdown('<div class="card">', unsafe_allow_html=True)

        # c1, c2 = st.columns(2)

        # with c1:
            # age = st.number_input("Age", 1, 120)
            # glucose = st.number_input("Glucose", 0.0, 300.0)
            # bp = st.number_input("Blood Pressure", 0.0, 200.0)

        # with c2:
            # insulin = st.number_input("Insulin", 0.0, 900.0)
            # skin = st.number_input("Skin Thickness", 0.0, 100.0)
            # bmi = st.number_input("BMI", 0.0, 60.0)

        # predict_btn = st.button("Predict Risk")

        # st.markdown('</div>', unsafe_allow_html=True)

    # with col2:
        # st.markdown('<div class="card">', unsafe_allow_html=True)

        # if predict_btn:
            # risk = calculate_risk(age, glucose, bp, insulin, skin, bmi)

            # st.progress(risk / 100)
            # st.metric("Risk Score", f"{risk}%")

            # # Save history
            # new_data = pd.DataFrame([[age, glucose, bp, insulin, skin, bmi, risk]],
                # columns=["Age","Glucose","BP","Insulin","Skin","BMI","Risk"])

            # if os.path.exists("history.csv"):
                # new_data.to_csv("history.csv", mode='a', header=False, index=False)
            # else:
                # new_data.to_csv("history.csv", index=False)

            # if risk >= 50:
                # st.error("⚠ High Risk of Diabetes")
            # else:
                # st.success("✅ Low Risk")

        # else:
            # st.info("Enter details and click Predict")

        # st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# HISTORY SCREEN
# ----------------------------
def history():
    st.title("📋 History")

    if os.path.exists("history.csv"):
        df = pd.read_csv("history.csv")
        st.dataframe(df)
    else:
        st.info("No records yet")

# ----------------------------
# SIDEBAR NAVIGATION
# ----------------------------
if st.session_state.page != "login":

    page = st.sidebar.radio(
        "Navigation",
        ["Home", "Predict", "History"],
        index=["home","predict","history"].index(st.session_state.page)
    )

    if page == "Home":
        st.session_state.page = "home"
    elif page == "Predict":
        st.session_state.page = "predict"
    elif page == "History":
        st.session_state.page = "history"

# ----------------------------
# ROUTING
# ----------------------------
if st.session_state.page == "login":
    login()
elif st.session_state.page == "home":
    home()
elif st.session_state.page == "predict":
    predict()
elif st.session_state.page == "history":
    history()

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("""
<hr>
<center>
<p style='color:grey'>Final Year Project | Diabetes Prediction App</p>
</center>
""", unsafe_allow_html=True)
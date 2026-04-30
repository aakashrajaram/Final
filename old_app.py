
import streamlit as st
st.markdown("""
<style>

/* Full background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Center container */
.center-card {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 80vh;
}

/* Glass card */
.card {
    background: rgba(255, 255, 255, 0.08);
    padding: 40px;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    width: 350px;
    text-align: center;
}

/* Inputs */
input {
    border-radius: 10px !important;
}

/* Button */
.stButton>button {
    width: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    height: 45px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f2027;
}

</style>
""", unsafe_allow_html=True)

import numpy as np
import pickle
import pandas as pd
import time
import os
import matplotlib.pyplot as plt

model = pickle.load(open("model.pkl", "rb"))

st.set_page_config(page_title="Diabetes Prediction Application", layout="wide")

# UI Styling
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #1f4037, #99f2c8);
}
.block-container {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 20px;
}
.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
    height: 45px;
}
[data-testid="stSidebar"] {
    background: #0f2027;
}
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "login"

def login():
    st.markdown('<div class="center-card">', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.image("assets/logo.png", width=80)

    st.markdown("## Welcome Back 👋")
    st.caption("AI Healthcare Platform")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "haritha" and pwd == "1234":
            st.session_state.page = "home"
        else:
            st.error("Invalid credentials")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def home():
    st.markdown("## 🧠 Diabetes Prediction with ML")

    col1, col2 = st.columns([1,1])

    with col1:
        st.image("assets/logo.png", width=200)
        st.markdown("### Smart Healthcare with AI")
        st.write("""
        Predict diabetes risk instantly using machine learning.
        Built for faster and smarter healthcare decisions.
        """)

        if st.button("🚀 Start Prediction"):
            st.session_state.page = "predict"

    with col2:
        st.markdown("""
        ### ✨ Features

        ✔ AI-powered prediction  
        ✔ Real-time results  
        ✔ Health analytics dashboard  
        ✔ Secure login system  
        ✔ History tracking  
        """)

def predict():
    st.title("🩺 Enter Details")

    glucose = st.slider("Glucose", 0, 200)
    bp = st.slider("Blood Pressure", 0, 140)
    bmi = st.slider("BMI", 0.0, 50.0)
    age = st.slider("Age", 1, 100)

    if st.button("Predict"):
        with st.spinner("Analyzing..."):
            time.sleep(2)

        data = np.array([[0, glucose, bp, 0, 0, bmi, 0, age]])
        result = model.predict(data)[0]
        prob = model.predict_proba(data)[0][1]

        st.session_state.result = result
        st.session_state.conf = prob
        st.session_state.page = "result"

def result():
    st.title("📊 Result")

    res = st.session_state.result
    conf = st.session_state.conf * 100

    if res == 1:
        st.error(f"High Risk ({round(conf,2)}%)")
    else:
        st.success(f"Low Risk ({round(conf,2)}%)")

    st.progress(int(conf))

def dashboard():
    st.title("📈 Dashboard")

    if os.path.exists("history.csv"):
        df = pd.read_csv("history.csv")
        st.dataframe(df)

def about():
    st.title("About")
    st.write("Diabetes Prediction ML App")

if st.session_state.page != "login":
    st.sidebar.image("assets/logo.png", width=100)
    st.sidebar.markdown("## 🧠 Diabetes AI App")
    page = st.sidebar.radio("Go to", ["Home","Predict","Dashboard","About"])

    if page == "Home":
        st.session_state.page = "home"
    elif page == "Predict":
        st.session_state.page = "predict"
    elif page == "Dashboard":
        st.session_state.page = "dashboard"
    elif page == "About":
        st.session_state.page = "about"

if st.session_state.page == "login":
    login()
elif st.session_state.page == "home":
    home()
elif st.session_state.page == "predict":
    predict()
elif st.session_state.page == "result":
    result()
elif st.session_state.page == "dashboard":
    dashboard()
elif st.session_state.page == "about":
    about()
st.markdown("""
<hr>
<p style='text-align:center; font-size:14px; color:lightgray;'>
Built with ❤️ using Machine Learning | Final Year Project
</p>
""", unsafe_allow_html=True)
import streamlit as st
import numpy as np
import pandas as pd
import os
import pickle
import time
import requests
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="Diabetes Risk Prediction",
    page_icon="🩺",
    layout="wide"
)

model = pickle.load(open("model.pkl", "rb"))

if "page" not in st.session_state:
    st.session_state.page = "login"

if "user" not in st.session_state:
    st.session_state.user = None


def load_lottie(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception:
        return None
    return None


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
    margin-bottom: 20px;
}

.stButton>button {
    background-color: #1f77b4;
    color: white;
    height: 50px;
    width: 100%;
    border-radius: 10px;
    font-size: 18px;
    border: none;
}

.stButton>button:hover {
    background-color: #155d8b;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #0f2027;
}

[data-testid="stSidebar"] * {
    color: white;
}
</style>
""", unsafe_allow_html=True)


def login():
    st.markdown("""
    <div class="hero">
        <h1>🧠 Diabetes AI Platform</h1>
        <p>Secure Login for Diabetes Risk Prediction System</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🔐 Login")

        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):
            if os.path.exists("users.csv"):
                users = pd.read_csv("users.csv")

                if ((users["username"] == user) & (users["password"] == pwd)).any():
                    st.session_state.page = "home"
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            else:
                st.error("No users found. Please create an account first.")

        st.markdown("---")

        if st.button("Create New Account"):
            st.session_state.page = "signup"
            st.rerun()

        st.info("Default login: admin / 1234")
        st.markdown('</div>', unsafe_allow_html=True)


def signup():
    st.markdown("""
    <div class="hero">
        <h1>📝 Create New Account</h1>
        <p>Register as a new user to access the prediction system</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        new_user = st.text_input("Choose Username")
        new_pass = st.text_input("Choose Password", type="password")
        confirm_pass = st.text_input("Confirm Password", type="password")

        if st.button("Sign Up"):
            if not new_user or not new_pass:
                st.warning("Please enter username and password.")
            elif new_pass != confirm_pass:
                st.error("Passwords do not match.")
            else:
                if os.path.exists("users.csv"):
                    users = pd.read_csv("users.csv")
                else:
                    users = pd.DataFrame(columns=["username", "password"])

                if new_user in users["username"].values:
                    st.error("Username already exists. Please choose another.")
                else:
                    new_data = pd.DataFrame(
                        [[new_user, new_pass]],
                        columns=["username", "password"]
                    )

                    new_data.to_csv(
                        "users.csv",
                        mode="a",
                        header=not os.path.exists("users.csv"),
                        index=False
                    )

                    st.success("Account created successfully. Please login.")
                    st.session_state.page = "login"
                    st.rerun()

        if st.button("Back to Login"):
            st.session_state.page = "login"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


def home():
    st.markdown("""
    <div class="hero">
        <h1>🩺 Diabetes Risk Prediction System</h1>
        <p>AI-powered health risk assessment tool using Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Welcome to the System")
        st.write("""
        This application predicts diabetes risk using a Machine Learning model.
        Users can enter health-related attributes such as glucose level, blood pressure,
        BMI, insulin level, gender, and family history. The system then produces a
        risk score and stores the result for dashboard analysis.
        """)

        st.markdown("### Key Features")
        st.write("""
        ✅ User login and signup module  
        ✅ ML-based diabetes risk prediction  
        ✅ Gender and genetic/family-history attributes  
        ✅ Prediction history tracking  
        ✅ Dashboard charts and visual analysis  
        """)

        if st.button("🚀 Start Prediction"):
            st.session_state.page = "predict"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        lottie = load_lottie("https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json")
        if lottie:
            st_lottie(lottie, height=300)
        else:
            st.info("Animation could not be loaded. Please check internet connection.")


def predict():
    st.markdown("""
    <div class="hero">
        <h1>🩺 Diabetes Risk Prediction</h1>
        <p>Enter patient details for AI-based diabetes risk analysis</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Enter Patient Details")

        c1, c2 = st.columns(2)

        with c1:
            age = st.number_input("Patient Age", min_value=1, max_value=120, value=30)
            glucose = st.number_input("Glucose Level (mg/dL)", min_value=0.0, max_value=300.0, value=120.0)
            bp = st.number_input("Blood Pressure (mm Hg)", min_value=0.0, max_value=200.0, value=80.0)
            gender = st.selectbox("Gender", ["Male", "Female"])

        with c2:
            insulin = st.number_input("Insulin (mu U/ml)", min_value=0.0, max_value=900.0, value=80.0)
            skin = st.number_input("Skin Thickness (mm)", min_value=0.0, max_value=100.0, value=20.0)
            bmi = st.number_input("BMI", min_value=0.0, max_value=60.0, value=25.0)
            genetics = st.selectbox("Family History / Genetics", ["No", "Yes"])

        predict_btn = st.button("Predict Risk")

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Prediction Result")

        if predict_btn:
            with st.spinner("🧠 AI is analyzing patient data..."):
                time.sleep(2)

            input_data = np.array([[0, glucose, bp, skin, insulin, bmi, 0, age]])

            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][1]

            risk = int(probability * 100)

            st.progress(risk / 100)
            st.metric("Risk Score", f"{risk}%")

            if prediction == 1:
                st.error("⚠ High Risk of Diabetes")
                result_text = "High Risk"
            else:
                st.success("✅ Low Risk of Diabetes")
                result_text = "Low Risk"

            new_data = pd.DataFrame(
                [[
                    st.session_state.user,
                    age,
                    gender,
                    genetics,
                    glucose,
                    bp,
                    insulin,
                    skin,
                    bmi,
                    risk,
                    result_text
                ]],
                columns=[
                    "User",
                    "Age",
                    "Gender",
                    "Genetics",
                    "Glucose",
                    "BP",
                    "Insulin",
                    "Skin",
                    "BMI",
                    "Risk",
                    "Result"
                ]
            )

            new_data.to_csv(
                "history.csv",
                mode="a",
                header=not os.path.exists("history.csv"),
                index=False
            )

            st.caption("Note: Gender and genetics are stored for dashboard analysis. To use them directly in the ML model, retraining is required with a dataset containing these fields.")

        else:
            st.info("Enter details and click Predict Risk.")

        st.markdown('</div>', unsafe_allow_html=True)


def dashboard():
    st.markdown("""
    <div class="hero">
        <h1>📊 Analytics Dashboard</h1>
        <p>Visual analysis of prediction history</p>
    </div>
    """, unsafe_allow_html=True)

    if not os.path.exists("history.csv"):
        st.info("No prediction data available yet.")
        return

    df = pd.read_csv("history.csv")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    total_predictions = len(df)
    avg_risk = round(df["Risk"].mean(), 2)
    high_risk_count = len(df[df["Result"] == "High Risk"])
    low_risk_count = len(df[df["Result"] == "Low Risk"])

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Predictions", total_predictions)
    m2.metric("Average Risk", f"{avg_risk}%")
    m3.metric("High Risk Cases", high_risk_count)
    m4.metric("Low Risk Cases", low_risk_count)

    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Risk Score Trend")
        st.line_chart(df["Risk"])
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Result Distribution")
        result_counts = df["Result"].value_counts()
        st.bar_chart(result_counts)
        st.markdown('</div>', unsafe_allow_html=True)

    c3, c4 = st.columns(2)

    with c3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Gender-wise Average Risk")
        gender_risk = df.groupby("Gender")["Risk"].mean()
        st.bar_chart(gender_risk)
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Genetics / Family History Risk")
        genetics_risk = df.groupby("Genetics")["Risk"].mean()
        st.bar_chart(genetics_risk)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Glucose, BMI and Risk Comparison")
    st.line_chart(df[["Glucose", "BMI", "Risk"]])
    st.markdown('</div>', unsafe_allow_html=True)


def history():
    st.markdown("""
    <div class="hero">
        <h1>📋 Prediction History</h1>
        <p>Stored records of previous diabetes risk predictions</p>
    </div>
    """, unsafe_allow_html=True)

    if os.path.exists("history.csv"):
        df = pd.read_csv("history.csv")
        st.dataframe(df, use_container_width=True)

        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download History as CSV",
            data=csv_data,
            file_name="diabetes_prediction_history.csv",
            mime="text/csv"
        )
    else:
        st.info("No records yet.")


def about():
    st.markdown("""
    <div class="hero">
        <h1>ℹ️ About Project</h1>
        <p>Diabetes Prediction Web Application using Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("""
    This final year project is designed to predict diabetes risk using a Machine Learning model.
    The system uses Python, Streamlit, Pandas, NumPy, and Scikit-learn. It includes user
    authentication, prediction history, dashboard charts, and enhanced input attributes such
    as gender and family history/genetics.
    """)

    st.markdown("""
    **Technology Used**
    - Python
    - Streamlit
    - Pandas
    - NumPy
    - Scikit-learn
    - CSV-based storage
    """)
    st.markdown('</div>', unsafe_allow_html=True)


if st.session_state.page not in ["login", "signup"]:
    st.sidebar.markdown("## 🧠 Diabetes AI App")
    st.sidebar.caption(f"Logged in as: {st.session_state.user}")

    page_names = ["Home", "Predict", "Dashboard", "History", "About"]
    page_keys = ["home", "predict", "dashboard", "history", "about"]

    current_index = page_keys.index(st.session_state.page) if st.session_state.page in page_keys else 0

    selected_page = st.sidebar.radio(
        "Navigation",
        page_names,
        index=current_index
    )

    st.session_state.page = page_keys[page_names.index(selected_page)]

    if st.sidebar.button("Logout"):
        st.session_state.page = "login"
        st.session_state.user = None
        st.rerun()


if st.session_state.page == "login":
    login()
elif st.session_state.page == "signup":
    signup()
elif st.session_state.page == "home":
    home()
elif st.session_state.page == "predict":
    predict()
elif st.session_state.page == "dashboard":
    dashboard()
elif st.session_state.page == "history":
    history()
elif st.session_state.page == "about":
    about()


st.markdown("""
<hr>
<center>
<p style='color:grey'>Final Year Project | Diabetes Prediction App using Machine Learning</p>
</center>
""", unsafe_allow_html=True)

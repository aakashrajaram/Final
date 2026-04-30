
import streamlit as st
import pandas as pd
import numpy as np
import os
import pickle

st.set_page_config(page_title="Diabetes App", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "login"

model = pickle.load(open("model.pkl","rb"))

def login():
    st.title("Login")
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

    if st.button("Signup"):
        st.session_state.page = "signup"

def signup():
    st.title("Signup")
    user = st.text_input("New Username")
    pwd = st.text_input("New Password", type="password")

    if st.button("Create Account"):
        if os.path.exists("users.csv"):
            users = pd.read_csv("users.csv")
        else:
            users = pd.DataFrame(columns=["username","password"])

        if user in users["username"].values:
            st.error("User exists")
        else:
            pd.DataFrame([[user,pwd]], columns=["username","password"]).to_csv("users.csv", mode='a', header=not os.path.exists("users.csv"), index=False)
            st.success("Account created")
            st.session_state.page = "login"

def home():
    st.title("Home")
    if st.button("Start Prediction"):
        st.session_state.page = "predict"

def predict():
    st.title("Prediction")

    age = st.number_input("Age",1,120)
    glucose = st.number_input("Glucose",0.0,300.0)
    bp = st.number_input("BP",0.0,200.0)
    insulin = st.number_input("Insulin",0.0,900.0)
    skin = st.number_input("Skin",0.0,100.0)
    bmi = st.number_input("BMI",0.0,60.0)

    gender = st.selectbox("Gender",["Male","Female"])
    genetic = st.selectbox("Family History",["No","Yes"])

    if st.button("Predict"):
        input_data = np.array([[0, glucose, bp, skin, insulin, bmi, 0, age]])
        pred = model.predict(input_data)[0]
        prob = model.predict_proba(input_data)[0][1]

        risk = int(prob*100)
        st.progress(risk/100)
        st.metric("Risk", f"{risk}%")

        df = pd.DataFrame([[age, glucose, bp, insulin, skin, bmi, gender, genetic, risk]],
        columns=["Age","Glucose","BP","Insulin","Skin","BMI","Gender","Genetics","Risk"])

        df.to_csv("history.csv", mode='a', header=not os.path.exists("history.csv"), index=False)

        if pred == 1:
            st.error("High Risk")
        else:
            st.success("Low Risk")

def dashboard():
    st.title("Dashboard")
    if os.path.exists("history.csv"):
        df = pd.read_csv("history.csv")
        st.bar_chart(df["Risk"])
        st.line_chart(df[["Glucose","Risk"]])
    else:
        st.info("No data")

def history():
    st.title("History")
    if os.path.exists("history.csv"):
        st.dataframe(pd.read_csv("history.csv"))

if st.session_state.page != "login":
    page = st.sidebar.radio("Nav",["Home","Predict","Dashboard","History"])

    if page == "Home":
        st.session_state.page="home"
    elif page=="Predict":
        st.session_state.page="predict"
    elif page=="Dashboard":
        st.session_state.page="dashboard"
    elif page=="History":
        st.session_state.page="history"

if st.session_state.page=="login":
    login()
elif st.session_state.page=="signup":
    signup()
elif st.session_state.page=="home":
    home()
elif st.session_state.page=="predict":
    predict()
elif st.session_state.page=="dashboard":
    dashboard()
elif st.session_state.page=="history":
    history()

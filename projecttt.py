# studyvault_app.py
# -------------------------------
# STUDY VAULT - STREAMLIT FRONTEND
# This file handles UI, dashboards, uploads, links, analytics views, etc.
# Works with: studyvault_ml_dl.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from project2 import (
    predict_study_time,
    recommend_topics,
    classify_notes,
    generate_quiz_from_text,
)

st.set_page_config(page_title="Study Vault", layout="wide")
# ------------------ LOGIN GATE ------------------
st.sidebar.title("🔐 Login")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    username = st.sidebar.text_input("Enter Username")
    password = st.sidebar.text_input("Enter Password", type="password")

    if st.sidebar.button("Login"):
        if username and password:
            st.session_state["logged_in"] = True
            st.session_state["user"] = username
            st.rerun()
        else:
            st.sidebar.warning("Please enter username and password")

    # ❗ VERY IMPORTANT — STOP HERE
    st.stop()

# After successful login
st.sidebar.success(f"Logged in as {st.session_state['user']}")

# Logout
if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.rerun()

# -------------------------------
# Sidebar Navigation
# -------------------------------
st.sidebar.title("📚 Study Vault")
menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Upload Notes",
        "YouTube Resources",
        "Performance Analytics",
        "Smart Recommendations",
        "Auto Quiz Generator",
    ],
)

# -------------------------------
# Session State
# -------------------------------
if "notes" not in st.session_state:
    st.session_state.notes = []

if "youtube_links" not in st.session_state:
    st.session_state.youtube_links = []

if "study_data" not in st.session_state:
    st.session_state.study_data = pd.DataFrame(
        columns=["Date", "Subject", "Hours"]
    )

# -------------------------------
# Dashboard
# -------------------------------
if menu == "Dashboard":
    st.title("📊 Study Dashboard")

    subject = st.text_input("Subject")
    hours = st.number_input("Hours Studied", 0.0, 24.0)

    if st.button("Add Record"):
        new_row = {
            "Date": datetime.now(),
            "Subject": subject,
            "Hours": hours,
        }
        st.session_state.study_data = pd.concat(
            [st.session_state.study_data, pd.DataFrame([new_row])],
            ignore_index=True,
        )

    st.dataframe(st.session_state.study_data)

    if not st.session_state.study_data.empty:
        fig, ax = plt.subplots()
        st.session_state.study_data.groupby("Subject")["Hours"].sum().plot(
            kind="bar", ax=ax
        )
        st.pyplot(fig)

# -------------------------------
# Upload Notes
# -------------------------------
if menu == "Upload Notes":
    st.title("📄 Upload Study Notes")
    file = st.file_uploader("Upload Text File", type=["txt"])

    if file:
        content = file.read().decode("utf-8")
        st.text_area("File Content", content, height=200)

        category = classify_notes(content)
        st.success(f"Predicted Category: {category}")

        st.session_state.notes.append(content)

# -------------------------------
# YouTube Resources
# -------------------------------
if menu == "YouTube Resources":
    st.title("🎥 YouTube Study Links")
    link = st.text_input("Paste YouTube Link")

    if st.button("Add Link"):
        st.session_state.youtube_links.append(link)

    for l in st.session_state.youtube_links:
        st.write(l)

# -------------------------------
# Performance Analytics
# -------------------------------
if menu == "Performance Analytics":
    st.title("📈 Performance Prediction")

    prev_hours = st.number_input("Previous Day Study Hours", 0.0, 24.0)
    sleep = st.number_input("Sleep Hours", 0.0, 12.0)

    if st.button("Predict Today's Study Capacity"):
        prediction = predict_study_time(prev_hours, sleep)
        st.info(f"Recommended Study Hours Today: {prediction:.2f}")

# -------------------------------
# Smart Recommendations
# -------------------------------
if menu == "Smart Recommendations":
    st.title("🤖 Topic Recommendations")
    interest = st.text_input("Enter Subject of Interest")

    if st.button("Recommend Topics"):
        recs = recommend_topics(interest)
        for r in recs:
            st.write("-", r)

# -------------------------------
# Auto Quiz Generator
# -------------------------------
if menu == "Auto Quiz Generator":
    st.title("📝 Quiz from Notes")

    if st.session_state.notes:
        quiz = generate_quiz_from_text(st.session_state.notes[-1])
        for q in quiz:
            st.write("Q:", q)
    else:
        st.warning("Upload notes first.")

import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh
import sqlite3
from reportlab.pdfgen import canvas
from datetime import datetime

# Page Config
st.set_page_config(
    page_title="Cyber Threat Detection",
    page_icon="🛡",
    layout="wide"
)

# ---------------- LOGIN SYSTEM ---------------- #

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login():

    st.title("🔐 AI Cyber Threat Detection Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.success("Login Successful ✅")
            st.rerun()

        else:
            st.error("Invalid Username or Password")


if not st.session_state.logged_in:
    login()
    st.stop()

    # Save threats into database

def save_threat(attack_type, severity):

    conn = sqlite3.connect("threat_logs.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO threats (
            attack_type,
            severity
        )
        VALUES (?, ?)
        """,
        (attack_type, severity)
    )

    conn.commit()

    conn.close()

    # Send Email Alert

import smtplib
from email.mime.text import MIMEText

def send_email_alert(threat_count, severity):

    sender_email = "ritwikvarshney25@gmail.com"

    sender_password = "alse wmdp slvz jfkl"

    receiver_email = "ritwikvarshney25@gmail.com"

    subject = "🚨 Cyber Threat Alert"

    body = f"""
    ALERT!

    Threats Detected: {threat_count}

    Severity Level: {severity}

    AI Cyber Threat Detection System
    """

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    server = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    server.starttls()

    server.login(
        sender_email,
        sender_password
    )

    server.send_message(msg)

    server.quit()

# ---------------- MAIN DASHBOARD ---------------- #

# Generate PDF Report

def generate_pdf(threat_count, severity):

    pdf = canvas.Canvas("Threat_Report.pdf")

    pdf.setFont("Helvetica-Bold", 18)

    pdf.drawString(
        150,
        800,
        "AI Cyber Threat Detection Report"
    )

    pdf.setFont("Helvetica", 12)

    pdf.drawString(
        50,
        750,
        f"Generated Time: {datetime.now()}"
    )

    pdf.drawString(
        50,
        720,
        f"Threats Detected: {threat_count}"
    )

    pdf.drawString(
        50,
        690,
        f"Threat Severity: {severity}"
    )

    pdf.drawString(
        50,
        660,
        "System Status: Monitoring Active"
    )

    pdf.drawString(
        50,
        630,
        "AI Model: Random Forest Classifier"
    )

    pdf.save()

st.title("🛡 AI-Powered Cyber Threat Detection System")

# Auto refresh every 5 seconds

st_autorefresh(
    interval=5000,
    key="dashboard_refresh"
)

st.markdown("---")

# Load trained model

import os
from sklearn.ensemble import RandomForestClassifier

# Load or Train Model

model = joblib.load("model/trained_model.pkl")

    # Load dataset
    train_data = pd.read_csv(
        "dataset/data.csv",
        header=None
    )

    # Encode categorical columns
    for col in train_data.columns:

        le = LabelEncoder()

        train_data[col] = le.fit_transform(
            train_data[col].astype(str)
        )

    # Features and Labels
    X = train_data.iloc[:, :-1]

    y = train_data.iloc[:, -1]

    # Train model
    model = RandomForestClassifier()

    model.fit(X, y)

    # Create model folder
    os.makedirs(
        "model",
        exist_ok=True
    )

    # Save model
    joblib.dump(
        model,
        "model/trained_model.pkl"
    )

# Upload CSV
uploaded_file = st.file_uploader("📂 Upload CSV File")

if uploaded_file is not None:

    # Read CSV
    data = pd.read_csv(uploaded_file, header=None)

    st.subheader("📊 Uploaded Dataset")
    st.dataframe(data.head())

    # Encode categorical columns
    for col in data.columns:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col].astype(str))

    # Remove last column (label column)
    data = data.iloc[:, :-1]

    # Prediction
    prediction = model.predict(data)

    # Attack Labels
    attack_names = []

    for p in prediction:

        if p == 0:
            attack_names.append("Normal Traffic")

        elif p == 1:
            attack_names.append("DOS Attack")

        elif p == 2:
            attack_names.append("Probe Attack")

        else:
            attack_names.append("Threat Detected")

    # Add prediction column
    data["Prediction"] = attack_names

    # Show prediction results
    st.subheader("🛡 Prediction Results")
    st.dataframe(data.head())

    # Threat summary
    threat_counts = data["Prediction"].value_counts()

    # ---------------- LIVE ALERTS ---------------- #

    st.subheader("🚨 Live Threat Alerts")

    normal_count = len(
        data[data["Prediction"] == "Normal Traffic"]
    )

    threat_count = len(data) - normal_count

    # Threat severity

    if threat_count > 100:
        severity = "CRITICAL"

    elif threat_count > 50:
        severity = "HIGH"

    elif threat_count > 20:
        severity = "MEDIUM"

    else:
        severity = "LOW"

    # Save threat into database

    if threat_count > 0:

        save_threat(
            "Cyber Attack",
            severity
        )
          
        send_email_alert(
        threat_count,
        severity
    )

        st.error(
            f"⚠ {threat_count} Threats Detected in Network Traffic"
        )

        st.warning(
            f"Threat Severity: {severity}"
        )

    else:

        st.success("✅ No Threats Detected")

    # ---------------- PIE CHART ---------------- #

    st.subheader("🥧 Threat Distribution Pie Chart")

    fig, ax = plt.subplots(figsize=(8, 8))

    wedges, texts, autotexts = ax.pie(
        threat_counts,
        autopct="%1.1f%%",
        startangle=90,
        textprops={'fontsize': 12}
    )

    for text in texts:
        text.set_visible(False)

    ax.legend(
        wedges,
        threat_counts.index,
        title="Threat Types",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    plt.tight_layout()

    st.pyplot(fig)

    # PDF Report Button

    if st.button("📄 Generate PDF Report"):

        generate_pdf(
            threat_count,
            severity
        )

        st.success(
            "✅ PDF Report Generated Successfully"
        )

    # ---------------- METRICS ---------------- #

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Records",
            len(data)
        )

    with col2:
        st.metric(
            "Detected Threats",
            threat_count
        )
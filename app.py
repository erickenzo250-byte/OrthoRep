import streamlit as st
from datetime import date
from database import SessionLocal, init_db, Rep, Doctor, Procedure, Case
import pandas as pd

# Initialize DB
init_db()
db = SessionLocal()

st.set_page_config(page_title="Ortho Tracker", layout="wide")

st.title("🏥 Ortho Tracker Dashboard")

menu = st.sidebar.selectbox("Menu", [
    "Dashboard",
    "Add Rep",
    "Add Doctor",
    "Add Procedure",
    "Add Case",
    "View Data"
])

# DASHBOARD
if menu == "Dashboard":
    st.subheader("📊 Overview")

    cases = db.query(Case).all()

    data = []
    for c in cases:
        data.append({
            "Date": c.date,
            "Rep": c.rep.name,
            "Doctor": c.doctor.name,
            "Hospital": c.doctor.hospital,
            "Procedure": c.procedure.type
        })

    df = pd.DataFrame(data)

    if not df.empty:
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Cases", len(df))
        col2.metric("Doctors", df["Doctor"].nunique())
        col3.metric("Reps", df["Rep"].nunique())

        st.subheader("Cases by Procedure")
        st.bar_chart(df["Procedure"].value_counts())

        st.subheader("Cases by Doctor")
        st.bar_chart(df["Doctor"].value_counts())

    else:
        st.info("No data yet")

# ADD REP
elif menu == "Add Rep":
    st.subheader("Add Sales Rep")

    name = st.text_input("Rep Name")

    if st.button("Save"):
        db.add(Rep(name=name))
        db.commit()
        st.success("Rep added")

# ADD DOCTOR
elif menu == "Add Doctor":
    st.subheader("Add Doctor")

    name = st.text_input("Doctor Name")
    hospital = st.text_input("Hospital")

    if st.button("Save"):
        db.add(Doctor(name=name, hospital=hospital))
        db.commit()
        st.success("Doctor added")

# ADD PROCEDURE
elif menu == "Add Procedure":
    st.subheader("Add Procedure")

    ptype = st.selectbox("Type", ["THR", "TKR", "Trauma", "Spine"])

    if st.button("Save"):
        db.add(Procedure(type=ptype))
        db.commit()
        st.success("Procedure added")

# ADD CASE
elif menu == "Add Case":
    st.subheader("Add Surgery Case")

    reps = db.query(Rep).all()
    doctors = db.query(Doctor).all()
    procedures = db.query(Procedure).all()

    rep = st.selectbox("Rep", reps, format_func=lambda x: x.name)
    doctor = st.selectbox("Doctor", doctors, format_func=lambda x: f"{x.name} ({x.hospital})")
    procedure = st.selectbox("Procedure", procedures, format_func=lambda x: x.type)
    case_date = st.date_input("Date", date.today())

    if st.button("Save Case"):
        new_case = Case(
            rep_id=rep.id,
            doctor_id=doctor.id,
            procedure_id=procedure.id,
            date=case_date
        )
        db.add(new_case)
        db.commit()
        st.success("Case recorded")

# VIEW DATA
elif menu == "View Data":
    st.subheader("All Cases")

    cases = db.query(Case).all()

    data = []
    for c in cases:
        data.append({
            "Date": c.date,
            "Rep": c.rep.name,
            "Doctor": c.doctor.name,
            "Hospital": c.doctor.hospital,
            "Procedure": c.procedure.type
        })

    df = pd.DataFrame(data)

    st.dataframe(df)

import streamlit as st
from datetime import date
import pandas as pd
from database import *
from auth import require_login

# INIT
init_db()
db = SessionLocal()

st.set_page_config(page_title="Ortho Tracker Pro", layout="wide")

require_login()

st.title(f"🏥 Ortho Tracker Pro | Welcome {st.session_state['user']}")

menu = st.sidebar.selectbox("Menu", [
    "Dashboard",
    "Add Data",
    "Record Case",
    "Log Visit",
    "Analytics"
])

# ================= DASHBOARD =================
if menu == "Dashboard":
    st.subheader("📊 Overview")

    cases = db.query(Case).all()

    data = [{
        "Date": c.date,
        "Rep": c.rep.name,
        "Doctor": c.doctor.name,
        "Hospital": c.doctor.hospital,
        "Procedure": c.procedure.type,
        "Revenue": c.revenue
    } for c in cases]

    df = pd.DataFrame(data)

    if not df.empty:
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Cases", len(df))
        col2.metric("Revenue", f"KES {df['Revenue'].sum():,.0f}")
        col3.metric("Doctors", df["Doctor"].nunique())
        col4.metric("Reps", df["Rep"].nunique())

        st.bar_chart(df["Procedure"].value_counts())
        st.line_chart(df.groupby("Date")["Revenue"].sum())

    else:
        st.info("No data yet")

# ================= ADD DATA =================
elif menu == "Add Data":
    tab1, tab2, tab3 = st.tabs(["Rep", "Doctor", "Procedure"])

    with tab1:
        name = st.text_input("Rep Name")
        if st.button("Save Rep"):
            db.add(Rep(name=name))
            db.commit()
            st.success("Saved")

    with tab2:
        name = st.text_input("Doctor Name")
        hospital = st.text_input("Hospital")
        specialty = st.text_input("Specialty")

        if st.button("Save Doctor"):
            db.add(Doctor(name=name, hospital=hospital, specialty=specialty))
            db.commit()
            st.success("Saved")

    with tab3:
        ptype = st.selectbox("Procedure", ["THR", "TKR", "Trauma", "Spine"])
        if st.button("Save Procedure"):
            db.add(Procedure(type=ptype))
            db.commit()
            st.success("Saved")

# ================= RECORD CASE =================
elif menu == "Record Case":
    st.subheader("🏥 Record Surgery")

    reps = db.query(Rep).all()
    doctors = db.query(Doctor).all()
    procedures = db.query(Procedure).all()

    rep = st.selectbox("Rep", reps, format_func=lambda x: x.name)
    doctor = st.selectbox("Doctor", doctors, format_func=lambda x: x.name)
    procedure = st.selectbox("Procedure", procedures, format_func=lambda x: x.type)
    revenue = st.number_input("Revenue (KES)")
    case_date = st.date_input("Date", date.today())

    if st.button("Save Case"):
        db.add(Case(
            rep_id=rep.id,
            doctor_id=doctor.id,
            procedure_id=procedure.id,
            revenue=revenue,
            date=case_date
        ))
        db.commit()
        st.success("Case recorded")

# ================= VISITS =================
elif menu == "Log Visit":
    st.subheader("📍 Doctor Visit")

    reps = db.query(Rep).all()
    doctors = db.query(Doctor).all()

    rep = st.selectbox("Rep", reps, format_func=lambda x: x.name)
    doctor = st.selectbox("Doctor", doctors, format_func=lambda x: x.name)
    notes = st.text_area("Visit Notes")
    visit_date = st.date_input("Date", date.today())

    if st.button("Save Visit"):
        db.add(Visit(
            rep_id=rep.id,
            doctor_id=doctor.id,
            notes=notes,
            date=visit_date
        ))
        db.commit()
        st.success("Visit logged")

# ================= ANALYTICS =================
elif menu == "Analytics":
    st.subheader("📊 Advanced Insights")

    cases = db.query(Case).all()

    data = [{
        "Date": c.date,
        "Rep": c.rep.name,
        "Doctor": c.doctor.name,
        "Procedure": c.procedure.type,
        "Revenue": c.revenue
    } for c in cases]

    df = pd.DataFrame(data)

    if not df.empty:
        st.write("### Revenue by Doctor")
        st.bar_chart(df.groupby("Doctor")["Revenue"].sum())

        st.write("### Revenue by Rep")
        st.bar_chart(df.groupby("Rep")["Revenue"].sum())

        st.write("### Procedure Trends")
        st.line_chart(df.groupby("Date")["Procedure"].count())

    else:
        st.info("No analytics yet")

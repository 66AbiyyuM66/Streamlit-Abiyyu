import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Customer Analytics Dashboard")

abyy = pd.read_csv("customers.csv")

st.sidebar.header("Filter Data")
departments = st.sidebar.multiselect(
    "Pilih Departments",
    abyy["Department"].dropna().unique()
)

genders = st.sidebar.multiselect(
    "Pilih Gender",
    abyy["Gender"].dropna().unique()
)

st.sidebar.header("Filter Rentang Umur")
min_usia, max_usia = int(abyy["Age"].min()), int(abyy["Age"].max())
usia_range = st.sidebar.slider(
    "Usia",
    min_value=min_usia,
    max_value=max_usia,
    value=(min_usia, max_usia)
)

abyy_filtered = abyy[
    (abyy["Department"].isin(departments)) &
    (abyy["Gender"].isin(genders)) &
    (abyy["Age"].between(usia_range[0], usia_range[1]))
]

st.subheader("Data Tabel")

st.dataframe(abyy_filtered)

st.subheader("Visualisasi Statistik")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribusi Gender")
    pie_gender = px.pie(
        abyy_filtered,
        names="Gender",
        color="Gender",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(pie_gender)

with col2:
    st.subheader("Gaji Rata-rata per Department")

    salary_dept = (
        abyy_filtered
        .groupby("Department")["AnnualSalary"]
        .mean()
        .reset_index()
    )

    bar_salary = px.bar(
        salary_dept,
        x="Department",
        y="AnnualSalary",
        color="Department",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(bar_salary) 


st.subheader("Rata-rata Gaji Berdasarkan Usia")

salary_age = (
    abyy_filtered
    .groupby("Age")["AnnualSalary"]
    .mean()
    .reset_index()
    .sort_values("Age")
)

line_age = px.line(
    salary_age,
    x="Age",
    y="AnnualSalary",
    markers=True
)

st.plotly_chart(line_age)   
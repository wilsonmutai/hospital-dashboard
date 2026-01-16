import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="HOSPITAL ANALYTICS DASHBOARD", layout="wide")

st.title("🏥HOSPITAL OPERATIONS & CLAIMS ANALYTICS DASHBOARD")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("hospital_data.csv")
    df["CLAIM_DATE"] = pd.to_datetime(df["CLAIM_DATE"], errors="coerce", dayfirst=True)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")

hospital = st.sidebar.multiselect(
    "Select Hospital(s)",
    df["HOSP_NAME"].unique(),
    default=df["HOSP_NAME"].unique()[:5]
)

category = st.sidebar.multiselect(
    "Select Treatment Category",
    df["CATEGORY_NAME"].unique(),
    default=df["CATEGORY_NAME"].unique()
)

# Apply filters
filtered_df = df[
    (df["HOSP_NAME"].isin(hospital)) &
    (df["CATEGORY_NAME"].isin(category))
]

# KPIs
st.subheader("Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric("Total Patients", filtered_df.shape[0])
col2.metric("Total Claim Amount", f"{filtered_df['CLAIM_AMOUNT'].sum():,.0f}")
col3.metric("Average Claim Amount", f"{filtered_df['CLAIM_AMOUNT'].mean():,.0f}")

# Claims by category
st.subheader("Claims by Treatment Category")

fig1, ax1 = plt.subplots()
filtered_df.groupby("CATEGORY_NAME")["CLAIM_AMOUNT"].sum().sort_values().plot(
    kind="barh", ax=ax1
)
ax1.set_xlabel("Total Claim Amount")
st.pyplot(fig1)

# Hospital workload
st.subheader("Patient Load by Hospital")

fig2, ax2 = plt.subplots()
filtered_df["HOSP_NAME"].value_counts().plot(
    kind="bar", ax=ax2
)
ax2.set_ylabel("Number of Patients")
st.pyplot(fig2)

# Mortality analysis
st.subheader("Patient Outcomes")

mortality_counts = filtered_df["Mortality Y / N"].value_counts()

fig3, ax3 = plt.subplots()
mortality_counts.plot(kind="pie", autopct="%1.1f%%", ax=ax3)
ax3.set_ylabel("")
st.pyplot(fig3)

# Data table
st.subheader("Filtered Dataset")
st.dataframe(filtered_df)



import streamlit as st
import pandas as pd
import altair as alt

# --- Load full dataset once ---
@st.cache_data
def load_data():
    return pd.read_csv("SGJobData_cleaned.csv.gz")

df = load_data()

# --- Sidebar control for sample size ---
sample_size = st.sidebar.slider(
    "Select sample size",
    min_value=100,
    max_value=500,   # safe cap to prevent crash
    step=100,
    value=200
)

# --- Apply random sampling ---
df_sample = df.sample(n=sample_size, random_state=42)

# --- Q1: Median Salary by Role/Level ---
st.header("Q1: Median Salary by Role/Level")
salary_summary = df_sample.groupby('positionLevels')['average_salary'].median().reset_index()

median_chart = alt.Chart(salary_summary).mark_bar().encode(
    x='positionLevels',
    y='average_salary'
)

st.altair_chart(median_chart, width="stretch")

# --- Q2: Applications vs Reposts ---
st.header("Q2: Applications vs Reposts")

apps_summary = df_sample.groupby('metadata_repostCount')['metadata_totalNumberJobApplication'].median().reset_index()

apps_chart = alt.Chart(apps_summary).mark_line(point=True).encode(
    x='metadata_repostCount',
    y='metadata_totalNumberJobApplication'
)

st.altair_chart(apps_chart, width="stretch")

# --- Q3: Industry Demand ---
st.header("Q3: Industry Demand")

# Automatically detect industry columns:
# They are the ones with "/" or spaces in their names, and not metadata/salary columns
industry_cols = [col for col in df_sample.columns 
                 if "/" in col or " " in col]

# Sum postings per industry
industry_counts = df_sample[industry_cols].sum().reset_index()
industry_counts.columns = ['Industry', 'Count']

# Sort and show top 10 industries
top_industries = industry_counts.sort_values(by='Count', ascending=False).head(10)

industry_chart = alt.Chart(top_industries).mark_bar().encode(
    x=alt.X('Industry', sort='-y'),
    y='Count'
)

st.altair_chart(industry_chart, width="stretch")
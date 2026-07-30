import streamlit as st
import pandas as pd
import altair as alt

# --- Load data once and cache it ---
@st.cache_data
def load_data():
    # Read the dataset from the db folder
    return pd.read_csv("db/SGJobData_cleaned.csv.gz")

df = load_data()

# --- Sidebar controls ---
st.sidebar.header("Filters")
# Dropdown to filter by industry
industry = st.sidebar.selectbox("Industry", df["industry_primary"].unique())
# Dropdown to filter by year
year = st.sidebar.selectbox("Year", sorted(df["posting_year"].unique()))
# Toggle for agency vs direct employer
agency_filter = st.sidebar.selectbox("Agency vs Direct", ["All","Agency","Direct"])
# Radio buttons to choose which business question (Q1–Q6) to answer
chart_choice = st.sidebar.radio(
    "Choose question",
    ["Q1 Salary Benchmark","Q2 Hard-to-Fill Roles","Q3 Demand","Q4 Selective Hiring","Q5 Posting Trends","Q6 Agency Filter"]
)

# --- Apply filters to dataset ---
filtered_df = df[(df["industry_primary"] == industry) & (df["posting_year"] == year)]
if agency_filter == "Agency":
    filtered_df = filtered_df[filtered_df['metadata_isPostedOnBehalf']==True]
elif agency_filter == "Direct":
    filtered_df = filtered_df[filtered_df['metadata_isPostedOnBehalf']==False]

# --- KPI cards (quick stats) ---
st.header("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Vacancies", int(filtered_df["numberOfVacancies"].sum()))   # total vacancies
col2.metric("Median Salary", int(filtered_df["salary_median"].median())) # median salary
col3.metric("Apps per Vacancy", round(filtered_df["applications_per_vacancy"].mean(), 2)) # avg applications per vacancy
col4.metric("Avg Repost Count", round(filtered_df["metadata_repostCount"].mean(), 2)) # avg repost count

# --- Charts by Question ---
if chart_choice == "Q1 Salary Benchmark":
    # Group by position level and calculate median salary
    salary_data = filtered_df.groupby("positionLevels")["average_salary"].median().reset_index()
    chart = alt.Chart(salary_data).mark_bar().encode(
            x=alt.X("positionLevels", axis=alt.Axis(title="Position Level")),
            y=alt.Y("average_salary", axis=alt.Axis(title="Median Salary (SGD)"))
    ).properties(width=700).interactive()
    st.subheader("Median Salary by Position Level")
    st.altair_chart(chart)

elif chart_choice == "Q2 Hard-to-Fill Roles":
    # Scatter plot: X = repost count, Y = applications per vacancy
    scatter_data = filtered_df[['metadata_repostCount','metadata_totalNumberJobApplication','numberOfVacancies']].dropna()
    scatter_data['apps_per_vacancy'] = scatter_data['metadata_totalNumberJobApplication'] / scatter_data['numberOfVacancies']
    chart = alt.Chart(scatter_data).mark_circle(size=60).encode(
         x=alt.X("metadata_repostCount", axis=alt.Axis(title="Repost Count")),
        y=alt.Y("apps_per_vacancy", axis=alt.Axis(title="Applications per Vacancy")),
        tooltip=['metadata_repostCount','apps_per_vacancy']
    ).properties(width=700).interactive()
    st.subheader("Hard-to-Fill Roles (bottom-right quadrant)")
    st.altair_chart(chart)

elif chart_choice == "Q3 Demand":
    # Top 10 industries by vacancies
    industry_data = df.groupby("industry_primary")["numberOfVacancies"].sum().reset_index().nlargest(10,"numberOfVacancies")
    chart = alt.Chart(industry_data).mark_bar().encode(
        x=alt.X("numberOfVacancies", axis=alt.Axis(title="Number of Vacancies")),
        y=alt.Y("industry_primary", sort="-x", axis=alt.Axis(title="Industry"))
    ).properties(width=700).interactive()
    st.subheader("Top 10 Industries by Vacancies")
    st.altair_chart(chart)

elif chart_choice == "Q4 Selective Hiring":
    # Scatter plot again, but highlight top-left quadrant (low repost, high applications)
    scatter_data = filtered_df[['metadata_repostCount','metadata_totalNumberJobApplication','numberOfVacancies']].dropna()
    scatter_data['apps_per_vacancy'] = scatter_data['metadata_totalNumberJobApplication'] / scatter_data['numberOfVacancies']
    chart = alt.Chart(scatter_data).mark_circle(size=60, color="green").encode(
         x=alt.X("metadata_repostCount", axis=alt.Axis(title="Repost Count")),
    y=alt.Y("apps_per_vacancy", axis=alt.Axis(title="Applications per Vacancy")),
        tooltip=['metadata_repostCount','apps_per_vacancy']
    ).properties(width=700).interactive()
    st.subheader("Selective Hiring (top-left quadrant)")
    st.altair_chart(chart)

elif chart_choice == "Q5 Posting Trends":
    # Line chart: postings count + average applications over time
    trend_data = df.groupby("posting_month_year").agg(
        postings=('posting_month_year','count'),
        avg_apps=('applications_per_vacancy','mean')
    ).reset_index()

    line1 = alt.Chart(trend_data).mark_line(color="blue").encode(
        x=alt.X("posting_month_year", axis=alt.Axis(title="Month-Year")),
        y=alt.Y("postings", axis=alt.Axis(title="Number of Postings"))
    )
    line2 = alt.Chart(trend_data).mark_line(color="orange").encode(
        x=alt.X("posting_month_year", axis=alt.Axis(title="Month-Year")),
        y=alt.Y("avg_apps", axis=alt.Axis(title="Average Applications per Vacancy"))
    )
    chart = (line1 + line2).properties(width=700).interactive()
    st.subheader("Job Postings & Avg Applications Over Time")
    st.altair_chart(chart)

elif chart_choice == "Q6 Agency Filter":
    # Prepare data for Q6
    agency_data = df.groupby("metadata_isPostedOnBehalf")["numberOfVacancies"].sum().reset_index()

    # Map True/False to readable labels
    agency_data["metadata_isPostedOnBehalf"] = agency_data["metadata_isPostedOnBehalf"].map({
        True: "Agency",
        False: "Direct Employer"
    })

    # Optional: add percentage share
    total_vacancies = agency_data["numberOfVacancies"].sum()
    agency_data["percentage"] = (agency_data["numberOfVacancies"] / total_vacancies * 100).round(1)

    # Chart
    chart = alt.Chart(agency_data).mark_bar().encode(
        x=alt.X("metadata_isPostedOnBehalf", axis=alt.Axis(title="Posting Type")),
        y=alt.Y("numberOfVacancies", axis=alt.Axis(title="Number of Vacancies")),
        tooltip=["metadata_isPostedOnBehalf","numberOfVacancies","percentage"]
    ).properties(width=700).interactive()

    st.subheader("Vacancies: Agency vs Direct Employer")
    st.altair_chart(chart)

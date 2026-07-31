import streamlit as st
import pandas as pd
import altair as alt

# --- Load data once and cache it ---
@st.cache_data
def load_data():
    # Load the cleaned job dataset
    return pd.read_csv("db/SGJobData_cleaned.csv.gz")

df = load_data()

# --- Pre-aggregate global data once (cached) ---
@st.cache_data
def global_aggregates(df):
    # Aggregate vacancies by industry, role, and position level
    industry_data = df.groupby("industry_primary")["numberOfVacancies"].sum().reset_index()
    role_data = df.groupby("title")["numberOfVacancies"].sum().reset_index()
    pos_data = df.groupby("positionLevels")["numberOfVacancies"].sum().reset_index()
    return industry_data, role_data, pos_data

global_industry, global_roles, global_pos = global_aggregates(df)

# --- Sidebar controls ---
st.sidebar.header("Filters")

industry = st.sidebar.selectbox("Industry", df["industry_primary"].unique())
year = st.sidebar.selectbox("Year", sorted(df["posting_year"].unique()))
agency_filter = st.sidebar.selectbox("Agency vs Direct", ["All","Agency","Direct"])
role = st.sidebar.text_input("Search for Role")

chart_choice = st.sidebar.radio(
    "Choose question",
    ["Q1 Salary Benchmark","Q2 Hard-to-Fill Roles","Q3 Demand",
     "Q4 Selective Hiring","Q5 Posting Trends","Q6 Agency Filter"]
)

# --- Apply filters to dataset ---
filtered_df = df[(df["industry_primary"] == industry) & (df["posting_year"] == year)]
if agency_filter == "Agency":
    filtered_df = filtered_df[filtered_df['metadata_isPostedOnBehalf']==True]
elif agency_filter == "Direct":
    filtered_df = filtered_df[filtered_df['metadata_isPostedOnBehalf']==False]

# --- KPI cards ---
st.header("Key Performance Indicators for Filtered View")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Vacancies", int(filtered_df["numberOfVacancies"].sum()))   # total vacancies
col2.metric("Median Salary", int(filtered_df["salary_median"].median())) # median salary
col3.metric("Apps per Vacancy", round(filtered_df["applications_per_vacancy"].mean(), 2)) # avg applications
col4.metric("Avg Repost Count", round(filtered_df["metadata_repostCount"].mean(), 2))    # avg reposts

# --- Q1 Salary Benchmark ---
if chart_choice == "Q1 Salary Benchmark":
    salary_data = filtered_df.groupby("positionLevels")["average_salary"].median().reset_index()
    chart = alt.Chart(salary_data).mark_bar().encode(
        x=alt.X("positionLevels", axis=alt.Axis(title="Position Level", labelAngle=-45)),
        y=alt.Y("average_salary", axis=alt.Axis(title="Median Salary (SGD)"))
    ).properties(width=700).interactive()
    st.subheader("Median Salary by Position Level")
    st.altair_chart(chart)

    chart = alt.Chart(filtered_df).mark_boxplot().encode(
        x=alt.X("positionLevels", axis=alt.Axis(title="Position Level", labelAngle=-45)),
        y=alt.Y("average_salary", axis=alt.Axis(title="Salary (SGD)"))
    ).properties(width=700).interactive()
    st.subheader("Salary Distribution by Position Level")
    st.altair_chart(chart)

    if role:
        role_data = filtered_df[filtered_df["title"].str.contains(role, case=False, na=False)]
        st.write(f"Found {len(role_data)} jobs for {role}")
        st.write(role_data["average_salary"].describe())

# --- Q2 Hard-to-Fill Roles (aggregated by industry) ---
elif chart_choice == "Q2 Hard-to-Fill Roles":
    scatter_data = df.groupby("industry_primary").agg({
        "metadata_repostCount":"sum",
        "applications_per_vacancy":"mean"
    }).reset_index()

    hard_to_fill = scatter_data.sort_values(
        ["metadata_repostCount","applications_per_vacancy"],
        ascending=[False, True]
    ).head(10)

    st.subheader("Top 10 Hard-to-Fill Industries")
    st.dataframe(hard_to_fill[["industry_primary","metadata_repostCount","applications_per_vacancy"]])

    q2_chart = alt.Chart(scatter_data).mark_circle(size=80).encode(
        x=alt.X("metadata_repostCount", title="Total Reposts"),
        y=alt.Y("applications_per_vacancy", title="Average Applications per Vacancy"),
        tooltip=["industry_primary","metadata_repostCount","applications_per_vacancy"]
    ).properties(title="Q2: Hard-to-Fill Roles (Aggregated by Industry)", width=700).interactive()
    st.altair_chart(q2_chart)

## --- Q3 Demand ---
elif chart_choice == "Q3 Demand":
    tab1, tab2 = st.tabs(["Filtered View", "Global View"])

    # --- Filtered View (Top 20 roles) ---
    with tab1:
        demand_filtered = (
            filtered_df.groupby("title")["numberOfVacancies"].sum()
            .reset_index()
            .sort_values("numberOfVacancies", ascending=False)  # sort high → low
            .head(20)
        )

        chart = alt.Chart(demand_filtered).mark_bar().encode(
            x=alt.X("title", sort="-y", axis=alt.Axis(title="Role", labelAngle=-45)),  # enforce sort
            y=alt.Y("numberOfVacancies", axis=alt.Axis(title="Vacancies")),
            tooltip=["title","numberOfVacancies"]
        ).properties(width=700).interactive()

        st.subheader("Top 20 Roles by Demand (Filtered View)")
        st.altair_chart(chart)
        st.dataframe(demand_filtered)

    # --- Global View (Top 20 roles) ---
    with tab2:
        demand_global = (
            df.groupby("title")["numberOfVacancies"].sum()
            .reset_index()
            .sort_values("numberOfVacancies", ascending=False)  # sort high → low
            .head(20)
        )

        chart = alt.Chart(demand_global).mark_bar().encode(
            x=alt.X("title", sort="-y", axis=alt.Axis(title="Role", labelAngle=-45)),  # enforce sort
            y=alt.Y("numberOfVacancies", axis=alt.Axis(title="Vacancies")),
            tooltip=["title","numberOfVacancies"]
        ).properties(width=700).interactive()

        st.subheader("Top 20 Roles by Demand (Global View)")
        st.altair_chart(chart)
        st.dataframe(demand_global)



# --- Q4 Selective Hiring (aggregated by industry) ---
elif chart_choice == "Q4 Selective Hiring":
    scatter_data = df.groupby("industry_primary").agg({
        "metadata_repostCount":"sum",
        "applications_per_vacancy":"mean"
    }).reset_index()

    selective_hiring = scatter_data.sort_values(
        ["metadata_repostCount","applications_per_vacancy"],
        ascending=[True, False]
    ).head(10)

    st.subheader("Top 10 Selective Hiring Industries")
    st.dataframe(selective_hiring[["industry_primary","metadata_repostCount","applications_per_vacancy"]])

    q4_chart = alt.Chart(scatter_data).mark_circle(size=80).encode(
        x=alt.X("metadata_repostCount", title="Total Reposts"),
        y=alt.Y("applications_per_vacancy", title="Average Applications per Vacancy"),
        tooltip=["industry_primary","metadata_repostCount","applications_per_vacancy"]
    ).properties(title="Q4: Selective Hiring (Aggregated by Industry)", width=700).interactive()
    st.altair_chart(q4_chart)




# --- Q5 Posting Trends (Filtered vs Global Tabs) ---
elif chart_choice == "Q5 Posting Trends":
    tab1, tab2 = st.tabs(["Filtered View", "Global View"])

    # --- Filtered View ---
    with tab1:
        trend_data = filtered_df.groupby("posting_month_year").agg(
            postings=('posting_month_year','count'),
            avg_apps=('applications_per_vacancy','mean')
        ).reset_index()

        # Melt into long format for legend
        trend_long = trend_data.melt(
            id_vars=["posting_month_year"],
            value_vars=["postings","avg_apps"],
            var_name="Metric",
            value_name="Value"
        )

        chart = alt.Chart(trend_long).mark_line().encode(
            x=alt.X("posting_month_year", axis=alt.Axis(title="Month-Year", labelAngle=-45)),
            y=alt.Y("Value", axis=alt.Axis(title="Count / Avg Apps")),
            color=alt.Color("Metric", title="Legend")  # adds legend
        ).properties(width=700).interactive()

        st.subheader("Job Postings & Avg Applications Over Time (Filtered)")
        st.altair_chart(chart)

    # --- Global View ---
    with tab2:
        trend_data = df.groupby("posting_month_year").agg(
            postings=('posting_month_year','count'),
            avg_apps=('applications_per_vacancy','mean')
        ).reset_index()

        trend_long = trend_data.melt(
            id_vars=["posting_month_year"],
            value_vars=["postings","avg_apps"],
            var_name="Metric",
            value_name="Value"
        )

        chart = alt.Chart(trend_long).mark_line().encode(
            x=alt.X("posting_month_year", axis=alt.Axis(title="Month-Year", labelAngle=-45)),
            y=alt.Y("Value", axis=alt.Axis(title="Count / Avg Apps")),
            color=alt.Color("Metric", title="Legend")  # adds legend
        ).properties(width=700).interactive()

        st.subheader("Job Postings & Avg Applications Over Time (Global)")
        st.altair_chart(chart)


# --- Q6 Agency Filter (Filtered vs Global Tabs) ---
elif chart_choice == "Q6 Agency Filter":
    tab1, tab2 = st.tabs(["Filtered View", "Global View"])

    with tab1:
        agency_data = filtered_df.groupby("metadata_isPostedOnBehalf")["numberOfVacancies"].sum().reset_index()
        agency_data["metadata_isPostedOnBehalf"] = agency_data["metadata_isPostedOnBehalf"].map({True:"Agency",False:"Direct Employer"})
        total_vacancies = agency_data["numberOfVacancies"].sum()
        agency_data["percentage"] = (agency_data["numberOfVacancies"]/total_vacancies*100).round(1)

        chart = alt.Chart(agency_data).mark_bar().encode(
            x=alt.X("metadata_isPostedOnBehalf", axis=alt.Axis(title="Posting Type")),
            y=alt.Y("numberOfVacancies", axis=alt.Axis(title="Vacancies")),
            tooltip=["metadata_isPostedOnBehalf","numberOfVacancies","percentage"]
        ).properties(width=700).interactive()
        st.subheader("Vacancies by Posting Type (Filtered)")
        st.altair_chart(chart)

    with tab2:
        agency_data = df.groupby("metadata_isPostedOnBehalf")["numberOfVacancies"].sum().reset_index()
        agency_data["metadata_isPostedOnBehalf"] = agency_data["metadata_isPostedOnBehalf"].map({True:"Agency",False:"Direct Employer"})
        total_vacancies = agency_data["numberOfVacancies"].sum()
        agency_data["percentage"] = (agency_data["numberOfVacancies"]/total_vacancies*100).round(1)

        chart = alt.Chart(agency_data).mark_bar().encode(
            x=alt.X("metadata_isPostedOnBehalf", axis=alt.Axis(title="Posting Type")),
            y=alt.Y("numberOfVacancies", axis=alt.Axis(title="Vacancies")),
            tooltip=["metadata_isPostedOnBehalf","numberOfVacancies","percentage"]
        ).properties(width=700).interactive()
        st.subheader("Vacancies by Posting Type (Global)")
        st.altair_chart(chart)

    #streamlit run dashboard.py (run in terminal to start the dashboard)

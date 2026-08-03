# --- Setup ---
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
year_options = ["All"] + sorted(df["posting_year"].unique())
year = st.sidebar.selectbox("Year", year_options)
agency_filter = st.sidebar.selectbox("Agency vs Direct", ["All","Agency","Direct"])
role = st.sidebar.text_input("Search for Role")

chart_choice = st.sidebar.radio(
    "Choose question",
    ["Q1 Salary Benchmark","Q2 Hard-to-Fill Roles","Q3 Demand",
     "Q4 Selective Hiring","Q5 Posting Trends","Q6 Agency Filter"]
)

# --- Apply filters to dataset ---
filtered_df = df[df["industry_primary"] == industry]

if year != "All":
    filtered_df = filtered_df[filtered_df["posting_year"] == year]

if agency_filter == "Agency":
    filtered_df = filtered_df[filtered_df['metadata_isPostedOnBehalf'] == True]
elif agency_filter == "Direct":
    filtered_df = filtered_df[filtered_df['metadata_isPostedOnBehalf'] == False]

# --- KPI cards ---
st.header("Key Performance Indicators for Filtered View")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Vacancies", int(filtered_df["numberOfVacancies"].sum()))
col2.metric("Job Postings", int(filtered_df["numberOfVacancies"].count()))
col3.metric("Median Salary", int(filtered_df["salary_median"].median()))
col4.metric("Apps per Vacancy", round(filtered_df["applications_per_vacancy"].mean(), 2))
col5.metric("Avg Repost Count", round(filtered_df["metadata_repostCount"].mean(), 2))


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

# --- Q2 Hard-to-Fill Roles by Industry (Chart View) ---
elif chart_choice == "Q2 Hard-to-Fill Roles":
    # Step 1: Filter jobs with activity data
    df_valid = df[
        (df['metadata_totalNumberJobApplication'] > 0) | 
        (df['metadata_repostCount'] > 0) |
        (df['applications_per_vacancy'] > 0)
    ].copy()

    # Step 2: Calculate median thresholds
    median_reposts = df_valid['metadata_repostCount'].median()
    median_apps_per_vac = df_valid['applications_per_vacancy'].median()

    # Step 3: Define hard-to-fill condition
    df_valid['is_hard_to_fill'] = (
        (df_valid['metadata_repostCount'] >= median_reposts) &
        (df_valid['applications_per_vacancy'] <= median_apps_per_vac)
    )

    # Step 4: Aggregate by industry
    industry_htf = df_valid.groupby("industry_primary").agg(
        Total_Jobs=("is_hard_to_fill", "count"),
        Hard_to_Fill_Count=("is_hard_to_fill", "sum"),
        Pct_Hard_to_Fill=("is_hard_to_fill", "mean")
    ).reset_index()

    # Convert fraction to percentage
    industry_htf["Pct_Hard_to_Fill"] = industry_htf["Pct_Hard_to_Fill"] * 100

    # Minimum sample size filter
    industry_htf = industry_htf[industry_htf["Total_Jobs"] >= 50]

    # Sort descending and take Top 10
    industry_htf = industry_htf.sort_values(by="Pct_Hard_to_Fill", ascending=False).head(10)

    # Step 5: Show chart instead of table
    st.subheader("Top 10 Industries with Highest % Hard to Fill (Chart View)")
    q2_chart = alt.Chart(industry_htf).mark_bar().encode(
        x=alt.X("Pct_Hard_to_Fill", title="% Hard to Fill"),
        y=alt.Y("industry_primary", sort="-x", title="Industry"),
        tooltip=["industry_primary","Total_Jobs","Hard_to_Fill_Count","Pct_Hard_to_Fill"]
    ).properties(width=700, height=400)

    st.altair_chart(q2_chart)

    # --- Aggregated scatter chart (industry-level) ---
    scatter_data = df.groupby("industry_primary").agg(
        avg_reposts=("metadata_repostCount","mean"),
        avg_apps=("applications_per_vacancy","mean")
    ).reset_index()

    q2_chart = alt.Chart(scatter_data).mark_circle(size=80).encode(
        x=alt.X("avg_reposts", title="Average Reposts"),
        y=alt.Y("avg_apps", title="Average Applications per Vacancy"),
        tooltip=["industry_primary","avg_reposts","avg_apps"]
    ).properties(title="Q2: Hard-to-Fill Roles (Industry Aggregates)", width=700).interactive()

    st.altair_chart(q2_chart)

# --- Q3 Demand ---
elif chart_choice == "Q3 Demand":
    tab1, tab2 = st.tabs(["Filtered View", "Global View"])

    # --- Filtered View (Top 20 roles) ---
    with tab1:
        demand_filtered = (
            filtered_df.groupby("title")["numberOfVacancies"].sum()
            .reset_index()
            .sort_values("numberOfVacancies", ascending=False)
            .head(20)
        )
        chart = alt.Chart(demand_filtered).mark_bar().encode(
            x=alt.X("title", sort="-y", axis=alt.Axis(title="Role", labelAngle=-45)),
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
            .sort_values("numberOfVacancies", ascending=False)
            .head(20)
        )
        chart = alt.Chart(demand_global).mark_bar().encode(
            x=alt.X("title", sort="-y", axis=alt.Axis(title="Role", labelAngle=-45)),
            y=alt.Y("numberOfVacancies", axis=alt.Axis(title="Vacancies")),
            tooltip=["title","numberOfVacancies"]
        ).properties(width=700).interactive()
        st.subheader("Top 20 Roles by Demand (Global View)")
        st.altair_chart(chart)
        st.dataframe(demand_global)


# --- Q4 Selective Hire by Industry ---
elif chart_choice == "Q4 Selective Hire":
    # Step 1: Create df_valid (same as EDA)
    df_valid = df[
        (df['metadata_totalNumberJobApplication'] > 0) | 
        (df['metadata_repostCount'] > 0) |
        (df['applications_per_vacancy'] > 0)
    ].copy()

    # Step 2: Calculate thresholds (25th and 75th percentiles)
    low_reposts_threshold = df_valid['metadata_repostCount'].quantile(0.25)
    high_apps_threshold = df_valid['applications_per_vacancy'].quantile(0.75)

    # Step 3: Define selective hire condition
    df_valid['is_selective_hire'] = (
        (df_valid['metadata_repostCount'] <= low_reposts_threshold) &
        (df_valid['applications_per_vacancy'] >= high_apps_threshold)
    )

    # --- Q4 Selective Hire by Industry ---
elif chart_choice == "Q4 Selective Hire":
    # Step 1: Create df_valid (same as EDA)
    df_valid = df[
        (df['metadata_totalNumberJobApplication'] > 0) | 
        (df['metadata_repostCount'] > 0) |
        (df['applications_per_vacancy'] > 0)
    ].copy()

    # Step 2: Calculate thresholds (25th and 75th percentiles)
    low_reposts_threshold = df_valid['metadata_repostCount'].quantile(0.25)
    high_apps_threshold = df_valid['applications_per_vacancy'].quantile(0.75)

    # Step 3: Define selective hire condition
    df_valid['is_selective_hire'] = (
        (df_valid['metadata_repostCount'] <= low_reposts_threshold) &
        (df_valid['applications_per_vacancy'] >= high_apps_threshold)
    )

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


elif chart_choice == "Q5 Posting Trends":
    tab1, tab2 = st.tabs(["Filtered View", "Global View"])
    
    def create_separate_charts(data, title_prefix):
        """Create separate bar and line charts side by side"""
        
        trend_data = data.groupby("posting_month_year").agg(
            postings=('posting_month_year','count'),
            avg_apps=('applications_per_vacancy','mean')
        ).reset_index()
        
        # Bar chart for postings
        bar_chart = alt.Chart(trend_data).mark_bar(color='#1f77b4', opacity=0.7).encode(
            x=alt.X("posting_month_year", 
                    axis=alt.Axis(title="Month-Year", labelAngle=-45),
                    sort=None),
            y=alt.Y("postings", axis=alt.Axis(title="Number of Postings"))
        ).properties(
            width=340,
            height=350,
            title=f"{title_prefix} - Postings"
        ).interactive()
        
        # Line chart for avg apps
        line_chart = alt.Chart(trend_data).mark_line(color='#ff7f0e', strokeWidth=3).encode(
            x=alt.X("posting_month_year", 
                    axis=alt.Axis(title="Month-Year", labelAngle=-45),
                    sort=None),
            y=alt.Y("avg_apps", axis=alt.Axis(title="Avg Applications"))
        ).properties(
            width=340,
            height=350,
            title=f"{title_prefix} - Avg Applications"
        ).interactive()
        
        # Add points to line chart
        line_chart_with_points = line_chart + alt.Chart(trend_data).mark_circle(
            color='#ff7f0e', 
            size=60
        ).encode(
            x="posting_month_year",
            y="avg_apps"
        )
        
        return bar_chart, line_chart_with_points
    
    # --- Filtered View ---
    with tab1:
        st.subheader("Filtered View")
        bar, line = create_separate_charts(filtered_df, "Filtered")
        col1, col2 = st.columns(2)
        with col1:
            st.altair_chart(bar)
        with col2:
            st.altair_chart(line)
    
    # --- Global View ---
    with tab2:
        st.subheader("Global View")
        bar, line = create_separate_charts(df, "Global")
        col1, col2 = st.columns(2)
        with col1:
            st.altair_chart(bar)
        with col2:
            st.altair_chart(line)

# --- Q6 Agency Filter (Filtered vs Global Tabs) ---
elif chart_choice == "Q6 Agency Filter":
    tab1, tab2 = st.tabs(["Filtered View", "Global View"])

    # --- Filtered View (Using Postings) ---
    with tab1:
        # Count postings (number of job ads) instead of vacancies
        agency_data = filtered_df.groupby("metadata_isPostedOnBehalf")["title"].count().reset_index()
        agency_data.columns = ["metadata_isPostedOnBehalf", "postings"]
        agency_data["metadata_isPostedOnBehalf"] = agency_data["metadata_isPostedOnBehalf"].map({True: "Agency", False: "Direct Employer"})
        total_postings = agency_data["postings"].sum()
        agency_data["percentage"] = (agency_data["postings"] / total_postings * 100).round(1)
        
        chart = alt.Chart(agency_data).mark_bar().encode(
            x=alt.X("metadata_isPostedOnBehalf", axis=alt.Axis(title="Posting Type")),
            y=alt.Y("postings", axis=alt.Axis(title="Number of Postings")),
            tooltip=["metadata_isPostedOnBehalf", "postings", "percentage"]
        ).properties(width=700).interactive()
        
        st.subheader("Postings by Posting Type (Filtered)")
        st.altair_chart(chart)
        st.dataframe(agency_data)

    # --- Global View (Using Postings) ---
    with tab2:
        # Count postings (number of job ads) instead of vacancies
        agency_data = df.groupby("metadata_isPostedOnBehalf")["title"].count().reset_index()
        agency_data.columns = ["metadata_isPostedOnBehalf", "postings"]
        agency_data["metadata_isPostedOnBehalf"] = agency_data["metadata_isPostedOnBehalf"].map({True: "Agency", False: "Direct Employer"})
        total_postings = agency_data["postings"].sum()
        agency_data["percentage"] = (agency_data["postings"] / total_postings * 100).round(1)

        chart = alt.Chart(agency_data).mark_bar().encode(
            x=alt.X("metadata_isPostedOnBehalf", axis=alt.Axis(title="Posting Type")),
            y=alt.Y("postings", axis=alt.Axis(title="Number of Postings")),
            tooltip=["metadata_isPostedOnBehalf", "postings", "percentage"]
        ).properties(width=700).interactive()

        st.subheader("Postings by Posting Type (Global)")
        st.altair_chart(chart)
        st.dataframe(agency_data)
    #streamlit run dashboard.py (run in terminal to start the dashboard)

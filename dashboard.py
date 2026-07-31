import streamlit as st
import pandas as pd
import altair as alt

# --- Load data once and cache it ---
@st.cache_data
def load_data():
    return pd.read_csv("db/SGJobData_cleaned.csv.gz")

df = load_data()

# --- Pre-aggregate global data once (cached) ---
@st.cache_data
def global_aggregates(df):
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
col1.metric("Vacancies", int(filtered_df["numberOfVacancies"].sum()))
col2.metric("Median Salary", int(filtered_df["salary_median"].median()))
col3.metric("Apps per Vacancy", round(filtered_df["applications_per_vacancy"].mean(), 2))
col4.metric("Avg Repost Count", round(filtered_df["metadata_repostCount"].mean(), 2))

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

# --- Q2 Hard-to-Fill Roles ---
elif chart_choice == "Q2 Hard-to-Fill Roles":
    scatter_data = filtered_df[['metadata_repostCount','metadata_totalNumberJobApplication','numberOfVacancies','title','industry_primary','positionLevels']].dropna()
    scatter_data['apps_per_vacancy'] = scatter_data['metadata_totalNumberJobApplication'] / scatter_data['numberOfVacancies']

    chart = alt.Chart(scatter_data).mark_circle(size=60).encode(
        x=alt.X("metadata_repostCount", axis=alt.Axis(title="Repost Count")),
        y=alt.Y("apps_per_vacancy", axis=alt.Axis(title="Applications per Vacancy")),
        tooltip=["title","industry_primary","positionLevels","metadata_repostCount","apps_per_vacancy"]
    ).properties(width=700).interactive()
    st.subheader("Hard-to-Fill Roles (bottom-right quadrant)")
    st.altair_chart(chart)

    hard_to_fill = scatter_data.sort_values(["metadata_repostCount","apps_per_vacancy"], ascending=[False, True]).head(10)
    st.subheader("Top 10 Hard-to-Fill Roles")
    st.dataframe(hard_to_fill[["title","industry_primary","positionLevels","metadata_repostCount","apps_per_vacancy"]])

# --- Q3 Demand (Filtered vs Global Tabs) ---
elif chart_choice == "Q3 Demand":
    tab1, tab2 = st.tabs(["Filtered View", "Global View"])

    with tab1:
        industry_data = filtered_df.groupby("industry_primary")["numberOfVacancies"].sum().reset_index().nlargest(10,"numberOfVacancies")
        chart = alt.Chart(industry_data).mark_bar().encode(
            x=alt.X("numberOfVacancies", axis=alt.Axis(title="Vacancies")),
            y=alt.Y("industry_primary", sort="-x", axis=alt.Axis(title="Industry"))
        ).properties(width=700).interactive()
        st.subheader("Top 10 Industries by Vacancies (Filtered)")
        st.altair_chart(chart)

        role_data = filtered_df.groupby("title")["numberOfVacancies"].sum().reset_index().nlargest(10,"numberOfVacancies")
        chart = alt.Chart(role_data).mark_bar().encode(
            x=alt.X("numberOfVacancies", axis=alt.Axis(title="Vacancies")),
            y=alt.Y("title", sort="-x", axis=alt.Axis(title="Role"))
        ).properties(width=700).interactive()
        st.subheader("Top 10 Roles by Vacancies (Filtered)")
        st.altair_chart(chart)

        pos_data = filtered_df.groupby("positionLevels")["numberOfVacancies"].sum().reset_index()
        chart = alt.Chart(pos_data).mark_bar().encode(
            x=alt.X("positionLevels", axis=alt.Axis(title="Position Level", labelAngle=-45)),
            y=alt.Y("numberOfVacancies", axis=alt.Axis(title="Vacancies"))
        ).properties(width=700).interactive()
        st.subheader("Vacancies by Position Level (Filtered)")
        st.altair_chart(chart)

    with tab2:
        chart = alt.Chart(global_industry.nlargest(10,"numberOfVacancies")).mark_bar().encode(
            x=alt.X("numberOfVacancies", axis=alt.Axis(title="Vacancies")),
            y=alt.Y("industry_primary", sort="-x", axis=alt.Axis(title="Industry"))
        ).properties(width=700).interactive()
        st.subheader("Top 10 Industries by Vacancies (Global)")
        st.altair_chart(chart)

        chart = alt.Chart(global_roles.nlargest(10,"numberOfVacancies")).mark_bar().encode(
            x=alt.X("numberOfVacancies", axis=alt.Axis(title="Vacancies")),
            y=alt.Y("title", sort="-x", axis=alt.Axis(title="Role"))
        ).properties(width=700).interactive()
        st.subheader("Top 10 Roles by Vacancies (Global)")
        st.altair_chart(chart)

        chart = alt.Chart(global_pos).mark_bar().encode(
            x=alt.X("positionLevels", axis=alt.Axis(title="Position Level", labelAngle=-45)),
            y=alt.Y("numberOfVacancies", axis=alt.Axis(title="Vacancies"))
        ).properties(width=700).interactive()
        st.subheader("Vacancies by Position Level (Global)")
        st.altair_chart(chart)

# --- Q4 Selective Hiring ---
elif chart_choice == "Q4 Selective Hiring":
    scatter_data = filtered_df[['metadata_repostCount','metadata_totalNumberJobApplication',
                                'numberOfVacancies','title','industry_primary','positionLevels']].dropna()
    scatter_data['apps_per_vacancy'] = scatter_data['metadata_totalNumberJobApplication'] / scatter_data['numberOfVacancies']

    chart = alt.Chart(scatter_data).mark_circle(size=60, color="green").encode(
        x=alt.X("metadata_repostCount", axis=alt.Axis(title="Repost Count")),
        y=alt.Y("apps_per_vacancy", axis=alt.Axis(title="Applications per Vacancy")),
        tooltip=["title","industry_primary","positionLevels","metadata_repostCount","apps_per_vacancy"]
    ).properties(width=700).interactive()
    st.subheader("Selective Hiring (top-left quadrant)")
    st.altair_chart(chart)   # ✅ correct function

    sh_position = filtered_df.groupby("positionLevels")["applications_per_vacancy"].mean().reset_index()
    chart = alt.Chart(sh_position).mark_bar().encode(
        x=alt.X("positionLevels", axis=alt.Axis(title="Position Level", labelAngle=-45)),
        y=alt.Y("applications_per_vacancy", axis=alt.Axis(title="Avg Apps per Vacancy"))
    ).properties(width=700).interactive()
    st.subheader("Selective Hire by Position Level")
    st.altair_chart(chart)  
    # Summary table of top 10 selective roles
    selective_roles = scatter_data.sort_values(
        ["apps_per_vacancy","metadata_repostCount"], ascending=[False, True]
    ).head(10)
    st.subheader("Top 10 Selective Hiring Roles")
    st.dataframe(selective_roles[["title","industry_primary","positionLevels","metadata_repostCount","apps_per_vacancy"]])

# --- Q5 Posting Trends (Filtered vs Global Tabs) ---
elif chart_choice == "Q5 Posting Trends":
    tab1, tab2 = st.tabs(["Filtered View", "Global View"])

    with tab1:
        trend_data = filtered_df.groupby("posting_month_year").agg(
            postings=('posting_month_year','count'),
            avg_apps=('applications_per_vacancy','mean')
        ).reset_index()

        line1 = alt.Chart(trend_data).mark_line(color="blue").encode(
            x=alt.X("posting_month_year", axis=alt.Axis(title="Month-Year", labelAngle=-45)),
            y=alt.Y("postings", axis=alt.Axis(title="Postings"))
        )
        line2 = alt.Chart(trend_data).mark_line(color="orange").encode(
            x=alt.X("posting_month_year", axis=alt.Axis(title="Month-Year", labelAngle=-45)),
            y=alt.Y("avg_apps", axis=alt.Axis(title="Avg Apps per Vacancy"))
        )
        chart = (line1 + line2).properties(width=700).interactive()
        st.subheader("Job Postings & Avg Applications Over Time (Filtered)")
        st.altair_chart(chart)

    with tab2:
        trend_data = df.groupby("posting_month_year").agg(
            postings=('posting_month_year','count'),
            avg_apps=('applications_per_vacancy','mean')
        ).reset_index()

        line1 = alt.Chart(trend_data).mark_line(color="blue").encode(
            x=alt.X("posting_month_year", axis=alt.Axis(title="Month-Year", labelAngle=-45)),
            y=alt.Y("postings", axis=alt.Axis(title="Postings"))
        )
        line2 = alt.Chart(trend_data).mark_line(color="orange").encode(
            x=alt.X("posting_month_year", axis=alt.Axis(title="Month-Year", labelAngle=-45)),
            y=alt.Y("avg_apps", axis=alt.Axis(title="Avg Apps per Vacancy"))
        )
        chart = (line1 + line2).properties(width=700).interactive()
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

    #streamlit run dashboard.py

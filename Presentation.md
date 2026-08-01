# Singapore Jobs Analytics - A Business Case for Talent Acquisition Market Intelligence Insights Dashboard

## Contents

1. Business Case
2. Data Handling & Process
3. Dashboard / app walkthrough
4. Challenges & Learning

## Team
| # | Member | GitHub | Primary Responsibility |
|---|---|---|---|
| 1 | Jenny Hwo | @jennyhwo85-lgtm | Repo setup, README (business case & scope), initial EDA on sample |
| 2 | Wong Lai Yoke | @laiyokew6996 | db/ folder setup & dataset handling (via PR) |
| 3 | Quxin | @quxin43 | Data cleaning (missing values, outliers) & conversion to .db/.sql |
| 4 | Wei Xiang (小翔) | @boyboi86 | Full EDA & feature engineering on cleaned data |
| 5 | Gerine Goh Sipei | @gerinegohsp | Streamlit dashboard & visualisation |

## Project Overview

### 1. Business Case

- **Business scenario:** A talent acquisition (TA) team at a mid-sized Singapore company planning its hiring strategy for the year ahead.

  **Why Plan Ahead?**

  Hiring is a lengthy process that involves budget approval, recruitment, interviews, and onboarding. Planning ahead allows companies to allocate resources and prepare for difficult-to-fill roles before hiring needs become urgent.

- **Problem statement:** The TA team needs better information to plan hiring. Without salary benchmarks and market insights, the company may offer unsuitable salaries, struggle to attract candidates, take longer to fill vacancies, and need to repost jobs multiple times. This can increase recruitment costs and effort.

- **Objective:** Help the TA team decide which roles to prioritise, what salary ranges to offer, and when to post jobs by showing market demand, salary benchmarks, and competition levels across roles and industries.

- **Target users & value:** TA specialists and hiring managers. Instead of guessing salary bands or posting jobs blindly, they can benchmark against 1M+ SG job postings — e.g. spotting roles where postings attract very few applications (hard-to-fill, needs stronger offers) vs. roles flooded with applicants (competitive market, can hire selectively).

**Success criteria:** a TA user can answer "what salary should we offer for role X?" in under one minute using the dashboard. The dashboard helps the company plan hiring better, save time, and use its recruitment budget more effectively.

### Key Business Questions
Each question maps to specific columns and one dashboard view:
| # | Business question | Key columns | Chart / view |
|---|---|---|---|
| Q1 | What salary should we offer for role X? | title, categories, positionLevels, salary columns | Box plot by level/industry + median/P25/P75 metric cards, with filters |
| Q2 | Which roles are hard to fill?  | metadata_repostCount, metadata_totalNumberJobApplication ÷ numberOfVacancies | Scatter plot (X = repost count, Y = applications per vacancy) — bottom-right quadrant = hard-to-fill |
| Q3 | Which roles/industries have the most demand? | parsed categories, numberOfVacancies | Horizontal bar: Top 10 industries by vacancies; bar by position level |
| Q4 | Where can we hire selectively? | same as Q2 | Same scatter, top-left quadrant (low repost, high applications) |
| Q5 | When should we post jobs? | metadata_originalPostingDate (monthly) | Line chart: postings & avg applications over time (from May 2023; earlier months are sparse) |
| Q6 | Agency vs direct employer?  | metadata_isPostedOnBehalf | Global filter toggle across all views |

## 2. Data Handling & Process
### Dataset

The dataset covers job postings across the Singapore market. This is useful because the company competes with employers from different sectors for the same talent.

- **Source:** Singapore job postings, provided by instructor
- **Size:** ~1,048,865 rows × 22 columns (~286 MB CSV)
- **Period covered:** Oct 2022 – May 2024

**Step by step summarize the clean procedure:** [View file](https://github.com/jennyhwo85-lgtm/module1-project/blob/main/notebooks/clean_db_summary.md)

## 3. Dashboard / app walkthrough

The dashboard answer six business questions to help the TA team’s annual hiring plan. 

It helps the team compare salaries, identify roles with high demand or possible hiring difficulties, understand applicant response, review posting trends and consider whether agency support is needed.

**Dashboard link:**

- **Local URL:** <http://localhost:8501>
- **Network URL:** <http://172.20.196.98:8501>
## 4. Challenges & Learning
### Challenges

Large dataset (1M+ rows) required efficient data loading and cleaning.

Missing values and outliers needed careful handling.

We needed to turn raw data into useful hiring insights.

### What We Learned

- How to work with large datasets.
- How to find useful patterns from data.
- How to answer business questions using dashboards.
- How to work as a team using GitHub.

### Next Steps

- Include predictive analytics to forecast hiring demand and salary trends.
- Deploy the dashboard for easier access by recruiters and hiring managers.
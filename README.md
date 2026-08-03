# SG Jobs Analytics — Talent Acquisition Insights Dashboard

**NTU SCTP Data Science & AI (Cohort 6) — Module 1 Assignment Project (Group 3)**

A data product built on 1M+ real Singapore job postings from MyCareersFuture,
helping talent acquisition teams make evidence-based hiring decisions.

**Original assignment repository:**  
[https://github.com/su-ntu-ctp/6m-data-C1.2-coaching-assignment-project](https://github.com/su-ntu-ctp/6m-data-C1.2-coaching-assignment-project)

---

## 1. Project Overview

### Business Case

- **Business scenario:** A talent acquisition (TA) team at a mid-sized
  Singapore company planning its hiring strategy for the year ahead.

  #### **Why Plan Ahead?**

   Hiring is a lengthy process that involves budget approval, recruitment, interviews, and onboarding.

   Planning ahead allows companies to allocate resources and prepare for difficult-to-fill roles before hiring needs become urgent.

- **Problem statement:** The TA team needs better information to plan hiring. Without salary benchmarks and market insights, the company may offer unsuitable salaries, struggle to attract candidates, take longer to fill vacancies, and need to repost jobs multiple times. This can increase recruitment costs and effort.
- **Objective:** Help the TA team decide **which roles to prioritise, what
  salary ranges to offer, and when to post jobs** — by revealing market
  demand, salary benchmarks, and competition levels across roles and
  industries.
- **Target users & value:** TA specialists and hiring managers. Instead of
  guessing salary bands or posting jobs blindly, they can benchmark against
  1M+ real MyCareersFuture postings — e.g. spotting roles where postings
  attract very few applications (hard-to-fill, needs stronger offers) vs.
  roles flooded with applicants (competitive market, can hire selectively).

**Success criteria:** a TA user can answer *"what salary should we offer for
role X?"* in under one minute using the dashboard.
The dashboard helps the company plan hiring better, save time, and use its
recruitment budget more effectively.

### Key Business Questions

Each question maps to specific columns and one dashboard view. All six
questions are implemented and selectable from the sidebar.

| # | Business question | Key columns | Chart / view as built |
|---|---|---|---|
| Q1 | What salary should we offer for role X? | `positionLevels`, `average_salary`, `title` | Bar chart — median salary by position level; box plot — salary distribution by position level; free-text role search returns matching-job salary summary |
| Q2 | Which roles are hard to fill? ⭐ | `metadata_repostCount`, `applications_per_vacancy` | Bar chart — Top 10 industries by % hard-to-fill; scatter plot — average reposts vs. average applications per vacancy, aggregated by industry |
| Q3 | Which roles/industries have the most demand? | `title`, `numberOfVacancies` | Bar chart + data table — Top 20 roles by vacancies. **Filtered View / Global View tabs** |
| Q4 | Where can we hire selectively? | `metadata_repostCount`, `applications_per_vacancy` | Data table — Top 10 selective-hiring industries; scatter plot — total reposts vs. average applications per vacancy, aggregated by industry |
| Q5 | When should we post jobs? | `posting_month_year`, `applications_per_vacancy` | Line chart — postings & average applications over time. **Filtered View / Global View tabs** |
| Q6 | Agency vs direct employer? | `metadata_isPostedOnBehalf` | Bar chart — vacancies by posting type. Also available as a global sidebar filter. **Filtered View / Global View tabs** |

**Definitions used**

- *Hard to fill* — reposts at or above the median **and** applications per
  vacancy at or below the median, among postings with recorded activity.
- *Selective hiring* — reposts in the bottom quartile **and** applications
  per vacancy in the top quartile.
- Both metrics are calculated on the subset of postings that have activity
  data (applications, views, or reposts recorded).

**Sidebar filters:** Industry · Year · Agency vs Direct · Search for Role

### Dataset

The dataset covers job postings across the Singapore market. This is useful
because the company competes with employers from different sectors for the
same talent.

- **Source:** Singapore job postings (MyCareersFuture), provided by instructor
- **Raw size:** ~1,048,865 rows × 22 columns (~286 MB CSV)
- **Cleaned size:** 1,044,597 rows × 32 columns (10 engineered features added)
- **Period covered:** Oct 2022 – May 2024
- **Note:** The raw CSV is **not** included in this repo (exceeds GitHub's
  100 MB limit) and its download link is **intentionally not published**
  here since this repo is public. Cohort members: get the dataset from the
  instructor's pinned message in the course Discord (ds6-lesson-prep). A
  cleaned, compressed version (`db/SGJobData_cleaned.csv.gz`) is included
  in this repo and is **all that is needed to run the dashboard.**

### Data Dictionary

Full column reference: [`report/data_dictionary.md`](report/data_dictionary.md)

**Source columns**

| Column | Type | Notes |
|---|---|---|
| `employmentTypes` | str | Permanent, Full Time, Contract, Part Time, Temporary, Internship/Attachment, Freelance, or Flexi-work. |
| `metadata_expiryDate` | date | Date when the job posting expires. |
| `metadata_isPostedOnBehalf` | bool | `True` if a recruiter posted the job on behalf of the hiring company. |
| `metadata_jobPostId` | str | Unique job-posting ID, for example `MCF-2023-0252866`. |
| `metadata_newPostingDate` | date | Date of the most recent repost. |
| `metadata_originalPostingDate` | date | Date when the job was first posted. |
| `metadata_repostCount` | int | Number of times the same job was reposted. A high value may indicate a hard-to-fill role. |
| `metadata_totalNumberJobApplication` | int | Total number of job applications received. |
| `metadata_totalNumberOfView` | int | Total number of times the job posting was viewed. |
| `minimumYearsExperience` | int | Minimum number of years of experience required. |
| `numberOfVacancies` | int | Number of available positions or open headcount. |
| `positionLevels` | str | Fresh/Entry Level, Junior Executive, Executive, Senior Executive, Professional, Manager, Middle Management, Senior Management, or Non-executive. |
| `postedCompany_name` | str | Name of the poster. It may be a recruitment agency rather than the actual hiring company. |
| `salary_minimum` / `salary_maximum` | int | Minimum and maximum salary offered. |
| `title` | str | Free-text job title. |
| `average_salary` | float | Average of `salary_minimum` and `salary_maximum`. |

**Engineered features (added during cleaning)**

| Column | Type | Notes |
|---|---|---|
| `industry_list` / `industry_primary` | str | Parsed from the raw `categories` JSON array. `industry_primary` is the first listed category and is what the dashboard filters on. |
| `applications_per_vacancy` | float | `metadata_totalNumberJobApplication ÷ numberOfVacancies`. Core competition metric for Q2 and Q4. |
| `salary_median` / `salary_range_width` / `salary_band` | int / str | Derived salary features. Bands: Entry, Mid, Senior, Lead, Executive. |
| `is_hard_to_fill` / `is_selective_hire` | bool | Pre-computed classification flags. |
| `is_agency_post` | bool | Mirrors `metadata_isPostedOnBehalf`. |
| `posting_year` / `posting_month` / `posting_quarter` / `posting_weekday` / `posting_month_year` | int / str | Date parts extracted for time-trend analysis. |
| `days_to_expiry` | int | Days between posting and expiry. |

### Data Handling & Process

Step-by-step cleaning procedure:
[`notebooks/clean_db_summary.md`](notebooks/clean_db_summary.md)

---

## 2. Dashboard Structure

The dashboard presents two levels of analysis, satisfying the assignment
requirement for both an overview and a drill-down view.

**Overview (Global View)** — headline patterns across the full 1M+ row
dataset, unaffected by sidebar filters. Available as the *Global View* tab
on Q3, Q5 and Q6.

**Drill-down (Filtered View)** — the same analysis narrowed by the sidebar
filters (industry, year, agency vs direct, role keyword), with five KPI
cards recalculating live: Total Vacancies · Job Postings · Median Salary ·
Apps per Vacancy · Avg Repost Count.

Users switch between the six business questions using the sidebar radio
control; each question renders its own charts within this two-level frame.

---

## 3. Learning Outcomes

Through this project, our team applies and consolidates the full Module 1
skill chain:

1. **Data loading at scale** — sampling strategies (`nrows`), memory-aware
   loading of a 1M+ row CSV with Pandas.
2. **Data cleaning & quality judgement** — identifying and justifying
   decisions on missing values, outlier salaries, and malformed fields.
3. **Feature engineering** — deriving business-meaningful features such as
   salary bands, industry categories (parsed from JSON), and
   demand/competition metrics.
4. **Exploratory Data Analysis (EDA)** — using descriptive statistics and
   visualisation to surface patterns that shape the dashboard design.
5. **Data storytelling** — framing findings as answers to a business
   question, not just charts.
6. **Dashboard development** — building an interactive, filterable data
   product for a specific user group.
7. **Collaboration with Git/GitHub** — branch/PR workflow, individual commit
   history, and code review as a team of five.

---

## 4. Team

| # | Member | GitHub | Primary Responsibility |
|---|---|---|---|
| 1 | Jenny Hwo | [@jennyhwo85-lgtm](https://github.com/jennyhwo85-lgtm) | Repo setup & scoping, preliminary EDA, project documentation (README) |
| 2 | Wong Lai Yoke | [@laiyokew6996](https://github.com/laiyokew6996) | `db/` folder setup, slide deck, chart visualisation, presenter |
| 3 | Qu Xin | [@quxin43](https://github.com/quxin43) | Data cleaning & validation, feature engineering |
| 4 | Wei Xiang (小翔) | [@boyboi86](https://github.com/boyboi86) | Full EDA & project coordination |
| 5 | Gerine Goh Sipei | [@gerinegohsp](https://github.com/gerinegohsp) | Streamlit dashboard & EDA validation |

> Workflow: each member works on their own branch and submits at least one
> Pull Request, since commit history is assessed individually.

---

## 5. Project Structure

```
module1-project/
├── .gitignore
├── README.md
├── Presentation.md                      ← presentation flow / speaker notes
├── Presentation Slide Deck - Group 3.pptx
├── dashboard.py                         ← Streamlit dashboard (Gerine)
├── environment.yml
├── requirements.txt
├── db/
│   └── SGJobData_cleaned.csv.gz         ← cleaned, compressed dataset (Qu Xin)
├── notebooks/
│   ├── clean_db_summary.md              ← step-by-step cleaning procedure
│   ├── explore.ipynb                    ← preliminary EDA on sample (Jenny)
│   ├── clean_db.ipynb                   ← cleaning notebook (Qu Xin)
│   └── full_eda.ipynb                   ← full EDA, Q1–Q5 analysis (Wei Xiang)
└── report/
    └── data_dictionary.md               ← full column reference
```

---

## 6. Setup & How to Run

### Prerequisites

- Python 3.10
- Conda (recommended) or pip

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/jennyhwo85-lgtm/module1-project.git
cd module1-project

# 2. Create and activate the environment
conda env create -f environment.yml
conda activate pds

#    Alternative, if you already have Python 3.10:
#    pip install -r requirements.txt

# 3. Launch the dashboard
streamlit run dashboard.py
```

The dashboard opens automatically at `http://localhost:8501`.

> **Important:** run `streamlit run dashboard.py` from the repository root.
> The dashboard loads its data using the relative path
> `db/SGJobData_cleaned.csv.gz` and will not start from another directory.

No additional data download is required — the cleaned dataset is versioned
in this repo. First load takes roughly 30–60 seconds while the compressed
CSV is read and cached; subsequent interactions are fast.

### Running the notebooks

Open any notebook in `notebooks/` in VS Code or Jupyter and select the
`pds` kernel. Notebooks read the dataset via `../db/SGJobData_cleaned.csv.gz`.

---

## 7. Milestones & Progress

| Week | Target (per assignment brief) | Status |
|---|---|---|
| Week 1 | Business case chosen + data loaded (sample first) + first EDA | ✅ Done |
| Week 2 | Cleaning + feature engineering + key charts drafted | ✅ Done |
| Week 3 | Dashboard assembled + story polished + presentation rehearsed | ✅ Done |

### Week 1 EDA highlights

- `occupationId` is 100% null → dropped during cleaning.
- Salary outliers found (min $1, max $205,000/month vs. median $3,750) →
  flagged for a justified filter range during cleaning.
- `categories` is stored as a JSON string (multi-label) → parsed into
  `industry_list` and `industry_primary` before industry-level analysis.
- Early months (Oct 2022 – Feb 2023) are sparse; volume stabilises from
  ~May 2023 → time-trend views note this.

---

## 8. Key Findings

<!-- TODO: fill in 3-5 findings once Wei Xiang confirms the final numbers.
     Candidates from full_eda.ipynb:
     - Personal Care / Beauty has the highest hard-to-fill rate at 85%.
     - Hard-to-fill roles receive 92.7% fewer applications than other roles,
       despite paying only 4.8% more on average.
     - Legal and Information Technology lead on median salary
       (SGD 7,000 and 6,750 respectively).
     - F&B leads on total vacancies (244,260), ahead of Customer Service
       and Information Technology.
     - Tuesday sees the most postings; Wednesday the best engagement. -->

---

## 9. Tools

Python 3.10 · Pandas · NumPy · Altair · Matplotlib / Seaborn ·
Streamlit · Jupyter (VS Code) · Git & GitHub

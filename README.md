# SG Jobs Analytics — Talent Acquisition Insights Dashboard

**NTU SCTP Data Science & AI (Cohort 6) — Module 1 Assignment Project**

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
The dashboard helps the company plan hiring better, save time, and use its recruitment budget more effectively.
### Key Business Questions

Each question maps to specific columns and one dashboard view:

| # | Business question | Key columns | Chart / view |
|---|---|---|---|
| Q1 | What salary should we offer for role X? | `title`, `categories`, `positionLevels`, salary columns | Box plot by level/industry + median/P25/P75 metric cards, with filters |
| Q2 | Which roles are hard to fill? ⭐ | `metadata_repostCount`, `metadata_totalNumberJobApplication` ÷ `numberOfVacancies` | Scatter plot (X = repost count, Y = applications per vacancy) — bottom-right quadrant = hard-to-fill |
| Q3 | Which roles/industries have the most demand? | parsed `categories`, `numberOfVacancies` | Horizontal bar: Top 10 industries by vacancies; bar by position level |
| Q4 | Where can we hire selectively? | same as Q2 | Same scatter, top-left quadrant (low repost, high applications) |
| Q5 | When should we post jobs? | `metadata_originalPostingDate` (monthly) | Line chart: postings & avg applications over time (from May 2023; earlier months are sparse) |
| Q6 | Agency vs direct employer? *(bonus)* | `metadata_isPostedOnBehalf` | Global filter toggle across all views |

Common sidebar filters: industry, position level, employment type, date
range, posted-on-behalf. The derived metric *applications per vacancy*
(Q2/Q4) is computed at the EDA stage.

Q1 + Q3 satisfy the pass requirement (one overview + one drill-down);
Q2 is our differentiator.

### Dataset

The dataset covers job postings across the Singapore market. This is useful because the company competes with employers from different sectors for the same talent. 

- **Source:** Singapore job postings (MyCareersFuture), provided by instructor
- **Size:** ~1,048,865 rows × 22 columns (~286 MB CSV)
- **Period covered:** Oct 2022 – May 2024
- **Note:** The raw CSV is **not** included in this repo (exceeds GitHub's
  100 MB limit) and its download link is **intentionally not published**
  here since this repo is public. Cohort members: get the dataset from the
  instructor's pinned message in the course Discord (ds6-lesson-prep) and
  place it in the project root as `SGJobData.csv`. A cleaned, compressed
  version (`SGJobData_cleaned.csv.gz`) is included in this repo and is
  sufficient for the EDA and dashboard stages.



### Data Dictionary


| Column | Type | Notes |
|---|---|---|
| `categories` | str (JSON array) | Example: `[{"id":21,"category":"Information Technology"}]`. A job can belong to multiple categories, so this column needs to be parsed. |
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
| `salary_minimum` | int | Minimum salary offered. |
| `salary_maximum` | int | Maximum salary offered. |
| `salary_type` | str | Salary frequency. Almost all records are `Monthly`. |
| `status_jobStatus` | str | Job-posting status: Open, Closed, or Re-open. |
| `title` | str | Free-text job title. |
| `average_salary` | float | Pre-calculated average of `salary_minimum` and `salary_maximum`. |

### Data Handling & Process

- **Step by step summarize the clean procedure:** [View file](https://github.com/jennyhwo85-lgtm/module1-project/blob/main/notebooks/clean_db_summary.md)

## 2. Learning Outcomes

Through this project, our team applies and consolidates the full Module 1
skill chain:

1. **Data loading at scale** — sampling strategies (`nrows`), memory-aware
   loading of a 1M+ row CSV with Pandas.
2. **Data cleaning & quality judgement** — identifying and justifying
   decisions on missing values, outlier salaries, and malformed fields.
3. **Feature engineering** — deriving business-meaningful features such as
   salary bands, seniority groups, industry categories (parsed from JSON),
   and demand/competition metrics.
4. **Exploratory Data Analysis (EDA)** — using descriptive statistics and
   visualisation (Matplotlib/Seaborn) to surface patterns that shape the
   dashboard design.
5. **Data storytelling** — framing findings as answers to a business
   question, not just charts.
6. **Dashboard development** — building an interactive, filterable data
   product for a specific user group.
7. **Collaboration with Git/GitHub** — branch/PR workflow, individual commit
   history, and code review as a team of five.

---

## 3. Team

| # | Member | GitHub | Primary Responsibility |
|---|---|---|---|
| 1 | Jenny Hwo | [@jennyhwo85-lgtm](https://github.com/jennyhwo85-lgtm) | Repo setup, README (business case & scope), initial EDA on sample |
| 2 | Wong Lai Yoke | [@laiyokew6996](https://github.com/laiyokew6996) | `db/` folder setup, prepare slide deck, Chart Visualization  |
| 3 | Quxin | [@quxin43](https://github.com/quxin43) | Data cleaning (missing values, outliers) & conversion to `.db`/`.sql` |
| 4 | Wei Xiang (小翔) | [@boyboi86](https://github.com/boyboi86) | Full EDA & feature engineering on cleaned data |
| 5 | Gerine Goh Sipei| [@gerinegohsp](https://github.com/gerinegohsp) | Streamlit dashboard & visualisation |

> Workflow: each member works on their own branch and submits at least one
> Pull Request, since commit history is assessed individually.
>
> **Note on the dataset:** the raw CSV (~286 MB) exceeds GitHub's 100 MB
> file limit and is git-ignored. A **cleaned, compressed** dataset
> (`SGJobData_cleaned.csv.gz`) is versioned in the repo instead; see
> Section 1 for how to obtain the raw CSV.

---

## 4. Project Structure

```

module1-project/
├── .gitignore
├── README.md
├── environment.yml
├── requirements.txt
├── db/
│   └── SGJobData.csv               ← Raw data (included in .gitignore)
|   └── SGJobData_cleaned.csv.gz        ← cleaned, compressed dataset (Quxin) (will be replaced)
├── notebooks/
├── ├── clean_db_summary.md       ← Step by step summarize the clean procedure
│   ├── explore.ipynb               ← Jenny's 50k EDA (reference)
│   ├── clean_db.ipynb              ← Quxin's cleaning (reference/ require update)
│   └── full_eda.ipynb           ← new full EDA (Wei Xiang)
├── app/                       ← (planned) Streamlit dashboard code (Gerine)
└── report/                    ← written report, Sections 1–4 (team)

```

---

## 5. Milestones & Progress

| Week | Target (per assignment brief) | Status |
|---|---|---|
| Week 1 | Business case chosen + data loaded (sample first) + first EDA | ✅ Done |
| Week 2 | Cleaning + feature engineering + key charts drafted | 🔄 In progress — cleaning done (`clean_db.ipynb`), full EDA & charts next |
| Week 3 | Dashboard assembled + story polished + presentation rehearsed | ⏳ Planned |

### Week 1 EDA highlights

- `occupationId` is 100% null → will be dropped.
- Salary outliers found (min $1, max $205,000/month vs. median $3,750) →
  a justified filter range will be applied during cleaning.
- `categories` is stored as a JSON string (multi-label) → needs parsing
  before industry-level analysis.
- Early months (Oct 2022 – Feb 2023) are sparse; volume stabilises from
  ~May 2023 → time-trend views will note this.

---

## 6. Setup & How to Run

```bash
# 1. Clone the repo
git clone https://github.com/jennyhwo85-lgtm/module1-project.git
cd module1-project

# 2. Environment (conda, Python 3.10)
conda activate pds        # or: conda create -n pds python=3.10 pandas matplotlib seaborn jupyter

# 3. Place the dataset (from instructor's link) in the project root
#    as SGJobData.csv — it is git-ignored on purpose.

# 4. Open and run the notebook
#    (VS Code: open explore.ipynb and select the 'pds' kernel)
```

*Dashboard run instructions will be added once the app is built (Week 3).*

---

## 7. Tools

Python 3.10 · Pandas · Matplotlib / Seaborn · Jupyter (VS Code) ·
Git & GitHub · Streamlit (dashboard)



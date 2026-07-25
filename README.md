# SG Jobs Analytics — Talent Acquisition Insights Dashboard

**NTU SCTP Data Science & AI (Cohort 6) — Module 1 Assignment Project**

A data product built on 1M+ real Singapore job postings from MyCareersFuture,
helping talent acquisition teams make evidence-based hiring decisions.

---

## 1. Project Overview

### Business Case

- **Business scenario:** A talent acquisition (TA) team at a mid-sized
  Singapore company planning its hiring strategy for the year ahead.
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

### Dataset

- **Source:** Singapore job postings (MyCareersFuture), provided by instructor
- **Size:** ~1,048,865 rows × 22 columns (~286 MB CSV)
- **Period covered:** Oct 2022 – May 2024
- **Note:** The raw CSV is **not** included in this repo (exceeds GitHub's
  100 MB limit). Download it from the link provided by the instructor and
  place it in the project root as `SGJobData.csv`.

---

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
| 2 | Wong Lai Yoke | [@laiyokew6996](https://github.com/laiyokew6996) | `db/` folder setup & dataset handling (via PR) |
| 3 | Quxin | [@quxin43](https://github.com/quxin43) | Data cleaning (missing values, outliers) & conversion to `.db`/`.sql` |
| 4 | Wei Xiang (小翔) | [@boyboi86](https://github.com/boyboi86) | Full EDA & feature engineering on cleaned data |
| 5 | Gerine Goh | [@gerinegohsp](https://github.com/gerinegohsp) | Streamlit dashboard & visualisation |

> Workflow: each member works on their own branch and submits at least one
> Pull Request, since commit history is assessed individually.
>
> **Note on the dataset:** the raw CSV (~286 MB) exceeds GitHub's 100 MB
> file limit and is git-ignored. The `db/` folder holds the **cleaned,
> compressed** database file instead; the raw CSV download link is in
> Section 1.

---

## 4. Project Structure

```
module1-project/
├── README.md            ← you are here
├── .gitignore           ← excludes the large raw CSV
├── explore.ipynb        ← Week 1: initial EDA on 50k sample (Jenny)
├── db/                  ← cleaned database file (.db / .parquet) + notes (Wong Lai Yoke, Quxin)
├── notebooks/           ← cleaning & EDA notebooks (Quxin, Wei Xiang)
├── app/                 ← Streamlit dashboard code (Gerine)
└── report/              ← written report, Sections 1–4 (team)
```

---

## 5. Milestones & Progress

| Week | Target (per assignment brief) | Status |
|---|---|---|
| Week 1 | Business case chosen + data loaded (sample first) + first EDA | ✅ Done |
| Week 2 | Cleaning + feature engineering + key charts drafted | 🔄 In progress |
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
Git & GitHub · *Dashboard framework: TBC (e.g. Streamlit)*
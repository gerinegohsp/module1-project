# Data Dictionary - SGJobData

**Version:** 2.0
**Last Updated:** July 2026
**Status:** Proposed Schema

---

## Purpose

This document defines the final database schema for `SGJobData.db`, which serves as the source of truth for all analysis, EDA, and dashboard development.

---

## 1. Original CSV Columns

### Job Posting Information

| Column Name | Type | Description | Notes |
|-------------|------|-------------|-------|
| `title` | TEXT | Job title (free text) | Used for role identification |
| `categories` | JSON | Industry/sector categories (array of objects) | Contains `id` and `category` fields; needs parsing |
| `positionLevels` | TEXT | Seniority level | Values: Entry, Mid, Senior, Executive, Lead |
| `employmentTypes` | TEXT | Employment type | Values: Permanent, Full Time, Part Time, Contract |
| `numberOfVacancies` | INTEGER | Number of positions available | Used for demand calculation |

### Salary Information

| Column Name | Type | Description | Notes |
|-------------|------|-------------|-------|
| `salary_minimum` | INTEGER | Minimum monthly salary (SGD) | Contains outliers ($1 - $205,000) |
| `salary_maximum` | INTEGER | Maximum monthly salary (SGD) | Contains outliers ($1 - $205,000) |
| `salary_type` | TEXT | Salary period | Values: Monthly, Hourly, Annual, Daily |
| `average_salary` | FLOAT | Average salary (pre-calculated) | May be inconsistently derived; verify or recalculate |

### Application & Engagement Metrics

| Column Name | Type | Description | Notes |
|-------------|------|-------------|-------|
| `metadata_totalNumberJobApplication` | INTEGER | Total number of applications received | Key metric for competition analysis |
| `metadata_totalNumberOfView` | INTEGER | Total number of job views | Supplementary engagement metric |
| `metadata_repostCount` | INTEGER | Number of times job was reposted | Indicator of difficulty filling role |
| `metadata_isPostedOnBehalf` | BOOLEAN | `True` = agency posting, `False` = direct employer | Differentiates hiring channels |

### Date Information

| Column Name | Type | Description | Notes |
|-------------|------|-------------|-------|
| `metadata_originalPostingDate` | DATE | Original job posting date | Primary time reference |
| `metadata_newPostingDate` | DATE | Latest repost date | Updated when reposted |
| `metadata_expiryDate` | DATE | Job posting expiration date | Used to calculate posting duration |

### Status & Identifiers

| Column Name | Type | Description | Notes |
|-------------|------|-------------|-------|
| `metadata_jobPostId` | TEXT | Unique job posting identifier | Primary key candidate |
| `postedCompany_name` | TEXT | Company name | For company-level analysis |
| `status_id` | INTEGER | Job status identifier code | Redundant with `status_jobStatus` |
| `status_jobStatus` | TEXT | Job status | Values: Open, Closed |
| `occupationId` | INTEGER | Occupation classification ID | **100% null** - no usable data |

---

## 2. New Features in Database

These derived features are calculated during data preparation and stored in `SGJobData.db` to support business questions.

### Salary-Related Features

| Feature | Type | Definition | Business Use |
|---------|------|------------|--------------|
| `salary_median` | INTEGER | `(salary_minimum + salary_maximum) / 2` | Single salary estimate for benchmarks (Q1) |
| `salary_band` | TEXT | Categorical salary range: `Entry (<3k)`, `Mid (3-6k)`, `Senior (6-10k)`, `Lead (10-20k)`, `Executive (>20k)` | Salary grouping for filtering and visualization (Q1) |
| `salary_range_width` | INTEGER | `salary_maximum - salary_minimum` | Indicates negotiation flexibility |

### Competition & Demand Features

| Feature | Type | Definition | Business Use |
|---------|------|------------|--------------|
| `applications_per_vacancy` | FLOAT | `metadata_totalNumberJobApplication / numberOfVacancies` | Competition intensity; higher = more applicants per role (Q2, Q4) |
| `is_hard_to_fill` | BOOLEAN | `(metadata_repostCount > median) AND (applications_per_vacancy < median)` | Flags roles with high repost frequency but low applicant interest (Q2) |
| `is_selective_hire` | BOOLEAN | `(metadata_repostCount < median) AND (applications_per_vacancy > median)` | Flags roles with high applicant interest requiring fewer reposts (Q4) |

### Industry Features

| Feature | Type | Definition | Business Use |
|---------|------|------------|--------------|
| `industry_list` | TEXT[] | Array of all industries from `categories` JSON | Full industry classification |
| `industry_primary` | TEXT | First industry from `industry_list` | Simplified primary industry for analysis (Q3) |

### Time-Based Features

| Feature | Type | Definition | Business Use |
|---------|------|------------|--------------|
| `posting_year` | INTEGER | Year extracted from `metadata_originalPostingDate` | Annual trend analysis (Q5) |
| `posting_month` | INTEGER | Month extracted from `metadata_originalPostingDate` | Monthly trend analysis (Q5) |
| `posting_quarter` | INTEGER | Quarter extracted from `metadata_originalPostingDate` | Quarterly trend analysis (Q5) |
| `posting_weekday` | INTEGER | Day of week from `metadata_originalPostingDate` (0=Monday) | Weekly pattern analysis (Q5) |
| `days_to_expiry` | INTEGER | `metadata_expiryDate - metadata_originalPostingDate` | Job duration metric (Q5) |

### Additional Features

| Feature | Type | Definition | Business Use |
|---------|------|------------|--------------|
| `is_agency_post` | BOOLEAN | Same as `metadata_isPostedOnBehalf` | Agency vs direct employer filtering (Q6) |
| `posting_month_year` | TEXT | `YYYY-MM` format | Grouped time filter for dashboard |

---

## 3. Columns to Keep (After Cleaning)

### Raw Columns Retained in Database

| Column | Cleaning Required | Final Type |
|--------|-------------------|------------|
| `metadata_jobPostId` | None | TEXT (PK) |
| `title` | None | TEXT |
| `postedCompany_name` | Fill nulls with "Unknown" | TEXT |
| `positionLevels` | Standardize values (e.g., "Executive" → "Executive") | TEXT |
| `employmentTypes` | Standardize values | TEXT |
| `numberOfVacancies` | None | INTEGER |
| `salary_minimum` | Filter to $500 - $25,000; drop rows outside range | INTEGER |
| `salary_maximum` | Filter to $500 - $25,000; drop rows outside range | INTEGER |
| `metadata_totalNumberJobApplication` | Fill nulls with 0 | INTEGER |
| `metadata_totalNumberOfView` | Fill nulls with 0 | INTEGER |
| `metadata_repostCount` | Fill nulls with 0 | INTEGER |
| `metadata_isPostedOnBehalf` | Fill nulls with False | BOOLEAN |
| `metadata_originalPostingDate` | Convert to datetime; drop invalid dates | DATETIME |
| `metadata_newPostingDate` | Convert to datetime; drop invalid dates | DATETIME |
| `metadata_expiryDate` | Convert to datetime; drop invalid dates | DATETIME |
| `status_jobStatus` | Keep as-is (Open/Closed/Filled) | TEXT |

### Derived Features Added

| Feature | Derived From | Type |
|---------|--------------|------|
| `salary_median` | `salary_minimum` + `salary_maximum` | INTEGER |
| `salary_band` | `salary_minimum` | TEXT |
| `salary_range_width` | `salary_maximum - salary_minimum` | INTEGER |
| `applications_per_vacancy` | `metadata_totalNumberJobApplication / numberOfVacancies` | FLOAT |
| `is_hard_to_fill` | `metadata_repostCount` + `applications_per_vacancy` | BOOLEAN |
| `is_selective_hire` | `metadata_repostCount` + `applications_per_vacancy` | BOOLEAN |
| `industry_list` | `categories` JSON | TEXT[] |
| `industry_primary` | `categories` JSON | TEXT |
| `posting_year` | `metadata_originalPostingDate` | INTEGER |
| `posting_month` | `metadata_originalPostingDate` | INTEGER |
| `posting_quarter` | `metadata_originalPostingDate` | INTEGER |
| `posting_weekday` | `metadata_originalPostingDate` | INTEGER |
| `days_to_expiry` | `metadata_expiryDate - metadata_originalPostingDate` | INTEGER |
| `is_agency_post` | `metadata_isPostedOnBehalf` | BOOLEAN |
| `posting_month_year` | `metadata_originalPostingDate` | TEXT |

---

## 4. Columns to Drop 
### Week 1 EDA highlights (See readme.md)

| Column | Reason |
|--------|--------|
| `occupationId` | 100% null values; no business value |
| `status_id` | Redundant with `status_jobStatus` | 
| `salary_type` | Redundant given only 1 unique value `monthly` | 
| `categories` | Replaced by parsed `industry_list` and `industry_primary` |

---

## 5. Database Schema Summary

### Table: `jobs`

| Column | Type | Nullable | PK / FK | Description |
|--------|------|----------|---------|-------------|
| `job_id` | TEXT | NO | PK | Unique job identifier |
| `title` | TEXT | NO | - | Job title |
| `company` | TEXT | YES | - | Company name |
| `position_level` | TEXT | YES | - | Seniority level (Entry/Mid/Senior/Executive/Lead) |
| `employment_type` | TEXT | YES | - | Employment type (Permanent/Full Time/Part Time) |
| `vacancies` | INTEGER | YES | - | Number of positions |
| `salary_min` | INTEGER | YES | - | Minimum salary (filtered) |
| `salary_max` | INTEGER | YES | - | Maximum salary (filtered) |
| `salary_median` | INTEGER | YES | - | Median salary (derived) |
| `salary_band` | TEXT | YES | - | Salary category (Entry/Mid/Senior/Lead/Executive) |
| `salary_range_width` | INTEGER | YES | - | Range width for negotiation |
| `posting_date` | DATETIME | YES | - | Original posting date |
| `expiry_date` | DATETIME | YES | - | Job expiry date |
| `repost_count` | INTEGER | YES | - | Number of reposts |
| `applications` | INTEGER | YES | - | Total applications |
| `views` | INTEGER | YES | - | Total views |
| `apps_per_vacancy` | FLOAT | YES | - | Applications per vacancy |
| `is_agency` | BOOLEAN | YES | - | Posted by agency? |
| `status` | TEXT | YES | - | Open/Closed/Filled |
| `industry_primary` | TEXT | YES | - | Primary industry |
| `industry_list` | TEXT | YES | - | All industries (JSON array) |
| `is_hard_to_fill` | BOOLEAN | YES | - | Hard-to-fill flag |
| `is_selective_hire` | BOOLEAN | YES | - | Selective hire flag |
| `posting_year` | INTEGER | YES | - | Year of posting |
| `posting_month` | INTEGER | YES | - | Month of posting |
| `posting_quarter` | INTEGER | YES | - | Quarter of posting |
| `posting_weekday` | INTEGER | YES | - | Day of week (0=Monday) |
| `days_to_expiry` | INTEGER | YES | - | Job duration in days |
| `posting_month_year` | TEXT | YES | - | Month/year grouping (YYYY-MM) |

### Indexes

```sql
CREATE INDEX idx_industry ON jobs(industry_primary);
CREATE INDEX idx_position_level ON jobs(position_level);
CREATE INDEX idx_posting_date ON jobs(posting_date);
CREATE INDEX idx_salary_band ON jobs(salary_band);
CREATE INDEX idx_is_agency ON jobs(is_agency);
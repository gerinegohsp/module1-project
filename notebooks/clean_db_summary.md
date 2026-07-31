# Step by step summarize the clean procedure

## Step 1 - Analysis 1

| Analysis | Finding | Action recorded |
|---------|--------------|------|
| df.head() | 'categories' is JSON array. a job can belong to multiple categories | parse 'categories' |
| df.shape | (1048585, 22) | - |
| df.info | 'metadata_isPostedOnBehalf', 'metadata_newPostingDate', 'metadata_originalPostingDate' data type is str, should be date; 100% Null in 'occupationId'  | change datatype of 'metadata_isPostedOnBehalf', 'metadata_newPostingDate', 'metadata_originalPostingDate' to date; drop 'occupationId' |
| df.describe() | 100% 0 value in 'status_id'; suspicious min/max in 'minimumYearsExperience', 'numberOfVacancies', 'salary_maximum', 'salary_minimum' | drop 'status_id'; further check value in 'minimumYearsExperience', 'numberOfVacancies', 'salary_maximum', 'salary_minimum' |
| df.describe(include=['object']) | single value Monthly in 'salary_type' | drop 'salary_type' |
| df[column].value_counts().head(10) | values in columns are standardized | - |
| df.duplicated().sum() | 3987 duplicated row found | drop duplicated row |
| df.isnull().sum() | 11 columns has missing value | recheck to decide drop or fill after drop duplicate rows and meaningless columns |

## Step 2 - Clean 1

#### Drop duplicates, keep='first' ensures you keep the first occurrence and delete the rest
df = df.drop_duplicates(keep='first')

#### Drop columns that are not useful for analysis
columns_to_drop = ['occupationId', 'status_id', 'status_jobStatus','salary_type']
df = df.drop(columns=columns_to_drop, axis=1)

## Step 3 - Analysis 2
| Analysis | Finding | Action recorded |
|---------|--------------|------|
| df[df.isnull().any(axis=1)].index.tolist() | only one row [197478] has missing value, in 11 columns | drop this row |

## Step 4 - Clean 2

#### Drop the row with missing values (row 197478)
df = df.dropna()

#### Convert metadata_expiryDate, metadata_newPostingDate, metadata_originalPostingDate to datetime format
date_cols = [
    "metadata_expiryDate",
    "metadata_newPostingDate",
    "metadata_originalPostingDate",
]
df[date_cols] = df[date_cols].apply(pd.to_datetime)

## Step 5 - create new columns based on "report/data_dictionary.md" for following analysis. Total 15 columns

## Step 6 - re-check the db after cleaning

| Analysis | Finding | Action recorded |
|---------|--------------|------|
| df.head() | normal | - |
| df.shape | (1044597, 32), 17 original columns + 15 calculated columns | - |
| df.info | data type matches requirement  | - |
| df.describe() | normal | - |
| df.describe(include=['object']) | normal | - |
| df.duplicated().sum() | no duplicate rows | - |
| df.isnull().sum() | no missing value | - |

## Step 7 - Analysis and clean on salary_maximum and salary_minimum

#### The highside of salary_maximum

| Analysis | Finding | Action taken |
|---------|--------------|------|
| draw box plot of salary_maximum by positionLevels | 12 obvious outliers | furture check detail |
| list the record with top 12 salary_maximum | all of these record are not reasonable | drop these 12 records |
| re-draw box plot of salary_maximum by positionLevels | 5 obvious outliers  | furture check detail |
| list the record with top 5 salary_maximum | 4 of the 5 records are not reasonable | drop these 4 records |
| re-draw box plot of salary_maximum by positionLevels | No obvious outliers  | furture check detail |
| list the record with top 1 salary_maximum in each positionLevels| all records are reasonable | - |

#### The highside of salary_minimum

| Analysis | Finding | Action taken |
|---------|--------------|------|
| draw box plot of salary_minimum by positionLevels | No obvious outliers  | furture check detail |
| list the record with top 3 salary_minimum in each positionLevels| all records are reasonable | - |

#### The lowside of salary_maximum and salary_minimum

| Analysis | Finding | Action taken |
|---------|--------------|------|
|  list down the bottom 10 unique value and their count of salary_minimum and salary_maximum by positionLevels | both salary_minimum and salary_maximum start from 1 in every positionLevels | - |

#### The high side of numberOfVacancies and minimumYearsExperience

| Analysis | Finding | Action taken |
|---------|--------------|------|
| draw boxplot of numberOfVacancies and minimumYearsExperience; list down the top 10 unique value and their count of numberOfVacancies and minimumYearsExperience | numberOfVacancies has outlier values, such as 999,998,900, 500...; minimumYearsExperience has value up to 80 | keep numberOfVacancies; drop rows w/ minimumYearsExperience >40 |


## Step 8 - Save the DB
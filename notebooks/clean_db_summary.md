# Step by step summarize the clean procedure

## Analysis 1

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

## Clean 1

#### Drop duplicates, keep='first' ensures you keep the first occurrence and delete the rest
df = df.drop_duplicates(keep='first')

#### Drop columns that are not useful for analysis
columns_to_drop = ['occupationId', 'status_id', 'status_jobStatus','salary_type']
df = df.drop(columns=columns_to_drop, axis=1)

## Analysis 2
| Analysis | Finding | Action recorded |
|---------|--------------|------|
| df[df.isnull().any(axis=1)].index.tolist() | only one row [197478] has missing value, in 11 columns | drop this row |

## Clean 2

#### Drop the row with missing values (row 197478)
df = df.dropna()

#### Convert metadata_expiryDate, metadata_newPostingDate, metadata_originalPostingDate to datetime format
date_cols = [
    "metadata_expiryDate",
    "metadata_newPostingDate",
    "metadata_originalPostingDate",
]
df[date_cols] = df[date_cols].apply(pd.to_datetime)


## EDA 1
#### create new columns based on "report/data_dictionary.md" for following analysis. Total 15 columns

## Clean 3

#### re-check the db after cleaning

| Analysis | Finding | Action recorded |
|---------|--------------|------|
| df.head() | normal | - |
| df.shape | (1044597, 32), 17 original columns + 15 calculated columns | - |
| df.info | data type matches requirement  | - |
| df.describe() | normal | - |
| df.describe(include=['object']) | normal | - |
| df.duplicated().sum() | no duplicate rows | - |
| df.isnull().sum() | no missing value | - |



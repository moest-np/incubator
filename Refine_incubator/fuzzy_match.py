import pandas as pd
from fuzzywuzzy import fuzz
import os

# Set display options
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

# Load the dataframes
df_Fuzzy_A = pd.read_csv('./Preprocessed_after_A_3.csv')
df_Fuzzy_B = pd.read_csv('./Preprocessed_after_B_2.csv')
district_id = pd.read_csv('./district_id.csv')


df_Fuzzy_A.shape
df_Fuzzy_B.shape


# Normalize the district names in both dataframes
df_Fuzzy_A['Matched_District'] = df_Fuzzy_A['Matched_District'].str.lower().str.strip()
district_id['modified_district'] = district_id['modified_district'].str.lower().str.strip()

# Merge the two dataframes on the normalized district name
df_Fuzzy_A = pd.merge(df_Fuzzy_A, district_id, left_on='Matched_District', right_on='modified_district', how='left')

# Drop the 'district' column as it's redundant now
df_Fuzzy_A = df_Fuzzy_A.drop(columns=['modified_district'])


df_Fuzzy_A.head()


df_Fuzzy_A.head()
df_Fuzzy_B.head()


# Replace null values by empty strings in df_Fuzzy_B
df_Fuzzy_B = df_Fuzzy_B.fillna('')
# Replace null values by empty strings in df_Fuzzy_B
df_Fuzzy_A = df_Fuzzy_A.fillna('')

# Drop rows from df_Fuzzy_B where 'root_school_name' is an empty string
df_Fuzzy_B = df_Fuzzy_B[df_Fuzzy_B['root_school_name'] != '']

# # Drop rows from df_Fuzzy_A where 'root_school_name' is an empty string
df_Fuzzy_A = df_Fuzzy_A[df_Fuzzy_A['School_name_transliterated'] != '']

# Replace specific patterns in the root_school_name column
df_Fuzzy_B['root_school_name'] = df_Fuzzy_B['root_school_name'].replace(
    {
        r'\benglish vi\b': 'ebs',
        r'\benglish boarding vi\b': 'ebs',
        r'\bboarding vi\b': 'ebs',
        r'\benglish ma boarding v\b': 'ebs',
        r'\benglish ma boarding v\b': 'ebs',
        r'\benglish ma boarding v\b': 'ebs',
        r'\b english bording vi\b': ' ebs',
        
        
    }, regex=True
)


# Replace specific patterns in the root_school_name column
df_Fuzzy_A['School_name_transliterated'] = df_Fuzzy_A['School_name_transliterated'].replace(
    {
        r'\benglish vi\b': 'ebs',
        r'\benglish boarding vi\b': 'ebs',
        r'\bboarding vi\b': 'ebs',
        r'\benglish ma boarding v\b': 'ebs',
        r'\benglish ma boarding v\b': 'ebs',
        r'\benglish ma boarding v\b': 'ebs',
        r'\b english bording vi\b': ' ebs',
        
        
    }, regex=True
)

df_Fuzzy_B.head(1)
df_Fuzzy_B.isnull().sum()

# Replace null values by empty strings in df_Fuzzy_B
df_Fuzzy_B = df_Fuzzy_B.fillna('')

# Drop rows where 'root_school_name' is an empty string
df_Fuzzy_B = df_Fuzzy_B[df_Fuzzy_B['root_school_name'] != '']


# Drop rows where 'root_school_name' is an empty string
df_Fuzzy_A = df_Fuzzy_A[df_Fuzzy_A['School_name_transliterated'] != '']



# Convert text columns to lowercase and strip leading/trailing spaces for df_Fuzzy_A
df_Fuzzy_A = df_Fuzzy_A.apply(lambda x: x.str.lower().str.strip() if x.dtype == "object" else x)

# Convert text columns to lowercase and strip leading/trailing spaces for df_Fuzzy_B
df_Fuzzy_B = df_Fuzzy_B.apply(lambda x: x.str.lower().str.strip() if x.dtype == "object" else x)

df_Fuzzy_B.head(10)
df_Fuzzy_A.head(10)





df_Fuzzy_A.columns
df_Fuzzy_A['School_level_transliterated'].unique()
df_Fuzzy_B['school_levels'].unique()
df_Fuzzy_B.head(100)

df_Fuzzy_B['school_levels'].unique()
# Filter rows where school_levels is 'pravi mavi'
pravi_mavi_rows = df_Fuzzy_B[df_Fuzzy_B['modified_old_name1'] == 'english school']

# Find and print the number of rows affected
affected_rows = df_Fuzzy_B[df_Fuzzy_B['school_levels'] == 'pravi mavi'].shape[0]
print(f"Number of rows affected: {affected_rows}")

# Change 'pravi mavi' to 'mavi'
df_Fuzzy_B['school_levels'] = df_Fuzzy_B['school_levels'].replace('pravi mavi', 'mavi')

pravi_mavi_rows.head()

# Replace specific patterns in the local_level column
df_Fuzzy_B['modified_local_level'] = df_Fuzzy_B['modified_local_level'].replace(
    {
        'municipality': 'napa',
        'metropolitan': 'napa',
        
    }, regex=True
)





# Replace null values by empty strings in df_B
df_Fuzzy_B = df_Fuzzy_B.fillna('')
# Replace null values by empty strings in df_A
df_Fuzzy_A = df_Fuzzy_A.fillna('')

df_Fuzzy_B.isnull().sum()
df_Fuzzy_A.isnull().sum()

# Define the mapping dictionary
mapping = {
    '': 0,
    'avi': 1,
    'pravi': 2,
    'nimavi': 3,
    'mavi': 4
}

df_Fuzzy_B['school_levels'].head()

# Apply the mapping to the 'school_levels' column
df_Fuzzy_B['school_levels_categorized'] = df_Fuzzy_B['school_levels'].map(mapping)



df_Fuzzy_B['school_levels_categorized'].unique()

df_Fuzzy_A.to_csv('./Preprocessed_after_fuzzy_A.csv',index=False)
df_Fuzzy_B.to_csv('./Preprocessed_after_fuzzy_B.csv',index=False)

df_Fuzzy_B.columns
df_Fuzzy_A.columns














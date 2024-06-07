import pandas as pd
from fuzzywuzzy import fuzz
import os

# Function to ensure a directory exists
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Processed data directory
processed_data_dir = os.path.normpath(os.path.join(base_dir, '../../data/processed'))

# Ensure the processed data directory exists
ensure_directory_exists(processed_data_dir)

# File paths
file_path_a3 = os.path.join(processed_data_dir, 'preprocessed_after_A_3.csv')
file_path_b2 = os.path.join(processed_data_dir, 'preprocessed_after_B_2.csv')
district_id_path = os.path.join(processed_data_dir, 'district_id.csv')
output_file_path_fuzzy_a = os.path.join(processed_data_dir, 'preprocessed_after_fuzzy_A.csv')
output_file_path_fuzzy_b = os.path.join(processed_data_dir, 'preprocessed_after_fuzzy_B.csv')

# Set display options
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

# Load the dataframes
df_Fuzzy_A = pd.read_csv(file_path_a3)
df_Fuzzy_B = pd.read_csv(file_path_b2)
district_id = pd.read_csv(district_id_path)

# Normalize the district names in both dataframes
df_Fuzzy_A['Matched_District'] = df_Fuzzy_A['Matched_District'].str.lower().str.strip()
district_id['modified_district'] = district_id['modified_district'].str.lower().str.strip()

# Merge the two dataframes on the normalized district name
df_Fuzzy_A = pd.merge(df_Fuzzy_A, district_id, left_on='Matched_District', right_on='modified_district', how='left')

# Drop the 'district' column as it's redundant now
df_Fuzzy_A = df_Fuzzy_A.drop(columns=['modified_district'])

# Replace null values by empty strings in both dataframes
df_Fuzzy_B = df_Fuzzy_B.fillna('')
df_Fuzzy_A = df_Fuzzy_A.fillna('')

# Drop rows from df_Fuzzy_B where 'root_school_name' is an empty string
df_Fuzzy_B = df_Fuzzy_B[df_Fuzzy_B['root_school_name'] != '']

# Drop rows from df_Fuzzy_A where 'School_name_transliterated' is an empty string
df_Fuzzy_A = df_Fuzzy_A[df_Fuzzy_A['School_name_transliterated'] != '']

# Replace specific patterns in the root_school_name column for both dataframes
pattern_replacements = {
    r'\benglish vi\b': 'ebs',
    r'\benglish boarding vi\b': 'ebs',
    r'\bboarding vi\b': 'ebs',
    r'\benglish ma boarding v\b': 'ebs',
    r'\b english bording vi\b': ' ebs'
}

df_Fuzzy_B['root_school_name'] = df_Fuzzy_B['root_school_name'].replace(pattern_replacements, regex=True)
df_Fuzzy_A['School_name_transliterated'] = df_Fuzzy_A['School_name_transliterated'].replace(pattern_replacements, regex=True)

# Convert text columns to lowercase and strip leading/trailing spaces for both dataframes
df_Fuzzy_A = df_Fuzzy_A.apply(lambda x: x.str.lower().str.strip() if x.dtype == "object" else x)
df_Fuzzy_B = df_Fuzzy_B.apply(lambda x: x.str.lower().str.strip() if x.dtype == "object" else x)

# Change 'pravi mavi' to 'mavi' in df_Fuzzy_B
df_Fuzzy_B['school_levels'] = df_Fuzzy_B['school_levels'].replace('pravi mavi', 'mavi')

# Replace specific patterns in the modified_local_level column of df_Fuzzy_B
df_Fuzzy_B['modified_local_level'] = df_Fuzzy_B['modified_local_level'].replace(
    {
        'municipality': 'napa',
        'metropolitan': 'napa',
    }, regex=True
)

# Define the mapping dictionary
mapping = {
    '': 0,
    'avi': 1,
    'pravi': 2,
    'nimavi': 3,
    'mavi': 4
}

# Apply the mapping to the 'school_levels' column of df_Fuzzy_B
df_Fuzzy_B['school_levels_categorized'] = df_Fuzzy_B['school_levels'].map(mapping)

# Save the updated dataframes to new CSV files
df_Fuzzy_A.to_csv(output_file_path_fuzzy_a, index=False)
df_Fuzzy_B.to_csv(output_file_path_fuzzy_b, index=False)

print("Updated dataframe for Fuzzy A saved to:", output_file_path_fuzzy_a)
print("Updated dataframe for Fuzzy B saved to:", output_file_path_fuzzy_b)

# Print the first 10 rows of the updated dataframes
print("First 10 rows of the updated dataframe for Fuzzy A:")
print(df_Fuzzy_A.head(10))
print("First 10 rows of the updated dataframe for Fuzzy B:")
df_Fuzzy_B.head(10)

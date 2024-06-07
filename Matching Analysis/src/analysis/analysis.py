import pandas as pd
import os

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Function to ensure a directory exists
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to capitalize the first letter of each word for English words
def capitalize_first_letter(text):
    if isinstance(text, str):
        # Only apply capitalization to English words and skip numerics and Devanagari script
        return ' '.join([word.title() if word.isascii() else word for word in text.split()])
    return text

# Base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Processed data directory
processed_data_dir = os.path.normpath(os.path.join(base_dir, '../../data/processed'))
results_dir = os.path.normpath(os.path.join(base_dir, '../../results'))

# Ensure the processed data and results directories exist
ensure_directory_exists(processed_data_dir)
ensure_directory_exists(results_dir)

# File paths
file_path_final_fuzzy = os.path.join(results_dir, 'Final_Fuzzy_Matches.csv')
file_path_preprocessed_a3 = os.path.join(processed_data_dir, 'preprocessed_after_A_3.csv')
file_path_preprocessed_b2 = os.path.join(processed_data_dir, 'preprocessed_after_B_2.csv')
output_file_path_complete_match = os.path.join(results_dir, 'Complete_match.csv')
output_file_path_df5 = os.path.join(results_dir, 'Final_Processed_Matches.csv')
output_file_path_df6 = os.path.join(results_dir, 'Filtered_Processed_Matches.csv')

# Load the dataframes
df1 = pd.read_csv(file_path_final_fuzzy)
df2 = pd.read_csv(file_path_preprocessed_a3)
df3 = pd.read_csv(file_path_preprocessed_b2)

# Check the shape and first few rows of the dataframe
print("Shape of df1:", df1.shape)
print("First few rows of df1:")
print(df1.head())

# Filter the dataframe for the specified Match_Type values and Fuzzy_match_score
filtered_match_type = 'District: complete, School level: no match, Root name: complete'
df6 = df1[(df1['Match_Type'] == filtered_match_type) & (df1['Fuzzy_match_score'] == 2.5)]
print("Shape of df6:", df6.shape)
print("First few rows of df6:")
print(df6.head())

# Save the filtered matches to a new CSV file
df6.to_csv(output_file_path_df6, index=False)
print(f"Filtered matches saved to: {output_file_path_df6}")

# Merge df6 with df2 to get additional columns from df2
merged_a = pd.merge(df6, df2, left_on='school_id', right_on='school_id', suffixes=('', '_df2'))

# Merge the result with df3 to get additional columns from df3
merged_b = pd.merge(merged_a, df3, left_on='school_id_B', right_on='school_id', suffixes=('', '_df3'))

# Create the new dataframe df5 with the specified columns
df5 = pd.DataFrame()

# For B (columns from df3)
df5['school_id_B'] = merged_b['school_id_B']
df5['school_name_B'] = merged_b['name_df3']
df5['province_id_B'] = merged_b['province_id']
df5['province_B'] = merged_b['province'].str.replace('province', '').str.strip()
df5['local_level_id_B'] = merged_b['local_level_id']
df5['district_id_B'] = merged_b['district_id']
df5['location_B'] = merged_b['location']
df5['local_level_B'] = merged_b['local_level']
df5['district_B'] = merged_b['district']

# For A (columns from df2)
df5['school_id_A'] = merged_b['school_id']
df5['school_name_A'] = merged_b['School_name'] + ' ' + merged_b['School_level']
df5['school_A'] = merged_b['school']
df5['extracted_district_A'] = merged_b['Potential_district']

# For matching
df5['Fuzzy_match_score'] = merged_b['Fuzzy_match_score']
df5['Match_Type'] = merged_b['Match_Type']

# Apply capitalization to the relevant columns
columns_to_capitalize = [
    'school_name_B', 'province_B', 'local_level_B', 'district_B', 'school_name_A', 'school_A', 'extracted_district_A', 'location_B'
]

for column in columns_to_capitalize:
    df5[column] = df5[column].apply(capitalize_first_letter)

# Reorder the columns
df5 = df5[[
    'school_id_A', 'school_id_B', 'school_A', 'school_name_B','school_name_A', 
    'extracted_district_A', 'district_id_B','district_B', 
    'province_id_B', 'province_B', 
    'local_level_id_B', 'location_B', 'local_level_B'
]]

# Save the new dataframe to a CSV file
df5.to_csv(output_file_path_df5, index=False)
print(f"Final processed matches saved to: {output_file_path_df5}")

# Print the first few rows of the new dataframe
print("First few rows of df5:")
df5.head()
df6.head(100)


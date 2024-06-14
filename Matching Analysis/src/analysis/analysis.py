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
file_path_preprocessed_a3 = os.path.join(processed_data_dir, 'preprocessed_after_fuzzy_second_A.csv')
file_path_preprocessed_b2 = os.path.join(processed_data_dir, 'preprocessed_after_fuzzy_second_A')
output_file_path_complete_match = os.path.join(results_dir, 'Complete_match.csv')
output_file_path_df5 = os.path.join(results_dir, 'Final_Processed_Matches.csv')

# Load the dataframes
df1 = pd.read_csv(file_path_final_fuzzy)
df2 = pd.read_csv(file_path_preprocessed_a3)
df3 = pd.read_csv(file_path_preprocessed_b2)

# Check the shape and first few rows of the dataframe
print("Shape of df1:", df1.shape)
print("First few rows of df1:")
print(df1.head())gig

# Filter the dataframe for the specified Match_Type values and Fuzzy_match_score
filtered_match_type = 'District: complete, School level: no match, Root name: complete'
df4 = df1[(df1['Match_Type'] == filtered_match_type) & (df1['Fuzzy_match_score'] == 2.5)]
print("Shape of df4:", df4.shape)
print("First few rows of df4:")
print(df4.head())

# Save the filtered matches to a new CSV file
df4.to_csv(output_file_path_complete_match, index=False)
print(f"Filtered matches saved to: {output_file_path_complete_match}")

# Merge df4 with df2 to get additional columns from df2
merged_a = pd.merge(df4, df2, left_on='school_id', right_on='school_id', suffixes=('', '_df2'))

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

# Check if 'school_levels' column exists in the merged dataframe
if 'school_levels_df3' in merged_b.columns:
    df5['school_levels'] = merged_b['school_levels_df3']
else:
    df5['school_levels'] = None

# Apply capitalization to the relevant columns
columns_to_capitalize = [
    'school_name_B', 'province_B', 'local_level_B', 'district_B', 'school_name_A', 'school_A', 'extracted_district_A', 'location_B'
]

for column in columns_to_capitalize:
    df5[column] = df5[column].apply(capitalize_first_letter)

# Reorder the columns
df5 = df5[[
    'school_id_A', 'school_id_B', 'school_A', 'school_name_B', 'school_name_A', 
    'extracted_district_A', 'district_id_B', 'district_B', 
    'province_id_B', 'province_B', 
    'local_level_id_B', 'location_B', 'local_level_B', 'school_levels'
]]

# Save the new dataframe to a CSV file
df5.to_csv(output_file_path_df5, index=False)
print(f"Final processed matches saved to: {output_file_path_df5}")

# Print the first few rows of the new dataframe
print("First few rows of df5:")
print(df5.head())

# Print the count of missing values in each column
print("Count of missing values in each column:")
print(df5.isna().sum())

# Check for missing entries in school levels
print("Missing entries in school levels:")
missing_school_levels = df5[df5['school_levels'].isna()]
print(missing_school_levels[['school_id_A', 'school_id_B', 'school_levels']].head(100))

# Find the intersection between df3 and df5 based on school_id and school_id_B
intersection_df = pd.merge(df3, df5[['school_id_B']], left_on='school_id', right_on='school_id_B')

# Drop the 'school_id_B' column from the intersection dataframe
intersection_df = intersection_df.drop(columns=['school_id_B'])

# Print the first 10 rows of the intersection dataframe
print("Intersection based on school_id and school_id_B:")
intersection_df.head(10)
intersection_df.shape
intersection_df.columns
intersection_df['school_levels'].head(10)
intersection_df.isna().sum()

# Save the intersection dataframe to a CSV file
output_file_path_intersection = os.path.join(results_dir, 'Intersection_Matches.csv')
intersection_df.to_csv(output_file_path_intersection, index=False)
print(f"Intersection matches saved to: {output_file_path_intersection}")

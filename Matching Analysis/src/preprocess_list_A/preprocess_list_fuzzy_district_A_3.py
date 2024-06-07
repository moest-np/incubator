import pandas as pd
from fuzzywuzzy import process
import os

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

# Function to ensure a directory exists
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Processed data directory
processed_data_dir = os.path.normpath(os.path.join(base_dir, '../../data/processed'))

# Raw data directory
raw_data_dir = os.path.normpath(os.path.join(base_dir, '../../data/raw'))

# Ensure the processed data directory exists
ensure_directory_exists(processed_data_dir)

# File paths
file_path_aa_transliterated = os.path.join(processed_data_dir, 'preprocessed_after_A_2.csv')
file_path_bb = os.path.join(raw_data_dir, 'school_list_B.tsv')
output_file_path = os.path.join(processed_data_dir, 'preprocessed_after_A_3.csv')

# Load the transliterated CSV file
df_aa_transliterated = pd.read_csv(file_path_aa_transliterated)
df_aa_transliterated = df_aa_transliterated.fillna('')

# Load the newly provided CSV file
df_bb = pd.read_csv(file_path_bb, delimiter='\t')
df_bb = df_bb.fillna('')

# Get unique values from 'district' column in df_bb
unique_districts_bb = df_bb['district'].unique()

# Function to get the best fuzzy match and match percentage
def get_best_match(word, choices):
    best_match = process.extractOne(word, choices, scorer=process.fuzz.token_sort_ratio)
    return best_match

# Function to fill empty columns based on fuzzy matching
def fill_empty_columns(row):
    if row['Location_transliterated'] == '':
        words = row['school_1_transliterated'].split()
        for word in words:
            match = get_best_match(word, unique_districts_bb)
            if match and match[1] > 60:  # Only consider good matches
                row['Location_transliterated'] = match[0]
                row['Potential_district_transliterated'] = match[0]
                break  # Stop after finding the first good match
    return row

# Apply the function to the DataFrame
df_aa_transliterated = df_aa_transliterated.apply(fill_empty_columns, axis=1)

# Check the number of empty entries in each column
empty_entries_count = df_aa_transliterated.apply(lambda column: (column == '').sum())
print("Number of empty entries in each column:")
print(empty_entries_count)

# Print rows where 'Location_transliterated' is still empty
empty_loc_rows = df_aa_transliterated[df_aa_transliterated['Location_transliterated'] == '']
print(f"Number of rows with empty 'Location_transliterated': {len(empty_loc_rows)}")
empty_loc_rows.tail(10)

# Function to count empty entries in each column
def count_empty_entries(column):
    return (column == '').sum()

# Apply the function to each column
empty_entries_count = df_aa_transliterated.apply(count_empty_entries)
print(f"Empty entries count: {len(empty_entries_count)}")
print(empty_entries_count)

# Print rows where 'School_level' is empty
empty_loc_rows = df_aa_transliterated[df_aa_transliterated['Location_transliterated'] == '']
print(f"Number of rows with empty 'Location_transliterated': {len(empty_loc_rows)}")
empty_loc_rows.tail(100)

# Remove rows where 'Location_transliterated' is empty
df_aa_transliterated = df_aa_transliterated[df_aa_transliterated['Location_transliterated'] != '']

# Define the mapping for replacements
transliteration_map = {
    'sya~naja': 'Syangja',
    'sya~nja': 'Syangja',
    'kabhre': 'Kavrepalanchok',
    'rukuma': 'Rukum',
    'saya~naja': 'Syangja'
}

# Replace values in the Potential_district_transliterated column
df_aa_transliterated['Potential_district_transliterated'] = df_aa_transliterated['Potential_district_transliterated'].replace(transliteration_map)

# Update the Matched_district column based on changes in Potential_district_transliterated
df_aa_transliterated['Matched_district'] = df_aa_transliterated['Potential_district_transliterated']

# Apply fuzzy matching to create new columns 'Matched_district' and 'Match_percent'
matches = df_aa_transliterated['Matched_district'].apply(
    lambda x: get_best_match(x, unique_districts_bb) if pd.notnull(x) else ('', 0)
)
df_aa_transliterated['Matched_District'] = matches.apply(lambda x: x[0])
df_aa_transliterated['Match_percent'] = matches.apply(lambda x: x[1])

# Print the range of the Match_percent column
match_percent_range = df_aa_transliterated['Match_percent'].min(), df_aa_transliterated['Match_percent'].max()
print("Range of Match_percent:", match_percent_range)

# Print the rows where Match_percent is less than 60
low_match_rows = df_aa_transliterated[df_aa_transliterated['Match_percent'] <  60]
low_match_rows[['Potential_district_transliterated', 'Matched_District', 'Match_percent']].head()

# Get top 20 frequent values in 'Potential_district_transliterated' column
top_20_frequent = low_match_rows['Potential_district_transliterated'].value_counts().head(20)

# Print the top 20 frequent values
print("Top 20 frequent values in 'Potential_district_transliterated':")
print(top_20_frequent)

# Remove rows where Match_percent is less than 60
df_aa_transliterated = df_aa_transliterated[df_aa_transliterated['Match_percent'] >= 60]

# Drop the Match_percent column
df_aa_transliterated.drop(columns=['Match_percent'], inplace=True)

# Reorder the columns
df_aa_transliterated = df_aa_transliterated[[
    'school_id', 'school', 'school_transliterated', 'school_1', 'school_1_transliterated', 'School_name', 
    'School_name_transliterated', 'School_level', 'School_level_transliterated', 
    'School_level_transliterated_categorized', 'Location', 'Location_transliterated', 
    'Potential_district', 'Potential_district_transliterated', 'Location_1', 'Matched_district', 
    'Matched_District', 'Location_1_transliterated'
]]

# Save the updated dataframe to a new CSV file
df_aa_transliterated.to_csv(output_file_path, index=False)
print("Updated dataframe saved to:", output_file_path)

# Print the first 10 rows of the updated dataframe
print("First 10 rows of the updated dataframe:")
print(df_aa_transliterated.head(10))
df_aa_transliterated.head(10)












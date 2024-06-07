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
results_dir = os.path.normpath(os.path.join(base_dir, '../../results'))

# Ensure the processed data and results directories exist
ensure_directory_exists(processed_data_dir)
ensure_directory_exists(results_dir)

# File paths
file_path_fuzzy_second_a = os.path.join(processed_data_dir, 'preprocessed_after_fuzzy_second_A.csv')
file_path_fuzzy_second_b = os.path.join(processed_data_dir, 'preprocessed_after_fuzzy_second_B.csv')
output_file_path_final_fuzzy_matches = os.path.join(results_dir, 'Final_Fuzzy_Matches.csv')

# Load the dataframes
df_Fuzzy_A = pd.read_csv(file_path_fuzzy_second_a)
df_Fuzzy_B = pd.read_csv(file_path_fuzzy_second_b)

# Rename column in df_Fuzzy_B
df_Fuzzy_B = df_Fuzzy_B.rename(columns={'school_id': 'school_id_B'})

# Replace null values by empty strings in both dataframes
df_Fuzzy_B = df_Fuzzy_B.fillna('')
df_Fuzzy_A = df_Fuzzy_A.fillna('')

# Change all columns to string dtype, convert to lowercase, and strip leading/trailing spaces
df_Fuzzy_A = df_Fuzzy_A.astype(str).applymap(lambda x: x.lower().strip())
df_Fuzzy_B = df_Fuzzy_B.astype(str).applymap(lambda x: x.lower().strip())

# Function to get match type and score
def get_match_type_and_score(value_a, value_b):
    value_a = str(value_a) if pd.notna(value_a) else ''
    value_b = str(value_b) if pd.notna(value_b) else ''
    if value_a == value_b:
        return 'complete', 1
    else:
        return 'no match', 0



# Function to perform weighted fuzzy matching
def get_fuzzy_match_score(row_a, row_b):
    total_score = 0
    match_types = []

    # District match
    district_match_type, district_score = get_match_type_and_score(row_a['district_id'], row_b['district_id'])
    if district_match_type == 'complete':
        district_score *= 0.5
    else:
        district_score = 0  # No match
    total_score += district_score
    match_types.append(f"District: {district_match_type}")

    # School level match
    school_level_a = row_a['School_level_transliterated_categorized']
    school_level_b = row_b['school_levels_categorized']

    if pd.isna(school_level_a) or school_level_a == '' or pd.isna(school_level_b) or school_level_b == '':
        school_level_match_type = 'no match'
        school_level_score = 0.0
    else:
        school_level_match_type, school_level_score = get_match_type_and_score(school_level_a, school_level_b)
        if school_level_match_type == 'complete':
            school_level_score *= 0.5
        else:
            school_level_score = 0  # No match

    total_score += school_level_score
    match_types.append(f"School level: {school_level_match_type}")

    # Root name match
    root_name_a = str(row_a['School_name_transliterated']) if pd.notna(row_a['School_name_transliterated']) else ''
    root_name_b = str(row_b['root_school_name']) if pd.notna(row_b['root_school_name']) else ''
    root_name_score = fuzz.ratio(root_name_a, root_name_b)
    if root_name_score >= 80:
        root_name_score = 2  # Complete match
        match_type = 'complete'
    elif root_name_score >= 50:
        root_name_score = 1  # Partial match
        match_type = 'partial'
    else:
        root_name_score = 0
        match_type = 'no match'
    total_score += root_name_score
    match_types.append(f"Root name: {match_type}")

    return total_score, ', '.join(match_types)

# Function to process and save batches
def process_and_save_batch(start_idx, end_idx, batch_num):
    matches = []
    for idx_a, row_a in df_Fuzzy_A.iloc[start_idx:end_idx].iterrows():
        best_score = 0
        best_match = None
        best_match_type = []

        for idx_b, row_b in df_Fuzzy_B.iterrows():
            match_score, match_type = get_fuzzy_match_score(row_a, row_b)
            if match_score > best_score:
                best_score = match_score
                best_match = row_b
                best_match_type = match_type

        if best_match is not None:
            match = list(row_a) + list(best_match) + [best_score, best_match_type]
            matches.append(match)
        else:
            match = list(row_a) + [None] * len(df_Fuzzy_B.columns) + [0, 'No Match']
            matches.append(match)

    # Create a dataframe from the matches
    columns = list(df_Fuzzy_A.columns) + list(df_Fuzzy_B.columns) + ['Fuzzy_match_score', 'Match_Type']
    df_matches = pd.DataFrame(matches, columns=columns)

    # Filter the DataFrame to keep only the specified columns
    columns_to_keep = [
        'school_id', 'school_1', 'school_id_B', 'name', 'district_id', 'Matched_District', 'root_school_name', 'School_name_transliterated',
        'School_level', 'school_levels', 'School_name', 'Fuzzy_match_score', 'Match_Type'
    ]
    df_matches = df_matches[columns_to_keep]

    # Sort the matches by Fuzzy_match_score
    df_matches = df_matches.sort_values(by='Fuzzy_match_score', ascending=False)

    # Save the batch to a CSV file
    if batch_num == 0:
        df_matches.to_csv(output_file_path_final_fuzzy_matches, index=False)
    else:
        df_matches.to_csv(output_file_path_final_fuzzy_matches, mode='a', header=False, index=False)

    print(f"Batch {batch_num} processed and saved.")

# Process data in batches
batch_size = 2
start_from_index = 18449
num_batches = (len(df_Fuzzy_A) - start_from_index + batch_size - 1) // batch_size  # Calculate the number of batches

for batch_num in range(num_batches):
    start_idx = start_from_index + batch_num * batch_size
    end_idx = min(start_from_index + (batch_num + 1) * batch_size, len(df_Fuzzy_A))
    process_and_save_batch(start_idx, end_idx, batch_num + (start_from_index // batch_size))

print("Processing completed.")

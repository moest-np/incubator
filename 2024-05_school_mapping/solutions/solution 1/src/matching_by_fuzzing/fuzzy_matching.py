import pandas as pd
import os
from fuzzywuzzy import fuzz

# Set display options
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def ensure_directory_exists(directory):
    """Ensure a directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_dataframe(file_path):
    """Load a dataframe from a CSV file."""
    return pd.read_csv(file_path)

def rename_and_filter_columns(df_A, df_B):
    """Rename and filter columns for the two dataframes."""
    df_A = df_A.rename(columns={
        'school_id': 'school_id_A',
        'school_name_transliterate': 'root_school_name_A',
        'school_level_transliterate': 'school_level_A',
        'matched_district': 'district_A'
    })[['school_id_A', 'root_school_name_A', 'school_level_A', 'district_A']]

    df_B = df_B.rename(columns={
        'school_id': 'school_id_B',
        'modified_name_root': 'root_school_name_B',
        'modified_name_school_level': 'school_level_B',
        'modified_old_name1_root': 'root_school_old_name1_B',
        'modified_old_name2_root': 'root_school_old_name2_B',
        'modified_old_name2_school_level': 'school_level_old_name2_B',
        'modified_old_name1_school_level': 'school_level_old_name1_B',
        'district': 'district_B'
    })[['school_id_B', 'root_school_name_B', 'school_level_B', 'root_school_old_name1_B', 
        'root_school_old_name2_B', 'school_level_old_name2_B', 'school_level_old_name1_B', 'district_B']]
    
    return df_A, df_B

def normalize_and_clean(df):
    """Normalize text columns and handle duplicates, filling NaN values with empty strings."""
    # Convert text columns to lowercase and strip leading/trailing spaces
    df = df.apply(lambda x: x.str.lower().str.strip() if x.dtype == "object" else x)
    
    # Drop duplicates
    df = df.drop_duplicates()
    
    # Fill NaN values with empty strings
    df = df.fillna('')
    
    return df

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
    district_match_type, district_score = get_match_type_and_score(row_a['district_A'], row_b['district_B'])
    if district_match_type == 'complete':
        district_score *= 0.5
    else:
        district_score = 0  # No match
    total_score += district_score
    match_types.append(f"District: {district_match_type}")

    # School level match
    school_level_a = row_a['school_level_A']
    school_level_values_b = [row_b['school_level_B'], row_b['school_level_old_name1_B'], row_b['school_level_old_name2_B']]

    if pd.isna(school_level_a) or school_level_a == '' or all(pd.isna(school_level_b) or school_level_b == '' for school_level_b in school_level_values_b):
        school_level_match_type = 'no match'
        school_level_score = 0.0
    else:
        school_level_match_type, school_level_score = get_match_type_and_score(school_level_a, school_level_values_b[0])
        if school_level_match_type == 'complete':
            school_level_score *= 0.5
        else:
            school_level_score = 0  # No match

    total_score += school_level_score
    match_types.append(f"School level: {school_level_match_type}")

    # Root name match
    root_name_a = str(row_a['root_school_name_A']) if pd.notna(row_a['root_school_name_A']) else ''
    root_name_b = str(row_b['root_school_name_B']) if pd.notna(row_b['root_school_name_B']) else ''
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

def save_intermediate_results(df_all_matches, output_dir):
    # Save final_fuzzy_matching
    final_fuzzy_matching_path = os.path.join(output_dir, 'final_fuzzy_matching.csv')
    df_all_matches.to_csv(final_fuzzy_matching_path, index=False)

    # Save complete matches
    complete_matches = df_all_matches[df_all_matches['Fuzzy_match_score'] == 3]
    complete_matches_path = os.path.join(output_dir, 'complete_match.csv')
    complete_matches.to_csv(complete_matches_path, index=False)

    # Save remaining after complete matches
    remaining_after_complete_matches = df_all_matches[df_all_matches['Fuzzy_match_score'] != 3]
    remaining_after_complete_matches_path = os.path.join(output_dir, 'remaining_after_complete_match.csv')
    remaining_after_complete_matches.to_csv(remaining_after_complete_matches_path, index=False)

    # Save preprocessed_after_fuzzy_A
    unmatched_school_ids_A = set(df_A['school_id_A']) - set(complete_matches['school_id_A'])
    preprocessed_after_fuzzy_A = df_A[df_A['school_id_A'].isin(unmatched_school_ids_A)]
    preprocessed_after_fuzzy_A_path = os.path.join(output_dir, 'preprocessed_after_fuzzy_A.csv')
    preprocessed_after_fuzzy_A = preprocessed_after_fuzzy_A.merge(df_all_matches[['school_id_A', 'Fuzzy_match_score']], on='school_id_A', how='left')
    preprocessed_after_fuzzy_A.to_csv(preprocessed_after_fuzzy_A_path, index=False)

    # Save preprocessed_after_fuzzy_B
    unmatched_school_ids_B = set(df_B['school_id_B']) - set(complete_matches['school_id_B'])
    preprocessed_after_fuzzy_B = df_B[df_B['school_id_B'].isin(unmatched_school_ids_B)]
    preprocessed_after_fuzzy_B_path = os.path.join(output_dir, 'preprocessed_after_fuzzy_B.csv')
    preprocessed_after_fuzzy_B = preprocessed_after_fuzzy_B.merge(df_all_matches[['school_id_B', 'Fuzzy_match_score']], on='school_id_B', how='left')
    preprocessed_after_fuzzy_B.to_csv(preprocessed_after_fuzzy_B_path, index=False)

def process_and_save_batch(start_idx, end_idx, batch_num, df_A, df_B, matched_ids_B, output_dir, df_all_matches):
    matches = []
    for idx_a, row_a in df_A.iloc[start_idx:end_idx].iterrows():
        best_score = 0
        best_match = None
        best_match_type = []

        for idx_b, row_b in df_B.iterrows():
            if row_b['school_id_B'] in matched_ids_B:
                continue

            match_score, match_type = get_fuzzy_match_score(row_a, row_b)
            if match_score > best_score:
                best_score = match_score
                best_match = row_b
                best_match_type = match_type

        if best_match is not None:
            match = list(row_a) + list(best_match) + [best_score, best_match_type]
            matches.append(match)
        else:
            match = list(row_a) + [None] * len(df_B.columns) + [0, 'No Match']
            matches.append(match)

    # Create a dataframe from the matches
    columns = list(df_A.columns) + list(df_B.columns) + ['Fuzzy_match_score', 'Match_Type']
    df_matches = pd.DataFrame(matches, columns=columns)

    # Filter the DataFrame to keep only the specified columns
    columns_to_keep = [
        'school_id_A','school_id_B', 'root_school_name_A','root_school_name_B', 'school_level_A',  'school_level_B',  'district_A',
        'district_B',
        'Fuzzy_match_score', 'Match_Type'
    ]
    df_matches = df_matches[columns_to_keep]

    # Sort the matches by Fuzzy_match_score
    df_matches = df_matches.sort_values(by='Fuzzy_match_score', ascending=False)

    # Save the batch to a CSV file
    final_fuzzy_matching_path = os.path.join(output_dir, 'final_fuzzy_matching.csv')
    if batch_num == 0:
        df_matches.to_csv(final_fuzzy_matching_path, index=False)
    else:
        df_matches.to_csv(final_fuzzy_matching_path, mode='a', header=False, index=False)

    print(f"Batch {batch_num} processed and saved.")

    df_all_matches = pd.concat([df_all_matches, df_matches], ignore_index=True)

    # Add school IDs from df_B that had a perfect match to the set of matched IDs
    perfect_matches = df_matches[df_matches['Fuzzy_match_score'] == 3]
    matched_ids_B.update(perfect_matches['school_id_B'])

    # Save intermediate results after each batch
    save_intermediate_results(df_all_matches, output_dir)

    return df_all_matches

if __name__ == "__main__":
    # Base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Processed data directory
    processed_data_dir = os.path.normpath(os.path.join(base_dir, '../../data/processed'))
    output_dir = '/Users/mahesh/Documents/GitHub/incubator/Matching Analysis/results'

    # Ensure the processed data directory and output directory exist
    ensure_directory_exists(processed_data_dir)
    ensure_directory_exists(output_dir)

    # File paths
    file_path_a = os.path.join(processed_data_dir, 'preprocessed_after_A.csv')
    file_path_b = os.path.join(processed_data_dir, 'preprocessed_after_B.csv')

    # Load the dataframes
    df_A = load_dataframe(file_path_a)
    df_B = load_dataframe(file_path_b)

    # Rename and filter columns
    df_A, df_B = rename_and_filter_columns(df_A, df_B)

    # Normalize and clean dataframes
    df_A = normalize_and_clean(df_A)
    df_B = normalize_and_clean(df_B)

    # Example usage for batch processing
    batch_size = 2
    start_from_index = 0
    num_batches = (len(df_A) - start_from_index + batch_size - 1) // batch_size  # Calculate the number of batches

    df_all_matches = pd.DataFrame()
    matched_ids_B = set()
    for batch_num in range(num_batches):
        start_idx = start_from_index + batch_num * batch_size
        end_idx = min(start_from_index + (batch_num + 1) * batch_size, len(df_A))
        df_all_matches = process_and_save_batch(start_idx, end_idx, batch_num, df_A, df_B, matched_ids_B, output_dir, df_all_matches)

    print("Processing completed.")

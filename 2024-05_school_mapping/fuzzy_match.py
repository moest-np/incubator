import pandas as pd
from fuzzywuzzy import process, fuzz
import time

# Load the dataframes
df_Fuzzy_A = pd.read_csv('Fuzzy_A.csv')
df_Fuzzy_B = pd.read_csv('Fuzzy_B.csv')

# Convert all text columns to lowercase and strip leading/trailing spaces
df_Fuzzy_A['Potential_School_Name_transliterated'] = df_Fuzzy_A['Potential_School_Name_transliterated'].str.lower().str.strip()
df_Fuzzy_A['Assigned_District_Name'] = df_Fuzzy_A['Assigned_District_Name'].str.lower().str.strip()
df_Fuzzy_B['location'] = df_Fuzzy_B['location'].str.lower().str.strip()
df_Fuzzy_B['district'] = df_Fuzzy_B['district'].str.lower().str.strip()
df_Fuzzy_B['modified_name_transliterated'] = df_Fuzzy_B['modified_name_transliterated'].str.lower().str.strip()

# Define a function to perform fuzzy matching with a timeout
def get_best_fuzzy_match_timeout(name, choices, timeout=5):
    if pd.isna(name):
        return None, 0
    start_time = time.time()
    best_match = None
    highest_score = 0
    for choice in choices:
        if time.time() - start_time > timeout:
            break
        score = fuzz.ratio(name, choice)
        if score > highest_score:
            highest_score = score
            best_match = choice
    return best_match, highest_score

# Process each row in df_Fuzzy_A to find the best match in df_Fuzzy_B
matches = []
for idx, row in df_Fuzzy_A.iterrows():
    best_match_name, name_score = get_best_fuzzy_match_timeout(row['Potential_School_Name_transliterated'], df_Fuzzy_B['modified_name_transliterated'])
    if best_match_name:
        matched_row = df_Fuzzy_B[df_Fuzzy_B['modified_name_transliterated'] == best_match_name].iloc[0]
        district_match = fuzz.ratio(row['Assigned_District_Name'], matched_row['district'])
        total_score = (name_score + district_match) / 2  # Averaging the scores for simplicity
        matches.append([
            row['school_id'],
            matched_row['school_id'],
            row['Potential_School_Name_transliterated'],
            matched_row['modified_name_transliterated'],
            matched_row['district'],
            row['Assigned_District_Name'],
            total_score
        ])
    else:
        matches.append([
            row['school_id'],
            None,
            row['Potential_School_Name_transliterated'],
            None,
            None,
            row['Assigned_District_Name'],
            0
        ])

# Create a dataframe from the matches
columns = ['school_id_A', 'school_id_B', 'Potential_School_Name_transliterated', 'modified_name_transliterated', 'district', 'Assigned_District_Name', 'Fuzzy_match_score']
df_matches = pd.DataFrame(matches, columns=columns)

# Save the processed dataframe to a CSV file
df_matches.to_csv('df_Fuzzy_Matches.csv', index=False)

print("Fuzzy matching complete. The results are saved in 'df_Fuzzy_Matches.csv'.")

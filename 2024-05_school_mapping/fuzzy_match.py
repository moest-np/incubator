import pandas as pd
from fuzzywuzzy import fuzz

# Load the dataframes
df_Fuzzy_A = pd.read_csv('Fuzzy_A.csv')
df_Fuzzy_B = pd.read_csv('Fuzzy_B.csv')

# Convert relevant text columns to lowercase and strip leading/trailing spaces
df_Fuzzy_A['Potential_School_Name_transliterated'] = df_Fuzzy_A['Potential_School_Name_transliterated'].str.lower().str.strip()
df_Fuzzy_A['district_A'] = df_Fuzzy_A['district_A'].str.lower().str.strip()
df_Fuzzy_B['modified_name_transliterated'] = df_Fuzzy_B['modified_name_transliterated'].str.lower().str.strip()
df_Fuzzy_B['district'] = df_Fuzzy_B['district'].str.lower().str.strip()

# Function to get match type and score
def get_match_type_and_score(value_a, value_b):
    value_a = str(value_a) if pd.notna(value_a) else ''
    value_b = str(value_b) if pd.notna(value_b) else ''
    if value_a == value_b:
        return 'complete', 1
    elif fuzz.partial_ratio(value_a, value_b) > 80:
        return 'partial', 0.5
    else:
        return 'no match', 0

# Function to perform weighted fuzzy matching
def get_fuzzy_match_score(row_a, row_b):
    total_score = 0
    match_types = []

    # District match
    district_match_type, district_score = get_match_type_and_score(row_a['district_A'], row_b['district'])
    if district_match_type == 'complete':
        district_score *= 0.5
    elif district_match_type == 'partial':
        district_score *= 0.2
    total_score += district_score
    match_types.append(f"District: {district_match_type}")

    # School level match
    school_level_match_type, school_level_score = get_match_type_and_score(row_a['School_level_A'], row_b['School_level_B'])
    if school_level_match_type == 'complete':
        school_level_score *= 0.5
    elif school_level_match_type == 'partial':
        school_level_score *= 0.2
    total_score += school_level_score
    match_types.append(f"School level: {school_level_match_type}")

    # Root name match
    root_name_a = str(row_a['Root_name_A']) if pd.notna(row_a['Root_name_A']) else ''
    root_name_b = str(row_b['Root_name_B']) if pd.notna(row_b['Root_name_B']) else ''
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

# Process each row in df_Fuzzy_A to find the best match in df_Fuzzy_B
matches = []
for idx_a, row_a in df_Fuzzy_A.iterrows():
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
        matches.append([
            row_a['school_id'],
            best_match['school_id'],
            row_a['Potential_School_Name_transliterated'],
            best_match['modified_name_transliterated'],
            best_match['district'],
            row_a['district_A'],
            best_score,
            best_match_type
        ])
    else:
        matches.append([
            row_a['school_id'],
            None,
            row_a['Potential_School_Name_transliterated'],
            None,
            None,
            row_a['district_A'],
            0,
            'No Match'
        ])

# Create a dataframe from the matches
columns = ['school_id_A', 'school_id_B', 'Potential_School_Name_transliterated', 'modified_name_transliterated', 'district', 'district_A', 'Fuzzy_match_score', 'Match_Type']
df_matches = pd.DataFrame(matches, columns=columns)

# Sort the matches by Fuzzy_match_score
df_matches = df_matches.sort_values(by='Fuzzy_match_score', ascending=False)
df_matches.head()
# Save the processed dataframe to a CSV file
df_matches.to_csv('df_Fuzzy_Matches.csv', index=False)

print("Matching complete. The results are saved in 'df_Fuzzy_Matches.csv'.")









import pandas as pd
from fuzzywuzzy import process, fuzz

# Load the dataframes
df_Fuzzy_A = pd.read_csv('Fuzzy_A.csv')
df_Fuzzy_B = pd.read_csv('Fuzzy_B.csv')

# Convert relevant text columns to lowercase and strip leading/trailing spaces
df_Fuzzy_A['district_A'] = df_Fuzzy_A['district_A'].str.lower().str.strip()
df_Fuzzy_B['district'] = df_Fuzzy_B['district'].str.lower().str.strip()

# Perform fuzzy matching between district_A and district
def get_best_fuzzy_match(name, choices):
    if pd.isna(name):
        return None, 0
    best_match = process.extractOne(name, choices, scorer=fuzz.ratio)
    return best_match[0], best_match[1]

df_Fuzzy_A['assigned_district_from_b'], df_Fuzzy_A['percentage'] = zip(*df_Fuzzy_A['district_A'].apply(
    lambda x: get_best_fuzzy_match(x, df_Fuzzy_B['district'].unique())
))


pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows',None)
df_Fuzzy_A.tail(5)






import pandas as pd

# Load the dataframes
df_Fuzzy_A = pd.read_csv('Fuzzy_A.csv')
df_Fuzzy_B = pd.read_csv('Fuzzy_B.csv')

# Convert relevant text columns to lowercase and strip leading/trailing spaces
df_Fuzzy_A['Potential_School_Name_transliterated'] = df_Fuzzy_A['Potential_School_Name_transliterated'].str.lower().str.strip()
df_Fuzzy_B['modified_name_transliterated'] = df_Fuzzy_B['modified_name_transliterated'].str.lower().str.strip()

# Define the suffix categories
suffix_categories = {'a vi': 1, 'pra vi': 2, 'ma vi': 3}

# Function to categorize school names
def categorize_school_name(name, suffix_categories):
    for suffix, category in suffix_categories.items():
        if f" {suffix} " in f" {name} ":
            root_name = name.replace(suffix, '').strip()
            return root_name, category
    return name, 4  # Default category if no suffix matches

# Apply the categorization for df_Fuzzy_A
df_Fuzzy_A[['Root_name_A', 'School_level_A']] = df_Fuzzy_A['Potential_School_Name_transliterated'].apply(
    lambda x: pd.Series(categorize_school_name(x, suffix_categories))
)

# Apply the categorization for df_Fuzzy_B
df_Fuzzy_B[['Root_name_B', 'School_level_B']] = df_Fuzzy_B['modified_name_transliterated'].apply(
    lambda x: pd.Series(categorize_school_name(x, suffix_categories))
)

# Save the updated dataframes
df_Fuzzy_A.to_csv('Fuzzy_A.csv', index=False)
df_Fuzzy_B.to_csv('Fuzzy_B.csv', index=False)

print("Categorization complete. The updated dataframes have been saved.")


df_Fuzzy_B.dtypes
df_Fuzzy_A.head(10)
df_Fuzzy_B.head(10)


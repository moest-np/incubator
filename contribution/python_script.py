import pandas as pd
from difflib import SequenceMatcher

# Function to check if two strings have at least 4 consecutive letters in order
def get_similarity_score(str1, str2):
    if pd.isna(str1) or pd.isna(str2):
        return 0
    matcher = SequenceMatcher(None, str1, str2)
    match = matcher.find_longest_match(0, len(str1), 0, len(str2))
    if match.size >= 4:
        return matcher.ratio()
    return 0

# Load the datasets
print("Loading datasets...")
# Load the datasets with handling of missing values
df_A = pd.read_csv('school_list_A_with_english1.csv', sep='\t', quotechar='"', na_values=['', 'NA', 'N/A'])
df_B = pd.read_csv('school_list_B1.csv', sep='\t', quotechar='"', na_values=['', 'NA', 'N/A'])

print("Datasets loaded.")

# Create a list to store the matched rows and their similarity scores
matched_rows = []
matched_districts = []  # Initialize matched_districts list

# Iterate through each row in df_A and df_B to find matches based on district names and locations
print("Matching districts and locations...")
for _, row_A in df_A.iterrows():
    for _, row_B in df_B.iterrows():
        district_score = get_similarity_score(row_A['district_english'], row_B['district'])
        location_score = get_similarity_score(row_A['velthuis'], row_B['name'])
        if district_score >= 0.9 and location_score >= 0.01:
            # Combine the matched rows into a single dictionary and add the similarity score
            combined_row = {**row_A, **row_B, 'district_similarity_score': district_score, 'location_similarity_score': location_score}
            combined_row['score_name_and_velthuis'] = get_similarity_score(row_A['velthuis'], row_B['name'])  # Add similarity score between velthuis and name
            matched_rows.append(combined_row)
            matched_districts.append((row_A['district_english'], row_B['district'], district_score, row_A['velthuis'], row_B['name'], location_score))
            # Print log for the matched rows
            print(f"Matched: {row_A['district_english']} -> {row_B['district']} with score {district_score:.2f} | {row_A['velthuis']} -> {row_B['name']} with score {location_score:.2f}")

print("District and location matching completed.")

# Print the contents of the matched_districts list after the loop
print("Contents of matched_districts list:")
print(matched_districts)

# Convert the list of matched rows into a DataFrame
matched_df = pd.DataFrame(matched_rows)

# Save the matched rows to a new TSV file
print("Saving matched rows to matched_schools_google_colab.tsv...")
matched_df.to_csv('matched_schools_google_colab.tsv', sep='\t', index=False)
print("File saved successfully.")

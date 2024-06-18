import pandas as pd
import os

# Base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Results directory
results_dir = os.path.normpath(os.path.join(base_dir, '../../results'))

# File path for the Intersection_Matches.csv
file_path_intersection = os.path.join(results_dir, 'Intersection_Matches.csv')

# Load the intersection matches dataframe
intersection_df = pd.read_csv(file_path_intersection)

intersection_df.head()
# Check for duplicate rows
print("Duplicate rows in intersection_df:")
print(intersection_df[intersection_df.duplicated()].head(10))
print("Number of duplicate rows:", intersection_df.duplicated().sum())

# Remove duplicate rows
intersection_df = intersection_df.drop_duplicates()

# Check for duplicate rows again
print("Number of duplicate rows after dropping duplicates:", intersection_df.duplicated().sum())

# Define the replacement patterns and corresponding school level values
replacement_patterns = {
    r'\bma vi\b$': 'mavi',
    r'\bma\b$': 'mavi',
    r'\bs vi\b$': 'mavi',
    r'\bsec vi\b$': 'mavi',
    r'\bsec\b$': 'mavi',
    r'\ba\b$': 'avi',
    r'\ba v\b$': 'avi',
    r'\baa bi\b$': 'avi',
    r'\bbasic\b$': 'avi',
    r'\bdurga rastriya a bidhyalaya\b$': 'avi'
}

# Apply the replacement patterns to the 'modified_name' column and update 'school_levels'
for pattern, replacement in replacement_patterns.items():
    match_rows = intersection_df['modified_name'].notna() & intersection_df['modified_name'].str.contains(pattern, regex=True)
    intersection_df.loc[match_rows, 'school_levels'] = intersection_df.loc[match_rows, 'school_levels'].fillna('') + ' ' + replacement
    intersection_df.loc[match_rows, 'school_levels'] = intersection_df.loc[match_rows, 'school_levels'].str.strip()

# Strip 'mavi' and 'avi' from 'modified_name' and update 'root_school_name'
def remove_school_levels(text, levels):
    for level in levels:
        text = text.replace(level, '')
    return text.strip()

intersection_df['root_school_name'] = intersection_df.apply(lambda row: remove_school_levels(row['modified_name'], ['mavi', 'avi']) if pd.notna(row['modified_name']) else row['modified_name'], axis=1)

# Print the shape and first few rows of the updated dataframe
print("Shape of updated intersection_df:", intersection_df.shape)
print("First few rows of updated intersection_df:")
intersection_df.head(10)

# Check for missing values
print("Missing values in each column:")
print(intersection_df.isna().sum())


# # Save the updated dataframe to a CSV file
# output_file_path_updated = os.path.join(results_dir, 'Updated_Intersection_Matches.csv')
# intersection_df.to_csv(output_file_path_updated, index=False)
# print(f"Updated intersection matches saved to: {output_file_path_updated}")

# Print specific columns for rows with missing 'school_levels'
print("Rows with missing 'school_levels':")
intersection_df[['root_school_name', 'modified_name', 'name']][intersection_df['school_levels'].isna()].tail(45)

# Print the first few rows of the selected columns
print("Selected columns:")
print(intersection_df[['name', 'modified_name', 'school_levels']].head())

# Print rows where 'modified_name' contains 'ma vi'
print("Rows where 'modified_name' contains 'ma vi':")
print(intersection_df[intersection_df['modified_name'].notna() & intersection_df['modified_name'].str.contains('ma vi')].head())

# Print rows where 'modified_name' ends with 'ma vi'
print("Rows where 'modified_name' ends with 'ma vi':")
print(intersection_df[intersection_df['modified_name'].notna() & intersection_df['modified_name'].str.contains(r'\bma vi\b$', regex=True)].head())






intersection_df.head(10)
intersection_df.isna().sum()
intersection_df[intersection_df.duplicated()].head(10)
intersection_df.duplicated().sum()
intersection_df.columns
# Remove duplicate rows
intersection_df = intersection_df.drop_duplicates()
intersection_df.duplicated().sum()



# # Save the updated dataframe to a CSV file
# output_file_path_updated = os.path.join(results_dir, 'Updated_Intersection_Matches.csv')
# intersection_df.to_csv(output_file_path_updated, index=False)
# print(f"Updated intersection matches saved to: {output_file_path_updated}")


intersection_df[['root_school_name','modified_name','name']][intersection_df['school_levels'].isna()].tail(100)
intersection_df[intersection_df['school_levels'].isna()].shape
intersection_df[['name','modified_name','school_levels']].head()

intersection_df[intersection_df['modified_name'].notna() & intersection_df['modified_name'].str.contains('ma vi')].head()
intersection_df[intersection_df['modified_name'].notna() & intersection_df['modified_name'].str.contains(r'\bma vi\b$', regex=True)]


intersection_df.shape

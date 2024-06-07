import pandas as pd
import re
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import os

# Function to ensure a directory exists
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Raw and processed data directories
raw_data_dir = os.path.normpath(os.path.join(base_dir, '../../data/raw'))
processed_data_dir = os.path.normpath(os.path.join(base_dir, '../../data/processed'))

# Ensure the processed data directory exists
ensure_directory_exists(processed_data_dir)

# File paths
file_path = os.path.join(processed_data_dir, 'preprocessed_after_A_1.csv')
output_file_path = os.path.join(processed_data_dir, 'preprocessed_after_A_2.csv')

# Load the provided CSV file
df = pd.read_csv(file_path)

# Replace NaN values with empty strings
df = df.fillna('')

# Function to clean the transliterated text
def clean_text(text):
    text = text.lower()  # Convert to lowercase
    text = text.strip()  # Remove leading and trailing spaces
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    return text

# Fill 'School_name' with 'School_level' where 'School_name' is empty
df.loc[df['School_name'] == '', 'School_name'] = df['School_level']

# Function to count empty entries in each column
def count_empty_entries(column):
    return (column == '').sum()

# Apply the function to each column
empty_entries_count = df.apply(count_empty_entries)

# Transliterate the remaining columns except for the first column (school_id)
for column in df.columns[1:]:
    df[f'{column}_transliterated'] = df[column].apply(lambda x: clean_text(transliterate(x, sanscript.DEVANAGARI, sanscript.ITRANS)) if isinstance(x, str) else x)

# Keep the 'school_id' column, original columns, and the new transliterated columns
columns_to_keep = ['school_id'] + [col for col in df.columns if col not in ['school_id']]

df_aa_transliterated = df[columns_to_keep]

# Define the mapping dictionary
mapping = {
    '': 0,
    'avi': 1,
    'pravi': 2,
    'nimavi': 3,
    'mavi': 4
}

# Apply the mapping to the 'School_level_transliterated' column
df['School_level_transliterated_categorized'] = df['School_level_transliterated'].map(mapping)

# Save the updated dataframe to a new CSV file
df.to_csv(output_file_path, index=False)

# Display the updated dataframe
print("Sample of the updated dataframe:")
df.head(100)

# Print statistics and sample data
print("Cleaned data sample:")
df.head(10)
print(df.columns)

print("Empty entries count:")
print(empty_entries_count)

print("Unique values in 'School_level_transliterated_categorized':")
print(df['School_level_transliterated_categorized'].unique())

import pandas as pd
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import re
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

# Ensure the processed data directory exists
ensure_directory_exists(processed_data_dir)

# File paths
file_path_b1 = os.path.join(processed_data_dir, 'preprocessed_after_B_1.csv')
output_file_path_b2 = os.path.join(processed_data_dir, 'preprocessed_after_B_2.csv')
district_id_output_path = os.path.join(processed_data_dir, 'district_id.csv')

# Function to detect if a string contains Devanagari script
def contains_devanagari(text):
    if isinstance(text, str):
        devanagari_pattern = re.compile('[\u0900-\u097F]+')
        return bool(devanagari_pattern.search(text))
    return False

# Function to transliterate if Devanagari is detected
def transliterate_if_devanagari(text):
    if contains_devanagari(text):
        return transliterate(text, sanscript.DEVANAGARI, sanscript.ITRANS)
    return text

# Load the dataset
df = pd.read_csv(file_path_b1)

# Print the columns to check for correct names
print(df.dtypes)

text_columns = df.select_dtypes(include='object').columns

df[text_columns] = df[text_columns].apply(lambda x: x.apply(transliterate_if_devanagari) if x.dtype == 'object' else x)

# Verify the new column has been created
print("Columns in the dataframe:", df.columns)

df[text_columns].isnull().sum()
df[text_columns] = df[text_columns].fillna('')

# Convert Text Columns to Lowercase
df[text_columns] = df[text_columns].apply(lambda x: x.str.lower(), axis='columns')

# Define the function to join specific words
def join_specific_words(text):
    if pd.isna(text) or not isinstance(text, str):
        return text  # Return the original value if it's not a string
    
    text = re.sub(r'\bni ma vi\b', 'nimavi', text)
    text = re.sub(r'\bpra vi\b', 'pravi', text)
    text = re.sub(r'\ba vi\b', 'avi', text)
    return text

# Identify columns with the 'modified_' prefix
modified_columns = [col for col in df.columns if col.startswith('modified_')]

# Apply the join_specific_words function only to these columns
df[modified_columns] = df[modified_columns].applymap(join_specific_words)

# Define the function to extract school levels
def extract_school_levels(text):
    levels = []
    if re.search(r'\bnimavi\b', text):
        levels.append('nimavi')
    if re.search(r'\bpravi\b', text):
        levels.append('pravi')
    if re.search(r'\bavi\b', text) and not re.search(r'\bpravi\b', text):
        levels.append('avi')
    if re.search(r'\bmavi\b', text):
        levels.append('mavi')
    return ' '.join(levels)

# Define the function to remove school levels from the text
def remove_school_levels(text):
    text = re.sub(r'\bnimavi\b', '', text)
    text = re.sub(r'\bpravi\b', '', text)
    text = re.sub(r'\bavi\b', '', text)
    text = re.sub(r'\bmavi\b', '', text)
    return text.strip()

# Apply the functions to the 'modified_name' column
df['school_levels'] = df['modified_name'].apply(extract_school_levels)
df['root_school_name'] = df['modified_name'].apply(remove_school_levels)

# Replace specific patterns in the root_school_name column
df['root_school_name'] = df['root_school_name'].replace(
    {
        r'\benglish vi\b': 'ebs',
        r'\benglish boarding vi\b': 'ebs',
        r'\bboarding vi\b': 'ebs',
        r'\benglish ma boarding v\b': 'ebs'
    }, regex=True
)

# Get unique districts and their respective unique IDs
unique_districts = df[['modified_district', 'district_id']].drop_duplicates()

# Sort by district and district_id in ascending order
unique_districts_sorted = unique_districts.sort_values(by=['district_id'])

# Save the unique districts to a CSV file
unique_districts_sorted.to_csv(district_id_output_path, index=False)

# Check for null values
df.isnull().sum()

# Save the updated dataframe to a new CSV file
df.to_csv(output_file_path_b2, index=False)

print("Updated dataframe saved to:", output_file_path_b2)
print("First 10 rows of the updated dataframe:")
df.head(10)


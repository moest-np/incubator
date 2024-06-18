import os
import sys
import pandas as pd
import re
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

# Add the path to the directory containing pattern_replacement_A.py
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from pattern_replacement import patterns_mavi, patterns_pravi, patterns_nimavi, patterns_avi

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Define the function to detect if a string contains Devanagari script
def contains_devanagari(text):
    if isinstance(text, str):
        devanagari_pattern = re.compile('[\u0900-\u097F]+')
        return bool(devanagari_pattern.search(text))
    return False

# Define the function to transliterate if Devanagari is detected
def transliterate_if_devanagari(text):
    if contains_devanagari(text):
        return transliterate(text, sanscript.DEVANAGARI, sanscript.ITRANS)
    return text

def clean_text(text):
    if text is None:  # Check if the text is None (null value)
        return ''
    if isinstance(text, str):
        text = re.sub(r'[:,\-।().]', ' ', text)  # Replace specified characters with a space
        text = re.sub(r'[0-9]', ' ', text)  # Remove numbers
        text = re.sub(r'\s+', ' ', text).strip()  # Replace multiple spaces with a single space and strip leading/trailing spaces
        return text.lower()
    else:
        return ''

# Define the function to replace patterns based on given mappings
def replace_patterns(text, patterns, replacement):
    if isinstance(text, str):
        for pattern in patterns:
            text = re.sub(pattern, replacement, text)
    return text

# Define the function to check for duplicates and null values
def check_and_clean_data(df):
    df = df.drop_duplicates()
    df = df.fillna('')
    return df

# Define the function to preprocess names
def preprocess_names(df):
    for column in df.columns:
        if df[column].dtype == object:
            df[column] = df[column].astype(str).apply(transliterate_if_devanagari).apply(clean_text)
            if 'name' in column.lower():
                df['modified_' + column] = df[column]
                print(f"Processed column: {column}")
    return df

# Define the function to apply replacements
def apply_replacements(df, patterns):
    for column in df.columns:
        if column.startswith('modified_'):
            for pattern, replacement in patterns:
                df[column] = df[column].apply(lambda x: replace_patterns(x, pattern, replacement))
                print(f"Applied replacements on column: {column}")
    return df

def load_and_preprocess_data(base_dir, apply_patterns=False):
    
    raw_data_dir = os.path.normpath(os.path.join(base_dir, '..', '..', 'data', 'raw'))
    file_path_bb = os.path.join(raw_data_dir, 'school_list_B.tsv')

    # Load Source B
    try:
        df2 = pd.read_csv(file_path_bb, sep='\t')
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

    # Check for duplicates and null values
    df2 = check_and_clean_data(df2)

    # Preprocess the names
    df2 = preprocess_names(df2)

    if apply_patterns:
        # Define replacement patterns
        replacement_patterns = [
            (patterns_nimavi, 'nimavi'),
            (patterns_mavi, 'mavi'),
            (patterns_pravi, 'pravi'),
            (patterns_avi, 'avi')
        ]
        # Apply replacements
        df2 = apply_replacements(df2, replacement_patterns)

    return df2

def extract_school_level_and_root(name):
    levels = ['nimavi', 'pravi', 'mavi', 'avi']
    school_level = ""
    root = name
    
    for level in levels:
        if level in name:
            school_level = level
            root = name.replace(level, "").strip()
            break
    
    return school_level, root

def main(apply_patterns=True):
    base_dir = os.getcwd()  # Use current working directory
    
    # Load and preprocess the data
    df2 = load_and_preprocess_data(base_dir, apply_patterns)
    if df2 is None:
        print("Data loading failed.")
        return None
    
    # Apply the new column creation if apply_patterns is True
    if apply_patterns:
        columns_to_process = ['modified_name', 'modified_old_name1', 'modified_old_name2', 'modified_old_name3']
        for col in columns_to_process:
            df2[f'{col}_school_level'] = df2[col].apply(lambda x: extract_school_level_and_root(x)[0] if pd.notnull(x) else "")
            df2[f'{col}_root'] = df2[col].apply(lambda x: extract_school_level_and_root(x)[1] if pd.notnull(x) else "")
    
    # Define the columns to save
    columns_to_save = [
        'school_id','district', 'modified_name', 'modified_name_school_level', 'modified_name_root',
        'modified_old_name1', 'modified_old_name1_school_level', 'modified_old_name1_root',
        'modified_old_name2', 'modified_old_name2_school_level', 'modified_old_name2_root','district'
    ]
    

    processed_data_dir = os.path.normpath(os.path.join(base_dir, '..', '..', 'data', 'processed'))
    ensure_directory_exists(processed_data_dir)
    
    # Save the processed data to CSV
    output_file_path = os.path.join(processed_data_dir, 'preprocessed_after_B.csv')
    df2.to_csv(output_file_path, columns=columns_to_save, index=False)
    
    print(f"Data saved to {output_file_path}")
    return df2

if __name__ == "__main__":
    apply_patterns = True  # Set to True for the second and subsequent runs
    df2 = main(apply_patterns)
    if df2 is not None:
        print("Data loaded and processed successfully")



df2.columns
df2[['modified_name','district','modified_name_school_level','modified_name_root','modified_old_name1','modified_old_name1_school_level','modified_old_name1_root','modified_old_name2','modified_old_name2_school_level','modified_old_name2_root']][df2['modified_name_school_level']==''].tail(10)
df2[(df2['modified_name_school_level'] == '') & 
                       (df2['modified_old_name1_school_level'] == '') & 
                       (df2['modified_old_name2_school_level'] == '')].shape
df2[['modified_name', 'modified_old_name1', 'modified_old_name2', 'modified_old_name3']].tail(20)


# Print the first few rows to inspect
df2.dtypes
df2.columns
df2.head()
df2.shape
df2.isnull().sum()
(df2=='').sum()
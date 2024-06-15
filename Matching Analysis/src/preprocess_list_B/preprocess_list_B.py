import pandas as pd
import re
import os
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

# Function to ensure a directory exists
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Define the function to clean text
def clean_text(text):
    if isinstance(text, str):
        text = re.sub(r'[:,\-।().]', ' ', text)  # Replace specified characters with a space
        text = re.sub(r'[0-9]', ' ', text)  # Remove numbers
        text = re.sub(r'\s+', ' ', text).strip()  # Replace multiple spaces with a single space and strip leading/trailing spaces
        return text.lower()
    else:
        return text

# Define the function to remove specific rows
def remove_specific_rows(df):
    # Convert the 'name' column to lowercase
    df['name'] = df['name'].str.lower()
    
    # Define the substrings to check for
    substrings = ['ebs', 'angreji', 'english', 'academy', 'boarding','e b s','e b school',r'\bemb\b',r'\bb school\b',r'\beng\b']
    
    # Create a boolean mask for rows that do not contain any of the substrings
    mask = ~df['name'].apply(lambda x: any(substring in x for substring in substrings))
    
    # Filter the DataFrame using the mask
    filtered_df = df[mask]
    
    return filtered_df

# Define the function to replace patterns in a DataFrame
def replace_patterns(df, patterns, replacement):
    for pattern in patterns:
        df = df.applymap(lambda x: re.sub(pattern, replacement, x) if isinstance(x, str) else x)
    return df

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

# Define the function to join specific words
def join_specific_words(text):
    if pd.isna(text) or not isinstance(text, str):
        return text  # Return the original value if it's not a string
    text = re.sub(r'\bni ma vi\b', 'nimavi', text)
    text = re.sub(r'\bpra vi\b', 'pravi', text)
    text = re.sub(r'\ba vi\b', 'avi', text)
    text = re.sub(r'\baa vi\b', 'avi', text)
    text = re.sub(r'\bma vi\b', 'mavi', text)
    return text

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

# Main function
def main():
    # Base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Raw and processed data directories
    raw_data_dir = os.path.normpath(os.path.join(base_dir, '../../data/raw'))
    processed_data_dir = os.path.normpath(os.path.join(base_dir, '../../data/processed'))

    # Ensure the processed data directory exists
    ensure_directory_exists(processed_data_dir)

    # File paths
    file_path_bb = os.path.join(raw_data_dir, 'school_list_B.tsv')
    output_file_path = os.path.join(processed_data_dir, 'preprocessed_after_B.csv')

    # Load Source B
    df2 = pd.read_csv(file_path_bb, sep='\t')

    # Print the first few rows of the dataframe
    print("First few rows of the dataframe:")
    print(df2.head())

    # Print the columns of the dataframe
    print("Columns in the dataframe:")
    print(df2.columns)

    # Patterns for 'मा वि'
    patterns_ma_vi = [
        r'\bsec\. school\b',
        r'\bma v\b',
        r'\bhigh school\b',
        r'\bsecondary school\b',
        r'\bmadhyamik\b',
        r'\bma vi\.\b',
        r'\bma vi\b',
        r'\bmavi\b',
        r'\bmv\b'
        r'\bma vidyalaya\b',
        r'\bsecondary\b',
        r'\bma विi\b',
        r'\baadharbhut viddhyalaya\b'
        r'\bseccondary school\b'
        r'\bmadhyamik vidyalay\b',
        r'\bmadhyamik bidhyalaya\b',
        r'\bma bi\b',
        r'\bsec school\b',
        r'\bsecodary school\b'
    ]
    # Patterns for 'प्रा वि'
    patterns_pra_vi = [
        r'\bprathamic bidyalaya\b',
        r'\bprathamik bidhyalaya\b',
        r'\bprathamik vidhyalaya\b',
        r'\bpra v\b',
        r'\bprimari school\b'
        r'\bprimary school\b',
        r'\bpra vi\b',
        r'\bpvt ltd\b',
        r'\bप्रा विi\b',
        r'\badharbhut pra v\b',
        r'\bpraimary school\b',
        r'\bpremary\b',
        r'\badharvut school\b',
        r'\baadharbhut vidhayala\b',
        r'\baadharbhut biddhyalaya\b',
        r'\baadharbhut vidhayalay\b',
        r'\baadharbhut bidayalaya\b'
    ]

    # Patterns for 'नि मा वि'
    patterns_ni_ma = [
        r'\bni ma v\b'
    ]

    # Patterns for 'आ वि'
    patterns_aa_vi = [
        r'\badharbhut bidyalay\b',
        r'\baadharbhut bidyalaya\b',
        r'\baadharbhut vidyalay\b',
        r'\baadharvut bidyalaya\b',
        r'\bbasic v\b',
        r'\badharbhut bidhyalaya\b',
        r'\badharbhut bidhyalay\b',
        r'\bbasic chool\b',
        r'\baadharvut vidyalaya\b',
        r'\baadharbhut vidhalaya\b',
        r'\badharbhut vidhyalaya\b',
        r'\badharbhut vidyalaya\b',
        r'\baa vi\b',
        r'\baa v\b',
        r'\baadharvut school\b',
        r'\badharbhoot vidhyalaya\b',
        r'\baadharbhut vidhyalaya\b',
        r'\badharbhut v\b',
        r'\bpre primary school\b',
        r'\badharbhoot v\b',
        r'\bbasic school\b',
        r'\baa\. v\b',
        r'\bbasic schoo\b',
        r'\baa\. vi\.\b',
        r'\baadharvut vidyalaya\b',
        r'\bpre primary school\b',
        r'\bpre school\b',
        r'\bBesic School\b',
        r'\bAdharbhut Vidhalaya\b',
        r'\bAadharbhut Vidyalaya\b',
        r'\bAadharbhut vidhyalaya\b',
        r'\badharbhoot v\b',
        r'\badhar v\b',
        r'\baa bi\b',
        r'\baadharbhut bidhyalaya\b',
        r'\bbasic scool\b',
        r'\bbasick school\b',
        r'\baadharbhut school\b',
        r'\badharbhut school\b',
        r'\bbasic level school\b',
        r'\baadharbhut vidyalaya\b',
        r'\badharbhut bidyalaya\b',
        r'\badharvut v\b',
        r'\badharbhut vidyalay\b',
        r'\badharbhut vidyalayai\b',
        r'\badhar vi\b',
        r'\bbasic cshool\b',
        r'\badharbhut vidayalay\b',
        r'\badharbhut bidhalaya\b',
        r'\baadharbhut bidhalaya\b',
        r'\baadharbhut bidhalaya\b',
        r'\badarbhut bidlaya\b',
        r'\bbesic school\b',
        r'\bbasic shool\b',
        r'\baadarbhut vidyalay\b',
        r'\baadharbhoot vidyalaya\b',
        r'\bbisic schoo\b',
        r'\baadharvut v\b',
        r'\badharbhut biddhyalaya\b',
        r'\badharboot vidyalaya\b',
        r'\badharvut vidyalaya\b',
        r'\badharbhoot vidhylaya\b',
        r'\bbasicschool\b',
        r'\badharbhoot vidyalaya\b',
        r'\badharbhut vidhalaya\b',
        r'\badharvut vidhyalaya\b',
        r'\badharvut school\b',
        r'\badharbhut bidhalya\b',
        r'\badharbhut biddyalaya\b',
        r'\badharbhut biddyalay\b',
        r'\b basic scchool\b',
        r'\baadharbhut vidalaya\b'
    ]

    
    # Identify text columns
    text_columns = df2.select_dtypes(include='object').columns

    # Apply replacements to 'name' column
    df2 = replace_patterns(df2, patterns_ma_vi, 'मा वि')
    df2 = replace_patterns(df2, patterns_pra_vi, 'प्रा वि')
    df2 = replace_patterns(df2, patterns_ni_ma, 'नि मा वि')
    df2 = replace_patterns(df2, patterns_aa_vi, 'आ वि')

    # Debugging: Print a sample of 'name' column to see if replacements worked
    print("After replacements in 'name' column:")
    print(df2['name'].head(10))

    # Apply
    df2 = remove_specific_rows(df2)

    # Apply the cleaning function to all text columns, handling missing values
    for col in text_columns:
        df2['modified_' + col] = df2[col].apply(lambda x: clean_text(x) if pd.notnull(x) else '')

    # Debugging: Print a sample of 'modified_name' column to see if cleaning worked
    print("After cleaning 'modified_name' column:")
    print(df2['modified_name'].head(10))

    # Apply replacements to 'modified_name' column again
    df2['modified_name'] = replace_patterns(df2[['modified_name']], patterns_ma_vi, 'मा वि')['modified_name']
    df2['modified_name'] = replace_patterns(df2[['modified_name']], patterns_pra_vi, 'प्रा वि')['modified_name']
    df2['modified_name'] = replace_patterns(df2[['modified_name']], patterns_ni_ma, 'नि मा वि')['modified_name']
    df2['modified_name'] = replace_patterns(df2[['modified_name']], patterns_aa_vi, 'आ वि')['modified_name']

    # Debugging: Print a sample of 'modified_name' column to see if replacements worked
    print("After replacements in 'modified_name' column:")
    print(df2['modified_name'].head(10))

    # Remove full stops from all text entries in the DataFrame
    df2 = df2.applymap(lambda text: re.sub(r'\.', '', text) if isinstance(text, str) else text)

    # Apply transliteration
    for col in text_columns:
        df2['modified_' + col] = df2['modified_' + col].apply(transliterate_if_devanagari)

    # Convert Text Columns to Lowercase
    for col in text_columns:
        df2['modified_' + col] = df2['modified_' + col].str.lower()

    # Apply the join_specific_words function only to these columns
    modified_columns = [col for col in df2.columns if col.startswith('modified_')]
    for col in modified_columns:
        df2[col] = df2[col].apply(join_specific_words)

    # Apply the functions to the 'modified_name' column
    df2['school_levels'] = df2['modified_name'].apply(extract_school_levels)
    df2['root_school_name'] = df2['modified_name'].apply(remove_school_levels)

    # Debugging: Print final DataFrame to see if all transformations worked
    print("Final DataFrame:")
    print(df2.head(10))

    # Get unique districts and their respective unique IDs
    unique_districts = df2[['modified_district', 'district_id']].drop_duplicates()
    unique_districts_sorted = unique_districts.sort_values(by=['district_id'])
    district_id_output_path = os.path.join(processed_data_dir, 'district_id.csv')
    unique_districts_sorted.to_csv(district_id_output_path, index=False)

    # Save the updated dataframe to a new CSV file
    df2.to_csv(output_file_path, index=False)
    print("Updated dataframe saved to:", output_file_path)

    # Print the columns of the updated dataframe
    print("Columns in the updated dataframe:")
    print(df2.columns)

    return df2

# If running in an interactive environment (e.g., Jupyter), call the main function and assign the result to a variable
if __name__ == "__main__":
    df2 = main()

# Now you can interactively print and inspect the DataFrame

df2.isnull().sum()
(df2 == '').sum()

# Print specific columns where 'school_levels' is empty
df2[['name', 'modified_name', 'school_levels']][df2['school_levels'] == ''].shape
# df2[['name', 'modified_name', 'school_levels']][(df2['modified_name'].str.contains('ma vi')) & (df2['school_levels'] == '') ].shape

df2[['name', 'modified_name', 'school_levels']][(df2['modified_name'].str.contains(r'\bprimari\b')) & (df2['school_levels'] == '') ].shape







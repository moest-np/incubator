import pandas as pd
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import re

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

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
df = pd.read_csv('./Preprocessed_after_B_1.csv')
# Print the columns to check for correct names
print(df.dtypes)

text_columns = df.select_dtypes(include='object').columns

df[text_columns] = df[text_columns].apply(lambda x: x.apply(transliterate_if_devanagari) if x.dtype == 'object' else x)

# Verify the new column has been created
print("Columns in the dataframe:", df.columns)

df.shape
df.dtypes
df.head(10)

df[text_columns].isnull().sum()
df[text_columns] = df[text_columns].fillna('')

## Header 2: Convert Text Columns to Lowercase
df[text_columns] = df[text_columns].apply(lambda x: x.str.lower(), axis='columns')


df.columns

# Define the function to join specific words
def join_specific_words(text):
    if pd.isna(text) or not isinstance(text, str):
        return text  # Return the original value if it's not a string
    
    text = re.sub(r'\bni ma vi\b', 'nimavi', text)
    text = re.sub(r'\bpra vi\b', 'pravi', text)
    text = re.sub(r'\ba vi\b', 'avi', text)
    return text

# Assume df is your DataFrame and it already contains the necessary columns
# Identify columns with the 'modified_' prefix
modified_columns = [col for col in df.columns if col.startswith('modified_')]

# Apply the join_specific_words function only to these columns
df[modified_columns] = df[modified_columns].applymap(join_specific_words)

df.head()


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
df.head(10)


# Replace specific patterns in the root_school_name column
df['root_school_name'] = df['root_school_name'].replace(
    {
        r'\benglish vi\b': 'ebs',
        r'\benglish boarding vi\b': 'ebs',
        r'\bboarding vi\b': 'ebs',
        r'\benglish ma boarding v\b': 'ebs'
    }, regex=True
)



df.head(10)

# df[['name','modified_name','modified_name_transliterated','root_school_name']].head(100)

df[['modified_district','district_id']].nunique()

# Get unique districts and their respective unique IDs
unique_districts = df[['modified_district', 'district_id']].drop_duplicates()

# Sort by district and district_id in ascending order
unique_districts_sorted = unique_districts.sort_values(by=['district_id'])

unique_districts_sorted.to_csv('district_id.csv',index=False)



df.isnull().sum()

df.head()

df.to_csv('Preprocessed_after_B_2.csv', index=False)
df.head()
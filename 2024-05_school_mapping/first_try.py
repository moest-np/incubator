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
df = pd.read_csv('./updated_merged_school_data_B.csv')
df = df.drop(columns=['school'])  # Ensure 'school' is the correct column name to drop
# Print the columns to check for correct names
print(df.dtypes)

# Create a copy of the dataframe to store transliterated columns
df_transliterated = df.copy()

# Apply transliteration check and create new columns for transliterated text
for column in df.columns:
    df_transliterated[column + '_transliterated'] = df[column].apply(transliterate_if_devanagari)

# Verify the new columns have been created
print("Columns in the transliterated dataframe:", df_transliterated.columns)

# Display the unique values in the 'Potential_District_Name_transliterated' column
if 'Potential_District_Name_transliterated' in df_transliterated.columns:
    print(df_transliterated['Potential_District_Name_transliterated'].unique())
else:
    print("Column 'Potential_District_Name_transliterated' does not exist in the dataframe.")

df_transliterated['Potential_District_Name_transliterated'].unique()
len(df_transliterated['Potential_District_Name_transliterated'].unique())
df_transliterated.to_csv('final_merged_school_data.csv',index=False)















import pandas as pd
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from fuzzywuzzy import fuzz
import numpy as np

# Load the dataframes
df_jilla = pd.read_csv('jilla.csv')
df_transliterated = pd.read_csv('./final_merged_school_data.csv')
df_jilla.columns = ['District_Name']

# Transliterate the district names from Devanagari to ITRANS
df_jilla['District_Name_ITRANS'] = df_jilla['District_Name'].apply(lambda x: transliterate(x, sanscript.DEVANAGARI, sanscript.ITRANS))

# Convert district names to lowercase for case-insensitive matching
df_jilla['District_Name_ITRANS'] = df_jilla['District_Name_ITRANS'].str.lower()
df_transliterated['Potential_District_Name_transliterated'] = df_transliterated['Potential_District_Name_transliterated'].str.lower()

# Function to perform fuzzy matching
def fuzzy_match(potential_name, district_names):
    if pd.isna(potential_name):
        return None
    
    best_match = None
    best_score = 0
    for district_name in district_names:
        if pd.isna(district_name):
            continue
        score = fuzz.ratio(str(potential_name), str(district_name))
        if score > best_score:
            best_match = district_name
            best_score = score
    return best_match

# Match the district names using fuzzy matching
df_transliterated['Matched_District_Name'] = df_transliterated['Potential_District_Name_transliterated'].apply(lambda x: fuzzy_match(x, df_jilla['District_Name_ITRANS'].tolist()))

# Create a new column 'Assigned_District_Name' based on the 'Matched_District_Name' column
df_transliterated['Assigned_District_Name'] = df_transliterated['Matched_District_Name']

# Select relevant columns to display
df_transliterated = df_transliterated[['school_id', 'Potential_School_Name', 'Potential_School_Name_transliterated', 'Potential_District_Name', 'Potential_District_Name_transliterated', 'Matched_District_Name', 'Assigned_District_Name']]

# Display the first 10 rows
df_transliterated.head(10)

# Display unique values and check for null values
print("Unique Assigned District Names: ", len(df_transliterated['Assigned_District_Name'].unique()))
print(df_transliterated['Assigned_District_Name'].unique())
print(df_transliterated['Assigned_District_Name'].isnull().sum())

# Display rows with null Potential_District_Name
df_transliterated[df_transliterated['Potential_District_Name'].isnull()]



df_transliterated.head(100)
df_transliterated[df_transliterated['Potential_District_Name'].isnull()]
df_transliterated.to_csv('ready_for_matching_A.csv',index=False)


import pandas as pd
df = pd.read_csv('ready_for_matching_B.csv')
df.isnull().sum()


df.head(200)
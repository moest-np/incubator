import pandas as pd
from indicnlp.tokenize import indic_tokenize
import re

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load Source A
df = pd.read_csv('./Processed_School_Data.csv')


df.shape
df.head()


# Remove ':', '-', and '।' from the 'school' column
df1['school'] = df1['school'].apply(lambda text: text.replace(':', ' ').replace('-', ' ').replace('।', ' '))

# Apply the cleaning function to remove commas, "॰", Devanagari numbers, and "ः"
df1['school'] = df1['school'].apply(lambda text: re.sub(r'[,\॰०१२३४५६७८९ः]', '', text).strip())
df1['school'] = df1['school'].apply(lambda text: re.sub(r'\s+', ' ', text).strip())

# Function to filter out rows containing English characters
def contains_english(text):
    return bool(re.search(r'[a-zA-Z]', text))

# Filter the DataFrame excluding the first row
filtered_df = df1[1:][df1['school'][1:].apply(contains_english)]

# Remove specific row
df1 = df1[df1['school_id'] != 20852]

# Lists of patterns to replace
patterns_ma_vi = [
    'माबी', 'उ म बि', 'मवि', 'म्ाा बी', 'उ०मा०वि', 'उच्च मा', 'उच्चमा', 'उमा वि', 'माध्यामिक वि',
    'मा वी', 'मा बी', 'मावि', 'माबि', 'मा बि', 'मावी'
]

patterns_pra_vi = [
    'प्राबि', 'प्रावि', 'प्रा बि', 'प्र बि', 'प्राबी', 'प्रँ ीव्', 'प््राा वि', 'प्र्रा वि', 'प्रा बी',
    'प्रा वी', 'प्र वि', 'प्रावी', 'प्रा बि', 'प्रा ि', 'प्रा। वी', 'प्र वी', 'प्रा स्कूल',
    'प्राइमरी स्कुल', 'प्राथमीक वि', 'प्रावऽि'
]

patterns_ni_ma = ['नि म', 'नि मा।वि']
patterns_aa_vi = ['आवि', 'आबि']

patterns_general = {
    'त्रि बि': 'त्रि वि', 'नेराप्रवि': 'नेरा प्रा वि', 'प्रा बाग्लुङ': 'प्रा वि बाग्लुङ', 'निमा': 'नि मा',
    'भूमे प्रा िचितवन': 'भूमे प्रा वि चितवन', 'माध्यमिक': 'मा', 'विद्यालय': 'वि', 'निम्न': 'नि',
    'प्रा ली': 'प्रा लि', 'विधालय': 'वि', 'प्राथमिक': 'प्रा', 'आधारभूत': 'आ', 'बिधालय': 'वि',
    'बिद्यालय': 'वि', 'विदोकानडाँडा': 'वि दोकानडाँडा', 'दरवार हाइस्कुल': 'दरवार हाइस्कुल मा वि',
    r'\bबी\b': 'बि', r'\bबि\b': 'वि', 'तनहु': 'तनहुँ', 'नि मा िपर्बत': 'नि मा वि पर्बत',
    'नि म बि': 'नि मा वि', 'नि वा': 'नि मा वि', 'त्रि वि': 'त्रिवि', 'मा ि': 'मा वि ',
    'नेराप्रा।वि': 'नेरा प्रा वि', 'वि पी': 'विपी', 'तनहूँ': 'तनहुँ', 'तनुहुँ': 'तनहुँ',
    'धनकुटा थाकले': 'थाकले धनकुटा', 'नेराप्रा वि': 'नेरा प्रा वि', 'निङ्गलाखसैनी बेतडि आ वि': 'निङ्गलाखसैनी आ वि बेतडि',
    'सरस्वती आ वि मा वि अर्खौले': 'सरस्वती-आवि मा वि अर्खौले', 'ने रा वि': 'नेरावि', 'ना वि मा': "ना वि मा",
    'वि मा वि': 'नावि मा वि'
}

# Function to apply replacements from lists
def replace_patterns(df, patterns, replacement):
    for pattern in patterns:
        df['school'] = df['school'].replace({pattern: replacement}, regex=True)
    return df

# Apply general replacements
df1['school'] = df1['school'].replace(patterns_general, regex=True)
df1 = replace_patterns(df1, patterns_ma_vi, 'मा वि')
df1 = replace_patterns(df1, patterns_pra_vi, 'प्रा वि')
df1 = replace_patterns(df1, patterns_ni_ma, 'नि मा वि')
df1 = replace_patterns(df1, patterns_aa_vi, 'आ वि')

# Function to tokenize and split the school name into desired columns
def split_school_name(row):
    tokens = indic_tokenize.trivial_tokenize(row)
    try:
        vi_index = tokens.index('वि')
        potential_school_name = ' '.join(tokens[:vi_index + 1])
        potential_location = ' '.join(tokens[vi_index + 1:])
        potential_district_name = tokens[-1]
    except ValueError:  # 'वि' not found
        potential_school_name = row
        potential_location = ''
        potential_district_name = ''
    return pd.Series([potential_school_name, potential_location, potential_district_name])

# Apply the function to create new columns
df1[['Potential_School_Name', 'Potential_Location', 'Potential_District_Name']] = df1['school'].apply(split_school_name)

# Define the school levels
school_levels = ['प्रा वि', 'आ वि', 'मा वि', 'नि मा वि']

# Function to split Potential_School_Name into Root_name and School_level
def split_root_and_level(row):
    for level in school_levels:
        if level in row:
            parts = row.split(level)
            root_name = parts[0].strip()
            school_level = level
            return pd.Series([root_name, school_level])
    return pd.Series([row, ''])

# Apply the function to create new columns
df1[['Root_name', 'School_level']] = df1['Potential_School_Name'].apply(split_root_and_level)

# Function to update Root_name based on the school column if null or empty
def update_root_name(row):
    if pd.isnull(row['Root_name']) or row['Root_name'] == '':
        for keyword in school_levels:
            if keyword in row['school']:
                return keyword
    return row['Root_name']

# Apply the function to update the Root_name column
df1['Root_name'] = df1.apply(update_root_name, axis=1)

# Filter out rows where School_level is null or an empty string
df1 = df1[~df1['School_level'].isnull() & (df1['School_level'] != '')]

# Remove unnecessary spaces from the specified columns
df1['district1'] = df1['district1'].str.strip()
df1['Potential_District_Name'] = df1['Potential_District_Name'].str.strip()

# Ensure no null or empty values
df1['Potential_Location'].fillna('', inplace=True)
df1['Potential_District_Name'].fillna('', inplace=True)

# Select specific columns and display the first few rows
df1 = df1[['school_id', 'Potential_School_Name', 'Potential_Location', 'Potential_District_Name', 'Root_name', 'School_level']]

# Debug: Check for null values before saving
print(df1.isnull().sum())
df1.head(100)

# Save the final cleaned DataFrame to CSV
df1.to_csv('cleaned_school_data.csv', index=False)

import pandas as pd
# Load the CSV file to verify changes
df_cleaned = pd.read_csv('cleaned_school_data.csv')
print(f"Null values in the cleaned DataFrame: {df.isnull().sum()}")
print(f"Unique values in School_level: {df['School_level'].unique()}")
print(f"Rows with null School_level: {len(df_cleaned[df['School_level'].isnull()])}")

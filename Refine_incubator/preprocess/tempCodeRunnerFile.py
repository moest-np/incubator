


import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Load the datasets
df_A = pd.read_csv('school_list_AA_2_transliterated_matched.tsv', sep='\t')
df_B = pd.read_csv('school_list_BB_3.csv')
# Drop the 'Unnamed: 0' column if it exists
df_A = df_A.drop(columns=['Unnamed: 0','Potential_district_transliterated','Matched_District'], errors='ignore')
df_B = df_B.drop(columns=['Unnamed: 0'], errors='ignore')

# # Replace null values by empty strings in df_B
# df_B = df_B.fillna('')
# # Replace null values by empty strings in df_A
# df_A = df_A.fillna('')
df_A.columns
df_A['School_level_transliterated'].unique()
df_B.head()

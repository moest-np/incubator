


import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Load the datasets
df_A = pd.read_csv('Preprocessed_after_fuzzy_A.csv')
df_B = pd.read_csv('Preprocessed_after_fuzzy_B.csv')
df_B.head()

# Replace null values by empty strings in df_B
df_B = df_B.fillna('')
# Replace null values by empty strings in df_A
df_A = df_A.fillna('')

df_A.isnull().sum()
df_B.isnull().sum()
df_B['modified_old_name1'].head()
df_B.dtypes



# Replace null values by empty strings in df_B
df_B = df_B.fillna('')
# Replace null values by empty strings in df_A
df_A = df_A.fillna('')

df_A.isnull().sum()
df_B.isnull().sum()

# Verify the changes by displaying the unique values in the modified column
df_B['school_levels'].unique()

df_A.to_csv('Preprocessed_after_fuzzy_second_A.csv',index=False)
df_B.to_csv('Preprocessed_after_fuzzy_second_B.csv',index=False)


import pandas as pd
import re
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

# Load the provided CSV file
file_path = 'Preprocessed_after_A_1.csv'
df = pd.read_csv(file_path)

df.head()

df.head()

# # Drop the specified columns
# df = df.drop(columns=['school', 'Location'])


# Replace NaN values with empty strings
df = df.fillna('')

# Print rows where 'School_level' is empty
empty_school_level_rows = df[df['School_level'] == '']
len(empty_school_level_rows)



# Function to clean the transliterated text
def clean_text(text):
    text = text.lower()  # Convert to lowercase
    #text = re.sub(r'[^a-z\s]', '', text)  # Remove special characters and numbers
    text = text.strip()  # Remove leading and trailing spaces
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    return text


df['School_level'].unique()

# Print rows where 'School_level' is empty
empty_school_level_rows = df[df['School_level'] == '']
len(empty_school_level_rows)




# Print rows where 'School_level' is empty
empty_school_rows = df[df['School_name'] == '']
len(empty_school_rows)

# Print rows where 'School_level' is empty
empty_school_leve_rows = df[df['School_name'] == '']
len(empty_school_leve_rows)
empty_school_leve_rows.tail(1)

# Fill 'School_name' with 'School_level' where 'School_name' is empty
df.loc[df['School_name'] == '', 'School_name'] = df['School_level']

# Function to count empty entries in each column
def count_empty_entries(column):
    return (column == '').sum()

# Apply the function to each column
empty_entries_count = df.apply(count_empty_entries)
empty_entries_count



# Transliterate the remaining columns except for the first column (school_id)
for column in df.columns[1:]:
    df[f'{column}_transliterated'] = df[column].apply(lambda x: clean_text(transliterate(x, sanscript.DEVANAGARI, sanscript.ITRANS)) if isinstance(x, str) else x)

# Keep the 'school_id' column, original columns, and the new transliterated columns
columns_to_keep = ['school_id'] + [col for col in df.columns if col not in ['school_id']]

df_aa_transliterated = df[columns_to_keep]
df_aa_transliterated.head()



# Display the updated dataframe
df.head()
# Print the rows where Matched_district is null or an empty string
df[df.isnull() | (df == '')].sum()

# Filter and display rows where 'school_transliterated' contains the text "prah vih"
prah_vih_rows = df[df['school_1_transliterated'].str.contains('prah vih', na=False)]
len(prah_vih_rows)

df['School_level_transliterated'].unique()

# Define the mapping dictionary
mapping = {
    '': 0,
    'avi': 1,
    'pravi': 2,
    'nimavi': 3,
    'mavi': 4
}

# Apply the mapping to the 'school_levels' column
df['School_level_transliterated_categorized'] = df['School_level_transliterated'].map(mapping)

# Verify the changes by displaying the unique values in the modified column
df['School_level_transliterated_categorized'].unique()

df.head()

# Save the updated dataframe to a new CSV file
# output_file_path = 'school_list_AA_2_transliterated.csv'
output_file_path = 'Preprocessed_after_A_2.csv'

df.to_csv(output_file_path, index=False)


df.head(100)
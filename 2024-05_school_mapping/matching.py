import pandas as pd
from indicnlp.tokenize import indic_tokenize
import re
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows',None)


# Load Source A
df1 = pd.read_csv('data/school_list_A.tsv', sep='\t')

# Load Source B
df2 = pd.read_csv('data/school_list_B.tsv', sep='\t')

df1.shape
df1.columns
df1.head()
df1.duplicated().sum()

df2.shape
df2.columns
df2.head()

df1['school'].head(100)
df1.head(100)
# Apply the cleaning function to remove commas, "॰", and Devanagari numbers
df1['school'] = df1['school'].apply(lambda text: re.sub(r'[,\॰०१२३४५६७८९]', '', text).strip())
df1['school'] = df1['school'].apply(lambda text: re.sub(r'\s+', ' ', text).strip())


def contains_english(text):
    return bool(re.search(r'[a-zA-Z]', text))

# Filter the DataFrame excluding the first row
filtered_df = df1[1:][df1['school'][1:].apply(contains_english)]
filtered_df


df1 = df1[df1['school_id'] != 20852]


# Create the replacement dictionary with word boundaries
replacement_dict = {
    'माध्यमिक': 'मा',
    'विद्यालय': 'वि',
    'विधालय': 'वि',
    'प्राथमिक': 'प्रा',
    'आधारभूत': 'आ',
    'बिधालय': 'वि',
    'बिद्यालय': 'वि',
    'विदोकानडाँडा': 'वि दोकानडाँडा',
    'माबी': 'मा वि',
    'उ०मा०वि': 'मा वि',
    'आवि': 'आ वि',
    'निम्न': 'आ वि',
    'मावि': 'मा वि',
    'प्राबि': 'प्रा वि',
    'प्रावि': 'प्रा वि',
    'प्रा बि': 'प्रा वि',
    'निमा': ' नि मा',
    'प्राबी': 'प्रा वि',
    'प्रा बी': 'प्रा वि',
    'प्रा वी': 'प्रा वि',
    'आबि': 'आ वि',
    'माबि': 'मा वि',
    'मा बि': 'मा वि',
    r'\bबी\b': 'बि',
    r'\bबि\b': 'वि',
    'तनहु': 'तनहुँ',
    'तनहूँ': 'तनहुँ',
    'तनुहुँ': 'तनहुँ',
    'धनकुटा थाकले': 'थाकले धनकुटा',
    'नेराप्रा वि': 'नेरा प्रा वि',
    'निङ्गलाखसैनी बेतडि आ वि': 'निङ्गलाखसैनी आ वि बेतडि',
    'सरस्वती आ वि मा वि अर्खौले': 'सरस्वती-आवि मा वि अर्खौले'

}

# Apply the replacements using the dictionary
df1['school'] = df1['school'].replace(replacement_dict, regex=True)


# Function to tokenize and split the school name into desired columns
def split_school_name(row):
    tokens = indic_tokenize.trivial_tokenize(row)
    try:
        # Find the index of 'वि'
        vi_index = tokens.index('वि')
        # Combine tokens before 'वि' and including 'वि' itself
        potential_school_name = ' '.join(tokens[:vi_index + 1])
        # The tokens after 'वि'
        potential_location = ' '.join(tokens[vi_index + 1:])
        # The last token as the district name (unchanged from input)
        potential_district_name = tokens[-1]
    except ValueError:  # 'वि' not found
        potential_school_name = row
        potential_location = ''
        potential_district_name = ''
    return pd.Series([potential_school_name, potential_location, potential_district_name])

# Apply the function to create new columns
df1[['Potential_School_Name', 'Potential_Location', 'Potential_District_Name']] = df1['school'].apply(split_school_name)

df1[['school', 'Potential_School_Name', 'Potential_Location', 'Potential_District_Name']].head()


df1[['school','Potential_School_Name','Potential_Location','Potential_District_Name']].head(100)



# Define the school levels
school_levels = ['प्रा वि','आ वि','मा वि', 'नि मा वि']

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

# Select specific columns and display the first few rows
df1[['school', 'Potential_School_Name', 'Potential_Location', 'Potential_District_Name', 'Root_name', 'School_level']].head(100)
df1.isnull().sum()
df1[['Root_name', 'School_level']].isnull().sum()
(df1[['Root_name', 'School_level']] == '').sum()

emptydf1[df1[['Root_name', 'School_level']] == '']



null_df1 = df1[df1['district1'].isnull()]

null_df1.to_csv('null_data_A.csv',index = False)


df_null_A = pd.read_csv('./null_data_A.csv')
df_null_A.shape
df_null_A.columns
df_null_A.dtypes
df_null_A.isnull().sum()
df_null_A.head(100)
df_null_A.duplicated()

df_null_A[df_null_A['School_level'].isnull()]




df1.isnull().sum()
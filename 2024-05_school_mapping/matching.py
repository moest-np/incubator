import pandas as pd
from indicnlp.tokenize import indic_tokenize
import re
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows',None)
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt


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
# Remove ':', '-', and '।' from the 'school' column
df1['school'] = df1['school'].apply(lambda text: text.replace(':', ' ').replace('-', ' ').replace('।', ' '))

# Apply the cleaning function to remove commas, "॰", Devanagari numbers, and "ः"
df1['school'] = df1['school'].apply(lambda text: re.sub(r'[,\॰०१२३४५६७८९ः]', '', text).strip())
df1['school'] = df1['school'].apply(lambda text: re.sub(r'\s+', ' ', text).strip())


def contains_english(text):
    return bool(re.search(r'[a-zA-Z]', text))

# Filter the DataFrame excluding the first row
filtered_df = df1[1:][df1['school'][1:].apply(contains_english)]
filtered_df


df1 = df1[df1['school_id'] != 20852]

# Lists of patterns to replace
patterns_ma_vi = [
    'माबी', 'उ म बि','मवि','म्ाा बी',
    'उ०मा०वि',
    'उच्च मा',
    'उच्चमा',
     'उमा वि',
     'माध्यामिक वि'
    'मा वी',
    'मा बी',
    'मावि',
'माबि',
'मा बि',
'मावी']



patterns_pra_vi = [ 'प्राबि',
 'प्रावि',
'प्रा बि',
'प्र बि',
 'प्राबी',
'प्रँ ीव्',
'प््राा वि',
'प्र्रा वि',
'प्र बि',
'प्रा बी',
'प्रा वी',
'प्र वि',
'प्र बि',
 'प्रावी',
'प््राा वि',
'प््राा वि',
'प्रा ब',
 'प्रवि', 
 'प्ा बि',
 'प्रा ि',
'प्रा। वी',
'प्र वी',
'प्रा स्कूल',
'प्राइमरी स्कुलप्रोवि', 
'प्राथमीक वि',
 'प््राावि',
 'जप्र्रावि',
 'प्रावऽि']
patterns_ni_ma = ['नि म','नि मा।वि']
patterns_aa_vi = ['आवि','आबि']
patterns_general = {
      'त्रि बि': 'त्रि वि',
    'नेराप्रवि': 'नेरा प्रा वि',
    'प्रा बाग्लुङ': 'प्रा वि बाग्लुङ',
    'निमा': 'नि मा', 
      'भूमे प्रा िचितवन': 'भूमे प्रा वि चितवन',
     'माध्यमिक': 'मा',
    'विद्यालय': 'वि',
    'निम्न': 'नि',
    'प्रा ली': 'प्रा लि',
    'विधालय': 'वि',
    'प्राथमिक': 'प्रा',
    'आधारभूत': 'आ',
    'बिधालय': 'वि',
    'बिद्यालय': 'वि',
    'विदोकानडाँडा': 'वि दोकानडाँडा',
    'दरवार हाइस्कुल': 'दरवार हाइस्कुल मा वि',
    r'\bबी\b': 'बि',
    r'\bबि\b': 'वि',
    'तनहु': 'तनहुँ',
    'नि मा िपर्बत':'नि मा वि पर्बत',
    'नि म बि':'नि मा वि',
    'नि वा':'नि मा वि',
    'त्रि वि': 'त्रिवि',
    'मा ि' : 'मा वि ',
    'नेराप्रा।वि': 'नेरा प्रा वि',
    'वि पी': 'विपी',
    'तनहूँ': 'तनहुँ',
    'तनुहुँ': 'तनहुँ',
    'धनकुटा थाकले': 'थाकले धनकुटा',
    'नेराप्रा वि': 'नेरा प्रा वि',
    'निङ्गलाखसैनी बेतडि आ वि': 'निङ्गलाखसैनी आ वि बेतडि',
    'सरस्वती आ वि मा वि अर्खौले': 'सरस्वती-आवि मा वि अर्खौले',
    'ने रा वि': 'नेरावि',
    'ना वि मा': "नि वि मा",
    'वि मा वि' :'नि मा वि'

}

# Function to apply replacements from lists
def replace_patterns(df, patterns, replacement):
    for pattern in patterns:
        df['school'] = df['school'].replace({pattern: replacement}, regex=True)
    return df

# Apply general replacements
df1['school'] = df1['school'].replace(patterns_general, regex=True)

# Apply grouped replacements
df1 = replace_patterns(df1, patterns_ma_vi, 'मा वि')
df1 = replace_patterns(df1, patterns_pra_vi, 'प्रा वि')
df1 = replace_patterns(df1, patterns_ni_ma, 'नि मा वि')
df1 = replace_patterns(df1, patterns_aa_vi, 'आ वि')
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
(df1[['Root_name']] == '').sum()

# Check for empty strings
emptydf1 = df1[['Root_name']] == ''
rows_with_empty_strings = df1[emptydf1.any(axis=1)]
rows_with_empty_strings.head(100)
len(rows_with_empty_strings)




df1[df1['Root_name'].isnull() | (df1['Root_name'] == '')]


# Define the keywords to check
keywords = ['मा वि', 'प्रा वि', 'नि मा वि', 'आ वि']

# Function to update Root_name based on the school column
def update_root_name(row):
    if pd.isnull(row['Root_name']) or row['Root_name'] == '':
        for keyword in keywords:
            if keyword in row['school']:
                return keyword
    return row['Root_name']

# Apply the function to update the Root_name column
df1['Root_name'] = df1.apply(update_root_name, axis=1)


df1['School_level'].unique()

# Filter out rows where School_level is null or an empty string
df1 = df1[~df1['School_level'].isnull() & (df1['School_level'] != '')]


df1.dtypes
df1.head()

# Filter rows where district1 is not equal to Potential_District_Name
unequal_districts = df1[df1['district1'] != df1['Potential_District_Name']]


# Remove unnecessary spaces from the specified columns
df1['district1'] = df1['district1'].str.strip()
df1['Potential_District_Name'] = df1['Potential_District_Name'].str.strip()

# Filter rows where district1 is not equal to Potential_District_Name
unequal_districts = df1[df1['district1'] != df1['Potential_District_Name']]
unequal_districts[['district1','Potential_District_Name']].head()











# Remove unnecessary spaces from the specified columns
df1['district1'] = df1['district1'].str.strip()
df1['Potential_District_Name'] = df1['Potential_District_Name'].str.strip()

# Function to calculate the percentage of matching characters
def matching_percentage(row):
    district1 = row['district1']
    potential_district = row['Potential_District_Name']
    
    if pd.isna(district1) or pd.isna(potential_district) or len(district1) == 0 or len(potential_district) == 0:
        return 0.0
    
    matches = sum(1 for a, b in zip(district1, potential_district) if a == b)
    total_chars = max(len(district1), len(potential_district))
    return (matches / total_chars) * 100

# Apply the function and create a new column for the percentage
df1['Match_Percentage'] = df1.apply(matching_percentage, axis=1)

df1[['district1','Potential_District_Name','Match_Percentage']].head(100)
# Find the range of percentages
min_percentage = df1['Match_Percentage'].min()
max_percentage = df1['Match_Percentage'].max()

# Print the range of percentages
print(f"Range of Match_Percentage: {min_percentage:.2f}% to {max_percentage:.2f}%")


# Get unique values and sort them in ascending order
unique_percentages = sorted(df1['Match_Percentage'].unique())
unique_percentages


# Get unique values and their counts
unique_percentages_counts = df1['Match_Percentage'].value_counts().sort_index()

# Print unique values and their counts
print("Unique Match_Percentage values and their counts:")
print(unique_percentages_counts)

# Print rows where Match_Percentage is less than 50
rows_less_than_50 = df1[df1['Match_Percentage'] == 0]
print("\nRows where Match_Percentage is less than 50:")
rows_less_than_50[['district1','Potential_District_Name','Match_Percentage']]

# Filter rows where Match_Percentage is less than 10 and greater than 0
filtered_rows = df1[(df1['Match_Percentage'] < 10) & (df1['Match_Percentage'] > 0)]
filtered_rows[['district1','Potential_District_Name','Match_Percentage']]

df1['School_level'].unique()



df1_modified = df1[['school_id','Potential_School_Name','Potential_Location','Potential_District_Name','Root_name','School_level','Match_Percentage']]

df1_modified.head()



len(df1_modified['Potential_District_Name'].unique())
df1_modified['Potential_District_Name'].unique()
df1_modified['Potential_District_Name'].isnull().sum()

df1_modified[df1_modified['Potential_District_Name'].isnull()]
df1_modified.to_csv('modified_AAA.csv',index=False)


# Ensure you are working on a copy to avoid the warning
df1_modified = df1_modified.copy()

# Use .loc to modify the column in place
df1_modified.loc[:, 'Potential_District_Name'] = df1_modified['Potential_District_Name'].str.strip()

# Save the DataFrame to CSV
df1_modified.to_csv('modified_AAA.csv', index=False)

# Load the CSV file
df_mess = pd.read_csv('modified_AAA.csv')

# Check for null values
null_count = df_mess['Potential_District_Name'].isnull().sum()
print(f"Null values in Potential_District_Name after loading CSV: {null_count}")

# Verify unique values
unique_potential_districts = df_mess['Potential_District_Name'].unique()
print(f"Unique Potential_District_Name values: {unique_potential_districts}")

# Check for null rows
null_rows = df_mess[df_mess['Potential_District_Name'].isnull()]
null_rows.head()







df_mess = pd.read_csv('./modified_AAA.csv')
len(df_mess['Potential_District_Name'].unique())
df_mess['Potential_District_Name'].unique()
df_mess['Potential_District_Name'].isnull().sum()

df_mess[df_mess['Potential_District_Name'].isnull()]


df1 = df1.drop(columns=['school','velthuis','district1','confidence','all_matches','Match_Percentage'])
df1.dtypes
df1['Potential_School_Name'].head(100)


df2.shape
df2.columns
df2.dtypes
df2.head()
df2.duplicated().sum()

df2.shape
df2.dtypes
df2.columns
df2.tail(10)





import pandas as pd
from indicnlp.tokenize import indic_tokenize
import re
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows',None)
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load Source B
df2 = pd.read_csv('data/school_list_B.tsv', sep='\t')

# Remove ':', '-', and '।' from the 'school' column
df2 = df2.apply(lambda text: text.replace(':', ' ')
                                          .replace('-', ' ')
                                          .replace('.', ' ')
                                          .replace('।', ' ')
                                          .replace('(', ' ')
                                          .replace(',', ' ')
                                          .replace(')', ' '))

# Apply the cleaning function to remove commas, "॰", Devanagari numbers, and "ः"

df2['name'] = df2['name'].apply(lambda text: re.sub(r'[,:\-।\(\)0123456789]', ' ', text).strip())
df2['name'] = df2['name'].apply(lambda text: re.sub(r'\s+', ' ', text).strip())
df2['name'] = df2['name'].apply(lambda text: text.lower())
df2 = df2.applymap(lambda text: text.lower() if isinstance(text, str) else text)
# Remove full stops from all text entries in the DataFrame
df2 = df2.applymap(lambda text: re.sub(r'\.', '', text) if isinstance(text, str) else text)

df2['name'].head(200)
# df2.head()


# Replacement dictionary
replace_dict = {
    'ni ma v':'नि मा वि', 
    'aadharbhut bidhyalaya': 'आ वि',
    'prathamik bidhyalaya':'प्रा वि',
    'prathamik vidhyalaya':'प्रा वि',
    'adharbhut vidhyalaya': 'आ वि',
    'adharbhut vidyalaya': 'आ वि',
    'sec. school': 'मा वि',
    'aa vi':'आ वि', 
    'aa v':'आ वि',
    'adharbhoot vidhyalaya': 'आ वि',
    'aadharbhut vidhyalaya': 'आ वि',
     'adharbhut v': 'आ वि',
    'pre primary school': 'आ वि',
    'aadharbhut bidyalaya': 'आ वि',
    'adharbhut': 'आ',
    'adharbhut pra v': 'adharbhut प्रा वि',
    'adharbhoot v': 'आ वि',
    'adharbhut': 'आ',
    'adharbhut': 'आ',
    'aadharbhut': 'आ',
    'aadharbhut': 'आ',
    'aadharvut': 'आ',
    'basic school':'आ वि',
    'aa. v':'आ वि',
    'aa. vi.':'आ वि',
    'aadharvut vidyalaya':'आ वि',
    'pra v':'प्रा वि',
    'ma v':'मा वि',
    'primary school':'प्रा वि',
    'pre primary school':'आ वि', 
    'pra vi':'प्रा वि', 
    'adhar v':'आ वि', 
    'pre school':'आ वि',
    'pvt ltd':'प्रा वि', 
    'high school':'मा वि',
    'secondary school':'मा वि', 
    'madhyamik':'मा', 
    'ma vi.':'मा वि', 	
    'ma vi':'मा वि',
    'pvt.ltd':'प्रा लि',
    'pvtltd':'प्रा लि',
    'mavi':'मा वि',
    'secondary':'मा',
    'school': 'वि',
    'bidhyalay': 'वि',
    'vidyalaya': 'वि',
    'vidhyalaya': 'वि',
    'bidyalaya': 'वि',
    'मा विi':'मा वि',
    'प्रा विi':'प्रा वि',
    'adarsha basic':'adarsha आ',
}
    
    


# Function to replace words based on the dictionary
def replace_words(text, replace_dict):
    for word, replacement in replace_dict.items():
        text = text.replace(word, replacement)
    return text

# Apply the replacement function to the 'name' column
df2['modified_name'] = df2['name'].apply(lambda text: replace_words(text, replace_dict))

df2[['name','modified_name']].head(200)

df2.head(100)
df2['district'].unique()

df2['modified_name'].isnull().sum()
df2.to_csv('updated_merged_school_data_B.csv',index=False)














import pandas as pd
from indicnlp.tokenize import indic_tokenize
import re
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows',None)
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
# Load Source B
df2 = pd.read_csv('/Users/mahesh/Documents/GitHub/incubator/Refine_incubator/preprocess/school_list_B.tsv', sep='\t')

# Define the cleaning function
def clean_text(text):
    if isinstance(text, str):
        text = re.sub(r'[:,\-।().]', ' ', text)  # Replace specified characters with a space
        text = re.sub(r'[0-9]', ' ', text)  # Remove numbers
        text = re.sub(r'\s+', ' ', text).strip()  # Replace multiple spaces with a single space and strip leading/trailing spaces
        return text.lower()
    else:
        return text

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
    'aadharbhut': 'आ',
    'aadharvut': 'आ',
    'basic school':'आ वि',
    'aa. v':'आ वि',
    'aa. vi.':'आ वि',
    'aadharvut vidyalaya':'आ वि',
    'aadharboot':'आ',
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
    'adarsha basic':'adarsha आ'
}

# Function to replace words based on the dictionary
def replace_words(text, replace_dict):
    if isinstance(text, str):
        for word, replacement in replace_dict.items():
            text = text.replace(word, replacement)
    return text

# Identify text columns
text_columns = df2.select_dtypes(include='object').columns

# Apply the cleaning function to all text columns, handling missing values
for col in text_columns:
    df2['modified_' + col] = df2[col].apply(lambda x: clean_text(x) if pd.notnull(x) else '')

# Apply the replacement function to all text columns
for col in text_columns:
    df2['modified_' + col] = df2['modified_' + col].apply(lambda x: replace_words(x, replace_dict) if pd.notnull(x) else '')

# Remove full stops from all text entries in the DataFrame
df2 = df2.applymap(lambda text: re.sub(r'\.', '', text) if isinstance(text, str) else text)


df2.head()
# # Drop the original columns
# df2.drop(columns=text_columns, inplace=True)

df2.head(10)



df2['modified_name'].isnull().sum()
df2.to_csv('preprocessed_after_B_1.csv',index=False)


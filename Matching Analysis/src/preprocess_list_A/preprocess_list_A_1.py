import pandas as pd
import re
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

# Function to load and preprocess the school list
def load_and_preprocess_school_list(file_path):
    # Load the TSV file with error handling for problematic rows
    df = pd.read_csv(file_path, sep='\t', on_bad_lines='skip')
    
    # Remove specified columns
    df = df.drop(columns=['velthuis', 'district1', 'confidence', 'all_matches'])
    
    # Create a new column 'school_1' with the same values as 'school'
    df['school_1'] = df['school']
    
    # Apply the specified transformations to the 'school_1' column
    df['school_1'] = df['school_1'].apply(lambda text: text.replace(':', ' ')
                                          .replace('-', ' ')
                                          .replace('.', ' ')
                                          .replace('।', ' ')
                                          .replace('(', ' ')
                                          .replace(',', ' ')
                                          .replace(')', ' ')
                                          .replace('॰', ' ')
                                          .replace('ः', ' '))
    

    
    df['school_1'] = df['school_1'].apply(lambda text: re.sub(r'[,:\-।\(\)॰०१२३४५६७८९]', ' ', text).strip())
    df['school_1'] = df['school_1'].apply(lambda text: re.sub(r'\s+', ' ', text).strip())
    df['school_1'] = df['school_1'].apply(lambda text: text.lower())
    
    # Apply general replacements
    patterns_general = {
        'त्रि बि': 'त्रि वि', 'नेराप्रवि': 'नेरा प्रा वि', 'प्रा बाग्लुङ': 'प्रा वि बाग्लुङ', 
        'निमा': 'नि मा', 'भूमे प्रा िचितवन': 'भूमे प्रा वि चितवन', 'माध्यमिक': 'मा', 
        'विद्यालय': 'वि', 'निम्न': 'नि', 'प्रा ली': 'प्रा लि', 'विधालय': 'वि', 
        'प्राथमिक': 'प्रा', 'आधारभूत': 'आ', 'बिधालय': 'वि', 'बिद्यालय': 'वि', 
        'विदोकानडाँडा': 'वि दोकानडाँडा', 'दरवार हाइस्कुल': 'दरवार हाइस्कुल मा वि', 
        r'\bबी\b': 'बि', r'\bबि\b': 'वि', 'तनहु': 'तनहुँ', 'नि मा िपर्बत': 'नि मा वि पर्बत', 
        'नि म बि': 'नि मा वि', 'नि वा': 'नि मा वि', 'त्रि वि': 'त्रिवि', 'मा ि': 'मा वि', 
        'नेराप्रा।वि': 'नेरा प्रा वि', 'वि पी': 'विपी', 'तनहूँ': 'तनहुँ', 'तनुहुँ': 'तनहुँ', 
        'धनकुटा थाकले': 'थाकले धनकुटा', 'नेराप्रा वि': 'नेरा प्रा वि', 
        'निङ्गलाखसैनी बेतडि आ वि': 'निङ्गलाखसैनी आ वि बेतडि', 
        'सरस्वती आ वि मा वि अर्खौले': 'सरस्वती-आवि मा वि अर्खौले', 'ने रा वि': 'नेरावि', 
        'ना वि मा': "नि वि मा", 'वि मा वि' :'नि मा वि', 'विा': 'वि','कालीका मा':'कालीका मा वि'
        
    }
    df['school_1'] = df['school_1'].replace(patterns_general, regex=True)

    # Patterns to replace
    patterns_ma_vi = [
        'माबी', 'उ म बि', 'मवि', 'म्ाा बी', 'उ०मा०वि', 'उच्च मा', 
        'उच्चमा', 'उमा वि', 'माध्यामिक वि', 'मा वी', 'मा बी', 'मावि', 
        'माबि', 'मा बि', 'मावी', 'उ मा वि','माध्यमिक','म वि','उ मा'
    ]
    
    patterns_pra_vi = [
        'प्राबि','प्रो वि', 'प्रावि','प्रा॰वऽि', 'प्रा बि', 'प्र बि', 'प्राबी', 'प्रँ ीव्', 
        'प््राा वि', 'प्र्रा वि', 'प्रा बी', 'प्रा वी', 'प्र वि', 'प्रावी', 
        'प््राा वि', 'प्रा ब', 'प्रवि', 'प्ा बि', 'प्रा ि', 'प्रा। वी', 
        'प्र वी', 'प्रा स्कूल', 'प्राइमरी स्कुलप्रोवि', 'प्राथमीक वि', 
        'प््राावि', 'जप्र्रावि', 'प्रावऽि','प्रँ बि'
    ]
    patterns_ni_ma = [
        'नि म', 'नि मा।वि', 'नि मा विा वि'
    ]
    patterns_aa_vi = [
        'आवि', 'आबि'
    ]

    # Function to apply replacements from lists
    def replace_patterns(df, patterns, replacement):
        for pattern in patterns:
            df['school_1'] = df['school_1'].replace({pattern: replacement}, regex=True)
        return df

    # Apply grouped replacements
    df = replace_patterns(df, patterns_ma_vi, 'मा वि')
    df = replace_patterns(df, patterns_pra_vi, 'प्रा वि')
    df = replace_patterns(df, patterns_ni_ma, 'नि मा वि')
    df = replace_patterns(df, patterns_aa_vi, 'आ वि')

    # Apply final replacements
    df['school_1'] = df['school_1'].replace('नि मा वि', 'निमावि', regex=True)
    df['school_1'] = df['school_1'].replace('मा वि', 'मावि', regex=True)
    df['school_1'] = df['school_1'].replace('प्रा वि', 'प्रावि', regex=True)
    df['school_1'] = df['school_1'].replace('आ वि', 'आवि', regex=True)

    # Create School_level column
    df['School_level'] = df['school_1'].apply(lambda text: re.findall(r'(मावि|निमावि|प्रावि|आवि)', text))
    df['School_level'] = df['School_level'].apply(lambda x: x[0] if x else '')

    # Create School_name and Location columns
    df['School_name'] = df.apply(lambda row: row['school_1'].split(row['School_level'])[0].strip() if row['School_level'] else row['school_1'], axis=1)
    df['Location'] = df.apply(lambda row: row['school_1'].split(row['School_level'])[1].strip() if row['School_level'] and len(row['school_1'].split(row['School_level'])) > 1 else '', axis=1)
    
    # Drop school_2 column if exists
    if 'school_2' in df.columns:
        df = df.drop(columns=['school_2'])
    
    return df

# Function to load district list
def load_jilla(file_path):
    # Load the CSV file without header
    df = pd.read_csv(file_path, header=None, names=['District_Nepal'])
    return df

# Load the provided school list and district list
file_path_school_list = './school_list_A.tsv'
file_path_district_list = './jilla.csv'

# Load and preprocess the school list
df_school_list = load_and_preprocess_school_list(file_path_school_list)

# Load the district list
df_district_list = load_jilla(file_path_district_list)

# Get the list of districts
district_list = df_district_list['District_Nepal'].tolist()

# Extract the last word from Location and store it in Potential_district
df_school_list['Potential_district'] = df_school_list['Location'].apply(lambda x: x.split()[-1] if len(x.split()) > 0 else '')
df_school_list.head()

# output_cleaned_file_path = './school_list_AA_1.csv'
# df_school_list.to_csv(output_cleaned_file_path, index=False)


# Create the Location_1 column by excluding the last word if there are more than one word
def create_location_1(location):
    words = location.split()
    if len(words) > 1:
        location_1 = ' '.join(words[:-1])
    else:
        location_1 = ''
    return location_1

df_school_list['Location_1'] = df_school_list['Location'].apply(create_location_1)

# Drop fuzzy matching related columns if they exist
if 'Matched_district' in df_school_list.columns:
    df_school_list = df_school_list.drop(columns=['Matched_district', 'Match_percent'])

df_school_list.head()

# Save the cleaned data to a new CSV file
output_cleaned_file_path = './Preprocessed_after_A_1.csv'
output_cleaned_file_path = './school_list_AA_2.csv'
df_school_list.to_csv(output_cleaned_file_path, index=False)

# Print statistics and sample data
print("Cleaned data sample:")
df_school_list.head(10)
df_school_list.columns

df_school_list.isnull().sum()


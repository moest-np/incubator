import os
import sys
import pandas as pd
import re
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from fuzzywuzzy import process, fuzz
import logging

# Add the path to the directory containing pattern_replacement_A.py
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from pattern_replacement_A import patterns_general, patterns_ma_vi, patterns_pra_vi, patterns_ni_ma, patterns_aa_vi

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Function to load the school list
def load_school_list(file_path):
    try:
        df = pd.read_csv(file_path, sep='\t', on_bad_lines='skip')
        return df
    except Exception as e:
        logging.error(f"An error occurred while loading the file: {e}")
        return None

# Function to load the district list
def load_jilla(file_path):
    try:
        df = pd.read_csv(file_path, sep='\t')
        df.columns = ['district_id', 'district', 'जिल्ला']
        return df
    except Exception as e:
        logging.error(f"An error occurred while loading the district file: {e}")
        return None

# Function to clean the data
def clean_data(df):
    df = df.drop_duplicates()
    df = df.fillna('')
    columns_to_drop = ['velthuis', 'district1', 'confidence', 'all_matches', 'Potential_district_transliterated_transliterated', 'Matched_district_transliterated_transliterated']
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')
    return df

# Function to replace patterns in the DataFrame
def replace_patterns(df, patterns, replacement):
    for pattern in patterns:
        df['school_1'] = df['school_1'].apply(lambda text: re.sub(pattern, replacement, text))
    return df

# Function to preprocess the 'school' column
def preprocess_school_column(df):
    df['school_1'] = df['school']
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

    df['school_1'] = df['school_1'].replace(patterns_general, regex=True)
    
    df = replace_patterns(df, patterns_ma_vi, 'मा वि')
    df = replace_patterns(df, patterns_pra_vi, 'प्रा वि')
    df = replace_patterns(df, patterns_ni_ma, 'नि मा वि')
    df = replace_patterns(df, patterns_aa_vi, 'आ वि')

    df['school_1'] = df['school_1'].replace('नि मा वि', 'निमावि', regex=True)
    df['school_1'] = df['school_1'].replace('मा वि', 'मावि', regex=True)
    df['school_1'] = df['school_1'].replace('प्रा वि', 'प्रावि', regex=True)
    df['school_1'] = df['school_1'].replace('आ वि', 'आवि', regex=True)
    
    return df

# Function to extract school details
def extract_school_details(df):
    df['School_level'] = df['school_1'].apply(lambda text: re.findall(r'(मावि|निमावि|प्रावि|आवि)', text))
    df['School_level'] = df['School_level'].apply(lambda x: x[0] if x else '')

    df['School_name'] = df.apply(lambda row: row['school_1'].split(row['School_level'])[0].strip() if row['School_level'] else row['school_1'], axis=1)
    df['Potential_location'] = df.apply(lambda row: row['school_1'].split(row['School_level'])[1].strip() if row['School_level'] and len(row['school_1'].split(row['School_level'])) > 1 else '', axis=1)
    
    df['Potential_district'] = df['Potential_location'].apply(lambda x: x.split()[-1] if len(x.split()) > 0 else '')

    return df

# Function to transliterate columns
def transliterate_columns(df):
    df['school_1_transliterate'] = df['school_1'].apply(lambda x: transliterate(x, sanscript.DEVANAGARI, sanscript.ITRANS).lower() if x else '')
    df['potential_district_transliterate'] = df['Potential_district'].apply(lambda x: transliterate(x, sanscript.DEVANAGARI, sanscript.ITRANS).lower() if x else '')
    df['school_level_transliterate'] = df['School_level'].apply(lambda x: transliterate(x, sanscript.DEVANAGARI, sanscript.ITRANS).lower() if x else '')
    df['school_name_transliterate'] = df['School_name'].apply(lambda x: transliterate(x, sanscript.DEVANAGARI, sanscript.ITRANS).lower() if x else '')
    return df


def fuzzy_match_individual_words(df, district_df):
    district_list = district_df['district'].tolist()
    
    # Dictionary for specific transformations
    transformations = {
        'sya~naja': 'Syangja',
        'sya~nja': 'Syangja',
        'kabhre': 'Kavrepalanchok',
        'rukuma': 'Rukum',
        'maera~na': 'Morang',
        'saya~naja': 'Syangja',
        'mavichitavana': 'mavi Chitwan',
        'pravichitavana': 'pravi Chitwan',
        'viratanagara': 'Morang',
        'nimavimakavanapura': 'nimavi makavanapura',
    }

    def apply_transformations(word):
        return transformations.get(word, word)

    def match_word_to_district(word):
        if word:
            match = process.extractOne(word, district_list, scorer=fuzz.ratio)
            if match and match[1] > 60:
                return match[0], match[1]
        return '', 0
    
    def match_row(row):
        words = row['school_1_transliterate'].split()
        best_match = ('', 0)
        for word in words:
            transformed_word = apply_transformations(word)
            match, score = match_word_to_district(transformed_word)
            if score > best_match[1]:
                best_match = (match, score)
        return best_match[0], f"{best_match[1]}%"
    
    def update_row(row):
        matched_district, fuzzy_score = match_row(row)
        if fuzzy_score[:-1].isdigit() and int(fuzzy_score[:-1]) > 60:
            row['matched_district'] = matched_district
            row['fuzzy_score'] = fuzzy_score
            row['Potential_district'] = matched_district
            row['potential_district_transliterate'] = transliterate(matched_district, sanscript.ITRANS, sanscript.DEVANAGARI).lower()
        return row
    
    df = df.apply(update_row, axis=1)
    return df

if __name__ == "__main__":
    base_dir = os.getcwd()
    raw_data_dir = os.path.normpath(os.path.join(base_dir, '../../data/raw'))
    file_path_school_list = os.path.join(raw_data_dir, 'school_list_A.tsv')
    file_path_district_list = os.path.join(raw_data_dir, 'jilla.tsv')
    
    df_school_list = load_school_list(file_path_school_list)
    df_district_list = load_jilla(file_path_district_list)
    
    if df_school_list is not None and df_district_list is not None:
        logging.info("Data loaded successfully.")
        try:
            df_school_list = clean_data(df_school_list)
            df_school_list = preprocess_school_column(df_school_list)
            df_school_list = extract_school_details(df_school_list)
            df_school_list = transliterate_columns(df_school_list)
            df_school_list = fuzzy_match_individual_words(df_school_list, df_district_list)
            
            df_selected_columns = df_school_list[['school_id', 'school', 'school_1', 'school_1_transliterate', 'School_level', 'Potential_location', 'School_name', 'Potential_district', 'potential_district_transliterate', 'school_level_transliterate', 'school_name_transliterate', 'matched_district', 'fuzzy_score']]
            print(df_selected_columns.head())
            
            # Remove rows where 'fuzzy_score' is NaN
            df_selected_columns = df_selected_columns.dropna(subset=['fuzzy_score'])
            
            # Remove rows where both 'school_level_transliterate' and 'matched_district' are null or empty
            df_selected_columns = df_selected_columns[~((df_selected_columns['school_level_transliterate'] == '') & (df_selected_columns['matched_district'] == ''))]

            # Remove rows where 'fuzzy_score' is less than 60%
            df_selected_columns = df_selected_columns[df_selected_columns['fuzzy_score'].astype(str).apply(lambda x: int(x.rstrip('%'))) >= 60]
            
            # Keep only the required columns
            df_final = df_selected_columns[['school_id', 'school_1', 'school_name_transliterate', 'school_level_transliterate', 'matched_district']]
            
            # Save the final data to preprocessed_after_A.csv in the processed folder
            processed_data_dir = os.path.normpath(os.path.join(base_dir, '../../data/processed'))
            os.makedirs(processed_data_dir, exist_ok=True)
            output_file_path = os.path.join(processed_data_dir, 'preprocessed_after_A.csv')
            df_final.to_csv(output_file_path, index=False)
            print(f"Final preprocessed data saved to {output_file_path}")
            
        except Exception as e:
            logging.error(f"An error occurred during data processing: {e}")
    else:
        logging.error("Failed to load data.")




df_school_list.columns
df_school_list.tail(10)
df_school_list.isnull().sum()
(df_school_list=='').sum()

df_selected_columns[['Potential_district', 'potential_district_transliterate', 'matched_district', 'school_1_transliterate', 'fuzzy_score', 'school_1']][df_selected_columns['fuzzy_score'].astype(str).apply(lambda x: int(x.rstrip('%'))) < 60].head(100)
df_selected_columns[['Potential_district', 'potential_district_transliterate', 'matched_district', 'school_1_transliterate', 'fuzzy_score', 'school_1']][df_selected_columns['fuzzy_score'].dropna().astype(str).apply(lambda x: int(x.rstrip('%'))) < 60].head(100)
df_selected_columns[df_selected_columns['fuzzy_score'].isna()].tail(300)
  # Print the row where school_id is 2641
df_selected_columns[df_selected_columns['school_id'] == 2641]

df_school_list[(df_school_list['Potential_district_transliterated']=='')].head()
df_selected_columns[df_selected_columns['school_1_transliterate'].str.contains('navalapura samudayika vi navalapura okhaladhumga')]


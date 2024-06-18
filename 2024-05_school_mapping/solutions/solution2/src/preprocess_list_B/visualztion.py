import os
import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk import ngrams
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Define the function to detect if a string contains Devanagari script
def contains_devanagari(text):
    if isinstance(text, str):
        devanagari_pattern = re.compile('[\u0900-\u097F]+')
        return bool(devanagari_pattern.search(text))
    return False

# Define the function to transliterate if Devanagari is detected
def transliterate_if_devanagari(text):
    if contains_devanagari(text):
        return transliterate(text, sanscript.DEVANAGARI, sanscript.ITRANS)
    return text

def clean_text(text):
    if text is None:  # Check if the text is None (null value)
        return ''
    if isinstance(text, str):
        text = re.sub(r'[:,\-।().]', ' ', text)  # Replace specified characters with a space
        text = re.sub(r'[0-9]', ' ', text)  # Remove numbers
        text = re.sub(r'\s+', ' ', text).strip()  # Replace multiple spaces with a single space and strip leading/trailing spaces
        return text.lower()
    else:
        return ''

# Define the function to check for duplicates and null values
def check_and_clean_data(df):
    df = df.drop_duplicates()
    df = df.fillna('')
    return df

# Define the function to preprocess names
def preprocess_names(df):
    for column in df.columns:
        if df[column].dtype == object:
            df[column] = df[column].astype(str).apply(transliterate_if_devanagari).apply(clean_text)
            if 'name' in column.lower():
                df['modified_' + column] = df[column]
                print(f"Processed column: {column}")
    return df

# Define the function to analyze and visualize frequencies
def analyze_and_visualize(df, columns):
    all_names = []
    for column in columns:
        if df[column].dtype == object:
            all_names.extend(df[column].dropna().tolist())

    # Tokenize the names
    tokens = [token for name in all_names if pd.notna(name) for token in name.split()]

    # Create a frequency count of the tokens
    token_counter = Counter(tokens)
    token_freq_data = pd.DataFrame(token_counter.items(), columns=['Token', 'Frequency']).sort_values(by='Frequency', ascending=False)

    # Generate bigrams and trigrams
    bigrams = list(ngrams(tokens, 2))
    trigrams = list(ngrams(tokens, 3))

    # Create a frequency count of the bigrams and trigrams
    bigram_counter = Counter(bigrams)
    trigram_counter = Counter(trigrams)

    bigram_freq_data = pd.DataFrame(bigram_counter.items(), columns=['Bigram', 'Frequency']).sort_values(by='Frequency', ascending=False)
    trigram_freq_data = pd.DataFrame(trigram_counter.items(), columns=['Trigram', 'Frequency']).sort_values(by='Frequency', ascending=False)

    # Generate a word cloud for tokens
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(tokens))
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Wordcloud of Combined Names Tokens')
    plt.show()

    return token_freq_data, bigram_freq_data, trigram_freq_data

def load_and_preprocess_data(base_dir):
    raw_data_dir = os.path.normpath(os.path.join(base_dir, '../../data/raw'))
    file_path_bb = os.path.join(raw_data_dir, 'school_list_B.tsv')

    # Load Source B
    try:
        df2 = pd.read_csv(file_path_bb, sep='\t')
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

    # Check for duplicates and null values
    df2 = check_and_clean_data(df2)

    # Preprocess the names
    df2 = preprocess_names(df2)

    return df2

def main():
    base_dir = os.getcwd()  # Use current working directory
    
    # Load and preprocess the data
    df2 = load_and_preprocess_data(base_dir)
    if df2 is None:
        print("Data loading failed.")
        return None, None, None, None
    
    # Analyze and visualize initial frequencies
    modified_columns = [col for col in df2.columns if col.startswith('modified_')]
    token_freq_data, bigram_freq_data, trigram_freq_data = analyze_and_visualize(df2, modified_columns)
    
    return df2, token_freq_data, bigram_freq_data, trigram_freq_data

if __name__ == "__main__":
    df2, token_freq_data, bigram_freq_data, trigram_freq_data = main()




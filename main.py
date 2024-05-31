import os
import pandas as pd

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from rapidfuzz import fuzz, process

# Set up the paths
base_dir = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(base_dir, '2024-05_school_mapping', 'data')

# Load the data
dev_nagari_data = pd.read_csv(os.path.join(data_path, 'school_list_A.tsv'), sep="\t")
english_data = pd.read_csv(os.path.join(data_path, 'school_list_B.tsv'), sep="\t")

# Remove duplicates based on school names and district to reduce unnecessary translations
unique_english_data = english_data[~english_data.name.duplicated()][['name']]

# Set up the MT5 model
model_name = 'google/mt5-small-eng2nep'  # Use the appropriate model checkpoint
tokenizer = AutoTokenizer.from_pretrained("d2niraj555/mt5-eng2nep")
model = AutoModelForSeq2SeqLM.from_pretrained("d2niraj555/mt5-eng2nep")
model.eval()

def translate(texts):
    input_ids = tokenizer(texts, return_tensors="pt", padding=True, truncation=True).input_ids
    output_ids = model.generate(input_ids, pad_token_id=tokenizer.eos_token_id)
    translated_texts = [tokenizer.decode(ids, skip_special_tokens=True) for ids in output_ids]
    return translated_texts

# Translate unique school names
batch_size = 5
translations = []
for i in range(0, unique_english_data.shape[0], batch_size):
    batch_translations = translate(unique_english_data['name'][i:i + batch_size].tolist())
    translations.extend(batch_translations)
unique_english_data['name_translated'] = translations

# Map translated names back to the original data
english_data = english_data.merge(unique_english_data, on=['name'], how='left')


# Fuzzy Matching
def match_schools(row):
    school_name = row['name_translated']
    district = row['district']
    possible_matches = dev_nagari_data[dev_nagari_data['district1'] == district]['school']
    best_match, score = process.extractOne(school_name, possible_matches, scorer=fuzz.token_sort_ratio)
    return pd.Series([best_match, score])

english_data[['best_match', 'match_score']] = english_data.apply(match_schools, axis=1)

# Save or print the results
english_data.to_csv('matched_schools.csv', index=False)
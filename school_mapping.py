import pandas as pd
from rapidfuzz import fuzz, process
from indic_transliteration import sanscript

# Load data
source_a = pd.read_csv('data/school_list_A.tsv', sep='\t')
source_b = pd.read_csv('data/school_list_B.tsv', sep='\t')

# Function to transliterate Devanagari text to Romanized text using Velthuis method
def transliterate_text(text):
    return sanscript.transliterate(text, sanscript.DEVANAGARI, sanscript.VELTHUIS)

# Clean and normalize data
source_a['velthuis'] = source_a['school'].apply(lambda x: transliterate_text(x)).str.lower().str.strip()
source_a['district1'] = source_a['district1'].str.lower().str.strip()
source_b['district'] = source_b['district'].str.lower().str.strip()

# Create a dictionary for district name to district id mapping in Source B
district_mapping_b = source_b[['district', 'district_id']].drop_duplicates().set_index('district')['district_id'].to_dict()

# Create a dictionary for district name to district id mapping in Source A (assuming jilla.tsv contains this mapping)
# Assuming 'जिल्ला' is the Devanagari name for 'district' in jilla.tsv
jilla = pd.read_csv('data/jilla.tsv', sep='\t')
district_mapping_a = jilla.set_index('जिल्ला')['district_id'].to_dict()

# Function to match schools based on transliteration and district
def match_schools(source_a, source_b, district_mapping_a, district_mapping_b, threshold=70):
    matches = []
    
    for index, row in source_a.iterrows():
        school_id_a = row['school_id']
        velthuis_name = row['velthuis']
        district_a = row['district1']
        
        # Get district id from district name in Source A
        district_id_a = district_mapping_a.get(district_a)
        
        if district_id_a is not None:
            # Filter Source B schools by district_id
            possible_matches = source_b[source_b['district_id'] == district_id_a]
            
            # Combine names and old names for matching
            possible_names = possible_matches['name'].tolist() + possible_matches[['old_name1', 'old_name2', 'old_name3']].stack().tolist()
            
            # Apply fuzzy matching on combined names
            best_match = process.extractOne(velthuis_name, possible_names, scorer=fuzz.token_sort_ratio)
            
            all_matches = process.extract(velthuis_name, possible_names, scorer=fuzz.token_sort_ratio)
            
            if best_match and best_match[1] >= threshold:
                best_match_name = best_match[0]
                
                # Determine if best match is from current or old names
                if best_match_name in possible_matches['name'].values:
                    best_match_row = possible_matches[possible_matches['name'] == best_match_name].iloc[0]
                else:
                    old_name_matches = possible_matches[possible_matches[['old_name1', 'old_name2', 'old_name3']].apply(lambda x: best_match_name in x.values, axis=1)]
                    if not old_name_matches.empty:
                        best_match_row = old_name_matches.iloc[0]
                    else:
                        continue
                
                school_id_b = best_match_row['school_id']
                
                # Append the match result
                matches.append({
                    'school_id_a': school_id_a,
                    'school_id_b': school_id_b,
                    'match_score': best_match[1],
                    'school_name_a': row['school'],
                    'school_name_b': best_match_row['name'],
                    'district_id_a': district_id_a,
                    'district_a': district_a,
                    'district_b': best_match_row['district'],
                    'confidence': best_match[1],
                    'all_matches': all_matches
                })
    
    return pd.DataFrame(matches)

# Run the matching function
matched_schools = match_schools(source_a, source_b, district_mapping_a, district_mapping_b)

# Save the matching results to a CSV file
matched_schools.to_csv('school_mapping_results.csv', index=False)

print(f"Total matches found: {len(matched_schools)}")

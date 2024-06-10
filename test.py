import pandas as pd
from rapidfuzz import fuzz
import csv

# this is the confidence level for fuzzy matching
fuzzy_similarity = 80

source_a_df = pd.read_csv('2024-05_school_mapping/data/school_list_A.tsv', sep='\t')
source_b_df = pd.read_csv('2024-05_school_mapping/data/school_list_B.tsv', sep='\t')
jilla_df = pd.read_csv('2024-05_school_mapping/data/jilla.tsv', sep='\t')

district_schools_a ={}


# Adding the school_list_a data to the dictionary with district name as key and school id and school name as value
def add_school(district_name, school_id, school_name):
    if district_name not in district_schools_a:
        district_schools_a[district_name] = {}    
    district_schools_a[district_name][school_id]=(school_name)


# Saving the data to the tsv file
def save_to_tsv( school_id_a, school_id_b, school_name_a, school_name_b):
    with open("2024-05_school_mapping/data/school_list.tsv", 'a', newline='', encoding='utf-8') as file:  # it creates school_list.tsv file in 2024-05_school_mapping/data folder
        writer = csv.writer(file, delimiter='\t')        
        writer.writerow([school_id_a, school_id_b, school_name_a, school_name_b])


for index , row in source_a_df.iterrows():
    add_school(row['district1'], row['school_id'], row['velthuis'].split(',')[0].lower())

for index1 , row1 in source_b_df.iterrows():
     district = jilla_df[jilla_df['district'] == row1['district']]['जिल्ला']  
     
     if not district.empty:      
        district_name = district.iloc[0]

        if district_name in district_schools_a:
            for school_id, school_name in district_schools_a[district_name].items():
                similarity = fuzz.ratio(row1["name"].lower(), school_name)  
                similarity1 = fuzz.ratio(str(row1["old_name1"]).lower(), school_name)  
                similarity2 = fuzz.ratio(str(row1["old_name2"]).lower(), school_name)  
                similarity3 = fuzz.ratio(str(row1["old_name3"]).lower(), school_name)  
                
                if similarity> fuzzy_similarity or similarity1 >fuzzy_similarity  or similarity2> fuzzy_similarity or similarity3> fuzzy_similarity:
                  save_to_tsv( school_id,row1['school_id'], school_name, row1['name'])







            
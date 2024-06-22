import pandas as pd
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


df_A = pd.read_csv('../../data/raw/school_list_A.tsv',delimiter='\t')
df_B = pd.read_csv('../../data/raw/school_list_B.tsv',delimiter='\t')
df1 = pd.read_csv('../../data/processed/preprocessed_after_A.csv')
df2 = pd.read_csv('../../data/processed/preprocessed_after_B.csv')
df3 = pd.read_csv('../../results/first attempt/complete_match.csv')
df4 = pd.read_csv('../../results/second attempt/complete_match_comparing_oldname1_level.csv')
df5 = pd.read_csv('../../results/third attempt/complete_match_comparing_oldname2_level.csv')

df_B.head()
df2.shape


#concatenate  root_school_name_A and  school_level_A in df3, and new columns as School_name_A
df_B['address_from_B'] = df_B['location'] + ', ' +  df_B['local_level']+', ' +  df_B['district']+', '+ df_B['province']
#concatenate  root_school_name_A and  school_level_A in df3, and new columns as School_name_A
df3['extracted_school_name_A'] = df3['root_school_name_A'] + ' ' +  df3['school_level_A']
#concatenate  root_school_name_A and  school_level_A in df3, and new columns as School_name_A
df4['extracted_school_name_A'] = df4['root_school_name_A'] + ' ' +  df4['school_level_A']
df4.head()
df5['extracted_school_name_A'] = df5['root_school_name_A'] + ' ' +  df5['school_level_A']



df3['Match_Type'] = df3['Match_Type'].replace( {'District: complete, School level: complete, Root name: complete': 'Matched with school name of B'})
df4['Match_Type'] = df4['Match_Type'].replace( {'District: complete, School level: complete, Root name: complete': 'Matched with old school name1 of B'})
df5['Match_Type'] = df5['Match_Type'].replace( {'District: complete, School level: complete, Root name: complete': 'Matched with old school name2 of B'})


df3 = df3[['school_id_A','school_id_B','extracted_school_name_A','Match_Type']]
df4 = df4[['school_id_A','school_id_B','extracted_school_name_A','Match_Type']]
df5 = df5[['school_id_A','school_id_B','extracted_school_name_A','Match_Type']]


tuple(df.shape for df in [df3,df4,df5])

concated_df = pd.concat([df3,df4,df5])
concated_df.shape



# Merge df1 with concated_df to get filtered_df_1
filtered_df_1 = pd.merge(df1, concated_df, left_on='school_id', right_on='school_id_A', how='inner')

# Filter concated_df to include only those entries where df1['school_id'] matches concated_df['school_id_A']
filtered_df_1 = concated_df[concated_df['school_id_A'].isin(df1['school_id'])]

# Merge the filtered_df_1 with df1 to add the 'school_1' column
filtered_df_1 = pd.merge(filtered_df_1, df1[['school_id', 'school_1']], left_on='school_id_A', right_on='school_id')

# Drop the extra 'school_id' column from the merge
filtered_df_1.drop('school_id', axis=1, inplace=True)

# Merge df_B with filtered_df_1 to add the 'address_from_B' column
filtered_df_1 = pd.merge(filtered_df_1, df_B[['school_id', 'address_from_B']], left_on='school_id_B', right_on='school_id', how='inner')

# Drop the extra 'school_id' column from the merge
filtered_df_1.drop('school_id', axis=1, inplace=True)

# Merge df2 with filtered_df_1 to add the 'name' column
filtered_df_1 = pd.merge(filtered_df_1, df2[['school_id', 'modified_name']], left_on='school_id_B', right_on='school_id', how='inner')

# Drop the extra 'school_id' column from the merge
filtered_df_1.drop('school_id', axis=1, inplace=True)

# Display the resulting DataFrame
filtered_df_1.head()
filtered_df_1['address_from_B'] = filtered_df_1['address_from_B'].replace({',,':','})


filtered_df_1[['modified_name', 'extracted_school_name_A']] = filtered_df_1[['modified_name', 'extracted_school_name_A']].apply(lambda col: col.str.title())
filtered_df_1.head()


filtered_df_1 = filtered_df_1.rename(columns={'school_1':'school_name_A','modified_name':'school_name_B'})


filtered_df_1 = filtered_df_1[['school_id_A','school_id_B','extracted_school_name_A','school_name_A','school_name_B','address_from_B','Match_Type']]



filtered_df_1['address_from_B'] = filtered_df_1['address_from_B'].str.strip().str.lower().str.title()

filtered_df_1.head()

# Sorting by 'school_name_B' in alphabetical order
filtered_df_1 = filtered_df_1.sort_values(by='school_name_B', ascending=True)



filtered_df_1.isna().sum()
filtered_df_1[(filtered_df_1['extracted_school_name_A'].isna())].head()
filtered_df_1 = filtered_df_1.dropna()
filtered_df_1.isnull().sum()
filtered_df_1.to_csv('../../results/final matching data/final_matching_data.csv',index=False)



df_A = pd.read_csv('../../data/raw/school_list_A.tsv',delimiter='\t')
df_B = pd.read_csv('../../data/raw/school_list_B.tsv',delimiter='\t')
tuple(df.shape for df in [df_A,df_B,filtered_df_1])
((29837, 6), (39798, 16), (11764, 7))

((9163, 4), (2144, 4), (505, 4))
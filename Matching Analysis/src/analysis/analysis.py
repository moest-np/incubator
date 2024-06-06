import pandas as pd

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

df = pd.read_csv('./df_Fuzzy_Matches.csv')

df.shape

df.head()

df_3 = df['Fuzzy_match_score' == 3.0 or 3]

df_3 = df[(df['Fuzzy_match_score'] == 3.0) | (df['Fuzzy_match_score'] == 2.5) ]





df_3 = df[(df['Fuzzy_match_score']==3.0) | (df['Fuzzy_match_score']==2.5) & (df['Match_Type'].str.contains('District: complete'))]
df_3.head(100)
df_3.shape
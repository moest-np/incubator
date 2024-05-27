We have schools from two different data sources. Problem is to map each school from Source A to a school in Source B - school_id_a, school_id_b. Please be advised a complete mapping may not be possible.

Discussion thread: https://github.com/moest-np/incubator/discussions/3


## Source A 
~29k schools - data/school_list_A.tsv
* name and address in devanagari in single text field
* Fields
  * school_id: numeric school id 
  * school: name and address in devanagari
  * velthuis: velthuis romanized transliteration (computed)
  * district1: most likely distrct (fuzzy matched using rapidfuzz library)
  * confidence: confidence score out of 100, higher is better, However, there may be wrong matches even for score of 100
  * all_matches: other matches by rapidfuzz


## Source B 
~40k schools - data/school_list_B.tsv 
* name in english
* ward, palika and district in separate fields 
* Up to 3 previous names, where available 
* Fields: 
  * school_id: numeric school id 
  * name: name of school
  * location: school address	
  * address fields : ward local_level_id, local_level, district_id, district, province_id,province	
  * Previous names: old_name1, old_name2, old_name3

One possible strategy is to try to match transliterated value of Source A with Source B, limiting search to schools in same district. Open to other approaches as well. 


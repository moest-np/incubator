# Matching Analysis

This project aims to enhance the accuracy of matching school records between two datasets by implementing a comprehensive text processing and fuzzy matching process.


## Directory Structure
```
solutions2/
├── data/
│   ├── raw/
│   │   ├── school_list_A.tsv
│   │   ├── school_list_B.tsv
│   │   └── jilla.tsv
│   └── preprocessed/
│       ├── preprocessed_after_A.csv
│       ├── preprocessed_after_B.csv
│
├── results/
│   ├── complete_match.csv
│   ├── final_fuzzy_matching.csv
│   ├── preprocessed_after_fuzzy_A.csv
│   ├── preprocessed_after_fuzzy_B.csv
│   └── remaining_after_complete_match.csv
│
├── src/
│   ├── analysis/
│   │   ├── Final_Fuzzy.csv
│   │   ├── analysis.py
│   │   └── analysis_1.py
│   ├── matching_by_fuzzing/
│   │   └── fuzzy_matching.py
│   ├── preprocess_list_A/
│   │   ├── pattern_replacement_A.py
│   │   ├── preprocess_list_A.py
│   │   └── visualization_A.py
│   └── preprocess_list_B/
│       ├── __init__.py
│       ├── pattern_replacement.py
│       ├── preprocess_list_B.py
│       └── visualization.py
│
├── README.md
├── .gitignore
├── requirements.txt

```
## Process Overview

1. **Standardizing School Names**:
   We standardized the school names in the `school_1` column by applying a series of predefined replacements to correct variations and ensure consistent naming conventions. This included handling different spellings, abbreviations, and common typographical errors across the dataset.

   **Examples**:
   - `त्रि बि बाल विद्यालय` -> `त्रि वि बाल वि`
   - `निम्न माध्यमिक विद्यालय` -> `नि मा वि`
   - `माबी उच्च मा विद्यालय` -> `मा वि उच्च मा वि`
   - `उ मा विद्यालय` -> `उ मा वि`
   - `प्राथमिक बिद्यालय` -> `प्रा वि`
   - `निम्न मा विद्यालय` -> `नि मा`
   - `नि मा विा वि` -> `नि मा`
   - `आधारभूत विद्यालय` -> `आ वि`
   - `आवि` -> `आ वि`

2. **Extracting District Information**:
   We extracted the last word from each school's entry, as it represents the district name, and stored this in a new column called "Potential District." We then created another column, "Location_1," which contains the location name without the last word and words after 'वि'. Next, we loaded a list of districts from a `jilla.tsv` file and performed a fuzzy matching process that compares the "Potential District" values with the loaded district list, ensuring high similarity. This method helps in standardizing the district and location information, making the dataset cleaner and more reliable for further analysis.

3. **Transliterating Devanagari Script**:
   We transliterated columns containing Devanagari script into Latin script using the ITRANS scheme, creating new columns with the transliterated text for each original column.

4. **Categorizing School Levels**:
   We categorized the `School_level` column by mapping its unique values to numeric codes, thereby standardizing and simplifying the school level information for further analysis.


5. **Standardizing Names in `school_list_B`**:
   We implemented a comprehensive text replacement process for the school names in the second file (`school_list_B.csv`). This involved defining a dictionary that mapped common variations and abbreviations of school-related terms to their standardized forms. For example, terms like 'primary school' were replaced with 'प्रा वि', and 'secondary school' was replaced with 'मा वि'. We also transliterated columns containing Devanagari scripts.

6. **Extracting and Standardizing School Levels and Names**:
   We defined functions to extract specific school levels (like 'nimavi', 'pravi', 'avi', and 'mavi') and to remove these levels from the school names, creating new columns for the extracted levels and the cleaned root names. Additionally, we analyzed unique districts by identifying and sorting unique district names and their IDs.

7. **Weighted Fuzzy Matching Process**:
   To enhance the accuracy of matching school records between two datasets, we implemented a weighted fuzzy matching process. This process involves three key comparisons: district ID, school level, and root school name. First, we compare the district IDs of the records and assign a score based on whether they are a complete match or not. Similarly, the school levels are compared and scored, both weighted with a score multiplier of 0.5 for complete matches. 
   
   For the root school name comparison, we use the fuzzy matching technique to calculate a similarity score between the names. If the similarity score is 80 or above, it is considered a complete match and assigned a score of 2. Scores between 50 and 79 are considered a partial match with a score of 1, and scores below 50 are considered no match with a score of 0. The total match score is calculated by summing the individual scores from the district, school level, and root name matches. Along with the total score, a description of the match types (complete, partial, no match) for each comparison is generated. This comprehensive matching process ensures a more accurate and reliable alignment of school records across the datasets.

## Sample Result Data
Complete matching

## School Matching Results

| school_id_A | school_id_B | root_school_name_A | root_school_name_B | school_level_A | school_level_B | district_A | district_B | Fuzzy_match_score | Match_Type |
|-------------|-------------|--------------------|--------------------|----------------|----------------|------------|------------|-------------------|------------|
| 1           | 12428       | janapriya          | jana priya         | pravi          | pravi          | bhojpur    | bhojpur    | 3.0               | District: complete, School level: complete, Root name: complete |
| 3           | 11716       | gograha            | gograha            | mavi           | mavi           | morang     | morang     | 3.0               | District: complete, School level: complete, Root name: complete |
| 9           | 11513       | durgeshvari        | durgeshwori        | pravi          | pravi          | bhojpur    | bhojpur    | 3.0               | District: complete, School level: complete, Root name: complete |
| 10          | 42934       | pavitra            | pabitra            | mavi           | mavi           | tanahun    | tanahun    | 3.0               | District: complete, School level: complete, Root name: complete |
| 11          | 42659       | mitrata            | mitrata            | mavi           | mavi           | tanahun    | tanahun    | 3.0               | District: complete, School level: complete, Root name: complete |
| 12          | 42659       | mitrata            | mitrata            | mavi           | mavi           | tanahun    | tanahun    | 3.0               | District: complete, School level: complete, Root name: complete |
| 13          | 15242       | saleva             | salewa             | mavi           | mavi           | bhojpur    | bhojpur    | 3.0               | District: complete, School level: complete, Root name: complete |
| 15          | 1393        | balakanya          | bal kanya          | pravi          | pravi          | bhojpur    | bhojpur    | 3.0               | District: complete, School level: complete, Root name: complete |
| 16          | 12252       | jalpa              | jalpa              | mavi           | mavi           | bhojpur    | bhojpur    | 3.0               | District: complete, School level: complete, Root name: complete |
| 17          | 12119       | jagadishvari       | jagadishwary       | pravi          | pravi          | bhojpur    | bhojpur    | 3.0               | District: complete, School level: complete, Root name: complete |
| 18          | 34887       | pa~nchakanya       | panchakanya        | mavi           | mavi           | chitwan    | chitwan    | 3.0               | District: complete, School level: complete, Root name: complete |
| 19          | 31055       | virendra adarsha   | birendra adarsha   | mavi           | mavi           | chitwan    | chitwan    | 3.0               | District: complete, School level: complete, Root name: complete |
| 21          | 14458       | pa~nchakanya       | pancha kanya       | mavi           | mavi           | bhojpur    | bhojpur    | 3.0               | District: complete, School level: complete, Root name: complete |
| 22          | 11146       | chinta~na devi     | chhintangdevi      | avi            | avi            | bhojpur    | bhojpur    | 3.0               | District: complete, School level: complete, Root name: complete |
| 23          | 1758        | bhimeshvari        | bhimeshwori        | avi            | avi            | bhojpur    | bhojpur    | 3.0               | District: complete, School level: complete, Root name: complete |
| 24          | 15543       | sarasvati          | saraswati          | pravi          | pravi          | bhojpur    | bhojpur    | 3.0               | District: complete, School level: complete, Root name: complete |
| 25          | 41719       | janajyoti          | jana jyoti         | pravi          | pravi          | tanahun    | tanahun    | 3.0               | District: complete, School level: complete, Root name: complete |
| 26          | 42297       | kyaminakota        | kyaminkot          | mavi           | mavi           | tanahun    | tanahun    | 3.0               | District: complete, School level: complete, Root name: complete |
| 27          | 4545        | bhavani            | bhawani            | pravi          | pravi          | tanahun    | tanahun    | 3.0               | District: complete, School level: complete, Root name: complete |
| 29          | 11069       | chandi             | chandi             | avi            | avi            | bhojpur    | bhojpur    | 3.0               | District: complete, School level: complete, Root name: complete |
| 30          | 12169       | jalapa             | jalapa             | avi            | avi            | bhojpur    | bhojpur    | 3.0               | District: complete, School level: complete, Root name: complete |
| 33          | 32558       | jagrriti           | jagriti            | mavi           | mavi           | bhaktapur  | bhaktapur  | 3.0               | District: complete, School level: complete, Root name: complete |
| 34          | 42906       | nirmala            | nirmal             | pravi          | pravi          | tanahun    | tanahun    | 3.0               | District: complete, School level: complete, Root name: complete |
| 35          | 4140        | annapurna          | annapurna          | pravi          | pravi          | tanahun    | tanahun    | 3.0               | District: complete, School level: complete, Root name: complete |
| 37          | 15302       | sa~ngarumba        | sangrumba          | mavi           | mavi           | ilam       | ilam       | 3.0               | District: complete, School level: complete, Root name: complete |
| 38          | 12862       | jivanajyoti        | jiwan jyoti        | mavi           | mavi           | ilam       | ilam       | 3.0               | District: complete, School level: complete, Root name: complete |
| 40          | 16573       | simhadevi          | siddha devi        | avi            | avi            | ilam       | ilam       | 3.0               | District: complete, School level: complete, Root name: complete |
| 41          | 1834        | vijaya             | bijaya             | avi            | avi            | ilam       | ilam       | 3.0               | District: complete, School level: complete, Root name: complete |
| 42          | 13015       | kalika             | kalika             | mavi           | mavi           | bhojpur    | bhojpur    | 3.0               | District: complete, School level: complete, Root name: complete |
| 45          | 12911       | jyoti              | jyoti              | pravi          | pravi          | bhojpur    | bhojpur    | 3.0               | District: complete, School level: complete, Root name: complete |
| 46          | 12911       | jyati              | jyoti              | pravi          | pravi          | bhojpur    | bhojpur    | 3.0               | District: complete, School level: complete, Root name: complete |
| 49          | 14424       | pa~nchakanya       | pancha kanya       | avi            | avi            | bhojpur    | bhojpur    | 3.0               | District: complete, School level: complete, Root name: complete |
| 51          | 4900        | chimkeshvari       | chimkeshwori       | pravi          | pravi          | tanahun    | tanahun    | 3.0               | District: complete, School level: complete, Root name: complete |
| 55          | 12131       | jalakanya          | jal kanya          | avi            | avi            | ilam       | ilam       | 3.0               | District: complete, School level: complete, Root name: complete |
| 57          | 12395       | janakalyana        | jana kalyan        | pravi          | pravi          | ilam       | ilam       | 3.0               | District: complete, School level: complete, Root name: complete |
| 59          | 12405       | janakalyana        | jana kalyan        | pravi          | pravi          | bhojpur    | bhojpur    | 3.0               | District: complete, School level: complete, Root name: complete |
| 62          | 13270       | krrishna           | krishna            | pravi          | pravi          | morang     | morang     | 3.0               | District: complete, School level: complete, Root name: complete |
| 63          | 437         | akala              | akala              | avi            | avi            | tanahun    | tanahun    | 3.0               | District: complete, School level: complete, Root name: complete |
| 66          | 11356       | dhapakharka        | dhap kharka        | pravi          | pravi          | bhojpur    | bhojpur    | 3.0               | District: complete, School level: complete, Root name: complete |
| 67          | 14464       | pa~nchakanya       | pancha kanya       | pravi          | pravi          | bhojpur    | bhojpur    | 3.0               | District: complete, School level: complete, Root name: complete |
| 68          | 475         | amara jyoti        | amar jyoti         | pravi          | pravi          | tanahun    | tanahun    | 3.0               | District: complete, School level: complete, Root name: complete |
| 69          | 12386       | jana kalyana       | jana kalyan        | avi            | avi            | ilam       | ilam       | 3.0               | District: complete, School level: complete, Root name: complete |
| 71          | 11331       | devithana          | devithan           | mavi           | mavi           | bhojpur    | bhojpur    | 3.0               | District: complete, School level: complete, Root name: complete |
| 72          | 478         | amarajyoti         | amar jyoti         | pravi          | pravi          | tanahun    | tanahun    | 3.0               | District: complete, School level: complete, Root name: complete |
| 74          | 41602       | nala devi          | jal devi           | pravi          | pravi          | tanahun    | tanahun    | 3.0               | District: complete, School level: complete, Root name: complete |
| 75          | 41059       | dharma             | dharma             | mavi           | mavi           | tanahun    | tanahun    | 3.0               | District: complete, School level: complete, Root name: complete |
| 76          | 13942       | miklacho           | miklachong         | mavi           | mavi           | ilam       | ilam       | 3.0               | District: complete, School level: complete, Root name: complete |
| 77          | 1994        | buddha             | buddha             | mavi           | mavi           | ilam       | ilam       | 3.0               | District: complete, School level: complete, Root name: complete |
| 78          | 11640       | ratna devi         | ganga devi         | avi            | avi            | ilam       | ilam       | 3.0               | District: complete, School level: complete, Root name: complete |

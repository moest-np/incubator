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

| school_id | school_1                        | school_id_B | name                    | district_id | Matched_District | root_school_name | School_name_transliterated | School_level | school_levels | School_name | Fuzzy_match_score | Match_Type                                               |
|-----------|---------------------------------|-------------|-------------------------|-------------|------------------|------------------|----------------------------|--------------|---------------|-------------|-------------------|----------------------------------------------------------|
| 1         | जनप्रिय प्रावि भोजपुर           | 12428       | jana priya pra v        | 1           | bhojpur          | jana priya       | janapriya                  | प्रावि        | pravi         | जनप्रिय      | 3.0               | District: complete, School level: complete, Root name: complete |
| 2         | छेनखामा प्रावि भोजपुर           | 11142       | chhenkhama basic school | 1           | bhojpur          | chhenkhama       | chenakhama                 | प्रावि        | avi           | छेनखामा      | 2.5               | District: complete, School level: no match, Root name: complete |
| 4         | श्री शंकर मावि गजरकोट तनहुँँ    | 6928        | hari shankar basic school| 46          | tanahun          | hari shankar     | shri shamkara              | मावि          | avi           | श्री शंकर    | 2.0               | District: no match, School level: no match, Root name: complete  |
| 3         | गोग्राहा मावि विराटनगर मोरङ     | 199         | ahale primary school    | 6           | morang           | ahale            | gograha                    | मावि          | pravi         | गोग्राहा      | 1.5               | District: complete, School level: no match, Root name: partial   |
| 5         | जनजागृति मावि तनहुँँ            | 41671       | jana jagriti basic school| 46          | tanahun          | jana jagriti     | janajagrriti               | मावि          | avi           | जनजागृति     | 2.5               | District: complete, School level: no match, Root name: complete |
| 6         | दाङसिङजरे प्रावि भोजपुर         | 1108        | aitabare pra v          | 1           | bhojpur          | aitabare         | da~nasi~najare             | प्रावि        | pravi         | दाङसिङजरे    | 2.0               | District: complete, School level: complete, Root name: partial  |

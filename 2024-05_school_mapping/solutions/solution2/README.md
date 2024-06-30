# Matching Analysis

This project aims to enhance the accuracy of matching school records between two datasets by implementing a comprehensive text processing and fuzzy matching process. We focused on cleaning, standardizing, and matching school names and district information to achieve reliable and consistent results.

## Overview and Results

We processed two primary datasets:

- `school_list_A.tsv` with 29,837 records.
- `school_list_B.tsv` with 39,798 records.

After applying our text processing and matching algorithms, we filtered and matched 11,764 records.

We obtained 
- 9,163 records in the first attempt (comparing school names from `school_list_A`
 with `school_list_B`),
 - 2,144 records in the second attempt (with `old_school_name1`) and
 - 505 records in the third attempt (with `old_school_name2`).

### Matching Efficiency:

- From `school_list_A`: 39.4% of records were matched.
- From `school_list_B`: 29.6% of records were matched.

We obtained the above results by following a structured approach that ensured a high level of accuracy and reliability in matching school records between the two datasets.
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
│   ├── final matching data/ 
│   │   └── final_matching_data.csv
│   ├── first attempt/
│   │   └── complete_match.csv
│   ├── second attempt/
│   │   └── complete_match.csv
│   ├── third attempt/
│   │   └── complete_match.csv
│
├── src/
│   ├── analysis/
│   │   ├── analysis_1.csv
│   │   ├── analysis_2.py
│   │   └── analysis_3.py
│   ├── matching_by_fuzzing/
│   │   └── fuzzy_matching.py
│   ├── preprocess_list_A/
│   │   ├── pattern_r``eplacement_A.py
│   │   ├── preprocess_list_A.py
│   │   └── visualization_A.py
│   └── preprocess_list_B/
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
   We standardized the school names in `school_list_A.csv` and `school_list_B.csv` by applying a series of predefined replacements to correct variations and ensure consistent naming conventions. This included handling different spellings, abbreviations, and common typographical errors across the datasets.

   **Examples**:
   - `निम्न माध्यमिक विद्यालय` -> `निमावि`
   - `उ मा विद्यालय` -> `मावि`
   - `प्राथमिक बिद्यालय` -> `प्रावि`
   - `निम्न मा विद्यालय` -> `निमावि`
   - `नि मा विा` -> `निमावि`
   - `आधारभूत विद्यालय` -> `आवि`

    and many more, check the pattern replacements in the files preprocessed_list_A and preprocessed_list_B.


2. **Extracting District Information**:
   We extracted the last word from each school's entry, as it often represents the district name, and stored this in a new column called "Potential District." We then created another column, "Location_1," which contains the location name without the last word and words after 'वि'. Next, we loaded a list of districts from a `jilla.tsv` file and performed a fuzzy matching process that compares the "Potential District" values with the loaded district list, ensuring high similarity. This method helps in standardizing the district and location information, making the dataset cleaner and more reliable for further analysis.

3. **Transliterating Devanagari Script**:
   We transliterated columns containing Devanagari script into Latin script using the ITRANS scheme, creating new columns with the transliterated text for each original column.

4. **Extracting and Standardizing School Levels and Names**:
   We defined functions to extract specific school levels (like 'nimavi', 'pravi', 'avi', and 'mavi') and to remove these levels from the school names, creating new columns for the extracted levels and the cleaned root names. Additionally, we analyzed unique districts by identifying and sorting unique district names and their IDs.

5. **Weighted Fuzzy Matching Process**:
   To enhance the accuracy of matching school records between the two datasets, we implemented a weighted fuzzy matching process. This process involves three key comparisons: district ID, school level, and root school name. 

   - First, we compare the district IDs of the records and assign a score based on whether they are a complete match or not.
   - Similarly, the school levels are compared and scored, both weighted with a score multiplier of 0.5 for complete matches.
   - For the root school name comparison, we use a fuzzy matching technique to calculate a similarity score between the names. Scores are categorized as follows:
     - Scores 80 and above are considered a complete match (score of 2).
     - Scores between 50 and 79 are considered a partial match (score of 1).
     - Scores below 50 are considered no match (score of 0).

   The total match score is calculated by summing the individual scores from the district, school level, and root name matches. Along with the total score, a description of the match types (complete, partial, no match) for each comparison is generated. This comprehensive matching process ensures a more accurate and reliable alignment of school records across the datasets.

   We conducted three attempts to improve matching accuracy:
   - **First Attempt**: Compared school names from `school_list_A` with those from `school_list_B`.
   - **Second Attempt**: Compared school names from `school_list_A` with the `old_school_name1` column in `school_list_B`.
   - **Third Attempt**: Compared school names from `school_list_A` with the `old_school_name2` column in `school_list_B`.

By following this structured approach, we aimed to ensure a high level of accuracy and reliability in matching school records between the two datasets.

((9163, 4), (2144, 4), (505, 4))


# Sample Results
The following table represents the results of the school matching process, detailing matched records between two datasets. For full matched data please check final_matching_data.csv in results folder. 

For any errors, queries, or suggestions, please feel free to contact me at [maheshtwari99@gmail.com](mailto:maheshtwari99@gmail.com).

| school_id_A | school_id_B | extracted_school_name_A | school_name_A | school_name_B | address_from_B | Match_Type |
|-------------|-------------|-------------------------|---------------|---------------|----------------|------------|
| 3383        | 57          | Ardasha Mavi            | आर्दश मावि खनदह अर्घाखाँची | Aadarsha Mavi | Khanchi Maidan, Sandhikharka Municipality, Arghakhanchi, Lumbini Province | Matched with school name of B |
| 8905        | 2135        | Badaharamala Pravi       | बडहरामाल प्रावि सिराहा | Aadhar Bhut Vi Badaharamal | Karjanha Municipality, Karjanha Municipality, Siraha, Madhesh Province | Matched with old school name2 of B |
| 18685       | 59          | Adharabhuta Mavi         | आधारभुत मावि रामपुर पाल्पा | Aadharbhoot Mavi | Dumrigaun, Palpa, Rampur Municipality, Palpa, Lumbini Province | Matched with old school name1 of B |
| 28767       | 40          | Adharabhuta Avi          | आधारभुत आवि स्याङ्जा | Aadharbhut Avi | Bejhang, Aandhikhola Rural Municipality, Syangja, Gandaki Province | Matched with school name of B |
| 4242        | 320         | Ahalada.Nda Avi          | आहालडाँडा आवि मेलुङ दोलखा | Aahaldanda Avi | Melung, Melung Rural Municipality, Dolakha, Bagamati Province | Matched with school name of B |
| 21643       | 321         | Ajadi Mavi               | आजडी मावि विरौट दोलखा | Aajadi Mavi | Melung, Melung Rural Municipality, Dolakha, Bagamati Province | Matched with school name of B |
| 24535       | 43          | Ama Avi                  | आमा आवि स्याङ्जा | Aama Avi | Chapakot, Chapakot Municipality, Syangja, Gandaki Province | Matched with school name of B |
| 3446        | 519         | Ama Mavi                 | आमा मावि आमा रुपन्देही | Aama Mavi | Aama, Lumbini Sanskritik Municipality, Rupandehi, Lumbini Province | Matched with school name of B |
| 15010       | 520         | Amari Pravi              | अमारी प्रावि अमारी रुपन्देही | Aamari Avi | Aamari, Lumbini Sanskritik Municipality, Rupandehi, Lumbini Province | Matched with old school name1 of B |
| 883         | 117         | Amagachi Pravi           | आमगाछी प्रावि झापा | Aamgachhi Pravi | Amgachhi, Gauriganj Rural Municipality, Jhapa, Koshi Province | Matched with school name of B |
| 19356       | 521         | Anandapura Mavi          | आनन्दपुर मावि गुल्मी | Aanandapur Mavi | Dobata, Isma Rural Municipality, Gulmi, Lumbini Province | Matched with school name of B |
| 12518       | 331         | Arukharka Mavi           | आरुखर्क मावि बेल्कोटगढी नुवाकोट | Aarukharka Mavi | Aarukharka, Belkotgadhi Municipality, Nuwakot, Bagamati Province | Matched with school name of B |
| 28965       | 67          | Autari Pravi             | औतारी प्रावि पाहाडा डोल्पा | Aautari Basic | Pahada, Tripurasundari Municipality, Dolpa, Karnali Province | Matched with old school name1 of B |
| 17748       | 2168        | Abhinandana Pravi        | अभिनन्दन प्रावि सारी जलेश्वर महोत्तरी | Abhinandan Pravi Sari | Jaleshwar, Jaleshwar Municipality, Mahottari, Madhesh Province | Matched with school name of B |
| 2101        | 343         | Achane Mavi              | अचने मावि त्रिपुरासुन्दरी धादिङ | Achane Mavi | Tripurasundari, Tripura Sundari Rural Municipality, Dhading, Bagamati Province | Matched with school name of B |
| 17823       | 130         | Adaraniya Mavi           | आदरणीय मावि इलाम | Adarniya Mavi | Sandakpur, Sandakpur Rural Municipality, Ilam, Koshi Province | Matched with school name of B |
| 302         | 131         | Adarsha Avi              | आदर्श आवि सुन्दरहरैंचा मोरङ | Adarsa Avi | Sundarharaincha, Sundarharaincha Municipality, Morang, Koshi Province | Matched with school name of B |
| 24574       | 724         | Adarsha Mavi             | आदर्श मावि जानकी कैलाली | Adarsh Mavi | Khargauli, Janaki Rural Municipality, Kailali, Sudurpashchim Province | Matched with school name of B |
| 5937        | 542         | Adarsha Mavi             | आदर्श मावि राँझा बाँके | Adarsh Mavi | Laxmanpur, Narainapur Rural Municipality, Banke, Lumbini Province | Matched with school name of B |
| 10396       | 541         | Adarsha Mavi             | आदर्श मावि रामग्राम नवलपरासी | Adarsh Mavi | Nawalparasi, Parasi, Ramgram Municipality, Nawalparasi, Lumbini Province | Matched with school name of B |
| 11623       | 353         | Adarsha Ajada Mavi       | आदर्श आजाद मावि भक्तपुर | Adarsha Ajadh Mavi | Bhelukhel, Bhaktapur Municipality, Bhaktapur, Bagamati Province | Matched with school name of B |
| 26069       | 352         | Adarsha Avi              | आदर्श आवि जुगल सिन्धुपाल्चोक | Adarsha Avi | Jugal, Jugal Rural Municipality, Sindhupalchok, Bagamati Province | Matched with school name of B |
| 17877       | 136         | Adarsha Avi              | आदर्श आवि संखुवासभा | Adarsha Avi | Amrang, Makalu Rural Municipality, Sankhuwasabha, Koshi Province | Matched with school name of B |
| 18147       | 547         | Adarsha Avi              | आदर्श आवि दोभान ज्यामिरे पाल्पा | Adarsha Avi | Tinau, Tinau Rural Municipality, Palpa, Lumbini Province | Matched with school name of B |
| 19610       | 351         | Adarsha Avi              | आदर्श आवि बालमन्दिर नक्साल काठमाडौं | Adarsha Avi | Ramhiti, Kathmandu Metropolitan City, Kathmandu, Bagamati Province | Matched with school name of B |
| 25545       | 611         | Adarsha Avi              | आदर्श आवि कालिकोट | Adarsha Avi | Aulgela, Mahawai Rural Municipality, Kalikot, Karnali Province | Matched with school name of B |
| 27005       | 144         | Adarsha Avi              | आदर्श आवि ओखलढुंगा | Adarsha Avi | Ramche, Siddhicharan Municipality, Okhaldhunga, Koshi Province | Matched with school name of B |
| 5548        | 552         | Adarsha Pravi            | आदर्श प्रावि गोठादी माथागढी पाल्पा | Adarsha Avi | Dambak, Ribdikot Rural Municipality, Palpa, Lumbini Province | Matched with old school name1 of B |
| 12210       | 545         | Adarsha Avi              | आदर्श आवि पाल्पा | Adarsha Avi | Mathagadhi Gaunpalika, Mathagadhi Rural Municipality, Palpa, Lumbini Province | Matched with school name of B |
| 22443       | 147         | Adarsha Avi              | आदर्श आवि कजनी इलाम | Adarsha Avi | Suryodaya Mun.-08, Koshi Province, Ilam, Suryodaya Municipality, Ilam, Koshi Province | Matched with school name of B |
| 28951       | 145         | Adarsha Avi              | आदर्श आवि ताप्लेजुङ | Adarsha Avi | Sirijangha, Sirijangha Rural Municipality, Taplejung, Koshi Province | Matched with school name of B |
| 9736        | 141         | Adarsha Avi              | आदर्श आवि इलाम | Adarsha Avi | Chiyabari, Ilam Municipality, Ilam, Koshi Province | Matched with school name of B |
| 15330       | 546         | Adarsha Avi              | आदर्श आवि चिदिपानी पाल्पा | Adarsha Avi | Jyamire, Tinau Rural Municipality, Palpa, Lumbini Province | Matched with school name of B |
| 15423       | 548         | Adarsha Avi              | आदर्श आवि चंघाट बुद्धभूिम न पा कपिलवस्तु | Adarsha Avi | Suddhodhan, Suddhodhan Rural Municipality, Kapilbastu, Lumbini Province | Matched with school name of B |
| 1379        | 551         | Adarsha Avi              | आदर्श आवि गैरीखुट्टा गुल्मी | Adarsha Avi | Chhatrkot, Chhatrakot Rural Municipality, Gulmi, Lumbini Province | Matched with school name of B |
| 1372        | 412         | Adarsha Avi              | आदर्श आवि सिरानचोक गा पा जौबारी गोरखा | Adarsha Avi | Langdi, Siranchowk Rural Municipality, Gorkha, Gandaki Province | Matched with school name of B |
| 5419        | 729         | Adarsha Avi              | आदर्श आवि मेल्लेख कुस्कोट अछाम | Adarsha Avi | Badchauki, Bannigadhi Jayagadh Rural Municipality, Achham, Sudurpashchim Province | Matched with school name of B |
| 150         | 140         | Adarsha Avi              | आदर्श आवि इलाम न पा इलाम | Adarsha Avi | Soktim, Mai Municipality, Ilam, Koshi Province | Matched with school name of B |
| 29455       | 413         | Adarsha Avi              | आदर्श आवि स्याङजा | Adarsha Avi | Lasargha, Kaligandaki Rural Municipality, Syangja, Gandaki Province | Matched with school name of B |
| 7541        | 732         | Ardasha Pravi            | आर्दश प्रावि साल्घाडी निगाली कैलाली | Adarsha Avi | Bhalauwa, Ghodaghodi Municipality, Kailali, Sudurpashchim Province | Matched with old school name1 of B |
| 20680       | 142         | Adarsha Avi              | आदर्श आवि माइ न पा इलाम | Adarsha Avi | Yang, Suryodaya Municipality, Ilam, Koshi Province | Matched with school name of B |
| 18728       | 553         | Adarsha Pravi            | आदर्श प्रावि देउराली पाल्पा | Adarsha Avi | Mathagadhi Gaunpalika, Mathagadhi Rural Municipality, Palpa, Lumbini Province | Matched with old school name1 of B |
| 10865       | 411         | Ardasha Pravi            | आर्दश प्रावि रापाकोट स्याङजा | Adarsha Avi Khewang | Arjunchaupari, Arjunchaupari Rural Municipality, Syangja, Gandaki Province | Matched with old school name1 of B |
| 12015       | 355         | Adarsha Avi              | आदर्श आवि इच्छाकामना चितवन | Adarsha Avi Laymdar | Lyamdhar, Ichchhakamana Rural Municipality, Chitwan, Bagamati Province | Matched with old school name1 of B |
| 15180       | 2176        | Adarsha Avi              | आदर्श आवि बेहरा नहर क्याम्प बारा | Adarsha Avi Naharcamp | Purano Behara, Jeetpursimara Sub Metropolitan City, Bara, Madhesh Province | Matched with old school name1 of B |
| 9810        | 138         | Adarsha Valika Mavi      | आदर्श वालिका मावि मोरङ | Adarsha Balika Mavi | Gahaile Tole, Biratnagar Metropolitan City, Morang, Koshi Province | Matched with school name of B |
| 26503       | 148         | Adarshasiddha Avi        | आदर्शसिद्ध आवि इलाम | Adarsha Buddha Avi | Bhalukhop, Mai Municipality, Ilam, Koshi Province | Matched with school name of B |
| 6388        | 357         | Adarsha Janapriya Pravi  | आदर्श जनप्रिय प्रावि फापरवारी मकवानपुर | Adarsha Jana Priya Aadharbhut | Lalbhitte, Bagmati Rural Municipality, Makwanpur, Bagamati Province | Matched with old school name1 of B |
| 16618       | 152         | Adarsha Janata Pravi     | आदर्श जनता प्रावि झापा | Adarsha Janata Pravi | Jhapa Ga. Pa, Jhapa Rural Municipality, Jhapa, Koshi Province | Matched with school name of B |
| 1257        | 362         | Adarsha Kanya Niketana Mavi | आदर्श कन्या निकेतन मावि ललितपुर | Adarsha Kanya Niketan Mavi | Mangal Bazar, Lalitpur Metropolitan City, Lalitpur, Bagamati Province | Matched with school name of B |
| 15625       | 735         | Adarsha Manileka Pravi   | आदर्श मणिलेक प्रावि लटसेरा डडेल्धुरा | Adarsha Manilek Pravi Latsera | Latshera, Amargadhi Municipality, Dadeldhura, Sudurpashchim Province | Matched with school name of B |
| 1250        | 132         | Adarsha Mavi             | आदर्श मावि गौरीगंज झापा | Adarsha Mavi | Jayapur, Buddhashanti Rural Municipality, Jhapa, Koshi Province | Matched with school name of B |
| 4608        | 153         | Adarsha Mavi             | आदर्श मावि विराटनगर मोरङ | Adarsha Mavi | Adarsh Tole, Rangeli Municipality, Morang, Koshi Province | Matched with school name of B |
| 2409        | 370         | Aadarsha Mavi            | अादर्श मावि गजुरी धादिङ | Adarsha Mavi | Gajuri, Gajuri Rural Municipality, Dhading, Bagamati Province | Matched with school name of B |
| 9246        | 168         | Adarsha Mavi             | आदर्श मावि बुद्धशान्ति जयपुर झापा | Adarsha Mavi | Aayabari, Mechinagar Municipality, Jhapa, Koshi Province | Matched with school name of B |
| 15893       | 418         | Adarsha Mavi             | आदर्श मावि स्याङ्जा | Adarsha Mavi | Chapakot, Chapakot Municipality, Syangja, Gandaki Province | Matched with school name of B |
| 2410        | 371         | Adarsha Mavi             | आदर्श मावि गजुरी धादिङ | Adarsha Mavi | Thakre,Damechaur, Thakre Rural Municipality, Dhading, Bagamati Province | Matched with school name of B |
| 9480        | 169         | Adarsha Mavi             | आदर्श मावि सफाई धाप धनकुटा | Adarsha Mavi | Saphaidhap,Dhankuta, Sahidbhumi Rural Municipality, Dhankuta, Koshi Province | Matched with school name of B |
| 24291       | 567         | Adarsha Mavi             | आदर्श मावि अर्घाखाँची | Adarsha Mavi | Malarani-3 , Khanadaha, Malarani Rural Municipality, Arghakhanchi, Lumbini Province | Matched with school name of B |
| 1289        | 566         | Ardasha Mavi             | आर्दश मावि वि दिगामकोट गुल्मी | Adarsha Mavi | Chhatrakot, Chhatrakot Rural Municipality, Gulmi, Lumbini Province | Matched with school name of B |
| 1476        | 154         | Adarsha Mavi             | आदर्श मावि मेचीनगर झापा | Adarsha Mavi | Tatuwamari, Gauriganj Rural Municipality, Jhapa, Koshi Province | Matched with school name of B |
| 92          | 167         | Adarsha Mavi             | आदर्श मावि इलाम | Adarsha Mavi | Suntalabari, Ilam Municipality, Ilam, Koshi Province | Matched with school name of B |
| 5813        | 155         | Adarsha Mavi             | आदर्श मावि डाइनियाँ मोरङ | Adarsha Mavi | Sahid Marg, Biratnagar Metropolitan City, Morang, Koshi Province | Matched with school name of B |
| 14544       | 568         | Adarsha Mavi             | आदर्श मावि वर्दिया | Adarsha Mavi | Motipur, Bansgadhi Municipality, Bardiya, Lumbini Province | Matched with school name of B |
| 1811        | 134         | Adarsha Mavi             | आदर्श मावि सुनसरी | Adarsha Mavi | Punarbas, Barahkshetra Municipality, Sunsari, Koshi Province | Matched with school name of B |
| 9545        | 369         | Adarsha Mavi             | आदर्श मावि कागेश्वरी मनहरा भद्रवास काठमाडौं | Adarsha Mavi | Bhadrabas, Kageshwori Manahara Municipality, Kathmandu, Bagamati Province | Matched with school name of B |
| 16691       | 166         | Adarsha Mavi             | आदर्श मावि खेजेनिम ताप्लेजुङ | Adarsha Mavi | Khejenim, Phaktanglung Rural Municipality, Taplejung, Koshi Province | Matched with school name of B |
| 8434        | 621         | Adarsha Mavi             | आदर्श मावि डोल्पा | Adarsha Mavi | Juphal, Thuli Bheri Municipality, Dolpa, Karnali Province | Matched with school name of B |
| 24724       | 422         | Adarsha Mavi             | आदर्श मावि हिस्तान म्याग्दी | Adarsha Mavi | Annapurna-7,Rima, Annapurna Rural Municipality, Myagdi, Gandaki Province | Matched with school name of B |
| 6630        | 560         | Adarsha Mavi             | आदर्श मावि खजुरा बाँके | Adarsha Mavi | Aadarsha Tole, Khajura Rural Municipality, Banke, Lumbini Province | Matched with school name of B |
| 2358        | 365         | Adarsha Mavi             | आदर्श मावि दिव्यनगर चितवन | Adarsha Mavi Bharatpur | Dibyanagar, Bharatpur Metropolitan City, Chitwan, Bagamati Province | Matched with old school name1 of B |
| 6792        | 614         | Adarsha Mavi             | आदर्श मावि वि मेहेली गर्पन सुर्खेत | Adarsha Mavi Lekhpharsha | Lekbeshi, Lekbesi Municipality, Surkhet, Karnali Province | Matched with old school name1 of B |
| 14309       | 133         | Adarsha Mavi             | आदर्श मावि रामधुनी वक्लौरी सुनसरी | Adarsha Mavi Vidhyalaya | Baklauri Bazaar, Ramdhuni Municipality, Sunsari, Koshi Province | Matched with old school name1 of B |
| 1956        | 366         | Adarsha Ra Pravi         | आदर्श रा प्रावि चितवन | Adarsha Pravi | Tarauli, Ratnangar Municipality, Chitwan, Bagamati Province | Matched with school name of B |
| 23795       | 164         | Adarsha Pravi            | आदर्श प्रावि शान्तीनगर झापा | Adarsha Pravi | Bhaishabari, Bhadrapur Municipality, Jhapa, Koshi Province | Matched with school name of B |
| 26917       | 420         | Adarsha Pravi            | आदर्श प्रावि देउपुर पर्वत | Adarsha Pravi | Tapu, Modi Rural Municipality, Parbat, Gandaki Province | Matched with school name of B |
| 1520        | 160         | Adarsha Pravi            | आदर्श प्रावि पथरिया झापा | Adarsha Pravi | Aadarsha Tol, Kachankawal Rural Municipality, Jhapa, Koshi Province | Matched with school name of B |
| 24222       | 163         | Adarsha Pravi            | आदर्श प्रावि तेह्रथुम | Adarsha Pravi | Myanglung, Myanglung Municipality, Tehrathum, Koshi Province | Matched with school name of B |
| 1472        | 159         | Adarsha Pravi            | आदर्श प्रावि झापा | Adarsha Pravi | Harira, Gauriganj Rural Municipality, Jhapa, Koshi Province | Matched with school name of B |
| 26070       | 419         | Adarsha Pravi            | आदर्श प्रावि शितल चौतारी लमजुङ | Adarsha Pravi | Sundarbazar Municipality, Sundarbazar Municipality, Lamjung, Gandaki Province | Matched with school name of B |
| 11008       | 161         | Adarsha Pravi            | आदर्श प्रावि विराटनगर मोरङ | Adarsha Pravi | Tribhuvan Tole, Biratnagar Metropolitan City, Morang, Koshi Province | Matched with school name of B |
| 4559        | 171         | Adarsha Shiksha Niketana Avi | आदर्श शिक्षा निकेतन आवि ग्रामथान मोरङ | Adarsha Sikshya Niketan Avi | Gramthan, Gramthan Rural Municipality, Morang, Koshi Province | Matched with school name of B |
| 22889       | 173         | Adarsha Shishu Pravi     | आदर्श शिशु प्रावि भोजपुर | Adarsha Sishu Pravi | Puranodabali, Bhojpur Municipality, Bhojpur, Koshi Province | Matched with school name of B |
| 23747       | 174         | Adarsha Sita Avi         | आदर्श सीता आवि मोरङ | Adarsha Sita Avi | Ringuwa, Pathari Shanishchare Municipality, Morang, Koshi Province | Matched with school name of B |
| 21021       | 176         | Adarsha Vidya Mandira Mavi | आदर्श विद्या मन्दिर मावि झापा | Adarsha Vidya Mandir Mavi | Kanakai, Kanakai Municipality, Jhapa, Koshi Province | Matched with school name of B |
| 3555        | 377         | Adharabhuta Shiksha Pravi | आधारभुत शिक्षा प्रावि मकवानपुर | Adharbhoot Shiksha Avi | Khaireni, Makawanpurgadhi Rural Municipality, Makwanpur, Bagamati Province | Matched with old school name2 of B |
| 23536       | 425         | Adharabhumi Mavi         | आधारभुमी मावि स्याङजा | Adharbhut Mavi | Chhekma, Harinas Rural Municipality, Syangja, Gandaki Province | Matched with school name of B |
| 481         | 427         | Adharabhuta Mavi         | आधारभुत मावि राईपुर तनहुँँ | Adharbhut Mavi | Sankhe, Shuklagandaki Municipality, Tanahun, Gandaki Province | Matched with school name of B |
| 19860       | 426         | Adharabhuta Pravi        | आधारभुत प्रावि बागलुङ | Adharbhut Pravi | Kafaldanda, Baglung Municipality, Baglung, Gandaki Province | Matched with school name of B |
| 10460       | 598         | Adhiyari Mavi            | अधियारी मावि एकला रुपन्देही | Adhiyari Mavi | Adhiyari, Lumbini Sanskritik Municipality, Rupandehi, Lumbini Province | Matched with school name of B |
| 3957        | 393         | Adhunika Rashtriya Mavi  | आधुनिक राष्ट्रिय मावि हेटौडा मकवानपुर | Adhunik Rastriya Mavi | Hetauda, Hetauda Sub Metropolitan City, Makwanpur, Bagamati Province | Matched with school name of B |
| 1297        | 397         | Adinatha Mavi            | आदिनाथ मावि चाेभार काठमाडौं | Adinath Mavi | Chobhar, Kirtipur Municipality, Kathmandu, Bagamati Province | Matched with school name of B |
| 24580       | 5102        | Aglu~Nga Mavi            | अग्लुङ्ग मावि मदाने गा पा गुल्मी | Aglung Mavi | Madane 1 Aglung, Madane Rural Municipality, Gulmi, Lumbini Province | Matched with school name of B |
| 16090       | 430         | Ahala Bha~Njya~Nga Mavi  | आहाल भञ्ज्याङ्ग मावि गोरखा | Ahal Bhanjyang Mavi | Siranchok, Siranchowk Rural Municipality, Gorkha, Gandaki Province | Matched with school name of B |
| 3027        | 3108        | Ahalada.Nda Pravi        | आहालडाँडा प्रावि धादिङ | Ahal Danda Avi | Neelakantha, Neelakantha Municipality, Dhading, Bagamati Province | Matched with old school name1 of B |
| 26028       | 198         | Ahale Avi                | आहाले आवि संखुवासभा | Ahale Avi | Aahale, Chichila Rural Municipality, Sankhuwasabha, Koshi Province | Matched with school name of B |
| 4533        | 3111        | Aiselu Bhume Mavi        | ऐसेलु भुमे मावि नुवाकोट | Aiselu Bhume Mavi | Aiselu Kuna, Kispang Rural Municipality, Nuwakot, Bagamati Province | Matched with school name of B |
| 13450       | 754         | Aishvarya Avi            | ऐश्वर्य आवि जानकी गा पा कैलाली | Aishwarya Avi | Pal Bazar, Janaki Rural Municipality, Kailali, Sudurpashchim Province | Matched with school name of B |
| 17341       | 756         | Aishvarya Mavi           | ऐश्वर्य मावि बान्नीगढ जयगढ अछाम | Aishwarya Mavi | Bannigadhi Jayagad R.M, Bannigadhi Jayagadh Rural Municipality, Achham, Sudurpashchim Province | Matched with school name of B |
| 21555       | 1103        | Aitavare Avi             | आइतवारे आवि संखुवासभा | Aitabare Avi | Panchkhapan, Panchakhapan Municipality, Sankhuwasabha, Koshi Province | Matched with school name of B |


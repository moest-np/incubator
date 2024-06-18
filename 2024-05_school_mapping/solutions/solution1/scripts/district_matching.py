# district_matching.py
#
# The school-to-district mapping in `school_list_A.tsv` is incorrect for some districts.
# This needs to be fixed before we start matching schools because we are using district
# as an important heuristic.
#
# Examples:
# लम्जुङ is matched to ताप्लेजुङ (example school_id 3429), पर्बत and नवलपरासी are matched to पर्सा (3625, 3918, etc.).
# And this is not small: 661 नवलपरासी schools, 160 पर्बत, to name a few.
# Also, नवलपरासी is one district in list A, but two (Nawalpur and Parasi) in list B and `jilla.tsv` file.
# Rukum (Rukum East and Rukum West) seems to have been handled.
#
# So we get a better district mapping before we begin with school mapping.
#
# Input: `jilla.tsv` and approximate English translations of `school_list_A` school names.
# Output: Split of high-confidence and low-confidence district-mapped `school_list_A` schools.
#

import pandas as pd
from functions import ngrams, nms_match
from sklearn.feature_extraction.text import TfidfVectorizer
import argparse


def main(args):
    districts = pd.read_csv(args.jilla, sep="\t")
    listA_with_translation = pd.read_csv(args.processed_listA, sep="\t")

    true_district_names = list(
        districts["district"]
    )  # using English district names because we use English translations

    # Assumption is that the last word of the school name is district name (in file A), not always true but mostly?
    # listA_with_translation["potential_district"] = listA_with_translation.apply(lambda x: x.school_processed.split(" ")[-1], axis=1)

    district_names_to_match = list(listA_with_translation["school_processed"])

    vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams)

    matrix_true = vectorizer.fit_transform(true_district_names)
    matrix_match = vectorizer.transform(district_names_to_match)

    nbrs = nms_match(matrix_true, matrix_match)

    matches = []

    for i in range(len(nbrs)):
        original_nm = district_names_to_match[i]
        school_id = listA_with_translation.at[i, 'school_id']

        try:
            matched_nm = true_district_names[nbrs[i][0][0]]
            conf = nbrs[i][1][0]
        except:
            matched_nm = "no match found"
            conf = None

        matches.append([school_id, original_nm, matched_nm, conf])

    matches = pd.DataFrame(matches, columns=['school_id', 'original_nm', 'matched_name', 'conf'])
    results = listA_with_translation.merge(matches, left_on='school_id', right_on='school_id')

    # split list A based on districts (high- and low-confidence)
    required_columns = ["school_id", "school", "matched_name", "conf"]

    listA_with_districts_confidence = results[required_columns]

    listA_with_districts_confidence.rename(
        columns={"matched_name": "district", "conf": "district_conf"},
        inplace=True
    )

    # Splitting list A based on the district confidence scores
    split_1 = listA_with_districts_confidence[listA_with_districts_confidence["district_conf"] <= -0.766]
    split_2 = listA_with_districts_confidence[listA_with_districts_confidence["district_conf"] > -0.766]

    split_1.to_csv("listA_dist_high_conf.tsv", sep="\t", index=False)
    split_2.to_csv("listA_dist_low_conf.tsv", sep="\t", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Run: python district_matching.py --jilla jilla.tsv --processed_listA processed_listA.tsv

    parser.add_argument('--jilla', type=str, default="jilla.tsv", help="Path to jilla.tsv with district names")
    parser.add_argument('--processed_listA', type=str, help="Path to file with translated school names")

    args = parser.parse_args()

    main(args)

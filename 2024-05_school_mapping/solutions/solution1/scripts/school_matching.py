# school_matching.py
#
# Input: `processed_listA_HC.tsv`, `processed_listA_LC.tsv` and `processed_listB.tsv`
# Output: Matched school names

import pandas as pd
from functions import ngrams, nms_match, get_matches_from_nbrs
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
import argparse


def main(args):
    listA, listB = pd.read_csv(args.listA_HC, sep="\t"), pd.read_csv(args.listB, sep='\t')

    # For HC district split
    # Group the schools by districts and match: computationally cheap and better confidence than
    # matching all schools from list A to all schools from list B
    listA_grouped, listB_grouped = listA.groupby('district_id'), listB.groupby('district_id')

    listA_groups, listB_groups = [listA_grouped.get_group(x) for x in listA_grouped.groups], \
        [listB_grouped.get_group(x) for x in listB_grouped.groups]

    # Handling the Nawalparasi case
    # list A has noisy Nawalparasi entries (maps to पर्सा, etc.), so map all Nawalparasi schools
    # (Nawalpur 43 and Parasi 48) together
    listB_groups[47] = pd.concat([listB_groups[42], listB_groups[47]])
    listB_groups[42] = listB_groups[47].iloc[0:1]

    grouped = {}
    for x, y in zip(listA_groups, listB_groups):
        x_district = list(set(x["district_id"].unique()))
        assert len(x_district) == 1, "problem"
        # had to remove this assert because of Nawalparasi
        # assert set(x["district_id"].unique()) == set(y["district_id"].unique()), "problem"
        grouped[x_district[0]] = [x, y]

    # vectorize
    vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams)

    match_groups = []
    for a, b in tqdm(grouped.items()):
        district_id = a

        if district_id == 43:
            # Ignore district 43 (i.e. Nawalpur) because we will match all schools in
            # Nawalparasi (Nawalpur + Parasi) together
            continue

        listA_group, listB_group = b[0], b[1]

        listB_names = list(listB_group["name_processed"])
        listB_matrix = vectorizer.fit_transform(listB_names)

        listA_names = list(listA_group["school_processed"])
        listA_matrix = vectorizer.transform(listA_names)

        nbrs = nms_match(listB_matrix, listA_matrix)
        matches = get_matches_from_nbrs(nbrs, listA_names, listB_names)

        merge_with_A = matches.merge(listA_group, left_on=["original_name"], right_on="school_processed")
        final_merge = merge_with_A.merge(listB_group, left_on=["matched_name"], right_on=["name_processed"])
        final_merge.rename(columns={"school_id_x": "listA_school_id", "school_id_y": "listB_school_id"}, inplace=True)

        match_groups.append(final_merge)

    print("Finished processing HC split")

    # For LC district split
    # Try mapping the schools against the entire list B
    listA_LC = pd.read_csv(args.listA_LC, sep="\t")

    listB_names = list(listB["name_processed"])
    listA_LC_names = list(listA_LC["school_processed"])

    listB_matrix = vectorizer.fit_transform(listB_names)
    listA_LC_matrix = vectorizer.transform(listA_LC_names)

    nbrs = nms_match(listB_matrix, listA_LC_matrix)
    matches_LC = get_matches_from_nbrs(nbrs, listA_LC_names, listB_names)

    merge_with_A_LC = matches_LC.merge(listA_LC, left_on=["original_name"], right_on="school_processed")
    final_merge = merge_with_A_LC.merge(listB, left_on=["matched_name"], right_on=["name_processed"])
    final_merge.rename(columns={"school_id_x": "listA_school_id", "school_id_y": "listB_school_id"}, inplace=True)

    final_merge.to_excel("results_LC.xlsx", index=False)

    match_groups.append(final_merge)
    
    print("Finished processing LC split")

    print("Saving result")
    result_HC_LC = pd.concat(match_groups)
    result_HC_LC.to_excel(f"{args.output_xlsx}.xlsx", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--listA_HC', type=str, help="Path to processed_listA_HC.tsv")
    parser.add_argument('--listA_LC', type=str, help="Path to processed_listA_LC.tsv")
    parser.add_argument('--listB', type=str, help="Path to processed_listB.tsv")
    parser.add_argument('--output_xlsx', type=str, help="Path to save final results (Excel)")

    args = parser.parse_args()

    main(args)

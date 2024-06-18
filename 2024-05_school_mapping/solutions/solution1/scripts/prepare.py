# prepare.py
#
# Three types of data preparations are handled:
# 1. Prepare `school_list_A.tsv` for approx English translation
# 2. Prepare translated list A names for school matching
# 3. Prepare `school_list_B.tsv` for school matching
#
# The central idea behind these routines is to standardize the names
# throughout the datasets for the final matching.
#
# The functions are descriptive enough, but comments are added as felt necessary.

import pandas as pd
import argparse
import re

comma = re.compile(r", ")


def listA_process(name):
    name = re.sub(comma, " , ", name)

    # Add rules as required but check how it affects the output

    name = re.sub("(नि॰मा॰वि॰|नि॰मा॰वि|नि ॰मा॰वि|नि मा वि)", "निम्न माध्यमिक विद्यालय ", name)

    # name = re.sub("नि॰मा॰वि॰", "निम्न माध्यमिक विद्यालय ", name)
    # name = re.sub("नि॰मा॰वि", "निम्न माध्यमिक विद्यालय ", name)
    # name = re.sub("नि ॰मा॰वि", "निम्न माध्यमिक विद्यालय ", name)
    # name = re.sub("नि मा वि", "निम्न माध्यमिक विद्यालय ", name)

    name = re.sub("उ मा वि", "निम्न माध्यमिक विद्यालय ", name)

    name = re.sub("(प्रा.वि.|प्रा.वि|प्रा. वि.|प्रा.बि.|प्रा. बि.|प्रा.बी.|प्रा. बी.)", "प्राथमिक विधालय ", name)

    # name = re.sub("प्रा.वि.", "प्राथमिक विधालय ", name)
    # name = re.sub("प्रा.वि", "प्राथमिक विधालय ", name)
    # name = re.sub("प्रा. वि.", "प्राथमिक विधालय ", name)
    # name = re.sub("प्रा.बि.", "प्राथमिक विधालय ", name)
    # name = re.sub("प्रा. बि.", "प्राथमिक विधालय ", name)
    # name = re.sub("प्रा.बी.", "प्राथमिक विधालय ", name)
    # name = re.sub("प्रा. बी.", "प्राथमिक विधालय ", name)

    name = re.sub("(मा.वि.|मा. वि.|मा.बि.|मा. बि. |मा. बी.|मा.बी.)", "माध्यमिक विद्यालय ", name)
    # name = re.sub("मा.वि.", "माध्यमिक विद्यालय ", name)
    # name = re.sub("मा. वि.", "माध्यमिक विद्यालय ", name)
    # name = re.sub("मा.बि.", "माध्यमिक विद्यालय ", name)
    # name = re.sub("मा. बि. ", "माध्यमिक विद्यालय ", name)
    # name = re.sub("मा. बी.", "माध्यमिक विद्यालय ", name)
    # name = re.sub("मा.बी.", "माध्यमिक विद्यालय ", name)

    name = re.sub("उ॰", "उच्च ", name)
    name = re.sub("नि॰", "निम्न ", name)

    return name


def listA_translated_process(name):
    # Handle very common errors in the approximate translations so that
    # we can improve the school matching
    name = re.sub("Children", "Bal ", name, re.IGNORECASE)
    name = re.sub("Child", "Bal ", name, re.IGNORECASE)
    name = re.sub("Development ", "Bikash ", name, re.IGNORECASE)
    name = re.sub("Welfare", "Kalyan ", name, re.IGNORECASE)
    return name


def listB_process(name, old_name, local_level):
    name = name + " " + old_name if isinstance(old_name, str) else name
    # name = name + ", " + location.split(" ")[0] if isinstance(location, str) else name
    name = name + ", " + local_level.split(" ")[0] if isinstance(local_level, str) else name

    name = re.sub(comma, " , ", name)

    # Add rules as required but check how it affects the output

    name = re.sub("(Ma Vi|Ma.Vi|MA. VI\S|Ma V|Ma Bi|Ma.V)", "Secondary School", name, flags=re.IGNORECASE)
    # name = re.sub("Ma Vi", "Secondary School", name, flags=re.IGNORECASE)
    # name = re.sub("Ma.Vi", "Secondary School", name, flags=re.IGNORECASE)
    # name = re.sub("MA. VI\S", "Secondary School", name, flags=re.IGNORECASE)
    # name = re.sub("Ma V", "Secondary School", name, flags=re.IGNORECASE)
    # name = re.sub("Ma Bi", "Secondary School", name, flags=re.IGNORECASE)
    # name = re.sub("Ma.V", "Secondary School", name, flags=re.IGNORECASE)

    name = re.sub("(Pra Vi|Pra.Vi|PRA. VI\S|Pra V|Pra.V|Pra. V\S)", "Primary School", name, flags=re.IGNORECASE)
    # name = re.sub("Pra Vi", "Primary School", name, flags=re.IGNORECASE)
    # name = re.sub("Pra.Vi", "Primary School", name, flags=re.IGNORECASE)
    # name = re.sub("PRA. VI\S", "Primary School", name, flags=re.IGNORECASE)
    # name = re.sub("Pra V", "Primary School", name, flags=re.IGNORECASE)
    # name = re.sub("Pra.V", "Primary School", name, flags=re.IGNORECASE)
    # name = re.sub("Pra. V\S", "Primary School", name, flags=re.IGNORECASE)

    name = re.sub("(Aa Vi|Aa.Vi|AA. VI\S|Aa V|Aa.V|Aa. V\S|Aa.Bi.|Aa. Bi.)", "Basic School", name, flags=re.IGNORECASE)
    # name = re.sub("Aa Vi", "Basic School", name, flags=re.IGNORECASE)
    # name = re.sub("Aa.Vi", "Basic School", name, flags=re.IGNORECASE)
    # name = re.sub("AA. VI\S", "Basic School", name, flags=re.IGNORECASE)
    # name = re.sub("Aa V", "Basic School", name, flags=re.IGNORECASE)
    # name = re.sub("Aa.V", "Basic School", name, flags=re.IGNORECASE)
    # name = re.sub("Aa. V\S", "Basic School", name, flags=re.IGNORECASE)
    # name = re.sub("Aa.Bi.", "Basic School", name, flags=re.IGNORECASE)
    # name = re.sub("Aa. Bi.", "Basic School", name, flags=re.IGNORECASE)

    name = re.sub("(Adharbhut|Adharbut|Adharbhoot|Aadharbhut|aadharvut|adhar)", "Basic", name, flags=re.IGNORECASE)
    name = re.sub("(Madhyamik|Madhyamic)", "Secondary", name, flags=re.IGNORECASE)
    name = re.sub("(Prathamik|Prathmik)", "Primary", name, flags=re.IGNORECASE)
    name = re.sub("(Bidyalaya|vidhyalaya|vidyalaya|Viddyalaya)", "School", name, flags=re.IGNORECASE)

    name = re.sub("(\sVi\s|\sV\s|\sBi\s)", " School ", name, flags=re.IGNORECASE)
    name = re.sub("(\sNi\s)", " Lower ", name, flags=re.IGNORECASE)
    name = re.sub("(\sMa\s)", " Secondary ", name, flags=re.IGNORECASE)
    name = re.sub("(\sPra\s)", " Secondary ", name, flags=re.IGNORECASE)
    name = re.sub("(\sAa\s)", " Secondary ", name, flags=re.IGNORECASE)

    name = " ".join(list(dict.fromkeys(name.split())))

    return name


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Usage
    # Task 1 (see beginning of file)
    # python prepare.py --type listA --listA path/to/list/A.tsv

    # Task 2 (see above)
    # python prepare.py --type listA_translated --listA path/to/list/A.tsv --listA_translated path/to/translated.csv

    # Task 3 (see above)
    # python prepare.py --type listB --listB path/to/list/B.tsv

    parser.add_argument('--type', type=str, help="Choose between (listA, listB, listA_translated")
    parser.add_argument('--listA', type=str, help="Path to listA")
    parser.add_argument('--listA_translated', type=str, help="Path to listA_translated")
    parser.add_argument('--listB', type=str, help="Path to listB")

    args = parser.parse_args()

    listA, listA_translated, listB = None, None, None

    if args.listA:
        listA = pd.read_csv(args.listA, sep="\t")

    if args.listA_translated:
        listA_translated = pd.read_csv(args.listA_translated, sep="\t")

    if args.listB:
        listB = pd.read_csv(args.listB, sep="\t")

    if args.type == "listA":
        # Output: listA file ready for translation
        listA["school"] = listA.apply(lambda x: listA_process(x['school']), axis=1)
        listA[["id", "school"]].to_csv("to_translate.tsv", sep="\t", index=False)
    elif args.type == "listA_translated":
        # Output: listA with translation file ready for school matching
        listA_translated["school_processed"] = listA_translated.apply(
            lambda x: listA_translated_process(x['school_processed']), axis=1)
        merged = listA_translated[["id", "school_processed"]].merge(listA, left_on=["id"], right_on=["school_id"])
        merged[["school_id", "school", "school_processed", "district_id"]].to_csv(
            "processed_listA_HC.tsv",
            sep="\t",
            index=False
        )
    elif args.type == "listB":
        # Output: listB ready for school matching
        listB = listB[listB["type"] == 2]
        listB["name_processed"] = listB.apply(
            lambda x: listB_process(x['name'], x["old_name1"], x["local_level"]), axis=1
        )
        listB["name_processed"] = listB["name_processed"] + " " + listB["district"]
        listB[["school_id", "name", "name_processed", "district_id"]].to_csv(
            "processed_listB.tsv",
            sep="\t",
            index=False
        )

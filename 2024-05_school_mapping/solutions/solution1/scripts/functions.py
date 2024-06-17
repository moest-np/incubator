from ftfy import fix_text
import pandas as pd
import nmslib
import re


def ngrams(string, n=3):
    string = str(string)
    string = string.lower()
    string = fix_text(string)
    string = string.encode("ascii", errors="ignore").decode()

    chars_to_remove = [")", "(", ".", "|", "[", "]", "{", "}", "'", "-"]
    rx = '[' + re.escape(''.join(chars_to_remove)) + ']'  # remove punc, brackets etc...
    string = re.sub(rx, '', string)

    string = string.replace("school", "")
    string = re.sub("(shree|shri|sri|sheree)", "", string, re.IGNORECASE)

    string = string.title()  # normalise case - capital at start of each word
    string = re.sub(' +', ' ', string).strip()  # get rid of multiple spaces and replace with a single
    string = ' ' + string + ' '  # pad names for ngrams...

    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]


def nms_match(true_matrix, match_matrix, method="simple_invindx"):
    index = nmslib.init(
        method=method,
        space='negdotprod_sparse_fast',
        data_type=nmslib.DataType.SPARSE_VECTOR
    )

    index.addDataPointBatch(true_matrix)
    index.createIndex()

    num_threads = 4
    K = 1

    return index.knnQueryBatch(match_matrix, k=K, num_threads=num_threads)


def get_matches_from_nbrs(nbrs, names_to_match, true_names):
    matches = []

    for i in range(len(nbrs)):
        original_name = names_to_match[i]

        try:
            matched_nm = true_names[nbrs[i][0][0]]
            conf = nbrs[i][1][0]
        except:
            matched_nm = "no match found"
            conf = None

        matches.append([original_name, matched_nm, conf])

    matches = pd.DataFrame(matches, columns=['original_name', 'matched_name', 'conf'])

    return matches

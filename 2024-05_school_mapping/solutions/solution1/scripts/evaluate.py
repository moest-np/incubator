import argparse
import pandas as pd
import numpy as np


def main(args):
    evaluation_set = open(args.eval_set).read().split("\n")
    output = pd.read_excel(args.output)

    correct_pairs = {}
    for pair in evaluation_set[1:]:
        a, b = pair.split(",")
        correct_pairs[int(a)] = int(b)

    correct_pairs = dict(sorted(correct_pairs.items()))

    listA = output["listA_school_id"]
    listB = output["listB_school_id"]

    output = {k: v for k, v in zip(listA, listB)}
    output_eval_pairs = {k: v for k, v in output.items() if k in correct_pairs}
    output_eval_pairs = dict(sorted(output_eval_pairs.items()))

    correct_pairs = {k: v for k, v in correct_pairs.items() if k in output_eval_pairs}
    correct_pairs = dict(sorted(correct_pairs.items()))

    assert output_eval_pairs.keys() == correct_pairs.keys(), f"unequal eval and correct pairs"

    print(f"Evaluation set size: {len(output_eval_pairs)}")

    correct_labels = np.array(list(correct_pairs.values()))
    predicted_labels = np.array(list(output_eval_pairs.values()))

    accuracy = np.count_nonzero(correct_labels == predicted_labels) / len(correct_labels) * 100
    print(f"Accuracy: {accuracy}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--eval_set', type=str, default="evaluation.set", help="Evaluation set to use (CSV)")
    parser.add_argument('--output', type=str, help="Excel file result")

    args = parser.parse_args()

    main(args)

## Solution 1
This solution cleans the data and uses basic [non-metric space searching](https://github.com/nmslib/nmslib/blob/ade4bcdc9dd3719990de2503871450b8a62df4a5/manual/README.md)
using k-NN search to match the school names. 

Final output [here](https://docs.google.com/spreadsheets/d/1cvlO0PE_lhPzLbqmDOJr9MRZd_04Tdcq/edit).

1. **Data preparation**:
   - School list A
     + School names cleaning and processing
     + School names translation
     + School-district mapping and split (High and Low Confidence)
   - School list B
     + School names cleaning and processing (include features as required: location, local_level, district, etc.)
2. **Match schools**
3. **Evaluate**


**Data preparation.** We first clean the data with standardization in mind: there
are instances where equivalent entities do not exactly match, so we try our best to reduce these distances.
For example: `मा.वि.`, `मा. वि.`, `मा.बि.`, `मा. बि.` all mean `माध्यमिक विद्यालय`. We then translate the Nepali names
to English using Google Translate. Here, too, we use regex to standardize. A comprehensive list of regexes
is in `scripts/prepare.py`. There could be some improvement possible here.

**Features selection.** After the data has been cleaned and standardized, we select what features to consider when matching: school name,
location, local_name, district, old names, etc. List A is straightforward in this because there aren't many features,
but list B has some room for maneuver. After some runs and evaluations, I settled on `name`, `local_level`, `district`,
`old_name1`. `location` seems to add some noise (shown in evaluation (below), compare D and E). Other columns don't have much usable
information.

**District-level (b) v Wholesale (a) matching**. Once the data is thus prepared, we use the [`nmslib`](https://github.com/nmslib/nmslib) library to begin matching. Two alternatives here: a) match
all entries from list A against all entries from list B, or b) group the entries by districts first then match. The latter
method has the advantage of being quicker because the search spaces are smaller when we align the entries by district. It
also enables confident matching because there are many schools with very similar names in different districts across the country.
Thus the district heuristic helps. The former is not too computationally expensive either.

We choose the second method for its advantages. However, it requires that the district mapping in list A is perfect because the smallest margin
of error in district-mapping means a lot of schools do not get matched up at all. The fuzzy district-mapping in list A turned out to have some issues.

Examples: लम्जुङ is matched to ताप्लेजुङ (example school_id 3429), पर्बत and नवलपरासी are matched to पर्सा (3625, 3918, etc.). And this is not minor: 
there are 661 नवलपरासी schools, 160 पर्बत ones, to name a few. Also, नवलपरासी is one district in list A, but two (Nawalpur and Parasi) in list B and `jilla.tsv` file. 
Rukum (Rukum East and Rukum West) seems to have been handled.

**School-district matching.** We fix this by first matching the schools and districts from list A using the English translations and `jilla.tsv` file. We then split
the schools in list A based on confidence of the matching: 0.77 cut-off for high confidence (HC) and low confidence (LC) district matching.

**Match and evaluate, results.** Then we proceed to the school matching and evaluation against a few eval sets. Output of method a) is 
[here](https://docs.google.com/spreadsheets/d/1JX-HiNMiE9YM2x9k29ACZApwsNpb2Dqx/edit) and b) is [here](https://docs.google.com/spreadsheets/d/1cvlO0PE_lhPzLbqmDOJr9MRZd_04Tdcq/edit).

**Evaluation sets.** We use synthetic or (small) manual evaluation sets. Refer to the `eval` folder. `true` is manual, `synth` is synthetic and `final` is a mix. 

**Intermediate files.** `work` directory has intermediate files to get the matcher running.

### Requirements
- [`nmslib-2.1.1`](https://github.com/nmslib/nmslib)
- `ftfy`
- `scikit-learn`
- `pandas`
- `tqdm`

### Match school
```
python scripts/school_matching.py --listA_HC work/processed_listA_dist_HC.tsv --listA_LC work/processed_listA_dist_LC.tsv --listB=work/processed_listB.tsv --output_xlsx=match_results
```

### Evaluate
```
python scripts/evaluate.py --eval_set eval/evaluation.final --output match_results.xlsx
```

### Evaluation
Accuracy of methods on the eval sets

| Method                                                                             | `true` | `synth` | `final` |
|------------------------------------------------------------------------------------|--------|---------|---------|
| A                                                                                  | 36     | 74.02   | -       |
| B                                                                                  | 48.07  | 78.64   | 73.65   |
| C                                                                                  | 46.29  | 79.92   | 74.30   |
| [D](https://docs.google.com/spreadsheets/d/1cvlO0PE_lhPzLbqmDOJr9MRZd_04Tdcq/edit) | 51.85  | 85.21   | 81.94   |
| E                                                                                  | 55.55  | 77.81   | 73.37   |
| [F](https://docs.google.com/spreadsheets/d/1JX-HiNMiE9YM2x9k29ACZApwsNpb2Dqx/edit) | 16.66  | -*      | -*      |

*: Big chunks of `synth` and `final` sets are created from F, so they score rather high: 97.53 and 88.64.

|   | Description                                                 |
|---|-------------------------------------------------------------|
| A | District-level matching HC + list B `name`                  |
| B | A + list B `district` + no "Shree" variants                 |
| C | DL HC and LC + list B `district` + no "Shree" + no "School" |
| D | C + list B `local_level.split()[0]` - no "Shree"            |
| E | D + list B `location.split()[0]`                            |
| F | Wholesale matching (Method a) `district`, `local_level`     |

### Possible extensions
- Standardize eval sets,
- Develop/improve methods from insights gained from good eval sets,
- Find noise and clean data, use more meaningful features,
- Experiment with other [search spaces](https://github.com/nmslib/nmslib/blob/ade4bcdc9dd3719990de2503871450b8a62df4a5/manual/spaces.md) 
and [methods](https://github.com/nmslib/nmslib/blob/ade4bcdc9dd3719990de2503871450b8a62df4a5/manual/methods.md)

Please feel free to experiment with the methods described here. Some improvements in the features engineering space should be possible, 
but the data might not be descriptive and clean enough to allow a perfect or near-perfect 1-1 mapping using only automatic methods.

Contributor: [Sharad Duwal](https://github.com/sharad461)

Please feel free to reach out with questions or suggestions at `<sharad[dot]duwal[at]gmail.com>`

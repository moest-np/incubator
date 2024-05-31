import pandas as pd
from fuzzywuzzy import fuzz
import time
import multiprocessing

# Define the function for comparing names
def compare_names(a_name, b_names):
    matches = []
    for b_name in b_names:
        score = fuzz.partial_ratio(a_name, b_name)
        if score >= 1:
            match = {"school_a": a_name, "school_b": b_name, "confidence_score": score}
            matches.append(match)
    return matches

# Define the function for processing comparisons
def process_comparisons(a_names, b_names_list):
    matches = []
    for a_name in a_names:
        matches.extend(compare_names(a_name, b_names_list))
    return matches

# Define file paths (replace with your actual paths)
file_a_path = "E:\\incubator-main\\incubator-main\\2024-05_school_mapping\\data\\Book3.csv"
file_b_path = "E:\\incubator-main\\incubator-main\\2024-05_school_mapping\\data\\school_list_B.tsv"
output_file_path = "E:\\incubator-main\\incubator-main\\2024-05_school_mapping\\data\\school_matches.csv"

# Read data using pandas.read_csv
try:
    df_a = pd.read_csv(file_a_path)
    df_b = pd.read_csv(file_b_path, sep="\t")
except FileNotFoundError:
    print("Error: One or both files not found. Please check the paths.")
    exit()

# Handle case-sensitivity issues (optional)
df_a["velthuis2"] = df_a["velthuis2"].str.lower()
df_b["name"] = df_b["name"].str.lower()

# Split df_b into chunks for multiprocessing
chunk_size = len(df_b) // multiprocessing.cpu_count()
b_chunks = [df_b[i:i+chunk_size] for i in range(0, len(df_b), chunk_size)]

# Start timer
start_time = time.time()

# Create a multiprocessing pool
pool = multiprocessing.Pool()

# Process comparisons using multiprocessing
matches = []
for match in pool.starmap(process_comparisons, [(df_a["velthuis2"], chunk) for chunk in b_chunks]):
    matches.extend(match)

# Close the pool
pool.close()
pool.join()

# Print elapsed time
elapsed_time = time.time() - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")

# Create DataFrame from matches
df_matches = pd.DataFrame(matches)

# Write DataFrame to CSV file
df_matches.to_csv(output_file_path, index=False)
print(f"Matches with confidence scores written to: {output_file_path}")

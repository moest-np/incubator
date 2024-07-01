import pandas as pd
from fuzzywuzzy import fuzz
import time


# Define file paths (replace with your actual paths)
file_a_path = "E:\\incubator-main\\incubator-main\\2024-05_school_mapping\\data\\Book3.csv"  
file_b_path = "E:\\incubator-main\\incubator-main\\2024-05_school_mapping\\data\\school_list_B.tsv"
output_file_path = "E:\\incubator-main\\incubator-main\\2024-05_school_mapping\\data\\school_matches.csv"  

# Define school name column names (replace with actual names)
school_column_name_a = "velthuis2"   ## from excel break down the column into multiple chunks. only for TSV A. So that, the we can match names only. 
school_column_name_b = "name"  

# Read data using pandas.read_csv (assuming TSV format)
try:
    df_a = pd.read_csv(file_a_path)
    df_b = pd.read_csv(file_b_path, sep="\t")
except FileNotFoundError:
    print("Error: One or both files not found. Please check the paths.")
    exit()

# Handle case-sensitivity issues (optional)
df_a[school_column_name_a] = df_a[school_column_name_a].str.lower()  
df_b[school_column_name_b] = df_b[school_column_name_b].str.lower()  

# Create an empty list to store matches with confidence scores
matches = []
start_time = time.time()

# Get total number of comparisons to estimate time
total_comparisons = len(df_a) * len(df_b)
processed_comparisons = 0

# Iterate through each school name in df_a
for a_id, a_name in zip(df_a['school_id'], df_a[school_column_name_a]):
    # if processed_comparisons >= 100:
    #     break
    for b_id, b_name in zip(df_b['school_id'], df_b[school_column_name_b]):
        processed_comparisons += 1
        
        # Calculate partial ratio score
        score = fuzz.partial_ratio(a_name, b_name)

        # Set a minimum score threshold (adjust as needed)
        if score >= 100:
            match = {"school_a_id": a_id, "school_a": a_name, "school_b_id": b_id, "school_b": b_name, "confidence_score": score}
            matches.append(match)
            
            if processed_comparisons % 100 == 1:  # Adjust the reporting frequency as needed
                elapsed_time = time.time() - start_time
                avg_time_per_comparison = elapsed_time / processed_comparisons
                remaining_comparisons = total_comparisons - processed_comparisons
                estimated_remaining_time = remaining_comparisons * avg_time_per_comparison
                remaining_hours = int(estimated_remaining_time // 3600)
                remaining_minutes = int((estimated_remaining_time % 3600) // 60)
                remaining_seconds = int(estimated_remaining_time % 60)

                print(f"Processed {processed_comparisons}/{total_comparisons} comparisons")
                print(f"Estimated remaining time: {remaining_hours} hours, {remaining_minutes} minutes, {remaining_seconds} seconds")

# Create a DataFrame from the matches list
if matches:
    df_matches = pd.DataFrame(matches)

    # Write the DataFrame to a CSV file
    df_matches.to_csv(output_file_path, index=False)
    print(f"Matches with confidence scores written to: {output_file_path}")
else:
    print("No matches found between the two files.")

import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os

# Function to ensure a directory exists
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Processed data directory
processed_data_dir = os.path.normpath(os.path.join(base_dir, '../../data/processed'))

# Ensure the processed data directory exists
ensure_directory_exists(processed_data_dir)

# File paths
file_path_fuzzy_a = os.path.join(processed_data_dir, 'preprocessed_after_fuzzy_A.csv')
file_path_fuzzy_b = os.path.join(processed_data_dir, 'preprocessed_after_fuzzy_B.csv')
output_file_path_fuzzy_second_a = os.path.join(processed_data_dir, 'preprocessed_after_fuzzy_second_A.csv')
output_file_path_fuzzy_second_b = os.path.join(processed_data_dir, 'preprocessed_after_fuzzy_second_B.csv')

# Load the datasets
df_A = pd.read_csv(file_path_fuzzy_a)
df_B = pd.read_csv(file_path_fuzzy_b)

# Replace null values by empty strings in both dataframes
df_B = df_B.fillna('')
df_A = df_A.fillna('')

# Check for null values in both dataframes
print("Null values in df_A:")
print(df_A.isnull().sum())
print("Null values in df_B:")
print(df_B.isnull().sum())

# Verify the changes by displaying the unique values in the modified column
print("Unique values in 'school_levels' in df_B:")
print(df_B['school_levels'].unique())

# Save the updated dataframes to new CSV files
df_A.to_csv(output_file_path_fuzzy_second_a, index=False)
df_B.to_csv(output_file_path_fuzzy_second_b, index=False)

print("Updated dataframe for Fuzzy Second A saved to:", output_file_path_fuzzy_second_a)
print("Updated dataframe for Fuzzy Second B saved to:", output_file_path_fuzzy_second_b)

# Print the first few rows of the updated dataframes
print("First few rows of the updated dataframe for Fuzzy B:")


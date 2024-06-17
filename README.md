# Incubator

Problem statements, discussions, and prototypes

This repo will host problem statements and inception discussions. Baselined requirements and context will be in the project-specific folder, and accompanying discussions will be in the discussion section.

## Setup Instructions

1. **Clone the repository** (if applicable) or navigate to the project directory.

2. **Create a virtual environment**:

    ```sh
    python3 -m venv venv
    ```

3. **Activate the virtual environment**:

    - On Windows:

      ```sh
      venv\Scripts\activate
      ```

    - On macOS/Linux:

      ```sh
      source venv/bin/activate
      ```

4. **Install the required packages**:

    ```sh
    pip install -r requirements.txt
    ```

## Running the Script

1. **Ensure your data files are placed in the `data/` directory**.

2. **Run the script**:

    ```sh
    python school_mapping.py
    ```

3. **Output**: The script will generate a `school_mapping_results.csv` file containing the matched schools along with their district information.

## Matching Logic

- The script transliterates school names from Devanagari to Roman script and matches them with the names in English.
- District information is used to filter potential matches to ensure they are from the same district.
- Fuzzy matching is applied to find the best match based on the transliterated school names.
- Matches with a score above a specified threshold (default: 80) are included in the final output.

## Output Fields

- `school_id_a`: School ID from Source A
- `school_id_b`: School ID from Source B
- `match_score`: Fuzzy match score
- `school_name_a`: School name from Source A
- `school_name_b`: School name from Source B
- `district_id_a`: District ID from Source A
- `district_a`: District name from Source A
- `district_b`: District name from Source B

## Dependencies

- pandas
- rapidfuzz

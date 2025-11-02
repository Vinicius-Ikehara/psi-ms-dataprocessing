"""
Script 03: Create Aligned Mass List
Collects all unique mass values from odd-numbered columns, sorts them, and creates aligned.csv
"""
import os
import sys
import pandas as pd
import numpy as np

# Add root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import INPUT_FILE, OUTPUT_DIR, ENCODING
from utils.csv_helper import read_csv_auto, validate_dataframe


def create_aligned_masses(input_file, output_file):
    """
    Creates a sorted list of unique mass values from all odd-numbered columns
    and adds sample headers from the first row

    Args:
        input_file: Input file path
        output_file: Output file path (03_aligned.csv)
    """
    print(f"Reading file: {input_file}")

    # Read CSV file with automatic delimiter detection
    df, delimiter = read_csv_auto(input_file, ENCODING)

    print(f"[INFO] File loaded: {len(df)} rows, {len(df.columns)} columns")

    # Validate file structure
    validate_dataframe(df, min_columns=2, script_name="Script 03")

    print(f"[INFO] Collecting unique mass values from odd-numbered columns...")

    # Collect all unique mass values from odd columns (indices 0, 2, 4, 6, ...)
    all_masses = set()
    sample_headers = []  # Store sample names from odd columns

    for col_idx in range(0, len(df.columns), 2):  # Step by 2 to get odd-numbered columns
        col_name = df.columns[col_idx]

        # Store sample name (header)
        sample_headers.append(col_name)

        # Skip empty columns
        if df[col_name].isna().all():
            continue

        # Convert to numeric (handles comma decimal separator if present)
        numeric_values = pd.to_numeric(df[col_name].astype(str).str.replace(',', '.'), errors='coerce')

        # Add non-null values to the set
        valid_values = numeric_values.dropna().values
        all_masses.update(valid_values)

        print(f"[OK] Column {col_idx + 1} ({col_name}) - {len(valid_values)} values processed")

    print(f"\n[INFO] Total unique mass values collected: {len(all_masses)}")
    print(f"[INFO] Total sample headers collected: {len(sample_headers)}")

    if len(all_masses) == 0:
        print("[ERROR] No numeric mass values found!")
        return

    # Convert set to sorted list
    print(f"[INFO] Sorting mass values...")
    sorted_masses = sorted(all_masses)

    # Create DataFrame with Aligned column + empty columns for each sample
    print(f"[INFO] Creating aligned DataFrame with sample headers...")

    # Start with Aligned column
    data_dict = {'Aligned': sorted_masses}

    # Add empty columns for each sample (will be filled in later steps)
    for sample_name in sample_headers:
        data_dict[sample_name] = [np.nan] * len(sorted_masses)

    df_aligned = pd.DataFrame(data_dict)

    # Save to output file
    print(f"[INFO] Saving aligned masses to file...")
    df_aligned.to_csv(output_file, sep=delimiter, encoding='utf-8', index=False)

    print(f"\n[OK] Aligned mass file created: {output_file}")
    print(f"[OK] Total distinct masses: {len(sorted_masses)}")
    print(f"[OK] Total sample columns: {len(sample_headers)}")
    print(f"[OK] Range: {sorted_masses[0]:.2f} to {sorted_masses[-1]:.2f}")


if __name__ == "__main__":
    # Output file for aligned masses
    output_file = os.path.join(OUTPUT_DIR, "03_aligned.csv")

    print("="*70)
    print("SCRIPT 03: CREATE ALIGNED MASS LIST")
    print("="*70)
    print(f"Input: {INPUT_FILE}")
    print(f"Output: {output_file}")
    print("\nOperation: Collect unique masses, sort, add sample headers")
    print("="*70 + "\n")

    try:
        create_aligned_masses(INPUT_FILE, output_file)

        print("\n" + "="*70)
        print("[OK] PROCESSING COMPLETED SUCCESSFULLY!")
        print("[INFO] 03_aligned.csv created with sorted unique masses")
        print("[INFO] Sample headers added (columns will be filled in next steps)")
        print("[INFO] Next step: run 04_[next_script].py")
        print("="*70)

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

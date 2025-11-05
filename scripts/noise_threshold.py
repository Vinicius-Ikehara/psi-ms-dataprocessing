"""
OPTIONAL SCRIPT: Apply Noise Threshold
Applies noise threshold to aligned data - values <= threshold become 0
This is an OPTIONAL intermediate step that modifies the output of Step 04

WARNING: This script OVERWRITES 04_aligned_filled.csv
"""
import os
import sys
import pandas as pd
import numpy as np

# Add root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import OUTPUT_DIR
from utils.csv_helper import read_csv_auto, validate_dataframe


def apply_noise_threshold(input_file, noise_level):
    """
    Applies noise threshold to all sample columns (except first column with labels)
    Values <= noise_level are set to 0

    Args:
        input_file: Input file (04_aligned_filled.csv)
        noise_level: Threshold value (float or int)
    """
    print(f"Reading file: {input_file}")
    df, delimiter = read_csv_auto(input_file, 'utf-8')

    print(f"[INFO] File loaded: {len(df)} rows, {len(df.columns)} columns")

    # Validate file structure
    validate_dataframe(df, min_columns=2, script_name="Noise Threshold Script")

    # First column is 'Aligned' (mass labels) - don't process it
    first_column = df.columns[0]
    columns_to_process = df.columns[1:].tolist()

    print(f"\n[INFO] Noise threshold: {noise_level}")
    print(f"[INFO] First column (labels): '{first_column}' - SKIPPED")
    print(f"[INFO] Columns to process: {len(columns_to_process)}")

    # Count values before processing
    print(f"\n[INFO] Counting values <= {noise_level}...")

    total_values = 0
    noise_values = 0

    for col in columns_to_process:
        col_numeric = pd.to_numeric(df[col], errors='coerce')
        valid_mask = col_numeric.notna()
        total_values += valid_mask.sum()
        noise_values += (col_numeric <= noise_level).sum()

    print(f"[INFO] Found {noise_values} values <= {noise_level} out of {total_values} total values")
    print(f"[INFO] Percentage: {(noise_values/total_values*100):.2f}%")

    # Apply threshold using vectorized operations for performance
    print(f"\n[INFO] Applying noise threshold (setting values <= {noise_level} to 0)...")

    values_changed = 0

    # Process all columns at once for better performance
    for col in columns_to_process:
        # Convert to numeric
        df[col] = pd.to_numeric(df[col], errors='coerce')

        # Count values to be changed
        mask = df[col] <= noise_level
        changed_in_col = mask.sum()
        values_changed += changed_in_col

        # Apply threshold: values <= noise_level become 0
        df[col] = df[col].where(df[col] > noise_level, 0)

        # Progress feedback for many columns
        if len(columns_to_process) > 50 and (columns_to_process.index(col) + 1) % 50 == 0:
            print(f"[INFO] Processed {columns_to_process.index(col) + 1}/{len(columns_to_process)} columns...")

    print(f"[OK] Processed all {len(columns_to_process)} columns")

    # Save back to the same file (OVERWRITE)
    print(f"\n[INFO] Saving file (OVERWRITING original)...")
    df.to_csv(input_file, sep=delimiter, encoding='utf-8', index=False)

    print(f"\n[OK] File updated: {input_file}")
    print(f"[OK] Total rows: {len(df)}")
    print(f"[OK] Total columns: {len(df.columns)}")
    print(f"[OK] Values changed to 0: {values_changed}")
    print(f"[INFO] Noise threshold applied successfully!")


if __name__ == "__main__":
    # Target file
    target_file = os.path.join(OUTPUT_DIR, "04_aligned_filled.csv")

    print("="*70)
    print("OPTIONAL SCRIPT: APPLY NOISE THRESHOLD")
    print("="*70)
    print(f"Target file: {target_file}")
    print("\nOperation: Set all values <= noise_threshold to 0")
    print("WARNING: This will OVERWRITE the file!")
    print("="*70 + "\n")

    try:
        # Check if input file exists
        if not os.path.exists(target_file):
            print(f"[ERROR] File not found: {target_file}")
            print("[INFO] Please run Step 04 first to create the aligned filled file")
            sys.exit(1)

        # Ask for noise level
        print("Enter the noise threshold level:")
        print("(All values <= this threshold will be set to 0)")

        while True:
            try:
                noise_input = input("\nNoise level: ").strip()
                noise_level = float(noise_input)

                if noise_level < 0:
                    print("[ERROR] Noise level must be >= 0. Please try again.")
                    continue

                break
            except ValueError:
                print("[ERROR] Invalid input. Please enter a number (e.g., 100, 500.5, 1000)")

        print(f"\n[OK] Noise level set to: {noise_level}")
        print("\n" + "="*70 + "\n")

        apply_noise_threshold(target_file, noise_level)

        print("\n" + "="*70)
        print("[OK] PROCESSING COMPLETED SUCCESSFULLY!")
        print(f"[INFO] Noise threshold ({noise_level}) applied to 04_aligned_filled.csv")
        print("[INFO] File has been overwritten with filtered data")
        print("[INFO] You can now continue with Step 05")
        print("="*70)

    except KeyboardInterrupt:
        print("\n\n[INFO] Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

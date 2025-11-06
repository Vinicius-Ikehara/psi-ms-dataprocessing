"""
Script 07: Calculate BFF (Background Filter Factor)
Calculates BFF = mean + (threshold * std_dev) from all "Blank" columns (excluding "BlankExt")
"""
import os
import sys
import pandas as pd
import numpy as np

# Add root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import OUTPUT_DIR
from utils.csv_helper import read_csv_auto, validate_dataframe
from utils import get_decimal_places


def get_threshold():
    """
    Ask user for the BFF threshold multiplier
    Returns the threshold as an integer or float
    """
    while True:
        try:
            print("\n" + "="*70)
            print("BFF THRESHOLD CONFIGURATION")
            print("="*70)
            print("The BFF (Background Filter Factor) is calculated as:")
            print("BFF = mean + (threshold × standard_deviation)")
            print("\nCommon values:")
            print("  - 3  : Standard approach (99.7% confidence interval)")
            print("  - 10 : More stringent filtering")
            print("="*70)

            threshold_input = input("\nEnter threshold value (e.g., 3, 10): ")
            threshold = float(threshold_input)

            if threshold <= 0:
                print("[ERROR] Threshold must be positive.")
                continue

            if threshold > 20:
                print("[WARNING] Using threshold > 20 is very unusual.")
                confirm = input("Continue anyway? (y/n): ")
                if confirm.lower() != 'y':
                    continue

            print(f"[OK] Will use threshold = {threshold}")
            print(f"[INFO] BFF formula: mean + ({threshold} × std_dev)")
            return threshold

        except ValueError:
            print("[ERROR] Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\n[CANCELLED] Operation cancelled by user.")
            sys.exit(0)


def calculate_bff(input_file, output_file, threshold):
    """
    Calculates BFF column based on "Blank" columns (excluding "BlankExt")

    BFF = mean + (threshold * standard_deviation) of all Blank column values per row

    Args:
        input_file: Input aligned file
        output_file: Output file with BFF column added
        threshold: Multiplier for standard deviation (e.g., 3 or 10)
    """
    print(f"Reading file: {input_file}")
    df, delimiter = read_csv_auto(input_file, 'utf-8')

    print(f"[INFO] File loaded: {len(df)} rows, {len(df.columns)} columns")

    # Validate file structure
    validate_dataframe(df, min_columns=2, script_name="Script 07")

    # Find columns containing "Blank" but not "BlankExt"
    print(f"\n[INFO] Searching for 'Blank' columns (excluding 'BlankExt')...")

    blank_cols = []
    for col in df.columns:
        col_str = str(col).lower()
        if 'blank' in col_str and 'blankext' not in col_str:
            blank_cols.append(col)

    if len(blank_cols) == 0:
        print("[ERROR] No columns with 'Blank' found (excluding 'BlankExt').")
        print(f"[INFO] Available columns: {list(df.columns[:10])}...")
        sys.exit(1)

    print(f"[OK] Found {len(blank_cols)} Blank columns:")
    for col in blank_cols:
        print(f"     - {col}")

    print(f"\n[INFO] Calculating BFF for each row...")
    print(f"[INFO] Formula: BFF = mean + ({threshold} × std_dev)")

    # Calculate BFF for each row
    bff_values = []

    for idx, row in df.iterrows():
        # Extract values from Blank columns
        blank_values = []
        for col in blank_cols:
            val = row[col]
            if pd.notna(val) and isinstance(val, (int, float)):
                blank_values.append(float(val))

        # Calculate BFF if we have values
        if len(blank_values) > 0:
            mean_val = np.mean(blank_values)

            if len(blank_values) > 1:
                std_val = np.std(blank_values, ddof=1)  # Sample standard deviation
            else:
                std_val = 0

            bff = mean_val + (threshold * std_val)
            bff_values.append(bff)
        else:
            bff_values.append(np.nan)

        # Progress feedback
        if (idx + 1) % 5000 == 0:
            print(f"[INFO] Processed {idx + 1}/{len(df)} rows...")

    # Add BFF column to dataframe
    df['BFF'] = bff_values

    # Count valid BFF values
    valid_bff = df['BFF'].notna().sum()

    # Get decimal places from config
    decimal_places = get_decimal_places(OUTPUT_DIR)

    # Save to output file
    print(f"\n[INFO] Saving file with BFF column...")
    float_format = f'%.{decimal_places}f'
    df.to_csv(output_file, sep=delimiter, encoding='utf-8', index=False, float_format=float_format)

    print(f"\n[OK] File with BFF column created: {output_file}")
    print(f"[OK] Total rows: {len(df)}")
    print(f"[OK] Rows with valid BFF: {valid_bff}")
    print(f"[OK] BFF column added as the last column")
    print(f"[INFO] BFF range: {df['BFF'].min():.2f} to {df['BFF'].max():.2f}")


if __name__ == "__main__":
    # Input and output files
    input_file = os.path.join(OUTPUT_DIR, "06_aligned_clean.csv")
    output_file = os.path.join(OUTPUT_DIR, "07_aligned_with_bff.csv")

    print("="*70)
    print("SCRIPT 07: CALCULATE BFF (BACKGROUND FILTER FACTOR)")
    print("="*70)
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print("\nOperation: Calculate BFF from 'Blank' columns")
    print("="*70)

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"\n[ERROR] Input file not found: {input_file}")
        print("[INFO] Please run Step 06 first to create the clean aligned file")
        sys.exit(1)

    # Ask user for threshold
    threshold = get_threshold()

    print("\n" + "="*70)
    print("PROCESSING...")
    print("="*70 + "\n")

    try:
        calculate_bff(input_file, output_file, threshold)

        print("\n" + "="*70)
        print("[OK] PROCESSING COMPLETED SUCCESSFULLY!")
        print("[INFO] BFF column calculated and added")
        print(f"[INFO] Threshold used: {threshold}")
        print("[INFO] Next step: run 08_subtract_bff.py to subtract BFF from all samples")
        print("="*70)

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

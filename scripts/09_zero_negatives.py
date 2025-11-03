"""
Script 09: Convert Negative Values to Zero
After BFF subtraction, converts all negative values to zero (background-level signals)
"""
import os
import sys
import pandas as pd

# Add root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import OUTPUT_DIR
from utils.csv_helper import read_csv_auto, validate_dataframe


def zero_negatives(input_file, output_file):
    """
    Converts all negative values to zero in sample columns

    Args:
        input_file: Input file with BFF subtracted (08_aligned_bff_subtracted.csv)
        output_file: Output file with negatives zeroed (09_aligned_final.csv)
    """
    print(f"Reading file: {input_file}")
    df, delimiter = read_csv_auto(input_file, 'utf-8')

    print(f"[INFO] File loaded: {len(df)} rows, {len(df.columns)} columns")

    # Validate file structure
    validate_dataframe(df, min_columns=2, script_name="Script 09")

    # Identify columns to process (all except 'Aligned' and 'BFF')
    columns_to_process = []
    for col in df.columns:
        if col not in ['Aligned', 'BFF']:
            columns_to_process.append(col)

    print(f"\n[INFO] Found {len(columns_to_process)} columns to process")

    # Count negative values before processing
    negative_count = 0
    total_values = 0

    for col in columns_to_process:
        col_data = df[col]
        # Count numeric negative values
        numeric_mask = pd.to_numeric(col_data, errors='coerce').notna()
        negative_mask = numeric_mask & (pd.to_numeric(col_data, errors='coerce') < 0)
        negative_count += negative_mask.sum()
        total_values += numeric_mask.sum()

    print(f"[INFO] Found {negative_count} negative values out of {total_values} total values")
    print(f"[INFO] Percentage of negative values: {(negative_count/total_values*100):.2f}%")

    print(f"\n[INFO] Converting negative values to zero...")

    # Replace negative values with 0
    values_changed = 0

    for col in columns_to_process:
        # Convert to numeric (in case there are any string values)
        df[col] = pd.to_numeric(df[col], errors='coerce')

        # Count negatives in this column
        neg_in_col = (df[col] < 0).sum()

        # Replace negatives with 0
        df[col] = df[col].clip(lower=0)

        if neg_in_col > 0:
            values_changed += neg_in_col
            print(f"[OK] Column '{col}': {neg_in_col} negative values converted to zero")

        # Progress feedback for many columns
        if len(columns_to_process) > 50 and (columns_to_process.index(col) + 1) % 50 == 0:
            print(f"[INFO] Processed {columns_to_process.index(col) + 1}/{len(columns_to_process)} columns...")

    # Save to output file
    print(f"\n[INFO] Saving final file...")
    df.to_csv(output_file, sep=delimiter, encoding='utf-8', index=False)

    print(f"\n[OK] Final file created: {output_file}")
    print(f"[OK] Total rows: {len(df)}")
    print(f"[OK] Total columns: {len(df.columns)}")
    print(f"[OK] Values converted to zero: {values_changed}")
    print(f"[INFO] All negative values have been replaced with 0")


if __name__ == "__main__":
    # Input and output files
    input_file = os.path.join(OUTPUT_DIR, "08_aligned_bff_subtracted.csv")
    output_file = os.path.join(OUTPUT_DIR, "09_aligned_final.csv")

    print("="*70)
    print("SCRIPT 09: CONVERT NEGATIVE VALUES TO ZERO")
    print("="*70)
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print("\nOperation: Replace all negative values with 0")
    print("="*70 + "\n")

    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"[ERROR] Input file not found: {input_file}")
            print("[INFO] Please run Step 08 first to subtract BFF")
            sys.exit(1)

        zero_negatives(input_file, output_file)

        print("\n" + "="*70)
        print("[OK] PROCESSING COMPLETED SUCCESSFULLY!")
        print("[INFO] All negative values converted to zero")
        print("[INFO] This is your final clean dataset ready for analysis!")
        print("="*70)

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

"""
Script 05: Add Total Sum Column
Adds a 'Total' column with the sum of all intensities for each mass
"""
import os
import sys
import pandas as pd

# Add root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import OUTPUT_DIR
from utils.csv_helper import read_csv_auto, validate_dataframe
from utils import get_decimal_places


def add_total_column(input_file, output_file):
    """
    Adds a 'Total' column with sum of all intensities for each mass

    Args:
        input_file: Input aligned file (04_aligned_filled.csv)
        output_file: Output file with total column (05_aligned_with_total.csv)
    """
    print(f"Reading aligned file: {input_file}")
    df, delimiter = read_csv_auto(input_file, 'utf-8')

    print(f"[INFO] File loaded: {len(df)} rows, {len(df.columns)} columns")

    # Validate file structure
    validate_dataframe(df, min_columns=2, script_name="Script 05")

    # Calculate row sum for all intensity columns (all columns except 'Aligned')
    print(f"[INFO] Calculating total sum for each row...")

    # Sum all columns except the first one (Aligned) and add as 'Total' column
    df['Total'] = df.iloc[:, 1:].sum(axis=1)

    # Count zero rows for information
    zero_rows = len(df[df['Total'] == 0])
    non_zero_rows = len(df[df['Total'] > 0])

    # Get decimal places from config (saved in script 02)
    decimal_places = get_decimal_places(OUTPUT_DIR)

    # Save to output file
    print(f"[INFO] Saving file with total column...")
    # Use float_format to preserve the exact number of decimal places
    float_format = f'%.{decimal_places}f'
    df.to_csv(output_file, sep=delimiter, encoding='utf-8', index=False, float_format=float_format)

    print(f"\n[OK] File with total column created: {output_file}")
    print(f"[OK] Total rows: {len(df)}")
    print(f"[OK] Rows with signal (Total > 0): {non_zero_rows}")
    print(f"[OK] Rows without signal (Total = 0): {zero_rows}")
    print(f"[OK] 'Total' column added as the last column")


if __name__ == "__main__":
    # Input and output files
    input_file = os.path.join(OUTPUT_DIR, "04_aligned_filled.csv")
    output_file = os.path.join(OUTPUT_DIR, "05_aligned_with_total.csv")

    print("="*70)
    print("SCRIPT 05: ADD TOTAL SUM COLUMN")
    print("="*70)
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print("\nOperation: Add 'Total' column with sum of all intensities")
    print("="*70 + "\n")

    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"[ERROR] Input file not found: {input_file}")
            print("[INFO] Please run Step 04 first to create the filled aligned file")
            sys.exit(1)

        add_total_column(input_file, output_file)

        print("\n" + "="*70)
        print("[OK] PROCESSING COMPLETED SUCCESSFULLY!")
        print("[INFO] 'Total' column added to aligned table")
        print("[INFO] You can now review which rows have zero signal")
        print("[INFO] Next step: run 06_remove_zero_rows.py to clean the data")
        print("="*70)

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

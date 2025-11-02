"""
Script 05: Clean Aligned (Remove Zero Rows)
Removes rows where all intensity values are zero (masses with no signal in any sample)
"""
import os
import sys
import pandas as pd

# Add root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import OUTPUT_DIR
from utils.csv_helper import read_csv_auto, validate_dataframe


def clean_aligned(input_file, output_file):
    """
    Removes rows from aligned table where all intensities are zero

    Args:
        input_file: Input aligned file (04_aligned_filled.csv)
        output_file: Output clean file (05_aligned_clean.csv)
    """
    print(f"Reading aligned file: {input_file}")
    df, delimiter = read_csv_auto(input_file, 'utf-8')

    print(f"[INFO] File loaded: {len(df)} rows, {len(df.columns)} columns")

    # Validate file structure
    validate_dataframe(df, min_columns=2, script_name="Script 05")

    # Calculate row sum for all intensity columns (all columns except 'Aligned')
    print(f"[INFO] Calculating row sums...")

    # Sum all columns except the first one (Aligned)
    df['row_sum'] = df.iloc[:, 1:].sum(axis=1)

    # Count rows before filtering
    rows_before = len(df)

    # Filter rows where sum > 0
    print(f"[INFO] Filtering rows where total intensity > 0...")
    df_clean = df[df['row_sum'] > 0].copy()

    # Remove the auxiliary column
    df_clean = df_clean.drop(columns=['row_sum'])

    # Count rows after filtering
    rows_after = len(df_clean)
    rows_removed = rows_before - rows_after

    # Save to output file
    print(f"[INFO] Saving cleaned aligned file...")
    df_clean.to_csv(output_file, sep=delimiter, encoding='utf-8', index=False)

    print(f"\n[OK] Cleaned aligned file created: {output_file}")
    print(f"[OK] Rows before: {rows_before}")
    print(f"[OK] Rows after: {rows_after}")
    print(f"[OK] Rows removed (zero intensities): {rows_removed}")
    print(f"[OK] Percentage kept: {rows_after / rows_before * 100:.1f}%")


if __name__ == "__main__":
    # Input and output files
    input_file = os.path.join(OUTPUT_DIR, "04_aligned_filled.csv")
    output_file = os.path.join(OUTPUT_DIR, "05_aligned_clean.csv")

    print("="*70)
    print("SCRIPT 05: CLEAN ALIGNED (REMOVE ZERO ROWS)")
    print("="*70)
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print("\nOperation: Remove rows where all intensities are zero")
    print("="*70 + "\n")

    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"[ERROR] Input file not found: {input_file}")
            print("[INFO] Please run Step 04 first to create the filled aligned file")
            sys.exit(1)

        clean_aligned(input_file, output_file)

        print("\n" + "="*70)
        print("[OK] PROCESSING COMPLETED SUCCESSFULLY!")
        print("[INFO] Aligned table cleaned - only masses with signal kept")
        print("[INFO] This is your final clean dataset!")
        print("="*70)

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

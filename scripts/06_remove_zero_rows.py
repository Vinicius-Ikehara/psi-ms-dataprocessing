"""
Script 06: Remove Zero Rows
Removes rows where the Total column equals zero (masses with no signal in any sample)
"""
import os
import sys
import pandas as pd

# Add root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import OUTPUT_DIR
from utils.csv_helper import read_csv_auto, validate_dataframe
from utils import get_decimal_places


def remove_zero_rows(input_file, output_file):
    """
    Removes rows where Total column equals zero

    Args:
        input_file: Input file with Total column (05_aligned_with_total.csv)
        output_file: Output clean file (06_aligned_clean.csv)
    """
    print(f"Reading file with total column: {input_file}")
    df, delimiter = read_csv_auto(input_file, 'utf-8')

    print(f"[INFO] File loaded: {len(df)} rows, {len(df.columns)} columns")

    # Validate file structure
    validate_dataframe(df, min_columns=2, script_name="Script 06")

    # Check if 'Total' column exists
    if 'Total' not in df.columns:
        print(f"[ERROR] 'Total' column not found in the file")
        print(f"[INFO] Available columns: {list(df.columns)}")
        print(f"[INFO] Please run Step 05 first to add the Total column")
        sys.exit(1)

    # Count rows before filtering
    rows_before = len(df)
    zero_rows = len(df[df['Total'] == 0])
    non_zero_rows = len(df[df['Total'] > 0])

    # Filter rows where Total > 0
    print(f"[INFO] Filtering rows where Total > 0...")
    df_clean = df[df['Total'] > 0].copy()

    # Remove the Total column from final output
    print(f"[INFO] Removing 'Total' column from final output...")
    df_clean = df_clean.drop(columns=['Total'])

    # Count rows after filtering
    rows_after = len(df_clean)
    rows_removed = rows_before - rows_after

    # Get decimal places from config
    decimal_places = get_decimal_places(OUTPUT_DIR)

    # Save to output file
    print(f"[INFO] Saving cleaned file...")
    float_format = f'%.{decimal_places}f'
    df_clean.to_csv(output_file, sep=delimiter, encoding='utf-8', index=False, float_format=float_format)

    print(f"\n[OK] Clean aligned file created: {output_file}")
    print(f"[OK] Rows before: {rows_before}")
    print(f"[OK] Rows after: {rows_after}")
    print(f"[OK] Rows removed (Total = 0): {rows_removed}")
    print(f"[OK] Percentage kept: {rows_after / rows_before * 100:.1f}%")


if __name__ == "__main__":
    # Input and output files
    input_file = os.path.join(OUTPUT_DIR, "05_aligned_with_total.csv")
    output_file = os.path.join(OUTPUT_DIR, "06_aligned_clean.csv")

    print("="*70)
    print("SCRIPT 06: REMOVE ZERO ROWS")
    print("="*70)
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print("\nOperation: Remove rows where Total = 0")
    print("="*70 + "\n")

    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"[ERROR] Input file not found: {input_file}")
            print("[INFO] Please run Step 05 first to create the file with Total column")
            sys.exit(1)

        remove_zero_rows(input_file, output_file)

        print("\n" + "="*70)
        print("[OK] PROCESSING COMPLETED SUCCESSFULLY!")
        print("[INFO] Aligned table cleaned - only masses with signal kept")
        print("[INFO] 'Total' column removed from final output")
        print("[INFO] This is your final clean dataset!")
        print("="*70)

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

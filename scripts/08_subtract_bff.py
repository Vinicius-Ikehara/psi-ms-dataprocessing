"""
Script 08: Subtract BFF from All Sample Columns
Subtracts the BFF value from each row across all sample columns (background correction)
"""
import os
import sys
import pandas as pd

# Add root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import OUTPUT_DIR
from utils.csv_helper import read_csv_auto, validate_dataframe
from utils import get_decimal_places


def subtract_bff(input_file, output_file):
    """
    Subtracts BFF value from all sample columns (horizontally, row by row)

    Args:
        input_file: Input file with BFF column (07_aligned_with_bff.csv)
        output_file: Output file with BFF subtracted (08_aligned_bff_subtracted.csv)
    """
    print(f"Reading file with BFF column: {input_file}")
    df, delimiter = read_csv_auto(input_file, 'utf-8')

    print(f"[INFO] File loaded: {len(df)} rows, {len(df.columns)} columns")

    # Validate file structure
    validate_dataframe(df, min_columns=2, script_name="Script 08")

    # Check if BFF column exists
    if 'BFF' not in df.columns:
        print(f"[ERROR] 'BFF' column not found in the file")
        print(f"[INFO] Available columns: {list(df.columns)}")
        print(f"[INFO] Please run Step 07 first to calculate BFF")
        sys.exit(1)

    print(f"[OK] BFF column found")

    # Identify columns to process
    # Skip: 'Aligned' column (first) and 'BFF' column (last)
    # Also skip any "Blank" columns since we don't want to subtract BFF from blanks

    columns_to_process = []
    for col in df.columns:
        col_str = str(col).lower()
        # Skip Aligned, BFF, and Blank columns
        if col not in ['Aligned', 'BFF'] and 'blank' not in col_str:
            columns_to_process.append(col)

    print(f"\n[INFO] Found {len(columns_to_process)} sample columns to process")
    print(f"[INFO] Skipping: 'Aligned', 'BFF', and any 'Blank' columns")

    # Count valid BFF values
    valid_bff_count = df['BFF'].notna().sum()
    print(f"[INFO] Rows with valid BFF values: {valid_bff_count}/{len(df)}")

    print(f"\n[INFO] Subtracting BFF from each sample column (row by row)...")

    # Subtract BFF from each sample column
    rows_processed = 0

    for idx, row in df.iterrows():
        bff_value = row['BFF']

        # Only process if BFF is numeric
        if pd.notna(bff_value) and isinstance(bff_value, (int, float)):
            for col in columns_to_process:
                val = row[col]
                if pd.notna(val) and isinstance(val, (int, float)):
                    df.at[idx, col] = val - bff_value

            rows_processed += 1

        # Progress feedback
        if (idx + 1) % 1000 == 0:
            print(f"[INFO] Processed {idx + 1}/{len(df)} rows...")

    # Remove BFF column from final output (optional - keep it for reference)
    # Uncomment the line below if you want to remove BFF column
    # df = df.drop(columns=['BFF'])

    # Get decimal places from config
    decimal_places = get_decimal_places(OUTPUT_DIR)

    print(f"\n[INFO] Saving file with BFF subtracted...")
    float_format = f'%.{decimal_places}f'
    df.to_csv(output_file, sep=delimiter, encoding='utf-8', index=False, float_format=float_format)

    print(f"\n[OK] BFF subtraction completed: {output_file}")
    print(f"[OK] Total rows: {len(df)}")
    print(f"[OK] Rows processed: {rows_processed}")
    print(f"[OK] Columns processed: {len(columns_to_process)}")
    print(f"[INFO] BFF column kept in output for reference")


if __name__ == "__main__":
    # Input and output files
    input_file = os.path.join(OUTPUT_DIR, "07_aligned_with_bff.csv")
    output_file = os.path.join(OUTPUT_DIR, "08_aligned_bff_subtracted.csv")

    print("="*70)
    print("SCRIPT 08: SUBTRACT BFF FROM SAMPLE COLUMNS")
    print("="*70)
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print("\nOperation: Subtract BFF value from all sample columns (background correction)")
    print("="*70 + "\n")

    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"[ERROR] Input file not found: {input_file}")
            print("[INFO] Please run Step 07 first to calculate BFF")
            sys.exit(1)

        subtract_bff(input_file, output_file)

        print("\n" + "="*70)
        print("[OK] PROCESSING COMPLETED SUCCESSFULLY!")
        print("[INFO] BFF subtracted from all sample columns")
        print("[INFO] Background correction applied")
        print("[INFO] This is your final background-corrected dataset!")
        print("="*70)

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

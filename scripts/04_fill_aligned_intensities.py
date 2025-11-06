"""
Script 04: Fill Aligned with Intensity Sums
Reads data.csv and fills the aligned table with summed intensities for each mass/sample
Then fills empty cells with zero
"""
import os
import sys
import pandas as pd
import numpy as np

# Add root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import INPUT_FILE, OUTPUT_DIR, ENCODING
from utils.csv_helper import read_csv_auto, validate_dataframe
from utils import get_decimal_places


def fill_aligned_with_intensities(data_file, aligned_file, output_file):
    """
    Fills the aligned table with intensity sums from data file

    Args:
        data_file: Input data file (data.csv)
        aligned_file: Aligned file with empty columns (03_aligned.csv)
        output_file: Output file with filled intensities (04_aligned_filled.csv)
    """
    print(f"Reading data file: {data_file}")
    df_data, delimiter_data = read_csv_auto(data_file, ENCODING)

    print(f"Reading aligned file: {aligned_file}")
    df_aligned, delimiter_aligned = read_csv_auto(aligned_file, 'utf-8')

    print(f"[INFO] Data file: {len(df_data)} rows, {len(df_data.columns)} columns")
    print(f"[INFO] Aligned file: {len(df_aligned)} rows, {len(df_aligned.columns)} columns")

    # Validate files
    validate_dataframe(df_data, min_columns=2, script_name="Script 04 - Data file")
    validate_dataframe(df_aligned, min_columns=2, script_name="Script 04 - Aligned file")

    # Get decimal places from config (saved in script 02)
    decimal_places = get_decimal_places(OUTPUT_DIR)
    print(f"[INFO] Using {decimal_places} decimal places (from config)")

    print(f"\n[INFO] Processing each sample and filling intensities...")

    # Process each pair of Mass/Intensity columns
    samples_processed = 0

    for col_idx in range(0, len(df_data.columns), 2):
        # Mass column (odd: 0, 2, 4, 6...)
        mass_col_name = df_data.columns[col_idx]

        # Intensity column (even: 1, 3, 5, 7...)
        if col_idx + 1 >= len(df_data.columns):
            print(f"[SKIP] Column {col_idx + 1} ({mass_col_name}) - no corresponding intensity column")
            break

        intensity_col_name = df_data.columns[col_idx + 1]

        # Check if this sample exists in aligned
        if mass_col_name not in df_aligned.columns:
            print(f"[SKIP] Sample {mass_col_name} not found in aligned file")
            continue

        # Extract Mass and Intensity for this sample
        df_sample = df_data[[mass_col_name, intensity_col_name]].copy()
        df_sample.columns = ['Mass', 'Intensity']

        # Convert to numeric
        df_sample['Mass'] = pd.to_numeric(df_sample['Mass'].astype(str).str.replace(',', '.'), errors='coerce')
        df_sample['Intensity'] = pd.to_numeric(df_sample['Intensity'].astype(str).str.replace(',', '.'), errors='coerce')

        # Remove NaN values
        df_sample = df_sample.dropna()

        if len(df_sample) == 0:
            print(f"[SKIP] Sample {mass_col_name} - no valid data")
            continue

        # Group by Mass and sum intensities (in case there are duplicates)
        df_grouped = df_sample.groupby('Mass', as_index=False)['Intensity'].sum()

        # Round mass to match aligned masses (handle floating point precision)
        df_grouped['Mass'] = df_grouped['Mass'].round(decimal_places)

        # Merge with aligned based on Mass
        # Use a temporary dataframe to avoid modifying df_aligned multiple times
        df_temp = df_aligned[['Aligned']].copy()
        df_temp = df_temp.merge(df_grouped, left_on='Aligned', right_on='Mass', how='left')

        # Fill the corresponding column in df_aligned
        df_aligned[mass_col_name] = df_temp['Intensity'].values

        samples_processed += 1
        print(f"[OK] Sample {col_idx // 2 + 1}/{len(df_data.columns) // 2} ({mass_col_name}) - {len(df_grouped)} unique masses")

    # Fill empty cells (NaN) with 0
    print(f"\n[INFO] Filling empty cells with 0...")
    df_aligned = df_aligned.fillna(0)

    # Save to output
    print(f"[INFO] Saving filled aligned file...")
    # Use float_format to preserve the exact number of decimal places
    float_format = f'%.{decimal_places}f'
    df_aligned.to_csv(output_file, sep=delimiter_aligned, encoding='utf-8', index=False, float_format=float_format)

    print(f"\n[OK] Aligned file filled successfully: {output_file}")
    print(f"[OK] Samples processed: {samples_processed}")
    print(f"[OK] Total rows: {len(df_aligned)}")
    print(f"[OK] Total columns: {len(df_aligned.columns)}")


if __name__ == "__main__":
    # Input and output files
    aligned_input = os.path.join(OUTPUT_DIR, "03_aligned.csv")
    output_file = os.path.join(OUTPUT_DIR, "04_aligned_filled.csv")

    print("="*70)
    print("SCRIPT 04: FILL ALIGNED WITH INTENSITY SUMS")
    print("="*70)
    print(f"Data input: {INPUT_FILE}")
    print(f"Aligned input: {aligned_input}")
    print(f"Output: {output_file}")
    print("\nOperation: Fill aligned table with intensity sums from data")
    print("="*70 + "\n")

    try:
        # Check if aligned file exists
        if not os.path.exists(aligned_input):
            print(f"[ERROR] Aligned file not found: {aligned_input}")
            print("[INFO] Please run Step 03 first to create the aligned file")
            sys.exit(1)

        fill_aligned_with_intensities(INPUT_FILE, aligned_input, output_file)

        print("\n" + "="*70)
        print("[OK] PROCESSING COMPLETED SUCCESSFULLY!")
        print("[INFO] Aligned table filled with intensity sums")
        print("[INFO] Empty cells filled with 0")
        print("[INFO] Next step: run 05_[next_script].py")
        print("="*70)

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

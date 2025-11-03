"""
Script 10: Add QC/RCP and Sample Totals
Creates two sum columns:
- QC_RCP_Total: Sum of all columns containing "QC" or "RCP"
- Samples_Total: Sum of all other sample columns (excluding QC/RCP, Aligned, BFF)
"""
import os
import sys
import pandas as pd

# Add root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import OUTPUT_DIR
from utils.csv_helper import read_csv_auto, validate_dataframe


def add_qc_totals(input_file, output_file):
    """
    Adds QC_RCP_Total and Samples_Total columns

    Args:
        input_file: Input file (09_aligned_final.csv)
        output_file: Output file with totals (10_aligned_with_qc_totals.csv)
    """
    print(f"Reading file: {input_file}")
    df, delimiter = read_csv_auto(input_file, 'utf-8')

    print(f"[INFO] File loaded: {len(df)} rows, {len(df.columns)} columns")

    # Validate file structure
    validate_dataframe(df, min_columns=2, script_name="Script 10")

    # Identify QC/RCP columns
    print(f"\n[INFO] Searching for QC and RCP columns...")

    qc_rcp_cols = []
    sample_cols = []

    for col in df.columns:
        col_str = str(col).upper()

        # Skip Aligned and BFF columns
        if col in ['Aligned', 'BFF']:
            continue

        # Check if column contains QC or RCP
        if 'QC' in col_str or 'RCP' in col_str:
            qc_rcp_cols.append(col)
        else:
            # It's a regular sample column
            sample_cols.append(col)

    print(f"\n[OK] Found {len(qc_rcp_cols)} QC/RCP columns:")
    for col in qc_rcp_cols:
        print(f"     - {col}")

    print(f"\n[OK] Found {len(sample_cols)} sample columns")

    if len(qc_rcp_cols) == 0:
        print("\n[WARNING] No QC or RCP columns found!")
        print("[INFO] Looking for columns with 'QC' or 'RCP' in their names")
        print(f"[INFO] Available columns: {list(df.columns[:20])}...")
        print("\n[INFO] Continuing anyway - QC_RCP_Total will be zero for all rows")

    # Calculate QC_RCP_Total
    print(f"\n[INFO] Calculating QC_RCP_Total (sum of QC/RCP columns)...")

    if len(qc_rcp_cols) > 0:
        # Convert columns to numeric and sum
        qc_rcp_data = df[qc_rcp_cols].apply(pd.to_numeric, errors='coerce')
        df['QC_RCP_Total'] = qc_rcp_data.sum(axis=1)
    else:
        # No QC/RCP columns - set to 0
        df['QC_RCP_Total'] = 0

    # Calculate Samples_Total
    print(f"[INFO] Calculating Samples_Total (sum of sample columns)...")

    if len(sample_cols) > 0:
        # Convert columns to numeric and sum
        sample_data = df[sample_cols].apply(pd.to_numeric, errors='coerce')
        df['Samples_Total'] = sample_data.sum(axis=1)
    else:
        print("[WARNING] No sample columns found!")
        df['Samples_Total'] = 0

    # Statistics
    qc_zero_count = (df['QC_RCP_Total'] == 0).sum()
    samples_zero_count = (df['Samples_Total'] == 0).sum()
    both_zero_count = ((df['QC_RCP_Total'] == 0) & (df['Samples_Total'] == 0)).sum()

    print(f"\n[INFO] Statistics:")
    print(f"  - Rows where QC_RCP_Total = 0: {qc_zero_count} ({qc_zero_count/len(df)*100:.1f}%)")
    print(f"  - Rows where Samples_Total = 0: {samples_zero_count} ({samples_zero_count/len(df)*100:.1f}%)")
    print(f"  - Rows where BOTH = 0: {both_zero_count} ({both_zero_count/len(df)*100:.1f}%)")
    print(f"  - Rows to be removed in next step: {qc_zero_count + samples_zero_count - both_zero_count}")

    # Save to output file
    print(f"\n[INFO] Saving file with QC totals...")
    df.to_csv(output_file, sep=delimiter, encoding='utf-8', index=False)

    print(f"\n[OK] File with QC totals created: {output_file}")
    print(f"[OK] Total rows: {len(df)}")
    print(f"[OK] Total columns: {len(df.columns)}")
    print(f"[OK] QC_RCP_Total range: {df['QC_RCP_Total'].min():.2f} to {df['QC_RCP_Total'].max():.2f}")
    print(f"[OK] Samples_Total range: {df['Samples_Total'].min():.2f} to {df['Samples_Total'].max():.2f}")


if __name__ == "__main__":
    # Input and output files
    input_file = os.path.join(OUTPUT_DIR, "09_aligned_final.csv")
    output_file = os.path.join(OUTPUT_DIR, "10_aligned_with_qc_totals.csv")

    print("="*70)
    print("SCRIPT 10: ADD QC/RCP AND SAMPLE TOTALS")
    print("="*70)
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print("\nOperation: Calculate QC_RCP_Total and Samples_Total columns")
    print("="*70 + "\n")

    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"[ERROR] Input file not found: {input_file}")
            print("[INFO] Please run Step 09 first to zero negative values")
            sys.exit(1)

        add_qc_totals(input_file, output_file)

        print("\n" + "="*70)
        print("[OK] PROCESSING COMPLETED SUCCESSFULLY!")
        print("[INFO] QC_RCP_Total and Samples_Total columns added")
        print("[INFO] Review the totals before proceeding to Step 11")
        print("[INFO] Next step: run 11_remove_qc_noise.py to filter out noise")
        print("="*70)

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

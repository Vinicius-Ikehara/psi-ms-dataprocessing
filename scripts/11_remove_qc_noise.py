"""
Script 11: Remove QC/RCP Noise
Removes rows where:
- QC_RCP_Total = 0 (signal not present in controls = contamination/noise)
- OR Samples_Total = 0 (no signal in samples = irrelevant data)

Keeps only rows where BOTH QC_RCP_Total > 0 AND Samples_Total > 0
"""
import os
import sys
import pandas as pd

# Add root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import OUTPUT_DIR
from utils.csv_helper import read_csv_auto, validate_dataframe


def remove_qc_noise(input_file, output_file):
    """
    Removes rows based on QC/RCP filtering logic

    Deletion criteria:
    - QC_RCP_Total = 0 (not in controls = noise/contamination)
    - OR Samples_Total = 0 (not in samples = irrelevant)

    Args:
        input_file: Input file with totals (10_aligned_with_qc_totals.csv)
        output_file: Output filtered file (11_aligned_qc_filtered.csv)
    """
    print(f"Reading file with QC totals: {input_file}")
    df, delimiter = read_csv_auto(input_file, 'utf-8')

    print(f"[INFO] File loaded: {len(df)} rows, {len(df.columns)} columns")

    # Validate file structure
    validate_dataframe(df, min_columns=2, script_name="Script 11")

    # Check if required columns exist
    if 'QC_RCP_Total' not in df.columns:
        print(f"[ERROR] 'QC_RCP_Total' column not found")
        print(f"[INFO] Please run Step 10 first to calculate QC totals")
        sys.exit(1)

    if 'Samples_Total' not in df.columns:
        print(f"[ERROR] 'Samples_Total' column not found")
        print(f"[INFO] Please run Step 10 first to calculate sample totals")
        sys.exit(1)

    print(f"[OK] Required columns found: QC_RCP_Total, Samples_Total")

    # Count rows before filtering
    rows_before = len(df)

    # Count rows by category
    qc_zero = (df['QC_RCP_Total'] == 0).sum()
    samples_zero = (df['Samples_Total'] == 0).sum()
    both_zero = ((df['QC_RCP_Total'] == 0) & (df['Samples_Total'] == 0)).sum()
    both_positive = ((df['QC_RCP_Total'] > 0) & (df['Samples_Total'] > 0)).sum()

    print(f"\n[INFO] Row statistics BEFORE filtering:")
    print(f"  - Total rows: {rows_before}")
    print(f"  - Rows with QC_RCP_Total = 0: {qc_zero}")
    print(f"  - Rows with Samples_Total = 0: {samples_zero}")
    print(f"  - Rows with both = 0: {both_zero}")
    print(f"  - Rows with both > 0 (will keep): {both_positive}")

    # Apply filter: Keep only rows where BOTH totals are > 0
    print(f"\n[INFO] Applying QC/RCP filter...")
    print(f"[INFO] Keeping rows where: QC_RCP_Total > 0 AND Samples_Total > 0")

    df_filtered = df[(df['QC_RCP_Total'] > 0) & (df['Samples_Total'] > 0)].copy()

    # Count rows after filtering
    rows_after = len(df_filtered)
    rows_removed = rows_before - rows_after

    print(f"\n[INFO] Filtering results:")
    print(f"  - Rows BEFORE: {rows_before}")
    print(f"  - Rows AFTER: {rows_after}")
    print(f"  - Rows REMOVED: {rows_removed} ({rows_removed/rows_before*100:.1f}%)")
    print(f"  - Rows KEPT: {rows_after} ({rows_after/rows_before*100:.1f}%)")

    # Remove the total columns from final output (optional - comment out if you want to keep them)
    print(f"\n[INFO] Removing QC_RCP_Total and Samples_Total columns from final output...")
    df_filtered = df_filtered.drop(columns=['QC_RCP_Total', 'Samples_Total'])

    # Save to output file
    print(f"[INFO] Saving filtered file...")
    df_filtered.to_csv(output_file, sep=delimiter, encoding='utf-8', index=False)

    print(f"\n[OK] QC-filtered file created: {output_file}")
    print(f"[OK] Final rows: {len(df_filtered)}")
    print(f"[OK] Final columns: {len(df_filtered.columns)}")


if __name__ == "__main__":
    # Input and output files
    input_file = os.path.join(OUTPUT_DIR, "10_aligned_with_qc_totals.csv")
    output_file = os.path.join(OUTPUT_DIR, "11_aligned_qc_filtered.csv")

    print("="*70)
    print("SCRIPT 11: REMOVE QC/RCP NOISE")
    print("="*70)
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print("\nOperation: Remove rows where QC_RCP_Total = 0 OR Samples_Total = 0")
    print("="*70 + "\n")

    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"[ERROR] Input file not found: {input_file}")
            print("[INFO] Please run Step 10 first to calculate QC totals")
            sys.exit(1)

        remove_qc_noise(input_file, output_file)

        print("\n" + "="*70)
        print("[OK] PROCESSING COMPLETED SUCCESSFULLY!")
        print("[INFO] QC/RCP noise filtering applied")
        print("[INFO] Removed rows with no signal in controls or samples")
        print("[INFO] This is your final QC-validated dataset!")
        print("="*70)

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

"""
Script 02: Round Mass Columns
Rounds all odd-numbered columns (Mass columns) to N decimal places
"""
import os
import sys
import pandas as pd
import shutil

# Add root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import INPUT_FILE, INPUT_DIR, OUTPUT_DIR, DELIMITER, ENCODING


def round_mass_columns(input_file, output_file, decimal_places):
    """
    Rounds all odd-numbered columns (Mass columns) to specified decimal places

    Args:
        input_file: Input file path
        output_file: Output file path
        decimal_places: Number of decimal places to round to
    """
    print(f"Reading file: {input_file}")

    # Read CSV file
    df = pd.read_csv(input_file, delimiter=DELIMITER, encoding=ENCODING, low_memory=False)

    print(f"[INFO] File loaded: {len(df)} rows, {len(df.columns)} columns")
    print(f"[INFO] Processing odd-numbered columns (Mass columns)...")

    # Process odd-numbered columns (indices 0, 2, 4, 6, ...)
    # In VBA, columns are 1-indexed, so column 1, 3, 5, 7...
    # In Python/pandas, columns are 0-indexed, so column 0, 2, 4, 6...
    columns_processed = 0

    for col_idx in range(0, len(df.columns), 2):  # Step by 2 to get odd-numbered columns
        col_name = df.columns[col_idx]

        # Check if column has any data
        if df[col_name].isna().all():
            print(f"[SKIP] Column {col_idx + 1} ({col_name}) - empty")
            continue

        # Convert to numeric (handles comma decimal separator if present)
        # coerce will turn non-numeric values into NaN
        df[col_name] = pd.to_numeric(df[col_name].astype(str).str.replace(',', '.'), errors='coerce')

        # Round to specified decimal places
        df[col_name] = df[col_name].round(decimal_places)

        columns_processed += 1
        print(f"[OK] Column {col_idx + 1} ({col_name}) - rounded to {decimal_places} decimals")

    # Save to output file
    print(f"\n[INFO] Saving processed file...")
    df.to_csv(output_file, sep=DELIMITER, encoding='utf-8', index=False)

    print(f"\n[OK] Processed file saved at: {output_file}")
    print(f"[OK] Total columns processed: {columns_processed}")
    print(f"[OK] Total rows: {len(df)}")


def get_decimal_places():
    """
    Ask user for the number of decimal places
    Returns the number of decimal places as an integer
    """
    while True:
        try:
            print("\n" + "="*70)
            decimal_input = input("How many decimal places do you want? (e.g., 2, 3, 4): ")
            decimal_places = int(decimal_input)

            if decimal_places < 0:
                print("[ERROR] Please enter a positive number or 0.")
                continue

            if decimal_places > 10:
                print("[WARNING] Using more than 10 decimal places may not be practical.")
                confirm = input("Continue anyway? (y/n): ")
                if confirm.lower() != 'y':
                    continue

            print(f"[OK] Will round to {decimal_places} decimal places")
            return decimal_places

        except ValueError:
            print("[ERROR] Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\n[CANCELLED] Operation cancelled by user.")
            sys.exit(0)


if __name__ == "__main__":
    # Input and output files
    output_file = os.path.join(OUTPUT_DIR, "02_mass_rounded.csv")
    updated_input = os.path.join(INPUT_DIR, "data.csv")

    print("="*70)
    print("SCRIPT 02: ROUND MASS COLUMNS")
    print("="*70)
    print(f"Input: {INPUT_FILE}")
    print(f"Output (backup): {output_file}")
    print(f"Updated input: {updated_input}")
    print("\nOperation: Round all odd-numbered columns (Mass) to N decimal places")
    print("="*70)

    # Ask user for decimal places
    decimal_places = get_decimal_places()

    print("\n" + "="*70)
    print("PROCESSING...")
    print("="*70 + "\n")

    try:
        # Save to OUTPUT for history
        round_mass_columns(INPUT_FILE, output_file, decimal_places)

        # Copy result to INPUT as updated version
        shutil.copy2(output_file, updated_input)
        print(f"\n[OK] Updated input file: {updated_input}")

        print("\n" + "="*70)
        print("[OK] PROCESSING COMPLETED SUCCESSFULLY!")
        print(f"[INFO] All Mass columns rounded to {decimal_places} decimal places")
        print("[INFO] Next step: run 03_[next_script].py")
        print("="*70)

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

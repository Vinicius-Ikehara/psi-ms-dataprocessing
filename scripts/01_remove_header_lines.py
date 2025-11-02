"""
Script 01: Remove header lines
Keeps only lines 2 and 8 from the first 8 lines, removes the rest
"""
import os
import sys

# Add root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import INPUT_FILE, OUTPUT_DIR


def remove_header_lines(input_file, output_file):
    """
    Removes lines 1, 3, 4, 5, 6, 7 from the header
    Keeps line 2, line 8 and all subsequent lines

    Args:
        input_file: Input file path
        output_file: Output file path
    """
    print(f"Reading file: {input_file}")

    # Lines to keep (indices start at 0, so line 2 = index 1, line 8 = index 7)
    lines_to_keep_start = {1, 7}  # line 2 and line 8

    with open(input_file, 'r', encoding='utf-8-sig') as f_in:
        with open(output_file, 'w', encoding='utf-8') as f_out:
            for i, line in enumerate(f_in):
                # If in the first 8 lines (indices 0-7)
                if i < 8:
                    # Only write if it's line 2 or line 8
                    if i in lines_to_keep_start:
                        f_out.write(line)
                        print(f"[OK] Line {i+1} kept")
                    else:
                        print(f"[X] Line {i+1} removed")
                else:
                    # From line 9 onwards, keep everything
                    f_out.write(line)

                # Progress feedback for large files
                if (i + 1) % 100000 == 0:
                    print(f"Processed {i + 1} lines...")

    print(f"\n[OK] Processed file saved at: {output_file}")
    print(f"[OK] Total lines processed: {i + 1}")


if __name__ == "__main__":
    # Define output file
    output_file = os.path.join(OUTPUT_DIR, "01_header_removed.csv")

    print("="*70)
    print("SCRIPT 01: REMOVE HEADER LINES")
    print("="*70)
    print(f"Input: {INPUT_FILE}")
    print(f"Output: {output_file}")
    print("\nOperation: Keep only lines 2 and 8 from the first 8 lines")
    print("="*70 + "\n")

    try:
        remove_header_lines(INPUT_FILE, output_file)
        print("\n" + "="*70)
        print("[OK] PROCESSING COMPLETED SUCCESSFULLY!")
        print("="*70)

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

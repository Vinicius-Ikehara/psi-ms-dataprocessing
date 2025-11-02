"""
CSV Helper functions for detecting delimiters and validating files
"""
import pandas as pd


def detect_delimiter(file_path, encoding='utf-8-sig'):
    """
    Automatically detects the CSV delimiter by reading the first few lines

    Args:
        file_path: Path to the CSV file
        encoding: File encoding

    Returns:
        The detected delimiter (';', ',', '\t', etc.)
    """
    # Try common delimiters
    delimiters = [';', ',', '\t', '|']

    # Read first line to check
    with open(file_path, 'r', encoding=encoding) as f:
        first_line = f.readline()

    # Count occurrences of each delimiter
    delimiter_counts = {delim: first_line.count(delim) for delim in delimiters}

    # Return delimiter with highest count (must be > 0)
    best_delimiter = max(delimiter_counts, key=delimiter_counts.get)

    if delimiter_counts[best_delimiter] == 0:
        raise ValueError("Could not detect delimiter. File may not be a valid CSV.")

    return best_delimiter


def validate_dataframe(df, min_columns=2, script_name=""):
    """
    Validates that the DataFrame has the expected structure

    Args:
        df: DataFrame to validate
        min_columns: Minimum number of columns expected
        script_name: Name of the script for error messages

    Raises:
        ValueError if validation fails
    """
    if len(df.columns) < min_columns:
        error_msg = f"""
[ERROR] File validation failed in {script_name}!

Expected: At least {min_columns} columns (Mass/Intensity pairs)
Found: {len(df.columns)} column(s)

This usually means:
1. Wrong delimiter detected (expected ';' or ',')
2. File is not in the correct format
3. Step 01 was not run before this step

Column names found: {list(df.columns[:5])}...

Please check:
- Is this the correct file?
- Did you run Step 01 first?
- Is the file using semicolon (;) or comma (,) as delimiter?
"""
        raise ValueError(error_msg)

    print(f"[OK] File validation passed: {len(df.columns)} columns detected")


def read_csv_auto(file_path, encoding='utf-8-sig'):
    """
    Reads CSV with automatic delimiter detection

    Args:
        file_path: Path to the CSV file
        encoding: File encoding

    Returns:
        DataFrame and the detected delimiter
    """
    # Detect delimiter
    delimiter = detect_delimiter(file_path, encoding)
    print(f"[INFO] Detected delimiter: '{delimiter}'")

    # Read CSV
    df = pd.read_csv(file_path, delimiter=delimiter, encoding=encoding, low_memory=False)

    return df, delimiter

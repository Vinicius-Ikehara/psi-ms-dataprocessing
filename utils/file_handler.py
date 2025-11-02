"""
Utility functions for reading and writing files
"""
import os


def read_file_lines(file_path, encoding='utf-8-sig'):
    """
    Reads a file line by line efficiently

    Args:
        file_path: Full path to the file
        encoding: File encoding

    Returns:
        List of file lines
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r', encoding=encoding) as f:
        lines = f.readlines()

    return lines


def write_file_lines(file_path, lines, encoding='utf-8'):
    """
    Writes lines to a file

    Args:
        file_path: Full path to the output file
        lines: List of lines to write
        encoding: File encoding
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', encoding=encoding) as f:
        f.writelines(lines)

    print(f"File saved: {file_path}")
    print(f"Total lines: {len(lines)}")


def process_file_in_chunks(input_path, output_path, processing_function, chunk_size=10000, encoding='utf-8-sig'):
    """
    Processes a large file in chunks to save memory

    Args:
        input_path: Input file path
        output_path: Output file path
        processing_function: Function that receives a list of lines and returns processed lines
        chunk_size: Size of each chunk
        encoding: File encoding
    """
    with open(input_path, 'r', encoding=encoding) as f_in:
        with open(output_path, 'w', encoding='utf-8') as f_out:
            chunk = []
            for i, line in enumerate(f_in):
                chunk.append(line)

                if len(chunk) >= chunk_size:
                    processed_lines = processing_function(chunk)
                    f_out.writelines(processed_lines)
                    chunk = []

                    if (i + 1) % 50000 == 0:
                        print(f"Processed {i + 1} lines...")

            # Process the last chunk
            if chunk:
                processed_lines = processing_function(chunk)
                f_out.writelines(processed_lines)

    print(f"Processing complete! File saved at: {output_path}")

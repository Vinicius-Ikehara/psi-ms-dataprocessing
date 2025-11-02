# Mass Spectrometry Data Processor

A modular Python-based toolkit for processing and analyzing mass spectrometry data from CSV files. This project provides a collection of standalone scripts that can be executed independently to perform various data processing operations.

## Features

- **Modular Design**: Each processing step is a separate script that can be run independently
- **Large File Support**: Efficient processing of large CSV files (hundreds of MB)
- **Easy to Extend**: Add new processing scripts following the established pattern
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Well Documented**: Clear code comments and docstrings

## Project Structure

```
mass-spec-processor/
├── input/                  # Place your input CSV files here
│   └── data.csv           # Your input file (rename your file to this)
├── output/                 # Processed files will be saved here
├── scripts/                # Processing scripts (run these)
│   └── 01_remove_header_lines.py
├── utils/                  # Utility functions
│   ├── __init__.py
│   └── file_handler.py
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── setup.sh              # Setup script for Linux/Mac
├── setup.bat             # Setup script for Windows
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Quick Start

### Option 1: Automated Setup (Recommended)

**For Windows:**
```bash
setup.bat
```

**For Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

1. **Clone or download this repository**

2. **Create a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Place your data file:**
   - Copy your CSV file to the `input/` directory
   - Rename it to `data.csv` (or update `config.py` with your filename)

## Usage

### Running Individual Scripts

Each script can be run independently. Make sure your virtual environment is activated first.

**Windows:**
```bash
venv\Scripts\activate
python scripts\01_remove_header_lines.py
```

**Linux/Mac:**
```bash
source venv/bin/activate
python scripts/01_remove_header_lines.py
```

### Available Scripts

#### Script 01: Remove Header Lines
**File:** `01_remove_header_lines.py`

**Purpose:** Cleans up the header section of mass spectrometry CSV exports

**What it does:**
- Removes unnecessary header lines (lines 1, 3, 4, 5, 6, 7)
- Keeps only line 2 (sample names) and line 8 (column headers)
- Preserves all data rows

**Output:** `output/01_header_removed.csv`

**Example:**
```bash
python scripts/01_remove_header_lines.py
```

## Configuration

Edit `config.py` to customize:

- **Input/Output directories**
- **Input filename** (default: `data.csv`)
- **File encoding** (default: `utf-8-sig` to handle BOM)
- **Delimiter** (default: `;` for semicolon-separated files)
- **Chunk size** for large file processing

```python
# Example configuration
INPUT_FILE = os.path.join(INPUT_DIR, "data.csv")
DELIMITER = ';'
ENCODING = 'utf-8-sig'
```

## Adding New Scripts

To add a new processing step:

1. Create a new file: `scripts/02_your_operation.py`
2. Follow this template:

```python
"""
Script 02: Description of what this script does
"""
import os
import sys

# Add root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import INPUT_FILE, OUTPUT_DIR

def your_processing_function(input_file, output_file):
    """
    Description of the processing operation

    Args:
        input_file: Input file path
        output_file: Output file path
    """
    # Your processing logic here
    pass

if __name__ == "__main__":
    # For the first script, use INPUT_FILE
    # For subsequent scripts, use the previous output
    input_file = os.path.join(OUTPUT_DIR, "01_header_removed.csv")
    output_file = os.path.join(OUTPUT_DIR, "02_your_output.csv")

    print("="*70)
    print("SCRIPT 02: YOUR OPERATION NAME")
    print("="*70)

    try:
        your_processing_function(input_file, output_file)
        print("[OK] PROCESSING COMPLETED SUCCESSFULLY!")
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        sys.exit(1)
```

## Dependencies

- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computing
- **scipy** - Scientific computing
- **matplotlib** - Plotting and visualization
- **openpyxl** - Excel file support

See `requirements.txt` for specific versions.

## File Format

**Expected Input Format:**
- CSV file with semicolon (`;`) as delimiter
- UTF-8 encoding with BOM
- Mass spectrometry data format (configurable)

**Output Format:**
- UTF-8 encoding
- Same delimiter as input
- Cleaned/processed data

## Troubleshooting

### Virtual environment not activating
**Windows:** Make sure you run `venv\Scripts\activate.bat` (not just `activate`)
**Linux/Mac:** Make sure you use `source venv/bin/activate`

### Python not found
Make sure Python 3.7+ is installed and added to your PATH. Download from [python.org](https://www.python.org/downloads/)

### Permission denied on setup.sh
Run: `chmod +x setup.sh` before executing

### Encoding errors
If you encounter encoding errors, update the `ENCODING` setting in `config.py`

## Best Practices

1. **Keep original files safe**: Always work with copies of your data
2. **Run scripts in sequence**: Script 02 uses output from Script 01, etc.
3. **Check output files**: Verify each processing step before moving to the next
4. **Use virtual environment**: Always activate the venv before running scripts

## Contributing

To contribute:
1. Fork the repository
2. Create a new branch for your feature
3. Add your processing script following the template
4. Test thoroughly with sample data
5. Submit a pull request

## License

[Add your license here]

## Authors

[Add authors here]

## Acknowledgments

This toolkit was developed for processing mass spectrometry data exports and making data analysis workflows more efficient and reproducible.

## Support

For issues, questions, or suggestions, please [open an issue](link-to-issues) or contact [contact info].

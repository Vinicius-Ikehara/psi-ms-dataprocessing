# How to Run the Scripts

This folder contains easy-to-use batch files to execute the data processing scripts.

## Instructions

1. **Make sure you have completed the setup** (created venv and installed dependencies)
2. **Place your data file** in the `input/` folder as `data.csv`
3. **Double-click the batch files** in the order shown below:

## Processing Steps

### Step 01: Remove Header Lines
**File:** `run_step_01.bat`

Double-click this file to:
- Remove unnecessary header lines from your CSV
- Keep only sample names and column headers
- Save result to `output/01_header_removed.csv`
- Update `input/data.csv` with the processed version

### Step 02: Round Mass Columns
**File:** `run_step_02.bat`

Double-click this file to:
- Round all Mass columns (odd-numbered columns) to N decimal places
- You will be asked how many decimal places you want (e.g., 2, 3, 4)
- Save result to `output/02_mass_rounded.csv`
- Update `input/data.csv` with the processed version

### Step 03: Create Aligned Mass List
**File:** `run_step_03.bat`

Double-click this file to:
- Collect all unique mass values from all Mass columns
- Sort them in ascending order
- Add sample headers as columns (empty, ready to be filled)
- Save result to `output/03_aligned.csv`

### Step 04: Fill Aligned with Intensities
**File:** `run_step_04.bat`

Double-click this file to:
- Read data from `input/data.csv`
- For each mass in the aligned table, sum the corresponding intensities
- Fill each sample column with the summed intensities
- Replace empty cells with 0
- Save result to `output/04_aligned_filled.csv`
- **Note:** This step requires Step 03 to be completed first

### Step 05: Clean Aligned (Remove Zero Rows)
**File:** `run_step_05.bat`

Double-click this file to:
- Read `output/04_aligned_filled.csv`
- Remove rows where all intensities are zero (masses with no signal)
- Save result to `output/05_aligned_clean.csv`
- **This is your final clean dataset ready for analysis!**
- **Note:** This step requires Step 04 to be completed first

## Troubleshooting

### "ModuleNotFoundError" when running
- Make sure you created the virtual environment: `python -m venv venv`
- Make sure you installed dependencies: `venv\Scripts\pip install -r requirements.txt`

### Scripts don't run
- Run the batch files from this folder only
- Don't move the batch files to another location

### Need help?
- Check the main README.md in the project root folder
- Make sure Python 3.7+ is installed

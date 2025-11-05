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

### OPTIONAL: Apply Noise Threshold
**File:** `run_noise_threshold.bat`

⚠️ **OPTIONAL STEP - Run between Step 04 and Step 05** ⚠️

Double-click this file to:
- Read `output/04_aligned_filled.csv`
- Ask for a noise threshold level (e.g., 100, 500, 1000)
- Set all values <= threshold to 0 (removes low-intensity noise)
- **OVERWRITES** `output/04_aligned_filled.csv` with filtered data
- **Note:** Only run if you want to apply noise filtering!

### Step 05: Add Total Sum Column
**File:** `run_step_05.bat`

Double-click this file to:
- Read `output/04_aligned_filled.csv`
- Add 'Total' column with sum of all intensities per mass
- Save result to `output/05_aligned_with_total.csv`
- **Note:** This step requires Step 04 to be completed first

### Step 06: Remove Zero Rows
**File:** `run_step_06.bat`

Double-click this file to:
- Remove masses with no signal in any sample (Total = 0)
- Save result to `output/06_aligned_clean.csv`

### Step 07: Calculate BFF
**File:** `run_step_07.bat`

Double-click this file to:
- Calculate BFF (Background Filter Factor) from Blank columns
- You will be asked for threshold multiplier (e.g., 3, 10)
- Save result to `output/07_aligned_with_bff.csv`

### Step 08: Subtract BFF
**File:** `run_step_08.bat`

Double-click this file to:
- Subtract BFF from all sample columns (background correction)
- Save result to `output/08_aligned_bff_subtracted.csv`

### Step 09: Convert Negatives to Zero
**File:** `run_step_09.bat`

Double-click this file to:
- Convert all negative values to zero (below-background signals)
- Save result to `output/09_aligned_final.csv`

### Step 10: Add QC/RCP Totals
**File:** `run_step_10.bat`

Double-click this file to:
- Calculate QC_RCP_Total and Samples_Total for quality control
- Save result to `output/10_aligned_with_qc_totals.csv`

### Step 11: Remove QC/RCP Noise
**File:** `run_step_11.bat`

Double-click this file to:
- Remove rows where QC_RCP_Total = 0 or Samples_Total = 0
- Save result to `output/11_aligned_qc_filtered.csv`
- **This is your final QC-validated dataset!**

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

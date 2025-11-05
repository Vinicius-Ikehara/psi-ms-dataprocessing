# Mass Spectrometry Data Processing Pipeline

Automated Python pipeline for processing mass spectrometry data. Transform your raw data into clean, aligned, and quality-controlled datasets ready for analysis.

---

## 🚀 Quick Start (3 Simple Steps!)

### Step 1: Install Python
1. Download Python 3.7+ from [python.org](https://www.python.org/downloads/)
2. **IMPORTANT:** During installation, check **"Add Python to PATH"**
3. Complete the installation

### Step 2: Download and Setup
1. Download this project and save it to a folder on your computer
2. Open the project folder
3. **Double-click** `setup.bat` (this installs everything automatically)
4. Wait for setup to complete

### Step 3: Process Your Data
1. Place your CSV file in the `input/` folder and name it `data.csv`
2. Open the `RUN_SCRIPTS/` folder
3. **Double-click** each `.bat` file in order: `run_step_01.bat`, `run_step_02.bat`, etc.
4. Wait for each step to finish before moving to the next

**That's it!** Your processed data will be in the `output/` folder.

---

## 📊 Complete Processing Pipeline (11 Steps + 1 Optional)

Each step has a `.bat` file - just **double-click** to run:

```
📁 input/data.csv (your raw data)
    ↓
Step 01 → Remove header lines
    ↓
Step 02 → Round mass values (you choose precision)
    ↓
Step 03 → Create aligned mass list
    ↓
Step 04 → Fill with intensities
    ↓
[OPTIONAL] → Apply noise threshold (removes low signals)
    ↓
Step 05 → Add total sum column
    ↓
Step 06 → Remove zero rows
    ↓
Step 07 → Calculate BFF (you choose threshold)
    ↓
Step 08 → Subtract BFF (background correction)
    ↓
Step 09 → Convert negatives to zero
    ↓
Step 10 → Add QC/RCP totals
    ↓
Step 11 → Remove QC/RCP noise (quality filtering)
    ↓
📁 output/11_aligned_qc_filtered.csv ✅ FINAL RESULT
```

### Detailed Step Descriptions

| Step | What It Does | Output File |
|------|--------------|-------------|
| **01** | Removes unnecessary header lines, keeps sample names and column headers | `01_header_removed.csv` |
| **02** | Rounds all mass columns to N decimal places (you choose: 2, 3, 4, etc.) | `02_mass_rounded.csv` |
| **03** | Collects all unique masses from all samples and creates sorted aligned table | `03_aligned.csv` |
| **04** | Fills the aligned table with intensity values from each sample | `04_aligned_filled.csv` |
| **OPTIONAL** | **Noise Threshold:** Sets all values ≤ threshold to 0 (overwrites file 04) | `04_aligned_filled.csv` |
| **05** | Adds 'Total' column with sum of all intensities per mass | `05_aligned_with_total.csv` |
| **06** | Removes masses with no signal in any sample (Total = 0) | `06_aligned_clean.csv` |
| **07** | Calculates BFF (Background Filter Factor) from Blank columns (you choose threshold: 3, 10, etc.) | `07_aligned_with_bff.csv` |
| **08** | Subtracts BFF from all sample columns (background correction) | `08_aligned_bff_subtracted.csv` |
| **09** | Converts all negative values to zero (below-background signals) | `09_aligned_final.csv` |
| **10** | Calculates QC_RCP_Total and Samples_Total for quality control | `10_aligned_with_qc_totals.csv` |
| **11** | Removes noise: rows where QC/RCP = 0 or Samples = 0 | `11_aligned_qc_filtered.csv` ✅ |

---

## 📂 Project Structure

```
psims-dataprocessing/
│
├── input/                          # Place your data.csv here
│   └── data.csv
│
├── output/                         # All processed files appear here
│   ├── 01_header_removed.csv
│   ├── 02_mass_rounded.csv
│   ├── 03_aligned.csv
│   ├── 04_aligned_filled.csv
│   ├── 05_aligned_with_total.csv
│   ├── 06_aligned_clean.csv
│   ├── 07_aligned_with_bff.csv
│   ├── 08_aligned_bff_subtracted.csv
│   ├── 09_aligned_final.csv
│   ├── 10_aligned_with_qc_totals.csv
│   └── 11_aligned_qc_filtered.csv  # ⭐ FINAL FILE
│
├── RUN_SCRIPTS/                    # Double-click these!
│   ├── run_step_01.bat
│   ├── run_step_02.bat
│   ├── run_step_03.bat
│   ├── run_step_04.bat
│   ├── run_noise_threshold.bat     # ⚠️ OPTIONAL (between 04-05)
│   ├── run_step_05.bat
│   ├── run_step_06.bat
│   ├── run_step_07.bat
│   ├── run_step_08.bat
│   ├── run_step_09.bat
│   ├── run_step_10.bat
│   └── run_step_11.bat
│
├── scripts/                        # Python scripts (run by .bat files)
├── utils/                          # Helper functions
├── config.py                       # Configuration
├── requirements.txt                # Python dependencies
└── setup.bat                       # Setup script (run once)
```

---

## 💡 What the .bat Files Do

Each `.bat` file automatically:
- ✅ Activates the Python virtual environment
- ✅ Runs the corresponding Python script
- ✅ Shows progress and results
- ✅ Pauses so you can read the output

**You don't need to type commands or use the terminal!**

---

## 📋 Input File Requirements

Your CSV file should have:
- **Format:** Mass/Intensity column pairs for each sample
- **Delimiter:** Semicolon (`;`), comma (`,`), or tab (auto-detected)
- **Encoding:** UTF-8 (with or without BOM)

**Example:**
```
Sample1,Sample1,Sample2,Sample2,Blank1,Blank1,QC1,QC1
Mass,Intensity,Mass,Intensity,Mass,Intensity,Mass,Intensity
100.52,1234.56,100.51,2345.67,100.50,123.45,100.52,2000.00
101.34,2345.67,101.35,3456.78,101.33,234.56,101.34,3000.00
...
```

**Important columns:**
- **Blank columns:** Used for BFF calculation (Step 07)
- **QC/RCP columns:** Used for quality control filtering (Steps 10-11)

---

## 🎯 Key Features

### Optional Noise Threshold (Between Steps 04-05)
An optional intermediate step to remove low-intensity noise:
- **When to use:** If you want to filter out weak signals before further processing
- **How it works:** All values ≤ your specified threshold are set to 0
- **Important:** This step **OVERWRITES** the file `04_aligned_filled.csv`
- **Performance:** Uses vectorized pandas operations for fast processing on large datasets
- **Usage:** Run `run_noise_threshold.bat` after Step 04 and before Step 05

### Background Correction (Steps 07-09)
The pipeline calculates and subtracts background noise using Blank samples:
- **Step 07:** Calculates BFF = mean + (threshold × std_dev) from Blank columns
- **Step 08:** Subtracts BFF from all samples
- **Step 09:** Converts negative values (below background) to zero

### Quality Control Filtering (Steps 10-11)
Removes contamination and noise using QC/RCP controls:
- **Step 10:** Sums QC/RCP columns and sample columns separately
- **Step 11:** Removes rows where:
  - QC_RCP_Total = 0 (not in controls = contamination)
  - OR Samples_Total = 0 (not in samples = irrelevant)

---

## 🔧 Configuration (Optional)

If needed, edit `config.py` to customize:

```python
# Input file name (default: data.csv)
INPUT_FILE = os.path.join(INPUT_DIR, "data.csv")

# File encoding (default: utf-8-sig)
ENCODING = 'utf-8-sig'  # or 'utf-8', 'latin-1', 'cp1252'

# Delimiter (default: auto-detected)
DELIMITER = ';'  # or ',', '\t', '|'
```

---

## 🐛 Troubleshooting

### "Python is not recognized as a command"
**Problem:** Python not installed or not in PATH
**Solution:**
1. Install Python from [python.org](https://www.python.org/downloads/)
2. **During installation, CHECK "Add Python to PATH"**
3. Restart your computer
4. Run `setup.bat` again

### "ModuleNotFoundError: No module named 'pandas'"
**Problem:** Dependencies not installed
**Solution:**
1. Double-click `setup.bat` again
2. Wait for it to complete
3. If still failing, open Command Prompt and run:
   ```
   cd path\to\project
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

### setup.bat won't run
**Problem:** PowerShell execution policy
**Solution:**
1. Open PowerShell as Administrator
2. Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
3. Run `setup.bat` again

### File not found errors
**Check:**
- Is your CSV file in `input/` folder?
- Is it named `data.csv`?
- Did you run the previous steps first?

### Encoding errors / strange characters
**Solution:** Edit `config.py` and try different encodings:
```python
ENCODING = 'utf-8'      # Try first
ENCODING = 'latin-1'    # Try second
ENCODING = 'cp1252'     # Try third
```

### No columns with "Blank" found (Step 07)
**Problem:** Your data doesn't have Blank samples
**Impact:** BFF will be zero for all rows (no background correction)
**Note:** This is OK if you don't have blank samples, but background correction won't be applied

### No columns with "QC" or "RCP" found (Step 10)
**Problem:** Your data doesn't have QC/RCP samples
**Impact:** Step 11 will remove rows where Samples_Total = 0 only
**Note:** You should have at least QC columns for proper quality control

---

## 📊 Understanding the Output

### After Step 06: Basic Processing Complete
- Data is aligned across all samples
- Zero-signal masses removed
- Ready for background correction

### After Step 09: Background Correction Complete
- Background noise (BFF) calculated and subtracted
- Negative values (below background) converted to zero
- Ready for quality control

### After Step 11: Final Dataset (RECOMMENDED)
- Quality control filtering applied
- Contamination removed (signals not in QC/RCP)
- Irrelevant data removed (zero signals)
- **This is your final, validated dataset**

---

## 🔬 Dependencies

Automatically installed by `setup.bat`:
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **scipy** - Scientific computing
- **matplotlib** - Visualization
- **openpyxl** - Excel support

---

## 📚 For Advanced Users

### Running via Command Line

If you prefer using the terminal:

```bash
# Activate environment
venv\Scripts\activate

# Run scripts manually
python scripts\01_remove_header_lines.py
python scripts\02_round_mass.py
# ... etc
```

### Linux/Mac Support

```bash
# Initial setup
chmod +x setup.sh
./setup.sh

# Activate environment
source venv/bin/activate

# Run scripts
python scripts/01_remove_header_lines.py
# ... etc
```

### Adding Custom Steps

1. Create new script: `scripts/12_your_operation.py`
2. Create batch file: `RUN_SCRIPTS/run_step_12.bat`
3. Follow the template from existing scripts

---

## 🤝 Contributing

Contributions welcome!

1. Fork the repository
2. Create a branch (`git checkout -b feature/new-step`)
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

[Add your license here]

---

## 👥 Authors

[Add authors here]

---

## 🙏 Acknowledgments

This pipeline was developed to make mass spectrometry data processing more efficient, reproducible, and accessible for researchers. It provides a complete workflow from raw data export to quality-controlled, analysis-ready datasets.

---

## 📞 Support

- 🐛 Report issues: [GitHub Issues](https://github.com/Vinicius-Ikehara/psims-dataprocessing/issues)
- 💬 Questions: Open an issue with the "question" label
- 📖 Documentation: This README

---

## 🔄 Version History

- **v2.0** - Extended to 11-step pipeline with background correction and QC filtering
- **v1.0** - Initial release with 6-step basic processing

---

**Developed with ❤️ to facilitate mass spectrometry research**

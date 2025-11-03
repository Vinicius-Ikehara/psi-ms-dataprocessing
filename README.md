# Mass Spectrometry Data Processing Pipeline

Automated Python pipeline for processing mass spectrometry data. Transform your raw data into clean, aligned datasets ready for analysis.

---

## 🚀 Quick Start (3 Simple Steps!)

### 1️⃣ Install Python
- Download and install Python 3.7+ from [python.org](https://www.python.org/downloads/)
- **IMPORTANT:** During installation, check "Add Python to PATH"

### 2️⃣ Download and Setup the Project
```bash
git clone https://github.com/Vinicius-Ikehara/psims-dataprocessing.git
cd psims-dataprocessing
setup.bat
```

### 3️⃣ Place Your File and Run
- Place your CSV file in the `input/` folder named `data.csv`
- Open the `RUN_SCRIPTS/` folder
- **Double-click** each `.bat` file in order (01, 02, 03...)

**That's it!** 🎉

---

## 📊 Processing Pipeline (6 Steps)

Each step has a `.bat` file in the `RUN_SCRIPTS/` folder - just **double-click** to execute:

```
📁 input/data.csv (your raw file)
    ↓
🔹 run_step_01.bat → Remove unnecessary header lines
    ↓
🔹 run_step_02.bat → Round mass values (you choose decimal places)
    ↓
🔹 run_step_03.bat → Create aligned list with all unique masses
    ↓
🔹 run_step_04.bat → Fill table with intensities
    ↓
🔹 run_step_05.bat → Add total sum column
    ↓
🔹 run_step_06.bat → Remove rows with no signal (zeros)
    ↓
📁 output/06_aligned_clean.csv (FINAL RESULT)
```

### Step Descriptions

| Step | Script | What It Does | Output File |
|------|--------|--------------|-------------|
| **01** | Remove Header Lines | Removes unnecessary header lines, keeps only sample names and headers | `01_header_removed.csv` |
| **02** | Round Mass | Rounds all mass columns to N decimal places (you choose) | `02_mass_rounded.csv` |
| **03** | Create Aligned | Collects all unique masses from all samples, sorts and creates base table | `03_aligned.csv` |
| **04** | Fill Intensities | Fills the aligned table with corresponding intensities from each sample | `04_aligned_filled.csv` |
| **05** | Add Total | Adds 'Total' column with sum of intensities across all samples | `05_aligned_with_total.csv` |
| **06** | Remove Zeros | Removes masses with no signal in any sample (Total = 0) | `06_aligned_clean.csv` ✅ |

---

## 📂 Project Structure

```
psims-dataprocessing/
│
├── input/                          # 📥 Place your data.csv here
│   └── data.csv
│
├── output/                         # 📤 All processed files
│   ├── 01_header_removed.csv
│   ├── 02_mass_rounded.csv
│   ├── 03_aligned.csv
│   ├── 04_aligned_filled.csv
│   ├── 05_aligned_with_total.csv
│   └── 06_aligned_clean.csv      # ⭐ FINAL FILE
│
├── RUN_SCRIPTS/                    # 🎯 Double-click here!
│   ├── run_step_01.bat            # Click to run step 1
│   ├── run_step_02.bat            # Click to run step 2
│   ├── run_step_03.bat            # Click to run step 3
│   ├── run_step_04.bat            # Click to run step 4
│   ├── run_step_05.bat            # Click to run step 5
│   └── run_step_06.bat            # Click to run step 6
│
├── scripts/                        # Python scripts (executed by .bat files)
├── utils/                          # Helper functions
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
└── setup.bat                       # Initial setup script
```

---

## ⚙️ How to Use

### First Time (Setup)

1. **Clone or download the project**
   ```bash
   git clone https://github.com/Vinicius-Ikehara/psims-dataprocessing.git
   cd psims-dataprocessing
   ```

2. **Run the setup** (only need to do this once!)
   ```bash
   setup.bat
   ```
   This will:
   - Create Python virtual environment
   - Install all necessary dependencies

### Processing Your Data

1. **Place your file:**
   - Copy your CSV to `input/data.csv`

2. **Open the `RUN_SCRIPTS/` folder**

3. **Execute steps in order:**
   - **Double-click** `run_step_01.bat` ➜ wait for completion
   - **Double-click** `run_step_02.bat` ➜ wait for completion
   - **Double-click** `run_step_03.bat` ➜ wait for completion
   - **Double-click** `run_step_04.bat` ➜ wait for completion
   - **Double-click** `run_step_05.bat` ➜ wait for completion
   - **Double-click** `run_step_06.bat` ➜ wait for completion

4. **Get your result:**
   - Final file is in `output/06_aligned_clean.csv`

**That's all! Simple as that!** 🎊

---

## 💡 What Do the .bat Files Do?

Each `.bat` file automatically:
- ✅ Activates the Python virtual environment
- ✅ Runs the corresponding Python script
- ✅ Shows progress on screen
- ✅ Pauses at the end so you can see results

**You don't need to open terminals, type commands, or activate virtual environments manually!**

---

## 📋 Input File Format

**Your CSV should have:**
- Mass/Intensity column pairs for each sample
- Delimiter: `;` (semicolon), `,` (comma), or `tab` (auto-detected)
- Encoding: UTF-8 (with or without BOM)

**Example:**
```
Sample1,Sample1,Sample2,Sample2,Sample3,Sample3
Mass,Intensity,Mass,Intensity,Mass,Intensity
100.52,1234.56,100.51,2345.67,100.53,3456.78
101.34,2345.67,101.35,3456.78,101.33,4567.89
...
```

---

## 🔧 Configuration (Optional)

If you need to customize, edit the `config.py` file:

```python
# Input file name (if not data.csv)
INPUT_FILE = os.path.join(INPUT_DIR, "data.csv")

# File encoding (if you have reading issues)
ENCODING = 'utf-8-sig'  # or 'utf-8', 'latin-1', 'cp1252'

# Delimiter (if you want to force a specific one)
DELIMITER = ';'  # or ',', '\t', '|'
```

---

## 🐛 Common Issues

### ❌ "Python is not recognized as a command"

**Cause:** Python is not installed or not in PATH

**Solution:**
1. Install Python from [python.org](https://www.python.org/downloads/)
2. **Important:** Check "Add Python to PATH" during installation
3. Restart terminal/computer

### ❌ "ModuleNotFoundError: No module named 'pandas'"

**Cause:** Dependencies were not installed

**Solution:**
```bash
setup.bat
```
If still not working:
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### ❌ Error running setup.bat

**Solution (PowerShell):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then run `setup.bat` again.

### ❌ File not found

**Check:**
- ✅ Is your CSV in `input/data.csv`?
- ✅ Is the name correct?
- ✅ Did you run previous steps first?

### ❌ Encoding error/strange characters

**Solution:** Edit `config.py` and try different encodings:
```python
ENCODING = 'utf-8'      # Try this first
ENCODING = 'latin-1'    # Then this
ENCODING = 'cp1252'     # Last this
```

---

## 🎯 Features

- ✅ **Super Easy**: Just two clicks per step
- ✅ **Automatic**: `.bat` scripts do everything
- ✅ **Smart Detection**: Delimiter detected automatically
- ✅ **Large Files**: Processes hundreds of MB efficiently
- ✅ **Real-Time Feedback**: See progress on screen
- ✅ **Data Validation**: Checks if files are correct
- ✅ **Complete History**: All intermediate files are saved

---

## 🔬 Dependencies

The project uses these Python libraries:
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **scipy** - Scientific computing
- **matplotlib** - Visualization
- **openpyxl** - Excel support

*All installed automatically by `setup.bat`*

---

## 📚 For Advanced Users

### Run via Command Line

If you prefer using the terminal:

```bash
# Activate virtual environment
venv\Scripts\activate

# Run scripts
python scripts\01_remove_header_lines.py
python scripts\02_round_mass.py
python scripts\03_create_aligned.py
python scripts\04_fill_aligned_intensities.py
python scripts\05_clean_aligned.py
python scripts\06_remove_zero_rows.py
```

### Linux/Mac

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

### Adding New Steps

1. Create a new script in `scripts/07_your_operation.py`
2. Create a `.bat` file in `RUN_SCRIPTS/run_step_07.bat`
3. Follow the template from existing scripts

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a branch (`git checkout -b feature/new-step`)
3. Make your changes
4. Test thoroughly
5. Open a Pull Request

---

## 📄 License

[Add your license here]

---

## 👥 Authors

[Add authors here]

---

## 🙏 Acknowledgments

This pipeline was developed to make mass spectrometry data processing more efficient, reproducible, and accessible for researchers.

---

## 📞 Support

- 🐛 Report bug: [GitHub Issues]
- 💬 Questions: [Contact]
- 📖 Documentation: This README

---

**Developed with ❤️ to facilitate your mass spectrometry research**

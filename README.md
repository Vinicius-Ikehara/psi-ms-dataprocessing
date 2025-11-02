# Mass Spectrometry Data Processor

A modular Python-based toolkit for processing and analyzing mass spectrometry data from CSV files. This project provides a collection of standalone scripts that can be executed independently to perform various data processing operations.

---

## 🚀 SETUP RÁPIDO - LEIA ISTO PRIMEIRO!

### ⚠️ IMPORTANTE: Você PRECISA criar o ambiente virtual!

**Este projeto usa bibliotecas Python que precisam ser instaladas. Siga os passos abaixo:**

### Passo 1: Clone ou baixe este repositório
```bash
git clone https://github.com/Vinicius-Ikehara/psims-dataprocessing.git
cd psims-dataprocessing
```

### Passo 2: Crie o ambiente virtual (venv)

**Windows:**
```bash
python -m venv venv
```

**Linux/Mac:**
```bash
python3 -m venv venv
```

### Passo 3: Ative o ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

**✅ Você saberá que o venv está ativo quando ver `(venv)` antes do seu prompt no terminal.**

### Passo 4: Instale as dependências
```bash
pip install -r requirements.txt
```

### Passo 5: Coloque seu arquivo CSV
- Copie seu arquivo CSV para a pasta `input/`
- Renomeie para `data.csv` (ou altere o nome em `config.py`)

### Passo 6: Execute o script
```bash
python scripts/01_remove_header_lines.py
```

### 🔴 COMUM ERRO: "ModuleNotFoundError"
Se você ver este erro, significa que:
1. Você NÃO criou o ambiente virtual, OU
2. Você NÃO ativou o ambiente virtual (passo 3), OU
3. Você NÃO instalou as dependências (passo 4)

**Solução:** Volte ao Passo 2 e siga todos os passos em ordem!

---

## Features

- **Modular Design**: Each processing step is a separate script that can be run independently
- **Large File Support**: Efficient processing of large CSV files (hundreds of MB)
- **Easy to Extend**: Add new processing scripts following the established pattern
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Well Documented**: Clear code comments and docstrings

## Project Structure

```
psims-dataprocessing/
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

## Setup Detalhado

### Opção 1: Setup Automático (Recomendado)

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

### Opção 2: Setup Manual (Passo a Passo)

1. **Clone ou baixe este repositório**

2. **Crie o ambiente virtual:**
   ```bash
   # Windows
   python -m venv venv

   # Linux/Mac
   python3 -m venv venv
   ```

3. **Ative o ambiente virtual:**
   ```bash
   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

   **Confirme que está ativo:** Você deve ver `(venv)` no início do prompt.

4. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Coloque seu arquivo de dados:**
   - Copie seu arquivo CSV para a pasta `input/`
   - Renomeie para `data.csv` (ou atualize o nome em `config.py`)

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

## Troubleshooting (Solução de Problemas)

### ❌ Erro: "ModuleNotFoundError: No module named 'pandas'" (ou numpy, scipy, etc.)

**Causa:** Você não instalou as dependências ou não ativou o ambiente virtual.

**Solução:**
1. Certifique-se de que o ambiente virtual está ativo (você deve ver `(venv)` no prompt)
2. Se não estiver ativo, execute:
   - **Windows:** `venv\Scripts\activate`
   - **Linux/Mac:** `source venv/bin/activate`
3. Instale as dependências: `pip install -r requirements.txt`

### ❌ Erro: "python: command not found"

**Causa:** Python não está instalado ou não está no PATH.

**Solução:**
1. Instale o Python 3.7 ou superior de [python.org](https://www.python.org/downloads/)
2. **Windows:** Durante a instalação, marque a opção "Add Python to PATH"
3. **Linux/Mac:** Python geralmente já vem instalado. Tente usar `python3` em vez de `python`

### ❌ Ambiente virtual não ativa

**Windows:**
- Certifique-se de usar `venv\Scripts\activate` (não apenas `activate`)
- Se der erro de execução de scripts, execute no PowerShell como administrador:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

**Linux/Mac:**
- Use `source venv/bin/activate` (não esqueça do `source`)
- Se der "permission denied", execute: `chmod +x venv/bin/activate`

### ❌ Erro: "Permission denied" no setup.sh

**Solução:**
```bash
chmod +x setup.sh
./setup.sh
```

### ❌ Erro de encoding ao ler arquivo CSV

**Solução:**
Edite o arquivo `config.py` e altere a variável `ENCODING`:
```python
ENCODING = 'utf-8'  # ou 'latin-1', 'cp1252', dependendo do seu arquivo
```

### ❌ Arquivo de saída não aparece na pasta output/

**Verifique:**
1. Se o script terminou sem erros
2. Se o arquivo de entrada está na pasta `input/`
3. Se o nome do arquivo está correto em `config.py`
4. Procure por mensagens de erro no terminal

### 💡 Dica: Como saber se o venv está ativo?

Quando o ambiente virtual está ativo, você verá `(venv)` no início da linha do terminal:

**Ativo:**
```
(venv) C:\Users\Work\Documents\PROJETOS\Brena>
```

**Inativo:**
```
C:\Users\Work\Documents\PROJETOS\Brena>
```

### 💡 Preciso ativar o venv toda vez?

**Sim!** Toda vez que você abrir um novo terminal, você precisa ativar o ambiente virtual antes de executar os scripts.

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

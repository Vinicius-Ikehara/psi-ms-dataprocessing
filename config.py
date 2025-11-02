"""
Configuration file for mass spectrometry data processing project
"""
import os

# Directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Input file
INPUT_FILE = os.path.join(INPUT_DIR, "data.csv")

# Processing settings
CHUNK_SIZE = 10000  # Number of lines to process at once (for large files)
ENCODING = 'utf-8-sig'  # To handle BOM (﻿) at the beginning of file

# Separators
DELIMITER = ';'  # File uses semicolon as separator

# Output settings
OUTPUT_ENCODING = 'utf-8'

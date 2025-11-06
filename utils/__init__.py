# Pacote de utilitários
import os


def get_decimal_places(output_dir):
    """
    Reads the decimal places configuration saved by script 02

    Args:
        output_dir: The OUTPUT directory path

    Returns:
        Number of decimal places (int), defaults to 2 if config not found
    """
    config_file = os.path.join(output_dir, ".decimal_config")

    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                return int(f.read().strip())
        except (ValueError, IOError):
            print("[WARNING] Could not read decimal config, using default: 2")
            return 2
    else:
        print("[WARNING] Decimal config not found, using default: 2")
        return 2

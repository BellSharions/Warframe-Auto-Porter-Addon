import subprocess
from pathlib import Path

from ..constants import extractor_commands


def extract_texture_with_cli(extractor_path, cache_path, texture_format, internal_path, output_dir):
    cmd = extractor_commands["Texture"].format(
        Path(extractor_path), Path(cache_path), texture_format, internal_path, Path(output_dir)
    )

    try:
        print(f"Running command: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Successfully extracted texture: {internal_path}")
            return True
        else:
            print(f"Extractor failed with error: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error running extractor: {e!s}")
        return False


def extract_material_with_cli(extractor_path, cache_path, internal_path, output_dir):
    cmd = extractor_commands["Material"].format(
        Path(extractor_path), Path(cache_path), internal_path, Path(output_dir)
    )

    try:
        print(f"Running command: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Successfully extracted material: {internal_path}")
            return True
        else:
            print(f"Extractor failed with error: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error running extractor: {e!s}")
        return False

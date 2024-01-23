#!.venv/bin/python3
import os
import shutil
import subprocess

import sys

PAPER_DIR_NAME = "doc/water"  # Paper directory name
PAPER_NAME = "paper.tex"  # Paper file name
OUT_DIR_NAME = "out"  # Output directory name
CALLEE_DIR_NAME = os.path.dirname(os.path.realpath(__file__))  # Callee directory name


def call_pdflatex():
    """Call the pdfLaTeX compiler."""
    # Change to the paper directory
    os.chdir(PAPER_DIR_NAME)

    # Call the pdfLaTeX compiler
    subprocess.call(["pdflatex", "-output-directory", os.path.join(CALLEE_DIR_NAME, OUT_DIR_NAME), PAPER_NAME])

    # Change back to the original directory
    os.chdir(CALLEE_DIR_NAME)


def main():
    """Call the pdfLaTeX compiler."""
    # Check if the paper directory exists
    if not os.path.isdir(PAPER_DIR_NAME):
        print("Error: The paper directory does not exist.")
        sys.exit(1)

    # Check if the output directory exists
    if os.path.isdir(OUT_DIR_NAME):
        # Delete the output directory
        shutil.rmtree(OUT_DIR_NAME)

    # Create the output directory
    os.mkdir(OUT_DIR_NAME)


# Call the main function
if __name__ == "__main__":
    main()
    call_pdflatex()

# %%

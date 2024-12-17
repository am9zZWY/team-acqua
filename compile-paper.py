#!.venv/bin/python3
import os
import shutil
import subprocess

import sys

CALLEE_DIR = os.path.dirname(os.path.realpath(__file__))  # Callee directory name
PAPER_DIR = os.path.join(CALLEE_DIR, "doc")  # Paper directory name
PAPER_NAME = "paper.tex"  # Paper file name
OUT_DIR = os.path.join(CALLEE_DIR, "out")  # Output directory name


def call_pdflatex():
    """Call the pdfLaTeX compiler."""
    # Change to the paper directory
    os.chdir(PAPER_DIR)

    # Call the pdfLaTeX compiler
    subprocess.call(["pdflatex", "-output-directory", OUT_DIR, PAPER_NAME])

    # Change back to the original directory
    os.chdir(CALLEE_DIR)


def main():
    # Check if the paper directory exists
    if not os.path.isdir(PAPER_DIR):
        print("Error: The paper directory does not exist.")
        sys.exit(1)

    # Check if the output directory exists
    if os.path.isdir(OUT_DIR):
        # Delete the output directory
        shutil.rmtree(OUT_DIR)

    # Create the output directory
    os.mkdir(OUT_DIR)

    # Call the pdfLaTeX compiler
    call_pdflatex()


# Call the main function
if __name__ == "__main__":
    main()

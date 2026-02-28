#!/usr/bin/env python3
"""Build script to package NHL Trade Analyzer as a Windows executable using PyInstaller."""

import subprocess
import sys


def build():
    """Build the Windows executable."""
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "NHL Trade Analyzer",
        "--onefile",
        "--windowed",
        "--add-data", "src;src",
        "--hidden-import", "customtkinter",
        "--hidden-import", "openai",
        "--hidden-import", "PIL",
        "--collect-all", "customtkinter",
        "main.py",
    ]

    print("Building NHL Trade Analyzer...")
    print(f"Command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    print("\nBuild complete! Executable is in the 'dist' folder.")


if __name__ == "__main__":
    build()

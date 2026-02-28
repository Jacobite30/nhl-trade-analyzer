#!/usr/bin/env python3
"""NHL Trade Analyzer - AI-Powered Trade Analysis Tool.

A Windows desktop application that uses AI to analyze NHL trades,
providing grades, impact analysis, and historical comparisons.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.gui import NHLTradeAnalyzerApp


def main():
    """Launch the NHL Trade Analyzer application."""
    app = NHLTradeAnalyzerApp()
    app.mainloop()


if __name__ == "__main__":
    main()

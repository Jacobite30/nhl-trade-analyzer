# NHL Trade Analyzer - AI-Powered Trade Analysis

A Windows desktop application that uses AI (OpenAI GPT) to analyze NHL trades, providing comprehensive grades, impact analysis, salary cap implications, and historical comparisons.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green.svg)
![OpenAI](https://img.shields.io/badge/AI-OpenAI%20GPT-orange.svg)

## Features

- **AI-Powered Analysis**: Uses OpenAI GPT models to provide expert-level trade analysis
- **Trade Grades**: Letter grades (A+ to F) for each team involved in the trade
- **Impact Analysis**: Detailed pros/cons, cap impact, and competitive window assessment
- **Historical Comparisons**: AI compares your trade to similar historical NHL trades
- **Fairness Score**: 1-10 scale showing which team benefits more
- **Full NHL Team Support**: All 32 NHL teams with accurate colors
- **Flexible Asset Input**: Add players (with cap hit, age, contract details), draft picks, and prospects
- **Salary Retention**: Support for salary retention percentages in trades
- **Trade History**: Track all analyzed trades within your session
- **Modern Dark UI**: Sleek, hockey-themed dark interface

## Screenshots

The app features a dark-themed modern interface with:
- Team selection dropdowns with all 32 NHL teams
- Side-by-side trade asset panels for each team
- Player, draft pick, and prospect input forms
- Real-time AI analysis results with grades and detailed breakdown

## Requirements

- Python 3.9 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation

### Option 1: Quick Launch (double-click)

1. Download and extract the ZIP from GitHub
2. Install dependencies once: open Command Prompt in the folder and run `pip install -r requirements.txt`
3. Double-click **`NHL Trade Analyzer.bat`** to launch the app anytime

### Option 2: Build Standalone .exe

1. Install dependencies: `pip install -r requirements.txt`
2. Double-click **`build_exe.bat`** (or run `python build.py`)
3. Your standalone `.exe` will be in the `dist/` folder — copy it anywhere and run it without needing Python

### Option 3: Run from Command Prompt

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Jacobite30/nhl-trade-analyzer.git
   cd nhl-trade-analyzer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

## Usage

1. **Set up your API key**: Click the ⚙ Settings button and enter your OpenAI API key
2. **Select teams**: Choose the two teams involved in the trade from the dropdowns
3. **Add assets**: For each team, add the players, draft picks, and/or prospects they are sending
   - **Players**: Enter name, position, age, cap hit, contract years, and salary retention
   - **Draft Picks**: Select from available future draft picks
   - **Prospects**: Enter prospect name and position
4. **Analyze**: Click "Analyze Trade" and wait for the AI analysis
5. **Review**: Read the comprehensive breakdown including grades, pros/cons, and cap implications

## AI Models

The app supports multiple OpenAI models:
- **GPT-4o** (default): Best analysis quality
- **GPT-4o-mini**: Faster and cheaper, good quality
- **GPT-4-turbo**: High quality, slightly slower
- **GPT-3.5-turbo**: Fastest and cheapest, basic analysis

## Project Structure

```
nhl-trade-analyzer/
├── main.py                    # Application entry point
├── NHL Trade Analyzer.bat     # Double-click launcher for Windows
├── build_exe.bat              # Double-click to build standalone .exe
├── build.py                   # PyInstaller build script (Python)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── src/
    ├── __init__.py
    ├── nhl_data.py            # NHL teams, positions, draft picks data
    ├── analyzer.py            # OpenAI-powered trade analysis engine
    └── gui.py                 # CustomTkinter GUI application
```

## Configuration

- **API Key**: Stored in memory only (not saved to disk for security)
- **Model**: Select your preferred OpenAI model in Settings

## License

MIT License - feel free to use and modify as you wish.

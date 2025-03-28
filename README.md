# pyta4j

A Python port of the excellent [TA4J](https://github.com/ta4j/ta4j) (Technical Analysis for Java) library.

**pyta4j** provides a flexible, extensible framework for building trading strategies and performing technical analysis using indicators, rules, and performance criteria.

---

## 🚀 Features

- Core components for technical analysis:
  - Candlestick bar series (`Bar`, `BarSeries`)
  - Indicators (e.g., `SMA`, `EMA`, `RSI`, `MACD`)
  - Trading rules (e.g., `StopLoss`, `StopGain`, `CrossOver`)
  - Strategy engine
  - Performance analysis criteria
- Extensible and test-driven
- Compatible with Pandas and Decimal for high-precision financial calculations
- CSV trade loaders and utilities for backtesting

---

## 📦 Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/quickfox15/pyta4j.git
   cd pyta4j/

2. **(Optional) Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate           # On Linux/macOS
   .venv\Scripts\activate              # On Windows

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

4. **Install in editable mode (recommended for development)**:
   ```bash
   pip install -e .

## 🧪 Running Tests
   Run all unit tests with:
   ```bash
   python -m unittest discover -s tests -p "test*.py"
   
## 🏁 Quickstart Example
   Run the example file:
   ```bash
   python quickstart.py

## 🗂 Project Structure
   ```bash
   pyta4j/
   ├── src/
   │   └── pyta4j/                    # Core library code
   │       ├── core/                 # Bars, trades, positions
   │       ├── indicators/           # Technical indicators
   │       ├── rules/                # Entry/exit rules
   │       ├── analysis/             # Performance criteria
   │       ├── cost/                 # Cost models
   │       └── utils/                # Helpers/loaders
   ├── tests/                        # Unit tests
   ├── quickstart.py                # Example script
   ├── requirements.txt
   ├── setup.py
   └── README.md

## 📋 Requirements
Python 3.9+

## 📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

## 🙏 Acknowledgments
ta4j – The original Java-based inspiration for this project.
Python open source community ❤️
# Module 4 — Professional Calculator

A command-line REPL calculator built with object-oriented design. It supports
addition, subtraction, multiplication, and division, keeps a history of the
session's calculations, and ships with 100% test coverage enforced through
pytest and GitHub Actions.

## Setup

```bash
# Clone and enter the project
git clone https://github.com/ZyrielZero/ProfessionalCalculator.git
cd ProfessionalCalculator

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

Start the calculator:

```bash
python main.py
```

Enter calculations in the form `<operation> <number1> <number2>`:

```
>> add 10 5
Result: AdditionCalculation: 10.0 Addition 5.0 = 15.0
>> divide 20 4
Result: DivisionCalculation: 20.0 Division 4.0 = 5.0
```

**Supported operations:** `add`, `subtract`, `multiply`, `divide`

**Special commands:** `help`, `history`, `exit`

## Running tests

```bash
pytest
```

This runs the full suite and enforces 100% coverage. The build fails if
coverage drops below 100%.
Black-Scholes Option Pricing Calculator

Project Overview and Purpose

This project is an interactive Command-Line Interface (CLI) application that calculates the theoretical price of European Call and Put options using the Black-Scholes-Merton model. It provides accurate financial pricing and basic risk analysis, serving as a robust tool for finance students and analysts.

Key Features:

Core Pricing: Accurate calculation and display of both European Call and Put Option prices.

Risk Metrics (The Greeks): Calculation and display of Delta (a measure of price sensitivity).

Input Validation: Robust error checking for numerical and financial constraints (ensuring Time and Volatility are positive).

Reach Version Feature (Sensitivity Matrix): Generation of a clear, text-based matrix showing how the Call Price changes with simultaneous 10% fluctuations in Stock Price (S) and Volatility (sigma).

Video Demonstration Link
https://youtu.be/I-gO2JP2flk

Technologies and Libraries Used

Language: Python 3

Standard Libraries: math

External Libraries: scipy (specifically scipy.stats.norm.cdf for the Cumulative Distribution Function)

Installation and Setup Instructions

Clone the Repository:

git clone https://github.com/agrimxsuri/Personal-project.git
cd Project


Install Dependencies:
This project requires the scipy library. Install it using pip:

pip install scipy


How to Run the Program and Reproduce Results

Running the Application (Calculator)

Navigate to the root of your project directory (Project/).

Run the main script using the Python interpreter:

python Black_Scholes_calculator.py


The program will prompt you sequentially for the five input variables.

Running Unit Tests (Verification)

To verify the core mathematical logic independently:

Ensure the test file is named tests/black_scholes_tests.py and the main app is Black_Scholes_calculator.py at the root.

Navigate to the root of your project directory (Project/).

Run the unit tests using the Python unittest module:

python -m unittest tests.black_scholes_tests


Sample Test Case to Verify (Inputs and Expected Outputs):
| Variable | Input | Units |
| :--- | :--- | :--- |
| S | 100 | $ |
| K | 100 | $ |
| T | 0.5 | years |
| r | 5.0 | % (0.05) |
| sigma | 25.0 | % (0.25) |

Expected Approximate Results:
| Output | Value |
| :--- | :--- |
| Call Price (C) | $7.66 |
| Put Price (P) | $5.19 |
| Call Delta | 0.6151 |
| Put Delta | -0.3849 |

Author(s) and Contribution Summary

Author: Agrim Suri

Contribution: Developed the Black-Scholes core logic, implemented robust CLI input validation, added Delta calculation, and created the Sensitivity Matrix feature (Reach Version).
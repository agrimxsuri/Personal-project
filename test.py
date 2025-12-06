# --- Black-Scholes Unit Tests ---
#
# This file contains unit tests for the core mathematical functions 
# (d1, d2, Call Price, Put Price, Delta) of the Black-Scholes model.
#
# To run these tests:
# 1. Navigate to the root of your project directory.
# 2. Run the command: python -m unittest tests.black_scholes_tests
#
# Requires the 'black_scholes_calculator.py' file to be available.

import unittest
import math
from black_scholes_calculator import (
    calculate_d1, calculate_d2, 
    black_scholes_call_price, black_scholes_put_price, 
    calculate_delta
)

# Test case parameters
S_TEST = 100.0   # Current Stock Price
K_TEST = 100.0   # Strike Price
T_TEST = 0.5     # Time to Expiration (0.5 years)
r_TEST = 0.05    # Risk-Free Rate (5%)
sigma_TEST = 0.25 # Volatility (25%)

# Known expected values (verified against external calculators)
EXPECTED_D1 = 0.2925
EXPECTED_D2 = 0.1160
EXPECTED_CALL_PRICE = 7.6631
EXPECTED_PUT_PRICE = 5.1882
EXPECTED_CALL_DELTA = 0.6151
EXPECTED_PUT_DELTA = -0.3849


class TestBlackScholesFunctions(unittest.TestCase):
    
    # Set a high tolerance for floating point comparisons
    TOLERANCE = 1e-4

    def test_d1_calculation(self):
        """Tests the accuracy of the d1 parameter calculation."""
        d1 = calculate_d1(S_TEST, K_TEST, T_TEST, r_TEST, sigma_TEST)
        self.assertAlmostEqual(d1, EXPECTED_D1, delta=self.TOLERANCE, 
                               msg=f"d1 mismatch. Expected: {EXPECTED_D1}, Got: {d1}")

    def test_d2_calculation(self):
        """Tests the accuracy of the d2 parameter calculation."""
        # Use the expected d1 value for a clean test of d2 formula
        d2 = calculate_d2(EXPECTED_D1, sigma_TEST, T_TEST)
        self.assertAlmostEqual(d2, EXPECTED_D2, delta=self.TOLERANCE, 
                               msg=f"d2 mismatch. Expected: {EXPECTED_D2}, Got: {d2}")

    def test_call_price_calculation(self):
        """Tests the accuracy of the European Call Option price."""
        call_price = black_scholes_call_price(S_TEST, K_TEST, T_TEST, r_TEST, sigma_TEST)
        self.assertAlmostEqual(call_price, EXPECTED_CALL_PRICE, delta=self.TOLERANCE,
                               msg=f"Call Price mismatch. Expected: {EXPECTED_CALL_PRICE}, Got: {call_price}")

    def test_put_price_calculation(self):
        """Tests the accuracy of the European Put Option price."""
        put_price = black_scholes_put_price(S_TEST, K_TEST, T_TEST, r_TEST, sigma_TEST)
        self.assertAlmostEqual(put_price, EXPECTED_PUT_PRICE, delta=self.TOLERANCE,
                               msg=f"Put Price mismatch. Expected: {EXPECTED_PUT_PRICE}, Got: {put_price}")

    def test_delta_calculation(self):
        """Tests the accuracy of Call and Put Delta."""
        call_delta, put_delta = calculate_delta(S_TEST, K_TEST, T_TEST, r_TEST, sigma_TEST)
        self.assertAlmostEqual(call_delta, EXPECTED_CALL_DELTA, delta=self.TOLERANCE,
                               msg=f"Call Delta mismatch. Expected: {EXPECTED_CALL_DELTA}, Got: {call_delta}")
        self.assertAlmostEqual(put_delta, EXPECTED_PUT_DELTA, delta=self.TOLERANCE,
                               msg=f"Put Delta mismatch. Expected: {EXPECTED_PUT_DELTA}, Got: {put_delta}")
        
    # --- Edge Cases (Input Validation Check) ---
    def test_zero_time_option(self):
        """Tests the case where time to expiration is zero (intrinsic value)."""
        T_ZERO = 0.0
        # In-the-money Call (S > K)
        call_itm = black_scholes_call_price(105, 100, T_ZERO, r_TEST, sigma_TEST)
        self.assertAlmostEqual(call_itm, 5.0, msg="T=0 ITM Call failed")
        # Out-of-the-money Put (K > S)
        put_otm = black_scholes_put_price(105, 100, T_ZERO, r_TEST, sigma_TEST)
        self.assertAlmostEqual(put_otm, 0.0, msg="T=0 OTM Put failed")
        
    def test_zero_volatility(self):
        """Tests the case where volatility is zero (deterministic outcome)."""
        sigma_ZERO = 0.0
        # Call should be the discounted intrinsic value
        call_price = black_scholes_call_price(S_TEST, K_TEST, T_TEST, r_TEST, sigma_ZERO)
        expected = max(0.0, S_TEST - K_TEST * math.exp(-r_TEST * T_TEST))
        self.assertAlmostEqual(call_price, expected, delta=self.TOLERANCE, msg="Sigma=0 Call failed")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
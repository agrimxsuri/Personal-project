# --- Black-Scholes Option Pricing Calculator (CLI Version) ---
#
# This script calculates the theoretical price of European Call and Put options
# using the Black-Scholes-Merton model via an interactive command-line interface (CLI).
#
# Requires: math (standard library) and scipy (for the Cumulative Distribution Function - CDF)
# Installation (if needed): pip install scipy

import math
import sys
from scipy.stats import norm

# ----------------- Core Mathematical Functions -----------------

def calculate_d1(S, K, T, r, sigma):
    """Calculates the d1 parameter of the Black-Scholes formula."""
    if T <= 0 or sigma <= 0:
        return 0.0

    numerator = math.log(S / K) + (r + (sigma**2) / 2) * T
    denominator = sigma * math.sqrt(T)

    return numerator / denominator

def calculate_d2(d1, sigma, T):
    """Calculates the d2 parameter of the Black-Scholes formula using d1."""
    if T <= 0:
        return 0.0
    return d1 - sigma * math.sqrt(T)

def black_scholes_call_price(S, K, T, r, sigma):
    """Calculates the theoretical price of a European Call Option."""
    if T <= 0:
        return max(0.0, S - K) # Intrinsic value at expiry
        
    d1 = calculate_d1(S, K, T, r, sigma)
    d2 = calculate_d2(d1, sigma, T)

    N_d1 = norm.cdf(d1)
    N_d2 = norm.cdf(d2)

    # C = S * N(d1) - K * exp(-r*T) * N(d2)
    call_price = (S * N_d1) - (K * math.exp(-r * T) * N_d2)
    return call_price

def black_scholes_put_price(S, K, T, r, sigma, call_price=None):
    """Calculates the theoretical price of a European Put Option using Put-Call Parity."""
    if T <= 0:
        return max(0.0, K - S)
        
    if call_price is None:
        call_price = black_scholes_call_price(S, K, T, r, sigma)

    # P = C - S + K * exp(-r*T)
    put_price = call_price - S + K * math.exp(-r * T)
    return put_price

def calculate_delta(S, K, T, r, sigma):
    """Calculates the Delta for Call and Put options (Delta_Call = N(d1))."""
    if T <= 0:
        call_delta = 1.0 if S > K else 0.0
        put_delta = -1.0 if S < K else 0.0
        return (call_delta, put_delta)
        
    d1 = calculate_d1(S, K, T, r, sigma)
    N_d1 = norm.cdf(d1)
    
    call_delta = N_d1
    put_delta = N_d1 - 1
    
    return (call_delta, put_delta)


# ----------------- CLI Input & Validation Functions -----------------

def get_validated_input(prompt, value_name, min_value=0.0, is_percent=False):
    """
    Prompts the user for a value and ensures it is a valid number,
    and optionally, is greater than or equal to a minimum value.
    Returns None if the user quits.
    """
    while True:
        try:
            value = input(prompt).strip()
            # Exit option
            if value.lower() in ('q', 'quit'):
                return None
            
            f_value = float(value)
            
            if f_value < min_value:
                print(f"Error: {value_name} must be greater than or equal to {min_value}.")
                continue
            
            # Convert percentage input (r and sigma)
            if is_percent:
                return f_value / 100.0
            
            return f_value
        
        except ValueError:
            print(f"Error: Invalid input for {value_name}. Please enter a numerical value.")


# ----------------- CLI Output Functions (Reach Version) -----------------

def generate_sensitivity_matrix(S, K, T, r, sigma, delta_percent=0.10):
    """
    Generates and prints a 3x3 sensitivity matrix for Call Price based on 
    changes in Stock Price (S) and Volatility (sigma) to the console.
    """
    print("\n" + "=" * 60)
    print("      Sensitivity Matrix: Call Price vs. S and Sigma (Reach Version)")
    print("=" * 60)
    
    # Define the changes in S and sigma to test (+10%, Base, -10%)
    s_changes = [-delta_percent, 0, delta_percent] 
    s_labels = [f"S - {delta_percent*100:.0f}%", "Base S", f"S + {delta_percent*100:.0f}%"]
    
    sigma_changes = [-delta_percent, 0, delta_percent]
    sigma_labels = [f"Sigma - {delta_percent*100:.0f}%", "Base Sigma", f"Sigma + {delta_percent*100:.0f}%"]
    
    # Header row formatting
    header = f"{'Sigma Change':<15} |" + " |".join(f"{label:<15}" for label in s_labels)
    separator = "-" * (15 * 4 + 4)
    print(separator)
    print(header)
    print(separator)

    # Nested loops to generate the 3x3 matrix
    for i, sigma_delta in enumerate(sigma_changes):
        row_prices = []
        new_sigma = sigma * (1 + sigma_delta)
        # Ensure new_sigma is positive
        if new_sigma <= 0:
            row_prices = ["N/A"] * 3
        else:
            for s_delta in s_changes:
                new_S = S * (1 + s_delta)
                
                # Calculate Call Price for the new S and new sigma
                try:
                    price = black_scholes_call_price(new_S, K, T, r, new_sigma)
                    row_prices.append(f"${price:13.2f}")
                except Exception:
                    row_prices.append("ERROR")

        # Print the row
        row_output = f"{sigma_labels[i]:<15} |" + " |".join(row_prices)
        print(row_output)
    
    print(separator)
    print(f"\nMatrix shows Call Price sensitivity around Base S (${S:.2f}) and Base Sigma ({sigma*100:.2f}%)")


# ----------------- Main Execution Block (Target Product) -----------------

def run_calculator():
    """
    The main interactive loop for the Black-Scholes Calculator.
    """
    print("=" * 60)
    print("      European Black-Scholes Option Pricing Calculator (CLI)")
    print("=" * 60)
    print("Enter the five variables. Type 'q' to quit at any time.")
    print("Note: Time (T), Stock Price (S), and Volatility (sigma) must be positive.")
    print("-" * 60)

    # 1. Get Stock Price (S)
    S = get_validated_input("Enter Current Stock Price (S): $", "Stock Price", min_value=0.01)
    if S is None: return

    # 2. Get Strike Price (K)
    K = get_validated_input("Enter Option Strike Price (K): $", "Strike Price", min_value=0.01)
    if K is None: return

    # 3. Get Time to Expiration (T) - Must be positive
    T = get_validated_input("Enter Time to Expiration (T) in years (e.g., 0.5 for 6 months): ", "Time to Expiration", min_value=0.01)
    if T is None: return

    # 4. Get Risk-Free Rate (r) - Input as percentage, stored as decimal
    r = get_validated_input("Enter Risk-Free Rate (r) in % (e.g., 5.0 for 5%): ", "Risk-Free Rate", is_percent=True)
    if r is None: return

    # 5. Get Volatility (sigma) - Input as percentage, must be positive
    sigma = get_validated_input("Enter Volatility (sigma) in % (e.g., 25.0 for 25%): ", "Volatility", min_value=0.01, is_percent=True)
    if sigma is None: return

    print("-" * 60)
    print("... Performing Calculations ...")
    
    try:
        call_price = black_scholes_call_price(S, K, T, r, sigma)
        put_price = black_scholes_put_price(S, K, T, r, sigma, call_price)
        call_delta, put_delta = calculate_delta(S, K, T, r, sigma)

        # --- Output: Target Product + Greeks ---
        print("\n" + "=" * 60)
        print(f"{'Black-Scholes Results':^60}")
        print("=" * 60)
        print(f"| {'Parameter':<25} | {'Value':<30} |")
        print("-" * 60)
        print(f"| {'Stock Price (S)':<25} | ${S:<29.2f} |")
        print(f"| {'Strike Price (K)':<25} | ${K:<29.2f} |")
        print(f"| {'Time (T) in Years':<25} | {T:<29.2f} |")
        print(f"| {'Risk-Free Rate (r)':<25} | {r*100:<29.2f}% |")
        print(f"| {'Volatility (sigma)':<25} | {sigma*100:<29.2f}% |")
        print("-" * 60)
        print(f"| {'European Call Price (C)':<25} | ${call_price:<29.2f} |")
        print(f"| {'European Put Price (P)':<25} | ${put_price:<29.2f} |")
        print("-" * 60)
        print(f"| {'Call Delta':<25} | {call_delta:<29.4f} |")
        print(f"| {'Put Delta':<25} | {put_delta:<29.4f} |")
        print("=" * 60)
        
        # --- Output: Reach Version ---
        generate_sensitivity_matrix(S, K, T, r, sigma, delta_percent=0.10)


    except Exception as e:
        print(f"\nAn error occurred during calculation: {e}")
        print("A common cause is Time (T) or Volatility (sigma) being invalid.")
        print("Please check your input values and ensure the 'scipy' library is installed.")
        

if __name__ == '__main__':
    # NOTE: Ensure 'scipy' is installed (pip install scipy)
    try:
        # Check for scipy dependency before starting
        import scipy.stats
        run_calculator()
    except ImportError:
        print("\nFATAL ERROR: The 'scipy' library is required but not installed.")
        print("Please install it using: pip install scipy")
    except Exception as e:
        print(f"\nFATAL ERROR: An unexpected error occurred: {e}")
        print("The program will now exit.")
        sys.exit(1)
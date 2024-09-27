import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def voltage_divider_3950(in_voltage: float, r_25_1: float, temp_1: float, r_25_2: float, temp_2: float, fixed_resistance: float) -> None:
    resistance_temp_1 = r_25_1
    
    # Calculate the voltage divider with r_25_1
    voltage_out_1 = in_voltage * (resistance_temp_1 / (resistance_temp_1 + fixed_resistance)) 
    
    resistance_temp_2 = r_25_2
    
    # Calculate the voltage divider with r_25_2
    voltage_out_2 = in_voltage * (resistance_temp_2 / (resistance_temp_2 + fixed_resistance))
    
    # Calculate the absolute difference between the two voltage dividers
    voltage_difference = abs(voltage_out_2 - voltage_out_1)
    
    # Print the values for r_25_1
    print(f'1. Resistance at {temp_1}°C: {resistance_temp_1} Ohms\n')
    print(f'The voltage divider output is {voltage_out_1} V with a fixed resistance of {fixed_resistance} Ohms\n')
    
    # Print the values for r_25_2
    print(f'2. Resistance at {temp_2}°C: {resistance_temp_2} Ohms\n')
    print(f'The voltage divider output is {voltage_out_2} V with a fixed resistance of {fixed_resistance} Ohms\n')
    
    # Print the voltage difference
    print(f'\nThe voltage difference between {temp_1}°C and {temp_2}°C is: {voltage_difference} V\n')

def find_optimal_fixed_resistance(res_temp_1: float, temp_1: float, res_temp_2: float, temp_2: float, step: float, limit: float) -> tuple:
    # Input voltage
    in_voltage = 3.3

    # Initialize fixed resistance
    fixed_res = step  # Ensure that it starts at a non-zero value

    # Arrays for storing fixed resistance values and voltage differences
    fixed_res_data = []
    voltage_diff_data = []

    prev_diff_voltage = 0

    # Loop through fixed resistance values up to the limit
    while fixed_res < limit:

        # Store current fixed resistance value
        fixed_res_data.append(fixed_res)

        # Calculate voltage divider for both temperatures
        voltage_out_1 = in_voltage * (res_temp_1 / (res_temp_1 + fixed_res))
        voltage_out_2 = in_voltage * (res_temp_2 / (res_temp_2 + fixed_res))

        # Calculate the absolute difference in voltage
        diff_voltage = abs(voltage_out_1 - voltage_out_2)

        # Stop if the change in voltage difference is below tolerance
        if abs(diff_voltage - prev_diff_voltage) < 1e-6:
            break

        prev_diff_voltage = diff_voltage

        # Add the voltage difference to the data
        voltage_diff_data.append(diff_voltage)

        # Increment the fixed resistance
        fixed_res += step

    return np.array(fixed_res_data), np.array(voltage_diff_data)

# Modified main function to call voltage_divider_3950 again with the optimal resistance
if __name__ == '__main__':
    
    """ The first function calculates the voltage difference with a specific fixed resistance, 
    while the second function searches for an ideal resistance that maximizes the voltage difference. 
    The first function is useful when using commercially available resistances. """
    
    print("Voltage Divider with Commercial Fixed Resistances: ")
    voltage_divider_3950(3.3, 19920, 10, 1261, 80, 1000)
    
    # Find the optimal resistance and voltage differences
    fixed_res, diff_voltage = find_optimal_fixed_resistance(19920, 10, 1261, 80, 1e+3, 1e+6)
    
    # Create a DataFrame to hold the results
    results_df = pd.DataFrame({
        'Fixed Resistance (Ohms)': fixed_res,
        'Voltage Difference (V)': diff_voltage
    })
    
    # Find the maximum voltage difference and corresponding resistance
    index_max = results_df['Voltage Difference (V)'].idxmax()
    optimal_resistance = results_df.iloc[index_max]['Fixed Resistance (Ohms)']
    
    # Print the row with the maximum voltage difference
    print("\nOptimal Fixed Resistance and Voltage Difference: ")
    print(results_df.iloc[index_max])
    
    # Call voltage_divider_3950 with the optimal fixed resistance found
    print("\nCalling voltage_divider_3950 with the optimal fixed resistance:")
    voltage_divider_3950(3.3, 19920, 10, 1261, 80, optimal_resistance)

    
    # Plot the voltage difference as a function of fixed resistance
    plt.plot(fixed_res, diff_voltage)
    plt.xlabel('Fixed Resistance (Ohms)')
    plt.ylabel('Voltage Difference (V)')
    plt.title('Voltage Difference vs Fixed Resistance')
    plt.grid(True)
    plt.show()
    
   


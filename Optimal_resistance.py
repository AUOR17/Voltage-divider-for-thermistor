import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calc_ntc_resistance(temp_celsius: float, r25: float, beta: float) -> float:
    """Calculate NTC resistance at a given temperature using the beta equation."""
    temp_kelvin = temp_celsius + 273.15
    return r25 * math.exp(beta * (1/temp_kelvin - 1/298.15))

def find_nearest_commercial(r_optimal: float) -> float:
    """Find the nearest commercial resistance value in E24 series."""
    e24 = [10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91]
    multipliers = [1, 10, 100, 1000, 10000, 100000]
    commercial_values = [e * m for m in multipliers for e in e24]
    return min(commercial_values, key=lambda x:abs(x-r_optimal))

def voltage_divider_analysis(in_voltage: float, r25: float, beta: float, temp_range: tuple, fixed_resistance: float) -> tuple:
    """Analyze voltage divider output across temperature range."""
    temps = np.linspace(temp_range[0], temp_range[1], 100)
    resistances = [calc_ntc_resistance(t, r25, beta) for t in temps]
    voltages = [in_voltage * (r / (r + fixed_resistance)) for r in resistances]
    
    min_voltage = min(voltages)
    max_voltage = max(voltages)
    voltage_range = max_voltage - min_voltage
    
    # Calculate average sensitivity (V/°C)
    sensitivity = voltage_range / (temp_range[1] - temp_range[0])
    
    return temps, voltages, sensitivity, voltage_range

def find_optimal_fixed_resistance(r25: float, beta: float, temp_range: tuple, 
                                in_voltage: float=3.3, step: float=1, limit: float=1e5) -> tuple:
    """Find optimal fixed resistance that maximizes both range and sensitivity."""
    fixed_res = step
    best_score = 0
    optimal_res = step
    
    results = []
    
    while fixed_res < limit:
        _, voltages, sensitivity, v_range = voltage_divider_analysis(
            in_voltage, r25, beta, temp_range, fixed_res)
        
        # Score based on voltage range utilization and sensitivity
        range_score = v_range / in_voltage  # How much of 3.3V we're using
        
        # Penalize if we're getting close to rails
        if min(voltages) < 0.1 or max(voltages) > (in_voltage - 0.1):
            score = 0
        else:
            score = range_score * sensitivity
            
        results.append({
            'resistance': fixed_res,
            'range': v_range,
            'sensitivity': sensitivity,
            'score': score
        })
        
        if score > best_score:
            best_score = score
            optimal_res = fixed_res
            
        fixed_res += step
        
    return optimal_res, pd.DataFrame(results)

def plot_analysis(temps, voltages, fixed_res, title):
    """Plot voltage vs temperature curve."""
    plt.figure(figsize=(10, 6))
    plt.plot(temps, voltages)
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Output Voltage (V)')
    plt.title(f'{title} (R_fixed = {fixed_res:.0f}Ω)')
    plt.grid(True)
    plt.show()
    

if __name__ == '__main__':
    # Parameters for both thermistors
    R25_A = 10000  # Thermistor A
    BETA_A = 3492
    R25_B = 10233  # Thermistor B (ejemplo)
    BETA_B = 3435
    TEMP_RANGE = (0, 300)
    VIN = 3.3

    # Find optimal resistances for both thermistors
    optimal_res_A, results_df_A = find_optimal_fixed_resistance(R25_A, BETA_A, TEMP_RANGE)
    optimal_res_B, results_df_B = find_optimal_fixed_resistance(R25_B, BETA_B, TEMP_RANGE)
    
    # Find commercial resistances
    commercial_res_A = find_nearest_commercial(optimal_res_A)
    commercial_res_B = find_nearest_commercial(optimal_res_B)
    
    # Analysis of thermistor A with its optimal resistance
    print("\nBehavior of Thermistor A (current thermistor):")
    print(f"Temperature Range: {TEMP_RANGE[0]}°C to {TEMP_RANGE[1]}°C")
    temps_A, voltages_A, sensitivity_A, v_range_A = voltage_divider_analysis(
        VIN, R25_A, BETA_A, TEMP_RANGE, optimal_res_A)
    print(f"Optimal theoretical resistance: {optimal_res_A:.0f}Ω")
    print(f"Nearest commercial resistance: {commercial_res_A}Ω")
    print(f"Voltage range: {v_range_A:.3f}V")
    print(f"Average sensitivity: {sensitivity_A*1000:.2f}mV/°C")
    
    # Analysis of thermistor B with its optimal resistance
    print("\nBehavior of Thermistor B (EPW proposal):")
    print(f"Temperature Range: {TEMP_RANGE[0]}°C to {TEMP_RANGE[1]}°C")
    temps_B, voltages_B, sensitivity_B, v_range_B = voltage_divider_analysis(
        VIN, R25_B, BETA_B, TEMP_RANGE, optimal_res_B)
    print(f"Optimal theoretical resistance: {optimal_res_B:.0f}Ω")
    print(f"Nearest commercial resistance: {commercial_res_B}Ω")
    print(f"Voltage range: {v_range_B:.3f}V")
    print(f"Average sensitivity: {sensitivity_B*1000:.2f}mV/°C")
    
    # Analysis of thermistor B with resistance from A
    print(f"\nBehavior of Thermistor B (EPW proposal) with R_A (current resistance) = {commercial_res_A:.0f}Ω:")
    print(f"Temperature Range: {TEMP_RANGE[0]}°C to {TEMP_RANGE[1]}°C")
    temps_B_withRA, voltages_B_withRA, sensitivity_B_withRA, v_range_B_withRA = voltage_divider_analysis(
        VIN, R25_B, BETA_B, TEMP_RANGE, commercial_res_A)
    print(f"Voltage range: {v_range_B_withRA:.3f}V")
    print(f"Average sensitivity: {sensitivity_B_withRA*1000:.2f}mV/°C")
    
    # Analysis of thermistor A with resistance from B
    print(f"\nBehavior of Thermistor A (current thermistor) with R_B (EPW proposal) = {commercial_res_B:.0f}Ω:")
    print(f"Temperature Range: {TEMP_RANGE[0]}°C to {TEMP_RANGE[1]}°C")
    temps_A_withRB, voltages_A_withRB, sensitivity_A_withRB, v_range_A_withRB = voltage_divider_analysis(
        VIN, R25_A, BETA_A, TEMP_RANGE, commercial_res_B)
    print(f"Voltage range: {v_range_A_withRB:.3f}V")
    print(f"Average sensitivity: {sensitivity_A_withRB*1000:.2f}mV/°C")
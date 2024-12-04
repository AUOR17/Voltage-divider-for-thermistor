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
    # Example parameters
    R25 = 10233  # 10kΩ at 25°C
    BETA = 3425  # Beta coefficient
    TEMP_RANGE = (0, 300)  # Temperature range in °C
    VIN = 3.3  # Input voltage
    
    # Find optimal resistance
    optimal_res, results_df = find_optimal_fixed_resistance(R25, BETA, TEMP_RANGE)
    commercial_res = find_nearest_commercial(optimal_res)
    
    # Analyze with optimal resistance
    temps, voltages, sensitivity, v_range = voltage_divider_analysis(
        VIN, R25, BETA, TEMP_RANGE, optimal_res)
    
    print(f"\nOptimal theoretical resistance: {optimal_res:.0f}Ω")
    print(f"Nearest commercial resistance: {commercial_res}Ω")
    print(f"Voltage range: {v_range:.3f}V")
    print(f"Average sensitivity: {sensitivity*1000:.2f}mV/°C")
    
    # Plot results
    plot_analysis(temps, voltages, optimal_res, "Voltage Divider Response with Optimal Resistance")
    
    # Also analyze with commercial resistance
    temps, voltages, sensitivity, v_range = voltage_divider_analysis(
        VIN, R25, BETA, TEMP_RANGE, commercial_res)
    plot_analysis(temps, voltages, commercial_res, "Voltage Divider Response with Commercial Resistance")
    
    # Plot optimization results
    plt.figure(figsize=(10, 6))
    plt.plot(results_df['resistance'], results_df['score'])
    plt.xlabel('Fixed Resistance (Ω)')
    plt.ylabel('Optimization Score')
    plt.title('Optimization Score vs Fixed Resistance')
    plt.grid(True)
    plt.show()
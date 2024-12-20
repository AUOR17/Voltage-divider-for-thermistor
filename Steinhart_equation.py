import math
import pandas as pd

def calculate_steinhart_hart(start_res, end_res, step, a, b, c, fixed_resistance, voltage):
    
    # emular voltaje de salida. 
    """
    Calcula la ecuación de Steinhart-Hart para un rango de valores de resistencias.
    
    Parámetros:
    - start_res: Valor inicial de resistencia en ohmios.
    - end_res: Valor final de resistencia en ohmios.
    - step: Incremento en el valor de resistencia.
    - a, b, c: Coeficientes de Steinhart-Hart específicos del termistor.
    
    Retorna:
    - Un DataFrame de pandas con las columnas 'Resistencia' y 'Temperatura'.
    """
    data = []
    resistance = start_res
    
    while resistance <= end_res:
        ln_r = math.log(resistance)
        inv_t = a + (b * ln_r) + (c * ln_r**3)
        temperature_kelvin = 1 / inv_t
        temperature_celsius = temperature_kelvin - 273.15
        
        data.append({'Resistencia': resistance, 'Temperatura': temperature_celsius})
        
        resistance += step
    
    df = pd.DataFrame(data)
    return df

# Ejemplo de uso
start_resistance = 1261
end_resistance = 19920
step_resistance = 5
a = 1.113232463e-3
b = 2.367687547e-4
c = 0.7687201539e-7
fixed_resistance = 5100
voltage = 3.3
Sensor_name = "SCF50"

result_df = calculate_steinhart_hart(start_resistance, end_resistance, step_resistance, a, b, c, fixed_resistance, voltage)
result_df.to_csv(Sensor_name + ".csv", index=True)
print(result_df.head())
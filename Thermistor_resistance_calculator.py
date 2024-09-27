import math
import numpy as np
import pandas as pd

def voltage_divisor_altern_3950(in_voltage, r_25_1,temperatura_1, r_25_2, temperatura_2, resistencia_fija):
    resistencia_temper_1 = r_25_1
    
    #se calcula el divisor de voltaje con el valor de r_25_1
    voltage_divisor_out_1 = in_voltage * (resistencia_temper_1/ (resistencia_temper_1+resistencia_fija)) 
    resistencia_temper_2 = r_25_2
    
    #se calcula el divisor de voltaje con el valor de r_25_2
    voltage_divisor_out_2 = in_voltage * (resistencia_temper_2/ (resistencia_temper_2+resistencia_fija))
    
    #Se calcula la diferencia de voltaje entre ambos divisores, entre mas diferencia halla mejor sera la precision del termistor
    voltage_var = voltage_divisor_out_2 - voltage_divisor_out_1 
    
    #Se imprimen los valores de r_25_1
    print(f'1. Una resistencia de temperatura a {temperatura_1}°C con valor {resistencia_temper_1}\n')
    print(f'El divisor de voltaje es de {voltage_divisor_out_1} V \nTiene una resistencia fija de {resistencia_fija} \n')
    
    #Se imprimen los valores de r_25_2
    print(f'2. Una resistencia de temperatura a {temperatura_2}°C con valor {resistencia_temper_2}\n')
    print(f'El divisor de voltaje es de {voltage_divisor_out_2} V \nTiene una resistencia fija de {resistencia_fija} \n')
    
    
    #Se imprime la diferencia de voltaje
    print(f'\nLa diferencia de voltaje es de : {voltage_var} V entre {temperatura_1}°C y {temperatura_2}°C del termistor\n')
    
def find_fix_resistance(res_temp_1,temp_1,res_temp_2,temp_2,aum,lim):
    
    #voltaje de entrada
    in_voltage = 3.3
    
    #se inicializa la resistencia
    fix_res = 0
    
    #Se crea un array para los valores de la resistencia
    data_fix_res = []
    
    #Se crea un array para los valores de la diferencia de voltaje
    data_diff_voltage = []
    
    #Comienza el ciclo de asignar los valores de la resistencia y seguira hasta que los valores sean iguales o mayores a lim
    while fix_res < lim:
        
        #se agrega el valor de la resistencia fija al array
        data_fix_res.append(fix_res)
        
        #se calcula el divisor de voltaje de acuerdo a las resistencias del termistor a ciertas temperaturas
        voltage_divisor_out_1 = in_voltage * (res_temp_1 / (res_temp_1 + fix_res))
        voltage_divisor_out_2 = in_voltage * (res_temp_2 / (res_temp_2 + fix_res))
        
        #se calcula la diferencia de voltaje
        diff_voltage = voltage_divisor_out_1 - voltage_divisor_out_2
        
        #se aumenta el valor de la resitencia fija de acuerdo al parametro que se coloca
        fix_res += aum
        
        #se agrega el valor de la diferencia de voltaje al array
        data_diff_voltage.append(diff_voltage)
        
    #regresa ambos arrays
    return data_fix_res, data_diff_voltage

if __name__ == '__main__':
    
    """ La diferencia entre la primera y la segunda funcion radica que la segunda busca una resistencia ideal, 
    pero esta resistencia no necesariamente existe, por ello la primera funcion busca la diferencia de voltaje con una resistencia
    especifica y asi se puede usar con las resistencias que existen o son comerciales

    """
    
    print("Divisor de voltaje y resistencias comerciales: ")
    voltage_divisor_altern_3950(3.3, 19920, 10,1261,80,1000)
    
    #se convierte el a un numpy array
    fix_res = np.array(find_fix_resistance(19920, 10,1261,80,10e+3,1e+6))

    #se aplica la transpuesta para que las columnas sean la que tiene el mayor numero de registros
    fix_res = np.transpose(fix_res)

    #se crea un DataFrame y se le asigna el nombte de las columnas
    diff_voltage = pd.DataFrame(fix_res,columns = ['Fix Resistance','Voltage Difference'])

    #se busca el renglon donde la diferencia de voltaje sea la mayor 
    index_max = diff_voltage.index[diff_voltage['Voltage Difference']==diff_voltage['Voltage Difference'].max()].tolist()

    #se imprime el renglon que se ha encontrado
    print("Resistencia ideal y diferencia de voltaje: ")
    print(diff_voltage.iloc[index_max])
    
 

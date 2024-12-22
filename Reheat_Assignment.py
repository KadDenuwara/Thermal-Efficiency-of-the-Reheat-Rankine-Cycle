import pyromat as pm
import numpy as np
import pandas as pd


# Define steam properties using pyromat
steam = pm.get('mp.H2O')

# Function to convert temperature from Celsius to Kelvin
def Kelivin_convertor(temperature):
    return temperature + 273.15

# Function to convert pressure from bar to Pa
def Pressure_convertor(pressure):
    return pressure / 100

class Reheat_Rankine_Cycle():

#   (1 Reservoir) --> |Feed water pump| --> (2) --> |Boiler| --> (3) ----->
#         ^                                                               |   
#         |                                                               v
#    |Condenser| <-- (6) <-- |Turbine|<-- (5) <--  |Reheat|<-- (4) <-- |Turbine|


    def Thermal_Efficiency(Reheat_pressure):
        
        'State 01'
        p1 = Pressure_convertor(10)  # Convert pressure from bar to Pa
        T1 = steam.Ts(p1) # Calculate temperature at p1
        h_1 = steam.hs(T=T1) # Calculate enthalpy at T1
        h1 = h_1[0][0]
        v1 = steam.v(T1)[0] # Calculate specific volume at T1

        'State 02'
        p2 = Pressure_convertor(15*1000)
        w_pump_in = v1*(p2 - p1)*100  # Calculate work done by pump
        h2 = h1 + w_pump_in  # Calculate enthalpy at p2

        'State 03'
        p3 = p2
        T3 = Kelivin_convertor(500)
        h_3 = steam.h(T = T3, p = p3) # Calculate enthalpy at T3 and p3
        h3 = h_3[0]
        s_3 = steam.s(T = T3, p = p3) # Calculate entropy at T3 and p3
        s3 = s_3[0]

        'State 04'
        p4 = Pressure_convertor(Reheat_pressure)
        s4 = s3
        s_f_4, s_g_4 = steam.ss(p = p4) # Calculate saturation enthalpy and entropy at p4
        s_f4, s_g4 = s_f_4[0], s_g_4[0]
        s_fg4 = s_g4 - s_f4 # Calculate entropy difference
        x4 = (s4 - s_f4)/s_fg4 # Calculate quality factor
        h_f_4, h_g_4 = steam.hs(p = p4)   # Calculate enthalpy at p4
        h_f4, h_g4 = h_f_4[0], h_g_4[0]
        h_fg4 = h_g4 - h_f4 # Calculate enthalpy difference
        h4 = h_f4 + x4 * h_fg4 # Calculate enthalpy at p4

        'State 05'
        p5 = p4
        T5 = Kelivin_convertor(500)
        h_5 = steam.h(T= T5, p = p5) # Calculate enthalpy at T5 and p5
        h5 = h_5[0]
        s_5 = steam.s(T= T5, p = p5) # Calculate entropy at T5 and p5
        s5 = s_5[0]

        'State 06'
        p6 = p1
        s6 = s5
        s_f_6, s_g_6 = steam.ss(p = p6) # Calculate saturation enthalpy and entropy at p6
        s_f6, s_g6 = s_f_6[0], s_g_6[0]
        s_fg6 = s_g6 - s_f6 # Calculate entropy difference
        x6 = (s6 - s_f6)/s_fg6
        h_f_6, h_g_6 = steam.hs(p = p6)
        h_f6, h_g6 = h_f_6[0], h_g_6[0]
        h_fg6 = h_g6 - h_f6
        h6 = h_f6 + x6 * h_fg6 # Calculate enthalpy at p6

        'Thermal Efficiency'
        q_in = (h3 - h2) + (h5 - h4) # Calculate net heat input
        q_out = h6 - h1 # Calculate net heat output
        w_net = q_in - q_out # Calculate net work
        n_th = w_net / q_in # Calculate thermal efficiency

        return n_th
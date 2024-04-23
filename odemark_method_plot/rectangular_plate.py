# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 15:25:49 2023

Use Boussinesq solution, uniform rectangular load method. 
This case considers the sensor is under one of eight wheels,all eight wheels are taken into account.

@author: jzhang33
"""


from scipy.integrate import dblquad
import math

# here consider 8 tyres case:
def integrand_2(y, x, z):
    #return z**3/((x)**2+(y)**2+z**2)**2.5
    return z**3/((0.92-x)**2+(1.11-y)**2+z**2)**2.5*4 + z**3/((2.62-x)**2+(1.11-y)**2+z**2)**2.5*4 
    # return z**3/(x**2+(0.87-y)**2+z**2)**2.5*2 + z**3/((0.85-x)**2+(0.87-y)**2+z**2)**2.5*4*0.5
# here x is the width of the tyre, and y is the length.
def compute_sigma_rectangular_plate(z_values, x,y,p):
    x_lower = x[0]
    x_upper = x[1]
    y_lower = lambda x: y[0]
    y_upper = lambda x: y[1]

    integral_results_2 = []
    
    for z in z_values:
        integral_result_2, _ = dblquad(integrand_2, x_lower, x_upper, y_lower, y_upper, args=(z,))
        integral_results_2.append(integral_result_2)
    sigma_z2_list = []
    

    for num in integral_results_2:
        sigma_z2 = 3*p/(2*math.pi)*num
        sigma_z2_list.append(sigma_z2)
    
    return sigma_z2_list

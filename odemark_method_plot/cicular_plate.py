# -*- coding: utf-8 -*-
"""

Use Boussinesq solution, uniform circular load method. 

Created on Thu Oct 19 15:22:19 2023

@author: jzhang33
"""

from scipy.integrate import dblquad
import math


# define function integrated:
def integrand_1(theta, r, z):
    return z**3*r/((1.44**2+r**2+z**2-2*1.44*r*math.cos(theta))**2.5)*4+z**3*r/(2.85**2+r**2+z**2-2*2.85*r*math.cos(theta))**2.5*4
def compute_sigma_circular_plate(z_values, theta,r,p):
    # define intergral range:
    # parameter r here is the raidus of plate
    theta_lower = theta[0]
    theta_upper = theta[1]
    r_lower = r[0]
    r_upper = r[1]
    
    
    # Initialise the list that stores the result of the integral
    integral_results_1 = []
    
    # Execute integral and record the results, 
    for z in z_values:
        integral_result_1, _ = dblquad(integrand_1, r_lower, r_upper,theta_lower, theta_upper,  args=(z,))
        integral_results_1.append(integral_result_1)
    sigma_z1_list = []
    
    # result is multiplied by the coefficient in Boussinesq solution
    # p_1 is distributed load

    for num in integral_results_1:
        sigma_z1 = 3*p/(2*math.pi)*num
        sigma_z1_list.append(sigma_z1)
    
    return sigma_z1_list
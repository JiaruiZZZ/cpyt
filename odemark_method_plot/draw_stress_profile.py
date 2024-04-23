# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 17:07:35 2023

@author: jzhang33
"""

#this program is used to use Odemark's method to calculate vertical stress under plate load
import numpy as np
import matplotlib.pyplot as plt
import math
from cicular_plate import compute_sigma_circular_plate
from rectangular_plate import compute_sigma_rectangular_plate

#%%
# use odemark's method, calculate equivalent thickness of upper layers: you can change thickness and modulus here
h1 = 0.1*(2000/4)**(1/3)
h2 = 0.8*1.4*(100/4)**(1/3)
h3 = 0.5


def calculate_z_target(z_values):
    z_target = np.zeros_like(z_values)  # Initialize with zeros

    # Define the piecewise conditions
    condition1 = (z_values >= 0) & (z_values < 0.1)
    condition2 = (z_values >= 0.1) & (z_values < 1.5)
    condition3 = (z_values >= 1.5) &(z_values < 1.9)
    condition4 = z_values >= 1.9

    # Calculate z_target based on conditions
    z_target[condition1] = (h1 / 0.1) * z_values[condition1]
    z_target[condition2] = h1 + (h2 / 1.4) * (z_values-0.1)[condition2]
    z_target[condition3] = h1 + h2  + (h3 / 0.5)* (z_values- 1.4 - 0.1)[condition3]
    z_target[condition4] = h1 + h2 + h3  + (z_values- 0.5 - 1.4 - 0.1)[condition4]#本层等效的厚度/原厚度*（深度-本层上部基准值）
    # condition1 = (z_values >= 0) & (z_values < 1.2)
    # condition2 = (z_values >= 1.2) & (z_values < 1.5)
    # condition3 = (z_values >= 1.5) & (z_values < 2.8)
    # condition4 = (z_values >= 2.8) & (z_values < 4.0)
    # condition5 = (z_values >= 2.8) & (z_values < 4.0)
    # condition6 = z_values >= 4
    return z_target
# euqivalent thickness of upper layer plus the depth of target sensor from soil interface:
z_values = np.linspace(0, 15, 1000) 
z_target = calculate_z_target(z_values)
print(type(z_values))
# find the index of the value at the target depth in Boussinesq solution:
z_indices = []
for target in z_target:
    index = np.argmin(np.abs(z_values - target))
    z_indices.append(index)
# Convert the list of indices to a numpy array
z_indices = np.array(z_indices, dtype=int)
# get the value of the sigma z at the certain index
# you can change the upper and lower limits of intergral here in the function, r is the radius of plate, p is distributed load
#sigma_z_list = compute_sigma_rectangular_plate(z_values,x=[-4.925,4.925],y=[-1.26,1.26],p=39)
sigma_z_list = compute_sigma_circular_plate(z_values,theta=[0,2*math.pi],r=[0,0.14],p=792)
# TODO: if you want to calculate rectangular case, change the function to below one and input x,y,p. x,y is the width and length of the plate.
# sigma_z_list = compute_sigma_rectangular_plate(z_values,x,y,p)
sigma_z_Odemark = []
for i in z_indices:    
    sigma_z_Odemark.append(sigma_z_list[i])

#%%
# load spread model
tan_angle_sand = 0.5*(3+0.0565*(2000/100-1))  #E asphalt / E sand

print(tan_angle_sand)

tan_angle_peat = 0.5*(3+0.0565*(100/4-1)) #E sand /E clay&peat

print(tan_angle_peat)


def piecewise_function(z3):
    if 0.1> z3 > 0:
        return 792*(0.062/((0.14+z3*0.79)**2*math.pi))*8
    elif 1.5>= z3 >= 0.1:
        return 325.89*(0.15/((0.219 + (z3-0.1)*tan_angle_sand)**2*math.pi))*8
    elif z3 > 1.5:
        return 1.65*(13.02/((2.036 + (z3-1.5)*tan_angle_peat)**2*math.pi))*8


# generater z3 values:
z3_values = np.linspace(0,15,1000)
function_values3 = [piecewise_function(z3) if z3 > 0.1 else np.nan for z3 in z3_values]


#%%  
# plot the result point at certain depth and compare with the measurement   

plt.plot(function_values3,z3_values, label='Load spread model')
plt.xlim((0,30))
plt.ylim(0,5)
plt.gca().invert_yaxis()

plt.scatter([3.8,3.2,3.2,2.8], [3,4,3,3], color='purple', label='Measurements of PWP gauge')
plt.plot(sigma_z_list,z_values, label='Boussinesq method' )
plt.plot(sigma_z_Odemark,z_values, color='red', label='Odemark\'s method')
#plt.plot([0.628,2.77,5.34,6.23,5.27,4.58,4.28,3.5], [0.14,0.6,1.17,1.54,2.81,3.76,4.35,5.19],'g-o',label = 'simulation result')
plt.plot([-2.845,-3.518,-0.644,0.966,3.855,3.797,3.439,3.171,3.038,2.5], [0,0.09,0.15,0.90,1.79,1.93,2.96,3.99,4.59,6],'g',label = 'FEM result')
# line=plt.plot([4.45,4.80,5.09,5.39,5.64,6.11,7.09,9,23.9,112],[4.9,4.07,3.54,2.838,2.46,2.01,1.469,1.27,0.61,0.27],'g-o',label='simulation result')


plt.xlabel('stress, $\sigma$ (kPa)')
plt.ylabel('depth,z(m,NAP)')
plt.grid(True)
plt.legend()
plt.show()


target_depth = 2.75
index_at_target_depth = np.argmin(np.abs(z_values - target_depth))

# Get the value of sigma_z_Odemark at the specified index
sigma_z_at_target_depth = sigma_z_Odemark[index_at_target_depth]

# Output the result
print(f"sigma_z_Odemark at z_values = {target_depth}: {sigma_z_at_target_depth}")
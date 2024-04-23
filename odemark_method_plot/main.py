# -*- coding: utf-8 -*-
"""
Main file
Created on Mon Oct 16 11:41:51 

@author: jzhang33
"""
#this program is used to use Odemark's method to calculate vertical stress under plate load
import numpy as np
import matplotlib.pyplot as plt
import math
from cicular_plate import compute_sigma_circular_plate
from rectangular_plate import compute_sigma_rectangular_plate

#%%
def function1():
    # use odemark's method, calculate equivalent thickness of upper layers: you can change thickness and modulus here
    h1 = 0.1*(4160/4)**(1/3)
    h2 = 0.8*1.4*(249/4)**(1/3)
    h3 = 0.5
    # euqivalent thickness of upper layer plus the depth of target sensor from soil interface:
    z_target =  h1 + h2 + h3 + 1
    print(z_target)
    # z_target =  h1 +h2 + h3 + (h4/1.2)*1.15
    # z_target =  h1 +h2 + h3 + h4 + 0.93
    z_values = np.linspace(0, 15, 1000) 
    # find the index of the value at the target depth in Boussinesq solution:
    z_index = np.argmin(np.abs(z_values - z_target))
    # get the value of the sigma z at the certain index
    # you can change the upper and lower limits of intergral here in the function, r is the radius of plate, p is distributed load
    sigma_z_list = compute_sigma_circular_plate(z_values,theta=[0,2*math.pi],r=[0,0.14],p=792)
    # TODO: if you want to calculate rectangular case, change the function to below one and input x,y,p. x,y is the width and length of the plate.
    #sigma_z_list = compute_sigma_rectangular_plate(z_values,x=[-0.14,0.14],y=[-0.14,0.14],p=792)
    sigma_z_Odemark = sigma_z_list[z_index]
    return sigma_z_Odemark


if __name__ == "__main__":
    sigma_z_Odemark = function1()
print(sigma_z_Odemark)
    # plot the result point at certain depth and compare with the measurement   
plt.xlim((0,50))
plt.ylim([0,5])
plt.gca().invert_yaxis()
plt.scatter([3.8,3.2,3.2,2.8], [3,4,3,3], color='purple', label='measurements of PWP gauge')
plt.scatter([sigma_z_Odemark],[3], color='red', label='Odemark\'s method')
plt.title('comparation of Odemark method and measurement')
plt.xlabel('stress, $\sigma$ (kPa)')
plt.ylabel('depth,z(m)')
plt.grid(True)
plt.legend()
plt.show()
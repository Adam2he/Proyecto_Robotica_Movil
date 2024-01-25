
import math
import random
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

import copy

def calcula_distancia(posicion,goal):
    return math.sqrt((posicion[0]-goal[0])**2+(posicion[1]-goal[1])**2+(posicion[2]-goal[2])**2)

def planificador(posicion,goal,m,F,N):
    steps=[copy.deepcopy(posicion)]
    convergence=True
    max_iter=10*N
    iter = 0
    while (calcula_distancia(posicion,goal) > m and convergence and iter<max_iter):

        p_posicion_0 = posicion[0] + F[round(posicion[0])][round(posicion[1])][round(posicion[2])][0]
        p_posicion_1 = posicion[1] + F[round(posicion[0])][round(posicion[1])][round(posicion[2])][1]
        p_posicion_2 = posicion[2] + F[round(posicion[0])][round(posicion[1])][round(posicion[2])][2]
        if (round(p_posicion_0) >= 0 and round(p_posicion_0) < N):
            posicion[0] = p_posicion_0
        if (round(p_posicion_1) >= 0 and round(p_posicion_1) < N):
            posicion[1] = p_posicion_1
        if (round(p_posicion_2) >= 0 and round(p_posicion_2) < N):
            posicion[2] = p_posicion_2
    
        if (posicion==steps[-1]):
            convergence = False
        else:
            steps.append(copy.deepcopy(posicion))
        iter+=1
    if iter >= max_iter:
        convergence = False
    #print("numero de iteraciones: ", iter)
    return steps,convergence

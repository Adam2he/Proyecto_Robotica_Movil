import math
import random
from tqdm import tqdm

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

def inicializa_F(N):
    # Crear una matriz tridimensional de NxNxN
    F = np.empty((N, N, N), dtype=object)

    # Crear un vector con 3 componentes
    vector = np.array([0, 0, 0])

    # Rellenar cada valor de la matriz con el vector
    for i in range(N):
        for j in range(N):
            for k in range(N):
                F[i, j, k] = vector
    return F


def gotogoal(goal,F,N,m_goal):
    #for i in tqdm(range(N),desc='Creando Goal'):
    for i in range(N):
        for j in range(N):
            for k in range(N):
                distancia=math.sqrt((goal[0]-i)**2+(goal[1]-j)**2+(goal[2]-k)**2)
                try:
                    F[i][j][k]= F[i][j][k]+m_goal*np.array([goal[0]-i,goal[1]-j,goal[2]-k])/distancia
                except ZeroDivisionError or RuntimeWarning:
                    a="hola"


def avoidobstacle(obstacle,F,N,R_soi):
    #pbar = tqdm(total=100, desc='Creando obstáculo', colour='green')
    for i in np.linspace(obstacle[0]-R_soi,obstacle[0]+R_soi,2*R_soi+1):
        i=int(i)
        #pbar.update(int(((i-(obstacle[0]-R_soi))*100) / (2*R_soi)))
        for j in np.linspace(obstacle[1]-R_soi,obstacle[1]+R_soi,2*R_soi+1):
            j=int(j)
            for k in np.linspace(obstacle[2]-R_soi,obstacle[2]+R_soi,2*R_soi+1):
                k=int(k)
                distancia=math.sqrt((obstacle[0]-i)**2+(obstacle[1]-j)**2+(obstacle[2]-k)**2)
                if distancia <= R_soi and i<N and j<N and k<N:
                    try:
                        F[i][j][k] = F[i][j][k] + ((R_soi-distancia)/distancia)*np.array([i-obstacle[0],j-obstacle[1],k-obstacle[2]])/distancia
                    except ZeroDivisionError:
                        a="hola"




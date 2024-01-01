import math
import random
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata








def calcula_distancia(posicion,goal):
    return math.sqrt((posicion[0]-goal[0])**2+(posicion[1]-goal[1])**2+(posicion[2]-goal[2])**2)

def planificador(posicion,goal,m,F):
    datos=[]
    while calcula_distancia(posicion,goal) > m:
        posicion[0] = posicion[0] + F[round(posicion[0])][round(posicion[1])][round(posicion[2])][0]
        posicion[1] = posicion[1] + F[round(posicion[0])][round(posicion[1])][round(posicion[2])][1]
        posicion[2] = posicion[2] + F[round(posicion[0])][round(posicion[1])][round(posicion[2])][2]
        datos+=posicion
    return datos

def planificador_con_representacion(posicion,goal,m,F,obstacle):
    # Crear una figura 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(goal[0], goal[1], goal[2], color='g', s=100)
    for i in range(len(obstacle)):
        ax.scatter(obstacle[i][0], obstacle[i][1], obstacle[i][2], color='r', s=100)

    # Mostrar el gráfico
    datos=[]
    while calcula_distancia(posicion,goal) > m:
        posicion[0] = posicion[0] + F[round(posicion[0])][round(posicion[1])][round(posicion[2])][0]
        posicion[1] = posicion[1] + F[round(posicion[0])][round(posicion[1])][round(posicion[2])][1]
        posicion[2] = posicion[2] + F[round(posicion[0])][round(posicion[1])][round(posicion[2])][2]
        # Dibujar el punto
        ax.scatter(posicion[0], posicion[1], posicion[2], color='b', s=1)  # 's' es el tamaño del punto
        datos+=posicion
        plt.draw()
        plt.pause(0.01)
    plt.show()
    return datos




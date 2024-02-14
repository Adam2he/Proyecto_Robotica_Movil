import numpy

from representaciones import *
from calculo_puntos import *
from funciones_mapas import *
from planificador import *


from numpy import *
import math
import random
from tqdm import tqdm
import json


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
from mpl_toolkits.mplot3d import Axes3D

m_goal=1 #Constante para el goal
N=50 #Tamaño del mapa
goal=[20,15,25] #Destino
R_soi=5 #Esfera de influencia del obstáculo
M=40 #Número de obstáculos
guardar_mapa=False #False o True
cargar_mapa=False #False o True

inicio=[0,0,0]
posicion=inicio
m=2 #Margen de error respecto al goal

obstacle=[]
for i in range(M):
    obstacle+=[[random.randint(0,N),random.randint(0,N),random.randint(0,N)]]


if __name__ == '__main__':
    if cargar_mapa==False:
        M=len(obstacle)
        F=inicializa_F(N)
        gotogoal(goal,F,N,m_goal)
        for i in range(M):
            avoidobstacle(obstacle[i],F,N,R_soi)
        #representar3d_puntos(N,F,M,goal,obstacle,R_soi)
        #representar2d_movimiento(N,M,goal,obstacle,R_soi,F)

        if guardar_mapa==True:
            guarda_mapa(F)
            guarda_variables(m_goal,N,goal,R_soi,M,inicio,obstacle)


    else:
        F=carga_mapa()
        m_goal, N, goal, R_soi, M, inicio, obstacle=carga_variables()
        print(m_goal)



    ##############################
    conc=[]
    N=10
    M=0
    R_soi=5
    k=0
    T4=0
    while N<31:
        M=1
        while M<N/2:
            obstacle = []
            posicion = [0, 0, 0]
            for i in range(M):
                obstacle += [[random.randint(0, N), random.randint(0, N), random.randint(0, N)]]
            goal = [N, N, N]
            F = inicializa_F(N)
            gotogoal(goal, F, N, m_goal)
            for i in range(M):
                avoidobstacle(obstacle[i], F, N, R_soi)
            T1 = time.time()
            dato = planificador2(posicion, goal, m, F, N)
            T2 = time.time()
            T3 = T2 - T1
            if dato == True:
                conc += [[M, N, T3]]
                print(conc)
                M += 1

        N+=1

    x = []
    y = []
    z = []
    datos=conc
    for i in range(len(datos)):
        x += [datos[i][0]]
        y += [datos[i][1]]
        z += [datos[i][2]]

    # Construir la matriz A y el vector b
    A = np.column_stack((x, y, np.ones_like(x)))
    b = z

    # Calcular mínimos cuadrados
    resultados = np.linalg.lstsq(A, b, rcond=None)
    a, b, c = resultados[0]

    # Imprimir los coeficientes
    print("El coeficiente a es:", a)
    print("El coeficiente b es:", b)
    print("El coeficiente c es:", c)


    # Crear una figura 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


    # Dibujar el punto
    med=np.mean(z)
    for i in range(len(datos)):
        if z[i]>med:
            color='r'
        else:
            color='g'
        ax.scatter(x[i], y[i], z[i], color=color, s=50)  # s es el tamaño del punto

    # Configurar etiquetas de los ejes
    ax.set_xlabel('Número de obstáculos')
    ax.set_ylabel('Tamaño del mapa')
    ax.set_zlabel('')

    # Mostrar la figura
    plt.show()








    #datos=planificador_con_representacion(posicion,goal,m,F,obstacle)
    #representar3d_puntos(N, F, M, goal, obstacle, R_soi)
    #mapa_y_camino(datos,goal,obstacle)














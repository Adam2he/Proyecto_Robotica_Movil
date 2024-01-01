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

m_goal=1 #Constante para el goal
N=30 #Tamaño del mapa
goal=[20,15,25] #Destino
R_soi=5 #Esfera de influencia del obstáculo
M=60 #Número de obstáculos
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


    datos=planificador_con_representacion(posicion,goal,m,F,obstacle)
    #representar3d_puntos(N, F, M, goal, obstacle, R_soi)
    #mapa_y_camino(datos,goal,obstacle)














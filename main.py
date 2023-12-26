from representaciones import *
from calculo_puntos import *


import math
import random
from tqdm import tqdm


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

m_goal=1 #Constante para el goal
N=30 #Tamaño del mapa
goal=[random.randint(0,N),random.randint(0,N),random.randint(0,N)] #Destino
R_soi=3 #Esfera de influencia del obstáculo
M=3 #Número de obstáculos

obstacle=[]
for i in range(M):
    obstacle+=[[random.randint(0,N),random.randint(0,N),random.randint(0,N)]]


if __name__ == '__main__':
    F=inicializa_F(N)
    gotogoal(goal,F,N,m_goal)
    for i in range(M):
        avoidobstacle(obstacle[i],F,N,R_soi)
    #representar3d_puntos(N,F,M,goal,obstacle,R_soi)
    representar2d_movimiento(N,M,goal,obstacle,R_soi,F)










import numpy

from generate_csv/representaciones import *
from generate_csv/calculo_puntos import *
from generate_csv/funciones_mapas import *
from generate_csv/planificador import *


from numpy import *
import math
import random
from tqdm import tqdm
import json


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

import csv
import copy

m_goal=1 #Constante para el goal
R_soi=5 #Esfera de influencia del obstáculo
guardar_mapa=False #False o True
cargar_mapa=False #False o True

m=2 #Margen de error respecto al goal

N_min=5  # Tamaño minimo de mapa N_min x N_min x N_min
N_max=14 # Tamaño maximo de mapa N_max x N_max x N_max

ocup_max = 10 # Porcentaje maximo de ocupacion

n_endpoints = 3 # Numero de inicios y finales distintos para cada set de obstaculos generado

# Insert here the name of the csv file
filename = "generate_csv/data_file6.csv"

if __name__ == '__main__':

    with open(filename, 'w', newline='') as data_file:
        pass
    for N in range(N_min,N_max+1): #Tamaño del mapa
        print("Tamaño del mapa: ",N)
        for M in range(1,round((N**3)*(ocup_max/100))): #Creando diferentes numeros de obstaculos para cada tamaño del mapa (hasta aprox. ocup_max %)
            print("Numero de obstaculos: ",M)
            obstacles=[]
            for i in range(M): #Creando un conjunto de obstaculos para cada numero de obstaculos y tamaño del mapa
                while True:
                    obstacle_x = random.randint(0,N-1)
                    obstacle_y = random.randint(0,N-1)
                    obstacle_z = random.randint(0,N-1)
                    add_obstacle = True
                    for obstacle in obstacles:
                        if (obstacle == [obstacle_x,obstacle_y,obstacle_z]):
                            add_obstacle = False
                    if add_obstacle:
                        obstacles+=[[obstacle_x,obstacle_y,obstacle_z]]
                        break
            for j in range(n_endpoints): #Creando diferentes inicios y goals para el anterior conjunto de obstaculos
                #print("Test numero: ",j)
                while True:
                    add_endpoints = True
                    goal = [random.randint(0,N-1),random.randint(0,N-1),random.randint(0,N-1)]
                    while True:
                        inicio = [random.randint(0,N-1),random.randint(0,N-1),random.randint(0,N-1)]
                        if (goal != inicio):
                            break
                    for obstacle in obstacles:
                        if (obstacle == goal or obstacle == inicio):
                            add_endpoints = False
                            break
                    if (add_endpoints):
                        break
                F=inicializa_F(N)
                gotogoal(goal,F,N,m_goal)
                for obstacle in obstacles:
                    avoidobstacle(obstacle,F,N,R_soi)

                steps,convergence=planificador(copy.deepcopy(inicio),goal,m,F,N)

                with open(filename, 'a', newline='') as data_file:
                    data_writer = csv.writer(data_file, delimiter=';')
                    data_writer.writerow([N, inicio, goal, M, obstacles, convergence, steps])

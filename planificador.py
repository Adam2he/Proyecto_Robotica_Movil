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

def planificador_pruebas(posicion,goal,m,F,N):
    datos = []
    cont=0
    while calcula_distancia(posicion, goal) > m and cont <1000:
        p1 = round(posicion[0])
        p2 = round(posicion[1])
        p3 = round(posicion[2])
        if p1 >= N:
            p1=N-1
        if p2 >= N:
            p2=N-1
        if p3 >= N:
            p3=N-1
        posicion[0] = posicion[0] + F[p1][p2][p3][0]
        posicion[1] = posicion[1] + F[p1][p2][p3][1]
        posicion[2] = posicion[2] + F[p1][p2][p3][2]
        datos += posicion
        cont+=1
    if cont==1000:
        return [0,0,0],cont
    else:
        return datos,cont


def planificador_nuevo(posicion,goal,m,obstacle,m_goal,R_soi):
    datos=[]
    while calcula_distancia(posicion,goal) > m:
        fuerzas=m_goal*np.array([goal[0]-posicion[0], goal[1] - posicion[1], goal[2] - posicion[2]]) / calcula_distancia(posicion,goal)
        for i in range(len(obstacle)):
            distancia=calcula_distancia(posicion,obstacle[i])
            if distancia<R_soi:
                fuerzas+=np.array([posicion[0]-obstacle[i][0],posicion[1]-obstacle[i][1],posicion[2]-obstacle[i][2]])*((R_soi-distancia)/distancia)/distancia
        posicion[0] = posicion[0] + fuerzas[0]
        posicion[1] = posicion[1] + fuerzas[1]
        posicion[2] = posicion[2] + fuerzas[2]
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



def planificador_nuevo_ajustable(posicion,goal,m,obstacle,m_goal,R_soi,N):
    datos=[]
    posicion_ant=[0,0,0]
    k=1 #Variable para salir del mínimo local
    cont=0
    while calcula_distancia(posicion,goal) > m and cont<1000:
        fuerzas=k*m_goal*np.array([goal[0]-posicion[0], goal[1] - posicion[1], goal[2] - posicion[2]]) / calcula_distancia(posicion,goal)
        for i in range(len(obstacle)):
            distancia=calcula_distancia(posicion,obstacle[i])
            if distancia<R_soi:
                fuerzas+=np.array([posicion[0]-obstacle[i][0],posicion[1]-obstacle[i][1],posicion[2]-obstacle[i][2]])*((R_soi-distancia)/distancia)/distancia
        posicion[0] += fuerzas[0]
        posicion[1] += fuerzas[1]
        posicion[2] += fuerzas[2]
        if posicion[0] > N or posicion[0] < 0:
            posicion[0]=posicion_ant[0]
        if posicion[1] > N or posicion[1] < 0:
            posicion[1]=posicion_ant[1]
        if posicion[2] > N or posicion[2] < 0:
            posicion[2]=posicion_ant[2]
        if calcula_distancia(posicion,posicion_ant) < 0.5:
            k+=0.1
        else:
            k=1
        posicion_ant[:]=posicion[:]
        datos+=posicion
        cont+=1
    if cont==1000:
        return [0,0,0],cont
    else:
        return datos,cont

def planificador_nuevo_ajustable_pruebas(posicion,goal,m,obstacle,m_goal,R_soi,N):
    datos=[]
    posicion_ant=[0,0,0]
    k=1 #Variable para salir del mínimo local
    cont=0
    while calcula_distancia(posicion,goal) > m and cont<1000:
        fuerzas=k*m_goal*np.array([goal[0]-posicion[0], goal[1] - posicion[1], goal[2] - posicion[2]]) / calcula_distancia(posicion,goal)
        for i in range(len(obstacle)):
            distancia=calcula_distancia(posicion,obstacle[i])
            if distancia<R_soi:
                fuerzas+=np.array([posicion[0]-obstacle[i][0],posicion[1]-obstacle[i][1],posicion[2]-obstacle[i][2]])*((R_soi-distancia)/distancia)/distancia
        posicion[0] += fuerzas[0]
        posicion[1] += fuerzas[1]
        posicion[2] += fuerzas[2]
        if posicion[0] > N or posicion[0] < 0:
            posicion[0]=posicion_ant[0]
        if posicion[1] > N or posicion[1] < 0:
            posicion[1]=posicion_ant[1]
        if posicion[2] > N or posicion[2] < 0:
            posicion[2]=posicion_ant[2]
        posicion_ant[:]=posicion[:]
        datos+=posicion
        cont+=1
    if cont==1000:
        return [0,0,0],cont
    else:
        return datos,cont


def planificador_nuevo_ajustable2(posicion,goal,m,obstacle,m_goal,R_soi,N):
    datos=[]
    posicion_ant=[0,0,0]
    cont=0
    k=1
    while calcula_distancia(posicion,goal) > m and cont<1000:
        fuerzas=k*m_goal*np.array([goal[0]-posicion[0], goal[1] - posicion[1], goal[2] - posicion[2]]) / calcula_distancia(posicion,goal)
        for i in range(len(obstacle)):
            distancia=calcula_distancia(posicion,obstacle[i])
            if distancia<R_soi:
                fuerzas+=np.array([posicion[0]-obstacle[i][0],posicion[1]-obstacle[i][1],posicion[2]-obstacle[i][2]])*((R_soi-distancia)/distancia)/distancia
        posicion[0] += fuerzas[0]
        posicion[1] += fuerzas[1]
        posicion[2] += fuerzas[2]
        if posicion[0] > N or posicion[0] < 0:
            posicion[0]=posicion_ant[0]
        if posicion[1] > N or posicion[1] < 0:
            posicion[1]=posicion_ant[1]
        if posicion[2] > N or posicion[2] < 0:
            posicion[2]=posicion_ant[2]
        if calcula_distancia(posicion,posicion_ant) < 0.5:
            R_soi-=0.1
            if R_soi<4:
                R_soi=4
        else:
            R_soi=5
        posicion_ant[:]=posicion[:]
        datos+=posicion
        cont+=1
    if cont==1000:
        return [0,0,0],cont
    else:
        return datos,cont






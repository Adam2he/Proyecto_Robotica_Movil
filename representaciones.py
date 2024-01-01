import math
import random
from tqdm import tqdm

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time


def representar3d(N,F):
    x, y, z = np.meshgrid(np.arange(N), np.arange(N), np.arange(N))

    # Crear una figura 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Graficar un vector en cada punto de la cuadrícula
    for i in range(N):
        for j in range(N):
            for k in range(N):
                ax.quiver(x[i, j, k], y[i, j, k], z[i, j, k], F[i, j, k][0], F[i, j, k][1], F[i, j, k][2])

    # Etiquetas de los ejes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Mostrar el gráfico
    plt.show()

def representar3d_puntos(N,F,M,goal,obstacle,R_soi):
    x, y, z = np.meshgrid(np.arange(N), np.arange(N), np.arange(N))

    # Crear una figura 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Etiquetas de los ejes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    k=0
    pbar = tqdm(total=100,desc='Creando gráfico',colour='blue')
    while k<N:
        for i in range(N):
            for j in range(N):
                for m in range(M):
                    obs = obstacle[m]
                    if math.sqrt((obs[0] - i) ** 2 + (obs[1] - j) ** 2 + (obs[2] - k) ** 2) <= R_soi:
                        color_flecha = 'r'
                        ax.quiver(y[i, j, k], x[i, j, k], z[i, j, k], F[i, j, k][0], F[i, j, k][1], F[i, j, k][2],
                                  color=color_flecha)
                if math.sqrt((goal[0] - i) ** 2 + (goal[1] - j) ** 2 + (goal[2] - k) ** 2) <= R_soi:
                    color_flecha = 'g'
                    ax.quiver(y[i, j, k], x[i, j, k], z[i, j, k], F[i, j, k][0], F[i, j, k][1], F[i, j, k][2],
                              color=color_flecha)
        pbar.update(100 / N)
        plt.draw()
        k=k+1
    plt.show()

def representar2d_movimiento(N,M,goal,obstacle,R_soi,F):
    x, y, z = np.meshgrid(np.arange(N), np.arange(N), np.arange(N))

    # Crear una figura 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Etiquetas de los ejes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    k=0
    t=0
    while True:
        for i in range(N):
            for j in range(N):
                color_flecha = 'b'
                for m in range(M):
                    obs = obstacle[m]
                    if math.sqrt((obs[0] - i) ** 2 + (obs[1] - j) ** 2 + (obs[2] - k) ** 2) <= R_soi:
                        color_flecha = 'r'
                if math.sqrt((goal[0] - i) ** 2 + (goal[1] - j) ** 2 + (goal[2] - k) ** 2) <= R_soi:
                    color_flecha = 'g'
                ax.quiver(y[i, j, k], x[i, j, k], z[i, j, k], F[i, j, k][0], F[i, j, k][1], F[i, j, k][2],
                          color=color_flecha)
        plt.draw()
        plt.pause(0.2)  # Mostrar la gráfica actual durante 1 segundo
        ax.clear()  # Limpiar la gráfica actual para la siguiente iteración
        if t==0:
            k=k+1
            if k==N-1:
                t=1
        else:
            k=k-1
            if k==0:
                t=0



def representar2d(k,N,obstacle,R_soi,goal,F,M):
    x, y, z = np.meshgrid(np.arange(N), np.arange(N), np.arange(N))

    # Crear una figura 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Graficar un vector en cada punto de la cuadrícula
    for i in range(N):
        for j in range(N):
            color_flecha = 'b'
            for m in range(M):
                obs=obstacle[m]
                if math.sqrt((obs[0]-i)**2+(obs[1]-j)**2+(obs[2]-k)**2) <= R_soi:
                    color_flecha='r'
            if math.sqrt((goal[0]-i)**2+(goal[1]-j)**2+(goal[2]-k)**2)<= R_soi:
                color_flecha='g'

            ax.quiver(y[i, j, k], x[i, j, k], z[i, j, k], F[i, j, k][0], F[i, j, k][1], F[i, j, k][2],color=color_flecha)

    # Etiquetas de los ejes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Mostrar el gráfico
    plt.show()


def mapa_y_camino(datos,goal,obstacle):
    # Crear una figura 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    i=0
    while i+2 < len(datos):
        x = datos[i]
        y = datos[i+1]
        z = datos[i+2]
        i+=3

        # Dibujar el punto
        ax.scatter(x, y, z, color='b',s=1)  # 's' es el tamaño del punto
    ax.scatter(goal[0], goal[1], goal[2], color='g', s=100)
    for i in range(len(obstacle)):
        ax.scatter(obstacle[i][0], obstacle[i][1], obstacle[i][2], color='r', s=100)

    # Mostrar el gráfico
    plt.show()


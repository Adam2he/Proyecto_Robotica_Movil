import math
import csv

import ast

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

if __name__ == '__main__':

    ############### INSERT HERE ###############

    # Insert here the name of the csv file
    filename = "data_file6.csv"

    # Insert here the number of figure rows
    n_rows=2

    ###########################################

    N_min=100000
    N_max=0

    with open(filename, newline='') as data_file:

        data_reader = csv.reader(data_file, delimiter=';')

        #row[0]: tamaño unidimensional del mapa
        #row[1]: inicio
        #row[2]: goal
        #row[3]: numero de obstaculos
        #row[4]: obstaculos
        #row[5]: convergencia
        #row[6]: steps

        for row in data_reader:
            N = int(row[0])
            if (N<N_min):
                N_min=N
            if (N>N_max):
                N_max=N
            
    # print("N_min: ", N_min)
    # print("N_max: ", N_max)

    # Calculating n_cols authomatically
    n_cols=1
    while(n_rows*n_cols<N_max-N_min+1):
        n_cols+=1
    # print("n_cols: ", n_cols)

    fig, axs = plt.subplots(n_rows, n_cols, subplot_kw={'projection': '3d'}, figsize=(24, 24))
    fig.suptitle('Comparativa entre densidad de obstáculos, distancia entre origen y destino, y número de pasos del algoritmo')
    for i in range(n_rows):
        for j in range(n_cols):
            if((i*n_cols+j)<=(N_max-N_min)):
                axs[i][j].set_title(f'Mapa de {(i*n_cols+j)+N_min}x{(i*n_cols+j)+N_min}x{(i*n_cols+j)+N_min}')
                axs[i][j].set_xlabel('Densidad (%)')
                axs[i][j].set_xlim(0, 10)
                axs[i][j].set_ylabel('Distancia')
                axs[i][j].set_ylim(0, 1.732*((i*n_cols+j)+N_min)) #(0,sqrt(3)*N])
                axs[i][j].set_zlabel('Numero de steps')

            else:
                axs[i][j].axis('off')
            
    

    fig2, axs2 = plt.subplots(n_rows, n_cols, figsize=(24, 24))
    fig2.suptitle('Comparativa entre casos de convergencia y de no convergencia')
    for i in range(n_rows):
        for j in range(n_cols):
            if((i*n_cols+j)<=(N_max-N_min)):
                axs2[i][j].set_title(f'Mapa de {(i*n_cols+j)+N_min}x{(i*n_cols+j)+N_min}x{(i*n_cols+j)+N_min}')
                axs2[i][j].set_xlabel('Densidad (%)')
                axs2[i][j].set_xlim(0, 10)
                axs2[i][j].set_ylabel('Distancia')
                axs2[i][j].set_ylim(0, 1.732*((i*n_cols+j)+N_min)) #(0,sqrt(3)*N])
            else:
                axs2[i][j].axis('off')
                    
    plt.subplots_adjust(wspace=0.5, hspace=0.5)
    

    with open(filename, newline='') as data_file:

        data_reader = csv.reader(data_file, delimiter=';')

        #row[0]: tamaño unidimensional del mapa
        #row[1]: inicio
        #row[2]: goal
        #row[3]: numero de obstaculos
        #row[4]: obstaculos
        #row[5]: convergencia
        #row[6]: steps

        for row in data_reader:

            N = int(row[0])
            inicio = ast.literal_eval(row[1])
            goal = ast.literal_eval(row[2])
            M = int(row[3])
            convergence = row[5] #como string
            size_steps = len(ast.literal_eval(row[6]))-1

            densidad = 100*M/(N**3)
            distancia = math.sqrt((inicio[0]-goal[0])**2+(inicio[1]-goal[1])**2+(inicio[2]-goal[2])**2)

            if (convergence=="True"):
                axs[int((N-N_min)/n_cols)][(N-N_min)%n_cols].scatter(densidad, distancia, size_steps, color='g', s=3)
                axs2[int((N-N_min)/n_cols)][(N-N_min)%n_cols].scatter(densidad, distancia, color='g', s=3)
            else:
                axs2[int((N-N_min)/n_cols)][(N-N_min)%n_cols].scatter(densidad, distancia, color='r', s=3)
    plt.show()

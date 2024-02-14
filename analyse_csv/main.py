import math
import csv
import numpy as np

import ast

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

if __name__ == '__main__':

    ############### INSERT HERE ###############

    # Insert here the name of the csv file
    filename = "generate_csv/data_file7.csv"

    # Insert here the number of figure rows
    n_rows=3

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
            
    print("N_min: ", N_min)
    print("N_max: ", N_max)

    # Calculating n_cols authomatically
    n_cols=1
    while(n_rows*n_cols<N_max-N_min+1):
        n_cols+=1
    print("n_cols: ", n_cols)

    fig1, axs1 = plt.subplots(n_rows, n_cols, figsize=(8, 8), squeeze=False)
    #fig1.suptitle('Comparativa entre casos de convergencia y de no convergencia')
    fig1.subplots_adjust(wspace=0.5, hspace=0.7, top=0.88)

    fig2, axs2 = plt.subplots(n_rows, n_cols, subplot_kw={'projection': '3d'}, figsize=(8, 8), squeeze=False)
    #fig2.suptitle('Comparativa entre densidad de obstáculos, distancia entre origen y destino, y número de pasos del algoritmo')
    fig2.subplots_adjust(wspace=0.8, hspace=0.8)

    fig3, axs3 = plt.subplots(n_rows, n_cols, figsize=(8, 8), squeeze=False)
    #fig3.suptitle('Comparativa entre densidad de obstáculos y número de pasos del algoritmo')
    fig3.subplots_adjust(wspace=0.8, hspace=0.7)

    fig4, axs4 = plt.subplots(n_rows, n_cols, figsize=(8, 8), squeeze=False)
    #fig4.suptitle('Comparativa entre distancia entre origen y destino y número de pasos del algoritmo')
    fig4.subplots_adjust(wspace=0.8, hspace=0.7)

    fig5, axs5 = plt.subplots(n_rows, n_cols, figsize=(8, 8), squeeze=False)
    #fig5.suptitle('Comparativa entre densidad de obstáculos y distancia salvada respecto al óptimo(%)')
    fig5.subplots_adjust(wspace=0.8, hspace=0.7)

    fig6, axs6 = plt.subplots(n_rows, n_cols, figsize=(8, 8), squeeze=False)
    #fig6.suptitle('Comparativa entre distancia inicial y distancia salvada respecto al óptimo(%)')
    fig6.subplots_adjust(wspace=0.8, hspace=0.7)

    qty_N5 = 0
    qty_N13 = 0
    

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
            final_step = ast.literal_eval(row[6])[-1]

            densidad = 100*M/(N**3)
            distancia = math.sqrt((inicio[0]-goal[0])**2+(inicio[1]-goal[1])**2+(inicio[2]-goal[2])**2)
            distancia_final = math.sqrt((final_step[0]-goal[0])**2+(final_step[1]-goal[1])**2+(final_step[2]-goal[2])**2)
            distancia_salvada = (distancia-distancia_final)/distancia*100

            if (convergence=="True"):
                axs1[int((N-N_min)/n_cols)][(N-N_min)%n_cols].scatter(densidad, distancia, color='g', s=3)
                axs2[int((N-N_min)/n_cols)][(N-N_min)%n_cols].scatter(densidad, distancia, size_steps, color='g', s=3)
                axs3[int((N-N_min)/n_cols)][(N-N_min)%n_cols].scatter(densidad, size_steps, color='g', s=3)
                axs4[int((N-N_min)/n_cols)][(N-N_min)%n_cols].scatter(distancia, size_steps, color='g', s=3)
            else:
                axs1[int((N-N_min)/n_cols)][(N-N_min)%n_cols].scatter(densidad, distancia, color='r', s=3)
                axs5[int((N-N_min)/n_cols)][(N-N_min)%n_cols].scatter(densidad, distancia_salvada, color='r', s=3)
                axs6[int((N-N_min)/n_cols)][(N-N_min)%n_cols].scatter(distancia, distancia_final, color='r', s=3)

            if (N==5):
                qty_N5 += 1
            if (N==13):
                qty_N13 += 1
    print("N5: ", qty_N5)
    print("N13: ", qty_N13)

    for i in range(n_rows):
        for j in range(n_cols):
            if((i*n_cols+j)<=(N_max-N_min)):
                axs1[i][j].set_title(f'Mapa de {(i*n_cols+j)+N_min}x{(i*n_cols+j)+N_min}x{(i*n_cols+j)+N_min}')
                axs1[i][j].set_xlabel('Densidad (%)')
                axs1[i][j].set_xlim(0, 10)
                axs1[i][j].set_ylabel('Distancia inicial')
                axs1[i][j].set_ylim(0, 1.732*((i*n_cols+j)+N_min)) #(0,sqrt(3)*N])
            else:
                axs1[i][j].axis('off')
    axs1[0][0].scatter([], [], color='g', s=3, label='Converge')
    axs1[0][0].scatter([], [], color='r', s=3, label='No converge')
    fig1.legend(loc='upper center')
    fig1.savefig('analyse_csv/convergence.png')

    for i in range(n_rows):
        for j in range(n_cols):
            if((i*n_cols+j)<=(N_max-N_min)):
                axs2[i][j].set_title(f'Mapa de {(i*n_cols+j)+N_min}x{(i*n_cols+j)+N_min}x{(i*n_cols+j)+N_min}')
                axs2[i][j].set_xlabel('Densidad (%)')
                axs2[i][j].set_xlim(0, 10)
                axs2[i][j].set_ylabel('Distancia inicial')
                axs2[i][j].set_ylim(0, 1.732*((i*n_cols+j)+N_min)) #(0,sqrt(3)*N])
                axs2[i][j].set_zlabel('Numero de steps')
            else:
                axs2[i][j].axis('off')
    fig2.savefig('analyse_csv/steps_number.png')

    for i in range(n_rows):
        for j in range(n_cols):
            if((i*n_cols+j)<=(N_max-N_min)):
                axs3[i][j].set_title(f'Mapa de {(i*n_cols+j)+N_min}x{(i*n_cols+j)+N_min}x{(i*n_cols+j)+N_min}')
                axs3[i][j].set_xlabel('Densidad (%)')
                axs3[i][j].set_xlim(0, 10)
                axs3[i][j].set_ylabel('Numero de steps')
            else:
                axs3[i][j].axis('off')
    fig3.savefig('analyse_csv/steps_numberVdensidad.png')

    for i in range(n_rows):
        for j in range(n_cols):
            if((i*n_cols+j)<=(N_max-N_min)):
                axs4[i][j].set_title(f'Mapa de {(i*n_cols+j)+N_min}x{(i*n_cols+j)+N_min}x{(i*n_cols+j)+N_min}')
                axs4[i][j].set_xlabel('Distancia inicial')
                axs4[i][j].set_xlim(0, 1.732*((i*n_cols+j)+N_min)) #(0,sqrt(3)*N])
                axs4[i][j].set_ylabel('Numero de steps')
            else:
                axs4[i][j].axis('off')
    fig4.savefig('analyse_csv/steps_numberVdistancia.png')

    for i in range(n_rows):
        for j in range(n_cols):
            if((i*n_cols+j)<=(N_max-N_min)):
                axs5[i][j].set_title(f'Mapa de {(i*n_cols+j)+N_min}x{(i*n_cols+j)+N_min}x{(i*n_cols+j)+N_min}')
                axs5[i][j].set_xlabel('Densidad (%)')
                axs5[i][j].set_xlim(0, 10)
                axs5[i][j].set_ylabel('Distancia salvada (%)')
                axs5[i][j].set_ylim(top=100)
                axs5[i][j].axhline(y=0, color='black', linestyle='--', alpha=0.75, zorder=0)
            else:
                axs5[i][j].axis('off')
    fig5.savefig('analyse_csv/recorridoVdensidad.png')

    for i in range(n_rows):
        for j in range(n_cols):
            if((i*n_cols+j)<=(N_max-N_min)):
                axs6[i][j].set_title(f'Mapa de {(i*n_cols+j)+N_min}x{(i*n_cols+j)+N_min}x{(i*n_cols+j)+N_min}')
                axs6[i][j].set_xlabel('Distancia inicial')
                axs6[i][j].set_xlim(0, 1.732*((i*n_cols+j)+N_min)) #(0,sqrt(3)*N])
                axs6[i][j].set_ylabel('Distancia final')
                lims = [
                    np.min([axs6[i][j].get_xlim(), axs6[i][j].get_ylim()]),  # min of both axes
                    np.max([axs6[i][j].get_xlim(), axs6[i][j].get_ylim()]),  # max of both axes
                ]
                axs6[i][j].plot(lims, lims, 'k--', alpha=0.75, zorder=0)
                axs6[i][j].set_aspect('equal')
                axs6[i][j].set_xlim(lims)
                axs6[i][j].set_ylim(lims)
            else:
                axs6[i][j].axis('off')
    fig6.savefig('analyse_csv/recorridoVdistancia.png')

    #plt.show()

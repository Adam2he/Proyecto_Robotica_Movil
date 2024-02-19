import math
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

############### INSERT HERE ###############

# Insert here the name of the csv file
filename = "data_file5.json"

###########################################

fig1 = plt.figure(figsize=(8, 8))
axs1 = fig1.add_subplot(111)
#fig1.suptitle('Comparativa entre casos de convergencia y de no convergencia')

#fig2 = plt.figure(figsize=(8, 8))
#axs2 = fig2.add_subplot(111, projection='3d')
#fig2.suptitle('Comparativa entre densidad de obstáculos, distancia entre origen y destino, y número de pasos del algoritmo')

fig3 = plt.figure(figsize=(8, 8))
axs3 = fig3.add_subplot(111)
#fig3.suptitle('Comparativa entre densidad de obstáculos y número de pasos del algoritmo')

fig4 = plt.figure(figsize=(8, 8))
axs4 = fig4.add_subplot(111)
#fig4.suptitle('Comparativa entre distancia entre origen y destino y número de pasos del algoritmo')

fig5 = plt.figure(figsize=(8, 8))
axs5 = fig5.add_subplot(111)
#fig5.suptitle('Comparativa entre densidad de obstáculos y distancia salvada respecto al óptimo(%)')

fig6 = plt.figure(figsize=(8, 8))
axs6 = fig6.add_subplot(111)
#fig6.suptitle('Comparativa entre distancia inicial y distancia salvada respecto al óptimo(%)')



with open(filename, "r") as data_file:

    for row in data_file:
    
        data=json.loads(row)
        
        N = int(data["N"])
        origen = np.array(data["origen"])
        destino = np.array(data["destino"])
        M = int(data["M"])
        status = data["status"]
        steps_number = int(data["steps_number"])
        final_step = np.array(data["final_step"])
        R_obstacle = float(data["R_obstacle"])

        V_obstacle = (4/3)*math.pi*(R_obstacle**3)
        densidad = M*V_obstacle/(N**3)*100
        distancia_inicial = math.sqrt((origen[0]-destino[0])**2+(origen[1]-destino[1])**2+(origen[2]-destino[2])**2)
        distancia_final = math.sqrt((final_step[0]-destino[0])**2+(final_step[1]-destino[1])**2+(final_step[2]-destino[2])**2)
        distancia_salvada = (distancia_inicial-distancia_final)/distancia_inicial*100

        if (status=="success"):
            axs1.scatter(M, distancia_inicial, color='g', s=5)
            #axs2.scatter(densidad, distancia_inicial, steps_number, color='g', s=5)
            axs3.scatter(M, steps_number, color='g', s=5)
            axs4.scatter(distancia_inicial, steps_number, color='g', s=5)
        elif (status=="fail_collision"):
            axs1.scatter(M, distancia_inicial, color='r', s=5)
            axs5.scatter(M, distancia_salvada, color='r', s=5)
            axs6.scatter(distancia_inicial, distancia_final, color='r', s=5)
        elif (status=="fail_not_arrived"):
            axs1.scatter(M, distancia_inicial, color='m', s=5)
            axs5.scatter(M, distancia_salvada, color='m', s=5)
            axs6.scatter(distancia_inicial, distancia_final, color='m', s=5)

axs1.set_xlabel('Número de obstáculos')
axs1.set_xlim(0, 10000)
axs1bis = axs1.twiny()
limL, limH = axs1.get_xlim()
axs1bis.set_xlim(limL*V_obstacle/(N**3)*100,limH*V_obstacle/(N**3)*100)
axs1bis.set_xlabel('Densidad (%)')
axs1.set_ylabel('Distancia entre origen y destino (m)')
axs1.set_ylim(0, 1.732*N) #(0,sqrt(3)*N])
axs1.scatter([], [], color='g', s=5, label='Éxito')
axs1.scatter([], [], color='r', s=5, label='Colisión')
axs1.scatter([], [], color='m', s=5, label='Mínimo local')
axs1.legend(loc='upper right')
fig1.savefig('convergence.png')

#axs2.set_xlabel('Densidad (%)')
#axs2.set_xlim(0, 35)
#axs2.set_ylabel('Distancia inicial')
#axs2.set_ylim(0, 1.732*N) #(0,sqrt(3)*N])
#axs2.set_zlabel('Numero de steps')
#fig2.savefig('steps_number.png')

axs3.set_xlabel('Número de obstáculos')
axs3.set_xlim(0, 10000)
axs3bis = axs3.twiny()
limL, limH = axs1.get_xlim()
axs3bis.set_xlim(limL*V_obstacle/(N**3)*100,limH*V_obstacle/(N**3)*100)
axs3bis.set_xlabel('Densidad (%)')
axs3.set_ylabel('Numero de steps')
axs3.scatter([], [], color='g', s=5, label='Éxito')
axs3.legend(loc='upper right')
fig3.savefig('steps_numberVdensidad.png')

axs4.set_xlabel('Distancia entre origen y destino (m)')
axs4.set_xlim(0, 1.732*N) #(0,sqrt(3)*N])
axs4.set_ylabel('Numero de steps')
axs4.scatter([], [], color='g', s=5, label='Éxito')
axs4.legend(loc='upper right')
fig4.savefig('steps_numberVdistancia.png')

axs5.set_xlabel('Número de obstáculos')
axs5.set_xlim(0, 10000)
axs5bis = axs5.twiny()
limL, limH = axs5.get_xlim()
axs5bis.set_xlim(limL*V_obstacle/(N**3)*100,limH*V_obstacle/(N**3)*100)
axs5bis.set_xlabel('Densidad (%)')
axs5.set_ylabel('Distancia salvada (%)')
axs5.set_ylim(top=100)
axs5.axhline(y=0, color='black', linestyle='--', alpha=0.75, zorder=0)
axs5.scatter([], [], color='r', s=5, label='Colisión')
axs5.scatter([], [], color='m', s=5, label='Mínimo local')
axs5.legend(loc='center left')
fig5.savefig('recorridoVdensidad.png')

axs6.set_xlabel('Distancia entre origen y destino (m)')
axs6.set_xlim(0, 1.732*N) #(0,sqrt(3)*N])
axs6.set_ylabel('Distancia final entre robot y destino (m)')
lims = [
    0,
    np.max([axs6.get_xlim(), axs6.get_ylim()]),  # max of both axes
]
axs6.plot(lims, lims, 'k--', alpha=0.75, zorder=0)
axs6.set_aspect('equal')
axs6.set_xlim(lims)
axs6.set_ylim(lims)
axs6.scatter([], [], color='r', s=5, label='Colisión')
axs6.scatter([], [], color='m', s=5, label='Mínimo local')
axs6.legend(loc='upper left')
fig6.savefig('recorridoVdistancia.png')

plt.show()

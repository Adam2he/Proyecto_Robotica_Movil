import math
import random
import numpy as np
import json

def calcula_distancia(posicion1, posicion2):
    return math.sqrt((posicion1[0]-posicion2[0])**2+(posicion1[1]-posicion2[1])**2+(posicion1[2]-posicion2[2])**2)
    
def calcula_fuerzas(posicion, goal, obstacles, m_goal, R_soi, R_obstacle, k):
    F = k*m_goal*np.array([goal[0]-posicion[0],goal[1]-posicion[1],goal[2]-posicion[2]]) / calcula_distancia(posicion, goal)
    for obstacle in obstacles:
        distancia = calcula_distancia(posicion, obstacle)
        if distancia <= R_soi:
            F += ((R_soi-distancia)/(R_soi-R_obstacle)) * np.array([posicion[0]-obstacle[0], posicion[1]-obstacle[1], posicion[2]-obstacle[2]]) / distancia
    F /= math.sqrt((F[0]**2)+(F[1]**2)+(F[2]**2))
    return F

def planificador(ini, goal, m, obstacles, m_goal, R_soi, R_obstacle, R_robot, N, maximum_step_size):
    steps=np.array([ini])
    max_iter = 3*calcula_distancia(ini,goal)/maximum_step_size
    iter = 0
    k=1
    status = "searching"
    while (calcula_distancia(steps[-1], goal) > maximum_step_size and iter<max_iter and status=="searching"):
        if any(calcula_distancia(steps[-1], obstacle) <=R_obstacle+R_robot for obstacle in obstacles):
            status = "fail_collision"
        else:
            F = calcula_fuerzas(steps[-1], goal, obstacles, m_goal, R_soi, R_obstacle, k)
            modulo_F = np.linalg.norm(F)
            #while(modulo_F>=maximum_step_size and k>1):
            #    k-=0.01
            #    F = calcula_fuerzas(steps[-1], goal, obstacles, m_goal, R_soi, R_obstacle, k)
            #    modulo_F = np.linalg.norm(F)
            #if k<1:
            #    k=1
            #
            if modulo_F>=maximum_step_size:
                F = F/modulo_F*maximum_step_size
            #else:
            #    k+=0.01
            
            p_posicion = steps[-1] + F
            
            for i in range(3):
                if p_posicion[i]<0:
                    p_posicion[i] = 0
                elif p_posicion[i]>N:
                    p_posicion[i] = N
            steps = np.append(steps, [p_posicion], axis=0)
            iter += 1
            
            if modulo_F<maximum_step_size*0.1:
                status = "fail_not_arrived"
    if status == "searching":
        if (calcula_distancia(steps[-1], goal) > maximum_step_size):
            status = "fail_not_arrived"
        else:
            status = "success"
            steps = np.append(steps, [goal], axis=0)
    return steps, status

N = 50 #tamaño de mapa
#M numero de obstáculos
R_soi = 3
R_obstacle = 1
R_robot = 0.25
m=1
m_goal=0.8
maximum_step_size=0.2

# Insert here the name of the csv file
filename = "data_file5.json"

with open(filename, 'w') as data_file:
    pass
    
for prueba in range(1500): #Numero de pruebas
    print("Prueba número: ",prueba)
    #obstáculos
    M = random.randint(0,10000)
    print("Número de obstáculos: ",M)
    obstacles=np.empty((0, 3))
    for _ in range(M):
        obstacles = np.append(obstacles, np.array([[random.uniform(0, N),random.uniform(0, N),random.uniform(0, N)]]), axis=0)
            
    #origen
    origen_valido=False
    while not origen_valido:
        origen_valido=True
        origen = np.array([random.uniform(0,N),random.uniform(0,N),random.uniform(0,N)])
        for obstacle in obstacles:
            if calcula_distancia(origen, obstacle) <= R_obstacle+R_robot:
                origen_valido = False
    
    #destino
    destino_valido=False
    while not destino_valido:
        destino_valido=True
        destino = np.array([random.uniform(0,N),random.uniform(0,N),random.uniform(0,N)])
        for obstacle in obstacles:
            if calcula_distancia(destino, obstacle) <= R_obstacle+R_robot:
                destino_valido = False
    
    #steps
    steps, status = planificador(origen,destino,m=m,obstacles=obstacles,m_goal=m_goal,R_soi=R_soi,R_obstacle=R_obstacle, R_robot=R_robot,N=N,maximum_step_size=maximum_step_size)
    print("status: ", status)
    
    with open(filename, 'a') as data_file:
        data = {
            "N": N,
            "origen": origen.tolist(),
            "destino": destino.tolist(),
            "M": M,
            "status": status,
            "steps_number": steps.shape[0],
            "final_step": steps[-1].tolist(),
            "R_soi": R_soi,
            "R_obstacle": R_obstacle,
            "R_robot": R_robot
        }
        json.dump(data, data_file)
        data_file.write('\n')

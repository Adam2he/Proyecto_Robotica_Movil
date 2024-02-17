#!/usr/bin/env python3

from __future__ import print_function

import sys
import rospy
from std_msgs.msg import String, Header
from visualization_msgs.msg import Marker
from sensor_msgs.msg import PointCloud2, PointField
from geometry_msgs.msg import Point
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
import random
import struct
import numpy as np
import math

def publish_marker(pub,marker_id, position, r, g, b, scale, marker_type):
    
    rate = rospy.Rate(10) # 10hz
    #rospy.sleep(0.3)
    
    # Crear un nuevo marcador
    marker = Marker()
    marker.header.frame_id = "base_link"
    marker.type = marker_type
    marker.action = Marker.ADD
    marker.scale.x = scale[0]  # Escala del marcador en el eje x
    marker.scale.y = scale[1]  # Escala del marcador en el eje y
    marker.scale.z = scale[2]  # Escala del marcador en el eje z
    marker.color.a = 1.0  # Opacidad del marcador
    marker.color.r = r  # Componente roja del color
    marker.color.g = g  # Componente verde del color
    marker.color.b = b  # Componente azul del color
    
    # Asignar el identificador al marcador
    marker.id = marker_id
    
    # Definir la posición del marcador
    marker.pose.position = Point()
    marker.pose.position.x = position[0]  # Coordenada x del punto
    marker.pose.position.y = position[1]  # Coordenada y del punto
    marker.pose.position.z = position[2]  # Coordenada z del punto
    
    #while not rospy.is_shutdown():
    hello_str = "publishing marker %s" % rospy.get_time()
    rospy.loginfo(hello_str)
    
    # Publicar el marcador
    pub.publish(marker)
    rate.sleep()

def publish_obstacles(pub, obstacles, r, g, b):
    
    rate = rospy.Rate(10) # 10hz
    #rospy.sleep(0.5)

    points = np.zeros(len(obstacles), dtype=[
        ('x', np.float32),
        ('y', np.float32),
        ('z', np.float32),
        ('rgba', np.uint32)
    ])
    
    a = 255
    color = struct.unpack('I', struct.pack('BBBB', b, g, r, a))[0]
    
    for i, obstacle in enumerate(obstacles):
        points['x'][i] = obstacle[0]
        points['y'][i] = obstacle[1]
        points['z'][i] = obstacle[2]
        points['rgba'][i] = color
    
    header = Header()
    header.stamp = rospy.Time.now()
    header.frame_id = "base_link"  # Adjust frame_id as needed

    cloud_msg = PointCloud2()
    cloud_msg.header = header
    cloud_msg.height = 1
    cloud_msg.width = points.shape[0]
    cloud_msg.fields = [
        PointField('x', 0, PointField.FLOAT32, 1),
        PointField('y', 4, PointField.FLOAT32, 1),
        PointField('z', 8, PointField.FLOAT32, 1),
        PointField('rgba', 12, PointField.UINT32, 1)
    ]
    cloud_msg.is_bigendian = False
    cloud_msg.point_step = 16
    cloud_msg.row_step = cloud_msg.point_step * cloud_msg.width
    cloud_msg.is_dense = True
    cloud_msg.data = points.tostring()
    
    # Publicar la nube de obstáculos
    hello_str = "publishing cloud %s" % rospy.get_time()
    rospy.loginfo(hello_str)
    pub.publish(cloud_msg)
    rate.sleep()

def publish_path(pub, steps):
    
    rate = rospy.Rate(10)  # 10 Hz
    #rospy.sleep(0.5)

    # Crea un mensaje de tipo Path
    path_msg = Path()
    path_msg.header.stamp = rospy.Time.now()
    path_msg.header.frame_id = "base_link"  # Ajusta el frame_id según sea necesario

    # Agrega algunas poses al mensaje Path
    for step in steps:
        pose = PoseStamped()
        pose.header.stamp = rospy.Time.now()
        pose.header.frame_id = "base_link"  # Ajusta el frame_id según sea necesario
        pose.pose.position.x = step[0]  # Ajusta las coordenadas x, y, z según sea necesario
        pose.pose.position.y = step[1]
        pose.pose.position.z = step[2]
        pose.pose.orientation.w = 1  # Orientación como cuaternión (en este caso, sin rotación)
        path_msg.poses.append(pose)

    # Publica el mensaje Path
    pub.publish(path_msg)
    rate.sleep()

def calcula_distancia(posicion1, posicion2):
    return math.sqrt((posicion1[0]-posicion2[0])**2+(posicion1[1]-posicion2[1])**2+(posicion1[2]-posicion2[2])**2)
    
def calcula_fuerzas(posicion, goal, obstacles, m_goal, R_soi, k):
    F = k*m_goal*np.array([goal[0]-posicion[0],goal[1]-posicion[1],goal[2]-posicion[2]]) / calcula_distancia(posicion, goal)
    for obstacle in obstacles:
        distancia = calcula_distancia(posicion, obstacle)
        if distancia <= R_soi:
            F += ((R_soi-distancia)/distancia) * np.array([posicion[0]-obstacle[0], posicion[1]-obstacle[1], posicion[2]-obstacle[2]]) / distancia
    F /= math.sqrt((F[0]**2)+(F[1]**2)+(F[2]**2))
    return F

def planificador(ini, goal, m, obstacles, m_goal, R_soi, R_obstacle, R_robot, N, step_size, path_pub):
    steps=np.array([ini])
    max_iter = 3*N/step_size
    iter = 0
    arrived = True
    k=1
    while (calcula_distancia(steps[-1], goal) > step_size and iter<max_iter):
        if any(calcula_distancia(steps[-1], obstacle) <=R_obstacle+R_robot for obstacle in obstacles):
            print("Ha chocado contra un obstáculo")
            break
        else:
            F = calcula_fuerzas(steps[-1], goal, obstacles, m_goal, R_soi,k)
            p_posicion = steps[-1] + step_size * F
            #if (len(steps)>2 and calcula_distancia(steps[-1],steps[-3])<step_size/10):
            #    print("getting stuck")
            #    k += 1
            #else:
            #    k = 1
            for i in range(3):
                if p_posicion[i]<0:
                    p_posicion[i] = 0
                elif p_posicion[i]>N:
                    p_posicion[i] = N
            steps = np.append(steps, [p_posicion], axis=0)
            iter += 1
            publish_path(path_pub, steps)
    if (calcula_distancia(steps[-1], goal) > step_size):
        arrived = False
    else:
        steps = np.append(steps, [goal], axis=0)
        publish_path(path_pub, steps)
    return steps, arrived

if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            M = int(sys.argv[1]) #numero de obstáculos
        else:
            print(usage())
            sys.exit(1)
        N = 50 #tamaño de mapa
        #M = 100 #numero de obstáculos
        R_soi = 5
        R_obstacle = 1
        R_robot = 0.25
        m=1
        m_goal=2.5
        step_size=1
        true_dimension = False
        
        rospy.init_node('planner')
        marker_pub = rospy.Publisher('visualization_marker', Marker, queue_size=10)
        obstacles_pub = rospy.Publisher('point_cloud', PointCloud2, queue_size=10)
        path_pub = rospy.Publisher('/path_topic', Path, queue_size=10)
        rospy.sleep(1)
        
        #obstáculos
        obstacles=np.empty((0, 3))
        for _ in range(M):
            obstacles = np.append(obstacles, np.array([[random.uniform(0, N),random.uniform(0, N),random.uniform(0, N)]]), axis=0)
        publish_obstacles(obstacles_pub, obstacles, r=255, g=0, b=0)
                
        #origen
        origen_valido=False
        while not origen_valido:
            origen_valido=True
            origen = np.array([random.uniform(0,N),random.uniform(0,N),random.uniform(0,N)])
            for obstacle in obstacles:
                if calcula_distancia(origen, obstacle) <= R_obstacle+R_robot:
                    origen_valido = False
        if true_dimension:
            publish_marker(marker_pub, marker_id=0, position = origen, r=1.0, g=1.0, b=0.0, scale=[R_robot*2, R_robot*2, R_robot], marker_type = Marker.CUBE)
        else:
            publish_marker(marker_pub, marker_id=0, position = origen, r=1.0, g=1.0, b=0.0, scale=[1, 1, 0.5], marker_type = Marker.CUBE)
        
        #destino
        destino_valido=False
        while not destino_valido:
            destino_valido=True
            destino = np.array([random.uniform(0,N),random.uniform(0,N),random.uniform(0,N)])
            for obstacle in obstacles:
                if calcula_distancia(destino, obstacle) <= R_obstacle+R_robot:
                    destino_valido = False
        publish_marker(marker_pub, marker_id=1, position = destino, r=0.0, g=1.0, b=0.0, scale=[2.0, 2.0, 2.0], marker_type=Marker.SPHERE)
        
        #steps
        steps, arrived = planificador(origen,destino,m=m,obstacles=obstacles,m_goal=m_goal,R_soi=R_soi,R_obstacle=R_obstacle, R_robot=R_robot,N=N,step_size=step_size,path_pub=path_pub)
        #publish_path(path_pub, steps)
        
        #mover el robot
        if arrived:
            for i in range(len(steps)-1):
                intra_steps=np.linspace(steps[i], steps[i+1], 1)
                for intra_step in intra_steps:
                    if true_dimension:
                        publish_marker(marker_pub, marker_id=0, position = intra_step, r=1.0, g=1.0, b=0.0, scale=[R_robot*2, R_robot*2, R_robot], marker_type = Marker.CUBE)
                    else:
                        publish_marker(marker_pub, marker_id=0, position = intra_step, r=1.0, g=1.0, b=0.0, scale=[1, 1, 0.5], marker_type = Marker.CUBE)
        
    except rospy.ROSInterruptException:
        pass

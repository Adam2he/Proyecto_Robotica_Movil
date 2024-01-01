from os import remove
import numpy
import pickle

def guarda_mapa(F):
    try:
        remove('mapa.npy')
    except:
        a = 'hola'
    numpy.save('mapa.npy', F)

def carga_mapa():
    F=numpy.load('mapa.npy',allow_pickle=True)
    return F

def guarda_variables(m_goal,N,goal,R_soi,M,inicio,obstacle):
    # Guardar las variables en un archivo
    try:
        remove('variables.pkl')
    except:
        a = 'hola'
    with open('variables.pkl', 'wb') as f:
        pickle.dump((m_goal,N,goal,R_soi,M,inicio,obstacle), f)

def carga_variables():
    with open('variables.pkl', 'rb') as f:
        m_goal,N,goal,R_soi,M,inicio,obstacle = pickle.load(f)
    return m_goal,N,goal,R_soi,M,inicio,obstacle
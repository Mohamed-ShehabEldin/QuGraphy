#This python file will contain the functions that make calculations & visualisation related to density matrix
import numpy as np
from numpy import linalg as LA

#Pauli Matrices
pauli_x=[
    [0 , 1],
    [1 , 0]
]

pauli_y=[
    [0 , -1j],
    [1j , 0]
]

pauli_z=[
    [1 , 0],
    [0 , -1]
]


#this function will form the density matrix from given states
def density(*states):
    composite=states[0]
    if len(states)>1:
        for s in range(len(states)-1):
            composite=np.kron(composite,states[s+1])
    return composite * np.transpose(np.conjugate(composite))


#this function will check is the given density matrix is valid or not
def checkdensity(density):
    w, v = LA.eig(density)
    for i in w:
        if i<0:
            raise Exception("invalid Matrix, not positive definite!")

    if np.trace(density) != 1:
        raise Exception("invalid Matrix, not unit traced!")

    if np.transpose(np.conjugate(density)) != density:
        raise Exception("invalid Matrix, not Hermitian!")

def schmidt_inner(A,B):
    return np.trace(np.transpose(np.conjugate(A))*B)

def bloch_vector(array):
    if np.ndim(array)==1:
        array=density(array)

    if np.ndim(array)>2:
        raise Exception("invalid Matrix/State, not single qubit!")

    v_x=2*schmidt_inner(array,pauli_x)
    v_y=2*schmidt_inner(array,pauli_y)
    v_z=2*schmidt_inner(array,pauli_z)

    return [v_x, v_y, v_z]




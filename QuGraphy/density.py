#This python file will contain the functions that make calculations & visualisation related to density matrix
import numpy as np
from .state import *
from numpy import linalg as LA
from qutip import *  #have matplotlib dependency
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
#Pauli Matrices
pauli_x=np.array([
    [0 , 1],
    [1 , 0]
])

pauli_y=np.array([
    [0 , -1j],
    [1j , 0]
])

pauli_z=np.array([
    [1 , 0],
    [0 , -1]
])

#standard basis
s0=np.array([
    [1],
    [0]
])
s1=np.array([
    [0],
    [1]
])
#this function will form the density matrix from given states
def density(*states):
    composite=states[0]
    if len(states)>1:
        for s in range(len(states)-1):
            composite=np.kron(composite,states[s+1])
    return composite * np.transpose(np.conjugate(composite))


#this function will check is the given density matrix is valid or not
def check_density(density):
    w, v = LA.eig(density)
    for i in w:
        if i<0:
            raise Exception("invalid Matrix, not positive definite!")

    if np.trace(density) != 1:
        raise Exception("invalid Matrix, not unit traced!")

    if np.transpose(np.conjugate(density)) != density:
        raise Exception("invalid Matrix, not Hermitian!")

    if np.shape(density)[0] != np.shape(density)[1]:
        raise Exception("invalid Matrix, not a Square Matrix!")

    possible_dim=[]
    n=1
    for i in range(1,100):
        n=n*2
        possible_dim.append(n)

    if np.shape(density)[0] not in possible_dim:
        print('\033[91m' + "Not a Qubit/s System!" + '\033[0m')

#this function compute the schmidt inner product between two matrices
def schmidt_inner(A,B):
    return np.trace(np.dot(np.transpose(np.conjugate(A)),B))


#This function will return bloch vector given the density matrix or the state
def bloch_vector(array,visualize=True):
    if min(np.shape(array))==1:
        array=density(array)

    if np.shape(array)[0]>2:
        raise Exception("invalid Matrix/State, not single qubit!")

    v_x=2*schmidt_inner(array,pauli_x)
    v_y=2*schmidt_inner(array,pauli_y)
    v_z=2*schmidt_inner(array,pauli_z)

    if visualize==True:
        b = Bloch()   #qutip object
        b.add_vectors([v_x,v_y,v_z])
        b.show()

    return [v_x, v_y, v_z]


def is_pure(density):
    check_density(density)

    if np.trace(np.dot(density,density)) ==1:
        return True
    elif 0<= np.trace(np.dot(density,density))<1:
        return False
    else:
        raise Exception("invalid Matrix, trace of squared matrix is not in range 0 to 1!")

#this function will make the tensor product for all matrices in a given list
def kron_all(list):
    kroned=1
    for matrix in list:
        kroned=np.kron(kroned,matrix)
    return kroned


#this function will compute the partial trace and trace out certain qubit
def trace_out(rho, out='1',check=False):
    if min(np.shape(rho))==1:
        if check == True: check_state(rho)
        rho=density(rho)
    else:
        if check == True: check_density(rho)

    if len(str(out)) > 1:
        raise Exception("this function only trace out one qubit, if you want more apply it more!")

    n_qubits = int(np.log(np.shape(rho)[0]) / np.log(2))
    op0 = [[[1, 0], [0, 1]]] * n_qubits
    op1 = [[[1, 0], [0, 1]]] * n_qubits

    if int(out) > n_qubits or '0' in str(out):
        raise Exception("the desired system out of range!")

    op0[int(out) - 1] = s0
    op1[int(out) - 1] = s1

    # make kron operation
    reduced0 = np.dot(np.transpose(kron_all(op0)), np.dot(density, kron_all(op0)))
    reduced1 = np.dot(np.transpose(kron_all(op1)), np.dot(density, kron_all(op1)))
    reduced = reduced0 + reduced1

    return reduced


#this function will calculate the trace distance given two density matrices
def trace_distance(rho1, rho2):

    A = rho1 - rho2
    eigA, vecA = LA.eig(A)

    d = 0
    for j in range(len(eigA)):
        if (eigA[j] > 0):
            d = d + eigA[j]

    return d

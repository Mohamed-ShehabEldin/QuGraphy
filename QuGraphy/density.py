#This python file will contain the functions that make calculations & visualisation related to density matrix
import numpy as np
from numpy import linalg as LA
from qutip import *  #have matplotlib dependency
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
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

#standard basis
s0=[
    [1],
    [0]
]
s1=[
    [0],
    [1]
]
#this function will form the density matrix from given states
def density(*states):
    composite=states[0]
    if len(states)>1:
        for s in range(len(states)-1):
            composite=np.kron(composite,states[s+1])
    return composite * np.transpose(np.conjugate(composite))

#this function will visualize the density matrix of given state or density
def density_visualize(array):
    pass


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
    return np.trace(np.transpose(np.conjugate(A))*B)

#This function will return bloch vector given the density matrix or the state
def bloch_vector(array,visualize=True):
    if np.ndim(array)==1:
        array=density(array)

    if np.ndim(array)>2:
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


#this function will compute the reduces states of subsystems in a composite system
def reduce(density,reducing='1'):
    global popped

    check_density(density)

    reducing = "".join(sorted(str(reducing)))

    n_qubits = np.log(np.shape(density)[0]) / np.log(2)
    qubits = ''.join(str(i+1) for i in range(n_qubits))
    op0 = np.zeros(n_qubits)
    op1 = np.zeros(n_qubits)

    if int(max(reducing))>n_qubits:
        raise Exception("the desired system out of range!")

    for i in range(n_qubits):
        if str(i+1) not in reducing:
            op0[i]=s0
            op1[i]=s1
            popped=i+1
            break

    #make kron operation
    reduced0 = np.dot( kron_all(op0) , np.dot( density , np.transpose(kron_all(op0))))
    reduced1 = np.dot( kron_all(op1) , np.dot( density , np.transpose(kron_all(op1))))
    reduced = reduced0 + reduced1

    qubits.replace(str(popped), '')   #this is the current reduces quibits you have

    if qubits != reducing:
        reduce(reduced,reducing=qubits)

    return reduced

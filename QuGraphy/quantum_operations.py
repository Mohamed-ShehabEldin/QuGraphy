import numpy as np
from numpy.random import randint
import scipy.optimize
from qiskit import *

pii = np.pi


def par_of_unitary(unitary, message=False):
    '''
    Given a Unitary matrix, this function will return the angles that decompose it into
     rotation around z multiplied by a rotation around x multiplied by a rotation around z
     :param unitary: the desired unitary matrix
     :return: the equivlent angles of rotation around z then x then z.
    '''
    unitary = np.array(unitary)

    re_u00 = np.real(unitary[0][0])  # real part of first entry of unitary matrix
    im_u00 = np.imag(unitary[0][0])  # imaginary part of first entry of unitary matrix
    re_u01 = np.real(unitary[0][1])
    im_u01 = np.imag(unitary[0][1])
    re_u10 = np.real(unitary[1][0])
    im_u10 = np.imag(unitary[1][0])
    re_u11 = np.real(unitary[1][1])
    im_u11 = np.imag(unitary[1][1])

    def equations(p):  # this is the set of equation came from equating the parameterized form with the given matrix
        a, b, c, f = p  # f is the phase, a,b,c are beta, gamma, delta

        f1 = (np.cos((-a - c + 2 * f) / 2) * np.cos(b / 2) - re_u00)
        f2 = (np.sin((-a - c + 2 * f) / 2) * np.cos(b / 2) - im_u00)
        f3 = (np.cos((-a + c + 2 * f + 3 * pii) / 2) * np.sin(b / 2) - re_u01)
        f4 = (np.sin((-a + c + 2 * f + 3 * pii) / 2) * np.sin(b / 2) - im_u01)
        f5 = (np.cos((a - c + 2 * f + 3 * pii) / 2) * np.sin(b / 2) - re_u10)
        f6 = (np.sin((a - c + 2 * f + 3 * pii) / 2) * np.sin(b / 2) - im_u10)
        f7 = (np.cos((a + c + 2 * f) / 2) * np.cos(b / 2) - re_u11)
        f8 = (np.sin((a + c + 2 * f) / 2) * np.cos(b / 2) - im_u11)

        return np.asarray((f1, f2, f3, f4, f5, f6, f7, f8, f8))

    # solving this set as homogoneus equation: f1=0,f2=0,...
    x = scipy.optimize.leastsq(equations, np.asarray((pii / 2, pii / 2, pii / 2, pii / 2)))[0]

    if message:
        print("The given unitary can be expressed as Rz({alpha})*Rx({beta})*Rz({gamma})*GlobalPhase({phi}))"
              .format(alpha=x[0], beta=x[1], gamma=x[2], phi=x[3]))
        print("Matching Error: ", equations(x))

    return x


def gate_to_matrix(gate_data):  # gate data : qc.data[gate_number],
    '''
    :param gate_data: the desired gate object, qc.data[gate_number]
    :return: the corresponding unitary
    '''

    # this convey the regester and all gate information inside a circuit.
    gate_object = gate_data[0]  # gate info
    register_object = gate_data[1]  # register info, I.E target and control

    qc = QuantumCircuit(len(register_object))  # making new quantum circuit to get its equivlent unitary

    qc.append(gate_object, list(range(len(register_object))))  # adding the gate to the new circuit
    backend = Aer.get_backend('unitary_simulator')
    unitary = execute(qc, backend).result().get_unitary()  # extract its equivlent unitary
    return unitary
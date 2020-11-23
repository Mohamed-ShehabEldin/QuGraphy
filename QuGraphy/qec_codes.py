from qiskit import *

def steane_encode(a,b):
    '''
    given the qubit state, this function will encode this state into steane code, returnign the encoding circuit
    :param a: the amplitude of |0>
    :param b:  the amplitude of |1>
    :return: the steane encoding circuit for given qubit, the qubit encoded in the 7th register
    '''
    qc=QuantumCircuit(7)
    qc.initialize([a,b], 6)
    qc.cx(6,[5,4])
    qc.h([0,1,2])
    qc.cx(0,[3,5,6])
    qc.cx(1,[3,4,6])
    qc.cx(2,[3,4,5])
    qc.name="Steane Encode"
    return qc
    #join it to main circuit by append

#decode
def steane_decode():
    '''

    :return: the decoding circuit for steane code (reverse encoding),the qubit decoded in the 7th register
    '''
    qc=QuantumCircuit(7)
    qc.cx(2,[3,4,5])
    qc.cx(1,[3,4,6])
    qc.cx(0,[3,5,6])
    qc.h([0,1,2])
    qc.cx(6,[5,4])
    qc.name="Steane Decode"
    return qc
    #join it to main circuit by append


###########OLD#######
# recovery
def Steane_recover(qc, code_reg, ancilla_reg):
    '''
    this function will prepare the stabilizer measurement and take the consequent conditional error recovery gates
    :param qc: quantum circuit including code and and recovery/ancilla register
    :param code_reg: the range where the steane code exist
    :param ancilla_reg: the range where tha ancilla exist
    :return: it attaches the recovery code to the given circuit
    '''

    # bit flip syndrom measurment
    c = list(code_reg)
    a = ancilla_reg
    print(c)

    qc.cx([c[0], c[2], c[4], c[6]], a[0])  # ZIZIZIZ  #1,3,5,7
    qc.cx([c[1], c[2], c[5], c[6]], a[1])  # IZZIIZZ  #2,3,6,7
    qc.cx([c[0], c[1], c[2], c[3]], a[2])  # ZZZZIII  #3,4,5,6

    # phase phlip error
    qc.h([a[3], a[4], a[5]])
    qc.cx(a[3], [c[0], c[2], c[4], c[6]])  # XIXIXIX  #1,3,5,7
    qc.cx(a[4], [c[1], c[2], c[5], c[6]])  # IXXIIXX  #2,3,6,7
    qc.cx(a[5], [c[0], c[1], c[2], c[3]])  # XXXXIII  #4,5,6,7
    qc.h([a[3], a[4], a[5]])

    # Measuring stabilizers
    cL = ClassicalRegister(6)  # instead of 6
    qc.add_register(cL)

    qc.measure(ancilla_reg, cL)

    qc.x(c[0]).c_if(cL, 5)
    qc.x(c[1]).c_if(cL, 6)
    qc.x(c[2]).c_if(cL, 7)
    qc.x(c[3]).c_if(cL, 4)
    qc.x(c[4]).c_if(cL, 1)
    qc.x(c[5]).c_if(cL, 2)
    qc.x(c[6]).c_if(cL, 3)

    qc.z(c[0]).c_if(cL, 40)
    qc.z(c[1]).c_if(cL, 48)
    qc.z(c[2]).c_if(cL, 56)
    qc.z(c[3]).c_if(cL, 32)
    qc.z(c[4]).c_if(cL, 8)
    qc.z(c[5]).c_if(cL, 16)
    qc.z(c[6]).c_if(cL, 24)

    qc.y(c[0]).c_if(cL, 45)
    qc.y(c[1]).c_if(cL, 54)
    qc.y(c[2]).c_if(cL, 63)
    qc.y(c[3]).c_if(cL, 64)
    qc.y(c[4]).c_if(cL, 9)
    qc.y(c[5]).c_if(cL, 18)
    qc.y(c[6]).c_if(cL, 27)

#applying transversal c not
def trans_cx(qc,c_range, t_range):
    '''
    apply transversal CNOT
    :param qc: the overall quantum circuit to apply transversal CNOT on
    :param c_range: the range of control registers
    :param t_range:  the range of target register
    :return: it attach the transversal CNOT the given circuit
    '''
    for i in range(len(c_range)):
        qc.cx(c_range[i],t_range[i])
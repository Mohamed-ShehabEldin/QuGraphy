#this file will contain function that related to vector state

from QuGraphy.density import *    #we may use some functions from them and dependencies

def check_state(state):
    if np.ndim(state)>1:
        raise Exception("invalid state, not a vector!")

    if np.transpose(np.conjugate(state))*state !=1:
        raise Exception("invalid state, not normalized!")
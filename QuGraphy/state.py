#this file will contain function that related to vector state

from .density import *    #we may use some functions from them and dependencies


def row2col(vec):
    if np.ndim(vec)==1:
        col=[]
        for element in vec:
            col.append([element])
        return col
    else:
        return vec

def check_state(state):
    row2col(state)
    if np.shape(state)[1]>1:
        raise Exception("invalid state, not a vector!")

    if schmidt_inner(state,state) !=1:
        raise Exception("invalid state, not normalized!")
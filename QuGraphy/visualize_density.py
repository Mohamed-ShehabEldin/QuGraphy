from QuGraphy.density import *
from QuGraphy.state import *
import itertools

def visualize_density(array, check=False):
    if np.ndim(array)[1]==1:
        if check==True: check_state(array)
        rho=density(array)
    else:
        if check==True: check_density(array)
        rho=array

    x = np.array(range(0,shape(rho)[0]), float)
    y = x.copy()
    z=np.array(rho)

    xpos, ypos = np.meshgrid(x, y)
    xpos = xpos.flatten()
    ypos = ypos.flatten()

    zpos = np.zeros_like(xpos)

    dx = 0.3 * np.ones_like(zpos)
    dy = dx.copy()
    dz = z.flatten()

    reals = [item.real for item in dz]
    positive_reals = [0 if i < 0 else np.abs(i) for i in reals]
    nigative_reals = [0 if i > 0 else np.abs(i) for i in reals]
    reals_abs = np.abs(reals)

    imags = [item.imag for item in dz]
    positive_imags = [0 if i < 0 else np.abs(i) for i in imags]
    nigative_imags = [0 if i > 0 else np.abs(i) for i in imags]

    fig = plt.figure(figsize=(7, 7), tight_layout=True, constrained_layout=True)

    ax = fig.add_subplot(111, projection="3d")

    ax.bar3d(xpos, ypos, zpos, dx, dy, positive_reals, color=['blue'] * len(zpos), edgecolor='black', alpha=0.8)
    ax.bar3d(xpos, ypos, zpos, dx, dy, nigative_reals, color=['red'] * len(zpos), edgecolor='black', alpha=0.8)
    ax.bar3d(xpos, ypos, reals_abs, dx, dy, positive_imags, color=['lightblue'] * len(zpos), edgecolor='black', alpha=0.4)
    ax.bar3d(xpos, ypos, reals_abs, dx, dy, nigative_imags, color=['lightcoral'] * len(zpos), edgecolor='black', alpha=0.4)

    colors = {'Real Positive': 'blue', 'Real Negative': 'red', 'Imaginary Positive': 'lightblue',
              'Imaginary Negative': 'lightcoral'}
    labels = list(colors.keys())
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
    plt.legend(handles, labels)

    ax.set_xticks(range(0, np.shape(rho)[0]))
    ax.set_yticks(range(0, np.shape(rho)[0]))

    n_qubits = np.log(np.shape(rho)[0]) / np.log(2)
    bases = list(map(list, itertools.product([0, 1], repeat=n_qubits)))
    for i in range(len(bases)):
        bases[i] = ''.join([str(elem) for elem in bases[i]])

    ax.set_xticklabels(bases)
    ax.set_yticklabels(bases)

    plt.show()
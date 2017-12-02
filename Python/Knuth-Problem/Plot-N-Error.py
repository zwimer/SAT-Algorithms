from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

from tomography import find_error
import time
import signal
import threading
import random
import os

# Generate a random boolean matrix of size y, x
def generate_rand( size ):
    ret = []
    for i in xrange(size[0]):
        tmp = []
        for i in xrange(size[1]):
            tmp.append(int(round(random.random())))
        ret.append(tmp)
    return ret

# Find min size matrix which can't be perfectly reconstructed
def get_error_dist(N, points):

    # Loop 
    err = []
    mx = min( 2**(N**2), points )
    for itr in xrange(mx):
        if itr%20 == 0:
            print itr

        # Generate a random matrix
        mtx = generate_rand( [N, N] )
        err.append(find_error( mtx ))
            
    # Return error
    return err

def plot_err( points = 1000 ):
    
    old_time = time.time()
    x = range(4, 25)
    y = {}
    maxbins = 0
    for i in x:
        print "N = ", i
        y[i] = get_error_dist(i, points)
        maxbins = max(maxbins, max(y[i]))
    maxbins = int(round(maxbins + 1))
    print time.time() - old_time

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    colors = ['r', 'g', 'b', 'y']
    for N in x:

        ys = np.asarray(y[N])
        hist, bins = np.histogram(ys, bins=maxbins, range = [0, max(ys)])
        xs = (bins[:-1] + bins[1:])/2

        c = colors[N % len(colors)]
        ax.bar(xs, hist, zs=N, zdir='y', color = c, ec = c, alpha=1)

    ax.set_xlabel('Error')
    ax.set_ylabel('# of points')
    ax.set_zlabel('# of Occurences')

    plt.show()

# Don't run on imports
if __name__ == '__main__':
    plot_err()

from tomography import find_error
from image import print_image
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
def find_min():

    # Size
    size = [ 5, 5 ];
    print size

    # Loop while err != 0
    err = 0
    while err == 0:

        # Try a bunch of times
        mx = min( 2**(size[0] * size[1]), 100**2 )
        for i in xrange( mx ):

            if i%100 == 0:
                print i

            # Generate a random matrix
            mtx = generate_rand( size )
            [ err, found_s ] = find_error( mtx )

            # If error, try the compliment
            if err != 0:
                for i in mtx:
                    for k in xrange(len(i)):
                        i[k] = 1 - i[k]
                [ err, found_s2 ] = find_error( mtx )
                
                # If error, break
                if err != 0:
                    break

        # If err == 0, increase size
        if err == 0:
            size[0 if size[0] < size[1] else 1] += 1
            print size
            
    # Print info
    print 'Min size matrix found is {} x {}'.format(size[0], size[1])
    print 'Error: ', err
    for i in mtx:
        for k in xrange(len(i)):
            i[k] = 1 - i[k]
    print_image(mtx)
    print "Found "
    print_image(found_s)

    for i in mtx:
        for k in xrange(len(i)):
            i[k] = 1 - i[k]
    print_image(mtx)
    print "Found "
    print_image(found_s2)

# Don't run on imports
if __name__ == '__main__':
    find_min()

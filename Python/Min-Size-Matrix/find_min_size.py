from tomography import find_error
import random

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
    size = [ 1, 1 ];

    # Loop while err != 0
    err = 0
    while err == 0:

        # Try a bunch of times
        mx = min( 2**(size[0] * size[1]), 100**2 )
        for i in xrange( mx ):

            # Generate a random matrix
            mtx = generate_rand( size )
            err = find_error( mtx )

            # Break if error = 0
            if err != 0:
                break

        # If err == 0, increase size
        if err == 0:
            size[0 if size[0] < size[1] else 1] += 1
            print size
            
    # Print info
    print 'Min size matrix found is {} x {}'.format(size[0], size[1])
    print 'Error: ', err
    print mtx

# Don't run on imports
if __name__ == '__main__':
    find_min()

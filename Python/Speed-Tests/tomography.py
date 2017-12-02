import sys, os
import numpy
from scipy.sparse.linalg import lsqr
from image import *

row_sum = 'row_sum'
column_sum = 'column_sum'
diag_sum = 'diag_sum'
antidiag_sum = 'antidiag_sum'
scaled_sum = 'scaled_sum'
x_chunk_size_s = 'x_chunk_size'
y_chunk_size_s = 'y_chunk_size'

# Define the constraints
def solve( sum_constraints ):

    # Define sizes
    n = len(sum_constraints[row_sum])
    m = len(sum_constraints[column_sum])

    # Matricies
    A = []
    bT = []

    # Row constraints
    for i in range(n):
        row = [0] * n*m;
        for k in range(m):
            row[m*i+k] = 1
        A.append(row)
    bT.extend(sum_constraints[row_sum])

    # Define column constraints
    for i in range(m):
        row = [0] * m*n;
        for k in range(n):
            row[k*n+i] = 1
        A.append(row)
    bT.extend(sum_constraints[column_sum])

    # Construct matrix of tuples with value as indicies
    mtx_index = blank_mtx_size(n,m)
    for i in xrange(n):
        for k in xrange(m):
            mtx_index[i][k] = (i,k)

    # Diagonalize it
    diags = diag_mtx(mtx_index)

    # Define diagonal constraints
    to_add = []
    for i in diags:
        row = [0] * n*m;
        for k in i:
            row[k[0]*m+k[1]] = 1
        to_add.append(row)
    A.extend(to_add)
    bT.extend(sum_constraints[diag_sum])

    # Define anti-aiagonal constraints
    to_add.reverse()
    A.extend(to_add)
    bT.extend(sum_constraints[antidiag_sum])

    # Define scaled matrix constraints.
    x = sum_constraints[x_chunk_size_s]
    y = sum_constraints[y_chunk_size_s]
    scaled = section_img(mtx_index, x, y)
    for i in xlen(scaled):
        for k in xlen(scaled[0]):
            row = [0] * n*m;
            for itr in scaled[i][k]:
                row[itr[0]*m+itr[1]] = 1
            A.append(row)
    bT.extend([ i for sub in sum_constraints[scaled_sum] for i in sub ])

    # Solve the problem
    b = numpy.array(bT).transpose();
    A = numpy.matrix(A);
    AT = A.transpose();
    x = lsqr(A, b)[0]
    x = x.tolist()

    # Rounding
    for i in xlen(x):
        x[i] = 0 if x[i] < .5 else 1

    # Create a matrix from the result
    ret = blank_mtx_size(n,m)
    for i in xlen(x):
        ret[i/m][i%m] = x[i]

    # Return the result
    return ret

# Main function
def main():

    # Print usage
    pt = "Usage: ./a.out <Image to test> <x chunk size> <y chunk size>"
    print pt

    # Load an image
    img = load_img(sys.argv[1])
    x_chunk_size = int(sys.argv[2])
    y_chunk_size = int(sys.argv[3])

    # Calculate sums
    print "Calculating sums..."
    sum_constraints = {}
    sum_constraints[row_sum] = calc_row_sums(img)
    sum_constraints[column_sum] = calc_column_sums(img)
    sum_constraints[diag_sum] = calc_diag_sums(img)
    sum_constraints[antidiag_sum] = calc_antidiag_sums(img)
    sum_constraints[scaled_sum] = calc_scaled_sums(img, x_chunk_size, y_chunk_size)
    sum_constraints[x_chunk_size_s] = x_chunk_size
    sum_constraints[y_chunk_size_s] = y_chunk_size

    # Print the image
    print "Input:"
    print_image(img)

    # Save it to the output file
    save_img('Input', 'Input.bmp', img)

    # Print down-scaled image
    print_image(sum_constraints[scaled_sum])
    save_img( None, 'Scaled.bmp', sum_constraints[scaled_sum] )

    # Create the problem and solve it
    print "Creating the problem and solving it; this could take a while..."
    soln = solve(sum_constraints)

    # Print the solution
    print "Output:"
    print_image(soln)

    # Save it to the output file
    save_img('Output', 'Output.bmp', soln)

    # Print error
    err = 0
    for i in xlen(soln):
        for k in xlen(soln[0]):
            if soln[i][k] != img[i][k]:
                err += 1
    err = float(err) / (len(img)*len(img[0])) 
    print '\n{} % error\n'.format(100*err)

# Don't run on imports
if __name__ == '__main__':
    main()

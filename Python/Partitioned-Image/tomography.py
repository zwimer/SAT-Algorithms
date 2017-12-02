import sys, os
import time
from pulp import *
from image import *

row_sum = 'row_sum'
column_sum = 'column_sum'
diag_sum = 'diag_sum'
antidiag_sum = 'antidiag_sum'

# Define the constraints
def define_constraints( prob, xs, sum_constraints ):

    # Define row constraints
    for i in xlen(xs):
        prob += lpSum(xs[i]) == sum_constraints[row_sum][i]

    # Define column constraints
    cols = []
    for i in xlen(xs[0]):
        cols.append([])
    for i in xlen(xs):
        for k in xlen(xs[i]):
            cols[k].append(xs[i][k])
    for i in xlen(cols):
        prob += lpSum(cols[i]) == sum_constraints[column_sum][i]

    # Define diagonal constraints
    diag = diag_mtx(xs)
    for i in xlen(diag):
        prob += lpSum(diag[i]) == sum_constraints[diag_sum][i]

    # Define anti-diagonal constraints
    xs.reverse()
    diag = diag_mtx(xs)
    xs.reverse()
    for i in xlen(diag):
        prob += lpSum(diag[i]) == sum_constraints[antidiag_sum][i]

# Create the IP problem
def create_problem(img, sum_constraints):

    # Create the problem
    prob = LpProblem("Digital Tomography", LpMaximize)

    # Define variables
    xs = blank_mtx(img)
    for i in xlen(img):
        for k in xlen(img[0]):
            xs[i][k] = LpVariable('{},{}'.format(i,k),0,1,LpInteger)
            prob += xs[i][k]

    # No maximization
    prob += 1

    # Define the constraints
    define_constraints( prob, xs, sum_constraints )

    # Return the problem
    return prob

def convert_solution(prob, img):
    vrs = prob.variables()
    ret = blank_mtx(img)
    for i in vrs:
        idx = i.name.split(',')
        if len(idx) == 2:
            [a,b] = [ int(k) for k in idx ]
            ret[a][b] = int(i.varValue)
    return ret

# Run tomography on img
def tomography_on_img( img ):

    # Calculate sums
    sum_constraints = {}
    sum_constraints[row_sum] = calc_row_sums(img)
    sum_constraints[column_sum] = calc_column_sums(img)
    sum_constraints[diag_sum] = calc_diag_sums(img)
    sum_constraints[antidiag_sum] = calc_antidiag_sums(img)

    # Solve it
    prob = create_problem(img, sum_constraints)
    prob.solve()
    return convert_solution(prob, img)

# Combine multiple sub-images together
def combine_images( solutions, img ):
    soln = blank_mtx(img)
    x_chunk_size = len(solutions[0][0])
    y_chunk_size = len(solutions[0])
    num_y_chunks = len(soln) / y_chunk_size
    num_x_chunks = len(soln[0]) / x_chunk_size
    for i_c in xrange(num_y_chunks):
        for k_c in xrange(num_x_chunks):
            for i in xlen(solutions[0]):
                for k in xlen(solutions[0][0]):
                    nxt = solutions[i_c * num_x_chunks + k_c][i][k]
                    soln[i_c*y_chunk_size + i][k_c*x_chunk_size + k] = nxt
    return soln

# Main functions
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

    # Partition the image
    partitioned = section_img(img, x_chunk_size, y_chunk_size)

    # Print the image
    print "Input:"
    print_image(img)
    save_img('Input', 'Input.bmp', img)

    # Tomography each partioned section
    solutions = []
    ln = float(len(partitioned))
    old_time = time.time()
    for i in xlen(partitioned):
        print 'Percent done: {}%'.format(100 * i / ln)
        solutions.append(tomography_on_img(partitioned[i]))

    # Stich images all back together
    soln = combine_images ( solutions, img )
    new_time = time.time()

    # Save it to the output file
    save_img('Output', 'Output.bmp', soln)

    # Print it and the error
    print_image(soln)
    err = 0
    for i in xlen(soln):
        for k in xlen(soln[0]):
            if soln[i][k] != img[i][k]:
                err += 1
    err = float(err) / (len(img)*len(img[0])) 
    print '\n{} % error\n'.format(100*err)

    # Print time
    print 'Time: ', new_time - old_time

# Don't run on imports
if __name__ == '__main__':
    main()

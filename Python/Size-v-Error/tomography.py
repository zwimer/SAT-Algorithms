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
        if ',' in str(lpSum(xs[i])):
            prob += lpSum(xs[i]) == sum_constraints[row_sum][i]

    # Define column constraints
    cols = []
    for i in xlen(xs[0]):
        cols.append([])
    for i in xlen(xs):
        for k in xlen(xs[i]):
            cols[k].append(xs[i][k])
    for i in xlen(cols):
        if ',' in str(lpSum(cols[i])):
            prob += lpSum(cols[i]) == sum_constraints[column_sum][i]

    # Define diagonal constraints
    diag = diag_mtx(xs)
    for i in xlen(diag):
        if ',' in str(lpSum(diag[i])):
            prob += lpSum(diag[i]) == sum_constraints[diag_sum][i]

    # Define anti-diagonal constraints
    xs.reverse()
    diag = diag_mtx(xs)
    xs.reverse()
    for i in xlen(diag):
        if ',' in str(lpSum(diag[i])):
            prob += lpSum(diag[i]) == sum_constraints[antidiag_sum][i]

# Create the IP problem
def create_problem(img, sum_constraints, known):

    # Create the problem
    prob = LpProblem("Digital Tomography", LpMaximize)

    # Define variables
    xs = blank_mtx(img)
    for i in xlen(img):
        for k in xlen(img[0]):
            if known[i][k] is None:
                xs[i][k] = LpVariable('{},{}'.format(i,k),0,1,LpInteger)
                prob += xs[i][k]
            else:
                xs[i][k] = known[i][k]

    # No maximization
    prob += 1

    # Define the constraints
    define_constraints( prob, xs, sum_constraints )

    # Return the problem
    return prob

def convert_solution(prob, img, known):
    vrs = prob.variables()
    ret = known
    for i in vrs:
        idx = i.name.split(',')
        if len(idx) == 2:
            [a,b] = [ int(k) for k in idx ]
            ret[a][b] = int(i.varValue)
    return ret

# Sum elements, ignore all but 1's and 0'
def known_sum(x):
    return sum([i for i in x if i in [0, 1]])

# Returns number of 0, 1 entries
def num_known(x):
    return sum([1 for i in x if i in [0, 1]])

# Signum
def sign(x):
    return 0 if x == 0 else (1 if x > 0 else -1)

# Returns True if we can know
# Second return value, the value items in it should be
# If there is nothing new to learn, returns False
def can_know(c, known):
    new_c = c - known_sum(known)
    new_len = (len(known) - num_known(known))
    return (False, 0) if new_len == 0 else ( new_c in [0, new_len], sign(new_c) )

# Pre-process the constraints
def pre_process( known, sum_constraints ):

    # Preload each part of known with it's coordinates
    for i in xlen(known):
        for k in xlen(known[0]):
            known[i][k] = (i,k)

    # Define the diag and antidiag known matricies
    antidiag_known = antidiag_mtx(known)
    diag_known = diag_mtx(known)

    # Used to keep track of those already checked
    row_did = [ False for i in sum_constraints[row_sum] ]
    column_did = [ False for i in sum_constraints[column_sum] ]
    diag_did = [ False for i in sum_constraints[diag_sum] ]
    antidiag_did = [ False for i in sum_constraints[antidiag_sum] ]

    done = False
    while not done:
        done = True

        # If the row constraints contain any all the same (after accounting for those already known)
        for i in xlen(sum_constraints[row_sum]):
            if not row_did[i]:
                tmp = can_know(sum_constraints[row_sum][i], known[i])
                if tmp[0]:
                    done = False
                    row_did[i] = True
                    for k in xlen(known[i]):
                        if known[i][k] not in [0,1]:
                            known[i][k] = tmp[1]

        # If the column constraints contain any all the same
        for i in xlen(sum_constraints[column_sum]):
            if not column_did[i]:
                tmp = can_know(sum_constraints[column_sum][i], [ j[i] for j in known])
                if tmp[0]:
                    done = False
                    column_did[i] = True
                    for k in xlen(known):
                        if known[k][i] not in [0,1]:
                            known[k][i] = tmp[1]

        # If the diag constraints contain any all the same
        for i in xlen(sum_constraints[diag_sum]):
            if not diag_did[i]:
                tmp = can_know(sum_constraints[diag_sum][i], diag_mtx(known)[i])
                if tmp[0]:
                    done = False
                    diag_did[i] = True
                    for L in diag_known[i]:
                        if known[L[0]][L[1]] not in [0,1]:
                            known[L[0]][L[1]] = tmp[1]

        # If the antidiag constraints contain any all the same
        for i in xlen(sum_constraints[antidiag_sum]):
            if not antidiag_did[i]:
                tmp = can_know(sum_constraints[antidiag_sum][i], antidiag_mtx(known)[i])
                if tmp[0]:
                    done = False
                    antidiag_did[i] = True
                    for L in antidiag_known[i]:
                        if known[L[0]][L[1]] not in [0,1]:
                            known[L[0]][L[1]] = tmp[1]

    # If done, replace all tuples with None's
    for i in xlen(known):
        for k in xlen(known[0]):
            if known[i][k] not in [0,1]:
                known[i][k] = None

# Run tomography on img
def tomography_on_img( img ):

    # Calculate sums
    sum_constraints = {}
    sum_constraints[row_sum] = calc_row_sums(img)
    sum_constraints[column_sum] = calc_column_sums(img)
    sum_constraints[diag_sum] = calc_diag_sums(img)
    sum_constraints[antidiag_sum] = calc_antidiag_sums(img)

    # Pre-process
    known = blank_mtx(img)
    pre_process( known, sum_constraints )

    # Solve it
    prob = create_problem(img, sum_constraints, known)
    prob.solve()
    return convert_solution(prob, img, known)

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

# Find error
def find_error( img ):

    # Calculate sums
    sum_constraints = {}
    sum_constraints[row_sum] = calc_row_sums(img)
    sum_constraints[column_sum] = calc_column_sums(img)
    sum_constraints[diag_sum] = calc_diag_sums(img)
    sum_constraints[antidiag_sum] = calc_antidiag_sums(img)

    # Do it
    soln = combine_images( [tomography_on_img(img)], img )

    # Find error
    err = 0
    for i in xlen(img):
        for k in xlen(img[i]):
            err += 1 if (img[i][k] != soln[i][k]) else 0

    # Result
    return err

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

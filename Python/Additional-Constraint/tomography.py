import sys, os
from pulp import *
from image import *

row_sum = 'row_sum'
column_sum = 'column_sum'
diag_sum = 'diag_sum'
antidiag_sum = 'antidiag_sum'
scaled_sum = 'scaled_sum'
x_chunk_size_s = 'x_chunk_size'
y_chunk_size_s = 'y_chunk_size'

# Define the constraints
def define_constraints( prob, xs, sum_constraints, solve_max ):

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

    # Define scaled matrix constraints.
    x = sum_constraints[x_chunk_size_s]
    y = sum_constraints[y_chunk_size_s]
    const = sum_constraints[scaled_sum]
    scaled = section_img(xs, x, y)
    for i in xlen(scaled):
        for k in xlen(scaled[0]):
            if const[i][k] == 1:
                prob += lpSum(scaled[i][k]) > (x*y)/2
            else:
                prob += lpSum(scaled[i][k]) <= (x*y)/2

# Create the IP problem
def create_problem(img, sum_constraints, solve_max):

    # Create the problem
    prob = LpProblem("Digital Tomography", LpMaximize)

    # Define variables
    xs = blank_mtx(img)
    for i in xlen(img):
        for k in xlen(img[0]):
            xs[i][k] = LpVariable('{},{}'.format(i,k),0,1,LpInteger)
            prob += xs[i][k]

    # Define objective if needed
    if solve_max:
        print "\n*** Optimization ENABLED ***\n"
        obj = []
        for i in xlen(img):
            for k in xlen(img[0]):
                if img[i][k] != 0:
                    obj.append(xs[i][k]);
        prob += lpSum(obj);

    # Otherwise, nothing to maximize
    else:
        prob += 1

    # Define the constraints
    define_constraints( prob, xs, sum_constraints, solve_max )

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

def main():

    # Print usage
    pt = "Usage: ./a.out <Image to test> <x chunk size> <y chunk size>"
    pt += " <Optional arg, put to ignore maximization function>"
    print pt

    # Load an image
    img = load_img(sys.argv[1])
    x_chunk_size = int(sys.argv[2])
    y_chunk_size = int(sys.argv[3])

    # Determine if maxmization should bother
    solve_max = True
    if len(sys.argv) == 4:
        solve_max = False

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

    # Print down-scaled image
    print_image(sum_constraints[scaled_sum])
    save_img( None, 'Scaled.bmp', sum_constraints[scaled_sum] )

    # Create the problem
    print "Creating the problem, adding maxmimization constraint to prove make it better"
    prob = create_problem(img, sum_constraints, solve_max )

    # Solve it
    print "Solving, this could take a while..."
    prob.solve()

    # Convert the solution to an image
    print "Extracting solution..."
    soln = convert_solution(prob, img)

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

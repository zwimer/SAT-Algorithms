import sys, os
from pulp import *
from image import *

# Define the constraints
def define_constraints( prob, xs, row_sum, column_sum, diag_sum, antidiag_sum, solve_max ):

    # Define row constraints
    for i in xlen(xs):
        prob += lpSum(xs[i]) == row_sum[i]

    # Define column constraints
    cols = blank_mtx(xs)
    for i in xlen(xs):
        for k in xlen(xs[i]):
            cols[k][i] = xs[i][k]
    for i in xlen(cols):
        prob += lpSum(cols[i]) == column_sum[i]

    # Define anti-diagonal constraints
    diag = [None] * ( len(xs) - 1 + len(xs[0]) )
    for i in xlen(diag):
        diag[i] = []
    for i in xlen(xs):
        for k in xlen(xs[0]):
            diag[len(xs)-i-1+k].append(xs[i][k])
    for i in xlen(diag):
        prob += lpSum(diag[i]) == antidiag_sum[i]

    # Define diagonal constraints
    xs.reverse()
    diag = [None] * ( len(xs) - 1 + len(xs[0]) )
    for i in xlen(diag):
        diag[i] = []
    for i in xlen(xs):
        for k in xlen(xs[0]):
            diag[len(xs)-i-1+k].append(xs[i][k])
    for i in xlen(diag):
        prob += lpSum(diag[i]) == diag_sum[i]
    xs.reverse()

# Create the IP problem
def create_problem(img, row_sum, column_sum, diag_sum, antidiag_sum, solve_max):

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
        print "Optimization ENABLED"
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
    define_constraints( prob, xs, row_sum, column_sum, diag_sum, antidiag_sum, solve_max )

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
    pt = "Usage: ./a.out <Image to test> "
    pt += "<Optional arg, put to ignore maximization function>"
    print pt

    # Load an image
    img = load_img(sys.argv[1])

    # Determine if maxmization should bother
    solve_max = True
    if len(sys.argv) == 2:
        solve_max = False

    # Print the image
    print "Input:"
    print_image(img)

    # Calculate sums
    print "Calculating sums..."
    row_sum = calc_row_sums(img)
    column_sum = calc_column_sums(img)
    diag_sum = calc_diag_sums(img)
    antidiag_sum = calc_antidiag_sums(img)

    # Create the problem
    print "Creating the problem, adding maxmimization constraint to prove make it better"
    prob = create_problem(img, row_sum, column_sum, diag_sum, antidiag_sum, solve_max )

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
    img = save_img('Output', soln)

# Don't run on imports
if __name__ == '__main__':
    main()

from pulp import *


# Run a simple pulp program to solve:
#   2x + 4y = 3*factor
#   4x + 2y = 3*factor
def code(factor):

    # Create the problem
    prob = LpProblem("Digital Tomography", LpMinimize)

    # Define variables
    x = LpVariable('x1',0,1,LpInteger);
    y = LpVariable('x2',0,1,LpInteger);

    # Define the constraints
    prob += (   2*x + 4*y == 3*factor   );
    prob += (   4*x + 2*y == 3*factor   );

    # Solve it
    prob.solve()

    # Extract results
    # Still not sure why, but pulp puts in a dummy variable
    [ dummy, i, k] = prob.variables()

    # Print results and bounds
    print 'Output: <lower bound>,  <  <var value>,  <  <upper bound>'
    print i.lowBound, ' < ', i.varValue, ' < ', i.upBound
    print k.lowBound, ' < ', k.varValue, ' < ', k.upBound
    print

# Ignore integer constraints example
def ignore_integer_constraint():
    print 'Pulp will ignore integer constraints here'
    code(1)

# Ignore bound constraints example
def ignore_bound_constraint():
    print 'Pulp will ignore bound constraints here'
    code(10)

# Don't run on imports
if __name__ == '__main__':
    ignore_integer_constraint()
    ignore_bound_constraint()

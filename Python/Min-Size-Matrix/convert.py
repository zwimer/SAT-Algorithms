import sys
from fractions import gcd

# This function takes a number and prints the factors
def print_factors(x):
   print("The factors of",x,"are:")
   for i in range(1, x + 1):
       if x % i == 0:
           print(i)

# Read in the file
with open(sys.argv[1]) as f:
    a = [ i for i in f.read().split('\n') if len(i) > 0 ]

# Convert it to 1s and 0s
out = []
for i in a:
    tmp = ''
    for k in i:
        tmp += '0' if k.isspace() else '1'
    out.append(tmp)

ln = max([len(i) for i in out])
# Square it
for i in xrange(len(out)):
    while len(out[i]) < ln:
        out[i] += '0'

# Print factors
print_factors(len(out))
print_factors(len(out[0]))

# Write out
with open(sys.argv[2], 'w') as f:
    f.write('\n'.join(out))

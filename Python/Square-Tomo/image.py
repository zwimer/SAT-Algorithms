def xlen(x):
    return xrange(len(x))

# Make a blank matrix of size the size of img
def blank_mtx(img):
    return blank_mtx_size(xlen(img), xlen(img[0]))

# Make a blank matrix of size the size n x m
def blank_mtx_size(n,m):    
    ret = []
    for i in n:
        tmp = []
        for k in m:
            tmp.append(None)
        ret.append(tmp)
    return ret

# Print an image
# full = '*'      # What is printed if 1
# empty = '.'     # What is printed if 0
def print_image(img, full = '*', empty = ' '):
    delim = '  '    # Delimiter put between each full or empty
    horiz = '-'     # Horizontal boarder line
    vert = '|'      # Vertical boarder line
    print (horiz*3)*(1+len(img[0])) + horiz
    for i in img:
        st = vert + delim
        for k in i:
            st += (full if (k != 0) else empty) + delim
        st += vert
        print st
    print (horiz*3)*(1+len(img[0])) + horiz

# Calculate row sums
def calc_row_sums(img):
    return [ sum(i) for i in img ]

# Calculate column sums
def calc_column_sums(img):
    sms = [0]*len(img[0])
    for i in img:
        for k in xlen(i):
            sms[k] += i[k]
    return sms

# Calculate anti-diagonal sums
def calc_antidiag_sums(img):
    sums = [0]*(len(img) - 1 + len(img[0]))
    for i in xlen(img):
        for k in xlen(img[0]):
            sums[len(img)-i-1+k] += img[i][k]
    return sums

# Calculate the diagonal sums
def calc_diag_sums(img):
    img.reverse()
    tmp = calc_antidiag_sums(img)
    img.reverse()
    return tmp

# Load an image from a file
def load_img(file_name):
    with open(file_name) as f:
        img_tmp = [ i for i in f.read().split('\n') if i ]
    img = []
    for i in xlen(img_tmp):
        img.append([ int(k) for k in img_tmp[i] ])
    return img

# Save an image to a file
def save_img(file_name, img):
    img2 = blank_mtx(img)
    for i in xlen(img):
        img2[i] = ''.join([ str(k) for k in img[i] ])
    with open(file_name, 'w') as f:
        f.write('\n'.join(img2))

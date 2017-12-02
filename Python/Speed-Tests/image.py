from PIL import Image

def xlen(x):
    return xrange(len(x))

# Make a blank matrix of size the size of img
def blank_mtx(img):
    return blank_mtx_size(len(img), len(img[0]))

# Make a blank matrix of size the size n x m
def blank_mtx_size(n,m):    
    ret = []
    for i in xrange(n):
        tmp = []
        for k in xrange(m):
            tmp.append(None)
        ret.append(tmp)
    return ret

# Split an (n,m) image up into (n/y,m/x) sections
# For example:
#  [
#   [ a b c d ]
#   [ e f g h ]
#   [ i j k l ]
#   [ m n o p ]
#  ]
# Becomes:
#  [
#   [ [ a b ; e f ] [ c d ; g h ] ] 
#   [ [ i j ; m n ] [ k l ; o p ] ] 
#  ]
def section_img(img, x, y):

    # Error checking
    n = len(img)
    m = len(img[0])
    if (n%y) or (m%x):
        print "Image of size ({},{}) cannot be sectioned by size x = {}, y = {}".format(n,m,x,y)
        exit()
    
    # Section the image
    ret = []
    for i in xlen(img):
        if (i%y == 0):
            ret.append([])
        for k in xlen(img[0]):
            if (i%y == 0) and (k%x == 0):
                ret[-1].append([])
            ret[-1][int(k/x)].append(img[i][k])
        
    # Return the result
    return ret

# Print an image
# full = u"\u2588"*2    # What is printed if 1
# empty = ' '*2         # What is printed if 0
def print_image(img, full = u"\u2588"*2, empty = ' '*2):
    delim = ''    # Delimiter put between each full or empty
    horiz = '-'     # Horizontal boarder line
    vert = '|'      # Vertical boarder line
    print horiz * (len(delim) + len(full)) * (1 + len(img[0]))
    for i in img:
        st = vert + delim
        for k in i:
            st += (full if (k != 0) else empty) + delim
        st += vert
        print st
    print horiz * (len(delim) + len(full)) * (1 + len(img[0]))

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

# Returns an array of arrays containing the diagonals of a matrix
def diag_mtx(mtx):

    # Locals
    ret = []
    n = len(mtx)
    m = len(mtx[0])

    # Prepare mtx
    for _ in xrange(m+n-1):
        ret.append([])

    # Loop
    for t in xrange(n+m):
        j = 0
        for i in reversed(xrange(t+1)):
            if (i<m) and (j<n):
                ret[t].append(mtx[j][i])
            j += 1

    # Return result
    return ret

# Calculate the diagonal sums
def calc_diag_sums(img):
    return [ sum(i) for i in diag_mtx(img) ]

# Calculate anti-diagonal sums
def calc_antidiag_sums(img):
    img.reverse()
    ret = calc_diag_sums(img)
    img.reverse()
    return ret

# Calculate scaled image sums
# If the number of 1s > x*y/2, then a 1 is put, else 0
def calc_scaled_sums(img, x_chunk_size, y_chunk_size):
    threshold = ( x_chunk_size * y_chunk_size ) / 2;
    scaled = section_img(img, x_chunk_size, y_chunk_size)
    for i in xlen(scaled):
        for k in xlen(scaled[0]):
            sm = sum(scaled[i][k])
            scaled[i][k] = (1 if sm > threshold else 0)
    return scaled

# Load an image from a file
def load_img(file_name):
    with open(file_name) as f:
        img_tmp = [ i for i in f.read().split('\n') if i ]
    img = []
    for i in xlen(img_tmp):
        img.append([ int(k) for k in img_tmp[i] ])
    return img

# Save an image data to a file
# Also saves the image to a file 
def save_img(file_name, bmp_name, img):

    # Save the image data
    if file_name is not None:
        img2 = blank_mtx(img)
        for i in xlen(img):
            img2[i] = ''.join([ str(k) for k in img[i] ])
        with open(file_name, 'w') as f:
            f.write('\n'.join(img2))
    
    # Save the bmp
    bmp = Image.new('1', (len(img), len(img[0])))
    pixels = bmp.load()
    for i in xlen(img):
        for k in xlen(img[0]):
            pixels[i,k] = img[i][k]
    bmp.save(bmp_name)

    # Show the bmp
    bmp.show()

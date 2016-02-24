import sys

#creates a cool gradient image
#dumps the results right to stdout

if __name__ == '__main__':
    nx = 200
    ny = 100

    # Dump header
    print('P3')
    print(str(nx)+' '+str(ny))
    print('255')
    # Make a cool gradient
    for y in xrange(ny-1,-1,-1):
        for x in xrange(nx):
            b = (0.2)*255
            r = (float(x)/float(nx))*255
            g = (float(y)/float(ny))*255
            sys.stdout.write('{r} {g} {b} '.format(r=int(r), g=int(g), b=int(b)))
    print('')

import sys
from tracer.ray import *
from tracer.vec3 import *

# Creates a cool gradient image using the ray class

def color(r):
    """
    Returns a color that is a "blend" of white and blue.
    The amount of blue depends on the y value of the ray given.

    The idea here is that if you gave a ray having a direction
    :param r:
    :return:
    """
    unit_direction = make_unit_vector(r.direction())
    t = 0.5*(unit_direction.y() + 1.0)
    return (1.0 - t)*Vec3(1.0, 1.0, 1.0) + t*Vec3(0.5, 0.7, 1.0)

if __name__ == '__main__':
    nx = 200
    ny = 100

    # Dump header
    print('P3')
    print(str(nx)+' '+str(ny))
    print('255')

    lower_left_corner = Vec3(-2.0, -1.0, -1.0)
    horizontal = Vec3(4.0, 0.0, 0.0)
    vertical = Vec3(0.0, 2.0, 0.0)
    origin = Vec3(0.0, 0.0, 0.0)

    # Make a cool gradient
    for y in xrange(ny-1,-1,-1):
        for x in xrange(nx):
            u = float(x)/float(nx)
            v = float(y)/float(ny)
            r = Ray(origin, lower_left_corner + u*horizontal + v*vertical)
            col = color(r)
            ir = int(255.99*col[0])
            ig = int(255.99*col[1])
            ib = int(255.99*col[2])

            sys.stdout.write('{r} {g} {b} '.format(r=ir, g=ig, b=ib))
    print('')

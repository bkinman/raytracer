import sys
from tracer.ray import *
from tracer.vec3 import *
from tracer.hitable import *
from tracer.sphere import *
from tracer.camera import *
from random import random

# Adding diffusion!
# Also adding gamma correction of 2.0!

def random_point_in_unit_sphere():
    p = Vec3(0, 0, 0)
    p_outside_sphere = True
    while p_outside_sphere:
        p = 2.0*Vec3(random(), random(), random()) - Vec3(1, 1, 1)
        p_outside_sphere = (dot(p, p) >= 1.0)
    return p

def color(r, world):
    """
    Returns a color that is a "blend" of white and blue.
    The amount of blue depends on the y value of the ray given.

    The idea here is that if you gave a ray having a direction
    :param r:
    :return:
    """
    hit, rec = world.hit(r, 0.0, sys.float_info.max)
    if hit:
        target = rec.p + rec.normal + random_point_in_unit_sphere()
        return 0.5*color(Ray(rec.p, target - rec.p), world)
    else:
        unit_direction = make_unit_vector(r.direction())
        t = 0.5*(unit_direction.y() + 1.0)
        return (1.0 - t)*Vec3(1.0, 1.0, 1.0) + t*Vec3(0.5, 0.7, 1.0)

if __name__ == '__main__':
    nx = 200
    ny = 100
    ns = 30

    # Dump header
    print('P3')
    print(str(nx)+' '+str(ny))
    print('255')

    lower_left_corner = Vec3(-2.0, -1.0, -1.0)
    horizontal = Vec3(4.0, 0.0, 0.0)
    vertical = Vec3(0.0, 2.0, 0.0)
    origin = Vec3(0.0, 0.0, 0.0)

    world = HitableList()
    cam = Camera()

    small_sphere = Sphere(Vec3(0, 0, -1), 0.5)
    big_sphere = Sphere(Vec3(0, -100.5, -1), 100)
    world.append(small_sphere)
    world.append(big_sphere)

    # Make a cool gradient
    for y in xrange(ny-1,-1,-1):
        for x in xrange(nx):
            col = Vec3(0, 0, 0)
            for s in xrange(ns):
                u = (float(x)+random())/float(nx)
                v = (float(y)+random())/float(ny)
                r = cam.get_ray(u, v)
                col += color(r, world)
            col /= float(ns)
            #Gamma correction
            col = Vec3(sqrt(col[0]), sqrt(col[1]), sqrt(col[2]))
            ir = int(255.99*col[0])
            ig = int(255.99*col[1])
            ib = int(255.99*col[2])

            sys.stdout.write('{r} {g} {b} '.format(r=ir, g=ig, b=ib))
    print('')

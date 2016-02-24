import sys
from tracer.ray import *
from tracer.vec3 import *
from tracer.hitable import *
from tracer.sphere import *
from tracer.camera import *
from tracer.materials import *
from random import random

# Now, with 100% more Materials!


def color(r, world, depth):
    hit, rec = world.hit(r, 0.001, sys.float_info.max)
    if hit:
        if depth < 50:
            was_scattered, atten, scattered = rec.material.scatter(r, rec)
            if was_scattered:
                col = color(scattered, world, depth+1)
                return atten*col
        return Vec3(0.0, 0.0, 0.0)
    else:
        unit_direction = make_unit_vector(r.direction())
        t = 0.5*(unit_direction.y() + 1.0)
        # Returns a color that is a "blend" of white and blue.
        # The amount of blue depends on the y value of the ray given.
        return (1.0 - t)*Vec3(1.0, 1.0, 1.0) + t*Vec3(0.5, 0.7, 1.0)


def main(filename):
    nx = 2000
    ny = 1000
    ns = 300

    file = open(filename, 'w')

    # Dump header
    file.write('P3\n')
    file.write(str(nx)+' '+str(ny)+'\n')
    file.write('255\n')

    world = HitableList()
    cam = Camera()

    small_sphere = Sphere(Vec3(0, 0, -1), 0.5, Lambertian(Vec3(0.8, 0.3, 0.3)))
    big_sphere = Sphere(Vec3(0, -100.5, -1), 100, Lambertian(Vec3(0.8, 0.8, 0.0)))
    another_sphere = Sphere(Vec3(1, 0, -1), 0.5, Metal(Vec3(0.8, 0.6, 0.2), 1.0))
    last_sphere = Sphere(Vec3(-1, 0, -1), 0.5, Metal(Vec3(0.8, 0.8, 0.8), 0.3))

    world.append(small_sphere)
    world.append(big_sphere)
    world.append(another_sphere)
    world.append(last_sphere)

    # Make a cool gradient
    for y in xrange(ny-1, -1, -1):
        for x in xrange(nx):
            col = Vec3(0, 0, 0)
            for s in xrange(ns):
                u = (float(x)+random())/float(nx)
                v = (float(y)+random())/float(ny)
                r = cam.get_ray(u, v)
                col += color(r, world, 0)
            col /= float(ns)
            # Gamma correction
            col = Vec3(sqrt(col[0]), sqrt(col[1]), sqrt(col[2]))
            ir = int(255.99*col[0])
            ig = int(255.99*col[1])
            ib = int(255.99*col[2])

            file.write('{r} {g} {b} '.format(r=ir, g=ig, b=ib))
        print('Percent done: '+str((ny-y)/(1.0*ny)*100))
    file.write('\n')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Must specify an output filename.')
    else:
        main(sys.argv[1])

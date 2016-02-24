import sys
from tracer.ray import *
from tracer.vec3 import *
from tracer.hitable import *
import math

# Add a sphere to the cool gradient image


def hit_sphere(center, radius, ray):
    """
    This is not an obvious function at all.
    I was able to mathematically derive it, but it was
    very much not intuitive, is all of graphics going to be this way?
    Essentially, I was able to form the equation, but not easily able
    to forulate it as a vector equation using dot products.

    :param center: Center of the sphere
    :param radius: Radius of the sphere
    :param r: The ray
    :return: True if the ray hits the sphere
    """
    oc = ray.origin() - center
    a = dot(ray.direction(), ray.direction())
    b = 2*dot(oc, ray.direction())
    c = dot(center, center) - radius*radius
    discriminant = b*b -4*a*c
    if discriminant > 0:
        return (-b - math.sqrt(discriminant))/(2.0*a)
    else:
        return -1


def color(ray):
    """
    Returns a color that is a "blend" of white and blue.
    The amount of blue depends on the y value of the ray given.

    The idea here is that if you gave a ray having a direction
    :param r:
    :return:
    """
    sphere_center = Vec3(0, 0, -1)
    t = hit_sphere(sphere_center, 0.5, r)
    if t > 0:
        norm = make_unit_vector(ray.point_at_parameter(t) - sphere_center)
        return 0.5*Vec3(norm.x()+1, norm.y()+1, norm.z()+1)
    unit_direction = make_unit_vector(ray.direction())
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

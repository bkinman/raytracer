from vec3 import *
from random import random


def random_point_in_unit_sphere():
    p = Vec3(0, 0, 0)
    p_outside_sphere = True
    while p_outside_sphere:
        p = 2.0*Vec3(random(), random(), random()) - Vec3(1, 1, 1)
        p_outside_sphere = (dot(p, p) >= 1.0)
    return p


def schlick(cosine, ref_idx):
    r0 = (1.0-ref_idx)/(1.0+ref_idx)
    r0 *= r0
    return r0 + (1.0-r0)*(1.0-cosine)**5

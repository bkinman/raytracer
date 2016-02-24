from hitable import *
from vec3 import *
from math import sqrt


class Sphere(Hitable):
    def __init__(self, center=Vec3(0, 0, 0), radius=1, material=None):
        self.center = center
        self.radius = float(radius)
        self.material = material

    def hit(self, ray, t_min, t_max):
        hit_record = HitRecord()
        oc = ray.origin() - self.center
        a = dot(ray.direction(), ray.direction())
        b = dot(oc, ray.direction())
        c = dot(oc, oc) - self.radius*self.radius
        discriminant = b*b - a*c

        if discriminant > 0:
            # A hit means that the the quadratic has one of the two solutions
            hit_record.material = self.material
            temp = (-b - sqrt(b*b - a*c))/a
            if t_min < temp < t_max:
                hit_record.t = temp
                hit_record.p = ray.point_at_parameter(temp)
                hit_record.normal = (hit_record.p - self.center)/self.radius
                return True, hit_record
            temp = (-b + sqrt(b*b - a*c))/a
            if t_min < temp < t_max:
                hit_record.t = temp
                hit_record.p = ray.point_at_parameter(temp)
                hit_record.normal = (hit_record.p - self.center)/self.radius
                return True, hit_record
        return False, None

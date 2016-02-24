from vec3 import *
from ray import *
import math


class Camera(object):
    def __init__(self, look_from, look_at, vup, vertical_fov, aspect_ratio):
        """
        Represents a camera in the scene.
        :param look_from: Position the camera is looking from
        :param look_at: Position the camera is looking at
        :param vup: No fucking idea
        :param vertical_fov: Vertical field of view (degrees)
        :param aspect_ratio: Height to width ratio
        :return:
        """
        theta = vertical_fov * math.pi/180
        half_height = math.tan(theta/2)
        half_width = aspect_ratio * half_height

        w = make_unit_vector(look_from - look_at)
        u = make_unit_vector(cross(vup, w))
        v = cross(w, u)

        self.origin = look_from
        self.lower_left_corner = self.origin - half_width*u - half_height*v - w
        self.horizontal = 2.0*half_width*u
        self.vertical = 2.0*half_height*v

    def get_ray(self, u, v):
        origin = self.origin
        direction = self.lower_left_corner + u*self.horizontal + v*self.vertical - self.origin
        return Ray(origin, direction)

from vec3 import Vec3


class Ray(object):
    def __init__(self, a=Vec3(), b=Vec3()):
        self.A = a
        self.B = b

    def origin(self): return self.A

    def direction(self): return self.B

    def point_at_parameter(self, t): return self.A + t*self.B

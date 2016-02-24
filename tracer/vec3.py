import numpy as np
from math import sqrt


def make_unit_vector(v1): return v1/v1.length()


def dot(v1, v2):
    return float(np.dot(v1.v.transpose(), v2.v))


def cross(v1, v2):
    return Vec3.from_np_arr(np.cross(v1.v.transpose(), v2.v.transpose()).transpose())


def reflect(vector, norm):
    return vector - 2.0*dot(vector, norm)*norm

def refract(vector, norm, ni_over_nt):
    """
    Compute the refraction vector using Snell's Law
    I must admit, it was pretty hard to justify exactly how the following
    code works. It's very much not easy to follow. The following link really
    helps: http://graphics.stanford.edu/courses/cs148-10-summer/docs/2006--degreve--reflection_refraction.pdf
    :param vector: Vector of incident ray
    :param norm: normal vector
    :param ni_over_nt: The ratio of indices of refraction (snell's law)
    :return: Refracted vector, if solution exists, None otherwise.
    """
    refracted = None
    uv = make_unit_vector(vector)
    norm = make_unit_vector(norm)
    dt = dot(uv, norm)
    discriminant = 1.0 - ni_over_nt*ni_over_nt*(1 - dt*dt)
    if discriminant > 0:
        refracted = ni_over_nt*(uv - norm*dt) - norm*sqrt(discriminant)
    return refracted


class Vec3(object):
    """
    A simple vector class. As you can see, much of the functionality here simply
    is simply operating on a numpy array. Rather than just doing this, I'm wondering
    if it would perhaps make more sense to just subclass a numpy array? I'm pretty
    sure that this would result in faster execution of code based on Vec3.
    """
    def __init__(self, v0=0, v1=0, v2=0):
        self.v = np.array([[v0], [v1], [v2]], dtype=float)

    @classmethod
    def from_np_arr(self, arr):
        result = Vec3(float(arr[0]), float(arr[1]), float(arr[2]))
        return result

    def x(self): return float(self.v[0])

    def y(self): return float(self.v[1])

    def z(self): return float(self.v[2])

    def r(self): return float(self.v[0])

    def g(self): return float(self.v[1])

    def b(self): return float(self.v[2])

    # Operator overloading

    def __pos__(self): return self

    def __neg__(self): return Vec3.from_np_arr(-self.v)

    def __getitem__(self, item): return self.v[item]

    def __add__(self, other): return Vec3.from_np_arr(self.v + other.v)

    def __sub__(self, other): return Vec3.from_np_arr(self.v - other.v)

    def __mul__(self, other):
        if type(other) is np.ndarray or type(other) is float:
            return Vec3.from_np_arr(self.v * other)
        elif type(other) is Vec3:
            return Vec3.from_np_arr(self.v * other.v)
        else:
            raise RuntimeError('Vec3.__mul__ passed incorrect types')

    __rmul__ = __mul__

    def __div__(self, other):
        if type(other) is np.ndarray:
            return Vec3.from_np_arr(self.v / other.v)
        else:
            return Vec3.from_np_arr(self.v / other)

    def length(self):
        return np.linalg.norm(self.v)

    def squared_length(self):
        return np.sum(self.v*self.v)


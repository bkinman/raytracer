import abc
from ray import *


class HitRecord(object):
    def __init__(self):
        self.t = float(0)
        self.p = Vec3(0, 0, 0)
        self.normal = Vec3(0, 0, 0)
        self.material = None


class Hitable(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def hit(self, ray, t_min, t_max):
        """
        Determines if they ray has hit the Hitable object within the time interval [t_min, t_max].
        The hit_record will be set in the circumstance that the object was hit
        :param ray: The ray
        :param t_min: the minimal time before which no hit will be registered
        :param t_max: the maximal time after which no hit will be registered
        :param hit_record: The hit record that will be completed if the object was hit
        :return: True if the object was hit, false otherwise
        """
        return False, None


class HitableList(list, Hitable):
    """ A hitable object, holding a list of hitable objects, returning a the
        closest hit.
    """
    def __init__(self):
        return

    def hit(self, ray, t_min, t_max):
        temp_rec = None
        hit_anything = False
        closest_so_far = t_max

        for hitable_item in self:
            hit, rec = hitable_item.hit(ray, t_min, closest_so_far)
            if hit:
                hit_anything = True
                temp_rec = rec
                closest_so_far = temp_rec.t

        return hit_anything, temp_rec


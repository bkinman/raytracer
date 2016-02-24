import abc
from utils import *
from ray import *
from random import random

class Material(object):
    ___metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def scatter(self, r_in, hit_record):
        return None, None, None


class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, r_in, hit_record):
        target = hit_record.p + hit_record.normal + random_point_in_unit_sphere()
        scattered = Ray(hit_record.p, target - hit_record.p)
        attenuation = self.albedo
        return True, attenuation, scattered


class Metal(Material):
    def __init__(self, albedo, fuzz):
        self.albedo = albedo
        if fuzz > 1:
            fuzz = 1
        self.fuzz = fuzz

    def scatter(self, r_in, hit_record):
        reflected = reflect(make_unit_vector(r_in.direction()), hit_record.normal)
        scattered = Ray(hit_record.p, reflected + self.fuzz*random_point_in_unit_sphere())
        attenuation = self.albedo
        did_scatter = dot(scattered.direction(), hit_record.normal) > 0
        return did_scatter, attenuation, scattered


class Dielectric(Material):
    def __init__(self, ref_idx):
        """
        A dielectric is a material that refracts.
        :param ref_idx: Index of refraction
        """
        self.ref_idx = ref_idx

    def scatter(self, r_in, hit_record):
        reflected = reflect(r_in.direction(), hit_record.normal)
        attenuation = Vec3(1.0, 1.0, 1.0)

        if dot(r_in.direction(), hit_record.normal) > 0:
            # We are hitting the interface from the dielectric side
            outward_normal = -hit_record.normal
            ni_over_nt = self.ref_idx
            cosine = self.ref_idx * dot(r_in.direction(), hit_record.normal) / r_in.direction().length()
        else:
            # We are hitting the interface from the air side
            outward_normal = hit_record.normal
            ni_over_nt = 1.0/self.ref_idx
            cosine = -dot(r_in.direction(), hit_record.normal) / r_in.direction().length()

        refracted = refract(r_in.direction(), outward_normal, ni_over_nt)
        if refracted:
            reflect_prob = schlick(cosine, self.ref_idx)
            # scattered = Ray(hit_record.p, refracted)
        else:
            # If it didn't refract, it reflected
            reflect_prob = 1.0
            # scattered = Ray(hit_record.p, reflected)
            # return False, attenuation, scattered
        if random() < reflect_prob:
            scattered = Ray(hit_record.p, reflected)
        else:
            scattered = Ray(hit_record.p, refracted)

        return True, attenuation, scattered

from math import radians
from math import tan


class ProjectionEstimator:

    # Should only range between 0 and 180 degrees or 0 to pi radians exclusive.
    _FOV = radians(120)

    def __init__(self, supported_objects, object_size_mapping):
        self._supported_objects = supported_objects
        self._object_size_mapping = object_size_mapping

    def estimate_depth(self, bound_box, class_type_index, im_width):
        """
        Estimates the distance of the actual 3D object from the camera, i.e the depth.

        :param bound_box: List of size 4, [x_start, y_start, x_end, y_end].
        :param class_type_index: Index to the name of the object category (chair, couch).
        :param im_width: Width of the image.
        :return: Classification of the object and the estimated depth.
        """
        # Derivation of this is shown in the dissertation paper.
        phi = self._FOV / 2
        focal_length = im_width / (2 * tan(phi))
        bound_width = bound_box[2] - bound_box[0]
        class_name = self._supported_objects[class_type_index]

        if class_name in self._object_size_mapping:
            default_width = self._object_size_mapping[class_name]
        else:
            return None, 0

        # Derivation of this is shown in the dissertation paper.
        depth = focal_length * default_width / bound_width

        return class_name, depth

    def estimate_x_displacement_from_center(self, depth, pos_x, im_width):
        """
        Estimates the x displacement from the center ray that goes through the camera, the
        center of the image plane, along the 3D world.

        :param depth: The distance from the image plane along the z-axis.
        :param pos_x: The x position of the center of the object on the image plane.
        :param im_width: Width of the image.
        :return: The displacement along the x axis from the central ray.
        """
        # Derivation of this is shown in the dissertation paper.
        phi = self._FOV / 2
        focal_length = im_width / (2 * tan(phi))
        # Derivation of this is shown in the dissertation paper.
        x_displacement = depth * ((pos_x - (im_width / 2)) / focal_length)

        return x_displacement

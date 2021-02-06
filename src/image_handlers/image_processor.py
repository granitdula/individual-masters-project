import cv2 as cv

from src.image_handlers.projection_estimator import ProjectionEstimator
from src.image_handlers.rcnn_segmenter import RCNNSegmenter


class ImageProcessor:

    _SEGMENT_ACC_THRESHOLD = 0.5

    def __init__(self):
        self._rcnn = RCNNSegmenter(self._SEGMENT_ACC_THRESHOLD)
        self._projection_estimator = ProjectionEstimator(self._rcnn.get_supported_classifications(),
                                                         self._rcnn.get_object_size_mapping())

    def process_image(self, image):
        """
        Segments the identifiable objects in the image into instances. Then it estimates
        projection related values for each of the instances and returns the data for all
        instances.

        :param image: OpenCV image.
        :return: List of tuples which contain data for the instance including: class name,
                 depth and x displacement.
        """
        segmented_image = self._rcnn.segment_image(image)
        instances = segmented_image["instances"]

        bounding_boxes, category_indices = instances.pred_boxes.tensor, instances.pred_classes
        image_width = instances.pred_masks.shape[2]
        all_instance_estimations = []

        for i in range(len(instances.pred_classes)):
            center_x = int(bounding_boxes[i][0] + ((bounding_boxes[i][2] - bounding_boxes[i][0]) / 2))
            class_name, depth = self._projection_estimator.estimate_depth(bounding_boxes[i],
                                                                          category_indices[i],
                                                                          image_width)
            if class_name:
                x_displacement = self._projection_estimator.estimate_x_displacement_from_center(
                                                                          depth, center_x,
                                                                          image_width)

                instance_data = (class_name, depth, x_displacement)
                all_instance_estimations.append(instance_data)

        # TODO: Remove this once the full pipeline is implemented.
        self._rcnn.visualise_segmentation(image)
        _ = cv.waitKey(0)

        return all_instance_estimations

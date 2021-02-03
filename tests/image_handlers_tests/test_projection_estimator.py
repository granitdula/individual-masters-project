from math import radians
from math import tan

from src.image_handlers.projection_estimator import ProjectionEstimator


_SUPPORTED_CLASSIFICATIONS = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck",
    "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
    "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra",
    "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis",
    "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
    "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork", "knife",
    "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot",
    "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed",
    "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard",
    "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book",
    "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
]

_OBJECT_WIDTH_MAPPING = {"chair": 1, "couch": 2}

projection_estimator = ProjectionEstimator(_SUPPORTED_CLASSIFICATIONS, _OBJECT_WIDTH_MAPPING)


# Utility functions.
def _estimate_depth(bound_box, image_width, class_name):
    # Uses formula as derived in dissertation report.
    phi = radians(120) / 2
    focal_length = image_width / (2 * tan(phi))
    bound_width = bound_box[2] - bound_box[0]
    default_width = _OBJECT_WIDTH_MAPPING[class_name]

    depth = focal_length * default_width / bound_width

    return depth


def _estimate_x_displacement_from_center(depth, pos_x, im_width):
    # Uses formula as derived in dissertation report.
    phi = radians(120) / 2
    focal_length = im_width / (2 * tan(phi))
    x_displacement = depth * ((pos_x - (im_width / 2)) / focal_length)

    return x_displacement


# Tests
def test_estimate_depth_for_nearby_chair_in_a_large_image_width():
    class_index = _SUPPORTED_CLASSIFICATIONS.index("chair")
    bound_box = [100, 300, 1100, 1400]
    image_width = 1920

    expected_depth = _estimate_depth(bound_box, image_width, "chair")
    class_name, depth = projection_estimator.estimate_depth(bound_box, class_index, image_width)

    assert (class_name == "chair" and depth == expected_depth)


def test_estimate_depth_for_far_away_chair_in_a_large_image_width():
    class_index = _SUPPORTED_CLASSIFICATIONS.index("chair")
    bound_box = [900, 1300, 950, 1375]
    image_width = 1920

    expected_depth = _estimate_depth(bound_box, image_width, "chair")
    class_name, depth = projection_estimator.estimate_depth(bound_box, class_index, image_width)

    assert (class_name == "chair" and depth == expected_depth)


def test_estimate_depth_for_nearby_chair_in_a_small_image_width():
    class_index = _SUPPORTED_CLASSIFICATIONS.index("chair")
    bound_box = [50, 1, 250, 251]
    image_width = 420

    expected_depth = _estimate_depth(bound_box, image_width, "chair")
    class_name, depth = projection_estimator.estimate_depth(bound_box, class_index, image_width)

    assert (class_name == "chair" and depth == expected_depth)


def test_estimate_depth_for_far_away_chair_in_a_small_image_width():
    class_index = _SUPPORTED_CLASSIFICATIONS.index("chair")
    bound_box = [50, 1, 250, 251]
    image_width = 420

    expected_depth = _estimate_depth(bound_box, image_width, "chair")
    class_name, depth = projection_estimator.estimate_depth(bound_box, class_index, image_width)

    assert (class_name == "chair" and depth == expected_depth)


def test_estimate_x_displacement_from_center_with_small_depth_and_far_left_x_pos_with_large_image():
    depth = 1
    im_width = 1400
    pos_x = 10

    expected_displacement = _estimate_x_displacement_from_center(depth, pos_x, im_width)
    displacement = projection_estimator.estimate_x_displacement_from_center(depth, pos_x,
                                                                            im_width)

    assert displacement == expected_displacement


def test_estimate_x_displacement_from_center_with_large_depth_and_far_left_x_pos_with_large_image():
    depth = 20
    im_width = 1400
    pos_x = 10

    expected_displacement = _estimate_x_displacement_from_center(depth, pos_x, im_width)
    displacement = projection_estimator.estimate_x_displacement_from_center(depth, pos_x,
                                                                            im_width)

    assert displacement == expected_displacement


def test_estimate_x_displacement_from_center_with_small_depth_and_middle_x_pos_with_large_image():
    depth = 2
    im_width = 1400
    pos_x = 700

    expected_displacement = _estimate_x_displacement_from_center(depth, pos_x, im_width)
    displacement = projection_estimator.estimate_x_displacement_from_center(depth, pos_x,
                                                                            im_width)

    assert displacement == expected_displacement


def test_estimate_x_displacement_from_center_with_large_depth_and_middle_x_pos_with_large_image():
    depth = 25
    im_width = 1400
    pos_x = 700

    expected_displacement = _estimate_x_displacement_from_center(depth, pos_x, im_width)
    displacement = projection_estimator.estimate_x_displacement_from_center(depth, pos_x,
                                                                            im_width)

    assert displacement == expected_displacement


def test_estimate_x_displacement_from_center_with_small_depth_and_far_right_x_pos_with_large_image():
    depth = 2.1
    im_width = 1400
    pos_x = 1300

    expected_displacement = _estimate_x_displacement_from_center(depth, pos_x, im_width)
    displacement = projection_estimator.estimate_x_displacement_from_center(depth, pos_x,
                                                                            im_width)

    assert displacement == expected_displacement


def test_estimate_x_displacement_from_center_with_large_depth_and_far_right_x_pos_with_large_image():
    depth = 15.56
    im_width = 1400
    pos_x = 1300

    expected_displacement = _estimate_x_displacement_from_center(depth, pos_x, im_width)
    displacement = projection_estimator.estimate_x_displacement_from_center(depth, pos_x,
                                                                            im_width)

    assert displacement == expected_displacement


def test_estimate_x_displacement_from_center_with_small_depth_and_far_left_x_pos_with_small_image():
    depth = 0.25
    im_width = 320
    pos_x = 5

    expected_displacement = _estimate_x_displacement_from_center(depth, pos_x, im_width)
    displacement = projection_estimator.estimate_x_displacement_from_center(depth, pos_x,
                                                                            im_width)

    assert displacement == expected_displacement


def test_estimate_x_displacement_from_center_with_large_depth_and_far_left_x_pos_with_small_image():
    depth = 30
    im_width = 320
    pos_x = 5

    expected_displacement = _estimate_x_displacement_from_center(depth, pos_x, im_width)
    displacement = projection_estimator.estimate_x_displacement_from_center(depth, pos_x,
                                                                            im_width)

    assert displacement == expected_displacement


def test_estimate_x_displacement_from_center_with_small_depth_and_middle_x_pos_with_small_image():
    depth = 1
    im_width = 320
    pos_x = 160

    expected_displacement = _estimate_x_displacement_from_center(depth, pos_x, im_width)
    displacement = projection_estimator.estimate_x_displacement_from_center(depth, pos_x,
                                                                            im_width)

    assert displacement == expected_displacement


def test_estimate_x_displacement_from_center_with_large_depth_and_middle_x_pos_with_small_image():
    depth = 32.1
    im_width = 320
    pos_x = 160

    expected_displacement = _estimate_x_displacement_from_center(depth, pos_x, im_width)
    displacement = projection_estimator.estimate_x_displacement_from_center(depth, pos_x,
                                                                            im_width)

    assert displacement == expected_displacement


def test_estimate_x_displacement_from_center_with_small_depth_and_far_right_x_pos_with_small_image():
    depth = 0.4
    im_width = 320
    pos_x = 280

    expected_displacement = _estimate_x_displacement_from_center(depth, pos_x, im_width)
    displacement = projection_estimator.estimate_x_displacement_from_center(depth, pos_x,
                                                                            im_width)

    assert displacement == expected_displacement


def test_estimate_x_displacement_from_center_with_large_depth_and_far_right_x_pos_with_small_image():
    depth = 25
    im_width = 320
    pos_x = 280

    expected_displacement = _estimate_x_displacement_from_center(depth, pos_x, im_width)
    displacement = projection_estimator.estimate_x_displacement_from_center(depth, pos_x,
                                                                            im_width)

    assert displacement == expected_displacement


def test_estimate_x_displacement_from_center_with_depth_of_zero():
    depth = 0
    im_width = 320
    pos_x = 280

    expected_displacement = _estimate_x_displacement_from_center(depth, pos_x, im_width)
    displacement = projection_estimator.estimate_x_displacement_from_center(depth, pos_x,
                                                                            im_width)

    assert displacement == expected_displacement


def test_estimate_x_displacement_from_center_with_pos_x_of_zero():
    depth = 2
    im_width = 320
    pos_x = 0

    expected_displacement = _estimate_x_displacement_from_center(depth, pos_x, im_width)
    displacement = projection_estimator.estimate_x_displacement_from_center(depth, pos_x,
                                                                            im_width)

    assert displacement == expected_displacement


def test_estimate_x_displacement_from_center_with_pos_x_equal_to_image_width():
    depth = 2
    im_width = 320
    pos_x = 320

    expected_displacement = _estimate_x_displacement_from_center(depth, pos_x, im_width)
    displacement = projection_estimator.estimate_x_displacement_from_center(depth, pos_x,
                                                                            im_width)

    assert displacement == expected_displacement

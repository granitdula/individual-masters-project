from src.three_d.room_estimator import RoomEstimator


def test_calculate_room_position_for_empty_instance_data():
    instance_data = []
    room_estimator = RoomEstimator(instance_data)

    x, y = room_estimator.calculate_room_position()
    expected_x, expected_y = 0, 0

    assert (x == expected_x and y == expected_y)


def test_calculate_room_position_for_singleton_instance_data():
    instance_data = [("chair", 1, 1)]
    room_estimator = RoomEstimator(instance_data)

    x, y = room_estimator.calculate_room_position()
    expected_x, expected_y = instance_data[0][2], instance_data[0][1]

    assert (x == expected_x and y == expected_y)


def test_calculate_room_position_for_three_chairs_instance_data():
    instance_data = [("chair", 1, 1), ("chair", 0, 1), ("chair", 0.5, 0.5)]
    room_estimator = RoomEstimator(instance_data)

    x, y = room_estimator.calculate_room_position()
    expected_x = (instance_data[0][2] + instance_data[1][2] + instance_data[2][2]) / 3.0
    expected_y = (instance_data[0][1] + instance_data[1][1] + instance_data[2][1]) / 3.0

    assert (x == expected_x and y == expected_y)


def test_calculate_room_position_for_three_chairs_and_one_couch_instance_data():
    instance_data = [("chair", 1, 1), ("chair", 0, 1), ("chair", 0.5, 0.5), ("couch", 2.2, 1.5)]
    room_estimator = RoomEstimator(instance_data)

    x, y = room_estimator.calculate_room_position()
    expected_x = (instance_data[0][2] + instance_data[1][2] + instance_data[2][2] +
                  instance_data[3][2]) / 4.0
    expected_y = (instance_data[0][1] + instance_data[1][1] + instance_data[2][1] +
                  instance_data[3][1]) / 4.0

    assert (x == expected_x and y == expected_y)


def test_calculate_room_position_average_to_zero_zero_position_instance_data():
    instance_data = [("chair", 0, -1), ("chair", 0, 1), ("chair", 0, -1.5), ("couch", 0, 1.5)]
    room_estimator = RoomEstimator(instance_data)

    x, y = room_estimator.calculate_room_position()
    expected_x, expected_y = 0, 0

    assert (x == expected_x and y == expected_y)


def test_calculate_room_scale_for_empty_instance_data():
    instance_data = []
    room_estimator = RoomEstimator(instance_data)

    scale = room_estimator.calculate_room_scale()
    expected_scale = 1

    assert scale == expected_scale


def test_calculate_room_scale_for_singleton_instance_data():
    instance_data = [("chair", 2, 3)]
    room_estimator = RoomEstimator(instance_data)

    scale = room_estimator.calculate_room_scale()
    expected_scale = 1

    assert scale == expected_scale


def test_calculate_room_scale_for_two_couches_instance_data():
    instance_data = [("couch", 2, 3), ("couch", 1.5, -1.5)]
    room_estimator = RoomEstimator(instance_data)

    scale = room_estimator.calculate_room_scale()
    expected_scale = 4.5

    assert scale == expected_scale


def test_calculate_room_scale_for_negative_value_cases_instance_data():
    instance_data = [("couch", 2, -3), ("couch", 1.5, -1.5)]
    room_estimator = RoomEstimator(instance_data)

    scale = room_estimator.calculate_room_scale()
    expected_scale = 1.5

    assert scale == expected_scale


def test_calculate_room_scale_for_two_couches_and_one_chair_instance_data():
    instance_data = [("couch", 2, 3), ("couch", 1.5, -1.5), ("chair", 0.4, 8)]
    room_estimator = RoomEstimator(instance_data)

    scale = room_estimator.calculate_room_scale()
    expected_scale = 9.5

    assert scale == expected_scale

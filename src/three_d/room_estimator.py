class RoomEstimator:

    def __init__(self, instance_data):
        self._instance_data = instance_data

    def calculate_room_position(self):
        """
        Calculates a position for the center of the room based on the mean positions of the
        furniture in the instance data.

        :return: x, y where x and y are float values of the position of the center of the room
                 along a plane.
        """
        # Returns a 0, 0 position for a room with no furniture
        if len(self._instance_data) == 0:
            return 0, 0

        x, y = 0, 0
        for instance in self._instance_data:
            depth, displacement = instance[1], instance[2]
            x += displacement
            y += depth

        x /= len(self._instance_data)
        y /= len(self._instance_data)

        return x, y

    def calculate_room_scale(self):
        """
        Calculates a scale for the room based on the range of the displacement and depth of all
        furniture in the instance data.

        :return: scale of the room as a float.
        """
        # Returns 1 which keeps the room at standard scale if no furniture or 1 furniture
        # exists.
        if len(self._instance_data) == 0 or len(self._instance_data) == 1:
            return 1

        depth_arr = [instance[1] for instance in self._instance_data]
        displacement_arr = [instance[2] for instance in self._instance_data]

        min_depth, max_depth = min(depth_arr), max(depth_arr)
        min_displacement, max_displacement = min(displacement_arr), max(displacement_arr)

        width, length = max_displacement - min_displacement, max_depth - min_depth
        scale = width if width > length else length

        return scale

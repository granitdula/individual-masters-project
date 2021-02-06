from panda3d.core import loadPrcFile, DirectionalLight, PointLight
from direct.showbase.ShowBase import ShowBase

from src.three_d.room_estimator import RoomEstimator

loadPrcFile("../config_3d/conf.prc")


# TODO: Maybe add an outside environment.
class View3D(ShowBase):

    # Add offsets to the furniture for better initial visibility.
    _FLOOR_Y_VALUE = -2
    _DISPLACEMENT_SCALE = 1.5
    _DEPTH_SCALE = 3
    _DEPTH_OFFSET = 10

    def __init__(self, instance_data):
        super().__init__()
        self._instance_data = instance_data

        self.set_background_color(0, 0, 0, 1)
        self._setup_global_lighting()

        self._create_room(instance_data)
        self._load_furniture_scene(instance_data)

    def _load_furniture_scene(self, instance_data):
        # Loads all appropriate furniture models and positions them in scene.
        for instance in instance_data:
            class_name, depth, x_displacement = instance[0], instance[1], instance[2]

            furniture = self.loader.load_model(f"../models/default_{class_name}")
            furniture.reparentTo(self.render)

            furniture.setPos(self._DISPLACEMENT_SCALE * x_displacement,
                             self._DEPTH_OFFSET + depth * self._DEPTH_SCALE,
                             self._FLOOR_Y_VALUE)

    def _setup_global_lighting(self):
        directional_light = DirectionalLight('directional_light')
        directional_light.setColor((1, 1, 1, 1))

        directional_light_node = self.render.attachNewNode(directional_light)
        directional_light_node.setHpr(0, -60, 0)

        self.render.setLight(directional_light_node)

    def _create_room(self, instance_data):
        room_estimator = RoomEstimator(instance_data)
        room = self.loader.load_model("../models/default_room")
        room.reparentTo(self.render)

        # Sets up room lighting.
        point_light = PointLight('point_light')
        point_light.setColor((0.5, 0.5, 0.5, 1))
        point_light_node = room.attachNewNode(point_light)
        room.setLight(point_light_node)

        room_x, room_y = room_estimator.calculate_room_position()
        room_scale = room_estimator.calculate_room_scale()

        room.setPos(self._DISPLACEMENT_SCALE * room_x, self._DEPTH_OFFSET + room_y *\
                    self._DEPTH_SCALE, self._FLOOR_Y_VALUE)
        room.setScale(room_scale, room_scale, 1)
        point_light_node.setPos(room, 0, 0, 2)

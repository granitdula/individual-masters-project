from panda3d.core import loadPrcFile, DirectionalLight
from direct.showbase.ShowBase import ShowBase

loadPrcFile("../config_3d/conf.prc")


class View3D(ShowBase):

    def __init__(self, instance_data):
        super().__init__()
        self._instance_data = instance_data

        self.set_background_color(0, 0, 0, 1)
        self._setup_lighting()

        self._load_furniture_scene(instance_data)

    def _load_furniture_scene(self, instance_data):
        # Add offsets to the furniture for better initial visibility.
        displacement_scale = 1.5
        depth_scale = 3
        depth_offset = 10
        floor_y_value = -2

        # Loads all appropriate furniture models and positions them in scene.
        for instance in instance_data:
            class_name, depth, x_displacement = instance[0], instance[1], instance[2]

            furniture = self.loader.load_model(f"../models/default_{class_name}")
            furniture.reparentTo(self.render)

            furniture.setPos(displacement_scale * x_displacement,
                             depth_offset + depth * depth_scale,
                             floor_y_value)

    def _setup_lighting(self):
        directional_light = DirectionalLight('directional_light')
        directional_light.setColor((0.8, 0.8, 0.5, 1))

        directional_light_node = self.render.attachNewNode(directional_light)
        directional_light_node.setHpr(0, -60, 0)

        self.render.setLight(directional_light_node)

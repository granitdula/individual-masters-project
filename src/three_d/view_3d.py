import math
import os
import random
import re

from panda3d.core import loadPrcFile, DirectionalLight, PointLight, GeoMipTerrain, Texture, \
    TextureStage
from direct.showbase.ShowBase import ShowBase

from src.three_d.room_estimator import RoomEstimator

loadPrcFile("../config_3d/conf.prc")


class View3D(ShowBase):

    # Add offsets to the furniture for better initial visibility.
    _FLOOR_Y_VALUE = -2
    _DISPLACEMENT_SCALE = 1.5
    _DEPTH_SCALE = 3
    _DEPTH_OFFSET = 10

    def __init__(self, instance_data):
        super().__init__()
        self._instance_data = instance_data

        self.set_background_color(0, 1, 1, 1)  # RGBA
        self._setup_global_lighting()

        self._create_terrain()
        self.room = self._create_room(instance_data)
        self._load_furniture_scene(instance_data)
        self._add_trees()

    def _create_terrain(self):
        # Set up the GeoMipTerrain.
        # NOTE: For whatever reason there seem to be warnings on the arguments for the method
        # calls: set_heightfield(), get_root() and generate(), because of not including an
        # argument of type GeoMipTerrain, even though the docs say its not required. the code
        # still works as intended though.
        terrain = GeoMipTerrain("ground_terrain")
        terrain.setHeightfield("../resources/images/textures/terrain_height_map.jpg")

        texture = self.loader.load_texture("../resources/images/textures/envir-ground.jpg")
        texture_scale = 128
        texture.set_wrap_u(Texture.WM_repeat)
        texture.set_wrap_v(Texture.WM_repeat)

        root = terrain.getRoot()
        tex_stage = TextureStage.default
        root.set_texture(tex_stage, texture)
        root.set_tex_scale(tex_stage, texture_scale)
        root.reparent_to(self.render)
        root.set_pos(-500, -500, self._FLOOR_Y_VALUE)
        terrain.calcAmbientOcclusion()

        # Can't seem to remove this warning and don't see why its even there when looking at
        # the docs. All use the generate function without arguments.
        terrain.generate()

    def _add_trees(self, num_of_trees=40, spawn_range=100):
        # Adds num_of_trees number of trees in areas which don't intersect with room.
        tree_files = self._get_all_tree_files()
        pos = self.room.get_pos()  # Center coordinates of room.
        min_bound, max_bound = self.room.get_tight_bounds()
        dimension_sizes = max_bound - min_bound

        # Radii of the two circles in which the trees can spawn in between.
        lower_radius = math.sqrt((dimension_sizes[0] / 2) ** 2 + (dimension_sizes[1] / 2) ** 2)
        upper_radius = lower_radius + spawn_range

        for i in range(num_of_trees):
            position = self._get_valid_random_position(pos[0], pos[1], lower_radius,
                                                       upper_radius)
            tree = self._get_random_tree_model(tree_files)

            if tree:
                tree.reparent_to(self.render)
                tree.set_pos(position[0], position[1], position[2])

    def _get_valid_random_position(self, center_x, center_y, lower_radius, upper_radius):
        # Gets a valid spawn location based on the center location and the two circles formed
        # by the two radii given.
        angle = random.uniform(-math.pi / 2, math.pi / 2)
        direction = random.choice([-1, 1])
        magnitude = random.uniform(lower_radius, upper_radius)

        x_component = magnitude * math.sin(angle)
        y_component = direction * magnitude * math.cos(angle)

        position = [center_x + x_component, center_y + y_component, self._FLOOR_Y_VALUE]

        return position

    def _get_random_tree_model(self, tree_file_names):
        # Returns a randomly selected tree model from the models/trees folder. Tree egg files
        # must be named with the following convention: tree_# where # is an integer.
        if len(tree_file_names) > 0:
            tree_file = random.choice(tree_file_names)
            tree_model = self.loader.load_model(f"../models/trees/{tree_file}")
            return tree_model

        return None

    @staticmethod
    def _get_all_tree_files():
        # Get tree egg files.
        files = os.listdir("../models/trees")
        regex = re.compile(r"tree_\d\.egg")

        tree_file_names = []

        for file in files:
            result = regex.match(file)
            if result:
                tree_file_names.append(result.group(0))

        return tree_file_names

    def _load_furniture_scene(self, instance_data):
        # Loads all appropriate furniture models and positions them in scene.
        for instance in instance_data:
            class_name, depth, x_displacement = instance[0], instance[1], instance[2]

            furniture = self.loader.load_model(f"../models/furniture/default_{class_name}")
            furniture.reparentTo(self.render)

            furniture.setPos(self._DISPLACEMENT_SCALE * x_displacement,
                             self._DEPTH_OFFSET + depth * self._DEPTH_SCALE,
                             self._FLOOR_Y_VALUE)

    def _setup_global_lighting(self):
        # Creates a default global lighting for the entire scene.
        directional_light = DirectionalLight('directional_light')
        directional_light.setColor((1, 1, 1, 1))

        directional_light_node = self.render.attach_new_node(directional_light)
        directional_light_node.set_hpr(0, -60, 0)

        self.render.set_light(directional_light_node)

    def _create_room(self, instance_data):
        # Creates a room that contains the furniture and is scaled based on the placement of
        # the furniture, so that it can all fit.
        room_estimator = RoomEstimator(instance_data)
        room = self.loader.load_model("../models/furniture/default_room")
        room.reparentTo(self.render)

        # Sets up room lighting.
        point_light = PointLight('point_light')
        point_light.setColor((0.5, 0.5, 0.5, 1))
        point_light_node = room.attach_new_node(point_light)
        room.set_light(point_light_node)

        room_x, room_y = room_estimator.calculate_room_position()
        room_scale = room_estimator.calculate_room_scale()

        room.set_pos(self._DISPLACEMENT_SCALE * room_x, self._DEPTH_OFFSET + room_y *
                     self._DEPTH_SCALE, self._FLOOR_Y_VALUE)
        room.set_scale(room_scale, room_scale, 1)
        point_light_node.set_pos(room, 0, 0, 2)

        return room

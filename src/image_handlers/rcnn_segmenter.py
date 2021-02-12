from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
import cv2 as cv


class RCNNSegmenter:

    # Supported object classifications for the predictor.
    _COCO_INSTANCE_CLASSIFICATION_NAMES = [
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

    # TODO: Change these arbitrary widths to be read from width of the actual default meshes used.
    _OBJECT_WIDTH_MAPPING = {"chair": 1, "couch": 2, "dining table": 2.5, "bed": 2, "oven": 1,
                             "refrigerator": 1}

    def __init__(self, threshold):
        self._create_pretrained_model(threshold)

    def _create_pretrained_model(self, threshold):
        # Loads a default Mask RCNN in detectron2.
        config_path = "COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml"
        self._cfg = get_cfg()

        self._cfg.merge_from_file(model_zoo.get_config_file(config_path))
        self._cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = threshold  # set threshold for this model

        # Use model X101-FPN-3X model from model zoo in detectron2
        self._cfg.MODEL.WEIGHTS = "./../pretrained_models/model_final_2d9806.pkl"

        self._cfg.MODEL.DEVICE = "cpu"

        self._predictor = DefaultPredictor(self._cfg)

    def segment_image(self, image):
        """
        Segments the input image into unique instances recognized by the model and returns useful
        data about the segmentation.

        :param image: OpenCV image.
        :return: Instances object from the detectron2 package.
        """
        return self._predictor(image)

    def visualise_segmentation(self, image):
        """
        Displays the input image with its segmentations and labels shown in colour coding.

        :param image: OpenCV image.
        :return: None.
        """
        v = Visualizer(image[:, :, ::-1], MetadataCatalog.get(self._cfg.DATASETS.TRAIN[0]), scale=1.2)

        outputs = self.segment_image(image)

        out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        cv.imshow("Segmented Image Visualisation", out.get_image()[:, :, ::-1])
        _ = cv.waitKey(0)

    def get_supported_classifications(self):
        """
        Gets a list of all the objects that can be classified by this model.
        :return: List of all objects that can be classified.
        """
        return self._COCO_INSTANCE_CLASSIFICATION_NAMES

    def get_object_size_mapping(self):
        """
        Gets a mapping of the classifiable objects and their default widths based on default
        mesh.
        :return: Dictionary of objects and their default widths
        """
        return self._OBJECT_WIDTH_MAPPING

from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
import cv2 as cv


class RCNNSegmenter:

    def __init__(self, threshold):
        self.__create_pretrained_model(threshold)

    def __create_pretrained_model(self, threshold):
        config_path = "COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml"
        self._cfg = get_cfg()

        self._cfg.merge_from_file(model_zoo.get_config_file(config_path))
        self._cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = threshold  # set threshold for this model

        # Use model X101-FPN-3X model from model zoo in detectron2
        self._cfg.MODEL.WEIGHTS = "./../../pretrained_models/model_final_2d9806.pkl"

        self._cfg.MODEL.DEVICE = "cpu"

        self._predictor = DefaultPredictor(self._cfg)

    def segment_image(self, image):
        return self._predictor(image)

    def visualise_segmentation(self, image):
        # We can use `Visualizer` to draw the predictions on the image. Used for debugging.
        v = Visualizer(image[:, :, ::-1], MetadataCatalog.get(self._cfg.DATASETS.TRAIN[0]), scale=1.2)

        outputs = self.segment_image(image)

        out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        cv.imshow("Segmented Image Visualisation", out.get_image()[:, :, ::-1])
        _ = cv.waitKey(0)

import torch
TORCH_VERSION = ".".join(torch.__version__.split(".")[:2])
CUDA_VERSION = torch.__version__.split("+")[-1]
print("torch: ", TORCH_VERSION, "; cuda: ", CUDA_VERSION)

from detectron2.data.datasets import register_coco_instances
from detectron2.data import DatasetCatalog, MetadataCatalog
import random
import numpy as np
import cv2
import matplotlib.pyplot as plt
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.utils.visualizer import Visualizer
from detectron2.utils.visualizer import ColorMode
import os
import glob


model_path = 'output/decay_iter_10k/model_final.pth'
output_path = 'outputs/output'

from detectron2.projects import point_rend
classes = ['fault',]
data_path = 'test'
register_coco_instances('model_test', {}, 'mockup.json', 'data/test_image')

cfg = get_cfg()
# Add PointRend-specific config
point_rend.add_pointrend_config(cfg)
cfg.merge_from_file("detectron2/projects/PointRend/configs/InstanceSegmentation/pointrend_rcnn_X_101_32x8d_FPN_3x_coco.yaml")
cfg.MODEL.WEIGHTS = "model/model_final_ba17b9.pkl"
cfg.MODEL.WEIGHTS = model_path
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
cfg.MODEL.POINT_HEAD.NUM_CLASSES = 1
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.DATASETS.TEST = ("fault_test", )
predictor = DefaultPredictor(cfg)

test_metadata = MetadataCatalog.get("model_test")
np.random.seed(304)


test_image = [file for file in os.listdir('data/test_image/') if file.endswith(('.png', 'jpg'))]
# print(test_image)
# print(os.listdir('test_image/'))


# for imageName in test_image: 
#     img = cv2.imread(imageName)
#     outputs = predictor(img)
#     v = Visualizer(img[:, :, ::-1],
#                    metadata=test_metadata, 
#                    scale=0.8, 
#                    instance_mode=ColorMode.IMAGE_BW # removes the colors of unsegmented pixels
#     )
#     v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
#     # print(f'{imageName[:-4].replace("/content/drive/MyDrive/dataset/coco/test","output_images")}_result.png')
#     # cv2.imwrite(f'{imageName[:-4].replace("/content/drive/MyDrive/dataset/coco/test","output_images")}_result.png', v.get_image()[:, :, ::-1])
#     plt.figure(figsize = (14, 10))
#     plt.imshow(cv2.cvtColor(v.get_image()[:, :, ::-1], cv2.COLOR_BGR2RGB))
#     plt.show()


# for imageName in test_image:  
#     im = cv2.imread('data/test_image/' + imageName)
#     # print(im)
#     outputs = predictor(im)
#     v = Visualizer(im[:, :, ::-1], metadata=test_metadata, scale=0.8)
#     v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
#     plt.figure(figsize = (14, 10))
#     plt.imshow(cv2.cvtColor(v.get_image()[:, :, ::-1], cv2.COLOR_BGR2RGB))
#     plt.show()

im = cv2.imread('data/test_image/' + '1-Figure1-1.png')
# print(im)
outputs = predictor(im)
# pred = outputs['instances'].pred_masks 
# # print(outputs['instances'].pred_masks)
# # print([outputs['instances']].pred_boxes.tensor.cpu().numpy())
# print(pred.shape)
# print(outputs['instances'])

v = Visualizer(im[:, :, ::-1], metadata=test_metadata, scale=1, )
v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
plt.figure(figsize = (14, 10))
plt.imshow(cv2.cvtColor(v.get_image()[:, :, ::-1], cv2.COLOR_BGR2RGB))
plt.show()
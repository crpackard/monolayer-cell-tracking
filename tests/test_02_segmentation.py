import pytest
from monolayer_cell_tracking.segmentation import Segmentation

def test_segmentation_Yamada():
  segmentation = Segmentation(
    src='./monolayer_cell_tracking/data/Yamada.mp4',
    model_path='./monolayer_cell_tracking/models/cellpose_segmentation_model_Yamada')
  segmentation.compute_segmentations()

def test_segmentation_Pertz():
  segmentation = Segmentation(
    src='./monolayer_cell_tracking/data/Pertz.mp4',
    model_path='./monolayer_cell_tracking/models/cellpose_segmentation_model_Pertz')
  segmentation.compute_segmentations()

def test_segmentation_Angelini():
  segmentation = Segmentation(
    src='./monolayer_cell_tracking/data/Angelini.mp4',
    model_path='./monolayer_cell_tracking/models/cellpose_segmentation_model_Angelini')
  segmentation.compute_segmentations()

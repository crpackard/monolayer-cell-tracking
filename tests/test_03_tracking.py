import pytest
from monolayer_cell_tracking.tracking import Tracking

#def test_tracking_Yamada():
#  tracking = Tracking(
#    src='./monolayer_cell_tracking/data/Yamada.mp4',
#    model_path='./monolayer_cell_tracking/models/cellpose_segmentation_model_Yamada')
#  tracking.extract_trajectories()

#def test_tracking_Pertz():
#  tracking = Tracking(
#    src='./monolayer_cell_tracking/data/Pertz.mp4',
#    model_path='./monolayer_cell_tracking/models/cellpose_segmentation_model_Pertz')
#  tracking.extract_trajectories()

def test_tracking_Angelini():
  tracking = Tracking(
    src='./monolayer_cell_tracking/data/Angelini.mp4',
    model_path='./monolayer_cell_tracking/models/cellpose_segmentation_model_Angelini')
  tracking.extract_trajectories()

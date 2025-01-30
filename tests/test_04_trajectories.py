import pytest
from monolayer_cell_tracking.trajectories import Trajectories

def test_trajectories_Angelini():
  trajectories = Trajectories(
    src='./monolayer_cell_tracking/data/Angelini.mp4',
    model_path='./monolayer_cell_tracking/models/cellpose_segmentation_model_Angelini')

  trajectories.dump_data()

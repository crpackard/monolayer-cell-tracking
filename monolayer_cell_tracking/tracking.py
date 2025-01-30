
import os
import numpy as np
import btrack, btrack.btypes
from btrack import datasets # don't remove! import statement triggers required internal proccesses within `cell_config()`
from typing import List
from .segmentation import Segmentation

class Tracking(Segmentation):
  def __init__(self, src: str, model_path: str) -> None:
    """ This class is used to track single cells across a time-series of segmentations. """
    Segmentation.__init__(self, src, model_path)
    self.trajectory_file = self.src.replace('.mp4', '.h5')

  def max_search_radius(self, scale: float = 1.0) -> float:
    """ Assume a maximum distance that each cell can travel between frames. """
    return scale * self.model.diam_labels.copy()

  def extract_trajectories(self) -> List[btrack.btypes.Tracklet]:
    """ Stitch a time-series of video frame segmentations together, and track individual cell trajectories. """
    if os.path.exists(self.trajectory_file):
      return self.load_trajectories()

    timeseries: List[np.ndarray] = [self.load_segmentations(t) for t in range(self.num_frames())]

    (ymax, xmax) = timeseries[0].shape
    (ymin, xmin) = (0, 0)

    FEATURES = (
        'area',
        'major_axis_length',
        'minor_axis_length',
        'orientation',
        'solidity')

    objects = btrack.utils.segmentation_to_objects(
      np.array(timeseries),
      properties=FEATURES,
      num_workers=4)

    with btrack.BayesianTracker() as tracker:
      tracker.configure(btrack.datasets.cell_config())
      tracker.max_search_radius = self.max_search_radius()
      tracker.tracking_updates = ["MOTION", "VISUAL"]
      tracker.features = FEATURES
      tracker.append(objects)
      tracker.volume=((xmin, xmax), (ymin, ymax))
      tracker.track()
      tracker.optimize()
      tracker.export(self.trajectory_file, obj_type="obj_type_1")

    return self.load_trajectories()

  def load_trajectories(self) -> List[btrack.btypes.Tracklet]:
    """ Load the trajectory data saved by extract_trajectories(). """
    return btrack.io.HDF5FileHandler(self.trajectory_file).tracks

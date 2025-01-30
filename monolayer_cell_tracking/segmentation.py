
import os, glob
import numpy as np
from tqdm import tqdm
from typing import Dict
from cellpose import models, utils
from shapely.geometry import Polygon, Point
from .video import Video

class Segmentation(Video):
  def __init__(self, src: str, model_path: str) -> None:
    """ This class is used to segment video data. """
    Video.__init__(self, src)

    self.model: any = self.load_segmentation_model(model_path)

    # Store the segmentation data for the ensemble of cells at a specific frame.
    self.cells: Dict = None
    self.cell_frame: int = -1

  def load_segmentation_model(self, model_path: str) -> any:
    """ Segmentation models are loaded as follows. """
    return models.CellposeModel(pretrained_model=model_path)

  def segment_image(self, t: int) -> np.ndarray:
    """ Return the segmenation masks for the video frame at time `t`. """
    return self.model.eval(self.load_frame(t), channels=[0, 0], diameter=self.model.diam_labels.copy())[0]

  def segmentation_file(self, t: int) -> str:
    """ Default naming convention for video frame segmentation files. """
    return os.path.join(self.dst, f't={t}.npz')

  def num_frames(self) -> int:
    """ Count how many video frame image datafiles there are. """
    return len(glob.glob(os.path.join(self.dst, '*.png')))

  def compute_segmentations(self) -> None:
    """ Obtain the segmentations for all frames in the video (return the total number of frames). """
    for t in tqdm(range(self.num_frames())):
      if os.path.exists(self.segmentation_file(t)):
        continue
      masks: np.ndarray = self.segment_image(t)
      np.savez_compressed(self.segmentation_file(t), masks)

  def load_segmentations(self, t: int) -> np.ndarray:
    """ Load the segmentation masks stored in a compressed numpy file. """
    npz_file = np.load(self.segmentation_file(t))
    return npz_file['arr_0']

  def cell_contours(self, t: int) -> Dict:
    """ Extract the (x,y) coordinates defining each cell's segmentation. """
    if (t == self.cell_frame):
      return self.cells
    else:
      self.cell_frame = t
      self.cells: Dict = {}
      segmentations = self.load_segmentations(t)
      for ii, cell_outline in enumerate(utils.outlines_list(segmentations)):
        self.cells[ii] = {}
        self.cells[ii]['x'] = cell_outline.flatten()[::2]
        self.cells[ii]['y'] = cell_outline.flatten()[1::2]
      return self.cells

  def lookup_cell_contour(self, t: int, x0: float, y0: float) -> Dict:
    """ Find the cell that contains the point (x0,y0); returns `None` if failure. """
    point = Point(x0, y0)
    for cell in self.cell_contours(t).values():
      if point.within(Polygon(zip(cell['x'], cell['y']))):
        return cell

  def shared_edge(self, cell_1: Dict, cell_2: Dict) -> np.ndarray:
    """ Find the coordinates that two cells. """
    connected_points = []
    for (x1, y1) in zip(cell_1['x'], cell_1['y']):
      for (x2, y2) in zip(cell_2['x'], cell_2['y']):
        if np.sqrt((x1-x2)**2 + (y1-y2)**2) <= 1:
          connected_points.append([int(x1), int(y1)])
          connected_points.append([int(x2), int(y2)])
    return np.array(connected_points)

  def cell_pixel_data(self, t: int, x0: float, y0: float) -> np.ndarray:
    """ Return the pixels belonging to the cell containing the point (x0,y0). """
    segmentations: np.ndarray = self.load_segmentations(t)
    frame: np.ndarray = self.load_frame(t)    
    label = segmentations[int(y0), int(x0)]
    object_mask = np.where(segmentations == label, True, False)
    object_pixels = frame[object_mask]
    return object_pixels

  def cell_avg_pixel_vector(self, t: int, x0: float, y0: float) -> np.ndarray:
    """ Return the pixels belonging to the cell containing the point (x0,y0). """
    return np.mean(self.cell_pixel_data(t, x0, y0), axis=1)

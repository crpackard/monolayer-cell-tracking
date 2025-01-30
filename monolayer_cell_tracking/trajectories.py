
import os, btrack
import numpy as np
import pandas as pd
from tqdm import tqdm
from typing import Dict, List
from .tracking import Tracking

class Trajectories(Tracking):
  def __init__(self, src: str, model_path: str):
    """ This class combines tracking and segmentation data to extract highly-detailed trajectory data. """
    Tracking.__init__(self, src, model_path)
    self.trajectories = self.extract_trajectories()
    self.max_nNeigh: int = 12

  def num_cells(self) -> int:
    """ Total number of cell trajectories that were tracked. """
    return len(self.trajectories)

  def x(self, t: int, ii: int) -> int:
    """ Return the x-coordinate of the centroid of cell `ii` at time `t`. """
    return int(self.trajectories[ii].x[self.trajectories[ii].t.index(t)])

  def y(self, t: int, ii: int) -> int:
    """ Return the y-coordinate of the centroid of cell `ii` at time `t`. """
    return int(self.trajectories[ii].y[self.trajectories[ii].t.index(t)])

  def A(self, t: int, ii: int) -> int:
    """ Return the cross-sectional area of cell `ii` at time `t`. """
    try:
      return int(self.trajectories[ii].properties['area'][self.trajectories[ii].t.index(t)])
    except ValueError:
      return -1

  def l1(self, t: int, ii: int) -> int:
    """ Return the major axis length of cell `ii` at time `t`. """
    try:
      return int(self.trajectories[ii].properties['major_axis_length'][self.trajectories[ii].t.index(t)])
    except ValueError:
      return -1

  def l2(self, t: int, ii: int) -> int:
    """ Return the minor axis length of cell `ii` at time `t`. """
    try:
      return int(self.trajectories[ii].properties['minor_axis_length'][self.trajectories[ii].t.index(t)])
    except ValueError:
      return -1

  def theta(self, t: int, ii: int) -> float:
    """ Return the nematic angular orientation of cell `ii` at time `t`. """
    return self.trajectories[ii].properties['orientation'][self.trajectories[ii].t.index(t)]

  def average_cell_size(self, t: int) -> float:
    """ Compute the characteristic length-scale of cells at time `t`. """
    area_distribution = [self.A(t, ii) for ii, _ in self.instantaneous_trajectories(t).items() if not np.isnan(self.A(t, ii))]
    return np.sqrt(np.mean(np.array(area_distribution)))

  def separation_distance(self, t: int, ii: int, jj: int) -> float:
    """ Compute the distance between two cells at time `t`. """
    xij: float = self.x(t, ii) - self.x(t, jj)
    yij: float = self.y(t, ii) - self.y(t, jj)
    return np.sqrt(xij**2 + yij**2)

  def null_trajectory_data(self) -> Dict:
    """ Return an empty template for a cell's trajectory data. """
    null_fields = {'t':[], 'x':[], 'y':[], 'A':[], 'l1':[], 'l2':[], 'theta':[], 'P':[], 'c1':[], 'c2':[], 'c3':[]}
    for jj in range(self.max_nNeigh):
      null_fields[f'neigh_{jj}'] = []
      null_fields[f'num_contact_pnts_{jj}'] = []
    return null_fields

  def instantaneous_trajectories(self, t: int) -> Dict[int, btrack.btypes.Tracklet]:
    """ Find the set of trajectories that exist at time `t`. """
    return {ii: traj for ii, traj in enumerate(self.trajectories) if (t in traj.t)}

  def subvolume_trajectories(self, t: int, window: List[int]) -> Dict[int, btrack.btypes.Tracklet]:
    """ Find the set of trajectories that exist at time `t` within a sub-volume `window`. """
    def is_within_window(traj: btrack.btypes.Tracklet) -> bool:
      x = traj.x[traj.t.index(t)]
      y = traj.y[traj.t.index(t)]
      is_within_y = (window[0] < y < window[1])
      is_within_x = (window[2] < x < window[3])
      return (is_within_x and is_within_y)
    return {ii: traj for ii, traj in self.instantaneous_trajectories(t).items() if is_within_window(traj)}

  def neighbor_candidates(self, t: int, ii: int) -> List[int]:
    """ Find the set of cells with centroids within a metric cut-off radius around cell `ii` at time `t`. """
    metric_neighbors: List[int] = []
    search_radius = 3.0 * self.average_cell_size(t)
    for jj, _ in self.instantaneous_trajectories(t).items():
      if (ii == jj):
        continue
      elif search_radius < self.separation_distance(t, ii, jj):
        continue
      else:
        metric_neighbors.append(jj)
    return metric_neighbors

  def are_neighbors(self, cell_1: Dict, cell_2: Dict) -> bool:
    """ Compare the contour coordinates of two cells to check whether they are in physical contact. """
    if isinstance(cell_1, type(None)) or isinstance(cell_2, type(None)):
      return False
    else:
      dx = cell_1['x'][:, np.newaxis] - cell_2['x']
      dy = cell_1['y'][:, np.newaxis] - cell_2['y']
      dr = np.sqrt(dx**2 + dy**2)
      return np.any(dr <= 2.0)

  def neighbors(self, t: int, ii: int) -> List[int]:
    """ Find the set of cells that are in physical contact with cell `ii`. """
    neighbor_list: List[int] = []
    cell_ii = self.lookup_cell_contour(t, self.x(t,ii), self.y(t,ii))
    for jj in self.neighbor_candidates(t, ii):
      cell_jj = self.lookup_cell_contour(t, self.x(t,jj), self.y(t,jj))
      if self.are_neighbors(cell_ii, cell_jj):
        neighbor_list.append(jj)
    return neighbor_list

  def dump_dir(self) -> str:
    """ Default location where trajectory data will be dumped to. """
    out = self.dst.replace('frames', 'trajectories')
    if not os.path.exists(out):
      os.mkdir(out)
    return out

  def dump_data(self, ii: int = -1) -> None:
    """ Primary function of this class; saves the trajectory data of each cell to a csv file. """
    iterator: any = [ii] if (0 <= ii) else range(self.num_cells())
    out = self.dump_dir()
    for ii in iterator:
      traj_file = os.path.join(out, f'ii={ii}.csv')
      if os.path.exists(traj_file):
        continue
      else:
        data = self.null_trajectory_data()
      for t in self.trajectories[ii].t:
        data['t'].append(t)
        data['x'].append(self.x(t, ii))
        data['y'].append(self.y(t, ii))
        data['A'].append(self.A(t, ii))
        data['l1'].append(int(self.l1(t, ii)))
        data['l2'].append(int(self.l2(t, ii)))
        data['theta'].append(self.theta(t, ii))
        vec = self.cell_avg_pixel_vector(t, self.x(t,ii), self.y(t,ii))
        data['c1'].append(int(vec[0]))
        data['c2'].append(int(vec[1]))
        data['c3'].append(int(vec[2]))
        cell = self.lookup_cell_contour(t, self.x(t,ii), self.y(t,ii))
        if not isinstance(cell, type(None)):
          data['P'].append(len(cell['x']))
        else:
          data['P'].append(-1)
        num_neighbors: int = 0
        for jj in self.neighbor_candidates(t, ii):
          if (ii == jj):
            continue
          else:
            cell_1 = self.lookup_cell_contour(t, self.x(t,ii), self.y(t,ii))
            cell_2 = self.lookup_cell_contour(t, self.x(t,jj), self.y(t,jj))
          if self.are_neighbors(cell_1, cell_2):
            connected_pnts: np.ndarray = self.shared_edge(cell_1, cell_2)
            data[f'neigh_{num_neighbors}'].append(jj)
            data[f'num_contact_pnts_{num_neighbors}'].append(connected_pnts.shape[0])
            num_neighbors += 1
        for jj in range(num_neighbors, self.max_nNeigh):
          data[f'neigh_{num_neighbors}'].append(-1)
          data[f'num_contact_pnts_{num_neighbors}'].append(-1)
          num_neighbors += 1
        df = pd.DataFrame(data)
        df.to_csv(traj_file, index=False)

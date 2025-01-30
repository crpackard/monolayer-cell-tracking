
import os
import itertools
import numpy as np
from typing import List
from tqdm import tqdm
import imageio.v2 as imageio
import matplotlib
import matplotlib.pyplot as plt
from .trajectories import Trajectories

class Visualization(Trajectories):
  def __init__(self, src: str, model_path: str):
    """ This class is used to overlay extracted trajectories and segmentations on raw experimental data. """
    Trajectories.__init__(self, src, model_path)

    self.cmaps = self.generate_colormaps()

  def overlay_segmentations(self, t: int) -> np.ndarray:
    """ Overlay the contours of segmented cells at time `t` on top of original video frame. """
    frame: np.ndarray = self.load_frame(t)
    for cell in self.cell_contours(t).values():
      for x, y in zip(cell['x'], cell['y']):
        frame[y,x] = np.array((255, 255, 255))
    return frame

  def highlight_shared_edges(self, frame: np.ndarray, t: int, zoom: List[int]) -> np.ndarray:
    """ Color the portions of cell contours that are shared by two different cells. """
    for ii, _ in tqdm(self.subvolume_trajectories(t, zoom).items()):
      for jj in tqdm(self.neighbor_candidates(t, ii)):
        if (ii == jj):
          continue
        else:
          cell_1 = self.lookup_cell_contour(t, self.x(t,ii), self.y(t,ii))
          cell_2 = self.lookup_cell_contour(t, self.x(t,jj), self.y(t,jj))
        if self.are_neighbors(cell_1, cell_2):
          for pnt in self.shared_edge(cell_1, cell_2):
            frame[pnt[1], pnt[0]] = np.array((0, 255, 0))
    return frame

  def animate_raw_data(self, t0: int, tf: int, dst: str, zoom: List = None) -> None:
    """ Create a movie of cell segmentations evolving over time. """
    if os.path.exists(dst):
      return None
    else:
      print(f'Creating file: {dst}')
      animation = []
      for t in tqdm(range(t0, tf)):
        frame = self.load_frame(t)
        if not isinstance(zoom, type(None)):
          frame = frame[zoom[0]:zoom[1], zoom[2]:zoom[3], :]
        animation.append(frame)
      imageio.mimsave(dst, animation, fps=10, format='GIF', loop=0)

  def animate_segmentations(self, t0: int, tf: int, dst: str, zoom: List = None) -> None:
    """ Create a movie of cell segmentations evolving over time. """
    if os.path.exists(dst):
      return None
    else:
      print(f'Creating file: {dst}')
      animation = []
      for t in tqdm(range(t0, tf)):
        frame = self.overlay_segmentations(t)
        if not isinstance(zoom, type(None)):
          frame = frame[zoom[0]:zoom[1], zoom[2]:zoom[3], :]
        animation.append(frame)
      imageio.mimsave(dst, animation, fps=10, format='GIF', loop=0)

  def animate_contact_points(self, t0: int, tf: int, dst: str, zoom: List[int]) -> None:
    """ Create a movie of cell segmentations evolving over time. """
    if os.path.exists(dst):
      return None
    else:
      print(f'Creating file: {dst}')
      animation = []
      for t in tqdm(range(t0, tf)):
        frame = self.overlay_segmentations(t)
        frame = self.highlight_shared_edges(frame, t, zoom)
        frame = frame[zoom[0]:zoom[1], zoom[2]:zoom[3], :]
        import cv2; cv2.imwrite('./tmp.png', frame)
        animation.append(frame)
        if (t-t0) % 5 == 0:
          imageio.mimsave(dst, animation, fps=5, format='GIF', loop=0)
      imageio.mimsave(dst, animation, fps=5, format='GIF', loop=0)

  def generate_colormaps(self) -> List[str]:
    """ Assign a colormap to each tracked cell. """
    cmap_options = itertools.cycle(['Greys', 'Purples', 'Oranges', 'Reds', 'Blues', 'Greens'])
    return [next(cmap_options) for _ in range(len(self.trajectories))]

  def overlay_trajectories(self, ax: matplotlib.axes, t: int, zoom: List[int], s: float, trail_length=9) -> matplotlib.axes:
    """ Plot the center-of-mass trajectory of each cell within a sub-volume window. """
    for ii, traj in self.subvolume_trajectories(t, zoom).items():
      tf = traj.t.index(t)
      t0 = tf - trail_length
      xarr: List[float] = [traj.x[tidx]     for tidx in range(t0, tf) if not (tidx < 0)]
      yarr: List[float] = [traj.y[tidx]     for tidx in range(t0, tf) if not (tidx < 0)]
      tarr: List[float] = [(tidx / (tf-t0)) for tidx in range(t0, tf) if not (tidx < 0)]
      ax.scatter(xarr, yarr, c=tarr, cmap=self.cmaps[ii], s=s, marker='o')
    return ax

  def animate_repo_main_mov(self, t0: int, tf: int, dst: str, dpi: int=50, dL0: int=100, rate: float=3.5) -> None:
    """ Make a pretty movie for the repsitory's root README. """
    if os.path.exists(dst):
      return None
    print(f'Creating file: {dst}')
    (Lx, Ly) = self.system_size()
    animation: List[np.ndarray] = []
    for t in tqdm(range(t0, tf)):
      fig, ax = plt.subplots(figsize=(9.0, 9.0))
      if 20 < (t - t0):
        ax.imshow(self.overlay_segmentations(t))
      else:
        ax.imshow(self.load_frame(t))
      if 30 < (t - t0):
        s = 100 - 0.3 * (t-t0)
      else:
        s = 1e-2
      dL = dL0 + rate * (t-t0)
      x1 = (Lx / 2) - (dL / 2)
      x2 = (Lx / 2) + (dL / 2)
      y1 = (Ly / 2) - (dL / 2)
      y2 = (Ly / 2) + (dL / 2)
      ax = self.overlay_trajectories(ax, t, zoom=[y1, y2, x1, x2], s=s)
      ax.set(xlim=[x1,x2], ylim=[y1,y2])
      ax.set_axis_off()
      plt.savefig('./tmp.png', bbox_inches='tight', dpi=dpi)
      frame = self.load_image('./tmp.png')
      os.remove('./tmp.png')
      plt.close()
      if (t == t0):
        animation.append(frame)
      elif (t > t0) and (frame.shape == animation[-1].shape):
        animation.append(frame)
      else:
        break
    imageio.mimsave(dst, animation, fps=10, format='GIF', loop=0)

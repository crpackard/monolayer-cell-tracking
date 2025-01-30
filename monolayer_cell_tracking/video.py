
import os, cv2
import numpy as np
from typing import Tuple

class Video():
  def __init__(self, src: str) -> None:
    """ This class is used to handle video data. """
    assert os.path.exists(src)
    self.src: str = src
    self.dst: str = self.config_frames_dir()

  def config_frames_dir(self) -> str:
    """ Create a directory (adjacent to the src file) in which to save video frame images. """
    src_file = os.path.basename(self.src)
    src_file_noExt = src_file.split('.')[0]
    src_dir = self.src.split(src_file)[0]
    dst_dir = (src_dir + f'{src_file_noExt}_frames')
    if not os.path.exists(dst_dir):
      os.mkdir(dst_dir)
    return dst_dir

  def frame_file(self, t: int) -> str:
    """ Default naming convention for video frame images files. """
    return os.path.join(self.dst, f't={t}.png')

  def extract_frames(self) -> int:
    """ Iterate over each frame in the src file, and save each one as an image file (return total number of frames). """
    vid = cv2.VideoCapture(self.src)
    assert vid.isOpened()

    t: int = 0
    while True:

      # Read in the current video frame.
      ret, frame = vid.read()
      if not ret:
        break
      elif os.path.exists(self.frame_file(t)):
        continue
      else:
        cv2.imwrite(self.frame_file(t), frame)
      t +=1

    return t

  def load_image(self, filepath: str) -> np.ndarray:
    """ Load an arbitrary image file (convert from bgr to rgb color channels). """
    return cv2.cvtColor(cv2.imread(filepath), cv2.COLOR_BGR2RGB)

  def load_frame(self, t: int) -> np.ndarray:
    """ Load the image data of a video frame at time `t`. """
    return self.load_image(self.frame_file(t))

  def system_size(self) -> Tuple[float]:
    """ Return the linear size of the video window. """
    frame = self.load_frame(t=0)
    (Ly, Lx, Lz) = frame.shape
    return (Lx, Ly)

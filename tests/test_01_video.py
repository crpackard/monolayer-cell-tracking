import pytest
from monolayer_cell_tracking.video import Video

def test_video_Yamada():
  video = Video(src='./monolayer_cell_tracking/data/Yamada.mp4')
  video.extract_frames()

def test_video_Pertz():
  video = Video(src='./monolayer_cell_tracking/data/Pertz.mp4')
  video.extract_frames()

def test_video_Angelini():
  video = Video(src='./monolayer_cell_tracking/data/Angelini.mp4')
  video.extract_frames()


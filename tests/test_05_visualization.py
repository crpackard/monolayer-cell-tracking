import pytest
from monolayer_cell_tracking.visualization import Visualization

def test_visualization_Yamada(keep_dir='./tests/keep', region = [150,250,150,250]):

  visualization = Visualization(
    src='./monolayer_cell_tracking/data/Yamada.mp4',
    model_path='./monolayer_cell_tracking/models/cellpose_segmentation_model_Yamada')

  visualization.animate_raw_data(t0=0, tf=30, dst=f'{keep_dir}/yamada_animate_raw_data.gif', zoom=region)
  visualization.animate_segmentations(t0=0, tf=30, dst=f'{keep_dir}/yamada_animate_segmentations.gif', zoom=region)
  visualization.animate_contact_points(t0=0, tf=10, dst=f'{keep_dir}/yamada_animate_contact_points.gif', zoom=region)
  visualization.animate_repo_main_mov(t0=0, tf=100, dst=f'{keep_dir}/yamada_animate_repo_main_mov.gif', dpi=60, dL0=50, rate=2.5)

def test_visualization_Pertz(keep_dir='./tests/keep', region = [150,250,350,450]):

  visualization = Visualization(
    src='./monolayer_cell_tracking/data/Pertz.mp4',
    model_path='./monolayer_cell_tracking/models/cellpose_segmentation_model_Pertz')

  visualization.animate_raw_data(t0=140, tf=170, dst=f'{keep_dir}/pertz_animate_raw_data.gif', zoom=region)
  visualization.animate_segmentations(t0=140, tf=170, dst=f'{keep_dir}/pertz_animate_segmentations.gif', zoom=region)

#def test_visualization_Angelini(keep_dir='./tests/keep'):
#
#  visualization = Visualization(
#    src='./monolayer_cell_tracking/data/Angelini.mp4',
#    model_path='./monolayer_cell_tracking/models/cellpose_segmentation_model_Angelini')
#
#  visualization.animate_segmentations(t0=800, tf=1200, dst=f'{keep_dir}/angelini_animate_segmentations.gif', zoom=[600,800,600,800])
#  visualization.animate_contact_points(t0=1000, tf=1020, dst=f'{keep_dir}/angelini_animate_contact_points.gif', zoom=[650,750,650,750])
#  visualization.animate_repo_main_mov(t0=300, tf=550, dst=f'{keep_dir}/angelini_animate_repo_main_mov.gif')

from monolayer_cell_tracking.trajectories import Trajectories

def main(ii: int) -> None:
  trajectories = Trajectories(
    src='./monolayer_cell_tracking/data/Yamada.mp4',
    model_path='./monolayer_cell_tracking/models/cellpose_segmentation_model_Yamada')

  trajectories.dump_data(ii)

import sys
if __name__=="__main__":
  main(ii=int(sys.argv[1]))

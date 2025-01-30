
# The gdown library makes downloading from Google Drive simple.
import os, gdown

# File ID's for trajectory data stored on Google Drive.
file_IDs = {
  "Yamada":   "11lD0xlcRKVBEL9x_fVB_YL4Nmlw8t4GM",
  "Pertz":    "1RMr42k4FX_-h9z8Z7pRUbcio_KpC7K6W",
  "Angelini": "1_cyrMDOkWpmv9V_VAw2XOW-zuHxVQ0Jr",
}

# Download each trajectory datafile.
for name, file_id in file_IDs.items():
  url = f"https://drive.google.com/uc?id={file_id}"
  output = f"./../monolayer_cell_tracking/models/cellpose_segmentation_model_{name}"
  if not os.path.exists(output):
    gdown.download(url, output, quiet=False)
  else:
    print(f"\nWarning! Attempting to over-write existing file: {output}")

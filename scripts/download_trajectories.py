
# The gdown library makes downloading from Google Drive simple.
import os, gdown

# File ID's for trajectory data stored on Google Drive.
file_IDs = {
  "Yamada":   "1PTJ3B-UBDkksbgIQbzwgsWI4vlPPwAm1",
  #"Pertz":    "",
  "Angelini": "1in4r_FucXs2UsJe5byJ20t-LHe1M1TBV",
}

# Download each trajectory datafile.
for name, file_id in file_IDs.items():
  url = f"https://drive.google.com/uc?id={file_id}"
  output = f"./../monolayer_cell_tracking/data/{name}.h5"
  if not os.path.exists(output):
    gdown.download(url, output, quiet=False)
  else:
    print(f"\nWarning! Attempting to over-write existing file: {output}")

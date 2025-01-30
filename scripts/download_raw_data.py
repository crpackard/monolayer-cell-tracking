
# The gdown library makes downloading from Google Drive simple.
import os, gdown

# File ID's for trajectory data stored on Google Drive.
file_IDs = {
  "Yamada":   "1gCXm0qXsiDpBp5MLPLwpNzKvWgC30MeN",
  "Pertz":    "1YBu0nrxgLNuGhJgPoS5S1eDb2MewBoEU",
  "Angelini": "1i1ZUwaVFxQrCGLVrO4Y20OozpivUL_Uz",
}

# Download each trajectory datafile.
for name, file_id in file_IDs.items():
  url = f"https://drive.google.com/uc?id={file_id}"
  output = f"./../monolayer_cell_tracking/data/{name}.mp4"
  if not os.path.exists(output):
    gdown.download(url, output, quiet=False)
  else:
    print(f"\nWarning! Attempting to over-write existing file: {output}")


# The gdown library makes downloading from Google Drive simple.
import os, gdown, subprocess

# File ID's for trajectory data stored on Google Drive.
file_IDs = {
  "Yamada":   "1vOSOU6z5RcUHeW_haTvzPPASjZTaRSez",
  "Pertz":    "1IJvH6uIAKf3DzL0UetH8H6MHy9U_8Y0K",
  "Angelini": "159IWCtQov4wAkhcNfcUwtdIvBLXLi6_R",
}

# Download each trajectory datafile.
for name, file_id in file_IDs.items():
  url = f"https://drive.google.com/uc?id={file_id}"
  zip_filepath = f"./../monolayer_cell_tracking/data/{name}.zip"
  extract_to_folder = f"./../monolayer_cell_tracking/data/"
  gdown.download(url, zip_filepath, quiet=False)
  command = ["unzip", "-o", zip_filepath, "-d", extract_to_folder]
  subprocess.run(command, capture_output=True, text=True, check=True)
  os.remove(zip_filepath)

from setuptools import setup, find_packages

setup(
    name="monolayer-cell-tracking",
    version="0.1.0",
    description="Computer vision package for extracting cell trajectories from microscopy videos.",
    author="Charles Packard",
    author_email="charles.robert.packard@gmail.com",
    url="https://github.com/crpackard/monolayer-cell-tracking",
    packages=find_packages(),
    install_requires=[
        "btrack",
        "numpy",
        "pandas",
        "tqdm",
        "imageio",
        "matplotlib",
        "cellpose",
        "shapely",
        "opencv-python",
        "gdown"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

from setuptools import setup, find_packages

setup(
  name="monolayer-cell-tracking",
  version="0.1.0",
  description="Computer vision package for extracting cell trajectories from microscopy videos.",
  long_description=open("README.md").read(),
  long_description_content_type="text/markdown",
  author="Charles Robert Packard",
  author_email="charles.robert.packard@gmail.com",
  url="https://github.com/crpackard/monolayer-cell-tracking",
  packages=find_packages(),
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
  python_requires=">=3.6",
  install_requires=[
      # Add your dependencies here, e.g., "numpy>=1.19.0"
  ],
)

# WORKS'2017: Example using NiW

**Jupyter notebook:**
* [GuardianGaza.ipynb](GuardianGaza.ipynb): the notebook version created after following guidelines; notebook used as example in the paper.
* [guardian_gaza-original.ipynb](guardian_gaza-original.ipynb): The original notebook downloaded from http://nbviewer.jupyter.org/gist/darribas/4121857.
* [guardian_gaza-fixed.ipynb](guardian_gaza-fixed.ipynb): the notebook version after fixing issue related to required key for the Google API use.

**Data:**
* [data.csv](data.csv): the data retrieved from the Google Fusion Table using the Google API.
* [modified-data.csv](modified-data): the csv file containing the data after changes in the notebook.

## Dependencies:**
### Instructions to install on Ubuntu.
**Proj4.9**
sudo apt-get install binutils libproj-dev gdal-bin

**GEOS**
sudo apt-get install libgeos-dev
sudo apt-get install libgeos++-dev
sudo apt-get install libgeos-3.5.0

**Cartopy**
sudo -H pip install cartopy

**PIL module**
sudo pip install image

**Scipy Spatial**
sudo pip install pysal
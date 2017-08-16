# WORKS'2017: Example using NiW

**Jupyter notebook:**
* [GuardianGaza.ipynb](GuardianGaza.ipynb): the notebook version created after following the guidelines proposed in the paper; notebook used as example in the paper.
* [guardian_gaza-original.ipynb](guardian_gaza-original.ipynb): the original notebook downloaded from http://nbviewer.jupyter.org/gist/darribas/4121857.
* [guardian_gaza-fixed.ipynb](guardian_gaza-fixed.ipynb): the notebook version after fixing issue related to required key for the use of Google API.

**Data:**
* [data.csv](data.csv): the data retrieved from the [Google Fusion Table](https://bit.ly/10dQEQl) using the Google API.
* [modified-data.csv](modified-data.csv): the csv file containing the data after changes in the notebook.

## Dependencies:
### Instructions to install on Ubuntu.
**Proj4.9**
```sh
sudo apt-get install binutils libproj-dev gdal-bin
```
**GEOS**
```sh
sudo apt-get install libgeos-dev
sudo apt-get install libgeos++-dev
sudo apt-get install libgeos-3.5.0
```
**Cartopy**
```sh
sudo pip install cartopy
```
**PIL module**
```sh
sudo pip install image
```
**Scipy Spatial**
```sh
sudo pip install pysal
```
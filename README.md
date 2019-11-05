# QCShapefiles
Scripts to assist QC'ing of interpretation of images.

## Overview

THE SHAPEFILES REFERRED TO ARE LOCATED AT:

\\TCMHarwell\Harwell\ProjectData\2019\PN19032_EAD_Habitat_Mapping\02_Processed_Data\WV_2014_HabitatMap\Habitat_Orthotile_Intersection.

THESE FILES CAN BE EDITED LOCALLY, BUT FOR THE SCRIPT TO WORK, THEY NEED TO BE REPLACED IN THE ABOVE DIRECTORY BEFORE RUNNING THE SCRIPTS

The scripts are run in two parts and creates a GUI for each part:

### extract_to_points_gui.py
- Extract to point (extract_to_points_gui.py):
Following the interpretation of habitat classes against imagery, this script can be run to fill in fields and extract the newly edited shapefile to the points shapefile. The edited shapefile will be saved with the same path, only prefixed with "...interp.shp". 

The only field that needs editing in the shapefile is HabitatSub (numeric code for habitat subtype). If any fields are changed, or if polygons are added/edited, the respective additional fields will be updated accordingly.

### fill_points_points_gui.py
- Fill QC point shapefile (fill_points_points_gui.py)
Following QC'ing of random point samples, this script can be run to fill in additional fields in the table. The edited point shapefile will be edited in place.

The only field that needs to be edited in the shapefile is QC_subNum (numeric code for habitat subtype). If any fields are changed, or if polygons are added/edited, the respective additional fields will be updated accordingly.

## Installing package

### Install Anaconda 
Download and install the Anaconda Python 3.x version from Anaconda [https://www.anaconda.com/distribution/#download-section]
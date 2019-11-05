# QCShapefiles
=================
Scripts to assist QC'ing of interpretation of images.

## Overview
=================
THE SHAPEFILES REFERRED TO ARE LOCATED AT:

\\TCMHarwell\Harwell\ProjectData\2019\PN19032_EAD_Habitat_Mapping\02_Processed_Data\WV_2014_HabitatMap\Habitat_Orthotile_Intersection.

THESE FILES CAN BE EDITED LOCALLY, BUT FOR THE SCRIPT TO WORK, THEY NEED TO BE REPLACED IN THE ABOVE DIRECTORY BEFORE RUNNING THE SCRIPTS

The scripts are run in two parts and creates a GUI for each part:

### extract_to_points_gui.py
- Extract to point (extract_to_points_gui.py):
Following the interpretation of habitat classes against imagery, this script can be run to fill in fields and extract the newly edited shapefile to the points shapefile. The edited shapefile will be saved with the same path, only prefixed with "...interp.shp". 

The only field that needs editing in the shapefile is HabitatSub (numeric code for habitat subtype). If any fields are changed, or if polygons are added/edited, the respective additional fields will be updated accordingly.

### fill_points_gui.py
- Fill QC point shapefile (fill_points_gui.py)
Following QC'ing of random point samples, this script can be run to fill in additional fields in the table. The edited point shapefile will be edited in place.

The only field that needs to be edited in the shapefile is QC_subNum (numeric code for habitat subtype). If any fields are changed, or if polygons are added/edited, the respective additional fields will be updated accordingly.

## Installing package
=====================

### Install Anaconda (This only needs to be done once)
Download and install the Anaconda Python 3.x version from [Anaconda](https://www.anaconda.com/distribution/#download-section).

### Set up environment (This only needs to be done once)
Once Anaconda is installed, open the Anaconda Prompt (Anaconda3) terminal from the start menu and and input the following:

```
(base) C:\Users\User>conda create --name qc_gui python=3.6

```
Type 'y' when prompted.
Change directory to the folder in which this package has been downloaded:

```
(base) C:\Users\User>cd Path/to/directory/of/QCShapfiles

```
### Start new environment (This should be done for each session):

```
(base) F:\Documents\QCShapfiles>conda activate qc_gui

(qc_gui) F:\Documents\QCShapfiles>

```

### Install packages (This only needs to be done once)
Install the python packages required to run the scripts. These packages are in the requirements.txt file in the package directory:

```
(qc_gui) F:\Documents\QCShapfiles>conda install -f -y -q --name qc_gui  --file requirements.txt

```

## Processing files and running scripts
=========================================

### Edit shapefiles and extract to points
1. Edit the habitat shapefiles accordingly, adding only values in the HabitatSub for the edits made. 
2. Once the edits have been carried, save the shapefile and remove if from the map project
3. In the Anaconda terminal, launch the extract_to_points_gui.py script:
```
(qc_gui) F:\Documents\QCShapfiles>python extract_to_points_gui.py

```
4. A gui should apear on the screen, and the python script in the terminal will keep running until the gui is closed or if an error is made.
5. Input the orthoID relating to the tile that has been edited (e.g. 'WV_WV_C18_L12').
6. Click 'Extract' and the script will run to fill in the missing/changed columns, and the new values will be extracted to a point shapefile. Check the Anaconda terminal for any errors.
7. The edited shapefile will be written to the same folder as the tile with the '_interp.shp' suffix.
8. Once all tiles have been processed, click 'Quit' to close the gui. Part 3 will need to be repeated to re-launch the gui.

### QC interpretations
1. During QC'ing, input only values in the 'QC_subNum' field.
2. Once QC'ing editing has been done, remove the point file from the map project and launch the fill_points_gui.py script:
```
(qc_gui) F:\Documents\QCShapfiles>python fill_points_gui.py

```
3. A gui should apear on the screen, and the python script in the terminal will keep running until the gui is closed or if an error is made.
4. Input the orthoID relating to the tile that has been edited along with the name of the person QC'ing.
5. Click "Complete attributes" to run the script to fill in additional fields.
6. Once all tiles have been processed, click 'Quit' to close the gui. Part 3 will need to be repeated to re-launch the gui.


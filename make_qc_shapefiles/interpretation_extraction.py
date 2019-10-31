"""Module with classes to:

ExtractInterpretationToPoints --> Extract values in edited interpretation to points

CompleteQCAttributes --> Fill in fields once QC has been carried out using QC_number

"""
from pathlib import Path
import geopandas as gpd
import pandas as pd
import numpy as np 
import sys

from make_qc_shapefiles.config import ROOT_DIR_TEST ###needs to be changed to server dir

ROOT_DIR = ROOT_DIR_TEST
CLS_CSV = Path(__file__).resolve().parent.joinpath('classes.csv')


class ExtractInterpretationToPoints:
    """
    Class to extract values from habitat layer to random points. This should be run after manual interpretation editing of the habitat layer has been done.

    The edited map needs to be saved in its original location as this script will point to that location
    """
    def __init__(self, orthoid):
        """
        orthoid:: (str) --> ID of tile that is being worked on.
        """
        if self.check_orthoid_exists(orthoid):
            self.orthoid = orthoid
        else:
            raise ValueError(f"Please check orthoid. There is no folder relating to this orthoid in {str(ROOT_DIR)}.")
        self.tile, self.point = self.get_shapefile_paths(self.orthoid)
        self.gdf_join = self.spatial_join(self.point, self.tile)

    def check_orthoid_exists(self, orthoid):
        """Returns true if folder exists for orthoid
        
        Parameters:
        orthoid:: (str) --> Orthoid for tile being QC'd

        Returns:
        Boolean:: (bool) --> True if exists, false if not
        """
        id_exists = False
        if orthoid in [x.name for x in ROOT_DIR.iterdir()]:
            id_exists = True 
        return id_exists

    def get_shapefile_paths(self, orthoid):
        """Returns paths for shapefiles
        
        Parameters:
        orthoid:: (str) --> Orthoid for tile

        Returns
        tile:: (Path) --> Path to tile shapefile
        point:: (Path) --> Path to point shapefile
        """
        tile = ROOT_DIR.joinpath(f'{orthoid}/{orthoid}.shp')
        point = ROOT_DIR.joinpath(f'{orthoid}/{orthoid}_points.shp')
        if not tile.exists() or not point.exists():
            raise FileNotFoundError("Point or tile shapefile is missing")
            sys.exit()
        else:
           return tile, point

    def spatial_join(self, point, tile):
        """Returns gdf of joined shapefiles, with only columns in point remaning (Num and Cls are filled from joined table)
        
        Parameters:
        point:: (Path) --> Path to point shapefile
        tile:: (Path) --> Path to tile shapefile

        Returns:
        gdf_join:: (gpd.GeoDataFrame) --> joined geodataframe with only point fields
        """
        gdf_pt = gpd.read_file(point)
        gdf_tile = gpd.read_file(tile)
        join_df = gpd.sjoin(gdf_pt, gdf_tile, op='within')
        join_df['Interp_cls'] = join_df['HabitatS_1']
        join_df['Interp_num'] = join_df['HabitatSub']
        cols = ['ID', 'Interp_cls', 'Interp_num', 'QC_cls', 'QC_num', 'QC_By', 'geometry']
        join_df = join_df[cols]
        return join_df
        
    def save_point_file(self, join_df, point):
        """Saves joined gdf to the same name as point (overwritten)"""
        join_df.to_file(point)

class CompleteQCAttributes:
    """Class to be run after numbers have been assigned to QC_num. Class will fill in appropriate class name to the QC_cls field and save the point shapefile to the same location"""
    def __init__(self, orthoid, name):
        """
        orthoid:: (str) --> Orthoid for tile being QC'd
        name:: (str) --> Name of person doing QC
        """
        if self.check_orthoid_exists(orthoid):
            self.orthoid = orthoid
        else:
            raise ValueError(f"Please check orthoid. There is no folder relating to this orthoid in {str(ROOT_DIR)}.")
        self.name = name
        self.point = self.get_shapefile_paths(self.orthoid)
        self.join_gdf = self.join_pt_to_csv(self.point, CLS_CSV)
        self.save_pt(self.join_gdf, self.point)


    def check_orthoid_exists(self, orthoid):
        """Returns true if folder exists for orthoid
        
        Parameters:
        orthoid:: (str) --> Orthoid for tile being QC'd

        Returns:
        Boolean:: (bool) --> True if exists, false if not
        """
        id_exists = False
        if orthoid in [x.name for x in ROOT_DIR.iterdir()]:
            id_exists = True 
        return id_exists

    def get_shapefile_paths(self, orthoid):
        """Returns paths for shapefiles
        
        Parameters:
        orthoid:: (str) --> Orthoid for tile

        Returns
        tile:: (Path) --> Path to tile shapefile
        point:: (Path) --> Path to point shapefile
        """
        point = ROOT_DIR.joinpath(f'{orthoid}/{orthoid}_points.shp')
        if not point.exists():
            raise FileNotFoundError("Point shapefile is missing")
            sys.exit()
        else:
           return point

    def join_pt_to_csv(self, point, csv):
        """Return gdf of point file joined with classes joined to csv and filled in
        
        Parameters:
        point:: (Path) --> Path to point shapefile
        csv:: (Path) --> Path to csv with classes
        """
        gdf = gpd.read_file(point)
        df = pd.read_csv(csv)
        df['QC_num'] = df['num']
        gdf = gdf.merge(df, on='QC_num', how='left')
        gdf['QC_cls'] = gdf['cls']
        cols = ['ID', 'Interp_cls', 'Interp_num', 'QC_cls', 'QC_num', 'QC_By', 'geometry']
        gdf = gdf[cols]
        return gdf

    def save_pt(self, gdf_join, point):
        """Saves gdf to original shapefile (overwrites)"""
        gdf_join['QC_By'] = self.name
        gdf_join.to_file(point)
"""Module with classes to:

ExtractInterpretationToPoints --> Extract values in edited interpretation to points

CompleteQCAttributes --> Fill in fields once QC has been carried out using QC_number

"""
from pathlib import Path
import geopandas as gpd
import pandas as pd
import numpy as np 
import sys

from make_qc_shapefiles.config import ROOT_DIR ###needs to be changed to server dir

#ROOT_DIR = ROOT_DIR_TEST
CLS_CSV = Path(__file__).resolve().parent.joinpath('classes.csv')
CLS_CSV_for_points = CLS_CSV.parent.joinpath('classes_for_points.csv')


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
        self.tile_overwritten = self.pre_fill_fields_based_on_Int_subNum(self.tile)
        self.gdf_join = self.spatial_join(self.point, self.tile_overwritten)
        self.save_point_file(self.gdf_join, self.point)
        print(f'{self.point.name} has been overwritten in the same location .\nPlease remove the shapefile from GIS and reload to see changes.')
        print(f'{self.tile_overwritten.name} has been saved with new habitat values')

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

    def pre_fill_fields_based_on_Int_subNum(self, tile):
        """Overwrites tile based on join between tile and CLS_CSV, filling all class fields based on tile 'Habitat_sub'
        
        Parameters
        tile:: (str/Path) --> Path to tile shapefile

        Returns
        tile:: (str/Path) --> Path to overwritten tile
        
        """
        df = pd.read_csv(CLS_CSV)
        gdf = gpd.read_file(tile)
        gdf_cols = gdf.columns
        df['HabitatSub'] = df['Int_SubNum']
        join_df = gdf.merge(df, on='HabitatSub', how='left')
        join_df['HabitatTyp'] = join_df['Int_num']
        join_df['HabitatT_1'] = join_df['Int_cls']
        join_df['HabitatS_1'] = join_df['Int_SubCls']
        join_df['MMU_HA'] = join_df['MMU_']
        join_df['Area_KM'] = join_df['geometry'].area / 10**6
        join_df['Area_HA'] = join_df['geometry'].area / 10**4
        #for i in range(len(join_df)):
        #    join_df['ID'][i] = i 
        join_df['Id'] = [x for x in range(len(join_df))]
        join_df['OrthoID'] = self.orthoid

        
        #Remove fields joined from table and save
        join_df = join_df[gdf_cols]
        out_tile = tile.parent.joinpath(tile.stem + '_interp.shp')
        join_df.to_file(out_tile)

        #return path to tile
        return out_tile

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
        join_df['Int_subCls'] = join_df['HabitatS_1']
        join_df['Int_subNum'] = join_df['HabitatSub']
        join_df['Int_cls'] = join_df['HabitatT_1']
        join_df['Int_num'] = join_df['HabitatTyp']
        cols = ['ID', 'Int_cls', 'Int_num', 'Int_subCls', 'Int_subNum',  'QC_cls', 'QC_num', 'QC_subCls', 'QC_subNum', 'QC_By', 'geometry']
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
        self.join_gdf = self.join_pt_to_csv(self.point, CLS_CSV_for_points)
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
        gdf['QC_subNum'] = gdf['QC_subNum'].astype(int)
        df = pd.read_csv(csv)
        df['QC_subNum'] = df['Int_SubNum_csv']
        gdf = gdf.merge(df, on='QC_subNum', how='left')
        gdf['QC_subCls'] = gdf['Int_SubCls_csv']
        gdf['QC_cls'] = gdf['Int_cls_csv']
        gdf['QC_subNum'] = gdf['Int_SubNum_csv'].astype(int)
        gdf['QC_num'] = gdf['Int_num_csv'].astype(int)
        print(gdf['QC_num'].dtype)
        cols = ['ID', 'Int_cls', 'Int_num', 'Int_subCls', 'Int_subNum', 'QC_cls', 'QC_num', 'QC_subNum', 'QC_subCls', 'QC_By', 'geometry']
        
        #gdf['Int_cls'] = gdf['Int_cls_x']
        #gdf['Int_num'] = gdf['Int_cls_x']
        gdf = gdf[cols]
        return gdf

    def save_pt(self, gdf_join, point):
        """Saves gdf to original shapefile (overwrites)"""
        if gdf_join['QC_subNum'].isnull().any():
            print(f"The following Point shp IDs' QC_nums are missing, incorrect or not valid. Please check these are correct and rerun function:\n {list(gdf_join['ID'][gdf_join['QC_subCls'].isnull()])}")
        schema = {
            'geometry': 'Point',
            'properties': {
                'QC_num': 'int',
                'QC_subNum': 'int',
        }}
        gdf_join['QC_By'] = self.name
        gdf_join.to_file(point)
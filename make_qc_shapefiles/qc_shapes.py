"""Module to split grid shapefile into constituent polygons, clip habitat map using individual grid tiles and also make 50 random points for each clipped tile"""
from pathlib import Path
import geopandas as gpd 

class MakeQCShapes:
    """Class to clip habitat map for each polygon in grid"""

    def __init__(self, grid, habitat, out_folder):
        """
        Initialisation

        Parameters:
        grid:: (Path/str) --> Path to grid shapefile in UTM39N 
        habitat:: (Path/str) --> Path to habitat shapefile for clipping
        out_folder:: (Path/str) --> Path to folder in which to save output. A new folder will be created in out_folder for each grid id. Inside the folder there will be a shapefile representing habitat interpretation and a point shapefile of 50 random points for QC

        Returns
        None
        """
        self.grid = grid
        self.habitat = habitat
        self.out_folder = out_folder
        self.grid_gdf, self.hab_gdf = self.get_gdf(self.grid, self.habitat)

    def get_gdf(self, grid, habitat):
        """Returns geodataframes for grid and habitat shapefiles
        
        Parameters:
        grid:: (Path/str) --> Path to grid shapefile in UTM39N 
        habitat:: (Path/str) --> Path to habitat shapefile for clipping

        Returns:
        grid_gdf:: (gpd.GeoDataFrame) --> gdf of grid shp
        hab_gdf:: (gpd.GeoDataFrame) --> gdf of habitat shp        
        """
        grid_gdf = gpd.read_file(str(grid))
        hab_gdf = gpd.read_file(str(habitat))
        return grid_gdf, hab_gdf
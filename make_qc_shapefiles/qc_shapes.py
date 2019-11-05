"""Module to split grid shapefile into constituent polygons, clip habitat map using individual grid tiles and also make 50 random points for each clipped tile"""
from pathlib import Path
import geopandas as gpd
from shapely.geometry import Point
import random
import fiona
import numpy as np

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
        self.intersect_grid_with_habitat(self.grid_gdf, self.hab_gdf)
        self.make_random_points(self.out_folder)

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

    def intersect_grid_with_habitat(self, grid_gdf, hab_gdf):
        """Returns list of geodataframes where grid_gdf intersects hab_gdf"""
        with open('missing_joins.txt', 'w+') as f:
            for _, grid_tile in grid_gdf.iterrows():
                tile = gpd.GeoDataFrame({'OrthoID': [grid_tile['OrthoID']], 'geometry': [grid_tile['geometry']]})
                tile.crs = {'init' :'epsg:32639'}
                gdf_sub = gpd.overlay(tile, hab_gdf, how='intersection')
                tile_folder = self.out_folder.joinpath(f'{grid_tile["OrthoID"]}')
                if not tile_folder.exists():
                    tile_folder.mkdir(parents=True, exist_ok=True)
                outfile = tile_folder.joinpath(f'{grid_tile["OrthoID"]}.shp')
                gdf_sub.crs = {'init' :'epsg:32639'}
                if not gdf_sub.empty:
                    gdf_sub.to_file(outfile)
                else:
                    f.write(grid_tile['OrthoID'] + '\n')

    def make_random_points(self, out_folder, num_points=50):
        """Creates num_points randomly within each polygon of grid_gdf"""
        folders = [x for x in out_folder.iterdir() if x.name.startswith('WV_')]
        for folder in folders:
            shp = folder.joinpath(f'{folder.name}.shp')
            grid_gdf = gpd.read_file(shp)
            grid_gdf = grid_gdf.dissolve(by=f'OrthoID')
            for _, orthoid in grid_gdf.iterrows():
                points = self.random_points_in_polygon(num_points, orthoid['geometry'])
                gdf = gpd.GeoDataFrame({'ID': range(50), 'geometry': points})
                gdf['Int_cls'] = ""
                gdf['Int_num'] = np.empty(50, dtype=np.int64)
                gdf['Int_num'] = 0
                gdf['Int_subCls'] = ""
                gdf['Int_subNum'] = np.empty(50, dtype=np.int64)
                gdf['Int_subNum'] = 0
                gdf['QC_cls'] = ""
                gdf['QC_num'] = np.empty(50, dtype=np.int64)
                gdf['QC_num'] = 0
                gdf['QC_subCls'] = ""
                gdf['QC_subNum'] = np.empty(50, dtype=np.int64)
                gdf['QC_subNum'] = 0
                gdf['QC_By'] = ""
                cols = ['ID', 'Int_cls', 'Int_num', 'Int_subCls', 'Int_subNum', 'QC_cls', 'QC_num', 'QC_subCls', 'QC_subNum', 'QC_By', 'geometry']
                gdf = gdf[cols]
                point_folder = self.out_folder.joinpath(f'{folder.name}')
                assert point_folder.exists()
                point_shp = point_folder.joinpath(f'{folder.name}_points.shp')
                gdf.crs = {'init' :'epsg:32639'}
                gdf.to_file(point_shp, na_rep='NULL')

    def random_points_in_polygon(self, number, polygon):
        """Returns n number random points generated within polygon"""
        points = []
        min_x, min_y, max_x, max_y = polygon.bounds
        i= 0
        while i < number:
            point = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
            if polygon.contains(point):
                points.append(point)
                i += 1
        return points  # returns list of shapely point

def make_random_points(out_folder, num_points=50):
        """Creates num_points randomly within each polygon of grid_gdf"""
        folders = sorted([x for x in out_folder.iterdir() if x.name.startswith('WV_')])
        for folder in folders:
            shp = folder.joinpath(f'{folder.name}.shp')
            grid_gdf = gpd.read_file(shp)
            grid_gdf = grid_gdf.dissolve(by=f'OrthoID')
            for _, orthoid in grid_gdf.iterrows():
                points = random_points_in_polygon(num_points, orthoid['geometry'])
                gdf = gpd.GeoDataFrame({'ID': range(50), 'geometry': points})
                gdf['Int_cls'] = ""
                gdf['Int_num'] = np.empty(50, dtype=np.int64)
                gdf['Int_num'] = 0
                gdf['Int_subCls'] = ""
                gdf['Int_subNum'] = np.empty(50, dtype=np.int64)
                gdf['Int_subNum'] = 0
                gdf['QC_cls'] = ""
                gdf['QC_num'] = np.empty(50, dtype=np.int64)
                gdf['QC_num'] = 0
                gdf['QC_subCls'] = ""
                gdf['QC_subNum'] = np.empty(50, dtype=np.int64)
                gdf['QC_subNum'] = 0
                gdf['QC_By'] = ""
                cols = ['ID', 'Int_cls', 'Int_num', 'Int_subCls', 'Int_subNum', 'QC_cls', 'QC_num', 'QC_subCls', 'QC_subNum', 'QC_By', 'geometry']
                gdf = gdf[cols]
                point_folder = out_folder.joinpath(f'{folder.name}')
                assert point_folder.exists()
                point_shp = point_folder.joinpath(f'{folder.name}_points.shp')
                gdf.crs = {'init' :'epsg:32639'}
                gdf.to_file(point_shp, na_rep='NULL')

def random_points_in_polygon(number, polygon):
    """Returns n number random points generated within polygon"""
    points = []
    min_x, min_y, max_x, max_y = polygon.bounds
    i= 0
    while i < number:
        point = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
        if polygon.contains(point):
            points.append(point)
            i += 1
    return points  # returns list of shapely point


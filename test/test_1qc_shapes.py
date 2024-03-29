from pathlib import Path
import pytest
import geopandas as gpd
import numpy as np 
import pandas as pd

from make_qc_shapefiles.qc_shapes import MakeQCShapes, make_random_points

BASE_DIR = Path(__file__).resolve().parent.parent

GRID = BASE_DIR.joinpath('test/test_data/test_data_in/tile_shp/test_tiles.shp')
HABITAT = GRID.parent.parent.joinpath('habitat_shp/test_habitat.shp')
OUT_FOLDER = BASE_DIR.joinpath('test/test_data/test_data_out')

@pytest.fixture
def qc_cls():
    """Set up basic test class"""
    x = MakeQCShapes(GRID, HABITAT, OUT_FOLDER)
    yield x
    

def test_class_set_up_with_test_data_and_data_exists(qc_cls):
    """Test instance and data exists"""
    assert isinstance(qc_cls, MakeQCShapes)
    assert qc_cls.grid.exists()
    assert qc_cls.habitat.exists()
    assert qc_cls.out_folder.exists()

def test_gdf_of_shps_made(qc_cls):
    """Are gdf made for both shps"""
    grid_gdf, hab_gdf = qc_cls.grid_gdf, qc_cls.hab_gdf
    assert isinstance(grid_gdf, gpd.GeoDataFrame)
    assert isinstance(hab_gdf, gpd.GeoDataFrame)
    assert list(hab_gdf.columns) == ['Id', 'HabitatTyp', 'HabitatT_1', 'HabitatSub', 'HabitatS_1', 'Area_KM', 'Area_HA', 'MMU_HA', 'RuleID', 'Shape_Leng', 'Shape_Area', 'geometry']
    assert list(grid_gdf.columns) == ['NAME', 'OrthoID', 'geometry']
    assert int(hab_gdf['Id'][142]) == 39446
    assert grid_gdf['NAME'][4] == 'C19_L13'
    assert grid_gdf.crs == {'init': 'epsg:32639'}
    assert hab_gdf.crs == {'init': 'epsg:32639'}

def test_shapefiles_made_for_each_tile(qc_cls):
    """Shapefile made for each of the tiles"""
    out_folders = [x for x in qc_cls.out_folder.iterdir()if not x.name == 'test']
    shps = []
    for folder in out_folders:
        shps.append([x.name for x in folder.iterdir() if x.name.endswith('.shp') if not x.name.endswith('points.shp')][0])
    assert len(out_folders) == 9
    assert 'WV_C19_L12.shp' in shps

def test_random_points_saved_in_tile_folder(qc_cls):
    """Test random points are saved in the folder with the tile and the points are contained by the tile"""
    #qc_cls.make_random_points(qc_cls.out_folder)
    out_folders = [x for x in qc_cls.out_folder.iterdir() if x.name.startswith('WV_')]
    shps = []
    for folder in out_folders:
        shps.append([x.name for x in folder.iterdir() if x.name.endswith('points.shp')][0])
    assert 'WV_C19_L12_points.shp' in shps
    gdf_poly = gpd.read_file(str(BASE_DIR.joinpath('test/test_data/test_data_in/QC_Dissolved.shp')))
    gdf_point = gpd.read_file(str(BASE_DIR.joinpath('test/test_data/test_data_out/WV_C20_L14/WV_C20_L14_points.shp')))
    for _, i in gdf_point.iterrows():
        assert gdf_poly['geometry'].contains(i['geometry']).all()
    assert gdf_point['Int_num'].dtype == np.int64
    assert gdf_point['QC_num'].dtype == np.int64
    cols = ['ID', 'Int_cls', 'Int_num', 'Int_subCls', 'Int_subNum', 'QC_cls', 'QC_num', 'QC_subCls', 'QC_subNum', 'QC_By', 'geometry']
    assert list(gdf_point.columns) == cols

@pytest.mark.random_function
def test_standalone_make_random_points_function():
    """Calling ONLY make_random_points function without object"""
    out_folder = BASE_DIR.joinpath('test/test_data/test_data_out/test')
    make_random_points(out_folder)
    shps = []
    for folder in out_folder.iterdir():
        shps.append([x.name for x in folder.iterdir() if x.name.endswith('points.shp')][0])
    assert 'WV_C18_L12_points.shp' in shps
    gdf_poly = gpd.read_file(str(BASE_DIR.joinpath('test/test_data/test_data_in/QC_Dissolved.shp')))
    gdf_point = gpd.read_file(str(BASE_DIR.joinpath('test/test_data/test_data_out/WV_C18_L12/WV_C18_L12_points.shp')))
    for _, i in gdf_point.iterrows():
        #assert gdf_poly['geometry'].contains(i['geometry']).all()
        assert gdf_point['Int_num'].dtype == np.int64
        assert gdf_point['QC_num'].dtype == np.int64

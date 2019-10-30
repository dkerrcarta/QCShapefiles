from pathlib import Path
import pytest
import geopandas as gpd

from make_qc_shapefiles.qc_shapes import MakeQCShapes 

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
 
    
from itertools import cycle
import pytest 
from pathlib import Path

import geopandas as gpd
import pandas as pd

from make_qc_shapefiles.config import ROOT_DIR_TEST
from make_qc_shapefiles.interpretation_extraction import CompleteQCAttributes, CLS_CSV_for_points

BASE_DIR = Path(__file__).resolve().parent

def test_classes_csv_in_place():
    """Checks if classes csv exists"""
    assert CLS_CSV_for_points.exists()

@pytest.fixture
def comp_qc():
    """Sets up test class"""
    ## Logic to imitate QC ##
    gdf = gpd.read_file(str(BASE_DIR.joinpath('test_data/test_data_out/WV_C18_L12/WV_C18_L12_points.shp')))
    df = pd.read_csv(CLS_CSV_for_points)
    df = list(df['Int_SubNum_csv'])[1:51]
    seq = cycle(df)
    gdf['QC_subNum'] = [next(seq) for count in range(gdf.shape[0])]
    gdf.to_file(str(BASE_DIR.joinpath('test_data/test_data_out/WV_C18_L12/WV_C18_L12_points.shp')))
    ## Logic to imitate QC ##
    x = CompleteQCAttributes('WV_C18_L12', 'David')
    yield x

def test_class_set_up(comp_qc):
    """Checks object set up"""
    assert isinstance(comp_qc, CompleteQCAttributes)

def test_exception_raised_if_wrong_orthod_id_input():
    """Check raises exception if orthoid incorrect"""
    with pytest.raises(ValueError):
        CompleteQCAttributes('WRONG_ORTHOID', 'David')

def test_shapefiles_exist_in_orthoid_folder(comp_qc):
    """Test function to check if shapefiles exist in folder and if so, assign them to variables"""
    point = comp_qc.point
    assert point.exists()
    assert point.name == 'WV_C18_L12_points.shp'

def test_spatial_join_is_successful(comp_qc):
    """Check join between shape and class csv"""
    join_gdf = comp_qc.join_gdf
    df = pd.read_csv(CLS_CSV_for_points)
    df['QC_subNum'] = df['Int_SubNum_csv']
    join_gdf = join_gdf.merge(df, on='QC_subNum', how='left')
    #assert list(join_gdf['QC_subCls']) == list(join_gdf['Int_SubCls'])

def test_point_shapefile_saved(comp_qc):
    gdf = gpd.read_file(comp_qc.point)
    assert gdf['QC_By'].all() == 'David'
    assert 'Saltmarsh' in list(gdf['QC_subCls'])
    assert gdf['QC_cls'][47] == 'Plantations' 
import pytest 
from pathlib import Path

import geopandas as gpd

from make_qc_shapefiles.config import ROOT_DIR_TEST
from make_qc_shapefiles.interpretation_extraction import ExtractInterpretationToPoints

def test_root_dir_exists():
    """Check config file import directory"""
    assert ROOT_DIR_TEST.exists()
    folders = [x for x in ROOT_DIR_TEST.iterdir()]
    assert len(folders) == 10
    assert "WV_C18_L13" in [x.name for x in folders]
    print(ROOT_DIR_TEST)

@pytest.fixture
def extr():
    """Set up ExtractInterpretationToPoints object"""
    x = ExtractInterpretationToPoints('WV_C18_L12')
    yield x 

def test_class_object_made(extr):
    """Check object made"""
    assert isinstance(extr, ExtractInterpretationToPoints)
    assert extr.orthoid == 'WV_C18_L12'

def test_exception_raised_if_wrong_orthod_id_input():
    """Check raises exception if orthoid incorrect"""
    with pytest.raises(ValueError):
        ExtractInterpretationToPoints('WRONG_ORTHOID')

def test_shapefiles_exist_in_orthoid_folder(extr):
    """Test function to check if shapefiles exist in folder and if so, assign them to variables"""
    tile, point = extr.tile, extr.point
    assert tile.exists()
    assert point.exists()
    assert tile.name == 'WV_C18_L12.shp'
    assert point.name == 'WV_C18_L12_points.shp'

@pytest.mark.skip(reason="This file will exist when test is run. This file needs to be removed manually for test to pass")
def test_error_raised_if_file_not_found():
    """Error raised if shapefile(s) not present in orthoid folder"""
    
    with pytest.raises(FileNotFoundError):
        ExtractInterpretationToPoints('WV_C18_L13')

def test_fields_pre_filled_and_overwritten(extr):
    """Overwrite sub class fields in shapefile and test that function fills them as expected"""
    gdf = gpd.read_file(extr.tile)
    gdf['HabitatSub'] = 9240
    gdf.to_file('dummy_test_shp.shp')
    tile_overwritten = extr.pre_fill_fields_based_on_Int_subNum('dummy_test_shp.shp')
    gdf = gpd.read_file(tile_overwritten)
    assert gdf['HabitatSub'][2] == 9240
    assert gdf['HabitatT_1'][2] == 'Urban habitat types'
    assert gdf['HabitatTyp'][2] == 9000
    assert gdf['HabitatS_1'][2] == 'Other industry'


def test_join_is_successful_between_point_and_polygon(extr):
    """Check join between point and polygon is successful by checking values match between cols"""
    join_df = extr.gdf_join
    expected_df = gpd.sjoin(gpd.read_file(extr.point), gpd.read_file(extr.tile), op='within')
    num_ = expected_df['HabitatTyp']
    cls_ = expected_df['HabitatT_1']
    assert isinstance(join_df, gpd.GeoDataFrame)
    assert list(join_df.columns) == ['ID', 'Int_cls', 'Int_num', 'Int_subCls', 'Int_subNum',  'QC_cls', 'QC_num', 'QC_subCls', 'QC_subNum', 'QC_By', 'geometry']
    assert list(join_df['Int_cls']) == list(cls_)
    assert list(join_df['Int_num']) == list(num_)

def test_points_shapefile_saved_with_join(extr):
    """Test points shapefile saved"""
    extr.save_point_file(extr.gdf_join, extr.point)
    gdf = gpd.read_file(extr.point)
    expected_num = extr.gdf_join['Int_num'][15]
    num = gdf['Int_num'][15]
    expected_cls = extr.gdf_join['Int_cls'][15]
    cls_ = gdf['Int_cls'][15]    
    assert extr.point.exists()
    assert expected_num == num
    assert expected_cls == cls_





    

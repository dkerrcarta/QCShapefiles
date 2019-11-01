from pathlib import Path
from make_qc_shapefiles.qc_shapes import MakeQCShapes, make_random_points

BASE_DIR = Path(__file__).resolve().parent

GRID = BASE_DIR.parent.joinpath('data/datain/tile_shp/PN19032_THabitat_UTM39N.shp')
HABITAT = BASE_DIR.parent.joinpath('data/datain/habitat_shp/habitat_UTM39N.shp')
OUT_FOLDER = BASE_DIR.parent.joinpath('data/Habitat_Orthotile_Intersection')
#OUT_FOLDER = BASE_DIR.parent.joinpath(r'\\TCMHarwell\Harwell\ProjectData\2019\PN19032_EAD_Habitat_Mapping\02_Processed_Data\WV_2014_HabitatMap\Habitat_Orthotile_Intersection')

def main(): 
    ### Clips habitat to tiles if habitat intersects tiles
    ### Makes 50 random points inside each shapefile
    #MakeQCShapes(GRID, HABITAT, OUT_FOLDER)

    ##Makes only 50 random points inside shapefiles in OUTFOLDER
    make_random_points(OUT_FOLDER)



if __name__ == "__main__":
    main()
from arcpy import CopyFeatures_management, CopyRaster_management,\
    TableToTable_conversion


# default extensions for layer tyeps
SHAPEFILE_EXT = ".shp"
DEFAULT_RASTER_EXT = ".img"
DEFAULT_TABLE_EXT = ".dbf"

# ArcGIS type codes for different layer types
FC_TYPECODE = "FeatureClass"
RASTER_TYPECODE = "RasterDataset"
TABLE_TYPECODE = "Table"

# default function for copying data of each layer type
COPY_FUNCTION = {
    FC_TYPECODE: CopyFeatures_management,
    RASTER_TYPECODE: CopyRaster_management,
    TABLE_TYPECODE: TableToTable_conversion,
}

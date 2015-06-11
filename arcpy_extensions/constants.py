from arcpy import CopyFeatures_management, CopyRaster_management,\
    TableToTable_conversion, Copy_management


# default extensions for layer tyeps
DEFAULT_FC_EXT = ".shp"
DEFAULT_RASTER_EXT = ".img"
DEFAULT_TABLE_EXT = ".dbf"

# ArcGIS type codes for different layer types
DATASET_TYPECODE = "FeatureDataset"
FC_TYPECODE = "FeatureClass"
RASTER_TYPECODE = "RasterDataset"
TABLE_TYPECODE = "Table"

# default function for copying data of each layer type
LAYER_TYPES = {
    "DEFAULT": {"copy_function": Copy_management,
                "extension": ""},
    FC_TYPECODE: {"copy_function": CopyFeatures_management,
                  "extension": DEFAULT_FC_EXT},
    RASTER_TYPECODE: {"copy_function": CopyRaster_management,
                      "extension": DEFAULT_RASTER_EXT},
    TABLE_TYPECODE: {"copy_function": TableToTable_conversion,
                     "extension": DEFAULT_TABLE_EXT},
}

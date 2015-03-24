import os
from logging import exception
from arcpy import ListFeatureClasses, ListRasters, ListTables, Describe
from arcpy import CopyFeatures_management, CopyRaster_management, TableToTable_conversion
from arcpy import env, ExecuteError
from utilities import generate_random_name
from constants import RASTER_TYPECODE, FC_TYPECODE, TABLE_TYPECODE,\
    SHAPEFILE_EXT, DEFAULT_RASTER_EXT, DEFAULT_TABLE_EXT



# *************** CONSTANTS ***************

# none

# **************** CLASSES ****************

class GeodatabaseError(Exception):
    pass


class Geodatabase(object):
    """
    """
    def __init__(self, path, fcs, rasters, tables):
        """Initialize the class.

        Required:  path - path to the geodatabase
                   fcs - list of feature classes in the gdb
                   rasters - list of rasters in the gdb
                   tables - list of tables in the gdb
        """
        self.path = path
        self.featureclasses = fcs
        self.rasterlayers = rasters
        self.tables = tables

    @classmethod
    def open_GDB(self, path):
        """
        """
        workspace = env.workspace
        env.workspace = path

        self.validate_geodatabase(path)

        fcs     = ListFeatureClasses()
        rasters = ListRasters()
        tables  = ListTables()

        env.workspace = workspace

        return Geodatabase(path, fcs, rasters, tables)

    @staticmethod
    def validate_geodatabase(path):
        """
        """
        try:
            desc = Describe(path)
            assert desc.DataType == 'Workspace'
            assert desc.workspacetype == 'LocalDatabase'
        except IOError as e:
            raise GeodatabaseError(e)
        except AssertionError:
            raise GeodatabaseError("{} is not a valid geodatabase.".format(path))

    def get_layers_dict(self):
        """
        Returns a dictionary of the geodatabase layers in the format:

            {RasterType: [list], FCType: [list], TableType: [list]}

        where the types are the ESRI types, set in the constants at the
        top of this file.
        """
        return {RASTER_TYPECODE: self.rasterlayers,
                FC_TYPECODE: self.feature_class_to_shapefile,
                TABLE_TYPECODE: self.tables}

    # TODO: convert to take layer type as argument, not function, and to detect if type not supplied
    # TODO: refactor into a public method
    def _layer_to_file(self, layer, extension, outputdirectory, copy_function,
                       outname=None):
        """
        """
        if outname:
            newname = outname
        else:
            # use same name as layer
            newname = layer

        if featureclass not in self.featureclasses:
            raise GeodatabaseError("{} not found in geodatabase.".format(featureclass))

        if not outputdirectory:
            outputdirectory = env.workspace

        if not extension.startswith("."):
            extension = "." + extension

        newlayer = os.path.join(outputdirectory, newname + extension)
        layer = os.path.join(self.path, layer)

        copy_function(layer, newlayer)

        return newlayer

    def _layer_to_file_multiple(self, layers, extension, outputdirectory, copy_function):
        """
        """
        converted = []

        for layer in layers:
            try:
                converted.append(_layer_to_file(layer, extension, outputdirectory, copy_function))
            except Exception as e:
                exception(e)
                print "Failed to convert layer {}.".format(layer)

        return converted

    def feature_class_to_shapefile(self, featureclass, outputdirectory,
                                   outname_to_use=None):
        """
        """
        return self._layer_to_file(featureclass,
                                   SHAPEFILE_EXT,
                                   outputdirectory,
                                   CopyFeatures_management,
                                   outname=outname_to_use)

    def feature_class_to_shapefile_multiple(self, outputdirectory,
                                            outputname=None
                                            featureclasses=None):
        """
        """
        if not featureclasses:
            featureclasses = self.featureclasses

        newfcs = _layer_to_file_multiple(
                featureclasses,
                SHAPEFILE_EXT,
                outputdirectory,
                CopyFeatures_management)
            )

        return newfcs

    def raster_layer_to_file(self, rasterlayer, outputdirectory,
                             rasterformat=DEFAULT_RASTER_FORMAT,
                             outname_to_use=None):
        """
        """
        return self._layer_to_file(rasterlayer,
                                   rasterformat,
                                   outputdirectory,
                                   CopyRaster_management,
                                   outname=outname_to_use)

    def raster_layer_to_file_multiple(self, outputdirectory,
                                      rasterlayers=None,
                                      rasterformat=DEFAULT_TABLE_FORMAT,
                                      outname_to_use=None):
        """
        """
        if not rasterlayers:
            rasterlayers = self.rasterlayers

        newrasters = _layer_to_file_multiple(
                featureclasses,
                rasterformat,
                outputdirectory,
                CopyFeatures_management)
            )

        return newfcs

    def table_to_file(self, table, outputdirectory,
                      tableformat=DEFAULT_TABLE_FORMAT,
                      outname=None):
        """
        """
        return self._layer_to_file(table,
                                   tableformat,
                                   outputdirectory,
                                   TableToTable_conversion,
                                   outname=outname)

    def table_to_file_multiple(self, outputdirectory,
                               tables=None,
                               tabularformat=DEFAULT_TABLE_FORMAT):
        """
        """
        if not tables:
            tables = self.tables

        newfcs = _layer_to_file_multiple(
                featureclasses,
                tabularformat,
                outputdirectory,
                CopyFeatures_management)
            )

        return newfcs

    def all_layers_to_files(self, outputdirectory, rasterformat=DEFAULT_RASTER_FORMAT,
                            tabularformat=DEFAULT_TABLE_FORMAT):
        """
        """
        copied = []
        copied += self.feature_class_to_shapefile_multiple(outputdirectory)
        copied += self.raster_layer_to_file_multiple(outputdirectory,
                                                     rasterformat=rasterformat)
        copied += self.table_to_file_multiple(outputdirectory,
                                              tabularformat=tabularformat)

        return copied


# *************** MAIN CHECK ***************

if __name__ == '__main__':
    pass

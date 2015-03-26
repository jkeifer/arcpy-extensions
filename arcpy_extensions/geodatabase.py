import os
from logging import exception
from arcpy import ListFeatureClasses, ListRasters, ListTables, Describe,\
    env, Copy_management
from constants import RASTER_TYPECODE, FC_TYPECODE, TABLE_TYPECODE,\
    SHAPEFILE_EXT, DEFAULT_RASTER_EXT, DEFAULT_TABLE_EXT, COPY_FUNCTION


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

        fcs = ListFeatureClasses()
        rasters = ListRasters()
        tables = ListTables()

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
            raise GeodatabaseError("{} is not a valid geodatabase."
                                   .format(path))

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

    def _layer_to_file(self, layer, layer_type, extension, outputdirectory,
                       outname=None):
        """
        """
        if outname:
            newname = outname
        else:
            # use same name as layer
            newname = layer

        if layer not in self.get_layers_dict()[layer_type]:
            raise GeodatabaseError("{} not found in geodatabase."
                                   .format(layer))

        if not outputdirectory:
            outputdirectory = env.workspace

        if not extension.startswith("."):
            extension = "." + extension

        newlayer = os.path.join(outputdirectory, newname + extension)
        layer = os.path.join(self.path, layer)

        copy_function = COPY_FUNCTION.pop(layer_type, Copy_management)
        copy_function(layer, newlayer)

        return newlayer

    def _layer_to_file_multiple(self, layers, layers_type, extension,
                                outputdirectory):
        """
        """
        converted = []

        for layer in layers:
            try:
                converted.append(self._layer_to_file(layer,
                                                     layers_type,
                                                     extension,
                                                     outputdirectory))
            except Exception as e:
                exception(e)
                print "Failed to convert layer {}.".format(layer)

        return converted

    def feature_class_to_shapefile(self, featureclass, outputdirectory,
                                   outname_to_use=None):
        """
        """
        return self._layer_to_file(featureclass,
                                   FC_TYPECODE,
                                   SHAPEFILE_EXT,
                                   outputdirectory,
                                   outname=outname_to_use)

    def feature_class_to_shapefile_multiple(self, outputdirectory,
                                            outputname=None,
                                            featureclasses=None):
        """
        """
        if not featureclasses:
            featureclasses = self.featureclasses

        newfcs = self._layer_to_file_multiple(
            featureclasses,
            FC_TYPECODE,
            SHAPEFILE_EXT,
            outputdirectory,
        )

        return newfcs

    def raster_layer_to_file(self, rasterlayer, outputdirectory,
                             rasterformat=DEFAULT_RASTER_EXT,
                             outname_to_use=None):
        """
        """
        return self._layer_to_file(rasterlayer,
                                   RASTER_TYPECODE,
                                   rasterformat,
                                   outputdirectory,
                                   outname=outname_to_use)

    def raster_layer_to_file_multiple(self, outputdirectory,
                                      rasterlayers=None,
                                      rasterformat=DEFAULT_TABLE_EXT,
                                      outname_to_use=None):
        """
        """
        if not rasterlayers:
            rasterlayers = self.rasterlayers

        newrasters = self._layer_to_file_multiple(
            rasterlayers,
            RASTER_TYPECODE,
            rasterformat,
            outputdirectory,
        )

        return newrasters

    def table_to_file(self, table, outputdirectory,
                      tableformat=DEFAULT_TABLE_EXT,
                      outname=None):
        """
        """
        return self._layer_to_file(table,
                                   TABLE_TYPECODE,
                                   tableformat,
                                   outputdirectory,
                                   outname=outname)

    def table_to_file_multiple(self, outputdirectory,
                               tables=None,
                               tabularformat=DEFAULT_TABLE_EXT):
        """
        """
        if not tables:
            tables = self.tables

        newtables = self._layer_to_file_multiple(
            tables,
            TABLE_TYPECODE,
            tabularformat,
            outputdirectory,
        )

        return newtables

    def all_layers_to_files(self, outputdirectory,
                            rasterformat=DEFAULT_RASTER_EXT,
                            tabularformat=DEFAULT_TABLE_EXT):
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

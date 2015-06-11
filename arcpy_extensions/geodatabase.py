import os
from arcpy import ListFeatureClasses, ListRasters, ListTables, ListDatasets,\
    Describe, env, CreateFileGDB_management
from layer import Layer
from constants import RASTER_TYPECODE, FC_TYPECODE, TABLE_TYPECODE,\
    DATASET_TYPECODE


# *************** CONSTANTS ***************

# none


# **************** CLASSES ****************

class GeodatabaseError(Exception):
    pass


class Geodatabase(object):
    """
    """
    def __init__(self, path, datasets=None, fcs=None,
                 rasters=None, tables=None):
        """Initialize the class.

        Required:  path - path to the geodatabase
                   fcs - list of feature classes in the gdb
                   rasters - list of rasters in the gdb
                   tables - list of tables in the gdb
        """
        self.name = os.path.basename(path)
        self.path = path
        self.contents = {
            DATASET_TYPECODE: {},
            FC_TYPECODE: {},
            RASTER_TYPECODE: {},
            TABLE_TYPECODE: {},
        }

        #if datasets:
        #    for dataset in datasets:
        #        self.contents[DATASET_TYPECODE][dataset.name] = dataset


        for fc in fcs:
            self.contents[FC_TYPECODE][fc.name] = fc

        for raster in rasters:
            self.contents[RASTER_TYPECODE][raster.name] = raster

        for table in tables:
            self.contents[TABLE_TYPECODE][table.name] = table

    @property
    def featuredatasets(self):
        return self.contents[DATASET_TYPECODE].values()

    @property
    def featureclasses(self):
        return self.contents[FC_TYPECODE].values()

    @property
    def rasters(self):
        return self.contents[RASTER_TYPECODE].values()

    @property
    def tables(self):
        return self.contents[TABLE_TYPECODE].values()

    @classmethod
    def New(cls, output_dir, name, version="CURRENT"):
        result = CreateFileGDB_management(output_dir, name, version=version)
        return Geodatabase(result.getOutput(0))

    @classmethod
    def Open(cls, path):
        """
        """
        # change the arcpy workspace for listing, but save the current setting
        workspace = env.workspace
        env.workspace = path

        cls.validate_geodatabase(path)

        # TODO: Need a generic workspace class, and a dataset class
        datasets = ListDatasets()
        fcs_names = ListFeatureClasses()
        rasters_names = ListRasters()
        tables_names = ListTables()

        # take all the found layers and make into layer objects
        fcs = []
        for fc in fcs_names:
            fcs.append(Layer(os.path.join(path, fc)))

        rasters = []
        for raster in rasters_names:
            rasters.append(Layer(os.path.join(path, raster)))

        tables = []
        for table in tables_names:
            tables.append(Layer(os.path.join(path, table)))

        # set the workspace back for the user
        env.workspace = workspace

        return Geodatabase(path, datasets, fcs, rasters, tables)

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

#    def as_dictionary(self):
#        """
#        Returns a dictionary of the geodatabase layer names in the format:
#
#            {RasterType: [list], FCType: [list], TableType: [list]}
#
#        where the types are the ESRI types, set in the constants at the
#        top of this file.
#        """
#        return {
#
#            RASTER_TYPECODE: [l.name for l in self.rasterlayers],
#            FC_TYPECODE: [l.name for l in self.featureclasses],
#            TABLE_TYPECODE: [l.name for l in self.tables],
#        }

    def add_dataset(self, dataset):
        raise NotImplementedError

    def add_layer(self, layer):
        if type(layer) != type(Layer):
            layer = Layer(layer)

        if layer.workspace == self.path:
            if layer.dataset:
                raise NotImplementedError
            else:
                self.contents[layer.type][layer.name] = layer
        else:
            layer.copy_to_geodatabase(self)



#    def _layer_to_file(self, layer, layer_type, extension, outputdirectory,
#                       outname=None):
#        """
#        """
#        if outname:
#            newname = outname
#        else:
#            # use same name as layer
#            newname = layer
#
#        if layer not in self.get_layers_dict()[layer_type]:
#            raise GeodatabaseError("{} not found in geodatabase."
#                                   .format(layer))
#
#        if not outputdirectory:
#            outputdirectory = env.workspace
#
#        if not extension.startswith("."):
#            extension = "." + extension
#
#        newlayer = os.path.join(outputdirectory, newname + extension)
#        layer = os.path.join(self.path, layer)
#
#        copy_function = COPY_FUNCTION.get(layer_type, Copy_management)
#        copy_function(layer, newlayer)
#
#        return newlayer
#
#    def _layer_to_file_multiple(self, layers, layers_type, extension,
#                                outputdirectory, strict=True):
#        """
#        """
#        converted = []
#
#        for layer in layers:
#            try:
#                converted.append(self._layer_to_file(layer,
#                                                     layers_type,
#                                                     extension,
#                                                     outputdirectory))
#            except Exception as e:
#                if strict:
#                    raise e
#                else:
#                    exception(e)
#                    print "Failed to convert layer {}.".format(layer)
#
#        return converted
#
#    def feature_class_to_shapefile(self, featureclass, outputdirectory,
#                                   outname_to_use=None):
#        """
#        """
#        return self._layer_to_file(featureclass,
#                                   FC_TYPECODE,
#                                   SHAPEFILE_EXT,
#                                   outputdirectory,
#                                   outname=outname_to_use)
#
#    def feature_class_to_shapefile_multiple(self, outputdirectory,
#                                            outputname=None,
#                                            featureclasses=None):
#        """
#        """
#        if not featureclasses:
#            featureclasses = self.featureclasses
#
#        newfcs = self._layer_to_file_multiple(
#            featureclasses,
#            FC_TYPECODE,
#            SHAPEFILE_EXT,
#            outputdirectory,
#        )
#
#        return newfcs
#
#    def raster_layer_to_file(self, rasterlayer, outputdirectory,
#                             rasterformat=DEFAULT_RASTER_EXT,
#                             outname_to_use=None):
#        """
#        """
#        return self._layer_to_file(rasterlayer,
#                                   RASTER_TYPECODE,
#                                   rasterformat,
#                                   outputdirectory,
#                                   outname=outname_to_use)
#
#    def raster_layer_to_file_multiple(self, outputdirectory,
#                                      rasterlayers=None,
#                                      rasterformat=DEFAULT_TABLE_EXT):
#        """
#        """
#        if not rasterlayers:
#            rasterlayers = self.rasterlayers
#
#        newrasters = self._layer_to_file_multiple(
#            rasterlayers,
#            RASTER_TYPECODE,
#            rasterformat,
#            outputdirectory,
#        )
#
#        return newrasters
#
#    def table_to_file(self, table, outputdirectory,
#                      tableformat=DEFAULT_TABLE_EXT,
#                      outname=None):
#        """
#        """
#        return self._layer_to_file(table,
#                                   TABLE_TYPECODE,
#                                   tableformat,
#                                   outputdirectory,
#                                   outname=outname)
#
#    def table_to_file_multiple(self, outputdirectory,
#                               tables=None,
#                               tabularformat=DEFAULT_TABLE_EXT):
#        """
#        """
#        if not tables:
#            tables = self.tables
#
#        newtables = self._layer_to_file_multiple(
#            tables,
#            TABLE_TYPECODE,
#            tabularformat,
#            outputdirectory,
#        )
#
#        return newtables
#
#    def all_layers_to_files(self, outputdirectory,
#                            rasterformat=DEFAULT_RASTER_EXT,
#                            tabularformat=DEFAULT_TABLE_EXT):
#        """
#        """
#        copied = []
#        copied += self.feature_class_to_shapefile_multiple(outputdirectory)
#        copied += self.raster_layer_to_file_multiple(outputdirectory,
#                                                     rasterformat=rasterformat)
#        copied += self.table_to_file_multiple(outputdirectory,
#                                              tabularformat=tabularformat)
#
#        return copied


# *************** MAIN CHECK ***************

if __name__ == '__main__':
    pass

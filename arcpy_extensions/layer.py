import os
from arcpy import Describe
from constants import LAYER_TYPES, DATASET_TYPECODE


# *************** CONSTANTS ***************

# none


# **************** CLASSES ****************

class LayerError(Exception):
    pass


class Layer(object):
    """
    """
    def __init__(self, path, layer_type=None):
        """Initialize the class.

        Required:  path -
        """
        try:
            desc = Describe(path)
        except IOError as e:
            raise LayerError(e)

        workspace, name = os.path.split(desc.catalogPath)
        dataset = ""
        workspace_desc = Describe(workspace)

        if hasattr(workspace_desc, "datasetType") and \
                workspace_desc.datasetType == DATASET_TYPECODE:
            workspace, dataset = os.path.split(workspace)

        self.workspace = workspace
        self.dataset = dataset
        self.name = name

        if not layer_type:
            try:
                layer_type = desc.dataType
            except AttributeError:
                raise LayerError("Could not determine layer type.")

        self.type = layer_type

        print name, layer_type

    @property
    def workspace_type(self):
        raise NotImplementedError

    @property
    def path(self):
        if self.dataset:
            path = os.path.join(self.workspace, self.dataset, self.name)
        else:
            path = os.path.join(self.workspace, self.name)
        return path

    def _copy(self, outputworkspace, outname=None, extension=None):
        """
        """
        type_properties = LAYER_TYPES.get(self.type, LAYER_TYPES["DEFAULT"])

        if not outname:
            # use same name as layer
            outname = self.name

        if not extension:
            extension = type_properties["extension"]
        elif not extension.startswith("."):
            extension = "." + extension

        print type_properties, extension, outname

        newlayername = outname + extension
        newlayer = os.path.join(outputworkspace, newlayername)

        copy_function = type_properties["copy_function"]
        copy_function(self.path, newlayer)

        return Layer(newlayer, layer_type=self.type)

    def copy_to_file(self, outputdirectory, outname=None, extension=None):
        """
        """
        return self._copy(outputworkspace=outputdirectory,
                          outname=outname,
                          extension=extension)

    def copy_to_geodatabase(self, geodatabase, outname=None):
        """
        """
        from geodatabase import Geodatabase
        is_gdb_object = False

        if type(geodatabase) == type(Geodatabase):
            outputgdb = geodatabase.path
            is_gdb_object = True

        outlyr = self._copy(outputworkspace=outputgdb,
                            outname=outname,
                            extension="")

        if is_gdb_object:
            geodatabase.add_layer(outlyr)

        return outlyr


# *************** MAIN CHECK ***************

if __name__ == '__main__':
    pass

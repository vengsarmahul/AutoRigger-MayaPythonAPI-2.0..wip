from AutoRig import mainUI
import maya.api.OpenMaya as om
import maya.cmds as cmds



def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass

class AutoRigger(om.MPxCommand):

    COMMAND_NAME = "AutoRigger"

    def __init__(self):
        super(AutoRigger, self).__init__()

    def doIt(self, args):
        a = mainUI.MainWindow()
        a.show()

    @classmethod
    def creator(cls):
        return AutoRigger()


def initializePlugin(plugin):

    vendor = "Mahul Vengsar"
    version = "1.0.0"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)

    try:
        plugin_fn.registerCommand(AutoRigger.COMMAND_NAME, AutoRigger.creator)
    except:
        om.MGlobal.displayError("Failed to register command: {0}".format(AutoRigger.COMMAND_NAME))


def uninitializePlugin(plugin):

    plugin_fn = om.MFnPlugin(plugin)

    try:
        plugin_fn.deregisterCommand(AutoRigger.COMMAND_NAME)
    except:
        om.MGlobal.displayError("Failed to unregister command: {0}".format(AutoRigger.COMMAND_NAME))


if __name__ == "__main__":

    cmds.file(new=True, force=True)
    plugin_name = "autoRigger.py"

    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))

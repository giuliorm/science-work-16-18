from fbx import *
import FbxCommon

class FBX_Class(object):
    def __init__(self, filename):
        """
        FBX Scene Object
        """
        self.filename = filename
        self.scene = None
        self.sdk_manager = None
        self.sdk_manager, self.scene = FbxCommon.InitializeSdkObjects()
        FbxCommon.LoadScene(self.sdk_manager, self.scene, filename)

        self.root_node = self.scene.GetRootNode()
        self.scene_nodes = self.get_scene_nodes()


fbx_scene = FBX_Class(r'example.fbx')  # instantiate the class
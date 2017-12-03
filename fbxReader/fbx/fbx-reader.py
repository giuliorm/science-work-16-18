import fbx
import FbxCommon

class Color:
    def __init__(self, r, g, b, a):
        self._r = r
        self._g = g
        self._b = b
        self._a = a

def	FbxVector4ToPoint(v):
    return [v.mData[0] / v.mData[3],
		    v.mData[1] / v.mData[3],
			v.mData[2] / v.mData[3]]

def	FbxVector4ToVector(v):
    return [v.mData[0],
			v.mData[1],
			v.mData[2]]

def	FbxColorToColor(c):
    return Color(c.mRed, c.mGreen, c.mBlue, c.mAlpha)


def	FbxVector2ToVector(v):
    return [v.mData[0], v.mData[1]]


class FBX:

    def __init__(self):
        print("FBX SDK {0}".format(fbx.FbxManager.GetVersion()))
        self.fbxManager = fbx.FbxManager().Create()
        self.fbxImporter = fbx.FbxImporter.Create(self.fbxManager , "Importer")
        self.fbxScene = fbx.FbxScene.Create(self.fbxManager, "FBX Scene")
        self.fbxGConv = fbx.FbxGeometryConverter(self.fbxManager)
        self.fbxManager, self.scene = FbxCommon.InitializeSdkObjects()

    def load_scene(self, filename, options=None): #Fusion::Engine::Graphics::Scene ^ FbxLoader::LoadScene( string ^filename, Options ^options2 )

        #this->options	=	options2;
        scene = FbxCommon.InitializeSdkObjects()
        FbxCommon.LoadScene(self.fbxManager, self.fbxScene, filename)

        #FbxTimeSpan timeSpan;
        #FbxTime		start;
        #FbxTime		end;

        timeSpan = self.fbxScene.GetGlobalSettings().GetTimelineDefaultTimeSpan()
        timeMode = self.fbxScene.GetGlobalSettings().GetTimeMode()
        start = timeSpan.GetStart()
        end = timeSpan.GetStop()

        rootNode = self.fbxScene.GetRootNode()

        #if (options->ImportAnimation) {
        scene.StartTime = start.GetMilliSeconds()
        scene.EndTime = end.GetMilliSeconds() #fbx.TimeSpan::FromMilliseconds( (long)end.GetMilliSeconds() );

        scene.CreateAnimation(start.GetFrameCount(timeMode), end.GetFrameCount( timeMode ),
                                   self.fbxScene.GetNodeCount())

        print("Animation time span : {0} - {1}",	scene.StartTime, scene.EndTime )
        print("Animation frame     : {0} - {1}",	scene.FirstFrame, scene.LastFrame )
        print("Total nodes : {0}",	scene.GetNodeCount())

        print("Traversing hierarchy...")

        scene.IterateChildren( rootNode, self.fbxScene, scene, -1, 1 )


        print("Import Geometry...")

        #if options and options.ImportGeometry:
        #    for node in self.scene.Nodes:
        #        #fbxNode	=	(FbxNode*)(((IntPtr)node->Tag).ToPointer());
        #        HandleMesh( self.scene, node, fbxNode );



        #//	do not destroy...
        #// 	stack overflow happens...
        #self.fbxImporter.Destroy();

        return scene


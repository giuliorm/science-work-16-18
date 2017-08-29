import fbx
import FbxCommon
scene = FbxCommon.InitializeSdkObjects()

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
        #self.fbxManager = fbx.FbxManager()
        #self.fbxImporter = fbx.FbxImporter(self.fbxManager , "Importer")
        #self.fbxScene = fbx.FbxScene(self.fbxManager, "Scene")
        #self.fbxGConv = fbx.FbxGeometryConverter(self.fbxManager)
        self.fbxManager, self.scene = FbxCommon.InitializeSdkObjects()

    def load_scene(self, filename, options=None): #Fusion::Engine::Graphics::Scene ^ FbxLoader::LoadScene( string ^filename, Options ^options2 )

        #this->options	=	options2;

        FbxCommon.LoadScene(self.fbxManager, self.scene, filename)

        #FbxTimeSpan timeSpan;
        #FbxTime		start;
        #FbxTime		end;

        timeSpan = self.scene.GetGlobalSettings().GetTimelineDefaultTimeSpan()
        timeMode = self.scene.GetGlobalSettings().GetTimeMode()
        start = timeSpan.GetStart()
        end   = timeSpan.GetStop()

        rootNode = self.scene.GetRootNode()

        #if (options->ImportAnimation) {
        self.scene.StartTime = start.GetMilliSeconds()
        self.scene.EndTime = end.GetMilliSeconds() #fbx.TimeSpan::FromMilliseconds( (long)end.GetMilliSeconds() );

        self.scene.CreateAnimation(start.GetFrameCount(timeMode), (int)end.GetFrameCount( timeMode ), fbxScene->GetNodeCount() );

            Console::WriteLine("Animation time span : {0} - {1}",	scene->StartTime, scene->EndTime );
            Console::WriteLine("Animation frame     : {0} - {1}",	scene->FirstFrame, scene->LastFrame );
            Console::WriteLine("Total nodes         : {0}",			fbxScene->GetNodeCount() );
        #}

        Console::WriteLine("Traversing hierarchy...");

        IterateChildren( rootNode, fbxScene, scene, -1, 1 );


        Console::WriteLine("Import Geometry...");

        if (options->ImportGeometry) {
            for each ( Node ^node in scene->Nodes ) {
                //Console::WriteLine( "  {0}",node->Name);

                FbxNode *fbxNode	=	(FbxNode*)(((IntPtr)node->Tag).ToPointer());
                HandleMesh( scene, node, fbxNode );
            }
        }

        //	do not destroy...
        // 	stack overflow happens...
        fbxImporter->Destroy(true);

        return scene;
    }

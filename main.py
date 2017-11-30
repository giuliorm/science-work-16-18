import fbx
import FbxCommon

class FbxCriteria:
    def __init__(self):
        self.ANIM_STACK_CRITERIA = FbxCommon.FbxCriteria.ObjectType(FbxCommon.FbxAnimStack.ClassId)
        self.ANIM_LAYER_CRITERIA = FbxCommon.FbxCriteria.ObjectType(FbxCommon.FbxAnimLayer.ClassId)

def main():
    path  = r"C:\Users\zotovy\Documents\fbx\01\01_01.fbx"
    manager = fbx.FbxManager.Create()
    importer = fbx.FbxImporter.Create(manager, 'myImporter')
    status = importer.Initialize( path )
    if not status:
        print("FBX cannot be read")
        exit(-1)
    criteria = FbxCriteria()
    scene = fbx.FbxScene.Create(manager, 'myScene')
    importer.Import(scene)
    importer.Destroy()
    animStacksCount = scene.GetSrcObjectCount(criteria.ANIM_STACK_CRITERIA)
    for i in xrange(animStacksCount):
        stack = scene.GetSrcObject(criteria.ANIM_STACK_CRITERIA, i)
        layers = stack.GetMemberCount(criteria.ANIM_LAYER_CRITERIA)
        for l in xrange(layers):
            layer = stack.GetMember(criteria.ANIM_LAYER_CRITERIA, l)
            print(layer.GetName())
        print(stack.GetName())

main()
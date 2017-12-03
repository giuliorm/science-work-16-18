import FbxCommon
import fbx
from fbxReader.fbx.display_animation import Animation


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
    a = Animation()
    a.DisplayAnimation(scene)
    if a.time_units is None or len(a.time_units) < 1:
        print("There hasnt been found any time units")
        exit()
    time = set()
    names = set()
    for k in a.time_units.keys():
        timeUnit = a.time_units[k]
        for key in timeUnit.keys():
            time.add(key)
            for name in timeUnit[key].keys():
                names.add((k, name))

    time = sorted(time)
    data = []
    for t in time:
        c_row = []
        c_row.append(float(t))
        for bodyPartName, propName in names:
            value = 0.0
            if bodyPartName in a.time_units.keys():
                if t in a.time_units[bodyPartName].keys():
                    if propName in a.time_units[bodyPartName][t].keys():
                        value = a.time_units[bodyPartName][t][propName]
            c_row.append(value)
        data.append(c_row)
    i = 1
    from neural.simple_net import SimpleNet
    import numpy as np
    s = SimpleNet()
    data = np.asarray(data)
    s.train(data, 1000)
    data_predicted = s.predict(data)
    print(data_predicted)
    errors = 0
    count = 0
    for i in range(len(data_predicted)):
        for j in range(len(data_predicted[i])):
            err = abs(data_predicted[i][j] - data[i][j])
            if err > 10e-6:
                errors = errors + 1
            count = count + 1
    print("Errors {0}%".format((float(errors)/count)*100))

    # for k in a.time_units.keys()
    # with open('fbx {0}.csv'.format(scene.GetName()), newline='') as myFile:
    #     writer = csv.DictWriter(myFile, fieldnames=names)
    #     writer.writeheader()
    #     writer.writerow()
    # animStacksCount = scene.GetSrcObjectCount(criteria.ANIM_STACK_CRITERIA)
    # for i in xrange(animStacksCount):
    #     stack = scene.GetSrcObject(criteria.ANIM_STACK_CRITERIA, i)
    #     layers = stack.GetMemberCount(criteria.ANIM_LAYER_CRITERIA)
    #     for l in xrange(layers):
    #         layer = stack.GetMember(criteria.ANIM_LAYER_CRITERIA, l)
    #         print(layer.GetName())
    #     print(stack.GetName())

main()
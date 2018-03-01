import FbxCommon
import fbx
from traverse_animation import Animation, FbxCriteria
import numpy as np
import sys

class FbxMapper:

    def __init__(self, path):
        # path to fbx file
        self.__path = path

    def __CollectTimeAndColumnNames(self, timeUnits):
        time = set()
        names = set()
        names.add(('Time', 'Time'))
        # collecting names and time
        for timeUnitKey in timeUnits.keys():
            timeUnit = timeUnits[timeUnitKey]
            for timeUnitSubKey in timeUnit.keys():
                time.add(timeUnitSubKey)
                for name in timeUnit[timeUnitSubKey].keys():
                    names.add((timeUnitKey, name))
        return time, names

    def __TimeUnitsToData(self, timeUnits):
        data = []
        time, names = self.__CollectTimeAndColumnNames(timeUnits)

        time = sorted(time)
        names = sorted(names)

        for timeKey in time:
            c_row = [float(timeKey)]
            for bodyPartName, transformPropName in names:
                value = None
                if bodyPartName in timeUnits.keys():
                    if timeKey in timeUnits[bodyPartName].keys():
                        if transformPropName in timeUnits[bodyPartName][timeKey].keys():
                            value = timeUnits[bodyPartName][timeKey][transformPropName]
                c_row.append(value)
            data.append(c_row)
        return names, np.asarray(data)

    def DataToCsv(self, csvPath):
        pass

    def FbxToData(self):
        """

        :return: a numpy table???
        """
        manager = fbx.FbxManager.Create()
        importer = fbx.FbxImporter.Create(manager, 'myImporter')
        status = importer.Initialize(self.__path)
        if not status:
            print("FBX cannot be read")
            return np.asarray([])
        criteria = FbxCriteria()
        scene = fbx.FbxScene.Create(manager, 'myScene')

        importer.Import(scene)
        importer.Destroy()
        #a = Animation()
        self.__animationTraverser = Animation()
        self.__animationTraverser.TraverseAnimation(scene)
        timeUnits = self.__animationTraverser.GetTimeUnits()

        if timeUnits is None or len(timeUnits) < 1:
            print("There hasnt been found any time units")
            return np.asarray([])

        columnNames, data = self.__TimeUnitsToData(timeUnits)
        return columnNames, np.asarray(data)

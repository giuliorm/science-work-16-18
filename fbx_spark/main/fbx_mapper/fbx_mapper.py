import FbxCommon
import fbx
from traverse_animation import Animation, FbxCriteria
import numpy as np
import sys

class FbxMapper:

    def __init__(self, path):
        # path to fbx file
        self.__path = path
        self.__data = np.asarray([])
        self.__columnNames = []

    def __CollectTimeAndColumnNames(self, timeUnits):
        time = set()
        names = set()

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
            c_row = []
            c_row.append(timeKey)
            for bodyPartName, transformPropName in names:
                value = None
                if bodyPartName in timeUnits.keys():
                    if timeKey in timeUnits[bodyPartName].keys():
                        if transformPropName in timeUnits[bodyPartName][timeKey].keys():
                            value = timeUnits[bodyPartName][timeKey][transformPropName]
                c_row.append(value)
            data.append(c_row)
        names_with_time = [('time', 'time')]
        names_with_time.extend(names)
        return names_with_time, np.asarray(data)

    def DataToCsv(self, csvPath):
        file = open(csvPath, "w")
        names_to_write = []
        eps = 5
        for i in range(self.__data.shape[1]):
            if (self.__data[:,i] == None).sum() - eps < 0:
                names_to_write.append(True)
            else:
                names_to_write.append(False)
        for i in range(len(self.__columnNames)):
            if names_to_write[i] is True:
                file.write("{0} {1},".format(self.__columnNames[i][0], self.__columnNames[i][1]))
        for i in range(self.__data.shape[0]):
            file.write("\n")
            for j in range(self.__data.shape[1]):
                if names_to_write[j] is True:
                    file.write("{},".format(self.__data[i][j]))
        file.close()

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
        self.__columnNames = columnNames
        self.__data = np.asarray(data)
        return columnNames, np.asarray(data)

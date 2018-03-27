import FbxCommon
from traverse_animation import FbxCriteria
from traverse_animation import FBXSDK_CURVENODE_COMPONENT_X
from  traverse_animation import FBXSDK_CURVENODE_COMPONENT_Y
from traverse_animation import FBXSDK_CURVENODE_COMPONENT_Z
from traverse_animation import NODE_ATTRIBUTE

class Animation:

    def __init__(self):
        self.__criteria = FbxCriteria()
        self.__time_units = {}
        self.__current_time_unit = None

    def GetTimeUnits(self):
        return self.__time_units

    def TraverseAnimation(self, pscene):
        """

        :param pscene:
        :type pscene: FbxCommon.FbxScene
        :return:
        """
        count = pscene.GetSrcObjectCount(self.__criteria.ANIM_STACK_CRITERIA)
        for i in xrange(count):
            lAnimStack = pscene.GetSrcObject(self.__criteria.ANIM_STACK_CRITERIA, i)
            self.TraverseAnimationStack(lAnimStack, pscene.GetRootNode())

    def TraverseAnimationStack(self, pAnimStack, pNode):
        """

        :param pAnimStack:
        :type pAnimStack: FbxCommon.FbxAnimStack
        :param pNode:
        :type pNode: FbxCommon.FbxNode
        :return:
        """
        nbAnimLayers = pAnimStack.GetMemberCount(self.__criteria.ANIM_LAYER_CRITERIA)
        for l in xrange(nbAnimLayers):
            lAnimLayer = pAnimStack.GetMember(self.__criteria.ANIM_LAYER_CRITERIA, l)
            self.TraverseAnimationLayer(lAnimLayer, pNode)

    def TraverseAnimationLayer(self, pAnimLayer, pNode):
            if self.__current_time_unit is not None and len(self.__current_time_unit.keys()) > 0:
                self.__time_units[pNode.GetName()] = self.__current_time_unit
            self.__current_time_unit = {}
            self.TraverseChannels(pNode, pAnimLayer) #??
            # print("")
            childCount = pNode.GetChildCount()
            for lModelCount in xrange(childCount):
                self.TraverseAnimationLayer(pAnimLayer, pNode.GetChild(lModelCount))

    def AddValues(self, values, message):
        if self.__current_time_unit is not None:
            for time, value in values:
                if time not in self.__current_time_unit.keys():
                    self.__current_time_unit[time] = {}
                self.__current_time_unit[time][message] = value

    def TraverseIfNotNone(self, lAnimCurve, message):
        if lAnimCurve:
            #print(message)
            values = self.TraverseCurve(lAnimCurve)
            self.AddValues(values, message)

    def TraverseTranslation(self, pNode, pAnimLayer):

        lAnimCurve = pNode.LclTranslation.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_X)
        self.TraverseIfNotNone(lAnimCurve, "        TX")
        lAnimCurve = pNode.LclTranslation.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Y)
        self.TraverseIfNotNone(lAnimCurve, "        TY")
        lAnimCurve = pNode.LclTranslation.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Z)
        self.TraverseIfNotNone(lAnimCurve, "        TZ")

    def TraverseRotation(self, pNode, pAnimLayer):

        lAnimCurve = pNode.LclRotation.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_X)
        self.TraverseIfNotNone(lAnimCurve, "        RX")
        lAnimCurve = pNode.LclRotation.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Y)
        self.TraverseIfNotNone(lAnimCurve, "        RY")
        lAnimCurve = pNode.LclRotation.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Z)
        self.TraverseIfNotNone(lAnimCurve, "        RZ")

    def TraverseScaling(self, pNode, pAnimLayer):

        lAnimCurve = pNode.LclScaling.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_X)
        self.TraverseIfNotNone(lAnimCurve, "        SX")
        lAnimCurve = pNode.LclScaling.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Y)
        self.TraverseIfNotNone(lAnimCurve, "        SY")
        lAnimCurve = pNode.LclScaling.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Z)
        self.TraverseIfNotNone(lAnimCurve, "        SZ")

    def TraverseColor(self, lNodeAttribute, pAnimLayer):

        lAnimCurve = lNodeAttribute.Color.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_X)
        self.TraverseIfNotNone(lAnimCurve, "        Red")
        lAnimCurve = lNodeAttribute.Color.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Y)
        self.TraverseIfNotNone(lAnimCurve, "        Green")
        lAnimCurve = lNodeAttribute.Color.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Z)
        self.TraverseIfNotNone(lAnimCurve, "        Blue")

    def TraverseLight(self, light, pAnimLayer):

        lAnimCurve = light.Intensity.GetCurve(pAnimLayer)
        self.TraverseIfNotNone(lAnimCurve, "        Intensity")
        lAnimCurve = light.OuterAngle.GetCurve(pAnimLayer)
        self.TraverseIfNotNone(lAnimCurve, "        Outer Angle")
        lAnimCurve = light.Fog.GetCurve(pAnimLayer)
        self.TraverseIfNotNone(lAnimCurve, "        Fog")

    def TraverseCamera(self, camera, pAnimLayer):

        lAnimCurve = camera.FieldOfView.GetCurve(pAnimLayer)
        self.TraverseIfNotNone(lAnimCurve, "        Field of View")
        lAnimCurve = camera.FieldOfViewX.GetCurve(pAnimLayer)
        self.TraverseIfNotNone(lAnimCurve, "        Field of View X")
        lAnimCurve = camera.FieldOfViewY.GetCurve(pAnimLayer)
        self.TraverseIfNotNone(lAnimCurve, "        Field of View Y")
        lAnimCurve = camera.OpticalCenterX.GetCurve(pAnimLayer)
        self.TraverseIfNotNone(lAnimCurve, "        Optical Center X")
        lAnimCurve = camera.OpticalCenterY.GetCurve(pAnimLayer)
        self.TraverseIfNotNone(lAnimCurve, "        Optical Center Y")
        lAnimCurve = camera.Roll.GetCurve(pAnimLayer)
        self.TraverseIfNotNone(lAnimCurve, "        Roll")

    def TraverseNodeAttribute(self, pAnimLayer, lNodeAttribute):

        if not lNodeAttribute:
            return
        type = lNodeAttribute.GetAttributeType()
        if type in [FbxCommon.FbxNodeAttribute.eMesh,
                    FbxCommon.FbxNodeAttribute.eNurbs, type == FbxCommon.FbxNodeAttribute.ePatch]:
            lGeometry = lNodeAttribute
            lBlendShapeDeformerCount = lGeometry.GetDeformerCount(FbxCommon.FbxDeformer.eBlendShape)
            for lBlendShapeIndex in xrange(lBlendShapeDeformerCount):
                lBlendShape = lGeometry.GetDeformer(lBlendShapeIndex, FbxCommon.FbxDeformer.eBlendShape)
                lBlendShapeChannelCount = lBlendShape.GetBlendShapeChannelCount()
                for lChannelIndex in xrange(lBlendShapeChannelCount):
                    lChannel = lBlendShape.GetBlendShapeChannel(lChannelIndex)
                    lChannelName = lChannel.GetName()
                    lAnimCurve = lGeometry.GetShapeChannel(lBlendShapeIndex, lChannelIndex, pAnimLayer, True)
                    self.TraverseIfNotNone(lAnimCurve, ("        Shape %s", lChannelName))

    def TraverseNumberProperty(self, lDataType, lProperty, lCurveNode):

        if lDataType.GetType() == FbxCommon.eFbxBool or \
                        lDataType.GetType() == FbxCommon.eFbxDouble or \
                        lDataType.GetType() == FbxCommon.eFbxFloat or \
                        lDataType.GetType() == FbxCommon.eFbxInt:
            for c in xrange(lCurveNode.GetCurveCount(0)):
                lAnimCurve = lCurveNode.GetCurve(0, c)
                self.TraverseIfNotNone(lAnimCurve, lProperty.GetName())

    def TraverseEnumProperty(self, lDataType, lProperty, lCurveNode):

        if lDataType.GetType() == FbxCommon.eFbxEnum:
            for c in xrange(lCurveNode.GetCurveCount(0)):
                lAnimCurve = lCurveNode.GetCurve(0, c)
                if lAnimCurve:
                    values = self.TraverseListCurve(lAnimCurve, lProperty)
                    self.AddValues(values, lProperty.GetName())

    def TraverseDoubleOrColorProperty(self, lDataType, lProperty, lCurveNode):

        if lDataType.GetType() == FbxCommon.eFbxDouble3 or lDataType.GetType() == FbxCommon.eFbxDouble4 or \
                lDataType.Is(FbxCommon.FbxColor3DT) or lDataType.Is(FbxCommon.FbxColor4DT):
            lComponentName1 = FBXSDK_CURVENODE_COMPONENT_X
            lComponentName2 = FBXSDK_CURVENODE_COMPONENT_Y
            lComponentName3 = FBXSDK_CURVENODE_COMPONENT_Z
            for c in xrange(lCurveNode.GetCurveCount(0)):
                lAnimCurve = lCurveNode.GetCurve(0, c)
                self.TraverseIfNotNone(lAnimCurve, "{0}      Component {1}".format(lProperty.GetName(), lComponentName1))
            for c in xrange(lCurveNode.GetCurveCount(1)):
                lAnimCurve = lCurveNode.GetCurve(1, c)
                self.TraverseIfNotNone(lAnimCurve, "{0}      Component {1}".format(lProperty.GetName(), lComponentName2))
            for c in xrange(lCurveNode.GetCurveCount(2)):
                lAnimCurve = lCurveNode.GetCurve(2, c)
                self.TraverseIfNotNone(lAnimCurve, "{0}      Component {1}".format(lProperty.GetName(), lComponentName3))

    def TraverseProperty(self, pNode, pAnimLayer, lProperty):

        while lProperty.IsValid():
            lCurveNode = lProperty.GetCurveNode(pAnimLayer)
            if not lCurveNode:
                lProperty = pNode.GetNextProperty(lProperty)
                continue

            lDataType = lProperty.GetPropertyDataType()
            self.TraverseNumberProperty(lDataType, lProperty, lCurveNode)
            self.TraverseDoubleOrColorProperty(lDataType, lProperty, lCurveNode)
            self.TraverseEnumProperty(lDataType, lProperty, lCurveNode)
            lProperty = pNode.GetNextProperty(lProperty)

    def TraverseChannels(self, pNode, pAnimLayer):

        if pNode and pAnimLayer:
            self.TraverseTranslation(pNode, pAnimLayer)
            self.TraverseRotation(pNode, pAnimLayer)
            self.TraverseScaling(pNode, pAnimLayer)

        lNodeAttribute = pNode.GetNodeAttribute()
        if lNodeAttribute:
            self.TraverseColor(lNodeAttribute, pAnimLayer)
        light = pNode.GetLight()
        if light:
            self.TraverseLight(light, pAnimLayer)
        camera = pNode.GetCamera()
        if camera:
            self.TraverseCamera(camera, pAnimLayer)

        self.TraverseNodeAttribute(pAnimLayer, lNodeAttribute)

        lProperty = pNode.GetFirstProperty()
        self.TraverseProperty(pNode, pAnimLayer, lProperty)

    def TraverseCurve(self, pCurve):
        """

        :param pCurve:
        :return: time, value
        """
        lKeyCount = pCurve.KeyGetCount()
        timeValue = []
        for lCount in xrange(lKeyCount):
            lKeyValue = pCurve.KeyGetValue(lCount)
            lKeyTime = pCurve.KeyGetTime(lCount).GetMilliSeconds()
            timeValue.append((lKeyTime, lKeyValue))
        return timeValue


    def TraverseListCurve(self, pCurve, pProperty):
        lKeyCount = pCurve.KeyGetCount()
        timeValues = []
        for lCount in xrange(lKeyCount):
            lKeyValue = pCurve.KeyGetValue(lCount)
            lKeyTime = pCurve.KeyGetTime(lCount).GetMilliSeconds()
            timeValues.append((lKeyTime, lKeyValue))
        return timeValues

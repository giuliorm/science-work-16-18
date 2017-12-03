import fbx, FbxCommon

class FbxCriteria:
    def __init__(self):
        self.ANIM_STACK_CRITERIA = FbxCommon.FbxCriteria.ObjectType(FbxCommon.FbxAnimStack.ClassId)
        self.ANIM_LAYER_CRITERIA = FbxCommon.FbxCriteria.ObjectType(FbxCommon.FbxAnimLayer.ClassId)



FBXSDK_CURVENODE_COMPONENT_X = "X"
FBXSDK_CURVENODE_COMPONENT_Y = "Y"
FBXSDK_CURVENODE_COMPONENT_Z = "Z"
NODE_ATTRIBUTE = ["eUnknown", "eNull", "eMarker", "eSkeleton", "eMesh", "eNurbs", "ePatch", "eCamera", "eCameraStereo",
                  "eCameraSwitcher", "eLight", "eOpticalReference", "eOpticalMarker"]

class Animation:

    def __init__(self):
        self.criteria = FbxCriteria()
        self.time_units = {}
        self.current_time_unit = None

    def DisplayAnimation(self, pscene):
        """

        :param pscene:
        :type pscene: FbxCommon.FbxScene
        :return:
        """
        count = pscene.GetSrcObjectCount(self.criteria.ANIM_STACK_CRITERIA)
        for i in xrange(count):
            lAnimStack = pscene.GetSrcObject(self.criteria.ANIM_STACK_CRITERIA, i)
            lOutputString = "Animation Stack Name: "
            lOutputString = lOutputString + lAnimStack.GetName()
            lOutputString = lOutputString + ""
            print(lOutputString)
            self.DisplayAnimationStack(lAnimStack, pscene.GetRootNode())
            #self.DisplayAnimationStack(lAnimStack, pscene.GetRootNode())

    def DisplayAnimationStack(self, pAnimStack, pNode):
        """

        :param pAnimStack:
        :type pAnimStack: FbxCommon.FbxAnimStack
        :param pNode:
        :type pNode: FbxCommon.FbxNode
        :return:
        """
        nbAnimLayers = pAnimStack.GetMemberCount(self.criteria.ANIM_LAYER_CRITERIA)
        lOutputString = "Animation stack contains "
        lOutputString = lOutputString + str(nbAnimLayers)
        lOutputString = lOutputString + " Animation Layer(s)"
        print(lOutputString)
        for l in xrange(nbAnimLayers):
            lAnimLayer = pAnimStack.GetMember(self.criteria.ANIM_LAYER_CRITERIA, l)
            lOutputString = "AnimLayer "
            lOutputString = lOutputString + str(l)
            lOutputString = lOutputString + ""
            print(lOutputString)
            self.DisplayAnimationLayer(lAnimLayer, pNode)

    def DisplayAnimationLayer(self, pAnimLayer, pNode):
            lModelCount = 0
            lOutputString = "     Node Name: "
            lOutputString = lOutputString + pNode.GetName()
            lOutputString = lOutputString + ""
            print(lOutputString)
            if self.current_time_unit is not None and len(self.current_time_unit.keys()) > 0:
                self.time_units[pNode.GetName()] = self.current_time_unit
            self.current_time_unit = {}
            self.DisplayChannels(pNode, pAnimLayer) #??
            print("")
            childCount = pNode.GetChildCount()
            for lModelCount in xrange(childCount):
                self.DisplayAnimationLayer(pAnimLayer, pNode.GetChild(lModelCount))

    def AddValues(self, values, message):
        if self.current_time_unit is not None:
            for time, value in values:
                if time not in self.current_time_unit.keys():
                    self.current_time_unit[time] = {}
                self.current_time_unit[time][message] = value

    def DisplayIfNotNone(self, lAnimCurve, message):
        if lAnimCurve:
            print(message)
            values = self.DisplayCurve(lAnimCurve)
            self.AddValues(values, message)

    def DisplayTranslation(self, pNode, pAnimLayer):
        lAnimCurve = pNode.LclTranslation.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_X)
        self.DisplayIfNotNone(lAnimCurve, "        TX")
        lAnimCurve = pNode.LclTranslation.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Y)
        self.DisplayIfNotNone(lAnimCurve, "        TY")
        lAnimCurve = pNode.LclTranslation.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Z)
        self.DisplayIfNotNone(lAnimCurve, "        TZ")

    def DisplayRotation(self, pNode, pAnimLayer):
        lAnimCurve = pNode.LclRotation.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_X)
        self.DisplayIfNotNone(lAnimCurve, "        RX")
        lAnimCurve = pNode.LclRotation.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Y)
        self.DisplayIfNotNone(lAnimCurve, "        RY")
        lAnimCurve = pNode.LclRotation.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Z)
        self.DisplayIfNotNone(lAnimCurve, "        RZ")

    def DisplayScaling(self, pNode, pAnimLayer):
        lAnimCurve = pNode.LclScaling.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_X)
        self.DisplayIfNotNone(lAnimCurve, "        SX")
        lAnimCurve = pNode.LclScaling.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Y)
        self.DisplayIfNotNone(lAnimCurve, "        SY")
        lAnimCurve = pNode.LclScaling.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Z)
        self.DisplayIfNotNone(lAnimCurve, "        SZ")

    def DisplayColor(self, lNodeAttribute, pAnimLayer):
        lAnimCurve = lNodeAttribute.Color.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_X)
        self.DisplayIfNotNone(lAnimCurve, "        Red")
        lAnimCurve = lNodeAttribute.Color.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Y)
        self.DisplayIfNotNone(lAnimCurve, "        Green")
        lAnimCurve = lNodeAttribute.Color.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Z)
        self.DisplayIfNotNone(lAnimCurve, "        Blue")

    def DisplayLight(self, light, pAnimLayer):
        lAnimCurve = light.Intensity.GetCurve(pAnimLayer)
        self.DisplayIfNotNone(lAnimCurve, "        Intensity")
        lAnimCurve = light.OuterAngle.GetCurve(pAnimLayer)
        self.DisplayIfNotNone(lAnimCurve, "        Outer Angle")
        lAnimCurve = light.Fog.GetCurve(pAnimLayer)
        self.DisplayIfNotNone(lAnimCurve, "        Fog")

    def DisplayCamera(self, camera, pAnimLayer):
        lAnimCurve = camera.FieldOfView.GetCurve(pAnimLayer)
        self.DisplayIfNotNone(lAnimCurve, "        Field of View")
        lAnimCurve = camera.FieldOfViewX.GetCurve(pAnimLayer)
        self.DisplayIfNotNone(lAnimCurve, "        Field of View X")
        lAnimCurve = camera.FieldOfViewY.GetCurve(pAnimLayer)
        self.DisplayIfNotNone(lAnimCurve, "        Field of View Y")
        lAnimCurve = camera.OpticalCenterX.GetCurve(pAnimLayer)
        self.DisplayIfNotNone(lAnimCurve, "        Optical Center X")
        lAnimCurve = camera.OpticalCenterY.GetCurve(pAnimLayer)
        self.DisplayIfNotNone(lAnimCurve, "        Optical Center Y")
        lAnimCurve = camera.Roll.GetCurve(pAnimLayer)
        self.DisplayIfNotNone(lAnimCurve, "        Roll")

    def DisplayNodeAttribute(self, pAnimLayer, lNodeAttribute):
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
                    self.DisplayIfNotNone(lAnimCurve, ("        Shape %s", lChannelName))

    def DisplayNumberProperty(self, lDataType, lProperty, lCurveNode):
        if lDataType.GetType() == FbxCommon.eFbxBool or \
                        lDataType.GetType() == FbxCommon.eFbxDouble or \
                        lDataType.GetType() == FbxCommon.eFbxFloat or \
                        lDataType.GetType() == FbxCommon.eFbxInt:
            lMessage = "\n        Property \n"
            lMessage = lMessage + lProperty.GetName()
            if lProperty.GetLabel().GetLen() > 0:
                lMessage = lMessage + " (Label: "
                lMessage = lMessage + lProperty.GetLabel()
                lMessage = lMessage + ")"
            print(lMessage)
            for c in xrange(lCurveNode.GetCurveCount(0)):
                lAnimCurve = lCurveNode.GetCurve(0, c)
                self.DisplayIfNotNone(lAnimCurve, lProperty.GetName())

    def DisplayEnumProperty(self, lDataType, lProperty, lCurveNode):
        if lDataType.GetType() == FbxCommon.eFbxEnum:
            lMessage = "        Property "
            lMessage = lMessage + lProperty.GetName()
            if lProperty.GetLabel().GetLen() > 0:
                lMessage = lMessage + " (Label: "
                lMessage = lMessage + lProperty.GetLabel()
                lMessage = lMessage + ")"
            print(lMessage)
            for c in xrange(lCurveNode.GetCurveCount(0)):
                lAnimCurve = lCurveNode.GetCurve(0, c)
                if lAnimCurve:
                    values = self.DisplayListCurve(lAnimCurve, lProperty)
                    self.AddValues(values, lProperty.GetName())

    def DisplayDoubleOrColorProperty(self, lDataType, lProperty, lCurveNode):
        if lDataType.GetType() == FbxCommon.eFbxDouble3 or lDataType.GetType() == FbxCommon.eFbxDouble4 or \
                lDataType.Is(FbxCommon.FbxColor3DT) or lDataType.Is(FbxCommon.FbxColor4DT):
            lComponentName1 = FBXSDK_CURVENODE_COMPONENT_X
            lComponentName2 = FBXSDK_CURVENODE_COMPONENT_Y
            lComponentName3 = FBXSDK_CURVENODE_COMPONENT_Z
            # char * lComponentName2 = (lDataType.Is(FbxColor3DT) | | lDataType.Is(FbxColor4DT)) ? (char *)
            # FBXSDK_CURVENODE_COLOR_GREEN: (char *)
            # "Y";
            # char * lComponentName3 = (lDataType.Is(FbxColor3DT) | | lDataType.Is(FbxColor4DT)) ? (char *)
            # FBXSDK_CURVENODE_COLOR_BLUE: (char *)
            # "Z";
            lMessage = "        Property "
            lMessage = lMessage + lProperty.GetName()
            if lProperty.GetLabel().GetLen() > 0:
                lMessage = lMessage + " (Label: "
                lMessage = lMessage + lProperty.GetLabel()
                lMessage += ")"
            print(lMessage)
            for c in xrange(lCurveNode.GetCurveCount(0)):
                lAnimCurve = lCurveNode.GetCurve(0, c)
                self.DisplayIfNotNone(lAnimCurve, "{0}      Component {1}".format(lProperty.GetName(), lComponentName1))
            for c in xrange(lCurveNode.GetCurveCount(1)):
                lAnimCurve = lCurveNode.GetCurve(1, c)
                self.DisplayIfNotNone(lAnimCurve, "{0}      Component {1}".format(lProperty.GetName(), lComponentName2))
            for c in xrange(lCurveNode.GetCurveCount(2)):
                lAnimCurve = lCurveNode.GetCurve(2, c)
                self.DisplayIfNotNone(lAnimCurve, "{0}      Component {1}".format(lProperty.GetName(), lComponentName3))

    def DisplayProperty(self, pNode, pAnimLayer, lProperty):
        while lProperty.IsValid():
            #if lProperty.GetFlag(FbxCommon.FbxPropertyFlags.eUserDefined):
            lFbxFCurveNodeName = lProperty.GetName()
            lCurveNode = lProperty.GetCurveNode(pAnimLayer)
            if not lCurveNode:
                lProperty = pNode.GetNextProperty(lProperty)
                continue

            lDataType = lProperty.GetPropertyDataType()
            self.DisplayNumberProperty(lDataType, lProperty, lCurveNode)
            self.DisplayDoubleOrColorProperty(lDataType, lProperty, lCurveNode)
            self.DisplayEnumProperty(lDataType, lProperty, lCurveNode)
            lProperty = pNode.GetNextProperty(lProperty)

    def DisplayChannels(self, pNode, pAnimLayer):
        if pNode and pAnimLayer:
            self.DisplayTranslation(pNode, pAnimLayer)
            self.DisplayRotation(pNode, pAnimLayer)
            self.DisplayScaling(pNode, pAnimLayer)

        lNodeAttribute = pNode.GetNodeAttribute()
        if lNodeAttribute:
            self.DisplayColor(lNodeAttribute, pAnimLayer)
        light = pNode.GetLight()
        if light:
            self.DisplayLight(light, pAnimLayer)
        camera = pNode.GetCamera()
        if camera:
            self.DisplayCamera(camera, pAnimLayer)

        self.DisplayNodeAttribute(pAnimLayer, lNodeAttribute)

        lProperty = pNode.GetFirstProperty()
        self.DisplayProperty(pNode, pAnimLayer, lProperty)

    def InterpolationFlagToIndex(self, flags):
        if flags and FbxCommon.FbxAnimCurveDef.eInterpolationConstant == \
                FbxCommon.FbxAnimCurveDef.eInterpolationConstant:
            return 1
        if flags and FbxCommon.FbxAnimCurveDef.eInterpolationLinear == FbxCommon.FbxAnimCurveDef.eInterpolationLinear:
            return 2
        if flags and FbxCommon.FbxAnimCurveDef.eInterpolationCubic == FbxCommon.FbxAnimCurveDef.eInterpolationCubic:
            return 3
        return 0

    def ConstantmodeFlagToIndex(self, flags):
        if flags and FbxCommon.FbxAnimCurveDef.eConstantStandard == FbxCommon.FbxAnimCurveDef.eConstantStandard:
            return 1
        if flags and FbxCommon.FbxAnimCurveDef.eConstantNext == FbxCommon.FbxAnimCurveDef.eConstantNext:
            return 2
        return 0

    def TangentmodeFlagToIndex(self, flags):
        if flags and FbxCommon.FbxAnimCurveDef.eTangentAuto == FbxCommon.FbxAnimCurveDef.eTangentAuto: return 1
        if flags and FbxCommon.FbxAnimCurveDef.eTangentAutoBreak == FbxCommon.FbxAnimCurveDef.eTangentAutoBreak: return 2
        if flags and FbxCommon.FbxAnimCurveDef.eTangentTCB == FbxCommon.FbxAnimCurveDef.eTangentTCB: return 3
        if flags and FbxCommon.FbxAnimCurveDef.eTangentUser == FbxCommon.FbxAnimCurveDef.eTangentUser: return 4
        if flags and FbxCommon.FbxAnimCurveDef.eTangentGenericBreak == FbxCommon.FbxAnimCurveDef.eTangentGenericBreak:
            return 5
        if flags and FbxCommon.FbxAnimCurveDef.eTangentBreak == FbxCommon.FbxAnimCurveDef.eTangentBreak: return 6
        return 0

    def TangentweightFlagToIndex(self, flags):
        if flags and FbxCommon.FbxAnimCurveDef.eWeightedNone == FbxCommon.FbxAnimCurveDef.eWeightedNone: return 1
        if flags and FbxCommon.FbxAnimCurveDef.eWeightedRight == FbxCommon.FbxAnimCurveDef.eWeightedRight: return 2
        if flags and FbxCommon.FbxAnimCurveDef.eWeightedNextLeft == FbxCommon.FbxAnimCurveDef.eWeightedNextLeft: return 3
        return 0

    def TangentVelocityFlagToIndex(self, flags):
        if flags and FbxCommon.FbxAnimCurveDef.eVelocityNone == FbxCommon.FbxAnimCurveDef.eVelocityNone: return 1
        if flags and FbxCommon.FbxAnimCurveDef.eVelocityRight == FbxCommon.FbxAnimCurveDef.eVelocityRight: return 2
        if flags and FbxCommon.FbxAnimCurveDef.eVelocityNextLeft == FbxCommon.FbxAnimCurveDef.eVelocityNextLeft: return 3
        return 0


    def DisplayCurve(self, pCurve):
        """

        :param pCurve:
        :return: time, value
        """
        interpolation = ["?", "constant", "linear", "cubic"]
        constantMode = ["?", "Standard", "Next"]
        cubicMode = ["?", "Auto", "Auto break", "Tcb", "User", "Break", "User break"]
        tangentWVMode = ["?", "None", "Right", "Next left"]
        lKeyCount = pCurve.KeyGetCount()
        timeValue = []
        for lCount in xrange(lKeyCount):
            lKeyValue = pCurve.KeyGetValue(lCount)
            lKeyTime = pCurve.KeyGetTime(lCount).GetMilliSeconds()
            timeValue.append((lKeyTime, lKeyValue))
            lOutputString = "            Time: "
            lOutputString = lOutputString + str(lKeyTime)
            lOutputString = lOutputString + "            Value: "
            lOutputString = lOutputString + str(lKeyValue)
            lOutputString = lOutputString + " [ "
            index = self.InterpolationFlagToIndex(pCurve.KeyGetInterpolation(lCount))
            lOutputString = lOutputString + interpolation[index]
            if pCurve.KeyGetInterpolation(lCount) and \
                FbxCommon.FbxAnimCurveDef.eInterpolationConstant == FbxCommon.FbxAnimCurveDef.eInterpolationConstant:
                lOutputString = lOutputString + " | "
                index = self.ConstantmodeFlagToIndex(pCurve.KeyGetConstantMode(lCount))
                lOutputString = lOutputString + constantMode[index]
            elif pCurve.KeyGetInterpolation(lCount) and \
                    FbxCommon.FbxAnimCurveDef.eInterpolationCubic == FbxCommon.FbxAnimCurveDef.eInterpolationCubic:
                lOutputString = lOutputString + " | "
                index = self.TangentmodeFlagToIndex(pCurve.KeyGetTangentMode(lCount))
                lOutputString = lOutputString + cubicMode[index]
                lOutputString = lOutputString + " | "
                index = self.TangentweightFlagToIndex(pCurve.KeyGet(lCount).GetTangentWeightMode())
                lOutputString = lOutputString + tangentWVMode[index]
                lOutputString = lOutputString + " | "
                index = self.TangentVelocityFlagToIndex(pCurve.KeyGet(lCount).GetTangentVelocityMode())
                lOutputString = lOutputString + tangentWVMode[index]
            lOutputString = lOutputString + " ]"
            print(lOutputString)
        return timeValue


    def DisplayListCurve(self, pCurve, pProperty):
        lTimeString = []
        lListValue = ""
        lKeyCount = pCurve.KeyGetCount()
        timeValues = []
        for lCount in xrange(lKeyCount):
            lKeyValue = pCurve.KeyGetValue(lCount)
            lKeyTime = pCurve.KeyGetTime(lCount).GetMilliSeconds()
            timeValues.append((lKeyTime, lKeyValue))
            lOutputString = "            Key Time: "
            lOutputString = lOutputString + str(lKeyTime)
            lOutputString = lOutputString + ".... Key Value: "
            lOutputString = lOutputString + str(lKeyValue)
            lOutputString = lOutputString + " ("
            lOutputString = lOutputString + pProperty.GetEnumValue(lKeyValue)
            lOutputString = lOutputString + ")"
            lOutputString = lOutputString + ""
            print(lOutputString)
        return timeValues

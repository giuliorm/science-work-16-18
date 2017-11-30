import fbx, FbxCommon

class FbxCriteria:
    def __init__(self):
        self.ANIM_STACK_CRITERIA = FbxCommon.FbxCriteria.ObjectType(FbxCommon.FbxAnimStack.ClassId)
        self.ANIM_LAYER_CRITERIA = FbxCommon.FbxCriteria.ObjectType(FbxCommon.FbxAnimLayer.ClassId)

criteria = FbxCriteria()

FBXSDK_CURVENODE_COMPONENT_X = "X"
FBXSDK_CURVENODE_COMPONENT_Y = "Y"
FBXSDK_CURVENODE_COMPONENT_Z = "Z"

def DisplayAnimation(pscene):
    """

    :param pscene:
    :type pscene: FbxCommon.FbxScene
    :return:
    """
    for i in xrange(pscene.GetSrcObjectCount(criteria.ANIM_STACK_CRITERIA)):
        lAnimStack = pscene.GetSrcObject(criteria.ANIM_STACK_CRITERIA, i)
        lOutputString = "Animation Stack Name: "
        lOutputString = lOutputString + lAnimStack.GetName()
        lOutputString = lOutputString + "\n\n"
        #FBXSDK_printf(lOutputString);
        DisplayAnimationStack(lAnimStack, pscene.GetRootNode(), True)
        DisplayAnimationStack(lAnimStack, pscene.GetRootNode())

def DisplayAnimationStack(pAnimStack, pNode, isSwitcher):
    """

    :param pAnimStack:
    :type pAnimStack: FbxCommon.FbxAnimStack
    :param pNode:
    :type pNode: FbxCommon.FbxNode
    :param isSwitcher:
    :type isSwitcher: bool
    :return:
    """
    nbAnimLayers = pAnimStack.GetMemberCount(criteria.ANIM_LAYER_CRITERIA)
    lOutputString = "Animation stack contains "
    lOutputString = lOutputString + str(nbAnimLayers)
    lOutputString = lOutputString + " Animation Layer(s)\n"
    print(lOutputString)
    for l in xrange(nbAnimLayers):
        lAnimLayer = pAnimStack.GetMember(criteria.ANIM_LAYER_CRITERIA, l)
        lOutputString = "AnimLayer "
        lOutputString = lOutputString + str(l)
        lOutputString = lOutputString + "\n"
        print(lOutputString)
        DisplayAnimationLayer(lAnimLayer, pNode, isSwitcher)

def DisplayAnimationLayer(pAnimLayer, pNode, isSwitcher):
        lModelCount = 0
        lOutputString = "     Node Name: "
        lOutputString = lOutputString + pNode.GetName()
        lOutputString = lOutputString + "\n\n"
        print(lOutputString)
        DisplayChannels(pNode, pAnimLayer, isSwitcher) #??
        print("\n")
        for lModelCount in xrange(pNode.GetChildCount()):
            DisplayAnimationLayer(pAnimLayer, pNode.GetChild(lModelCount), isSwitcher)

def DisplayIfNotNone(lAnimCurve, message):
    if lAnimCurve:
        print(message)
        DisplayCurve(lAnimCurve)

def DisplayTranslation(pNode, pAnimLayer):
    lAnimCurve = pNode.LclTranslation.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_X)
    DisplayIfNotNone(lAnimCurve, "        TX\n")
    lAnimCurve = pNode.LclTranslation.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Y)
    DisplayIfNotNone(lAnimCurve, "        TY\n")
    lAnimCurve = pNode.LclTranslation.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Z)
    DisplayIfNotNone(lAnimCurve, "        TZ\n")

def DisplayRotation(pNode, pAnimLayer):
    lAnimCurve = pNode.LclRotation.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_X)
    DisplayIfNotNone(lAnimCurve, "        RX\n")
    lAnimCurve = pNode.LclRotation.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Y)
    DisplayIfNotNone(lAnimCurve, "        RY\n")
    lAnimCurve = pNode.LclRotation.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Z)
    DisplayIfNotNone(lAnimCurve, "        RZ\n")

def DisplayScaling(pNode, pAnimLayer):
    lAnimCurve = pNode.LclScaling.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_X)
    DisplayIfNotNone(lAnimCurve, "        SX\n")
    lAnimCurve = pNode.LclScaling.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Y)
    DisplayIfNotNone(lAnimCurve, "        SY\n")
    lAnimCurve = pNode.LclScaling.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Z)
    DisplayIfNotNone(lAnimCurve, "        SZ\n")

def DisplayColor(lNodeAttribute, pAnimLayer):
    lAnimCurve = lNodeAttribute.Color.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_X)
    DisplayIfNotNone(lAnimCurve, "        Red\n")
    lAnimCurve = lNodeAttribute.Color.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Y)
    DisplayIfNotNone(lAnimCurve, "        Green\n")
    lAnimCurve = lNodeAttribute.Color.GetCurve(pAnimLayer, FBXSDK_CURVENODE_COMPONENT_Z)
    DisplayIfNotNone(lAnimCurve, "        Blue\n")

def DisplayLight(light, pAnimLayer):
    lAnimCurve = light.Intensity.GetCurve(pAnimLayer)
    DisplayIfNotNone(lAnimCurve, "        Intensity\n")
    lAnimCurve = light.OuterAngle.GetCurve(pAnimLayer)
    DisplayIfNotNone(lAnimCurve, "        Outer Angle\n")
    lAnimCurve = light.Fog.GetCurve(pAnimLayer)
    DisplayIfNotNone(lAnimCurve, "        Fog\n")

def DisplayCamera(camera, pAnimLayer):
    lAnimCurve = camera.FieldOfView.GetCurve(pAnimLayer)
    DisplayIfNotNone(lAnimCurve, "        Field of View\n")
    lAnimCurve = camera.FieldOfViewX.GetCurve(pAnimLayer)
    DisplayIfNotNone(lAnimCurve, "        Field of View X\n")
    lAnimCurve = camera.FieldOfViewY.GetCurve(pAnimLayer)
    DisplayIfNotNone(lAnimCurve, "        Field of View Y\n")
    lAnimCurve = camera.OpticalCenterX.GetCurve(pAnimLayer)
    DisplayIfNotNone(lAnimCurve, "        Optical Center X\n")
    lAnimCurve = camera.OpticalCenterY.GetCurve(pAnimLayer)
    DisplayIfNotNone(lAnimCurve, "        Optical Center Y\n")
    lAnimCurve = camera.Roll.GetCurve(pAnimLayer)
    DisplayIfNotNone(lAnimCurve, "        Roll\n")

def DisplayNodeAttribute(pAnimLayer, lNodeAttribute):
    if not lNodeAttribute:
        return
    if lNodeAttribute.GetAttributeType() == FbxCommon.FbxNodeAttribute.eMesh or \
            lNodeAttribute.GetAttributeType() == FbxCommon.FbxNodeAttribute.eNurbs or \
            lNodeAttribute.GetAttributeType() == FbxCommon.FbxNodeAttribute.ePatch:
        lGeometry = lNodeAttribute
        lBlendShapeDeformerCount = lGeometry.GetDeformerCount(FbxCommon.FbxDeformer.eBlendShape)
        for lBlendShapeIndex in xrange(lBlendShapeDeformerCount):
            lBlendShape = lGeometry.GetDeformer(lBlendShapeIndex, FbxCommon.FbxDeformer.eBlendShape)
            lBlendShapeChannelCount = lBlendShape.GetBlendShapeChannelCount()
            for lChannelIndex in xrange(lBlendShapeChannelCount):
                lChannel = lBlendShape.GetBlendShapeChannel(lChannelIndex)
                lChannelName = lChannel.GetName()
                lAnimCurve = lGeometry.GetShapeChannel(lBlendShapeIndex, lChannelIndex, pAnimLayer, True)
                if lAnimCurve:
                    print("        Shape %s\n", lChannelName)
                    DisplayCurve(lAnimCurve)

def DisplayNumberProperty(lDataType, lProperty, lCurveNode):
    if lDataType.GetType() == FbxCommon.eFbxBool or \
                    lDataType.GetType() == FbxCommon.eFbxDouble or \
                    lDataType.GetType() == FbxCommon.eFbxFloat or \
                    lDataType.GetType() == FbxCommon.eFbxInt:
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
                DisplayCurve(lAnimCurve)

def DisplayEnumProperty(lDataType, lProperty, lCurveNode):
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
                DisplayListCurve(lAnimCurve, lProperty)

def DisplayDoubleOrColorProperty(lDataType, lProperty, lCurveNode):
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
            DisplayIfNotNone(lAnimCurve, "        Component {0}".format(lComponentName1))
        for c in xrange(lCurveNode.GetCurveCount(1)):
            lAnimCurve = lCurveNode.GetCurve(1, c)
            DisplayIfNotNone(lAnimCurve, "        Component {0}".format(lComponentName2))
        for c in xrange(lCurveNode.GetCurveCount(2)):
            lAnimCurve = lCurveNode.GetCurve(2, c)
            DisplayIfNotNone(lAnimCurve, "        Component {0}".format(lComponentName3))

def DisplayProperty(pNode, pAnimLayer, lProperty):
    while lProperty.IsValid():
        if lProperty.GetFlag(FbxCommon.FbxPropertyFlags.eUserDefined):
            lFbxFCurveNodeName = lProperty.GetName()
            lCurveNode = lProperty.GetCurveNode(pAnimLayer)
            if not lCurveNode:
                lProperty = pNode.GetNextProperty(lProperty)
                continue

            lDataType = lProperty.GetPropertyDataType()
            DisplayNumberProperty(lDataType, lProperty, lCurveNode)
            DisplayDoubleOrColorProperty(lDataType, lProperty, lCurveNode)
            DisplayEnumProperty(lDataType, lProperty, lCurveNode)
            lProperty = pNode.GetNextProperty(lProperty)

def DisplayChannels(pNode, pAnimLayer, isSwitcher):
    lAnimCurve = None
    if isSwitcher:
        DisplayTranslation(pNode, pAnimLayer)
        DisplayRotation(pNode, pAnimLayer)
        DisplayScaling(pNode, pAnimLayer)

    lNodeAttribute = pNode.GetNodeAttribute()
    if lNodeAttribute:
        DisplayColor(lNodeAttribute, pAnimLayer)
    light = pNode.GetLight()
    if light:
        DisplayLight(light, pAnimLayer)
    camera = pNode.GetCamera()
    if camera:
        DisplayCamera(camera, pAnimLayer)

    DisplayNodeAttribute(pAnimLayer, lNodeAttribute)

    lProperty = pNode.GetFirstProperty()
    DisplayProperty(pNode, pAnimLayer, lProperty)

def InterpolationFlagToIndex(flags):
    if flags and FbxCommon.FbxAnimCurveDef.eInterpolationConstant == \
            FbxCommon.FbxAnimCurveDef.eInterpolationConstant:
        return 1
    if flags and FbxCommon.FbxAnimCurveDef.eInterpolationLinear == FbxCommon.FbxAnimCurveDef.eInterpolationLinear:
        return 2
    if flags and FbxCommon.FbxAnimCurveDef.eInterpolationCubic == FbxCommon.FbxAnimCurveDef.eInterpolationCubic:
        return 3
    return 0

def ConstantmodeFlagToIndex(flags):
    if flags and FbxCommon.FbxAnimCurveDef.eConstantStandard == FbxCommon.FbxAnimCurveDef.eConstantStandard:
        return 1
    if flags and FbxCommon.FbxAnimCurveDef.eConstantNext == FbxCommon.FbxAnimCurveDef.eConstantNext:
        return 2
    return 0

def TangentmodeFlagToIndex(flags):
    if flags and FbxCommon.FbxAnimCurveDef.eTangentAuto == FbxCommon.FbxAnimCurveDef.eTangentAuto: return 1
    if flags and FbxCommon.FbxAnimCurveDef.eTangentAutoBreak == FbxCommon.FbxAnimCurveDef.eTangentAutoBreak: return 2
    if flags and FbxCommon.FbxAnimCurveDef.eTangentTCB == FbxCommon.FbxAnimCurveDef.eTangentTCB: return 3
    if flags and FbxCommon.FbxAnimCurveDef.eTangentUser == FbxCommon.FbxAnimCurveDef.eTangentUser: return 4
    if flags and FbxCommon.FbxAnimCurveDef.eTangentGenericBreak == FbxCommon.FbxAnimCurveDef.eTangentGenericBreak:
        return 5;
    if flags and FbxCommon.FbxAnimCurveDef.eTangentBreak == FbxCommon.FbxAnimCurveDef.eTangentBreak: return 6
    return 0

def TangentweightFlagToIndex(flags):
    if flags and FbxCommon.FbxAnimCurveDef.eWeightedNone == FbxCommon.FbxAnimCurveDef.eWeightedNone: return 1
    if flags and FbxCommon.FbxAnimCurveDef.eWeightedRight == FbxCommon.FbxAnimCurveDef.eWeightedRight: return 2
    if flags and FbxCommon.FbxAnimCurveDef.eWeightedNextLeft == FbxCommon.FbxAnimCurveDef.eWeightedNextLeft: return 3
    return 0

def TangentVelocityFlagToIndex(flags):
    if flags and FbxCommon.FbxAnimCurveDef.eVelocityNone == FbxCommon.FbxAnimCurveDef.eVelocityNone: return 1
    if flags and FbxCommon.FbxAnimCurveDef.eVelocityRight == FbxCommon.FbxAnimCurveDef.eVelocityRight: return 2
    if flags and FbxCommon.FbxAnimCurveDef.eVelocityNextLeft == FbxCommon.FbxAnimCurveDef.eVelocityNextLeft: return 3
    return 0


def DisplayCurve(pCurve):
    interpolation = ["?", "constant", "linear", "cubic"]
    constantMode = ["?", "Standard", "Next"]
    cubicMode = ["?", "Auto", "Auto break", "Tcb", "User", "Break", "User break"]
    tangentWVMode = ["?", "None", "Right", "Next left"]
    lTimeString = []
    lKeyCount = pCurve.KeyGetCount()
    for lCount in xrange(lKeyCount):
        lKeyValue = pCurve.KeyGetValue(lCount)
        lKeyTime = pCurve.KeyGetTime(lCount)
        lOutputString = "            Key Time: "
        #lOutputString = lKeyTime.GetTimeString(lTimeString, FbxCommon.FbxUShort(256))
        lOutputString = lOutputString + str(lKeyTime)
        lOutputString = lOutputString + ".... Key Value: "
        lOutputString = lOutputString + lKeyValue
        lOutputString = lOutputString + " [ "
        lOutputString = lOutputString + interpolation[InterpolationFlagToIndex(pCurve.KeyGetInterpolation(lCount))]
        if pCurve.KeyGetInterpolation(lCount) and \
            FbxCommon.FbxAnimCurveDef.eInterpolationConstant == FbxCommon.FbxAnimCurveDef.eInterpolationConstant:
            lOutputString = lOutputString + " | "
            lOutputString = lOutputString + constantMode[ConstantmodeFlagToIndex(pCurve.KeyGetConstantMode(lCount))]
        elif pCurve.KeyGetInterpolation(lCount) and \
                FbxCommon.FbxAnimCurveDef.eInterpolationCubic == FbxCommon.FbxAnimCurveDef.eInterpolationCubic:
            lOutputString = lOutputString + " | "
            lOutputString = lOutputString + cubicMode[TangentmodeFlagToIndex(pCurve.KeyGetTangentMode(lCount))]
            lOutputString = lOutputString + " | "
            lOutputString = lOutputString + tangentWVMode[TangentweightFlagToIndex(pCurve.KeyGet(lCount)
                                                                                   .GetTangentWeightMode())]
            lOutputString = lOutputString + " | "
            lOutputString = lOutputString + tangentWVMode[TangentVelocityFlagToIndex(pCurve.KeyGet(lCount)
                                                                                     .GetTangentVelocityMode())]
        lOutputString = lOutputString + " ]"
        lOutputString = lOutputString + "\n"
        print(lOutputString)


def DisplayListCurve(pCurve, pProperty):
    lTimeString = []
    lListValue = ""
    lKeyCount = pCurve.KeyGetCount()
    for lCount in xrange(lKeyCount):
        lKeyValue = pCurve.KeyGetValue(lCount)
        lKeyTime = pCurve.KeyGetTime(lCount)
        lOutputString = "            Key Time: "
        #lOutputString = lOutputString + lKeyTime.GetTimeString(lTimeString, FbxUShort(256));
        lOutputString = lOutputString + str(lKeyTime)
        lOutputString = lOutputString + ".... Key Value: "
        lOutputString = lOutputString + str(lKeyValue)
        lOutputString = lOutputString + " ("
        lOutputString = lOutputString + pProperty.GetEnumValue(lKeyValue)
        lOutputString = lOutputString + ")"
        lOutputString = lOutputString + "\n"
        print(lOutputString)

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import maya.api.OpenMaya as om

from shiboken2 import wrapInstance


def maya_main_window():

    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class MainWindow(QtWidgets.QDialog):

    WINDOW_TITLE = "MoCap-AutoRigger v1.0.0"

    def __init__(self, parent=maya_main_window()):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumWidth(600)
        #self.setMinimumHeight(600)

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.createWidgets()
        self.createLayout()

    def createWidgets(self):
        self.createLocatorBut = QtWidgets.QPushButton('Create Locator')
        self.createLocatorBut.clicked.connect(self.createLocator)
        self.deleteLocatorBut = QtWidgets.QPushButton('Delete Locator')
        self.deleteLocatorBut.clicked.connect(self.deleteLocator)
        self.createSpineText = QtWidgets.QLineEdit()
        self.countFingers = QtWidgets.QLineEdit()
        self.mirrorCheckBox = QtWidgets.QCheckBox()
        self.editModeCheckBox = QtWidgets.QCheckBox()

    def createLayout(self):
        form_layout_1 = QtWidgets.QFormLayout()
        form_layout_1.addRow("Enter No. Of Spine:", self.createSpineText)
        form_layout_1.addRow("Enter No. Of Finger:", self.countFingers)

        form_layout_2 = QtWidgets.QFormLayout()
        form_layout_2.addRow("Mirror Loc (X)->(-X)", self.mirrorCheckBox)
        form_layout_2.addRow("Edit Mode", self.editModeCheckBox)


        horizonLayout = QtWidgets.QHBoxLayout()
        horizonLayout.addWidget(self.createLocatorBut)
        horizonLayout.addWidget(self.deleteLocatorBut)
        horizonLayout.addLayout(form_layout_2)
        #horizonLayout.addWidget(self.mirrorCheckBox)
        #horizonLayout.addWidget(self.editModeCheckBox)
        #subLayoutH.addStretch()

        mainLayoutV = QtWidgets.QVBoxLayout(self)
        mainLayoutV.addLayout(horizonLayout)
        mainLayoutV.addLayout(form_layout_1)

    def createUIConnection(self):
        self.mirrorCheckBox.toggled.connect(self.mirrorLocator)
        self.editModeCheckBox.toggled.connect(self.editMode)

    def createLocator(self):
        loc_nam = "loc_grp"
        obj_list = om.MSelectionList()

        try:
            obj_list.add(loc_nam)
        except:
            loc_grp = om.MFnDagNode()
            loc_obj = loc_grp.create("transform", "loc_Grp")
            self.loc_root_tn = loc_grp.create("transform", "loc_Root", loc_obj)
            loc_root_mn = loc_grp.create("locator", "locatorShape1", self.loc_root_tn)

            loc_transform = om.MFnTransform(self.loc_root_tn)

            loc_plug_ty = loc_transform.findPlug("translateY", False)
            loc_plug_ty.setInt(1)
        else:
            print("loc_grp already exist")

        self.createSpine()

    def createSpine(self):
        spineloc_grp = om.MFnDagNode()

        for i in range(0, int(self.createSpineText.text())):

            if i == 0:
                self.spine_tn = spineloc_grp.create("transform", "loc_Spine_"+str(i), self.loc_root_tn)
                spine_ln = spineloc_grp.create("locator", "locatorShape1", self.spine_tn)
            else:
                self.spine_tn = spineloc_grp.create("transform", "loc_Spine_"+str(i), self.spine_tn)
                spine_ln = spineloc_grp.create("locator", "locatorShape1", self.spine_tn)

            spineloc_transform = om.MFnTransform(self.spine_tn)
            spineloc_plug_ty = spineloc_transform.findPlug("translateY", False)
            spineloc_plug_ty.setDouble(2.25)

        self.createShoulder(1)
        self.createShoulder(-1)
        self.createArms(1)
        self.createArms(-1)
        self.createHead()
        self.createLegs(1)
        self.createLegs(-1)

    def createHead(self):
        headloc_grp = om.MFnDagNode()

        neckloc_tn = headloc_grp.create("transform", "loc_neck", self.spine_tn)
        neckloc_ln = headloc_grp.create("locator", "locatorShape1", neckloc_tn)

        neckloc_transform_t = om.MFnTransform(neckloc_tn)
        neckloc_plug_s = neckloc_transform_t.findPlug("scale", False)

        if neckloc_plug_s.isCompound:
            for i in range(neckloc_plug_s.numChildren()):
                child_plug = neckloc_plug_s.child(i)

                attr_value = child_plug.setDouble(0.5)

        neckloc_plug_ty = neckloc_transform_t.findPlug("translateY", False)
        neckloc_plug_ty.setDouble((((int(self.createSpineText.text())-1)*0.5)+1.25))

        headlowloc_tn = headloc_grp.create("transform", "loc_headlower", neckloc_tn)
        headlowloc_ln = headloc_grp.create("locator", "locatorShape1", headlowloc_tn)

        headlowloc_transform_t = om.MFnTransform(headlowloc_tn)
        headlowloc_plug_ty = headlowloc_transform_t.findPlug("translateY", False)
        headlowloc_plug_ty.setDouble((((int(self.createSpineText.text())-1)*0.5)+0.75))

        headendloc_tn = headloc_grp.create("transform", "loc_headend", headlowloc_tn)
        headendloc_ln = headloc_grp.create("locator", "locatorShape1", headendloc_tn)

        headendloc_transform_t = om.MFnTransform(headendloc_tn)
        headendloc_plug_ty = headendloc_transform_t.findPlug("translateY", False)
        headendloc_plug_ty.setDouble((((int(self.createSpineText.text())-1)*0.5)+3))

    def createShoulder(self, side):
        loc_shoulder = ["loc_L_shoulder", "loc_R_shoulder"]
        obj_list = om.MSelectionList()
        shoulderloc_grp = om.MFnDagNode()

        if side == 1:
            try:
                obj_list.add(loc_shoulder[0])
            except:
                self.l_shoulder_tn = shoulderloc_grp.create("transform", "loc_L_shoulder", self.spine_tn)
                l_shoulder_ln = shoulderloc_grp.create("locator", "locatorShape1", self.l_shoulder_tn)

                lshoulder_transform = om.MFnTransform(self.l_shoulder_tn)
                lshoulder_plug_s = lshoulder_transform.findPlug("scale", False)

                if lshoulder_plug_s.isCompound:
                    for i in range(lshoulder_plug_s.numChildren()):
                        child_plug = lshoulder_plug_s.child(i)

                        attr_value = child_plug.setDouble(0.5)

                lshoulder_plug_t = lshoulder_transform.findPlug("translate", False)

                if lshoulder_plug_t.isCompound:
                    for i in range(lshoulder_plug_t.numChildren()):
                        child_plugX = lshoulder_plug_t.child(0)
                        child_plugY = lshoulder_plug_t.child(1)

                        attr_valueX = child_plugX.setDouble(2.50)
                        attr_valueY = child_plugY.setDouble((((int(self.createSpineText.text())-1)*0.5)+0.50))

        if side == -1:
            try:
                obj_list.add(loc_shoulder[1])
            except:
                self.r_shoulder_tn = shoulderloc_grp.create("transform", "loc_R_shoulder", self.spine_tn)
                r_shoulder_ln = shoulderloc_grp.create("locator", "locatorShape1", self.r_shoulder_tn)

                rshoulder_transform = om.MFnTransform(self.r_shoulder_tn)
                rshoulder_plug_s = rshoulder_transform.findPlug("scale", False)

                if rshoulder_plug_s.isCompound:
                    for i in range(rshoulder_plug_s.numChildren()):
                        child_plug = rshoulder_plug_s.child(i)

                        attr_value = child_plug.setDouble(0.5)

                rshoulder_plug_t = rshoulder_transform.findPlug("translate", False)

                if rshoulder_plug_t.isCompound:
                    for i in range(rshoulder_plug_t.numChildren()):
                        child_plugX = rshoulder_plug_t.child(0)
                        child_plugY = rshoulder_plug_t.child(1)

                        attr_valueX = child_plugX.setDouble(-2.50)
                        attr_valueY = child_plugY.setDouble((((int(self.createSpineText.text())-1)*0.5)+0.50))

    def createArms(self, side):
        loc_arm = ["loc_L_arm_grp", "loc_R_arm_grp"]
        obj_list = om.MSelectionList()
        armloc_grp = om.MFnDagNode()

        if side == 1:
            try:
                obj_list.add(loc_arm[0])
            except:
                self.l_arm_Grp = armloc_grp.create("transform", "loc_L_arm_grp", self.l_shoulder_tn)
                up_Larm_tn = armloc_grp.create("transform", "loc_L_upperarm", self.l_arm_Grp)
                up_Larm_ln = armloc_grp.create("locator", "locatorShape1", up_Larm_tn)

                larmloc_transform = om.MFnTransform(self.l_arm_Grp)
                larmloc_plug_tx = larmloc_transform.findPlug("translateX", False)
                larmloc_plug_ty = larmloc_transform.findPlug("translateY", False)
                larmloc_plug_tx.setDouble(4.5)
                larmloc_plug_ty.setDouble(-(((int(self.createSpineText.text())-1)*0.5)+2))

                l_elbow_tn = armloc_grp.create("transform", "loc_L_elbow", up_Larm_tn)
                l_elbow_ln = armloc_grp.create("locator", "locatorShape1", l_elbow_tn)

                lelbowloc_transform = om.MFnTransform(l_elbow_tn)
                lelbow_plug_t = lelbowloc_transform.findPlug("translate", False)

                if lelbow_plug_t.isCompound:
                    for i in range(lelbow_plug_t.numChildren()):
                        child_plugX = lelbow_plug_t.child(0)
                        child_plugY = lelbow_plug_t.child(1)

                        attr_valueX = child_plugX.setDouble(4.35)
                        attr_valueY = child_plugY.setDouble(-(((int(self.createSpineText.text())-1)*0.5)+5.25))

                self.l_wrist_tn = armloc_grp.create("transform", "loc_L_wrist", l_elbow_tn)
                l_wrist_ln = armloc_grp.create("locator", "locatorShape1", self.l_wrist_tn)

                lwristloc_transform = om.MFnTransform(self.l_wrist_tn)
                lwrist_plug_t = lwristloc_transform.findPlug("translate", False)

                if lwrist_plug_t.isCompound:
                    for i in range(lwrist_plug_t.numChildren()):
                        child_plugX = lwrist_plug_t.child(0)
                        child_plugY = lwrist_plug_t.child(1)

                        attr_valueX = child_plugX.setDouble(6.35)
                        attr_valueY = child_plugY.setDouble(-(((int(self.createSpineText.text())-1)*0.5)+6.25))

                self.createHands(1)
            else:
                print("loc_Larm_grp already exist")


        if side == -1:
            try:
                obj_list.add(loc_arm[1])
            except:
                self.r_arm_Grp = armloc_grp.create("transform", "loc_R_arm_grp", self.r_shoulder_tn)
                up_Rarm_tn = armloc_grp.create("transform", "loc_R_upperarm", self.r_arm_Grp)
                up_Rarm_ln = armloc_grp.create("locator", "locatorShape1", up_Rarm_tn)

                rarmloc_transform = om.MFnTransform(self.r_arm_Grp)
                rarmloc_plug_tx = rarmloc_transform.findPlug("translateX", False)
                rarmloc_plug_ty = rarmloc_transform.findPlug("translateY", False)
                rarmloc_plug_tx.setDouble(-4.5)
                rarmloc_plug_ty.setDouble(-(((int(self.createSpineText.text())-1)*0.5)+2))

                r_elbow_tn = armloc_grp.create("transform", "loc_R_elbow", up_Rarm_tn)
                r_elbow_ln = armloc_grp.create("locator", "locatorShape1", r_elbow_tn)

                relbowloc_transform = om.MFnTransform(r_elbow_tn)
                relbow_plug_t = relbowloc_transform.findPlug("translate", False)

                if relbow_plug_t.isCompound:
                    for i in range(relbow_plug_t.numChildren()):
                        child_plugX = relbow_plug_t.child(0)
                        child_plugY = relbow_plug_t.child(1)

                        attr_valueX = child_plugX.setDouble(-4.35)
                        attr_valueY = child_plugY.setDouble(-(((int(self.createSpineText.text())-1)*0.5)+5.25))

                self.r_wrist_tn = armloc_grp.create("transform", "loc_R_wrist", r_elbow_tn)
                r_wrist_ln = armloc_grp.create("locator", "locatorShape1", self.r_wrist_tn)

                rwristloc_transform = om.MFnTransform(self.r_wrist_tn)
                rwrist_plug_t = rwristloc_transform.findPlug("translate", False)

                if rwrist_plug_t.isCompound:
                    for i in range(rwrist_plug_t.numChildren()):
                        child_plugX = rwrist_plug_t.child(0)
                        child_plugY = rwrist_plug_t.child(1)

                        attr_valueX = child_plugX.setDouble(-6.35)
                        attr_valueY = child_plugY.setDouble(-(((int(self.createSpineText.text())-1)*0.5)+6.25))

                self.createHands(-1)
            else:
                print("loc_Larm_grp already exist")

            self.createHands(-1)

    def createHands(self, side):
        loc_hand = ["loc_L_hand_grp", "loc_R_hand_grp"]
        obj_list = om.MSelectionList()
        handloc_grp = om.MFnDagNode()

        if side == 1:
            try:
                obj_list.add(loc_hand[0])
            except:
                self.l_hand_tn = handloc_grp.create("transform", "loc_L_hand_grp", self.l_wrist_tn)

                for i in range(0, int(self.countFingers.text())):
                    self.createFingers(1, i)

        if side == -1:
            try:
                obj_list.add(loc_hand[1])
            except:
                self.r_hand_tn = handloc_grp.create("transform", "loc_R_hand_grp", self.r_wrist_tn)

                for i in range(0, int(self.countFingers.text())):
                    self.createFingers(-1, i)

    def createFingers(self, side, count):
        fingerloc_grp = om.MFnDagNode()

        for i in range(0,4):
            if side == 1:
                if i == 0:
                    self.loc_lfinger_tn = fingerloc_grp.create("transform", "loc_L_finger_"+str(count)+"_"+str(i), self.l_hand_tn)
                    loc_lfinger_ln = fingerloc_grp.create("locator", "locatorShape1", self.loc_lfinger_tn)

                    l_finger_transform_t = om.MFnTransform(self.loc_lfinger_tn)
                    l_finger_plug_t = l_finger_transform_t.findPlug("translate", False)

                    if l_finger_plug_t.isCompound:
                        for i in range(l_finger_plug_t.numChildren()):
                            child_plugX = l_finger_plug_t.child(0)
                            child_plugY = l_finger_plug_t.child(1)
                            child_plugZ = l_finger_plug_t.child(2)

                            attr_valueX = child_plugX.setDouble(1)
                            attr_valueY = child_plugY.setDouble(-2)
                            attr_valueZ = child_plugZ.setDouble(count*1)

                    l_finger_plug_s = l_finger_transform_t.findPlug("scale", False)

                    if l_finger_plug_s.isCompound:
                        for i in range(l_finger_plug_s.numChildren()):
                            child_plug = l_finger_plug_s.child(i)

                            attr_value = child_plug.setDouble(0.5)


                else:
                    self.loc_lfinger_tn = fingerloc_grp.create("transform", "loc_L_finger_"+str(count)+"_"+str(i), self.loc_lfinger_tn)
                    loc_lfinger_ln = fingerloc_grp.create("locator", "locatorShape1", self.loc_lfinger_tn)

                    l_finger_transform_t = om.MFnTransform(self.loc_lfinger_tn)
                    l_finger_plug_t = l_finger_transform_t.findPlug("translate", False)

                    if l_finger_plug_t.isCompound:
                        for i in range(l_finger_plug_t.numChildren()):
                            child_plugX = l_finger_plug_t.child(0)
                            child_plugY = l_finger_plug_t.child(1)

                            attr_valueX = child_plugX.setDouble(1)
                            attr_valueY = child_plugY.setDouble(-1)

            if side == -1:
                if i == 0:
                    self.loc_rfinger_tn = fingerloc_grp.create("transform", "loc_R_finger_"+str(count)+"_"+str(i), self.r_hand_tn)
                    loc_rfinger_ln = fingerloc_grp.create("locator", "locatorShape1", self.loc_rfinger_tn)

                    r_finger_transform_t = om.MFnTransform(self.loc_rfinger_tn)
                    r_finger_plug_t = r_finger_transform_t.findPlug("translate", False)

                    if r_finger_plug_t.isCompound:
                        for i in range(r_finger_plug_t.numChildren()):
                            child_plugX = r_finger_plug_t.child(0)
                            child_plugY = r_finger_plug_t.child(1)
                            child_plugZ = r_finger_plug_t.child(2)

                            attr_valueX = child_plugX.setDouble(-1)
                            attr_valueY = child_plugY.setDouble(-2)
                            attr_valueZ = child_plugZ.setDouble(count*1)

                    r_finger_plug_s = r_finger_transform_t.findPlug("scale", False)

                    if r_finger_plug_s.isCompound:
                        for i in range(r_finger_plug_s.numChildren()):
                            child_plug = r_finger_plug_s.child(i)

                            attr_value = child_plug.setDouble(0.5)
                else:
                    self.loc_rfinger_tn = fingerloc_grp.create("transform", "loc_R_finger_"+str(count)+"_"+str(i), self.loc_rfinger_tn)
                    loc_rfinger_ln = fingerloc_grp.create("locator", "locatorShape1", self.loc_rfinger_tn)

                    r_finger_transform_t = om.MFnTransform(self.loc_rfinger_tn)
                    r_finger_plug_t = r_finger_transform_t.findPlug("translate", False)

                    if r_finger_plug_t.isCompound:
                        for i in range(r_finger_plug_t.numChildren()):
                            child_plugX = r_finger_plug_t.child(0)
                            child_plugY = r_finger_plug_t.child(1)

                            attr_valueX = child_plugX.setDouble(-1)
                            attr_valueY = child_plugY.setDouble(-1)

    def createLegs(self, side):
        loc_leg = ["loc_L_leg_grp", "loc_R_leg_grp"]
        obj_list = om.MSelectionList()
        legloc_grp = om.MFnDagNode()

        if side == 1:
            try:
                obj_list.add(loc_leg[0])
            except:
                l_leg_Grp = legloc_grp.create("transform", "loc_L_leg_grp", self.loc_root_tn)
                l_upleg_tn = legloc_grp.create("transform", "loc_l_upperleg", l_leg_Grp)
                l_upleg_ln = legloc_grp.create("locator", "locatorShape1", l_upleg_tn)

                l_leg_transform_t = om.MFnTransform(l_leg_Grp)
                l_leg_plug_tx = l_leg_transform_t.findPlug("translateX", False)
                l_leg_plug_ty = l_leg_transform_t.findPlug("translateY", False)
                l_leg_plug_tx.setDouble(2.35)
                l_leg_plug_ty.setDouble(-(((int(self.createSpineText.text()))*0.5)+1))

                l_leg_transform_s = om.MFnTransform(l_upleg_tn)
                l_leg_plug_s = l_leg_transform_s.findPlug("scale", False)

                if l_leg_plug_s.isCompound:
                    for i in range(l_leg_plug_s.numChildren()):
                        child_plug = l_leg_plug_s.child(i)

                        attr_value = child_plug.setDouble(0.7)

                l_knee_tn = legloc_grp.create("transform", "loc_l_knee", l_upleg_tn)
                l_knee_ln = legloc_grp.create("locator", "locatorShape1", l_knee_tn)

                l_knee_transform_t = om.MFnTransform(l_knee_tn)
                l_knee_plug_ty = l_knee_transform_t.findPlug("translateY", False)
                l_knee_plug_ty.setDouble(-((int(self.createSpineText.text())*2.5)))

                l_football_tn = legloc_grp.create("transform", "loc_l_football", l_knee_tn)
                l_football_ln = legloc_grp.create("locator", "locatorShape1", l_football_tn)

                l_football_transform_t = om.MFnTransform(l_football_tn)
                l_football_plug_ty = l_football_transform_t.findPlug("translateY", False)
                l_football_plug_ty.setDouble(-((int(self.createSpineText.text())*3.5)))

                l_foot_tn = legloc_grp.create("transform", "loc_l_foot", l_football_tn)
                l_football_ln = legloc_grp.create("locator", "locatorShape1", l_foot_tn)

                l_foot_transform_t = om.MFnTransform(l_foot_tn)
                l_foot_plug_ty = l_foot_transform_t.findPlug("translateY", False)
                l_foot_plug_tz = l_foot_transform_t.findPlug("translateZ", False)
                l_foot_plug_ty.setDouble(-((int(self.createSpineText.text())*0.5)))
                l_foot_plug_tz.setDouble(((int(self.createSpineText.text())*0.7)))

                l_toe_tn = legloc_grp.create("transform", "loc_l_toe", l_foot_tn)
                l_toe_ln = legloc_grp.create("locator", "locatorShape1", l_toe_tn)

                l_toe_transform_t = om.MFnTransform(l_toe_tn)
                l_toe_plug_tz = l_toe_transform_t.findPlug("translateZ", False)
                l_toe_plug_tz.setDouble(((int(self.createSpineText.text())*0.7)))

        if side == -1:
            try:
                obj_list.add(loc_leg[1])
            except:
                r_leg_Grp = legloc_grp.create("transform", "loc_L_leg_grp", self.loc_root_tn)
                r_upleg_tn = legloc_grp.create("transform", "loc_l_upperleg", r_leg_Grp)
                r_upleg_ln = legloc_grp.create("locator", "locatorShape1", r_upleg_tn)

                r_leg_transform_t = om.MFnTransform(r_leg_Grp)
                r_leg_plug_tx = r_leg_transform_t.findPlug("translateX", False)
                r_leg_plug_ty = r_leg_transform_t.findPlug("translateY", False)
                r_leg_plug_tx.setDouble(-2.35)
                r_leg_plug_ty.setDouble(-(((int(self.createSpineText.text()))*0.5)+1))

                r_leg_transform_s = om.MFnTransform(r_upleg_tn)
                r_leg_plug_s = r_leg_transform_s.findPlug("scale", False)

                if r_leg_plug_s.isCompound:
                    for i in range(r_leg_plug_s.numChildren()):
                        child_plug = r_leg_plug_s.child(i)

                        attr_value = child_plug.setDouble(0.7)

                r_knee_tn = legloc_grp.create("transform", "loc_l_knee", r_upleg_tn)
                r_knee_ln = legloc_grp.create("locator", "locatorShape1", r_knee_tn)

                r_knee_transform_t = om.MFnTransform(r_knee_tn)
                r_knee_plug_ty = r_knee_transform_t.findPlug("translateY", False)
                r_knee_plug_ty.setDouble(-((int(self.createSpineText.text())*2.5)))

                r_football_tn = legloc_grp.create("transform", "loc_l_football", r_knee_tn)
                r_football_ln = legloc_grp.create("locator", "locatorShape1", r_football_tn)

                r_football_transform_t = om.MFnTransform(r_football_tn)
                r_football_plug_ty = r_football_transform_t.findPlug("translateY", False)
                r_football_plug_ty.setDouble(-((int(self.createSpineText.text())*3.5)))

                r_foot_tn = legloc_grp.create("transform", "loc_l_foot", r_football_tn)
                r_football_ln = legloc_grp.create("locator", "locatorShape1", r_foot_tn)

                r_foot_transform_t = om.MFnTransform(r_foot_tn)
                r_foot_plug_ty = r_foot_transform_t.findPlug("translateY", False)
                r_foot_plug_tz = r_foot_transform_t.findPlug("translateZ", False)
                r_foot_plug_ty.setDouble(-((int(self.createSpineText.text())*0.5)))
                r_foot_plug_tz.setDouble(((int(self.createSpineText.text())*0.7)))

                r_toe_tn = legloc_grp.create("transform", "loc_l_toe", r_foot_tn)
                r_toe_ln = legloc_grp.create("locator", "locatorShape1", r_toe_tn)

                r_toe_transform_t = om.MFnTransform(r_toe_tn)
                r_toe_plug_tz = r_toe_transform_t.findPlug("translateZ", False)
                r_toe_plug_tz.setDouble(((int(self.createSpineText.text())*0.7)))

    def mirrorLocator(self):
        mirrorLocator = self.mirrorLocator.isChecked()

    def editMode(self):
        print("2")

    def deleteLocator(self):
        node = cmds.ls("loc_*")
        cmds.delete(node)

try:
    display_dailog.close()
    display_dailog.deleteLater()
except:
    pass

display_dailog = MainWindow()
display_dailog.show()

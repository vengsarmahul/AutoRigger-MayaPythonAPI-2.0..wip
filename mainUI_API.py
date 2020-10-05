from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

import maya.OpenMayaUI as omui1
import maya.cmds as cmds
import maya.api.OpenMaya as om2
import maya.api.OpenMayaUI as omui2
import maya.OpenMaya as om1
import maya.OpenMayaAnim as omanim1
import math

from shiboken2 import wrapInstance


def maya_main_window():

    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui1.MQtUtil.mainWindow()
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
        self.createUIConnection()

    def createWidgets(self):
        self.createLocatorBut = QtWidgets.QPushButton('Create Locator')
        self.deleteLocatorBut = QtWidgets.QPushButton('Delete Locator')
        self.mirrorLocatorBut = QtWidgets.QPushButton('Mirror Locator (X)-->(-X)')
        self.createJointBut = QtWidgets.QPushButton('Create Joints')
        self.insertJointBut = QtWidgets.QPushButton('Insert Joint')
        self.deleteJointBut = QtWidgets.QPushButton('Delete Joints')
        self.jointOrientBut = QtWidgets.QPushButton('Set Orientation')
        self.boundingBoxBut = QtWidgets.QPushButton('Create Override Bounding Box')
        self.rigCharBut = QtWidgets.QPushButton('Rig Character')
        self.delRigBut = QtWidgets.QPushButton('Delete Rig')


        self.createSpineText = QtWidgets.QLineEdit()
        self.countFingers = QtWidgets.QLineEdit()

        self.editModeCheckBox = QtWidgets.QCheckBox()

        self.typeofJointOrient = QtWidgets.QComboBox()
        self.typeofJointOrient.addItems(["Option 1(mixamo compatible)", "Option 2(world space)"])

        self.typeofRigComboBox = QtWidgets.QComboBox()
        self.typeofRigComboBox.addItems(["Biped Rig", "Quadruple Rig"])

        self.typeofLHandIK = QtWidgets.QComboBox()
        self.typeofLHandIK.addItems(["None", "Rotate Plane IK"])

        self.typeofRHandIK = QtWidgets.QComboBox()
        self.typeofRHandIK.addItems(["None", "Rotate Plane IK"])

        self.typeofLLegIK = QtWidgets.QComboBox()
        self.typeofLLegIK.addItems(["None", "Rotate Plane IK"])

        self.typeofRLegIK = QtWidgets.QComboBox()
        self.typeofRLegIK.addItems(["None", "Rotate Plane IK"])

        self.autostretch = QtWidgets.QComboBox()
        self.autostretch.addItems(["No", "Yes"])

    def createLayout(self):
        form_layout_1 = QtWidgets.QFormLayout()
        form_layout_1.addRow("Enter No. Of Spine:", self.createSpineText)
        form_layout_1.addRow("Enter No. Of Finger:", self.countFingers)

        form_layout_2 = QtWidgets.QFormLayout()
        form_layout_2.addRow("Edit Mode", self.editModeCheckBox)

        form_layout_3 = QtWidgets.QFormLayout()
        form_layout_3.addRow("Rig Type", self.typeofRigComboBox)

        form_layout_5 = QtWidgets.QFormLayout()
        form_layout_5.addRow("Left Hand", self.typeofLHandIK)
        form_layout_5.addRow("Right Hand", self.typeofRHandIK)

        form_layout_6 = QtWidgets.QFormLayout()
        form_layout_6.addRow("Left Leg", self.typeofLLegIK)
        form_layout_6.addRow("Right Leg", self.typeofRLegIK)

        form_layout_7 = QtWidgets.QFormLayout()
        form_layout_7.addRow("Include Auto-Stretchy", self.autostretch)

        horizonLayout = QtWidgets.QHBoxLayout()
        horizonLayout.addWidget(self.createLocatorBut)
        horizonLayout.addWidget(self.deleteLocatorBut)
        horizonLayout.addWidget(self.mirrorLocatorBut)
        horizonLayout.addLayout(form_layout_2)

        jnt_HorizonLayout = QtWidgets.QHBoxLayout()
        jnt_HorizonLayout.addWidget(self.createJointBut)
        jnt_HorizonLayout.addWidget(self.insertJointBut)
        jnt_HorizonLayout.addWidget(self.deleteJointBut)

        jntOrient_HorizonLayout = QtWidgets.QHBoxLayout()
        jntOrient_HorizonLayout.addWidget(self.jointOrientBut)
        jntOrient_HorizonLayout.addWidget(self.typeofJointOrient)

        ik_HorizonLayout = QtWidgets.QHBoxLayout()
        ik_HorizonLayout.addLayout(form_layout_5)
        ik_HorizonLayout.addLayout(form_layout_6)

        rig_HorizonLayout = QtWidgets.QHBoxLayout()
        rig_HorizonLayout.addWidget(self.rigCharBut)
        rig_HorizonLayout.addWidget(self.delRigBut)

        #horizonLayout.addWidget(self.mirrorCheckBox)

        #horizonLayout.addWidget(self.editModeCheckBox)
        #subLayoutH.addStretch()

        mainLayoutV = QtWidgets.QVBoxLayout(self)
        mainLayoutV.addLayout(form_layout_3)
        mainLayoutV.addLayout(horizonLayout)
        mainLayoutV.addLayout(form_layout_1)
        mainLayoutV.addLayout(jnt_HorizonLayout)
        mainLayoutV.addLayout(jntOrient_HorizonLayout)
        mainLayoutV.addLayout(ik_HorizonLayout)
        mainLayoutV.addWidget(self.boundingBoxBut)
        mainLayoutV.addLayout(form_layout_7)
        mainLayoutV.addLayout(rig_HorizonLayout)

    def createUIConnection(self):
        self.createLocatorBut.clicked.connect(self.createLocator)
        self.deleteLocatorBut.clicked.connect(self.deleteLocator)
        self.mirrorLocatorBut.clicked.connect(self.mirrorLocator)
        self.createJointBut.clicked.connect(self.createJoints)
        self.insertJointBut.clicked.connect(self.insertJoint)
        self.deleteJointBut.clicked.connect(self.deleteJoints)
        self.jointOrientBut.clicked.connect(self.setJointOrientation)
        self.editModeCheckBox.toggled.connect(self.editMode)
        self.typeofLHandIK.activated.connect(self.createLHandIK)
        self.typeofRHandIK.activated.connect(self.createRHandIK)
        self.typeofLLegIK.activated.connect(self.createLlegIk)
        self.typeofRLegIK.activated.connect(self.createRlegIk)
        self.boundingBoxBut.clicked.connect(self.createBoundingBox)
        self.rigCharBut.clicked.connect(self.rigChar)
        self.delRigBut.clicked.connect(self.deleteRig)

    def createLocator(self):
        loc_nam = "loc_grp"
        obj_list = om2.MSelectionList()

        try:
            obj_list.add(loc_nam)
        except:
            loc_grp = om2.MFnDagNode()
            loc_obj = loc_grp.create("transform", "loc_Grp")
            self.loc_root_tn = loc_grp.create("transform", "loc_root", loc_obj)
            loc_root_mn = loc_grp.create("locator", "locatorShape1", self.loc_root_tn)

            self.loc_transform = om2.MFnTransform(self.loc_root_tn)

            loc_plug_ty = self.loc_transform.findPlug("translateY", False)
            loc_plug_ty.setInt(1)
        else:
            print("loc_grp already exist")

        self.createSpine()

    def createSpine(self):
        spineloc_grp = om2.MFnDagNode()

        for i in range(0, int(self.createSpineText.text())):
            if i == 0:
                self.spine_tn = spineloc_grp.create("transform", "loc_spine_"+str(i), self.loc_root_tn)
                spine_ln = spineloc_grp.create("locator", "locatorShape1", self.spine_tn)
            else:
                self.spine_tn = spineloc_grp.create("transform", "loc_spine_"+str(i), self.spine_tn)
                spine_ln = spineloc_grp.create("locator", "locatorShape1", self.spine_tn)

            self.spineloc_transform = om2.MFnTransform(self.spine_tn)
            spineloc_plug_ty = self.spineloc_transform.findPlug("translateY", False)
            spineloc_plug_ty.setDouble(2.25)

        self.createShoulder(1)
        self.createShoulder(-1)
        self.createArms(1)
        self.createArms(-1)
        self.createHead()
        self.createLegs(1)
        self.createLegs(-1)

        transform = ["translate", "rotate", "scale"]
        axis = ["X", "Y", "Z"]
        nodes = cmds.ls("loc_*", transforms=True)

        for t in transform:
            for ax in axis:
                for n in nodes:
                    cmds.setAttr(n+'.'+t+ax, lock=True)

    def createHead(self):
        headloc_grp = om2.MFnDagNode()

        neckloc_tn = headloc_grp.create("transform", "loc_neck", self.spine_tn)
        neckloc_ln = headloc_grp.create("locator", "locatorShape1", neckloc_tn)

        self.neckloc_transform_t = om2.MFnTransform(neckloc_tn)

        # neckloc_plug_s = self.neckloc_transform_t.findPlug("scale", False)
        # if neckloc_plug_s.isCompound:
        #     for i in range(neckloc_plug_s.numChildren()):
        #         child_plug = neckloc_plug_s.child(i)
        #         attr_value = child_plug.setDouble(0.5)

        neckloc_plug_ty = self.neckloc_transform_t.findPlug("translateY", False)
        neckloc_plug_ty.setDouble((((int(self.createSpineText.text())-1)*0.5)+1.25))

        headlowloc_tn = headloc_grp.create("transform", "loc_headlower", neckloc_tn)
        headlowloc_ln = headloc_grp.create("locator", "locatorShape1", headlowloc_tn)

        self.headlowloc_transform_t = om2.MFnTransform(headlowloc_tn)

        headlowloc_plug_ty = self.headlowloc_transform_t.findPlug("translateY", False)
        headlowloc_plug_ty.setDouble((((int(self.createSpineText.text())-1)*0.5)+0.75))

        headendloc_tn = headloc_grp.create("transform", "loc_headend", headlowloc_tn)
        headendloc_ln = headloc_grp.create("locator", "locatorShape1", headendloc_tn)

        self.headendloc_transform_t = om2.MFnTransform(headendloc_tn)
        headendloc_plug_ty = self.headendloc_transform_t.findPlug("translateY", False)
        headendloc_plug_ty.setDouble((((int(self.createSpineText.text())-1)*0.5)+3))

    def createShoulder(self, side):
        loc_shoulder = ["loc_L_shoulder", "loc_R_shoulder"]
        obj_list = om2.MSelectionList()
        shoulderloc_grp = om2.MFnDagNode()

        if side == 1:
            try:
                obj_list.add(loc_shoulder[0])
            except:
                self.l_shoulder_tn = shoulderloc_grp.create("transform", "loc_L_shoulder", self.spine_tn)
                l_shoulder_ln = shoulderloc_grp.create("locator", "locatorShape1", self.l_shoulder_tn)

                self.lshoulder_transform = om2.MFnTransform(self.l_shoulder_tn)

                # lshoulder_plug_s = self.lshoulder_transform.findPlug("scale", False)
                # if lshoulder_plug_s.isCompound:
                #     for i in range(lshoulder_plug_s.numChildren()):
                #         child_plug = lshoulder_plug_s.child(i)
                #         attr_value = child_plug.setDouble(0.5)

                lshoulder_plug_t = self.lshoulder_transform.translation(om2.MSpace.kTransform)
                lshoulder_plug_t[0], lshoulder_plug_t[1] = 2.5, ((int(self.createSpineText.text())-1)*0.5)+0.50
                self.lshoulder_transform.setTranslation(lshoulder_plug_t, om2.MSpace.kTransform)


        if side == -1:
            try:
                obj_list.add(loc_shoulder[1])
            except:
                self.r_shoulder_tn = shoulderloc_grp.create("transform", "loc_R_shoulder", self.spine_tn)
                r_shoulder_ln = shoulderloc_grp.create("locator", "locatorShape1", self.r_shoulder_tn)

                self.rshoulder_transform = om2.MFnTransform(self.r_shoulder_tn)

                # rshoulder_plug_s = self.rshoulder_transform.findPlug("scale", False)
                # if rshoulder_plug_s.isCompound:
                #     for i in range(rshoulder_plug_s.numChildren()):
                #         child_plug = rshoulder_plug_s.child(i)
                #         attr_value = child_plug.setDouble(0.5)

                rshoulder_plug_t = self.rshoulder_transform.translation(om2.MSpace.kTransform)
                rshoulder_plug_t[0], rshoulder_plug_t[1] = -2.5, ((int(self.createSpineText.text())-1)*0.5)+0.50
                self.rshoulder_transform.setTranslation(rshoulder_plug_t, om2.MSpace.kTransform)

    def createArms(self, side):
        loc_arm = ["loc_L_upperarm", "loc_R_upperarm"]
        obj_list = om2.MSelectionList()
        armloc_grp = om2.MFnDagNode()

        if side == 1:
            try:
                obj_list.add(loc_arm[0])
                print("loc_Larm already exist")
            except:
                up_Larm_tn = armloc_grp.create("transform", "loc_L_upperarm", self.l_shoulder_tn)
                up_Larm_ln = armloc_grp.create("locator", "locatorShape1", up_Larm_tn)

                self.larmloc_transform = om2.MFnTransform(up_Larm_tn)
                larmloc_t = self.larmloc_transform.translation(om2.MSpace.kTransform)
                larmloc_t[0], larmloc_t[1] = 4.5, -(((int(self.createSpineText.text())-1)*0.5)+2)
                self.larmloc_transform.setTranslation(larmloc_t, om2.MSpace.kTransform)

                l_elbow_tn = armloc_grp.create("transform", "loc_L_elbow", up_Larm_tn)
                l_elbow_ln = armloc_grp.create("locator", "locatorShape1", l_elbow_tn)

                self.lelbowloc_transform = om2.MFnTransform(l_elbow_tn)
                lelbowloc_t = self.lelbowloc_transform.translation(om2.MSpace.kTransform)
                lelbowloc_t[0], lelbowloc_t[1] = 4.35, -(((int(self.createSpineText.text())-1)*0.5)+5.25)
                self.lelbowloc_transform.setTranslation(lelbowloc_t, om2.MSpace.kTransform)

                self.l_wrist_tn = armloc_grp.create("transform", "loc_L_wrist", l_elbow_tn)
                l_wrist_ln = armloc_grp.create("locator", "locatorShape1", self.l_wrist_tn)

                self.lwristloc_transform = om2.MFnTransform(self.l_wrist_tn)
                lwristloc_t = self.lwristloc_transform.translation(om2.MSpace.kTransform)
                lwristloc_t[0], lwristloc_t[1] = 6.35, -(((int(self.createSpineText.text())-1)*0.5)+6.25)
                self.lwristloc_transform.setTranslation(lwristloc_t, om2.MSpace.kTransform)

                self.createHands(1)

        if side == -1:
            try:
                obj_list.add(loc_arm[1])
                print("loc_Rarm already exist")
            except:
                up_Rarm_tn = armloc_grp.create("transform", "loc_R_upperarm", self.r_shoulder_tn)
                up_Rarm_ln = armloc_grp.create("locator", "locatorShape1", up_Rarm_tn)

                self.rarmloc_transform = om2.MFnTransform(up_Rarm_tn)
                rarmloc_t = self.rarmloc_transform.translation(om2.MSpace.kTransform)
                rarmloc_t[0], rarmloc_t[1] = -4.5, -(((int(self.createSpineText.text())-1)*0.5)+2)
                self.rarmloc_transform.setTranslation(rarmloc_t, om2.MSpace.kTransform)

                r_elbow_tn = armloc_grp.create("transform", "loc_R_elbow", up_Rarm_tn)
                r_elbow_ln = armloc_grp.create("locator", "locatorShape1", r_elbow_tn)

                self.relbowloc_transform = om2.MFnTransform(r_elbow_tn)
                relbowloc_t = self.relbowloc_transform.translation(om2.MSpace.kTransform)
                relbowloc_t[0], relbowloc_t[1] = -4.35, -(((int(self.createSpineText.text())-1)*0.5)+5.25)
                self.relbowloc_transform.setTranslation(relbowloc_t, om2.MSpace.kTransform)

                self.r_wrist_tn = armloc_grp.create("transform", "loc_R_wrist", r_elbow_tn)
                r_wrist_ln = armloc_grp.create("locator", "locatorShape1", self.r_wrist_tn)

                self.rwristloc_transform = om2.MFnTransform(self.r_wrist_tn)
                rwristloc_t = self.rwristloc_transform.translation(om2.MSpace.kTransform)
                rwristloc_t[0], rwristloc_t[1] = -6.35, -(((int(self.createSpineText.text())-1)*0.5)+6.25)
                self.rwristloc_transform.setTranslation(rwristloc_t, om2.MSpace.kTransform)

                self.createHands(-1)

    def createHands(self, side):
        loc_hand = ["loc_L_hand_grp", "loc_R_hand_grp"]
        obj_list = om2.MSelectionList()
        handloc_grp = om2.MFnDagNode()

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
        fingerloc_grp = om2.MFnDagNode()

        for i in range(0,4):
            if side == 1:
                if i == 0:
                    self.loc_lfinger_tn = fingerloc_grp.create("transform", "loc_L_finger_"+str(count)+"_"+str(i), self.l_hand_tn)
                    loc_lfinger_ln = fingerloc_grp.create("locator", "locatorShape1", self.loc_lfinger_tn)

                    l_finger_transform_t = om2.MFnTransform(self.loc_lfinger_tn)

                    lfingerloc_t = l_finger_transform_t.translation(om2.MSpace.kTransform)
                    lfingerloc_t[0], lfingerloc_t[1], lfingerloc_t[2] = 1, -2, count*1
                    l_finger_transform_t.setTranslation(lfingerloc_t, om2.MSpace.kTransform)

                    # l_finger_plug_s = l_finger_transform_t.findPlug("scale", False)

                    # if l_finger_plug_s.isCompound:
                    #     for i in range(l_finger_plug_s.numChildren()):
                    #         child_plug = l_finger_plug_s.child(i)
                    #         attr_value = child_plug.setDouble(0.5)

                else:
                    self.loc_lfinger_tn = fingerloc_grp.create("transform", "loc_L_finger_"+str(count)+"_"+str(i), self.loc_lfinger_tn)
                    loc_lfinger_ln = fingerloc_grp.create("locator", "locatorShape1", self.loc_lfinger_tn)

                    l_finger_transform_t = om2.MFnTransform(self.loc_lfinger_tn)

                    lfingerloc_t = l_finger_transform_t.translation(om2.MSpace.kTransform)
                    lfingerloc_t[0], lfingerloc_t[1] = 1, -1
                    l_finger_transform_t.setTranslation(lfingerloc_t, om2.MSpace.kTransform)

            if side == -1:
                if i == 0:
                    self.loc_rfinger_tn = fingerloc_grp.create("transform", "loc_R_finger_"+str(count)+"_"+str(i), self.r_hand_tn)
                    loc_rfinger_ln = fingerloc_grp.create("locator", "locatorShape1", self.loc_rfinger_tn)

                    r_finger_transform_t = om2.MFnTransform(self.loc_rfinger_tn)

                    r_finger_plug_t = r_finger_transform_t.translation(om2.MSpace.kTransform)
                    r_finger_plug_t[0], r_finger_plug_t[1], r_finger_plug_t[2] = -1, -2, count*1
                    r_finger_transform_t.setTranslation(r_finger_plug_t, om2.MSpace.kTransform)

                    # r_finger_plug_s = r_finger_transform_t.findPlug("scale", False)

                    # if r_finger_plug_s.isCompound:
                    #     for i in range(r_finger_plug_s.numChildren()):
                    #         child_plug = r_finger_plug_s.child(i)
                    #         attr_value = child_plug.setDouble(0.5)

                else:
                    self.loc_rfinger_tn = fingerloc_grp.create("transform", "loc_R_finger_"+str(count)+"_"+str(i), self.loc_rfinger_tn)
                    loc_rfinger_ln = fingerloc_grp.create("locator", "locatorShape1", self.loc_rfinger_tn)

                    r_finger_transform_t = om2.MFnTransform(self.loc_rfinger_tn)
                    r_finger_plug_t = r_finger_transform_t.translation(om2.MSpace.kTransform)
                    r_finger_plug_t[0], r_finger_plug_t[1] = -1, -1
                    r_finger_transform_t.setTranslation(r_finger_plug_t, om2.MSpace.kTransform)

    def createLegs(self, side):
        loc_leg = ["loc_L_upperleg", "loc_R_upperleg"]
        obj_list = om2.MSelectionList()
        legloc_grp = om2.MFnDagNode()

        if side == 1:
            try:
                obj_list.add(loc_leg[0])
                print("loc_L_leg already exist")
            except:
                l_upleg_tn = legloc_grp.create("transform", "loc_L_upperleg", self.loc_root_tn )
                l_upleg_ln = legloc_grp.create("locator", "locatorShape1", l_upleg_tn)

                self.l_leg_transform_t = om2.MFnTransform(l_upleg_tn)
                l_leg_transform = self.l_leg_transform_t.translation(om2.MSpace.kTransform)
                l_leg_transform[0], l_leg_transform[1] = 2.35, -(((int(self.createSpineText.text()))*0.5)+1)
                self.l_leg_transform_t.setTranslation(l_leg_transform, om2.MSpace.kTransform)

                # l_leg_transform_s = om2.MFnTransform(l_upleg_tn)
                # l_leg_plug_s = l_leg_transform_s.findPlug("scale", False)

                # if l_leg_plug_s.isCompound:
                #     for i in range(l_leg_plug_s.numChildren()):
                #         child_plug = l_leg_plug_s.child(i)
                #         attr_value = child_plug.setDouble(0.7)

                l_knee_tn = legloc_grp.create("transform", "loc_L_knee", l_upleg_tn)
                l_knee_ln = legloc_grp.create("locator", "locatorShape1", l_knee_tn)

                self.l_knee_transform_t = om2.MFnTransform(l_knee_tn)
                l_knee_transform_t = self.l_knee_transform_t.translation(om2.MSpace.kTransform)
                l_knee_transform_t[1] = -((int(self.createSpineText.text())*2.5))
                self.l_knee_transform_t.setTranslation(l_knee_transform_t, om2.MSpace.kTransform)

                l_football_tn = legloc_grp.create("transform", "loc_L_football", l_knee_tn)
                l_football_ln = legloc_grp.create("locator", "locatorShape1", l_football_tn)

                self.l_football_transform_t = om2.MFnTransform(l_football_tn)
                l_football_plug_ty = self.l_football_transform_t.findPlug("translateY", False)
                l_football_plug_ty.setDouble(-((int(self.createSpineText.text())*3.5)))

                l_foot_tn = legloc_grp.create("transform", "loc_L_foot", l_football_tn)
                l_football_ln = legloc_grp.create("locator", "locatorShape1", l_foot_tn)

                self.l_foot_transform_t = om2.MFnTransform(l_foot_tn)
                l_foot_transform = self.l_foot_transform_t.translation(om2.MSpace.kTransform)
                l_foot_transform[1], l_foot_transform[2] = -(int(self.createSpineText.text())*0.5), (int(self.createSpineText.text())*0.7)
                self.l_foot_transform_t.setTranslation(l_foot_transform, om2.MSpace.kTransform)

                l_toe_tn = legloc_grp.create("transform", "loc_L_toe", l_foot_tn)
                l_toe_ln = legloc_grp.create("locator", "locatorShape1", l_toe_tn)

                self.l_toe_transform_t = om2.MFnTransform(l_toe_tn)
                l_toe_plug_tz = self.l_toe_transform_t.findPlug("translateZ", False)
                l_toe_plug_tz.setDouble(((int(self.createSpineText.text())*0.7)))

        if side == -1:
            try:
                obj_list.add(loc_leg[1])
                print("loc_L_leg already exist")
            except:
                r_upleg_tn = legloc_grp.create("transform", "loc_R_upperleg", self.loc_root_tn)
                r_upleg_ln = legloc_grp.create("locator", "locatorShape1", r_upleg_tn)

                self.r_leg_transform_t = om2.MFnTransform(r_upleg_tn)
                r_leg_plug_tx = self.r_leg_transform_t.findPlug("translateX", False)
                r_leg_plug_ty = self.r_leg_transform_t.findPlug("translateY", False)
                r_leg_plug_tx.setDouble(-2.35)
                r_leg_plug_ty.setDouble(-(((int(self.createSpineText.text()))*0.5)+1))

                # r_leg_transform_s = om2.MFnTransform(r_upleg_tn)
                # r_leg_plug_s = r_leg_transform_s.findPlug("scale", False)

                # if r_leg_plug_s.isCompound:
                #     for i in range(r_leg_plug_s.numChildren()):
                #         child_plug = r_leg_plug_s.child(i)
                #         attr_value = child_plug.setDouble(1)

                r_knee_tn = legloc_grp.create("transform", "loc_R_knee", r_upleg_tn)
                r_knee_ln = legloc_grp.create("locator", "locatorShape1", r_knee_tn)

                self.r_knee_transform_t = om2.MFnTransform(r_knee_tn)
                r_knee_plug_ty = self.r_knee_transform_t.findPlug("translateY", False)
                r_knee_plug_ty.setDouble(-((int(self.createSpineText.text())*2.5)))

                r_football_tn = legloc_grp.create("transform", "loc_R_football", r_knee_tn)
                r_football_ln = legloc_grp.create("locator", "locatorShape1", r_football_tn)

                self.r_football_transform_t = om2.MFnTransform(r_football_tn)
                r_football_plug_ty = self.r_football_transform_t.findPlug("translateY", False)
                r_football_plug_ty.setDouble(-((int(self.createSpineText.text())*3.5)))

                r_foot_tn = legloc_grp.create("transform", "loc_R_foot", r_football_tn)
                r_football_ln = legloc_grp.create("locator", "locatorShape1", r_foot_tn)

                self.r_foot_transform_t = om2.MFnTransform(r_foot_tn)
                r_foot_transform = self.r_foot_transform_t.translation(om2.MSpace.kTransform)
                r_foot_transform[1], r_foot_transform[2] = -(int(self.createSpineText.text())*0.5), (int(self.createSpineText.text())*0.7)
                self.r_foot_transform_t.setTranslation(r_foot_transform, om2.MSpace.kTransform)

                r_toe_tn = legloc_grp.create("transform", "loc_R_toe", r_foot_tn)
                r_toe_ln = legloc_grp.create("locator", "locatorShape1", r_toe_tn)

                self.r_toe_transform_t = om2.MFnTransform(r_toe_tn)
                r_toe_plug_tz = self.r_toe_transform_t.findPlug("translateZ", False)
                r_toe_plug_tz.setDouble(((int(self.createSpineText.text())*0.7)))

    def mirrorLocator(self):
        allLeftLocator = "loc_L_*"
        leftloc_ls = om2.MSelectionList()
        leftloc_ls.add(allLeftLocator)

        allRightLocator = "loc_R_*"
        rightloc_ls = om2.MSelectionList()
        rightloc_ls.add(allRightLocator)

        for index in range(leftloc_ls.length()):
            obj_l_loc = leftloc_ls.getDependNode(index)
            l_obj_tn = om2.MFnTransform(obj_l_loc)

            obj_r_loc = rightloc_ls.getDependNode(index)
            r_obj_tn = om2.MFnTransform(obj_r_loc)

            translation = l_obj_tn.translation(om2.MSpace.kTransform)
            rotation = l_obj_tn.rotation(om2.MSpace.kTransform)
            translation[0] = -translation[0]
            rotation[1], rotation[2] = -rotation[1], -rotation[2]
            r_obj_tn.setTranslation(translation, om2.MSpace.kTransform)
            r_obj_tn.setRotation(rotation, om2.MSpace.kTransform)

    def editMode(self):
        loc_lock = self.editModeCheckBox.isChecked()
        transform = ["translate", "rotate", "scale"]
        axis = ["X", "Y", "Z"]
        nodes = cmds.ls("loc_*", transforms=True)

        for t in transform:
            for ax in axis:
                for n in nodes:
                    if loc_lock:
                        cmds.setAttr(n+'.'+t+ax, lock=False)
                    else:
                        cmds.setAttr(n+'.'+t+ax, lock=True)

    def deleteLocator(self):
        node = cmds.ls("loc_*")
        cmds.delete(node)

    def createJoints(self):
        self.jnt_grp = "Biped_jnt_grp"
        obj_lst = om2.MSelectionList()
        spinejnt_grp = om2.MFnDagNode()

        root_loc = "loc_root"
        root_loc_ls = om2.MSelectionList()
        root_loc_ls.add(root_loc)
        root_loc_obj = root_loc_ls.getDependNode(0)
        root_loc_transform = om2.MFnTransform(root_loc_obj)
        self.loc_root_transform = root_loc_transform.transformation()

        try:
            obj_lst.add(self.jnt_grp)
            print("Rig_grp already exist")
        except:
            self.jnt_grp = spinejnt_grp.create("transform", "Biped_jnt_grp")
            self.donttouchjnt_grp = spinejnt_grp.create("transform", "DoNotTouch", self.jnt_grp)
            self.splineik_grp = spinejnt_grp.create("transform", "SplineIk_grp", self.donttouchjnt_grp)
            self.jnt_root_tn = spinejnt_grp.create("joint", "Hip", self.jnt_grp)
            self.jnt_ikroot_tn = spinejnt_grp.create("joint", "IkHip", self.splineik_grp)
            self.jnt_ikrootcv_tn = spinejnt_grp.create("joint", "IkCvHip", self.donttouchjnt_grp)

            self.jnt_root_transform = om2.MFnTransform(self.jnt_root_tn)
            self.jnt_root_transform.setTransformation(self.loc_root_transform)

            self.jnt_ikroot_transform = om2.MFnTransform(self.jnt_ikroot_tn)
            self.jnt_ikroot_transform.setTransformation(self.loc_root_transform)

            self.jnt_ikrootcv_transform = om2.MFnTransform(self.jnt_ikrootcv_tn)
            self.jnt_ikrootcv_transform.setTransformation(self.loc_root_transform)

            spine_loc = "loc_spine_*"
            spine_loc_ls = om2.MSelectionList()
            spine_loc_ls.add(spine_loc)

            for index in range(spine_loc_ls.length()):
                spine_loc_obj = spine_loc_ls.getDependNode(index)
                spine_loc_tn = om2.MFnTransform(spine_loc_obj)
                loc_spine_transform = spine_loc_tn.transformation()
                loc_spinesec_transform_t = spine_loc_tn.translation(om2.MSpace.kTransform)

                spine_path_n = om2.MDagPath()
                spine_path = spine_path_n.getAPathTo(spine_loc_obj)
                spine_loc_path_tn = om2.MFnTransform(spine_path)
                spine_t = spine_loc_path_tn.translation(om2.MSpace.kWorld)

                if index == 0:
                    self.spine_jnt = spinejnt_grp.create("joint", "Spine"+str(index), self.jnt_root_tn)
                    self.ikspine_jnt = spinejnt_grp.create("joint", "IkSpine"+str(index), self.jnt_ikroot_tn)
                    self.ikspinesec_jnt = spinejnt_grp.create("joint", "IkSpine"+str(index+1), self.ikspine_jnt)
                else:
                    self.spine_jnt = spinejnt_grp.create("joint", "Spine"+str(index), self.spine_jnt)
                    self.ikspine_jnt = spinejnt_grp.create("joint", "IkSpine"+str(index*2), self.ikspinesec_jnt)
                    self.ikspinesec_jnt = spinejnt_grp.create("joint", "IkSpine"+str((index*2)+1), self.ikspine_jnt)

                    if index == spine_loc_ls.length()-1:
                        self.ikspinecv_jnt = spinejnt_grp.create("joint", "IkCvSpine", self.donttouchjnt_grp)

                        jnt_ikspinecv_tranform = om2.MFnTransform(self.ikspinecv_jnt)
                        jnt_ikspinecv_tranform.setTranslation(spine_t, om2.MSpace.kTransform)

                jnt_spine_tranform = om2.MFnTransform(self.spine_jnt)
                jnt_spine_tranform.setTransformation(loc_spine_transform)

                jnt_ikspine_tranform = om2.MFnTransform(self.ikspine_jnt)
                jnt_ikspine_tranform_t = jnt_ikspine_tranform.translation(om2.MSpace.kTransform)
                jnt_ikspine_tranform_t[0], jnt_ikspine_tranform_t[1], jnt_ikspine_tranform_t[2] = loc_spinesec_transform_t[0]/2, loc_spinesec_transform_t[1]/2, loc_spinesec_transform_t[2]/2
                jnt_ikspine_tranform.setTranslation(jnt_ikspine_tranform_t, om2.MSpace.kTransform)

                jnt_ikspinesec_tranform = om2.MFnTransform(self.ikspinesec_jnt)
                jnt_ikspinesec_tranform_t = jnt_ikspinesec_tranform.translation(om2.MSpace.kTransform)
                jnt_ikspinesec_tranform_t[0], jnt_ikspinesec_tranform_t[1], jnt_ikspinesec_tranform_t[2] = loc_spinesec_transform_t[0]/2, loc_spinesec_transform_t[1]/2, loc_spinesec_transform_t[2]/2
                jnt_ikspinesec_tranform.setTranslation(jnt_ikspinesec_tranform_t, om2.MSpace.kTransform)

            self.createHeadJoints()
            self.createShoulderJoints(1)
            self.createShoulderJoints(-1)
            self.createArmJoints(1)
            self.createArmJoints(-1)
            self.createLegJoints(1)
            self.createLegJoints(-1)

            lfinger_loc = "loc_L_finger_*"
            self.lfinger_lst = om2.MSelectionList()
            self.lfinger_lst.add(lfinger_loc)

            rfinger_loc = "loc_R_finger_*"
            rfinger_lst = om2.MSelectionList()
            rfinger_lst.add(rfinger_loc)

            self.createFingerJoints()

    def createHeadJoints(self):
        headjnt_grp = om2.MFnDagNode()

        head_loc = ["loc_neck", "loc_headlower", "loc_headend"]
        head_loc_ls = om2.MSelectionList()
        head_loc_ls.add(head_loc[0])
        neck_loc_obj = head_loc_ls.getDependNode(0)
        neck_loc_transform = om2.MFnTransform(neck_loc_obj)
        loc_neck_transform = neck_loc_transform.transformation()

        neck_path_n = om2.MDagPath()
        neck_path = neck_path_n.getAPathTo(neck_loc_obj)
        neck_loc_path_tn = om2.MFnTransform(neck_path)
        neck_t = neck_loc_path_tn.translation(om2.MSpace.kWorld)

        head_loc_ls.add(head_loc[1])
        headlower_loc_obj = head_loc_ls.getDependNode(1)
        headlower_loc_transform = om2.MFnTransform(headlower_loc_obj)
        loc_headlower_transform = headlower_loc_transform.transformation()
        loc_headlower_t = headlower_loc_transform.translation(om2.MSpace.kTransform)

        head_path_n = om2.MDagPath()
        head_path = head_path_n.getAPathTo(headlower_loc_obj)
        head_loc_path_tn = om2.MFnTransform(head_path)
        head_t = head_loc_path_tn.translation(om2.MSpace.kWorld)

        head_loc_ls.add(head_loc[2])
        headend_loc_obj = head_loc_ls.getDependNode(2)
        headend_loc_transform = om2.MFnTransform(headend_loc_obj)
        loc_headend_transform = headend_loc_transform.transformation()

        jnt_neck = headjnt_grp.create("joint", "Neck", self.spine_jnt)
        jnt_ikneck0 = headjnt_grp.create("joint", "IkNeck0", self.splineik_grp)
        jnt_ikcvneck = headjnt_grp.create("joint", "IkCvNeck", self.donttouchjnt_grp)

        jnt_neck_transform = om2.MFnTransform(jnt_neck)
        jnt_neck_transform.setTransformation(loc_neck_transform)

        jnt_ikneck0_transform = om2.MFnTransform(jnt_ikneck0)
        jnt_ikneck0_transform.setTranslation(neck_t, om2.MSpace.kTransform)

        jnt_ikcvneck_transform = om2.MFnTransform(jnt_ikcvneck)
        jnt_ikcvneck_transform.setTranslation(neck_t, om2.MSpace.kTransform)

        jnt_ikneck1 = headjnt_grp.create("joint", "IkNeck1", jnt_ikneck0)

        jnt_ikneck1_tranform = om2.MFnTransform(jnt_ikneck1)
        jnt_ikneck1_tranform_t = jnt_ikneck1_tranform.translation(om2.MSpace.kTransform)
        jnt_ikneck1_tranform_t[0], jnt_ikneck1_tranform_t[1], jnt_ikneck1_tranform_t[2] = loc_headlower_t[0]/3, loc_headlower_t[1]/3, loc_headlower_t[2]/3
        jnt_ikneck1_tranform.setTranslation(jnt_ikneck1_tranform_t, om2.MSpace.kTransform)

        jnt_ikneck2 = headjnt_grp.create("joint", "IkNeck2", jnt_ikneck1)

        jnt_ikneck2_tranform = om2.MFnTransform(jnt_ikneck2)
        jnt_ikneck2_tranform_t = jnt_ikneck2_tranform.translation(om2.MSpace.kTransform)
        jnt_ikneck2_tranform_t[0], jnt_ikneck2_tranform_t[1], jnt_ikneck2_tranform_t[2] = loc_headlower_t[0]/3, loc_headlower_t[1]/3, loc_headlower_t[2]/3
        jnt_ikneck2_tranform.setTranslation(jnt_ikneck2_tranform_t, om2.MSpace.kTransform)

        jnt_ikneck3 = headjnt_grp.create("joint", "IkNeck3", jnt_ikneck2)

        jnt_ikneck3_tranform = om2.MFnTransform(jnt_ikneck3)
        jnt_ikneck3_tranform_t = jnt_ikneck3_tranform.translation(om2.MSpace.kTransform)
        jnt_ikneck3_tranform_t[0], jnt_ikneck3_tranform_t[1], jnt_ikneck3_tranform_t[2] = loc_headlower_t[0]/3, loc_headlower_t[1]/3, loc_headlower_t[2]/3
        jnt_ikneck3_tranform.setTranslation(jnt_ikneck3_tranform_t, om2.MSpace.kTransform)

        jnt_head = headjnt_grp.create("joint", "Head", jnt_neck)
        jnt_ikhead = headjnt_grp.create("joint", "IkCvHead", self.donttouchjnt_grp)

        jnt_head_transform = om2.MFnTransform(jnt_head)
        jnt_head_transform.setTransformation(loc_headlower_transform)

        jnt_ikhead_transform = om2.MFnTransform(jnt_ikhead)
        jnt_ikhead_transform.setTranslation(head_t, om2.MSpace.kTransform)

        jnt_headend = headjnt_grp.create("joint", "HeadTopEnd", jnt_head)

        jnt_headend_transform = om2.MFnTransform(jnt_headend)
        jnt_headend_transform.setTransformation(loc_headend_transform)

    def createShoulderJoints(self, side):
        shoulderjnt_grp = om2.MFnDagNode()

        shoulder_loc = ["loc_*_shoulder"]
        shoulder_loc_ls = om2.MSelectionList()
        shoulder_loc_ls.add(shoulder_loc[0])
        lshoulder_loc_obj = shoulder_loc_ls.getDependNode(0)
        lshoulder_loc_transform = om2.MFnTransform(lshoulder_loc_obj)
        loc_lshoulder_transform = lshoulder_loc_transform.transformation()

        rshoulder_loc_obj = shoulder_loc_ls.getDependNode(1)
        rshoulder_loc_transform = om2.MFnTransform(rshoulder_loc_obj)
        loc_rshoulder_transform = rshoulder_loc_transform.transformation()

        if side == 1:
            self.jnt_lshoulder = shoulderjnt_grp.create("joint", "LeftShoulder", self.spine_jnt)

            jnt_lshoulder_transform = om2.MFnTransform(self.jnt_lshoulder)
            jnt_lshoulder_transform.setTransformation(loc_lshoulder_transform)

        if side == -1:
            self.jnt_rshoulder = shoulderjnt_grp.create("joint", "RightShoulder", self.spine_jnt)

            jnt_rshoulder_transform = om2.MFnTransform(self.jnt_rshoulder)
            jnt_rshoulder_transform.setTransformation(loc_rshoulder_transform)

    def createArmJoints(self, side):
        armjnt_grp = om2.MFnDagNode()

        hand_loc = ["loc_L_upperarm", "loc_L_elbow", "loc_L_wrist", "loc_R_upperarm", "loc_R_elbow", "loc_R_wrist"]
        hand_loc_ls = om2.MSelectionList()

        if side == 1:
            self.jnt_lupperarm = armjnt_grp.create("joint", "LeftArm", self.jnt_lshoulder)
            self.jnt_fklupperarm = armjnt_grp.create("joint", "FkLeftArm", self.jnt_lshoulder)
            self.jnt_iklupperarm = armjnt_grp.create("joint", "IkLeftArm", self.jnt_lshoulder)

            hand_loc_ls.add(hand_loc[0])
            lupperarm_loc_obj = hand_loc_ls.getDependNode(0)
            lupperarm_loc_transform = om2.MFnTransform(lupperarm_loc_obj)
            loc_lupperarm_transform = lupperarm_loc_transform.transformation()

            jnt_lupperarm_transform = om2.MFnTransform(self.jnt_lupperarm)
            jnt_lupperarm_transform.setTransformation(loc_lupperarm_transform)

            jnt_fklupperarm_transform = om2.MFnTransform(self.jnt_fklupperarm)
            jnt_fklupperarm_transform.setTransformation(loc_lupperarm_transform)

            jnt_iklupperarm_transform = om2.MFnTransform(self.jnt_iklupperarm)
            jnt_iklupperarm_transform.setTransformation(loc_lupperarm_transform)

            jnt_lelbow = armjnt_grp.create("joint", "LeftForeArm", self.jnt_lupperarm)
            jnt_fklelbow = armjnt_grp.create("joint", "FkLeftForeArm", self.jnt_fklupperarm)
            jnt_iklelbow = armjnt_grp.create("joint", "IkLeftForeArm", self.jnt_iklupperarm)

            hand_loc_ls.add(hand_loc[1])
            larm_loc_obj = hand_loc_ls.getDependNode(1)
            larm_loc_transform = om2.MFnTransform(larm_loc_obj)
            loc_lelbow_transform = larm_loc_transform.transformation()

            jnt_lelbow_transform = om2.MFnTransform(jnt_lelbow)
            jnt_lelbow_transform.setTransformation(loc_lelbow_transform)

            jnt_fklelbow_transform = om2.MFnTransform(jnt_fklelbow)
            jnt_fklelbow_transform.setTransformation(loc_lelbow_transform)

            jnt_iklelbow_transform = om2.MFnTransform(jnt_iklelbow)
            jnt_iklelbow_transform.setTransformation(loc_lelbow_transform)

            self.jnt_lwrist = armjnt_grp.create("joint", "LeftHand", jnt_lelbow)
            self.jnt_fklwrist = armjnt_grp.create("joint", "FkLeftHand", jnt_fklelbow)
            self.jnt_iklwrist = armjnt_grp.create("joint", "IkLeftHand", jnt_iklelbow)

            hand_loc_ls.add(hand_loc[2])
            lelbow_loc_obj = hand_loc_ls.getDependNode(2)
            lelbow_loc_transform = om2.MFnTransform(lelbow_loc_obj)
            loc_lwrist_transform = lelbow_loc_transform.transformation()

            jnt_lwrist_transform = om2.MFnTransform(self.jnt_lwrist)
            jnt_lwrist_transform.setTransformation(loc_lwrist_transform)

            jnt_fklwrist_transform = om2.MFnTransform(self.jnt_fklwrist)
            jnt_fklwrist_transform.setTransformation(loc_lwrist_transform)

            jnt_iklwrist_transform = om2.MFnTransform(self.jnt_iklwrist)
            jnt_iklwrist_transform.setTransformation(loc_lwrist_transform)

        if side == -1:
            self.jnt_rupperarm = armjnt_grp.create("joint", "RightArm", self.jnt_rshoulder)
            self.jnt_fkrupperarm = armjnt_grp.create("joint", "FkRightArm", self.jnt_rshoulder)
            self.jnt_ikrupperarm = armjnt_grp.create("joint", "IkRightArm", self.jnt_rshoulder)

            hand_loc_ls.add(hand_loc[3])
            rupperarm_loc_obj = hand_loc_ls.getDependNode(0)
            rupperarm_loc_transform = om2.MFnTransform(rupperarm_loc_obj)
            loc_rupperarm_transform = rupperarm_loc_transform.transformation()

            jnt_rupperarm_transform = om2.MFnTransform(self.jnt_rupperarm)
            jnt_rupperarm_transform.setTransformation(loc_rupperarm_transform)

            jnt_fkrupperarm_transform = om2.MFnTransform(self.jnt_fkrupperarm)
            jnt_fkrupperarm_transform.setTransformation(loc_rupperarm_transform)

            jnt_ikrupperarm_transform = om2.MFnTransform(self.jnt_ikrupperarm)
            jnt_ikrupperarm_transform.setTransformation(loc_rupperarm_transform)

            jnt_relbow = armjnt_grp.create("joint", "RightForeArm", self.jnt_rupperarm)
            jnt_fkrelbow = armjnt_grp.create("joint", "FkRightForeArm", self.jnt_fkrupperarm)
            jnt_ikrelbow = armjnt_grp.create("joint", "IkRightForeArm", self.jnt_ikrupperarm)

            hand_loc_ls.add(hand_loc[4])
            rarm_loc_obj = hand_loc_ls.getDependNode(1)
            rarm_loc_transform = om2.MFnTransform(rarm_loc_obj)
            loc_relbow_transform = rarm_loc_transform.transformation()

            jnt_relbow_transform = om2.MFnTransform(jnt_relbow)
            jnt_relbow_transform.setTransformation(loc_relbow_transform)

            jnt_fkrelbow_transform = om2.MFnTransform(jnt_fkrelbow)
            jnt_fkrelbow_transform.setTransformation(loc_relbow_transform)

            jnt_ikrelbow_transform = om2.MFnTransform(jnt_ikrelbow)
            jnt_ikrelbow_transform.setTransformation(loc_relbow_transform)

            self.jnt_rwrist = armjnt_grp.create("joint", "RightHand", jnt_relbow)
            self.jnt_fkrwrist = armjnt_grp.create("joint", "FkRightHand", jnt_fkrelbow)
            self.jnt_ikrwrist = armjnt_grp.create("joint", "IkRightHand", jnt_ikrelbow)

            hand_loc_ls.add(hand_loc[5])
            relbow_loc_obj = hand_loc_ls.getDependNode(2)
            relbow_loc_transform = om2.MFnTransform(relbow_loc_obj)
            loc_rwrist_transform = relbow_loc_transform.transformation()

            jnt_rwrist_transform = om2.MFnTransform(self.jnt_rwrist)
            jnt_rwrist_transform.setTransformation(loc_rwrist_transform)

            jnt_fkrwrist_transform = om2.MFnTransform(self.jnt_fkrwrist)
            jnt_fkrwrist_transform.setTransformation(loc_rwrist_transform)

            jnt_ikrwrist_transform = om2.MFnTransform(self.jnt_ikrwrist)
            jnt_ikrwrist_transform.setTransformation(loc_rwrist_transform)

    def createFingerJoints(self):
        for i in range(0, self.lfinger_lst.length()/4):
            self.createFingersJoints(1, i)
            self.createFingersJoints(-1, i)

    def createFingersJoints(self, side, i):
        fingerjnt_grp = om2.MFnDagNode()

        if side == 1:
            if i == 0:
                loc_thumb = "loc_L_finger_0_*"
                sl_lst = om2.MSelectionList()
                sl_lst.add(loc_thumb)

                for index in range(sl_lst.length()):
                    if index == 0:
                        self.jnt_finger = fingerjnt_grp.create("joint", "LeftFingerPinky1", self.jnt_lwrist)
                    else:
                        self.jnt_finger = fingerjnt_grp.create("joint", "LeftFingerPinky"+str(index+1), self.jnt_finger)

                    obj_lthumb_loc = sl_lst.getDependNode(index)
                    lthumbloc_transform = om2.MFnTransform(obj_lthumb_loc)
                    loc_lthumb_transform = lthumbloc_transform.transformation()

                    jnt_thump_transform = om2.MFnTransform(self.jnt_finger)
                    jnt_thump_transform.transformation()
                    jnt_thump_transform.setTransformation(loc_lthumb_transform)

            if i == 1:
                loc_index = "loc_L_finger_1_*"
                sl_lst = om2.MSelectionList()
                sl_lst.add(loc_index)

                for index in range(sl_lst.length()):
                    if index == 0:
                        self.jnt_finger = fingerjnt_grp.create("joint", "LeftFingerRing1", self.jnt_lwrist)
                    else:
                        self.jnt_finger = fingerjnt_grp.create("joint", "LeftFingerRing"+str(index+1), self.jnt_finger)

                    obj_lfinger_loc = sl_lst.getDependNode(index)
                    lindexloc_transform = om2.MFnTransform(obj_lfinger_loc)
                    loc_lindex_transform = lindexloc_transform.transformation()

                    jnt_index_transform = om2.MFnTransform(self.jnt_finger)
                    jnt_index_transform.transformation()
                    jnt_index_transform.setTransformation(loc_lindex_transform)

            if i == 2:
                loc_middle = "loc_L_finger_2_*"
                sl_lst = om2.MSelectionList()
                sl_lst.add(loc_middle)

                for index in range(sl_lst.length()):
                    if index == 0:
                        self.jnt_finger = fingerjnt_grp.create("joint", "LeftFingerMiddle1", self.jnt_lwrist)
                    else:
                        self.jnt_finger = fingerjnt_grp.create("joint", "LeftFingerMiddle"+str(index+1), self.jnt_finger)

                    obj_lfinger_loc = sl_lst.getDependNode(index)
                    lmiddleloc_transform = om2.MFnTransform(obj_lfinger_loc)
                    loc_lindex_transform = lmiddleloc_transform.transformation()

                    jnt_middle_transform = om2.MFnTransform(self.jnt_finger)
                    jnt_middle_transform.transformation()
                    jnt_middle_transform.setTransformation(loc_lindex_transform)

            if i == 3:
                loc_ring = "loc_L_finger_3_*"
                sl_lst = om2.MSelectionList()
                sl_lst.add(loc_ring)

                for index in range(sl_lst.length()):
                    if index == 0:
                        self.jnt_finger = fingerjnt_grp.create("joint", "LeftFingerIndex1", self.jnt_lwrist)
                    else:
                        self.jnt_finger = fingerjnt_grp.create("joint", "LeftFingerIndex"+str(index+1), self.jnt_finger)

                    obj_lfinger_loc = sl_lst.getDependNode(index)
                    lringloc_transform = om2.MFnTransform(obj_lfinger_loc)
                    loc_lring_transform = lringloc_transform.transformation()

                    jnt_ring_transform = om2.MFnTransform(self.jnt_finger)
                    jnt_ring_transform.transformation()
                    jnt_ring_transform.setTransformation(loc_lring_transform)

            if i == 4:
                loc_pinky = "loc_L_finger_4_*"
                sl_lst = om2.MSelectionList()
                sl_lst.add(loc_pinky)

                for index in range(sl_lst.length()):
                    if index == 0:
                        self.jnt_finger = fingerjnt_grp.create("joint", "LeftFingerThumb1", self.jnt_lwrist)
                    else:
                        self.jnt_finger = fingerjnt_grp.create("joint", "LeftFingerThumb"+str(index+1), self.jnt_finger)

                    obj_lfinger_loc = sl_lst.getDependNode(index)
                    lpinkyloc_transform = om2.MFnTransform(obj_lfinger_loc)
                    loc_lpinky_transform = lpinkyloc_transform.transformation()

                    jnt_pinky_transform = om2.MFnTransform(self.jnt_finger)
                    jnt_pinky_transform.transformation()
                    jnt_pinky_transform.setTransformation(loc_lpinky_transform)

        if side == -1:
            if i == 0:
                loc_thumb = "loc_R_finger_0_*"
                sl_lst = om2.MSelectionList()
                sl_lst.add(loc_thumb)

                for index in range(sl_lst.length()):
                    if index == 0:
                        self.jnt_finger = fingerjnt_grp.create("joint", "RightFingerPinky1", self.jnt_rwrist)
                    else:
                        self.jnt_finger = fingerjnt_grp.create("joint", "RightFingerPinky"+str(index+1), self.jnt_finger)

                    obj_rthumb_loc = sl_lst.getDependNode(index)
                    rthumbloc_transform = om2.MFnTransform(obj_rthumb_loc)
                    loc_rthumb_transform = rthumbloc_transform.transformation()

                    jnt_thump_transform = om2.MFnTransform(self.jnt_finger)
                    jnt_thump_transform.transformation()
                    jnt_thump_transform.setTransformation(loc_rthumb_transform)

            if i == 1:
                loc_index = "loc_R_finger_1_*"
                sl_lst = om2.MSelectionList()
                sl_lst.add(loc_index)

                for index in range(sl_lst.length()):
                    if index == 0:
                        self.jnt_finger = fingerjnt_grp.create("joint", "RightFingerRing1", self.jnt_rwrist)
                    else:
                        self.jnt_finger = fingerjnt_grp.create("joint", "RightFingerRing"+str(index+1), self.jnt_finger)

                    obj_rfinger_loc = sl_lst.getDependNode(index)
                    rindexloc_transform = om2.MFnTransform(obj_rfinger_loc)
                    loc_rindex_transform = rindexloc_transform.transformation()

                    jnt_index_transform = om2.MFnTransform(self.jnt_finger)
                    jnt_index_transform.transformation()
                    jnt_index_transform.setTransformation(loc_rindex_transform)

            if i == 2:
                loc_middle = "loc_R_finger_2_*"
                sl_lst = om2.MSelectionList()
                sl_lst.add(loc_middle)

                for index in range(sl_lst.length()):
                    if index == 0:
                        self.jnt_finger = fingerjnt_grp.create("joint", "RightFingerMiddle1", self.jnt_rwrist)
                    else:
                        self.jnt_finger = fingerjnt_grp.create("joint", "RightFingerMiddle"+str(index+1), self.jnt_finger)

                    obj_rfinger_loc = sl_lst.getDependNode(index)
                    rmiddleloc_transform = om2.MFnTransform(obj_rfinger_loc)
                    loc_rindex_transform = rmiddleloc_transform.transformation()

                    jnt_middle_transform = om2.MFnTransform(self.jnt_finger)
                    jnt_middle_transform.transformation()
                    jnt_middle_transform.setTransformation(loc_rindex_transform)

            if i == 3:
                loc_ring = "loc_R_finger_3_*"
                sl_lst = om2.MSelectionList()
                sl_lst.add(loc_ring)

                for index in range(sl_lst.length()):
                    if index == 0:
                        self.jnt_finger = fingerjnt_grp.create("joint", "RightFingerIndex1", self.jnt_rwrist)
                    else:
                        self.jnt_finger = fingerjnt_grp.create("joint", "RightFingerIndex"+str(index+1), self.jnt_finger)

                    obj_rfinger_loc = sl_lst.getDependNode(index)
                    rringloc_transform = om2.MFnTransform(obj_rfinger_loc)
                    loc_rring_transform = rringloc_transform.transformation()

                    jnt_ring_transform = om2.MFnTransform(self.jnt_finger)
                    jnt_ring_transform.transformation()
                    jnt_ring_transform.setTransformation(loc_rring_transform)

            if i == 4:
                loc_pinky = "loc_R_finger_4_*"
                sl_lst = om2.MSelectionList()
                sl_lst.add(loc_pinky)

                for index in range(sl_lst.length()):
                    if index == 0:
                        self.jnt_finger = fingerjnt_grp.create("joint", "RightFingerThumb1", self.jnt_rwrist)
                    else:
                        self.jnt_finger = fingerjnt_grp.create("joint", "RightFingerThumb"+str(index+1), self.jnt_finger)

                    obj_rfinger_loc = sl_lst.getDependNode(index)
                    rpinkyloc_transform = om2.MFnTransform(obj_rfinger_loc)
                    loc_rpinky_transform = rpinkyloc_transform.transformation()

                    jnt_pinky_transform = om2.MFnTransform(self.jnt_finger)
                    jnt_pinky_transform.transformation()
                    jnt_pinky_transform.setTransformation(loc_rpinky_transform)

    def createLegJoints(self, side):
        legjnt_grp = om2.MFnDagNode()

        leg_loc = ["loc_L_upperleg", "loc_L_knee", "loc_L_football", "loc_L_foot", "loc_L_toe", "loc_R_upperleg", "loc_R_knee", "loc_R_football", "loc_R_foot", "loc_R_toe"]
        leg_loc_ls = om2.MSelectionList()

        if side == 1:
            self.llegik_grp = legjnt_grp.create("transform", "LeftLegIk_grp", self.donttouchjnt_grp)
            self.llegikcluster_grp = legjnt_grp.create("transform", "LeftLegIkCluster_grp", self.splineik_grp)
            self.lupperlegikcluster_grp = legjnt_grp.create("transform", "LeftUpperLegIkCluster_grp", self.llegikcluster_grp)
            self.lupperlegikcluster0_grp = legjnt_grp.create("transform", "LeftUpperLegIkCluster0_grp", self.lupperlegikcluster_grp)
            self.lupperlegikcluster1_grp = legjnt_grp.create("transform", "LeftUpperLegIkCluster1_grp", self.lupperlegikcluster_grp)
            self.lupperlegikcluster2_grp = legjnt_grp.create("transform", "LeftUpperLegIkCluster2_grp", self.lupperlegikcluster_grp)
            self.llowerlegikcluster_grp = legjnt_grp.create("transform", "LeftLowerLegIkCluster_grp", self.llegikcluster_grp)
            self.llowerlegikcluster0_grp = legjnt_grp.create("transform", "LeftLowerLegIkCluster0_grp", self.llowerlegikcluster_grp)
            self.llowerlegikcluster1_grp = legjnt_grp.create("transform", "LeftLowerLegIkCluster1_grp", self.llowerlegikcluster_grp)
            self.llowerlegikcluster2_grp = legjnt_grp.create("transform", "LeftLowerLegIkCluster2_grp", self.llowerlegikcluster_grp)

            grp_lupperleg = legjnt_grp.create("transform", "LeftJointLeg_grp", self.jnt_root_tn)
            jnt_lupperleg = legjnt_grp.create("joint", "LeftUpLeg", grp_lupperleg)

            grp_fklupperleg = legjnt_grp.create("transform", "FkLeftJointLeg_grp", self.jnt_root_tn)
            jnt_fklupperleg = legjnt_grp.create("joint", "FkLeftUpLeg", grp_fklupperleg)

            grp_iklupperleg = legjnt_grp.create("transform", "IkLeftJointLeg_grp", self.jnt_root_tn)
            jnt_iklupperleg = legjnt_grp.create("joint", "IkLeftUpLeg", grp_iklupperleg)
            jnt_iknofliprupperleg = legjnt_grp.create("joint", "IkNoFlipLeftUpLeg", grp_iklupperleg)
            jnt_ikpvrupperleg = legjnt_grp.create("joint", "IkPVLeftUpLeg", grp_iklupperleg)

            leg_loc_ls.add(leg_loc[0])
            lupperleg_loc_obj = leg_loc_ls.getDependNode(0)
            lupperleg_loc_transform = om2.MFnTransform(lupperleg_loc_obj)
            loc_lupperleg_transform = lupperleg_loc_transform.transformation()

            lupperleg_loc_path_n = om2.MDagPath()
            lupperleg_loc_path = lupperleg_loc_path_n.getAPathTo(lupperleg_loc_obj)
            loc_lupperleg_worldtransform = om2.MFnTransform(lupperleg_loc_path)
            loc_lupperleg_t = loc_lupperleg_worldtransform.translation(om2.MSpace.kWorld)

            jnt_lupperleg_transform = om2.MFnTransform(jnt_lupperleg)
            jnt_lupperleg_transform.setTransformation(loc_lupperleg_transform)

            jnt_fklupperleg_transform = om2.MFnTransform(jnt_fklupperleg)
            jnt_fklupperleg_transform.setTransformation(loc_lupperleg_transform)

            jnt_iklupperleg_transform = om2.MFnTransform(jnt_iklupperleg)
            jnt_iklupperleg_transform.setTransformation(loc_lupperleg_transform)
        #
        #     jnt_iknofliplupperleg_transform = om2.MFnTransform(jnt_iknofliplupperleg)
        #     jnt_iknofliplupperleg_transform.setTransformation(loc_lupperleg_transform)
        #
        #     jnt_ikpvlupperleg_transform = om2.MFnTransform(jnt_ikpvlupperleg)
        #     jnt_ikpvlupperleg_transform.setTransformation(loc_lupperleg_transform)
        #
        #     jnt_lknee = legjnt_grp.create("joint", "LeftLeg", jnt_lupperleg)
        #     jnt_fklknee = legjnt_grp.create("joint", "FkLeftLeg", jnt_fklupperleg)
        #     jnt_iklknee = legjnt_grp.create("joint", "IkLeftLeg", jnt_iklupperleg)
        #     jnt_iknofliplknee = legjnt_grp.create("joint", "IkNoFlipLeftLeg", jnt_iknofliplupperleg)
        #     jnt_ikpvlknee = legjnt_grp.create("joint", "IkPVLeftLeg", jnt_ikpvlupperleg)
        #
        #     leg_loc_ls.add(leg_loc[1])
        #     lknee_loc_obj = leg_loc_ls.getDependNode(1)
        #     lknee_loc_transform = om2.MFnTransform(lknee_loc_obj)
        #     loc_lknee_transform = lknee_loc_transform.transformation()
        #     loc_lknee_transform_t = loc_lknee_transform.translation(om2.MSpace.kTransform)
        #
        #     lkneeleg_loc_path_n = om2.MDagPath()
        #     lkneeleg_loc_path = lkneeleg_loc_path_n.getAPathTo(lknee_loc_obj)
        #     loc_lkneeleg_transform = om2.MFnTransform(lkneeleg_loc_path)
        #     loc_lkneeleg_t = loc_lkneeleg_transform.translation(om2.MSpace.kWorld)
        #
        #     jnt_lknee_transform = om2.MFnTransform(jnt_lknee)
        #     jnt_lknee_transform.setTransformation(loc_lknee_transform)
        #
        #     jnt_fklknee_transform = om2.MFnTransform(jnt_fklknee)
        #     jnt_fklknee_transform.setTransformation(loc_lknee_transform)
        #
        #     jnt_iklknee_transform = om2.MFnTransform(jnt_iklknee)
        #     jnt_iklknee_transform.setTransformation(loc_lknee_transform)
        #
        #     jnt_iknofliplknee_transform = om2.MFnTransform(jnt_iknofliplknee)
        #     jnt_iknofliplknee_transform.setTransformation(loc_lknee_transform)
        #
        #     jnt_ikpvlknee_transform = om2.MFnTransform(jnt_ikpvlknee)
        #     jnt_ikpvlknee_transform.setTransformation(loc_lknee_transform)
        #
        #     jnt_lfootball = legjnt_grp.create("joint", "LeftFoot", jnt_lknee)
        #     jnt_fklfootball = legjnt_grp.create("joint", "FkLeftFoot", jnt_fklknee)
        #     jnt_iklfootball = legjnt_grp.create("joint", "IkLeftFoot", jnt_iklknee)
        #     jnt_iknofliplfootball = legjnt_grp.create("joint", "IkNoFlipLeftFoot", jnt_iknofliplknee)
        #     jnt_ikpvlfootball = legjnt_grp.create("joint", "IkPVLeftFoot", jnt_ikpvlknee)
        #     lreversefoot_hell = legjnt_grp.create("transform", "LeftReverseFootHeel")
        #     lreversefoot_hell_ln = legjnt_grp.create("locator", "LeftReverseFootHeelShape", lreversefoot_hell)
        #
        #     leg_loc_ls.add(leg_loc[2])
        #     lfootball_loc_obj = leg_loc_ls.getDependNode(2)
        #     lfootball_loc_transform = om2.MFnTransform(lfootball_loc_obj)
        #     loc_lfootball_transform = lfootball_loc_transform.transformation()
        #     loc_lfootball_t = lfootball_loc_transform.translation(om2.MSpace.kTransform)
        #
        #     lfootballleg_loc_path_n = om2.MDagPath()
        #     lfootballleg_loc_path = lfootballleg_loc_path_n.getAPathTo(lfootball_loc_obj)
        #     loc_lfootballleg_transform = om2.MFnTransform(lfootballleg_loc_path)
        #     loc_lfootballleg_t = loc_lfootballleg_transform.translation(om2.MSpace.kWorld)
        #
        #     jnt_lfootball_transform = om2.MFnTransform(jnt_lfootball)
        #     jnt_lfootball_transform.setTransformation(loc_lfootball_transform)
        #
        #     jnt_fklfootball_transform = om2.MFnTransform(jnt_fklfootball)
        #     jnt_fklfootball_transform.setTransformation(loc_lfootball_transform)
        #
        #     jnt_iklfootball_transform = om2.MFnTransform(jnt_iklfootball)
        #     jnt_iklfootball_transform.setTransformation(loc_lfootball_transform)
        #
        #     jnt_iknofliplfootball_transform = om2.MFnTransform(jnt_iknofliplfootball)
        #     jnt_iknofliplfootball_transform.setTransformation(loc_lfootball_transform)
        #
        #     jnt_ikpvlfootball_transform = om2.MFnTransform(jnt_ikpvlfootball)
        #     jnt_ikpvlfootball_transform.setTransformation(loc_lfootball_transform)
        #
        #     lreversefoot_hell_transform = om2.MFnTransform(lreversefoot_hell)
        #     lreversefoot_hell_transform_t = lreversefoot_hell_transform.translation(om2.MSpace.kTransform)
        #     lreversefoot_hell_transform_t[0], lreversefoot_hell_transform_t[1], lreversefoot_hell_transform_t[2] = loc_lfootballleg_t[0], loc_lfootballleg_t[1], -loc_lfootballleg_t[2]*10
        #     lreversefoot_hell_transform.setTranslation(lreversefoot_hell_transform_t, om2.MSpace.kTransform)
        #
        #     grp_llegik_transform = om2.MFnTransform(self.llegik_grp)
        #     grp_llegik_transform.setTranslation(loc_lfootballleg_t, om2.MSpace.kTransform)
        #
        #     jnt_lfoot = legjnt_grp.create("joint", "LeftToeBase", jnt_lfootball)
        #     jnt_fklfoot = legjnt_grp.create("joint", "FkLeftToeBase", jnt_fklfootball)
        #     jnt_iklfoot = legjnt_grp.create("joint", "IkLeftToeBase", jnt_iklfootball)
        #     lreversefoot_foot = legjnt_grp.create("transform", "LeftReverseFootToe")
        #     lreversefoot_foot_ln = legjnt_grp.create("locator", "LeftReverseFootToeShape", lreversefoot_foot)
        #     lreverseinner_foot = legjnt_grp.create("transform", "LeftReverseInnerFoot")
        #     lreverseinner_foot_ln = legjnt_grp.create("locator", "LeftReverseInnerFootShape", lreverseinner_foot)
        #     lreverseouter_foot = legjnt_grp.create("transform", "LeftReverseOuterFoot")
        #     lreverseouter_foot_ln = legjnt_grp.create("locator", "LeftReverseOuterFootShape", lreverseouter_foot)
        #
        #     leg_loc_ls.add(leg_loc[3])
        #     lfoot_loc_obj = leg_loc_ls.getDependNode(3)
        #     lfoot_loc_transform = om2.MFnTransform(lfoot_loc_obj)
        #     loc_lfoot_transform = lfoot_loc_transform.transformation()
        #
        #     lfootleg_loc_path_n = om2.MDagPath()
        #     lfootleg_loc_path = lfootleg_loc_path_n.getAPathTo(lfoot_loc_obj)
        #     loc_lfootleg_transform = om2.MFnTransform(lfootleg_loc_path)
        #     loc_lfootleg_t = loc_lfootleg_transform.translation(om2.MSpace.kWorld)
        #
        #     jnt_lfoot_transform = om2.MFnTransform(jnt_lfoot)
        #     jnt_lfoot_transform.setTransformation(loc_lfoot_transform)
        #
        #     jnt_fklfoot_transform = om2.MFnTransform(jnt_fklfoot)
        #     jnt_fklfoot_transform.setTransformation(loc_lfoot_transform)
        #
        #     jnt_iklfoot_transform = om2.MFnTransform(jnt_iklfoot)
        #     jnt_iklfoot_transform.setTransformation(loc_lfoot_transform)
        #
        #     lreversefoot_foot_transform = om2.MFnTransform(lreversefoot_foot)
        #     lreversefoot_foot_transform.setTranslation(loc_lfootleg_t, om2.MSpace.kTransform)
        #
        #     lreverseinner_foot_transform = om2.MFnTransform(lreverseinner_foot)
        #     lreverseinner_foot_transform_t = lreverseinner_foot_transform.translation(om2.MSpace.kTransform)
        #     lreverseinner_foot_transform_t[0], lreverseinner_foot_transform_t[2], lreverseinner_foot_transform_t[2] = loc_lfootleg_t[0]*0.1, loc_lfootleg_t[1], loc_lfootleg_t[2]
        #     lreverseinner_foot_transform.setTranslation(lreverseinner_foot_transform_t, om2.MSpace.kTransform)
        #
        #     lreverseouter_foot_transform = om2.MFnTransform(lreverseouter_foot)
        #     lreverseouter_foot_transform_t = lreverseouter_foot_transform.translation(om2.MSpace.kTransform)
        #     lreverseouter_foot_transform_t[0], lreverseouter_foot_transform_t[2], lreverseouter_foot_transform_t[2] = loc_lfootleg_t[0]*1.9, loc_lfootleg_t[1], loc_lfootleg_t[2]
        #     lreverseouter_foot_transform.setTranslation(lreverseouter_foot_transform_t, om2.MSpace.kTransform)
        #
        #     jnt_ltoe = legjnt_grp.create("joint", "LeftToeEnd", jnt_lfoot)
        #     jnt_fkltoe = legjnt_grp.create("joint", "FkLeftToeEnd", jnt_fklfoot)
        #     jnt_ikltoe = legjnt_grp.create("joint", "IkLeftToeEnd", jnt_iklfoot)
        #     lreversefoot_toe = legjnt_grp.create("transform", "LeftReverseFootToeEnd")
        #     lreversefoot_toe_ln = legjnt_grp.create("locator", "LeftReverseFootToeEndShape", lreversefoot_toe)
        #     lreversefoot_toewiggle = legjnt_grp.create("transform", "LeftReverseFootToeWiggle", lreversefoot_toe)
        #
        #     leg_loc_ls.add(leg_loc[4])
        #     ltoe_loc_obj = leg_loc_ls.getDependNode(4)
        #     ltoe_loc_transform = om2.MFnTransform(ltoe_loc_obj)
        #     loc_ltoe_transform = ltoe_loc_transform.transformation()
        #
        #     ltoeleg_loc_path_n = om2.MDagPath()
        #     ltoeleg_loc_path = ltoeleg_loc_path_n.getAPathTo(ltoe_loc_obj)
        #     loc_ltoeleg_transform = om2.MFnTransform(ltoeleg_loc_path)
        #     loc_ltoeleg_t = loc_ltoeleg_transform.translation(om2.MSpace.kWorld)
        #
        #     jnt_ltoe_transform = om2.MFnTransform(jnt_ltoe)
        #     jnt_ltoe_transform.setTransformation(loc_ltoe_transform)
        #
        #     jnt_fkltoe_transform = om2.MFnTransform(jnt_fkltoe)
        #     jnt_fkltoe_transform.setTransformation(loc_ltoe_transform)
        #
        #     jnt_ikltoe_transform = om2.MFnTransform(jnt_ikltoe)
        #     jnt_ikltoe_transform.setTransformation(loc_ltoe_transform)
        #
        #     lreversefoot_toe_transform = om2.MFnTransform(lreversefoot_toe)
        #     lreversefoot_toe_transform.setTranslation(loc_ltoeleg_t, om2.MSpace.kTransform)
        #
        #     lfoottoewiggle_path_n = om2.MDagPath()
        #     lfoottoewiggle_path = lfoottoewiggle_path_n.getAPathTo(lreversefoot_toewiggle)
        #     lfoottoewiggle_worldtransform = om2.MFnTransform(lfoottoewiggle_path)
        #     lfoottoewiggle_worldtransform.setRotatePivot(om2.MPoint(loc_lfootleg_t), om2.MSpace.kWorld, False)
        #
        #     grp_stretchyiklleg = legjnt_grp.create("transform", "IkStretchyLeftJointLeg_grp", self.splineik_grp)
        #
        #     grp_stretchyiklleg_transform = om2.MFnTransform(grp_stretchyiklleg)
        #     grp_stretchyiklleg_transform.setTransformation(self.loc_root_transform)
        #
        #     jnt_stretchyiklupperleg0 = legjnt_grp.create("joint", "IkSplineLeftUpperLeg0", grp_stretchyiklleg)
        #     jnt_stretchyikcvlupperleg0 = legjnt_grp.create("joint", "IkCvSplineLeftUpperLeg0", self.lupperlegikcluster0_grp)
        #
        #     jnt_stretchyiklupperleg0_transform = om2.MFnTransform(jnt_stretchyiklupperleg0)
        #     jnt_stretchyiklupperleg0_transform.setTransformation(loc_lupperleg_transform)
        #
        #     jnt_stretchyikcvlupperleg0_transform = om2.MFnTransform(self.lupperlegikcluster_grp)
        #     jnt_stretchyikcvlupperleg0_transform.setTranslation(loc_lupperleg_t, om2.MSpace.kTransform)
        #
        #     jnt_stretchyiklupperleg1 = legjnt_grp.create("joint", "IkSplineLeftUpperLeg1", jnt_stretchyiklupperleg0)
        #
        #     jnt_stretchyiklupperleg1_transform = om2.MFnTransform(jnt_stretchyiklupperleg1)
        #     jnt_stretchyiklupperleg1_transform_t = jnt_stretchyiklupperleg1_transform.translation(om2.MSpace.kTransform)
        #     jnt_stretchyiklupperleg1_transform_t[0], jnt_stretchyiklupperleg1_transform_t[1], jnt_stretchyiklupperleg1_transform_t[2] = loc_lknee_transform_t[0]/4, loc_lknee_transform_t[1]/4, loc_lknee_transform_t[2]/4
        #     jnt_stretchyiklupperleg1_transform.setTranslation(jnt_stretchyiklupperleg1_transform_t, om2.MSpace.kTransform)
        #
        #     jnt_stretchyiklupperleg2 = legjnt_grp.create("joint", "IkSplineLeftUpperLeg2", jnt_stretchyiklupperleg1)
        #     jnt_stretchyikcvlupperleg1 = legjnt_grp.create("joint", "IkCvSplineLeftUpperLeg1", self.lupperlegikcluster1_grp)
        #
        #     jnt_stretchyiklupperleg2_transform = om2.MFnTransform(jnt_stretchyiklupperleg2)
        #     jnt_stretchyiklupperleg2_transform_t = jnt_stretchyiklupperleg2_transform.translation(om2.MSpace.kTransform)
        #     jnt_stretchyiklupperleg2_transform_t[0], jnt_stretchyiklupperleg2_transform_t[1], jnt_stretchyiklupperleg2_transform_t[2] = loc_lknee_transform_t[0]/2, (loc_lknee_transform_t[1]/2)-jnt_stretchyiklupperleg1_transform_t[1], (loc_lknee_transform_t[2]/2)-jnt_stretchyiklupperleg1_transform_t[2]
        #     jnt_stretchyiklupperleg2_transform.setTranslation(jnt_stretchyiklupperleg2_transform_t, om2.MSpace.kTransform)
        #
        #     jnt_stretchyikcvlupperleg0_transform_t = jnt_stretchyikcvlupperleg0_transform.translation(om2.MSpace.kTransform)
        #
        #     jnt_stretchyikcvlupperleg1grp_transform = om2.MFnTransform(self.lupperlegikcluster1_grp)
        #     jnt_stretchyikcvlupperleg1grp_transform_t = jnt_stretchyikcvlupperleg1grp_transform.translation(om2.MSpace.kTransform)
        #     jnt_stretchyikcvlupperleg1grp_transform_t[0], jnt_stretchyikcvlupperleg1grp_transform_t[1], jnt_stretchyikcvlupperleg1grp_transform_t[2] = -(jnt_stretchyikcvlupperleg0_transform_t[0]-loc_lkneeleg_t[0])/2, -(jnt_stretchyikcvlupperleg0_transform_t[1]-loc_lkneeleg_t[1])/2, -(jnt_stretchyikcvlupperleg0_transform_t[2]-loc_lkneeleg_t[2])/2 #loc_lkneeleg_t[0]+(loc_lupperleg_t[0]-loc_lkneeleg_t[0])/2, loc_lkneeleg_t[1]+(loc_lupperleg_t[1]-loc_lkneeleg_t[1])/2, loc_lkneeleg_t[2]+(loc_lupperleg_t[2]-loc_lkneeleg_t[2])/2
        #     jnt_stretchyikcvlupperleg1grp_transform.setTranslation(jnt_stretchyikcvlupperleg1grp_transform_t, om2.MSpace.kTransform)
        #
        #     jnt_stretchyiklupperleg3 = legjnt_grp.create("joint", "IkSplineLeftUpperLeg3", jnt_stretchyiklupperleg2)
        #
        #     jnt_stretchyiklupperleg3_transform = om2.MFnTransform(jnt_stretchyiklupperleg3)
        #     jnt_stretchyiklupperleg3_transform_t = jnt_stretchyiklupperleg3_transform.translation(om2.MSpace.kTransform)
        #     jnt_stretchyiklupperleg3_transform_t[0], jnt_stretchyiklupperleg3_transform_t[1], jnt_stretchyiklupperleg3_transform_t[2] = jnt_stretchyiklupperleg2_transform_t[0], jnt_stretchyiklupperleg2_transform_t[1], jnt_stretchyiklupperleg2_transform_t[2]
        #     jnt_stretchyiklupperleg3_transform.setTranslation(jnt_stretchyiklupperleg3_transform_t, om2.MSpace.kTransform)
        #
        #     jnt_stretchyiklupperleg4 = legjnt_grp.create("joint", "IkSplineLeftUpperLeg4", jnt_stretchyiklupperleg3)
        #     jnt_stretchyikcvlupperleg2 = legjnt_grp.create("joint", "IkCvSplineLeftUpperLeg2", self.lupperlegikcluster2_grp)
        #
        #     jnt_stretchyiklupperleg4_transform = om2.MFnTransform(jnt_stretchyiklupperleg4)
        #     jnt_stretchyiklupperleg4_transform_t = jnt_stretchyiklupperleg4_transform.translation(om2.MSpace.kTransform)
        #     jnt_stretchyiklupperleg4_transform_t[0], jnt_stretchyiklupperleg4_transform_t[1], jnt_stretchyiklupperleg4_transform_t[2] = jnt_stretchyiklupperleg3_transform_t[0], jnt_stretchyiklupperleg3_transform_t[1], jnt_stretchyiklupperleg3_transform_t[2]
        #     jnt_stretchyiklupperleg4_transform.setTranslation(jnt_stretchyiklupperleg4_transform_t, om2.MSpace.kTransform)
        #
        #     jnt_stretchyikcvlupperleg2_transform = om2.MFnTransform(self.lupperlegikcluster2_grp)
        #     jnt_stretchyikcvlupperleg2_transform_t = jnt_stretchyikcvlupperleg2_transform.translation(om2.MSpace.kTransform)
        #     jnt_stretchyikcvlupperleg2_transform_t[0], jnt_stretchyikcvlupperleg2_transform_t[1], jnt_stretchyikcvlupperleg2_transform_t[2] = -(jnt_stretchyikcvlupperleg0_transform_t[0]-loc_lkneeleg_t[0]), -(jnt_stretchyikcvlupperleg0_transform_t[1]-loc_lkneeleg_t[1]), -(jnt_stretchyikcvlupperleg0_transform_t[2]-loc_lkneeleg_t[2]) #loc_lkneeleg_t[0], loc_lkneeleg_t[1], loc_lkneeleg_t[2]
        #     jnt_stretchyikcvlupperleg2_transform.setTranslation(jnt_stretchyikcvlupperleg2_transform_t, om2.MSpace.kTransform)
        #
        #     jnt_stretchyikllowerleg0 = legjnt_grp.create("joint", "IkSplineLeftLowerLeg0", grp_stretchyiklleg)
        #     jnt_stretchyikcvllowerleg0 = legjnt_grp.create("joint", "IkCvSplineLeftLowerLeg0", self.llowerlegikcluster0_grp)
        #
        #     jnt_stretchyikllowerleg0_transform = om2.MFnTransform(jnt_stretchyikllowerleg0)
        #     jnt_stretchyikllowerleg0_transform.setTranslation(loc_lkneeleg_t-grp_stretchyiklleg_transform.translation(om2.MSpace.kTransform), om2.MSpace.kTransform)
        #
        #     jnt_stretchyikcvllowerleg0_transform = om2.MFnTransform(self.llowerlegikcluster_grp)
        #     jnt_stretchyikcvllowerleg0_transform.setTranslation(loc_lkneeleg_t, om2.MSpace.kTransform)
        #
        #     jnt_stretchyikllowerleg1 = legjnt_grp.create("joint", "IkSplineLeftLowerLeg1", jnt_stretchyikllowerleg0)
        #
        #     jnt_stretchyikllowerleg1_transform = om2.MFnTransform(jnt_stretchyikllowerleg1)
        #     jnt_stretchyikllowerleg1_transform_t = jnt_stretchyikllowerleg1_transform.translation(om2.MSpace.kTransform)
        #     jnt_stretchyikllowerleg1_transform_t[0], jnt_stretchyikllowerleg1_transform_t[1], jnt_stretchyikllowerleg1_transform_t[2] = loc_lfootball_t[0]/4, loc_lfootball_t[1]/4, loc_lfootball_t[2]/4
        #     jnt_stretchyikllowerleg1_transform.setTranslation(jnt_stretchyikllowerleg1_transform_t, om2.MSpace.kTransform)
        #
        #     jnt_stretchyikllowerleg2 = legjnt_grp.create("joint", "IkSplineLeftLowerLeg2", jnt_stretchyikllowerleg1)
        #     jnt_stretchyikvcvllowerleg1 = legjnt_grp.create("joint", "IkCvSplineLeftLowerLeg1", self.llowerlegikcluster1_grp)
        #
        #     jnt_stretchyikllowerleg2_transform = om2.MFnTransform(jnt_stretchyikllowerleg2)
        #     jnt_stretchyikllowerleg2_transform_t = jnt_stretchyikllowerleg2_transform.translation(om2.MSpace.kTransform)
        #     jnt_stretchyikllowerleg2_transform_t[0], jnt_stretchyikllowerleg2_transform_t[1], jnt_stretchyikllowerleg2_transform_t[2] = (loc_lfootball_t[0]/2)-jnt_stretchyikllowerleg1_transform_t[0], (loc_lfootball_t[1]/2)-jnt_stretchyikllowerleg1_transform_t[1], (loc_lfootball_t[2]/2)-jnt_stretchyikllowerleg1_transform_t[2]
        #     jnt_stretchyikllowerleg2_transform.setTranslation(jnt_stretchyikllowerleg2_transform_t, om2.MSpace.kTransform)
        #
        #     jnt_stretchyikcvllowerleg0_transform_t = jnt_stretchyikcvllowerleg0_transform.translation(om2.MSpace.kTransform)
        #
        #     jnt_stretchyikcvllowerleg1_transform = om2.MFnTransform(self.llowerlegikcluster1_grp)
        #     jnt_stretchyikcvllowerleg1_transform_t = jnt_stretchyikcvllowerleg1_transform.translation(om2.MSpace.kTransform)
        #     jnt_stretchyikcvllowerleg1_transform_t[0], jnt_stretchyikcvllowerleg1_transform_t[1], jnt_stretchyikcvllowerleg1_transform_t[2] = -(jnt_stretchyikcvllowerleg0_transform_t[0]-loc_lfootballleg_t[0])/2, -(jnt_stretchyikcvllowerleg0_transform_t[1]-loc_lfootballleg_t[1])/2, -(jnt_stretchyikcvllowerleg0_transform_t[2]-loc_lfootballleg_t[2])/2 #loc_lfootballleg_t[0]+((loc_lkneeleg_t[0]-loc_lfootballleg_t[0])/2), loc_lfootballleg_t[1]+((loc_lkneeleg_t[1]-loc_lfootballleg_t[1])/2), loc_lfootballleg_t[2]+((loc_lkneeleg_t[2]-loc_lfootballleg_t[2])/2)
        #     jnt_stretchyikcvllowerleg1_transform.setTranslation(jnt_stretchyikcvllowerleg1_transform_t, om2.MSpace.kTransform)
        #
        #     jnt_stretchyikllowerleg3 = legjnt_grp.create("joint", "IkSplineLeftLowerLeg3", jnt_stretchyikllowerleg2)
        #
        #     jnt_stretchyikllowerleg3_transform = om2.MFnTransform(jnt_stretchyikllowerleg3)
        #     jnt_stretchyikllowerleg3_transform_t = jnt_stretchyikllowerleg3_transform.translation(om2.MSpace.kTransform)
        #     jnt_stretchyikllowerleg3_transform_t[0], jnt_stretchyikllowerleg3_transform_t[1], jnt_stretchyikllowerleg3_transform_t[2] = jnt_stretchyikllowerleg2_transform_t[0], jnt_stretchyikllowerleg2_transform_t[1], jnt_stretchyikllowerleg2_transform_t[2]
        #     jnt_stretchyikllowerleg3_transform.setTranslation(jnt_stretchyikllowerleg3_transform_t, om2.MSpace.kTransform)
        #
        #     jnt_stretchyikllowerleg4 = legjnt_grp.create("joint", "IkSplineLeftLowerLeg4", jnt_stretchyikllowerleg3)
        #     jnt_stretchyikvcvllowerleg2 = legjnt_grp.create("joint", "IkCvSplineLeftLowerLeg2", self.llowerlegikcluster2_grp)
        #
        #     jnt_stretchyikllowerleg4_transform = om2.MFnTransform(jnt_stretchyikllowerleg4)
        #     jnt_stretchyikllowerleg4_transform_t = jnt_stretchyikllowerleg4_transform.translation(om2.MSpace.kTransform)
        #     jnt_stretchyikllowerleg4_transform_t[0], jnt_stretchyikllowerleg4_transform_t[1], jnt_stretchyikllowerleg4_transform_t[2] = jnt_stretchyikllowerleg3_transform_t[0], jnt_stretchyikllowerleg3_transform_t[1], jnt_stretchyikllowerleg3_transform_t[2]
        #     jnt_stretchyikllowerleg4_transform.setTranslation(jnt_stretchyikllowerleg4_transform_t, om2.MSpace.kTransform)
        #
        #     jnt_stretchyikcvllowerleg4_transform = om2.MFnTransform(self.llowerlegikcluster2_grp)
        #     jnt_stretchyikcvllowerleg4_transform_t = jnt_stretchyikcvllowerleg4_transform.translation(om2.MSpace.kTransform)
        #     jnt_stretchyikcvllowerleg4_transform_t[0], jnt_stretchyikcvllowerleg4_transform_t[1], jnt_stretchyikcvllowerleg4_transform_t[2] = -(jnt_stretchyikcvllowerleg0_transform_t[0]-loc_lfootballleg_t[0]), -(jnt_stretchyikcvllowerleg0_transform_t[1]-loc_lfootballleg_t[1]), -(jnt_stretchyikcvllowerleg0_transform_t[2]-loc_lfootballleg_t[2]) #loc_lfootballleg_t[0], loc_lfootballleg_t[1], loc_lfootballleg_t[2]
        #     jnt_stretchyikcvllowerleg4_transform.setTranslation(jnt_stretchyikcvllowerleg4_transform_t, om2.MSpace.kTransform)

        if side == -1:
            self.rlegik_grp = legjnt_grp.create("transform", "RightLegIk_grp", self.donttouchjnt_grp)
            self.rlegikcluster_grp = legjnt_grp.create("transform", "RightLegIkCluster_grp", self.splineik_grp)
            self.rupperlegikcluster_grp = legjnt_grp.create("transform", "RightUpperLegIkCluster_grp", self.rlegikcluster_grp)
            self.rupperlegikcluster0_grp = legjnt_grp.create("transform", "RightUpperLegIkCluster0_grp", self.rupperlegikcluster_grp)
            self.rupperlegikcluster1_grp = legjnt_grp.create("transform", "RightUpperLegIkCluster1_grp", self.rupperlegikcluster_grp)
            self.rupperlegikcluster2_grp = legjnt_grp.create("transform", "RightUpperLegIkCluster2_grp", self.rupperlegikcluster_grp)
            self.rlowerlegikcluster_grp = legjnt_grp.create("transform", "RightLowerLegIkCluster_grp", self.rlegikcluster_grp)
            self.rlowerlegikcluster0_grp = legjnt_grp.create("transform", "RightLowerLegIkCluster0_grp", self.rlowerlegikcluster_grp)
            self.rlowerlegikcluster1_grp = legjnt_grp.create("transform", "RightLowerLegIkCluster1_grp", self.rlowerlegikcluster_grp)
            self.rlowerlegikcluster2_grp = legjnt_grp.create("transform", "RightLowerLegIkCluster2_grp", self.rlowerlegikcluster_grp)

            grp_rupperleg = legjnt_grp.create("transform", "RightJointLeg_grp", self.jnt_root_tn)
            jnt_rupperleg = legjnt_grp.create("joint", "RightUpLeg", grp_rupperleg)

            jnt_fkrupperleg = legjnt_grp.create("joint", "FkRightUpLeg", self.jnt_root_tn)

            grp_ikrupperleg = legjnt_grp.create("transform", "IkRightJointLeg_grp", self.jnt_root_tn)
            jnt_ikrupperleg = legjnt_grp.create("joint", "IkRightUpLeg", grp_ikrupperleg)
            jnt_iknofliprupperleg = legjnt_grp.create("joint", "IkNoFlipRightUpLeg", grp_ikrupperleg)
            jnt_ikpvrupperleg = legjnt_grp.create("joint", "IkPVRightUpLeg", grp_ikrupperleg)

            leg_loc_ls.add(leg_loc[5])
            rupperleg_loc_obj = leg_loc_ls.getDependNode(0)
            rupperleg_loc_transform = om2.MFnTransform(rupperleg_loc_obj)
            loc_rupperleg_transform = rupperleg_loc_transform.transformation()

            rupperleg_loc_path_n = om2.MDagPath()
            rupperleg_loc_path = rupperleg_loc_path_n.getAPathTo(rupperleg_loc_obj)
            loc_rupperleg_worldtransform = om2.MFnTransform(rupperleg_loc_path)
            loc_rupperleg_t = loc_rupperleg_worldtransform.translation(om2.MSpace.kWorld)

            jnt_rupperleg_transform = om2.MFnTransform(jnt_rupperleg)
            jnt_rupperleg_transform.setTransformation(loc_rupperleg_transform)

            jnt_fkrupperleg_transform = om2.MFnTransform(jnt_fkrupperleg)
            jnt_fkrupperleg_transform.setTransformation(loc_rupperleg_transform)

            jnt_ikrupperleg_transform = om2.MFnTransform(jnt_ikrupperleg)
            jnt_ikrupperleg_transform.setTransformation(loc_rupperleg_transform)

            jnt_iknofliprupperleg_transform = om2.MFnTransform(jnt_iknofliprupperleg)
            jnt_iknofliprupperleg_transform.setTransformation(loc_rupperleg_transform)

            jnt_ikpvrupperleg_transform = om2.MFnTransform(jnt_ikpvrupperleg)
            jnt_ikpvrupperleg_transform.setTransformation(loc_rupperleg_transform)

            jnt_rknee = legjnt_grp.create("joint", "RightLeg", jnt_rupperleg)
            jnt_fkrknee = legjnt_grp.create("joint", "FkRightLeg", jnt_fkrupperleg)
            jnt_ikrknee = legjnt_grp.create("joint", "IkRightLeg", jnt_ikrupperleg)
            jnt_iknofliprknee = legjnt_grp.create("joint", "IkNoFlipRightLeg", jnt_iknofliprupperleg)
            jnt_ikpvrknee = legjnt_grp.create("joint", "IkPVRightLeg", jnt_ikpvrupperleg)

            leg_loc_ls.add(leg_loc[6])
            rknee_loc_obj = leg_loc_ls.getDependNode(1)
            rknee_loc_transform = om2.MFnTransform(rknee_loc_obj)
            loc_rknee_transform = rknee_loc_transform.transformation()
            loc_rknee_transform_t = loc_rknee_transform.translation(om2.MSpace.kTransform)

            rkneeleg_loc_path_n = om2.MDagPath()
            rkneeleg_loc_path = rkneeleg_loc_path_n.getAPathTo(rknee_loc_obj)
            loc_rkneeleg_transform = om2.MFnTransform(rkneeleg_loc_path)
            loc_rkneeleg_t = loc_rkneeleg_transform.translation(om2.MSpace.kWorld)

            jnt_rknee_transform = om2.MFnTransform(jnt_rknee)
            jnt_rknee_transform.setTransformation(loc_rknee_transform)

            jnt_fkrknee_transform = om2.MFnTransform(jnt_fkrknee)
            jnt_fkrknee_transform.setTransformation(loc_rknee_transform)

            jnt_ikrknee_transform = om2.MFnTransform(jnt_ikrknee)
            jnt_ikrknee_transform.setTransformation(loc_rknee_transform)

            jnt_iknofliprknee_transform = om2.MFnTransform(jnt_iknofliprknee)
            jnt_iknofliprknee_transform.setTransformation(loc_rknee_transform)

            jnt_ikpvrknee_transform = om2.MFnTransform(jnt_ikpvrknee)
            jnt_ikpvrknee_transform.setTransformation(loc_rknee_transform)

            jnt_rfootball = legjnt_grp.create("joint", "RightFoot", jnt_rknee)
            jnt_fkrfootball = legjnt_grp.create("joint", "FkRightFoot", jnt_fkrknee)
            jnt_ikrfootball = legjnt_grp.create("joint", "IkRightFoot", jnt_ikrknee)
            jnt_iknofliprfootball = legjnt_grp.create("joint", "IkNoFlipRightFoot", jnt_iknofliprknee)
            jnt_ikpvrfootball = legjnt_grp.create("joint", "IkPVRightFoot", jnt_ikpvrknee)
            rreversefoot_hell = legjnt_grp.create("transform", "RightReverseFootHeel")
            rreversefoot_hell_ln = legjnt_grp.create("locator", "RightReverseFootHeelShape", rreversefoot_hell)

            leg_loc_ls.add(leg_loc[7])
            rfootball_loc_obj = leg_loc_ls.getDependNode(2)
            rfootball_loc_transform = om2.MFnTransform(rfootball_loc_obj)
            loc_rfootball_transform = rfootball_loc_transform.transformation()
            loc_rfootball_t = rfootball_loc_transform.translation(om2.MSpace.kTransform)

            rfootballleg_loc_path_n = om2.MDagPath()
            rfootballleg_loc_path = rfootballleg_loc_path_n.getAPathTo(rfootball_loc_obj)
            loc_rfootballleg_transform = om2.MFnTransform(rfootballleg_loc_path)
            loc_rfootballleg_t = loc_rfootballleg_transform.translation(om2.MSpace.kWorld)

            jnt_rfootball_transform = om2.MFnTransform(jnt_rfootball)
            jnt_rfootball_transform.setTransformation(loc_rfootball_transform)

            jnt_fkrfootball_transform = om2.MFnTransform(jnt_fkrfootball)
            jnt_fkrfootball_transform.setTransformation(loc_rfootball_transform)

            jnt_ikrfootball_transform = om2.MFnTransform(jnt_ikrfootball)
            jnt_ikrfootball_transform.setTransformation(loc_rfootball_transform)

            jnt_iknofliprfootball_transform = om2.MFnTransform(jnt_iknofliprfootball)
            jnt_iknofliprfootball_transform.setTransformation(loc_rfootball_transform)

            jnt_ikpvrfootball_transform = om2.MFnTransform(jnt_ikpvrfootball)
            jnt_ikpvrfootball_transform.setTransformation(loc_rfootball_transform)

            rreversefoot_hell_transform = om2.MFnTransform(rreversefoot_hell)
            rreversefoot_hell_transform_t = rreversefoot_hell_transform.translation(om2.MSpace.kTransform)
            rreversefoot_hell_transform_t[0], rreversefoot_hell_transform_t[1], rreversefoot_hell_transform_t[2] = loc_rfootballleg_t[0], loc_rfootballleg_t[1], -loc_rfootballleg_t[2]*10
            rreversefoot_hell_transform.setTranslation(rreversefoot_hell_transform_t, om2.MSpace.kTransform)

            grp_rlegik_transform = om2.MFnTransform(self.rlegik_grp)
            grp_rlegik_transform.setTranslation(loc_rfootballleg_t, om2.MSpace.kTransform)

            jnt_rfoot = legjnt_grp.create("joint", "RightToeBase", jnt_rfootball)
            jnt_fkrfoot = legjnt_grp.create("joint", "FkRightToeBase", jnt_fkrfootball)
            jnt_ikrfoot = legjnt_grp.create("joint", "IkRightToeBase", jnt_ikrfootball)
            rreversefoot_foot = legjnt_grp.create("transform", "RightReverseFootToe")
            rreversefoot_foot_ln = legjnt_grp.create("locator", "RightReverseFootToeShape", rreversefoot_foot)
            rreverseinner_foot = legjnt_grp.create("transform", "RightReverseInnerFoot")
            rreverseinner_foot_ln = legjnt_grp.create("locator", "RightReverseInnerFootShape", rreverseinner_foot)
            rreverseouter_foot = legjnt_grp.create("transform", "RightReverseOuterFoot")
            rreverseouter_foot_ln = legjnt_grp.create("locator", "RightReverseOuterFootShape", rreverseouter_foot)

            leg_loc_ls.add(leg_loc[8])
            rfoot_loc_obj = leg_loc_ls.getDependNode(3)
            rfoot_loc_transform = om2.MFnTransform(rfoot_loc_obj)
            loc_rfoot_transform = rfoot_loc_transform.transformation()

            rfootleg_loc_path_n = om2.MDagPath()
            rfootleg_loc_path = rfootleg_loc_path_n.getAPathTo(rfoot_loc_obj)
            loc_rfootleg_transform = om2.MFnTransform(rfootleg_loc_path)
            loc_rfootleg_t = loc_rfootleg_transform.translation(om2.MSpace.kWorld)

            jnt_rfoot_transform = om2.MFnTransform(jnt_rfoot)
            jnt_rfoot_transform.setTransformation(loc_rfoot_transform)

            jnt_fkrfoot_transform = om2.MFnTransform(jnt_fkrfoot)
            jnt_fkrfoot_transform.setTransformation(loc_rfoot_transform)

            jnt_ikrfoot_transform = om2.MFnTransform(jnt_ikrfoot)
            jnt_ikrfoot_transform.setTransformation(loc_rfoot_transform)

            rreversefoot_foot_transform = om2.MFnTransform(rreversefoot_foot)
            rreversefoot_foot_transform.setTranslation(loc_rfootleg_t, om2.MSpace.kTransform)

            rreverseinner_foot_transform = om2.MFnTransform(rreverseinner_foot)
            rreverseinner_foot_transform_t = rreverseinner_foot_transform.translation(om2.MSpace.kTransform)
            rreverseinner_foot_transform_t[0], rreverseinner_foot_transform_t[2], rreverseinner_foot_transform_t[2] = loc_rfootleg_t[0]*0.1, loc_rfootleg_t[1], loc_rfootleg_t[2]
            rreverseinner_foot_transform.setTranslation(rreverseinner_foot_transform_t, om2.MSpace.kTransform)

            rreverseouter_foot_transform = om2.MFnTransform(rreverseouter_foot)
            rreverseouter_foot_transform_t = rreverseouter_foot_transform.translation(om2.MSpace.kTransform)
            rreverseouter_foot_transform_t[0], rreverseouter_foot_transform_t[2], rreverseouter_foot_transform_t[2] = loc_rfootleg_t[0]*1.9, loc_rfootleg_t[1], loc_rfootleg_t[2]
            rreverseouter_foot_transform.setTranslation(rreverseouter_foot_transform_t, om2.MSpace.kTransform)

            jnt_rtoe = legjnt_grp.create("joint", "RightToeEnd", jnt_rfoot)
            jnt_fkrtoe = legjnt_grp.create("joint", "FkRightToeEnd", jnt_fkrfoot)
            jnt_ikrtoe = legjnt_grp.create("joint", "IkRightToeEnd", jnt_ikrfoot)
            rreversefoot_toe = legjnt_grp.create("transform", "RightReverseFootToeEnd")
            rreversefoot_toe_ln = legjnt_grp.create("locator", "RightReverseFootToeEndShape", rreversefoot_toe)
            rreversefoot_toewiggle = legjnt_grp.create("transform", "RightReverseFootToeWiggle", rreversefoot_toe)

            leg_loc_ls.add(leg_loc[9])
            rtoe_loc_obj = leg_loc_ls.getDependNode(4)
            rtoe_loc_transform = om2.MFnTransform(rtoe_loc_obj)
            loc_rtoe_transform = rtoe_loc_transform.transformation()

            rtoeleg_loc_path_n = om2.MDagPath()
            rtoeleg_loc_path = rtoeleg_loc_path_n.getAPathTo(rtoe_loc_obj)
            loc_rtoeleg_transform = om2.MFnTransform(rtoeleg_loc_path)
            loc_rtoeleg_t = loc_rtoeleg_transform.translation(om2.MSpace.kWorld)

            jnt_rtoe_transform = om2.MFnTransform(jnt_rtoe)
            jnt_rtoe_transform.setTransformation(loc_rtoe_transform)

            jnt_fkrtoe_transform = om2.MFnTransform(jnt_fkrtoe)
            jnt_fkrtoe_transform.setTransformation(loc_rtoe_transform)

            jnt_ikrtoe_transform = om2.MFnTransform(jnt_ikrtoe)
            jnt_ikrtoe_transform.setTransformation(loc_rtoe_transform)

            rreversefoot_toe_transform = om2.MFnTransform(rreversefoot_toe)
            rreversefoot_toe_transform.setTranslation(loc_rtoeleg_t, om2.MSpace.kTransform)

            rfoottoewiggle_path_n = om2.MDagPath()
            rfoottoewiggle_path = rfoottoewiggle_path_n.getAPathTo(rreversefoot_toewiggle)
            rfoottoewiggle_worldtransform = om2.MFnTransform(rfoottoewiggle_path)
            rfoottoewiggle_worldtransform.setRotatePivot(om2.MPoint(loc_rfootleg_t), om2.MSpace.kWorld, False)

            # grp_stretchyikrleg = legjnt_grp.create("transform", "IkStretchyRightJointLeg_grp", self.splineik_grp)
            #
            # grp_stretchyikrleg_transform = om2.MFnTransform(grp_stretchyikrleg)
            # grp_stretchyikrleg_transform.setTransformation(self.loc_root_transform)
            #
            # jnt_stretchyikrupperleg0 = legjnt_grp.create("joint", "IkSplineRightUpperLeg0", grp_stretchyikrleg)
            # jnt_stretchyikcvrupperleg0 = legjnt_grp.create("joint", "IkCvSplineRightUpperLeg0", self.rupperlegikcluster0_grp)
            #
            # jnt_stretchyikrupperleg0_transform = om2.MFnTransform(jnt_stretchyikrupperleg0)
            # jnt_stretchyikrupperleg0_transform.setTransformation(loc_rupperleg_transform)
            #
            # jnt_stretchyikcvrupperleg0_transform = om2.MFnTransform(self.rupperlegikcluster_grp)
            # jnt_stretchyikcvrupperleg0_transform.setTranslation(loc_rupperleg_t, om2.MSpace.kTransform)
            #
            # jnt_stretchyikrupperleg1 = legjnt_grp.create("joint", "IkSplineRightUpperLeg1", jnt_stretchyikrupperleg0)
            #
            # jnt_stretchyikrupperleg1_transform = om2.MFnTransform(jnt_stretchyikrupperleg1)
            # jnt_stretchyikrupperleg1_transform_t = jnt_stretchyikrupperleg1_transform.translation(om2.MSpace.kTransform)
            # jnt_stretchyikrupperleg1_transform_t[0], jnt_stretchyikrupperleg1_transform_t[1], jnt_stretchyikrupperleg1_transform_t[2] = loc_rknee_transform_t[0]/4, loc_rknee_transform_t[1]/4, loc_rknee_transform_t[2]/4
            # jnt_stretchyikrupperleg1_transform.setTranslation(jnt_stretchyikrupperleg1_transform_t, om2.MSpace.kTransform)
            #
            # jnt_stretchyikrupperleg2 = legjnt_grp.create("joint", "IkSplineRightUpperLeg2", jnt_stretchyikrupperleg1)
            # jnt_stretchyikcvlupperleg1 = legjnt_grp.create("joint", "IkCvSplineRightUpperLeg1", self.rupperlegikcluster1_grp)
            #
            # jnt_stretchyiklupperleg2_transform = om2.MFnTransform(jnt_stretchyikrupperleg2)
            # jnt_stretchyiklupperleg2_transform_t = jnt_stretchyiklupperleg2_transform.translation(om2.MSpace.kTransform)
            # jnt_stretchyiklupperleg2_transform_t[0], jnt_stretchyiklupperleg2_transform_t[1], jnt_stretchyiklupperleg2_transform_t[2] = loc_lknee_transform_t[0]/2, (loc_lknee_transform_t[1]/2)-jnt_stretchyikrupperleg1_transform_t[1], (loc_lknee_transform_t[2]/2)-jnt_stretchyikrupperleg1_transform_t[2]
            # jnt_stretchyiklupperleg2_transform.setTranslation(jnt_stretchyiklupperleg2_transform_t, om2.MSpace.kTransform)
            #
            # jnt_stretchyikcvlupperleg0_transform_t = jnt_stretchyikcvrupperleg0_transform.translation(om2.MSpace.kTransform)
            #
            # jnt_stretchyikcvlupperleg1grp_transform = om2.MFnTransform(self.rupperlegikcluster1_grp)
            # jnt_stretchyikcvlupperleg1grp_transform_t = jnt_stretchyikcvlupperleg1grp_transform.translation(om2.MSpace.kTransform)
            # jnt_stretchyikcvlupperleg1grp_transform_t[0], jnt_stretchyikcvlupperleg1grp_transform_t[1], jnt_stretchyikcvlupperleg1grp_transform_t[2] = -(jnt_stretchyikcvlupperleg0_transform_t[0]-loc_rkneeleg_t[0])/2, -(jnt_stretchyikcvlupperleg0_transform_t[1]-loc_rkneeleg_t[1])/2, -(jnt_stretchyikcvlupperleg0_transform_t[2]-loc_rkneeleg_t[2])/2 #loc_lkneeleg_t[0]+(loc_lupperleg_t[0]-loc_lkneeleg_t[0])/2, loc_lkneeleg_t[1]+(loc_lupperleg_t[1]-loc_lkneeleg_t[1])/2, loc_lkneeleg_t[2]+(loc_lupperleg_t[2]-loc_lkneeleg_t[2])/2
            # jnt_stretchyikcvlupperleg1grp_transform.setTranslation(jnt_stretchyikcvlupperleg1grp_transform_t, om2.MSpace.kTransform)
            #
            # jnt_stretchyiklupperleg3 = legjnt_grp.create("joint", "IkSplineLeftUpperLeg3", jnt_stretchyikrupperleg2)
            #
            # jnt_stretchyiklupperleg3_transform = om2.MFnTransform(jnt_stretchyiklupperleg3)
            # jnt_stretchyiklupperleg3_transform_t = jnt_stretchyiklupperleg3_transform.translation(om2.MSpace.kTransform)
            # jnt_stretchyiklupperleg3_transform_t[0], jnt_stretchyiklupperleg3_transform_t[1], jnt_stretchyiklupperleg3_transform_t[2] = jnt_stretchyiklupperleg2_transform_t[0], jnt_stretchyiklupperleg2_transform_t[1], jnt_stretchyiklupperleg2_transform_t[2]
            # jnt_stretchyiklupperleg3_transform.setTranslation(jnt_stretchyiklupperleg3_transform_t, om2.MSpace.kTransform)
            #
            # jnt_stretchyiklupperleg4 = legjnt_grp.create("joint", "IkSplineLeftUpperLeg4", jnt_stretchyiklupperleg3)
            # jnt_stretchyikcvlupperleg2 = legjnt_grp.create("joint", "IkCvSplineLeftUpperLeg2", self.rupperlegikcluster2_grp)
            #
            # jnt_stretchyiklupperleg4_transform = om2.MFnTransform(jnt_stretchyiklupperleg4)
            # jnt_stretchyiklupperleg4_transform_t = jnt_stretchyiklupperleg4_transform.translation(om2.MSpace.kTransform)
            # jnt_stretchyiklupperleg4_transform_t[0], jnt_stretchyiklupperleg4_transform_t[1], jnt_stretchyiklupperleg4_transform_t[2] = jnt_stretchyiklupperleg3_transform_t[0], jnt_stretchyiklupperleg3_transform_t[1], jnt_stretchyiklupperleg3_transform_t[2]
            # jnt_stretchyiklupperleg4_transform.setTranslation(jnt_stretchyiklupperleg4_transform_t, om2.MSpace.kTransform)
            #
            # jnt_stretchyikcvlupperleg2_transform = om2.MFnTransform(self.rupperlegikcluster2_grp)
            # jnt_stretchyikcvlupperleg2_transform_t = jnt_stretchyikcvlupperleg2_transform.translation(om2.MSpace.kTransform)
            # jnt_stretchyikcvlupperleg2_transform_t[0], jnt_stretchyikcvlupperleg2_transform_t[1], jnt_stretchyikcvlupperleg2_transform_t[2] = -(jnt_stretchyikcvlupperleg0_transform_t[0]-loc_rkneeleg_t[0]), -(jnt_stretchyikcvlupperleg0_transform_t[1]-loc_rkneeleg_t[1]), -(jnt_stretchyikcvlupperleg0_transform_t[2]-loc_rkneeleg_t[2]) #loc_lkneeleg_t[0], loc_lkneeleg_t[1], loc_lkneeleg_t[2]
            # jnt_stretchyikcvlupperleg2_transform.setTranslation(jnt_stretchyikcvlupperleg2_transform_t, om2.MSpace.kTransform)
            #
            # jnt_stretchyikllowerleg0 = legjnt_grp.create("joint", "IkSplineLeftLowerLeg0", grp_stretchyiklleg)
            # jnt_stretchyikcvllowerleg0 = legjnt_grp.create("joint", "IkCvSplineLeftLowerLeg0", self.rlowerlegikcluster0_grp)
            #
            # jnt_stretchyikllowerleg0_transform = om2.MFnTransform(jnt_stretchyikllowerleg0)
            # jnt_stretchyikllowerleg0_transform.setTranslation(loc_rkneeleg_t-grp_stretchyiklleg_transform.translation(om2.MSpace.kTransform), om2.MSpace.kTransform)
            #
            # jnt_stretchyikcvllowerleg0_transform = om2.MFnTransform(self.rlowerlegikcluster_grp)
            # jnt_stretchyikcvllowerleg0_transform.setTranslation(loc_rkneeleg_t, om2.MSpace.kTransform)
            #
            # jnt_stretchyikllowerleg1 = legjnt_grp.create("joint", "IkSplineLeftLowerLeg1", jnt_stretchyikllowerleg0)
            #
            # jnt_stretchyikllowerleg1_transform = om2.MFnTransform(jnt_stretchyikllowerleg1)
            # jnt_stretchyikllowerleg1_transform_t = jnt_stretchyikllowerleg1_transform.translation(om2.MSpace.kTransform)
            # jnt_stretchyikllowerleg1_transform_t[0], jnt_stretchyikllowerleg1_transform_t[1], jnt_stretchyikllowerleg1_transform_t[2] = loc_lfootball_t[0]/4, loc_lfootball_t[1]/4, loc_lfootball_t[2]/4
            # jnt_stretchyikllowerleg1_transform.setTranslation(jnt_stretchyikllowerleg1_transform_t, om2.MSpace.kTransform)
            #
            # jnt_stretchyikllowerleg2 = legjnt_grp.create("joint", "IkSplineLeftLowerLeg2", jnt_stretchyikllowerleg1)
            # jnt_stretchyikvcvllowerleg1 = legjnt_grp.create("joint", "IkCvSplineLeftLowerLeg1", self.rlowerlegikcluster1_grp)
            #
            # jnt_stretchyikllowerleg2_transform = om2.MFnTransform(jnt_stretchyikllowerleg2)
            # jnt_stretchyikllowerleg2_transform_t = jnt_stretchyikllowerleg2_transform.translation(om2.MSpace.kTransform)
            # jnt_stretchyikllowerleg2_transform_t[0], jnt_stretchyikllowerleg2_transform_t[1], jnt_stretchyikllowerleg2_transform_t[2] = (loc_lfootball_t[0]/2)-jnt_stretchyikllowerleg1_transform_t[0], (loc_lfootball_t[1]/2)-jnt_stretchyikllowerleg1_transform_t[1], (loc_lfootball_t[2]/2)-jnt_stretchyikllowerleg1_transform_t[2]
            # jnt_stretchyikllowerleg2_transform.setTranslation(jnt_stretchyikllowerleg2_transform_t, om2.MSpace.kTransform)
            #
            # jnt_stretchyikcvllowerleg0_transform_t = jnt_stretchyikcvllowerleg0_transform.translation(om2.MSpace.kTransform)
            #
            # jnt_stretchyikcvllowerleg1_transform = om2.MFnTransform(self.rlowerlegikcluster1_grp)
            # jnt_stretchyikcvllowerleg1_transform_t = jnt_stretchyikcvllowerleg1_transform.translation(om2.MSpace.kTransform)
            # jnt_stretchyikcvllowerleg1_transform_t[0], jnt_stretchyikcvllowerleg1_transform_t[1], jnt_stretchyikcvllowerleg1_transform_t[2] = -(jnt_stretchyikcvllowerleg0_transform_t[0]-loc_rfootballleg_t[0])/2, -(jnt_stretchyikcvllowerleg0_transform_t[1]-loc_rfootballleg_t[1])/2, -(jnt_stretchyikcvllowerleg0_transform_t[2]-loc_rfootballleg_t[2])/2 #loc_lfootballleg_t[0]+((loc_lkneeleg_t[0]-loc_lfootballleg_t[0])/2), loc_lfootballleg_t[1]+((loc_lkneeleg_t[1]-loc_lfootballleg_t[1])/2), loc_lfootballleg_t[2]+((loc_lkneeleg_t[2]-loc_lfootballleg_t[2])/2)
            # jnt_stretchyikcvllowerleg1_transform.setTranslation(jnt_stretchyikcvllowerleg1_transform_t, om2.MSpace.kTransform)
            #
            # jnt_stretchyikllowerleg3 = legjnt_grp.create("joint", "IkSplineLeftLowerLeg3", jnt_stretchyikllowerleg2)
            #
            # jnt_stretchyikllowerleg3_transform = om2.MFnTransform(jnt_stretchyikllowerleg3)
            # jnt_stretchyikllowerleg3_transform_t = jnt_stretchyikllowerleg3_transform.translation(om2.MSpace.kTransform)
            # jnt_stretchyikllowerleg3_transform_t[0], jnt_stretchyikllowerleg3_transform_t[1], jnt_stretchyikllowerleg3_transform_t[2] = jnt_stretchyikllowerleg2_transform_t[0], jnt_stretchyikllowerleg2_transform_t[1], jnt_stretchyikllowerleg2_transform_t[2]
            # jnt_stretchyikllowerleg3_transform.setTranslation(jnt_stretchyikllowerleg3_transform_t, om2.MSpace.kTransform)
            #
            # jnt_stretchyikllowerleg4 = legjnt_grp.create("joint", "IkSplineLeftLowerLeg4", jnt_stretchyikllowerleg3)
            # jnt_stretchyikvcvllowerleg2 = legjnt_grp.create("joint", "IkCvSplineLeftLowerLeg2", self.rlowerlegikcluster2_grp)
            #
            # jnt_stretchyikllowerleg4_transform = om2.MFnTransform(jnt_stretchyikllowerleg4)
            # jnt_stretchyikllowerleg4_transform_t = jnt_stretchyikllowerleg4_transform.translation(om2.MSpace.kTransform)
            # jnt_stretchyikllowerleg4_transform_t[0], jnt_stretchyikllowerleg4_transform_t[1], jnt_stretchyikllowerleg4_transform_t[2] = jnt_stretchyikllowerleg3_transform_t[0], jnt_stretchyikllowerleg3_transform_t[1], jnt_stretchyikllowerleg3_transform_t[2]
            # jnt_stretchyikllowerleg4_transform.setTranslation(jnt_stretchyikllowerleg4_transform_t, om2.MSpace.kTransform)
            #
            # jnt_stretchyikcvllowerleg4_transform = om2.MFnTransform(self.rlowerlegikcluster2_grp)
            # jnt_stretchyikcvllowerleg4_transform_t = jnt_stretchyikcvllowerleg4_transform.translation(om2.MSpace.kTransform)
            # jnt_stretchyikcvllowerleg4_transform_t[0], jnt_stretchyikcvllowerleg4_transform_t[1], jnt_stretchyikcvllowerleg4_transform_t[2] = -(jnt_stretchyikcvllowerleg0_transform_t[0]-loc_rfootballleg_t[0]), -(jnt_stretchyikcvllowerleg0_transform_t[1]-loc_rfootballleg_t[1]), -(jnt_stretchyikcvllowerleg0_transform_t[2]-loc_rfootballleg_t[2]) #loc_lfootballleg_t[0], loc_lfootballleg_t[1], loc_lfootballleg_t[2]
            # jnt_stretchyikcvllowerleg4_transform.setTranslation(jnt_stretchyikcvllowerleg4_transform_t, om2.MSpace.kTransform)

    def setJointOrientation(self):
        dg_modifier = om2.MDGModifier()
        dg_n = om2.MFnDagNode()
        dg_transform = om2.MFnTransform()

        hipjoint_sl_lst = om2.MSelectionList()
        hipjoint_sl_lst.add("Hip")

        spinejoint_sl_lst = om2.MSelectionList()
        spinejoint_sl_lst.add("Spine*")

        jnt_lastspine_obj = spinejoint_sl_lst.getDependNode(spinejoint_sl_lst.length()-1)

        ikspinejoint_sl_lst = om2.MSelectionList()
        ikspinejoint_sl_lst.add("IkSpine*")

        jnt_iklastspine_obj = ikspinejoint_sl_lst.getDependNode(ikspinejoint_sl_lst.length()-1)

        lhandjoint_sl_lst = om2.MSelectionList()
        lhandjoint_sl_lst.add("LeftShoulder*")
        lhandjoint_sl_lst.add("LeftArm*")
        lhandjoint_sl_lst.add("LeftForeArm*")
        lhandjoint_sl_lst.add("LeftHand")

        jnt_lshoulder_obj = lhandjoint_sl_lst.getDependNode(0)
        jnt_lhand_obj = lhandjoint_sl_lst.getDependNode(lhandjoint_sl_lst.length()-1)

        fklhandjoint_sl_lst = om2.MSelectionList()
        fklhandjoint_sl_lst.add("LeftShoulder*")
        fklhandjoint_sl_lst.add("FkLeftArm*")
        fklhandjoint_sl_lst.add("FkLeftForeArm*")
        fklhandjoint_sl_lst.add("FkLeftHand")

        jnt_fklhand_obj = fklhandjoint_sl_lst.getDependNode(fklhandjoint_sl_lst.length()-1)

        iklhandjoint_sl_lst = om2.MSelectionList()
        iklhandjoint_sl_lst.add("LeftShoulder*")
        iklhandjoint_sl_lst.add("IkLeftArm*")
        iklhandjoint_sl_lst.add("IkLeftForeArm*")
        iklhandjoint_sl_lst.add("IkLeftHand")

        jnt_iklhand_obj = iklhandjoint_sl_lst.getDependNode(iklhandjoint_sl_lst.length()-1)

        lfingerjoint_sl_lst = om2.MSelectionList()
        lfingerjoint_sl_lst.add("LeftFinger*")

        rhandjoint_sl_lst = om2.MSelectionList()
        rhandjoint_sl_lst.add("RightShoulder*")
        rhandjoint_sl_lst.add("RightArm*")
        rhandjoint_sl_lst.add("RightForeArm*")
        rhandjoint_sl_lst.add("RightHand")

        jnt_rshoulder_obj = rhandjoint_sl_lst.getDependNode(0)
        jnt_rhand_obj = rhandjoint_sl_lst.getDependNode(rhandjoint_sl_lst.length()-1)

        fkrhandjoint_sl_lst = om2.MSelectionList()
        fkrhandjoint_sl_lst.add("RightShoulder*")
        fkrhandjoint_sl_lst.add("FkRightArm*")
        fkrhandjoint_sl_lst.add("FkRightForeArm*")
        fkrhandjoint_sl_lst.add("FkRightHand")

        jnt_fkrhand_obj = fkrhandjoint_sl_lst.getDependNode(fkrhandjoint_sl_lst.length()-1)

        ikrhandjoint_sl_lst = om2.MSelectionList()
        ikrhandjoint_sl_lst.add("RightShoulder*")
        ikrhandjoint_sl_lst.add("IkRightArm*")
        ikrhandjoint_sl_lst.add("IkRightForeArm*")
        ikrhandjoint_sl_lst.add("IkRightHand")

        jnt_ikrhand_obj = ikrhandjoint_sl_lst.getDependNode(ikrhandjoint_sl_lst.length()-1)

        rfingerjoint_sl_lst = om2.MSelectionList()
        rfingerjoint_sl_lst.add("RightFinger*")

        legjoint_sl_lst = om2.MSelectionList()
        legjoint_sl_lst.add("LeftUpLeg*")
        legjoint_sl_lst.add("LeftFoot*")
        legjoint_sl_lst.add("LeftToeBase*")
        legjoint_sl_lst.add("LeftToeEnd*")
        legjoint_sl_lst.add("RightUpLeg*")
        legjoint_sl_lst.add("RightFoot*")
        legjoint_sl_lst.add("RightToeBase*")
        legjoint_sl_lst.add("RightToeEnd*")
        legjoint_sl_lst.add("FkLeftUpLeg*")
        legjoint_sl_lst.add("FkLeftFoot*")
        legjoint_sl_lst.add("FkLeftToeBase*")
        legjoint_sl_lst.add("FkLeftToeEnd*")
        legjoint_sl_lst.add("FkRightUpLeg*")
        legjoint_sl_lst.add("FkRightFoot*")
        legjoint_sl_lst.add("FkRightToeBase*")
        legjoint_sl_lst.add("FkRightToeEnd*")
        legjoint_sl_lst.add("IkLeftUpLeg*")
        legjoint_sl_lst.add("IkLeftFoot*")
        legjoint_sl_lst.add("IkLeftToeBase*")
        legjoint_sl_lst.add("IkLeftToeEnd*")
        legjoint_sl_lst.add("IkRightUpLeg*")
        legjoint_sl_lst.add("IkRightFoot*")
        legjoint_sl_lst.add("IkRightToeBase*")
        legjoint_sl_lst.add("IkRightToeEnd*")
        legjoint_sl_lst.add("IkNoFlipLeftUpLeg*")
        legjoint_sl_lst.add("IkNoFlipLeftFoot*")
        legjoint_sl_lst.add("IkPVLeftUpLeg*")
        legjoint_sl_lst.add("IkPVLeftFoot*")

        llegupperikjoint_sl_lst = om2.MSelectionList()
        llegupperikjoint_sl_lst.add("IkSplineLeftUpperLeg*")

        lleglowerikjoint_sl_lst = om2.MSelectionList()
        lleglowerikjoint_sl_lst.add("IkSplineLeftLowerLeg*")

        legjointknee_sl_lst = om2.MSelectionList()
        legjointknee_sl_lst.add("LeftLeg*")
        legjointknee_sl_lst.add("RightLeg*")
        legjointknee_sl_lst.add("FkLeftLeg*")
        legjointknee_sl_lst.add("FkRightLeg*")
        legjointknee_sl_lst.add("IkLeftLeg*")
        legjointknee_sl_lst.add("IkRightLeg*")
        legjointknee_sl_lst.add("IkNoFlipLeftLeg*")
        legjointknee_sl_lst.add("IkPVLeftLeg*")

        endjoint_sl_lst = om2.MSelectionList()
        endjoint_sl_lst.add("*End")
        endjoint_sl_lst.add("RightFinger*4")
        endjoint_sl_lst.add("LeftFinger*4")
        endjoint_sl_lst.add("IkSplineLeftLowerLeg4")
        endjoint_sl_lst.add(jnt_iklastspine_obj)

        spineikjoint_sl_lst = om2.MSelectionList()
        spineikjoint_sl_lst.add("IkCvHip")
        spineikjoint_sl_lst.add("IkCvSpine")

        neckikjoint_sl_lst = om2.MSelectionList()
        neckikjoint_sl_lst.add("IkNeck1")
        neckikjoint_sl_lst.add("IkNeck2")

        if self.typeofJointOrient.currentIndex() == 0:
            for index in range(spinejoint_sl_lst.length()):
                dg_n.setObject(jnt_lastspine_obj)
                dg_n.removeChild(jnt_lshoulder_obj)
                dg_n.removeChild(jnt_rshoulder_obj)

                dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient yup -zeroScaleOrient Spine{0}'.format(index))
                if index == spinejoint_sl_lst.length()-1:
                    lastspine_r = cmds.xform("Spine{0}".format(index), query=True, rotation=True, worldSpace=True)

                    cmds.setAttr("IkCvSpine.jointOrientX", lastspine_r[0])
                    cmds.setAttr("IkCvSpine.jointOrientY", lastspine_r[1])
                    cmds.setAttr("IkCvSpine.jointOrientZ", lastspine_r[2])

                dg_n.addChild(jnt_lshoulder_obj)
                dg_n.addChild(jnt_rshoulder_obj)

            for index in range(neckikjoint_sl_lst.length()):
                dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient yup -zeroScaleOrient IkNeck{0}'.format(index+1))

            for index in range(ikspinejoint_sl_lst.length()):
                dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient yup -zeroScaleOrient IkSpine{0}'.format(index))

            for index in range(lfingerjoint_sl_lst.length()-1):
                dg_n.setObject(jnt_lhand_obj)

                if index%4 == 0:
                    jnt_lparentfinger_obj = lfingerjoint_sl_lst.getDependNode(index)
                    dg_n.removeChild(jnt_lparentfinger_obj)

            dg_n.create("joint", "lnull", jnt_lhand_obj)
            dg_n.create("joint", "fklnull", jnt_fklhand_obj)
            dg_n.create("joint", "iklnull", jnt_iklhand_obj)
            for index in range(lhandjoint_sl_lst.length()):
                jnt_active_string = lhandjoint_sl_lst.getSelectionStrings(index)
                fkjnt_active_string = fklhandjoint_sl_lst.getSelectionStrings(index)
                ikjnt_active_string = iklhandjoint_sl_lst.getSelectionStrings(index)
                dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(jnt_active_string)[3:][:-3]))
                dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(fkjnt_active_string)[3:][:-3]))
                dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(ikjnt_active_string)[3:][:-3]))

            for index in range(lfingerjoint_sl_lst.length()-1):
                dg_n.setObject(jnt_lhand_obj)

                if index%4 == 0:
                        jnt_lparentfinger_obj = lfingerjoint_sl_lst.getDependNode(index)
                        dg_n.addChild(jnt_lparentfinger_obj)

            for index in range(lfingerjoint_sl_lst.length()):
                jnt_active_string = lfingerjoint_sl_lst.getSelectionStrings(index)
                dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(jnt_active_string)[3:][:-3]))

            for index in range(rfingerjoint_sl_lst.length()-1):
                dg_n.setObject(jnt_rhand_obj)

                if index%4 == 0:
                    jnt_rparentfinger_obj = rfingerjoint_sl_lst.getDependNode(index)
                    dg_n.removeChild(jnt_rparentfinger_obj)

            dg_n.create("joint", "rnull", jnt_rhand_obj)
            dg_n.create("joint", "fkrnull", jnt_fkrhand_obj)
            dg_n.create("joint", "ikrnull", jnt_ikrhand_obj)
            for index in range(rhandjoint_sl_lst.length()):
                jnt_active_string = rhandjoint_sl_lst.getSelectionStrings(index)
                fkjnt_active_string = fkrhandjoint_sl_lst.getSelectionStrings(index)
                ikjnt_active_string = ikrhandjoint_sl_lst.getSelectionStrings(index)
                dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(jnt_active_string)[3:][:-3]))
                dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(fkjnt_active_string)[3:][:-3]))
                dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(ikjnt_active_string)[3:][:-3]))

            for index in range(rfingerjoint_sl_lst.length()-1):
                dg_n.setObject(jnt_rhand_obj)

                if index%4 == 0:
                        jnt_rparentfinger_obj = rfingerjoint_sl_lst.getDependNode(index)
                        dg_n.addChild(jnt_rparentfinger_obj)

            for index in range(rfingerjoint_sl_lst.length()):
                jnt_active_string = rfingerjoint_sl_lst.getSelectionStrings(index)
                dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(jnt_active_string)[3:][:-3]))

            for index in range(legjoint_sl_lst.length()):
                jnt_active_obj = legjoint_sl_lst.getDependNode(index)
                if jnt_active_obj.hasFn(om2.MFn.kJoint):
                    jnt_active_string = legjoint_sl_lst.getSelectionStrings(index)
                    dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient yup -zeroScaleOrient {0}'.format(str(jnt_active_string)[3:][:-3]))

            for index in range(llegupperikjoint_sl_lst.length()):
                jnt_active_obj = llegupperikjoint_sl_lst.getDependNode(index)
                if jnt_active_obj.hasFn(om2.MFn.kJoint):
                    jnt_active_string = llegupperikjoint_sl_lst.getSelectionStrings(index)
                    dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient yup -zeroScaleOrient {0}'.format(str(jnt_active_string)[3:][:-3]))

            for index in range(lleglowerikjoint_sl_lst.length()):
                jnt_active_obj = lleglowerikjoint_sl_lst.getDependNode(index)
                if jnt_active_obj.hasFn(om2.MFn.kJoint):
                    jnt_active_string = lleglowerikjoint_sl_lst.getSelectionStrings(index)
                    dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(jnt_active_string)[3:][:-3]))

            for index in range(legjointknee_sl_lst.length()):
                jnt_active_obj = legjointknee_sl_lst.getDependNode(index)
                if jnt_active_obj.hasFn(om2.MFn.kJoint):
                    jnt_active_string = legjointknee_sl_lst.getSelectionStrings(index)
                    dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(jnt_active_string)[3:][:-3]))

            for index in range(endjoint_sl_lst.length()):
                jnt_end_obj = endjoint_sl_lst.getDependNode(index)
                if jnt_end_obj.hasFn(om2.MFn.kJoint):
                    dg_transform.setObject(jnt_end_obj)
                    endjoint_orient_plug = dg_transform.findPlug("jointOrient", False)

                    if endjoint_orient_plug.isCompound:
                        for i in range(endjoint_orient_plug.numChildren()):
                             child_plug = endjoint_orient_plug.child(i)
                             attr_value = child_plug.setDouble(0)

            dg_modifier.commandToExecute('delete "lnull"')
            dg_modifier.commandToExecute('delete "fklnull"')
            dg_modifier.commandToExecute('delete "iklnull"')
            dg_modifier.commandToExecute('delete "rnull"')
            dg_modifier.commandToExecute('delete "fkrnull"')
            dg_modifier.commandToExecute('delete "ikrnull"')
            dg_modifier.doIt()

            leftupperlegikcluster_r = cmds.xform("LeftUpLeg", query=True, rotation=True, worldSpace=True)

            try:
                cmds.parent("LeftUpperLegIkCluster1_grp", world=True)
                cmds.parent("LeftUpperLegIkCluster2_grp", world=True)
            except:
                pass

            cmds.setAttr("LeftUpperLegIkCluster_grp.rotateX", leftupperlegikcluster_r[0])
            cmds.setAttr("LeftUpperLegIkCluster_grp.rotateY", leftupperlegikcluster_r[1])
            cmds.setAttr("LeftUpperLegIkCluster_grp.rotateZ", leftupperlegikcluster_r[2])

            try:
                cmds.parent("LeftUpperLegIkCluster1_grp", "LeftUpperLegIkCluster_grp")
                cmds.parent("LeftUpperLegIkCluster2_grp", "LeftUpperLegIkCluster_grp")
            except:
                pass

            cmds.setAttr("LeftUpperLegIkCluster1_grp.rotateX", 0)
            cmds.setAttr("LeftUpperLegIkCluster1_grp.rotateY", 0)
            cmds.setAttr("LeftUpperLegIkCluster1_grp.rotateZ", 0)

            ikcvsplineleftupperleg2_rx = cmds.getAttr("LeftLeg.jointOrientX")
            ikcvsplineleftupperleg2_ry = cmds.getAttr("LeftLeg.jointOrientY")
            ikcvsplineleftupperleg2_rz = cmds.getAttr("LeftLeg.jointOrientZ")
            cmds.setAttr("LeftUpperLegIkCluster2_grp.rotateX", ikcvsplineleftupperleg2_rx)
            cmds.setAttr("LeftUpperLegIkCluster2_grp.rotateY", ikcvsplineleftupperleg2_ry)
            cmds.setAttr("LeftUpperLegIkCluster2_grp.rotateZ", ikcvsplineleftupperleg2_rz)
            cmds.setAttr("IkSplineLeftUpperLeg4.jointOrientX", 0)
            cmds.setAttr("IkSplineLeftUpperLeg4.jointOrientY", 0)
            cmds.setAttr("IkSplineLeftUpperLeg4.jointOrientZ", 0)

            leftlowerlegikcluster_r = cmds.xform("LeftLeg", query=True, rotation=True, worldSpace=True)

            try:
                cmds.parent("LeftLowerLegIkCluster1_grp", world=True)
                cmds.parent("LeftLowerLegIkCluster2_grp", world=True)
            except:
                pass

            cmds.setAttr("LeftLowerLegIkCluster_grp.rotateX", leftlowerlegikcluster_r[0])
            cmds.setAttr("LeftLowerLegIkCluster_grp.rotateY", leftlowerlegikcluster_r[1])
            cmds.setAttr("LeftLowerLegIkCluster_grp.rotateZ", leftlowerlegikcluster_r[2])

            try:
                cmds.parent("LeftLowerLegIkCluster1_grp", "LeftLowerLegIkCluster_grp")
                cmds.parent("LeftLowerLegIkCluster2_grp", "LeftLowerLegIkCluster_grp")
            except:
                pass

            cmds.setAttr("LeftLowerLegIkCluster1_grp.rotateX", 0)
            cmds.setAttr("LeftLowerLegIkCluster1_grp.rotateY", 0)
            cmds.setAttr("LeftLowerLegIkCluster1_grp.rotateZ", 0)

            ikcvsplineleftlowerleg2_rx = cmds.getAttr("LeftFoot.jointOrientX")
            ikcvsplineleftlowerleg2_ry = cmds.getAttr("LeftFoot.jointOrientY")
            ikcvsplineleftlowerleg2_rz = cmds.getAttr("LeftFoot.jointOrientZ")
            cmds.setAttr("LeftLowerLegIkCluster2_grp.rotateX", ikcvsplineleftlowerleg2_rx)
            cmds.setAttr("LeftLowerLegIkCluster2_grp.rotateY", ikcvsplineleftlowerleg2_ry)
            cmds.setAttr("LeftLowerLegIkCluster2_grp.rotateZ", ikcvsplineleftlowerleg2_rz)
            cmds.setAttr("IkNoFlipLeftFoot.jointOrientX", ikcvsplineleftlowerleg2_rx)
            cmds.setAttr("IkNoFlipLeftFoot.jointOrientY", ikcvsplineleftlowerleg2_ry)
            cmds.setAttr("IkNoFlipLeftFoot.jointOrientZ", ikcvsplineleftlowerleg2_rz)
            cmds.setAttr("IkPVLeftFoot.jointOrientX", ikcvsplineleftlowerleg2_rx)
            cmds.setAttr("IkPVLeftFoot.jointOrientY", ikcvsplineleftlowerleg2_ry)
            cmds.setAttr("IkPVLeftFoot.jointOrientZ", ikcvsplineleftlowerleg2_rz)
            cmds.setAttr("IkSplineLeftLowerLeg4.jointOrientX", 0)
            cmds.setAttr("IkSplineLeftLowerLeg4.jointOrientY", 0)
            cmds.setAttr("IkSplineLeftLowerLeg4.jointOrientZ", 0)


        elif self.typeofJointOrient.currentIndex() == 1:
            for index in range(hipjoint_sl_lst.length()):
                jnt_active_string = hipjoint_sl_lst.getSelectionStrings(index)
                dg_modifier.commandToExecute('joint -e -orientJoint none -children -zeroScaleOrient {0}'.format(str(jnt_active_string)[3:][:-3]))

            dg_modifier.doIt()

    def insertJoint(self):
        jnt_extra_n = om2.MFnDagNode()
        jnt_active_sl_ls = om2.MGlobal.getActiveSelectionList()

        for index in range(jnt_active_sl_ls.length()):
            jnt_active_obj = jnt_active_sl_ls.getDependNode(index)
            jnt_active_string = jnt_active_sl_ls.getSelectionStrings(index)

            jnt_sl = om2.MFnDagNode(jnt_active_obj)
            jnt_child = jnt_sl.child(0)

            jnt_extra_tn = jnt_extra_n.create("joint", str(jnt_active_string)[2:][:-3]+"Extras"+str(index), jnt_active_obj)

            jnt_child_transform = om2.MFnTransform(jnt_child)
            jnt_child_transform_t = jnt_child_transform.translation(om2.MSpace.kTransform)

            jnt_extra_transform = om2.MFnTransform(jnt_extra_tn)
            jnt_extra_transform_t = jnt_extra_transform.translation(om2.MSpace.kTransform)
            jnt_extra_transform_t[0], jnt_extra_transform_t[1], jnt_extra_transform_t[2] = jnt_child_transform_t[0]/2, jnt_child_transform_t[1]/2, jnt_child_transform_t[2]/2
            jnt_extra_transform.setTranslation(jnt_extra_transform_t, om2.MSpace.kTransform)

            jnt_child_transform_t[0], jnt_child_transform_t[1], jnt_child_transform_t[2] = jnt_child_transform_t[0]-jnt_extra_transform_t[0], jnt_child_transform_t[1]-jnt_extra_transform_t[1], jnt_child_transform_t[2]-jnt_extra_transform_t[2]
            jnt_child_transform.setTranslation(jnt_child_transform_t, om2.MSpace.kTransform)

            jnt_parentextra_n = om2.MFnDagNode(jnt_extra_tn)
            jnt_parentextra_n.addChild(jnt_child)

    def deleteJoints(self):
        cmds.delete("Biped_jnt_grp")

    def createLHandIK(self, index):
        iksolver_lst = om1.MSelectionList()
        dag_n = om1.MFnDagNode()
        dg_modifier = om1.MDGModifier()

        obj_arm = om1.MObject()
        obj_wrist = om1.MObject()

        larm_sl_lst = om1.MSelectionList()
        larm_sl_lst.add("IkLeftArm*")
        larm_sl_lst.add("IkLeftHand")
        larm_sl_lst.getDependNode(0, obj_arm)
        larm_sl_lst.getDependNode(larm_sl_lst.length()-1, obj_wrist)

        lhand_pathnode = om1.MDagPath()
        lupperarm_path = lhand_pathnode.getAPathTo(obj_arm)

        ik_system = omanim1.MIkSystem()

        try:
            if cmds.objExists("LeftHand_Ik") and cmds.objExists("LeftHand_effector"):

                cmds.delete("LeftHand_Ik")
        except:
            pass

        if index == 0 :

            try:
                cmds.delete("LeftHand_effector")
            except:
                pass

            print("All Ik Removed")

        elif index == 1 :

            try:
                iksolver_lst.add("ikRPsolver*")
            except:
                cmds.createNode("ikRPsolver")

            rp_solver = ik_system.findSolver("ikRPsolver")

            ik_effector = omanim1.MFnIkEffector()
            self.lhand_effector = ik_effector.create(obj_wrist)
            lhand_effector_path = lhand_pathnode.getAPathTo(self.lhand_effector)

            ik_handle = omanim1.MFnIkHandle()
            self.l_hand_ik = ik_handle.create(lupperarm_path, lhand_effector_path)
            ik_handle.setSolver(rp_solver)

            dg_modifier.renameNode(self.l_hand_ik, "LeftHand_Ik")
            dg_modifier.renameNode(self.lhand_effector, "LeftHand_effector")
            dg_modifier.commandToExecute('parent LeftHand_effector IkLeftForeArm')
            dg_modifier.commandToExecute('parent LeftHand_Ik DoNotTouch')
            dg_modifier.doIt()

    def createRHandIK(self, index):
        iksolver_lst = om1.MSelectionList()
        dag_n = om1.MFnDagNode()
        dg_modifier = om1.MDGModifier()

        obj_arm = om1.MObject()
        obj_wrist = om1.MObject()

        rarm_sl_lst = om1.MSelectionList()
        rarm_sl_lst.add("IkRightArm*")
        rarm_sl_lst.add("IkRightHand")
        rarm_sl_lst.getDependNode(0, obj_arm)
        rarm_sl_lst.getDependNode(rarm_sl_lst.length()-1, obj_wrist)

        rhand_pathnode = om1.MDagPath()
        rupperarm_path = rhand_pathnode.getAPathTo(obj_arm)

        ik_system = omanim1.MIkSystem()

        try:
            if cmds.objExists("RightHand_Ik") and cmds.objExists("RightHand_effector"):

                cmds.delete("RightHand_Ik")
        except:
            pass

        if index == 0 :

            try:
                cmds.delete("RightHand_effector")
            except:
                pass

            print("All Ik Removed")

        elif index == 1 :

            try:
                iksolver_lst.add("ikRPsolver*")
            except:
                cmds.createNode("ikRPsolver")

            rp_solver = ik_system.findSolver("ikRPsolver")

            ik_effector = omanim1.MFnIkEffector()
            self.rhand_effector = ik_effector.create(obj_wrist)
            rhand_effector_path = rhand_pathnode.getAPathTo(self.rhand_effector)

            ik_handle = omanim1.MFnIkHandle()
            self.r_hand_ik = ik_handle.create(rupperarm_path, rhand_effector_path)
            ik_handle.setSolver(rp_solver)

            dg_modifier.renameNode(self.r_hand_ik, "RightHand_Ik")
            dg_modifier.renameNode(self.rhand_effector, "RightHand_effector")
            dg_modifier.commandToExecute('parent RightHand_effector IkRightForeArm')
            dg_modifier.commandToExecute('parent RightHand_Ik DoNotTouch')
            dg_modifier.doIt()

    def createLlegIk(self, index):
        iksolver_lst = om1.MSelectionList()
        dg_modifier = om1.MDGModifier()

        obj_upleg = om1.MObject()
        obj_foot = om1.MObject()
        obj_toe = om1.MObject()
        obj_toeend = om1.MObject()
        obj_noflipupleg = om1.MObject()
        obj_noflipfoot = om1.MObject()
        obj_pvupleg = om1.MObject()
        obj_pvfoot = om1.MObject()

        lleg_sl_lst = om1.MSelectionList()
        lleg_sl_lst.add("IkLeftFoot")
        lleg_sl_lst.add("IkLeftToeBase")
        lleg_sl_lst.add("IkLeftToeEnd")
        lleg_sl_lst.getDependNode(0, obj_foot)
        lleg_sl_lst.getDependNode(1, obj_toe)
        lleg_sl_lst.getDependNode(lleg_sl_lst.length()-1, obj_toeend)

        nofliplleg_sl_lst = om1.MSelectionList()
        nofliplleg_sl_lst.add("IkNoFlipLeftUpLeg")
        nofliplleg_sl_lst.add("IkNoFlipLeftFoot")
        nofliplleg_sl_lst.getDependNode(0, obj_noflipupleg)
        nofliplleg_sl_lst.getDependNode(1, obj_noflipfoot)

        pvlleg_sl_lst = om1.MSelectionList()
        pvlleg_sl_lst.add("IkPVLeftUpLeg")
        pvlleg_sl_lst.add("IkPVLeftFoot")
        pvlleg_sl_lst.getDependNode(0, obj_pvupleg)
        pvlleg_sl_lst.getDependNode(1, obj_pvfoot)

        lleg_pathnode = om1.MDagPath()
        nofliplupleg_path = lleg_pathnode.getAPathTo(obj_noflipupleg)
        pvlupleg_path = lleg_pathnode.getAPathTo(obj_pvupleg)
        llegfoot_path = lleg_pathnode.getAPathTo(obj_foot)
        llegtoe_path = lleg_pathnode.getAPathTo(obj_toe)

        ik_system = omanim1.MIkSystem()

        try:
            if cmds.objExists("NoFlipLeftLeg_Ik") and cmds.objExists("NoFlipLeftLeg_effector"):

                cmds.delete("NoFlipLeftLeg_Ik")
                cmds.delete("PVLeftLeg_Ik")
                cmds.delete("LeftLegFoot_Ik")
                cmds.delete("LeftLegToe_Ik")
        except:
            pass

        if index == 0 :
            try:
                cmds.delete("NoFlipLeftLeg_effector")
                cmds.delete("PVLeftLeg_effector")
            except:
                pass

            print("All Ik Removed")

        elif index == 1:
            try:
                iksolver_lst.add("ikRPsolver*")
            except:
                cmds.createNode("ikRPsolver")

            rp_solver = ik_system.findSolver("ikRPsolver")

            ik_effector = omanim1.MFnIkEffector()
            self.llegtoe_effector = ik_effector.create(obj_toe)
            llegtoe_effector_path = lleg_pathnode.getAPathTo(self.llegtoe_effector)

            self.llegtoeend_effector = ik_effector.create(obj_toeend)
            llegtoeend_effector_path = lleg_pathnode.getAPathTo(self.llegtoeend_effector)

            # self.noflipllegfoot_effector = ik_effector.create(obj_noflipfoot)
            # noflipllegfoot_effector_path = lleg_pathnode.getAPathTo(self.noflipllegfoot_effector)

            # self.pvllegfoot_effector = ik_effector.create(obj_pvfoot)
            # pvllegfoot_effector_path = lleg_pathnode.getAPathTo(self.pvllegfoot_effector)

            ik_handlelegtoe = omanim1.MFnIkHandle()
            self.llegtoe_ik = ik_handlelegtoe.create(llegfoot_path, llegtoe_effector_path)
            ik_handlelegtoe.setSolver(rp_solver)

            ik_handlelegtoeend = omanim1.MFnIkHandle()
            self.llegtoeend_ik = ik_handlelegtoeend.create(llegtoe_path, llegtoeend_effector_path)
            ik_handlelegtoeend.setSolver(rp_solver)

            # ik_handlenoflipleg = omanim1.MFnIkHandle()
            # self.noflipllegfoot_ik = ik_handlenoflipleg.create(nofliplupleg_path, noflipllegfoot_effector_path)
            # ik_handlenoflipleg.setSolver(rp_solver)

            # ik_handlepvleg = omanim1.MFnIkHandle()
            # self.pvllegfoot_ik = ik_handlepvleg.create(pvlupleg_path, pvllegfoot_effector_path)
            # ik_handlepvleg.setSolver(rp_solver)

            # dg_modifier.renameNode(self.noflipllegfoot_ik, "NoFlipLeftLeg_Ik")
            # dg_modifier.renameNode(self.pvllegfoot_ik, "PVLeftLeg_Ik")
            dg_modifier.renameNode(self.llegtoe_ik, "LeftLegFoot_Ik")
            dg_modifier.renameNode(self.llegtoeend_ik, "LeftLegToe_Ik")
            # dg_modifier.renameNode(self.noflipllegfoot_effector, "NoFlipLeftLeg_effector")
            # dg_modifier.renameNode(self.pvllegfoot_effector, "PVLeftLeg_effector")
            dg_modifier.renameNode(self.llegtoe_effector, "LeftFoot_effector")
            dg_modifier.renameNode(self.llegtoeend_effector, "LeftToe_effector")
            dg_modifier.commandToExecute('ikHandle -name "PVLeftLeg_Ik" -startJoint "IkPVLeftUpLeg" -endEffector "IkPVLeftFoot" -solver "ikRPsolver"')
            dg_modifier.commandToExecute('rename effector1 PVLeftLeg_effector')
            dg_modifier.commandToExecute('ikHandle -name "NoFlipLeftLeg_Ik" -startJoint "IkNoFlipLeftUpLeg" -endEffector "IkNoFlipLeftFoot" -solver "ikRPsolver"')
            dg_modifier.commandToExecute('rename effector1 NoFlipLeftLeg_effector')
            dg_modifier.commandToExecute('parent LeftReverseFootToe LeftReverseFootToeEnd')
            dg_modifier.commandToExecute('parent LeftReverseFootToeEnd LeftReverseInnerFoot')
            dg_modifier.commandToExecute('parent LeftReverseInnerFoot LeftReverseOuterFoot')
            dg_modifier.commandToExecute('parent LeftReverseOuterFoot LeftReverseFootHeel')
            dg_modifier.commandToExecute('parent PVLeftLeg_Ik LeftReverseFootToe')
            dg_modifier.commandToExecute('parent NoFlipLeftLeg_Ik LeftReverseFootToe')
            dg_modifier.commandToExecute('parent LeftLegFoot_Ik LeftReverseFootToe')
            dg_modifier.commandToExecute('parent LeftLegToe_Ik LeftReverseFootToeWiggle')
            # dg_modifier.commandToExecute('parent NoFlipLeftLeg_effector IkNoFlipLeftLeg')
            # dg_modifier.commandToExecute('parent PVLeftLeg_effector IkPVLeftLeg')
            dg_modifier.commandToExecute('parent LeftFoot_effector IkLeftFoot')
            dg_modifier.commandToExecute('parent LeftToe_effector IkLeftToeBase')
            dg_modifier.doIt()

    def createRlegIk(self, index):
        iksolver_lst = om1.MSelectionList()
        dg_modifier = om1.MDGModifier()

        obj_upleg = om1.MObject()
        obj_foot = om1.MObject()
        obj_toe = om1.MObject()
        obj_toeend = om1.MObject()

        rleg_sl_lst = om1.MSelectionList()
        rleg_sl_lst.add("IkRightUpLeg*")
        rleg_sl_lst.add("IkRightFoot")
        rleg_sl_lst.add("IkRightToeBase")
        rleg_sl_lst.add("IkRightToeEnd")
        rleg_sl_lst.getDependNode(0, obj_upleg)
        rleg_sl_lst.getDependNode(1, obj_foot)
        rleg_sl_lst.getDependNode(2, obj_toe)
        rleg_sl_lst.getDependNode(rleg_sl_lst.length()-1, obj_toeend)

        rleg_pathnode = om1.MDagPath()
        rupleg_path = rleg_pathnode.getAPathTo(obj_upleg)
        rlegfoot_path = rleg_pathnode.getAPathTo(obj_foot)
        rlegtoe_path = rleg_pathnode.getAPathTo(obj_toe)

        ik_system = omanim1.MIkSystem()

        try:
            if cmds.objExists("RightLeg_Ik") and cmds.objExists("RightLeg_effector"):

                cmds.delete("RightLeg_Ik")
                cmds.delete("RightLegFoot_Ik")
                cmds.delete("RightLegToe_Ik")

        except:
            pass

        if index == 0 :
            try:
                cmds.delete("RightLeg_effector")
            except:
                pass

            print("All Ik Removed")

        elif index == 1:
            try:
                iksolver_lst.add("ikRPsolver*")
            except:
                cmds.createNode("ikRPsolver")

            rp_solver = ik_system.findSolver("ikRPsolver")

            ik_effector = omanim1.MFnIkEffector()
            self.rleg_effector = ik_effector.create(obj_foot)
            rleg_effector_path = rleg_pathnode.getAPathTo(self.rleg_effector)

            self.rlegtoe_effector = ik_effector.create(obj_toe)
            rlegtoe_effector_path = rleg_pathnode.getAPathTo(self.rlegtoe_effector)

            self.rlegtoeend_effector = ik_effector.create(obj_toeend)
            rlegtoeend_effector_path = rleg_pathnode.getAPathTo(self.rlegtoeend_effector)

            ik_handleleg = omanim1.MFnIkHandle()
            self.rlegfoot_ik = ik_handleleg.create(rupleg_path, rleg_effector_path)
            ik_handleleg.setSolver(rp_solver)

            ik_handlelegtoe = omanim1.MFnIkHandle()
            self.rlegtoe_ik = ik_handlelegtoe.create(rlegfoot_path, rlegtoe_effector_path)
            ik_handlelegtoe.setSolver(rp_solver)

            ik_handlelegtoeend = omanim1.MFnIkHandle()
            self.rlegtoeend_ik = ik_handlelegtoeend.create(rlegtoe_path, rlegtoeend_effector_path)
            ik_handlelegtoeend.setSolver(rp_solver)

            dg_modifier.renameNode(self.rlegfoot_ik, "RightLeg_Ik")
            dg_modifier.renameNode(self.rlegtoe_ik, "RightLegFoot_Ik")
            dg_modifier.renameNode(self.rlegtoeend_ik, "RightLegToe_Ik")
            dg_modifier.renameNode(self.rleg_effector, "RightLeg_effector")
            dg_modifier.renameNode(self.rlegtoe_effector, "RightFoot_effector")
            dg_modifier.renameNode(self.rlegtoeend_effector, "RightToe_effector")
            dg_modifier.commandToExecute('parent RightLeg_Ik DoNotTouch')
            dg_modifier.commandToExecute('parent RightLeg_effector IkRightLeg')
            dg_modifier.commandToExecute('parent RightFoot_effector IkRightFoot')
            dg_modifier.commandToExecute('parent RightToe_effector IkRightToeBase')
            dg_modifier.doIt()

    def createBoundingBox(self):

        try:
            box_sl_ls = om2.MSelectionList()
            box_sl_ls.add("boundingBox")
            print("BoundingBox already Exist")
        except:
            box_tn = om2.MFnDagNode()
            self.boundingbox_tn = box_tn.create("transform", "boundingBox")

            box_sn = om2.MFnDagNode()
            box_sn.create("mesh", "boundingboxShape", self.boundingbox_tn)

            box_objtype_n = om2.MFnDependencyNode()
            box_objtype_n.create("polyCube")

            boundingbox_otp_plug = box_objtype_n.findPlug("output", False)
            boundingbox_inp_plug = box_sn.findPlug("inMesh", False)

            box_mod_n = om2.MDGModifier()
            box_mod_n.connect(boundingbox_otp_plug, boundingbox_inp_plug)
            box_mod_n.doIt()

    def rigChar(self):
        ctrl_cv_n = om2.MFnNurbsCurve()
        self.ctrl_mod_n = om2.MDGModifier()
        ctrl_tr_n = om2.MFnDagNode()

        obj_sl_lst = om2.MSelectionList()
        obj_sl_lst.add("boundingBox")
        box_obj = obj_sl_lst.getDependNode(0)

        self.box_transform = om2.MFnTransform(box_obj)
        box_transform_s = self.box_transform.scale()

        ctrl_master_circle_points = [om2.MPoint(0.75, 0.0, 0.25), om2.MPoint(0.0, 0.0, 1.0), om2.MPoint(-1.0, 0.0), om2.MPoint(0.0, 0.0, -1.0), om2.MPoint(0.75, 0.0, -0.25)]
        ctrl_master_arrow_points = [om2.MPoint(0.75, 0.0, -0.25), om2.MPoint(1.50, 0.0, -0.50), om2.MPoint(1.50, 0.0, -0.65), om2.MPoint(2.0, 0.0, 0.0), om2.MPoint(1.50, 0.0, 0.65), om2.MPoint(1.50, 0.0, 0.50), om2.MPoint(0.75, 0.0, 0.25)]

        self.globalctrl_tn =  ctrl_tr_n.create("transform", "Biped_ctrl_grp")
        self.draw_global_tn = ctrl_tr_n.create("transform", "Draw_global_ctrl")
        crv_ctrl_master_circle = ctrl_cv_n.createWithEditPoints(ctrl_master_circle_points, 3, 1, False, True, True, self.draw_global_tn)
        crv_ctrl_master_arrow = ctrl_cv_n.createWithEditPoints(ctrl_master_arrow_points, 1, 1, False, True, True, self.draw_global_tn)

        self.masterctrl_tn = ctrl_tr_n.create("transform", "Biped_Master_ctrl", self.globalctrl_tn)
        ctrl_global_comb_cv = ctrl_cv_n.create([crv_ctrl_master_circle, crv_ctrl_master_arrow], self.masterctrl_tn)

        masctrl_transform = om2.MFnTransform(self.masterctrl_tn)
        masctrl_transform_s = masctrl_transform.findPlug("scale", False)

        if masctrl_transform_s.isCompound:
            for i in range(masctrl_transform_s.numChildren()):
                child_plug = masctrl_transform_s.child(i)
                attr_value = child_plug.setDouble(box_transform_s[2])

        masctrl_transform_r = masctrl_transform.rotation(om2.MSpace.kTransform)
        masctrl_transform_r[1] = -1.57079
        masctrl_transform.setRotation(masctrl_transform_r, om2.MSpace.kTransform)

        self.ctrl_mod_n.commandToExecute('delete "Draw_global_ctrl"')
        self.ctrl_mod_n.renameNode(ctrl_global_comb_cv, "Master_shape")
        self.ctrl_mod_n.commandToExecute('color -rgbColor 0.5 1 0 "Biped_Master_ctrl"')
        self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_Master_ctrl"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_ctrl_grp.translateX"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_ctrl_grp.translateY"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_ctrl_grp.translateZ"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_ctrl_grp.rotateX"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_ctrl_grp.rotateY"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_ctrl_grp.rotateZ"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_ctrl_grp.scaleX"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_ctrl_grp.scaleY"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_ctrl_grp.scaleZ"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_ctrl_grp.visibility"')
        self.ctrl_mod_n.doIt()

        ctrl_root_points = [om2.MPoint(0.75, 0.2, 0.0), om2.MPoint(0.75, 0.0, 0.50), om2.MPoint(0.0, 1, 1), om2.MPoint(-0.75, 0.0, 0.50), om2.MPoint(-0.75, 0.2, 0.0), om2.MPoint(-0.75, 0.0, -0.50), om2.MPoint(0.0, 1, -1), om2.MPoint(0.75, 0.0, -0.50), om2.MPoint(0.75, 0.2, 0.0)]

        self.rootnull_tn = ctrl_tr_n.create("transform", "Biped_Root_null", self.masterctrl_tn)
        self.rootctrl_tn = ctrl_tr_n.create("transform", "Biped_Root_ctrl", self.rootnull_tn)
        crv_ctrl_root = ctrl_cv_n.createWithEditPoints(ctrl_root_points, 3, 1, False, True, True, self.rootctrl_tn)

        ctrl_hip_line_points = [om2.MPoint(0.75, 0.00, -0.75), om2.MPoint(0.75, 0.00, 0.75), om2.MPoint(0.75, 0.00, 0.00), om2.MPoint(-0.75, 0.00), om2.MPoint(-0.75, 0.00, 0.75), om2.MPoint(-0.75, 0.00, -0.75)]
        ctrl_hip_arcback_points = [om2.MPoint(0.75, 0.00, -0.75), om2.MPoint(1, 0.5, 0.00), om2.MPoint(0.75, 0.00, 0.75)]
        ctrl_hip_linefront_points = [om2.MPoint(-0.75, 0.00, -0.75), om2.MPoint(-1, 0.5, 0.00), om2.MPoint(-0.75, 0.00, 0.75)]

        self.hipctrl_tn = ctrl_tr_n.create("transform", "Biped_Hip_ctrl", self.rootctrl_tn)
        crv_ctrl_hip_line = ctrl_cv_n.createWithEditPoints(ctrl_hip_line_points, 1, 1, False, True, True, self.hipctrl_tn)
        crv_ctrl_hip_arcback = ctrl_cv_n.createWithEditPoints(ctrl_hip_arcback_points, 3, 1, False, True, True, self.hipctrl_tn)
        crv_ctrl_hip_linefront = ctrl_cv_n.createWithEditPoints(ctrl_hip_linefront_points, 3, 1, False, True, True, self.hipctrl_tn)

        obj_sl_lst.add("Hip")
        hip_obj = obj_sl_lst.getDependNode(1)
        jnt_root_transform = om2.MFnTransform(hip_obj)
        jnt_root_trans = jnt_root_transform.transformation()

        rootnull_transform = om2.MFnTransform(self.rootnull_tn)
        rootnull_transform.transformation()
        rootnull_transform.setTransformation(jnt_root_trans)

        rootctrl_transform = om2.MFnTransform(self.rootctrl_tn)
        rootctrl_transform_s = rootctrl_transform.findPlug("scale", False)

        if rootctrl_transform_s.isCompound:
            for i in range(rootctrl_transform_s.numChildren()):
                child_plug = rootctrl_transform_s.child(i)
                attr_value = child_plug.setDouble(box_transform_s[0]/2)

        rootctrl_transform_r = rootctrl_transform.rotation(om2.MSpace.kTransform)
        rootctrl_transform_r[0], rootctrl_transform_r[1] = 3.1415, -1.57079
        rootctrl_transform.setRotation(rootctrl_transform_r, om2.MSpace.kTransform)

        hipctrl_transform = om2.MFnTransform(self.hipctrl_tn)
        hipctrl_transform_r = hipctrl_transform.rotation(om2.MSpace.kTransform)
        hipctrl_transform_r[1] = -1.57079
        hipctrl_transform.setRotation(hipctrl_transform_r, om2.MSpace.kTransform)

        hipctrl_transform_s = hipctrl_transform.scale()
        hipctrl_transform_s[2] = 0.7
        hipctrl_transform.setScale(hipctrl_transform_s)

        self.ctrl_mod_n.renameNode(crv_ctrl_root, "Root_shape")
        self.ctrl_mod_n.renameNode(crv_ctrl_hip_line, "HipLine_shape")
        self.ctrl_mod_n.renameNode(crv_ctrl_hip_arcback, "HipArcRight_shape")
        self.ctrl_mod_n.renameNode(crv_ctrl_hip_linefront, "HipArcLeft_shape")
        self.ctrl_mod_n.commandToExecute('color -rgbColor 1 0 0 "Biped_Root_ctrl"')
        self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 0 "Biped_Hip_ctrl"')
        self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_Root_ctrl"')
        self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_Hip_ctrl"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_null.translateX"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_null.translateY"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_null.translateZ"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_null.rotateX"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_null.rotateY"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_null.rotateZ"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_null.scaleX"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_null.scaleY"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_null.scaleZ"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_null.visibility"')
        self.ctrl_mod_n.doIt()

        spine_sl_lst = om2.MSelectionList()
        spine_sl_lst.add("Spine*")

        ctrl_spine_line_l_points = [om2.MPoint(0.50, 0.00, 0.25), om2.MPoint(0.50, 0.05, 0.25), om2.MPoint(0.50, 0.00, 0.20), om2.MPoint(-0.50, 0.00, 0.20), om2.MPoint(-0.50, 0.05, 0.25), om2.MPoint(-0.50, 0.00, 0.25)]
        ctrl_spine_line_r_points = [om2.MPoint(-0.50, 0.00, -0.25), om2.MPoint(-0.50, 0.05, -0.25), om2.MPoint(-0.50, 0.00, -0.20), om2.MPoint(0.50, 0.00, -0.20), om2.MPoint(0.50, 0.05, -0.25), om2.MPoint(0.50, 0.00, -0.25) ]
        ctrl_spine_curve_fl_points = [om2.MPoint(0.50, -0.15, 0.00), om2.MPoint(0.50, -0.06, 0.10), om2.MPoint(0.50, 0.00, 0.25)]
        ctrl_spine_curve_fr_points = [om2.MPoint(0.50, 0.00, -0.25), om2.MPoint(0.50, -0.06, -0.10), om2.MPoint(0.50, -0.15, 0.00)]
        ctrl_spine_curve_b_points = [om2.MPoint(-0.50, 0.00, 0.25), om2.MPoint(-0.50, -0.06, 0.10), om2.MPoint(-0.50, -0.15, 0.00), om2.MPoint(-0.50, -0.06, -0.10),  om2.MPoint(-0.50, 0.00, -0.25)]

        self.draw_spine_tn = ctrl_tr_n.create("transform", "Draw_Spine_ctrl")
        crv_ctrl_spine_line_l = ctrl_cv_n.createWithEditPoints(ctrl_spine_line_l_points, 1, 1, False, True, True, self.draw_spine_tn)
        crv_ctrl_spine_line_r = ctrl_cv_n.createWithEditPoints(ctrl_spine_line_r_points, 1, 1, False, True, True, self.draw_spine_tn)
        crv_ctrl_spine_curve_fl = ctrl_cv_n.createWithEditPoints(ctrl_spine_curve_fl_points, 3, 1, False, True, True, self.draw_spine_tn)
        crv_ctrl_spine_curve_fr = ctrl_cv_n.createWithEditPoints(ctrl_spine_curve_fr_points, 3, 1, False, True, True, self.draw_spine_tn)
        crv_ctrl_spine_curve_b = ctrl_cv_n.createWithEditPoints(ctrl_spine_curve_b_points, 3, 1, False, True, True, self.draw_spine_tn)

        ctrl_stretchyspine_circle_points = [om2.MPoint(0.70, 0.00, 0.00), om2.MPoint(0.00, -0.20, 0.70), om2.MPoint(-0.70, 0.00, 0.00), om2.MPoint(0.00, -0.20, -0.70), om2.MPoint(0.70, 0.00, 0.00)]

        for index in range(spine_sl_lst.length()):
            if index == 0:
                self.spinenull_tn = ctrl_tr_n.create("transform", "Biped_Spine"+str(index)+"_null", self.rootctrl_tn)
                self.spinectrl_tn = ctrl_tr_n.create("transform", "Biped_Spine"+str(index)+"_ctrl", self.spinenull_tn)
                ctrl_spine_comb_cv = ctrl_cv_n.create([crv_ctrl_spine_curve_fl, crv_ctrl_spine_line_l, crv_ctrl_spine_curve_b, crv_ctrl_spine_line_r, crv_ctrl_spine_curve_fr], self.spinectrl_tn)

            else:
                self.spinenull_tn = ctrl_tr_n.create("transform", "Biped_Spine"+str(index)+"_null")
                self.spinectrl_tn = ctrl_tr_n.create("transform", "Biped_Spine"+str(index)+"_ctrl", self.spinenull_tn)
                ctrl_spine_comb_cv = ctrl_cv_n.create([crv_ctrl_spine_curve_fl, crv_ctrl_spine_line_l, crv_ctrl_spine_curve_b, crv_ctrl_spine_line_r, crv_ctrl_spine_curve_fr], self.spinectrl_tn)

            if index == spine_sl_lst.length()-1:
                self.stretchyspine_tn = ctrl_tr_n.create("transform", "Biped_StretchySpine_ctrl", self.spinectrl_tn)
                crv_ctrl_stretchyspine = ctrl_cv_n.createWithEditPoints(ctrl_stretchyspine_circle_points, 3, 1, False, True, True, self.stretchyspine_tn)

                self.ctrl_mod_n.renameNode(crv_ctrl_stretchyspine, "StretchySpine_shape")

            jnt_spine_obj = spine_sl_lst.getDependNode(index)
            spine_path_n = om2.MDagPath()
            spine_path = spine_path_n.getAPathTo(jnt_spine_obj)
            jnt_spine_transform = om2.MFnTransform(spine_path)
            jnt_spine_t = jnt_spine_transform.translation(om2.MSpace.kWorld)

            spinenull_transform = om2.MFnTransform(self.spinenull_tn)
            spinenull_transform.setRotatePivotTranslation(jnt_spine_t, om2.MSpace.kTransform)

            spinectrl_transform = om2.MFnTransform(self.spinectrl_tn)
            spinectrl_transform_s = spinectrl_transform.findPlug("scale", False)

            if spinectrl_transform_s.isCompound:
                for i in range(spinectrl_transform_s.numChildren()):
                    child_plug = spinectrl_transform_s.child(i)
                    attr_value = child_plug.setDouble(box_transform_s[0]/1.3)

            spinectrl_transform_align = spinectrl_transform.rotation(om2.MSpace.kTransform)
            spinectrl_transform_align[1] = -1.57079
            spinectrl_transform.setRotation(spinectrl_transform_align, om2.MSpace.kTransform)
            self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_Spine{0}_ctrl"'.format(index))
            self.ctrl_mod_n.doIt()

            jnt_spine_r = cmds.xform("Spine{0}".format(index), query=True, rotation=True, worldSpace=True)

            radian_spine_x = (jnt_spine_r[0]/180)*3.1415
            radian_spine_y = (jnt_spine_r[1]/180)*3.1415
            radian_spine_z = (jnt_spine_r[2]/180)*3.1415

            spinenull_transform_r = spinenull_transform.rotation(om2.MSpace.kTransform)
            spinenull_transform_r[0], spinenull_transform_r[1], spinenull_transform_r[2] = radian_spine_x, radian_spine_y, radian_spine_z
            spinenull_transform.setRotation(spinenull_transform_r, om2.MSpace.kTransform)

            if index == 0:

                rootctrl_transform_matrix = rootnull_transform.transformation()
                rootctrl_transform_worldmatrix = rootctrl_transform_matrix.asMatrixInverse()

                spinenull_childtransform_trans = spinenull_transform.transformation()
                spinenull_childtransform_worldmatrix = spinenull_childtransform_trans.asMatrix()

                spinenull_childtransform_localmatrix = spinenull_childtransform_worldmatrix * rootctrl_transform_worldmatrix

                spinenull_transform.setTransformation(om2.MTransformationMatrix(spinenull_childtransform_localmatrix))

            else:
                parent_index = index - 1

                spinectrl_sl_lst = om2.MSelectionList()
                spinectrl_sl_lst.add("Biped_Spine*_ctrl")
                spinectrl_obj = spinectrl_sl_lst.getDependNode(parent_index)


                spinenull_sl_lst = om2.MSelectionList()
                spinenull_sl_lst.add("Biped_Root_null")
                spinenull_sl_lst.add("Biped_Spine*_null")

                spine_tr_n = om2.MFnDagNode(spinectrl_obj)
                spine_tr_n.addChild(self.spinenull_tn)

                spinenull_parentinvtransform_matrix = om2.MMatrix()
                for i in range(spinenull_sl_lst.length()-1):
                    parentobj = spinenull_sl_lst.getDependNode(i)
                    parentinvtransform = om2.MFnTransform(parentobj)
                    parentinvtransform_trans = parentinvtransform.transformation()
                    null_Matrix = parentinvtransform_trans.asMatrixInverse()

                    spinenull_parentinvtransform_matrix = spinenull_parentinvtransform_matrix * null_Matrix

                spinenull_childtransform_trans = spinenull_transform.transformation()
                spinenull_childtransform_worldmatrix = spinenull_childtransform_trans.asMatrix()

                spinenull_childtransform_localmatrix = spinenull_childtransform_worldmatrix * spinenull_parentinvtransform_matrix

                spinenull_transform.setTransformation(om2.MTransformationMatrix(spinenull_childtransform_localmatrix))

            self.ctrl_mod_n.renameNode(ctrl_spine_comb_cv, "Spine"+str(index)+"_shape")
            self.ctrl_mod_n.commandToExecute('color -rgbColor 1 1 0 "Biped_Spine{0}_ctrl"'.format(index))
            self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_Spine{0}_ctrl"'.format(index))
            self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_null.translateX"'.format(index))
            self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_null.translateY"'.format(index))
            self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_null.translateZ"'.format(index))
            self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_null.rotateX"'.format(index))
            self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_null.rotateY"'.format(index))
            self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_null.rotateZ"'.format(index))
            self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_null.scaleX"'.format(index))
            self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_null.scaleY"'.format(index))
            self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_null.scaleZ"'.format(index))
            self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_null.visibility"'.format(index))

        self.ctrl_mod_n.commandToExecute('color -rgbColor 1 0 0 "Biped_StretchySpine_ctrl"')
        self.ctrl_mod_n.commandToExecute('delete "Draw_Spine_ctrl"')
        self.ctrl_mod_n.doIt()

        head_sl_ls = om2.MSelectionList()
        head_sl_ls.add("Neck")
        head_sl_ls.add("Head")
        head_sl_ls.add("HeadTopEnd")

        ctrl_neck_line_up_points = [om2.MPoint(0.00, 0.05, 0.02), om2.MPoint(0.60, 0.05, 0.02)]
        ctrl_neck_star_up_points = [om2.MPoint(0.60, 0.05, 0.02), om2.MPoint(0.70, 0.15, 0.20), om2.MPoint(0.70, 0.09, 0.20), om2.MPoint(0.70, 0.06, 0.13), om2.MPoint(0.60, 0.00, 0.00), om2.MPoint(0.70, 0.05, -0.13), om2.MPoint(0.70, 0.09, -0.20), om2.MPoint(0.70, 0.15, -0.20), om2.MPoint(0.60, 0.05, -0.02)]
        ctrl_neck_line_down_points = [om2.MPoint(0.60, 0.05, -0.02), om2.MPoint(0.00, 0.05, -0.02)]

        self.draw_neck_tn = ctrl_tr_n.create("transform", "Draw_neck_ctrl")
        crv_ctrl_neck_line_up = ctrl_cv_n.createWithEditPoints(ctrl_neck_line_up_points, 1, 1, False, True, True, self.draw_neck_tn)
        crv_ctrl_neck_star = ctrl_cv_n.createWithEditPoints(ctrl_neck_star_up_points, 1, 1, False, True, True, self.draw_neck_tn)
        crv_ctrl_neck_line_down = ctrl_cv_n.createWithEditPoints(ctrl_neck_line_down_points, 1, 1, False, True, True, self.draw_neck_tn)

        if self.autostretch.currentIndex() == 1:
            self.necknull_tn = ctrl_tr_n.create("transform", "Biped_Neck_null", self.stretchyspine_tn)
        else:
            self.necknull_tn = ctrl_tr_n.create("transform", "Biped_Neck_null", self.spinectrl_tn)

        self.neckctrl_tn = ctrl_tr_n.create("transform", "Biped_Neck_ctrl", self.necknull_tn)
        ctrl_neck_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.neckctrl_tn)

        jnt_neck_obj = head_sl_ls.getDependNode(0)
        neck_path_n = om2.MDagPath()
        neck_path = neck_path_n.getAPathTo(jnt_neck_obj)
        jnt_neck_transform = om2.MFnTransform(neck_path)
        jnt_neck_t = jnt_neck_transform.translation(om2.MSpace.kWorld)

        necknull_transform = om2.MFnTransform(self.necknull_tn)
        necknull_transform.rotatePivotTranslation(om2.MSpace.kTransform)
        necknull_transform.setRotatePivotTranslation(jnt_neck_t, om2.MSpace.kTransform)

        neckctrl_transform = om2.MFnTransform(self.neckctrl_tn)
        neckctrl_transform_s = neckctrl_transform.findPlug("scale", False)

        if neckctrl_transform_s.isCompound:
            for i in range(neckctrl_transform_s.numChildren()):
                child_plug = neckctrl_transform_s.child(i)
                attr_value = child_plug.setDouble(box_transform_s[0]/1.2)

        neckctrl_transform_align = neckctrl_transform.rotation(om2.MSpace.kTransform)
        neckctrl_transform_align[1] = +1.57079
        neckctrl_transform.setRotation(neckctrl_transform_align, om2.MSpace.kTransform)

        jnt_neck_r = cmds.xform("Neck", query=True, rotation=True, worldSpace=True)

        radian_neck_x = (jnt_neck_r[0]/180)*3.1415
        radian_neck_y = (jnt_neck_r[1]/180)*3.1415
        radian_neck_z = (jnt_neck_r[2]/180)*3.1415

        necknull_transform_r = necknull_transform.rotation(om2.MSpace.kTransform)
        necknull_transform_r[0], necknull_transform_r[1], necknull_transform_r[2] = radian_neck_x, radian_neck_y, radian_neck_z
        necknull_transform.setRotation(necknull_transform_r, om2.MSpace.kTransform)

        necknull_transform_trans = necknull_transform.transformation()
        necknull_transform_worldmatrix = necknull_transform_trans.asMatrix()

        necknull_transform_localmatrix = necknull_transform_worldmatrix * spinenull_parentinvtransform_matrix * spinenull_childtransform_localmatrix.inverse()

        necknull_transform.setTransformation(om2.MTransformationMatrix(necknull_transform_localmatrix))

        self.ctrl_mod_n.renameNode(ctrl_neck_comb_cv, "Neck_shape")
        self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 1 "Biped_Neck_ctrl"')
        self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_Neck_ctrl"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_null.translateX"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_null.translateY"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_null.translateZ"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_null.rotateX"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_null.rotateY"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_null.rotateZ"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_null.scaleX"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_null.scaleY"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_null.scaleZ"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_null.visibility"')
        self.ctrl_mod_n.doIt()

        ctrl_head_arcl_points = [om2.MPoint(-0.70, -0.1), om2.MPoint(-0.65, -0.03, 0.04), om2.MPoint(-0.50, 0.00, 0.1)]
        ctrl_head_sq_points = [om2.MPoint(-0.50, 0.00, 0.1), om2.MPoint(-0.30, 0.00, 0.25),  om2.MPoint(0.10, 0.00, 0.25),  om2.MPoint(0.20, 0.00, 0.05), om2.MPoint(0.20, 0.00, -0.05), om2.MPoint(0.10, 0.00, -0.25), om2.MPoint(-0.30, 0.00, -0.25), om2.MPoint(-0.50, 0.00, -0.1)]
        ctrl_head_arcr_points = [om2.MPoint(-0.50, 0.00, -0.1), om2.MPoint(-0.65, -0.03, -0.04), om2.MPoint(-0.70, -0.1)]

        self.draw_head_tn = ctrl_tr_n.create("transform", "Draw_head_ctrl")
        crv_ctrl_head_line_l = ctrl_cv_n.createWithEditPoints(ctrl_head_sq_points, 1, 1, False, True, True, self.draw_head_tn)
        crv_ctrl_arc_l = ctrl_cv_n.createWithEditPoints(ctrl_head_arcl_points, 3, 1, False, True, True, self.draw_head_tn)
        crv_ctrl_arc_r = ctrl_cv_n.createWithEditPoints(ctrl_head_arcr_points, 3, 1, False, True, True, self.draw_head_tn)

        self.headnull_tn = ctrl_tr_n.create("transform", "Biped_Head_null", self.neckctrl_tn)
        self.headctrl_tn = ctrl_tr_n.create("transform", "Biped_Head_ctrl", self.headnull_tn)
        ctrl_head_comb_cv = ctrl_cv_n.create([crv_ctrl_head_line_l, crv_ctrl_arc_l, crv_ctrl_arc_r], self.headctrl_tn)

        ctrl_stretchyspine_circle_points = [om2.MPoint(0.30, 0.00, 0.00), om2.MPoint(0.00, 0.20, 0.30), om2.MPoint(-0.30, 0.00, 0.00), om2.MPoint(0.00, 0.20, -0.30), om2.MPoint(0.30, 0.00, 0.00)]

        self.stretchyheadctrl_tn = ctrl_tr_n.create("transform", "Biped_StretchyNeck_ctrl", self.headctrl_tn)
        crv_ctrl_stretchyhead = ctrl_cv_n.createWithEditPoints(ctrl_stretchyspine_circle_points, 3, 1, False, True, True, self.stretchyheadctrl_tn)

        jnt_head_obj = head_sl_ls.getDependNode(1)
        head_path_n = om2.MDagPath()
        head_path = head_path_n.getAPathTo(jnt_head_obj)
        jnt_head_transform = om2.MFnTransform(head_path)
        jnt_head_t = jnt_head_transform.translation(om2.MSpace.kWorld)

        jnt_headtop_obj = head_sl_ls.getDependNode(2)
        jnt_headtop_transform = om2.MFnTransform(jnt_headtop_obj)
        jnt_headtop_t = jnt_headtop_transform.translation(om2.MSpace.kTransform)

        headtopnull_transform = om2.MFnTransform(self.headnull_tn)
        headtopnull_transform.setRotatePivotTranslation(jnt_head_t, om2.MSpace.kTransform)

        headtopctrl_transform = om2.MFnTransform(self.headctrl_tn)

        headtopctrl_transform_t = headtopctrl_transform.rotatePivotTranslation(om2.MSpace.kTransform)
        headtopctrl_transform_t[1] = jnt_headtop_t[1]+1
        headtopctrl_transform.setRotatePivotTranslation(headtopctrl_transform_t, om2.MSpace.kTransform)

        headtopctrl_transform_s = headtopctrl_transform.findPlug("scale", False)

        if headtopctrl_transform_s.isCompound:
            for i in range(headtopctrl_transform_s.numChildren()):
                child_plug = headtopctrl_transform_s.child(i)
                attr_value = child_plug.setDouble(box_transform_s[0]/1.7)

        headtopctrl_transform_align = headtopctrl_transform.rotation(om2.MSpace.kTransform)
        headtopctrl_transform_align[1] = +1.57079
        headtopctrl_transform.setRotation(headtopctrl_transform_align, om2.MSpace.kTransform)

        jnt_head_r = cmds.xform("Head", query=True, rotation=True, worldSpace=True)

        radian_head_x = (jnt_head_r[0]/180)*3.1415
        radian_head_y = (jnt_head_r[1]/180)*3.1415
        radian_head_z = (jnt_head_r[2]/180)*3.1415

        headnull_transform_r = headtopnull_transform.rotation(om2.MSpace.kTransform)
        headnull_transform_r[0], headnull_transform_r[1], headnull_transform_r[2] = radian_head_x, radian_head_y, radian_head_z
        headtopnull_transform.setRotation(headnull_transform_r, om2.MSpace.kTransform)

        headtopnull_transform_trans = headtopnull_transform.transformation()
        headtopnull_transform_worldmatrix = headtopnull_transform_trans.asMatrix()

        headtopnull_transform_localmatrix = headtopnull_transform_worldmatrix * spinenull_parentinvtransform_matrix * spinenull_childtransform_localmatrix.inverse() * necknull_transform_localmatrix.inverse()

        headtopnull_transform.setTransformation(om2.MTransformationMatrix(headtopnull_transform_localmatrix))

        headtopctrl_path_n = om2.MDagPath()
        headtopctrl_path = headtopctrl_path_n.getAPathTo(self.headctrl_tn)
        headtopctrl_worldtransform = om2.MFnTransform(headtopctrl_path)

        headtopctrl_worldtransform.setRotatePivot(om2.MPoint(jnt_head_t), om2.MSpace.kWorld, False)

        stretchyheadctrl_path = headtopctrl_path_n.getAPathTo(self.stretchyheadctrl_tn)
        stretchyheadctrl_worldtransform = om2.MFnTransform(stretchyheadctrl_path)

        stretchyheadctrl_worldtransform.setRotatePivot(om2.MPoint(jnt_head_t), om2.MSpace.kWorld, False)

        self.ctrl_mod_n.commandToExecute('delete "Draw_head_ctrl"')
        self.ctrl_mod_n.renameNode(ctrl_head_comb_cv, "Head_shape")
        self.ctrl_mod_n.renameNode(crv_ctrl_stretchyhead, "StretchyNeck_shape")
        self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 0 "Biped_Head_ctrl"')
        self.ctrl_mod_n.commandToExecute('color -rgbColor 1 0 0 "Biped_StretchyNeck_ctrl"')
        self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_Head_ctrl"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_null.translateX"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_null.translateY"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_null.translateZ"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_null.rotateX"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_null.rotateY"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_null.rotateZ"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_null.scaleX"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_null.scaleY"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_null.scaleZ"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_null.visibility"')
        self.ctrl_mod_n.doIt()

        larm_sl_ls = om2.MSelectionList()
        larm_sl_ls.add("LeftArm")
        larm_sl_ls.add("LeftForeArm")
        larm_sl_ls.add("LeftHand")

        fklarm_sl_ls = om2.MSelectionList()
        fklarm_sl_ls.add("LeftShoulder")
        fklarm_sl_ls.add("FkLeftArm")
        fklarm_sl_ls.add("FkLeftForeArm")
        fklarm_sl_ls.add("FkLeftHand")

        ctrl_shoulder_arc_l = [om2.MPoint(1.20, 0.15), om2.MPoint(1.10, 0.28, 0.10), om2.MPoint(0.90, 0.35, 0.25)]
        ctrl_shoulder_line = [om2.MPoint(0.90, 0.35, 0.25), om2.MPoint(0.30, 0.50, 0.25), om2.MPoint(0.25, 0.55, 0.20), om2.MPoint(0.25, 0.55, -0.20), om2.MPoint(0.30, 0.50, -0.25), om2.MPoint(0.90, 0.35, -0.25)]
        ctrl_shoulder_arc_r = [om2.MPoint(0.90, 0.35, -0.25), om2.MPoint(1.10, 0.28, -0.10), om2.MPoint(1.20, 0.15)]

        self.draw_shoulder_tn = ctrl_tr_n.create("transform", "Draw_shoulder_ctrl")
        crv_ctrl_shoulder_arc_l = ctrl_cv_n.createWithEditPoints(ctrl_shoulder_arc_l, 3, 1, False, True, True, self.draw_shoulder_tn)
        crv_ctrl_shoulder_line = ctrl_cv_n.createWithEditPoints(ctrl_shoulder_line, 1, 1, False, True, True, self.draw_shoulder_tn)
        crv_ctrl_shoulder_arc_r = ctrl_cv_n.createWithEditPoints(ctrl_shoulder_arc_r, 3, 1, False, True, True, self.draw_shoulder_tn)

        if self.autostretch.currentIndex() == 1:
            self.lshouldernull_tn = ctrl_tr_n.create("transform", "Biped_LeftShoulder_null", self.stretchyspine_tn)
        else:
            self.lshouldernull_tn = ctrl_tr_n.create("transform", "Biped_LeftShoulder_null", self.spinectrl_tn)

        self.lshoulderctrl_tn = ctrl_tr_n.create("transform", "Biped_LeftShoulder_ctrl", self.lshouldernull_tn)
        ctrl_shoulder_comb_cv = ctrl_cv_n.create([crv_ctrl_shoulder_arc_l, crv_ctrl_shoulder_line, crv_ctrl_shoulder_arc_r], self.lshoulderctrl_tn)

        jnt_lshoulder_obj = fklarm_sl_ls.getDependNode(0)
        lshoulder_path_n = om2.MDagPath()
        lshoulder_path = lshoulder_path_n.getAPathTo(jnt_lshoulder_obj)
        jnt_lshoulder_transform = om2.MFnTransform(lshoulder_path)
        jnt_lshoulder_t = jnt_lshoulder_transform.translation(om2.MSpace.kWorld)

        lshouldernull_transform = om2.MFnTransform(self.lshouldernull_tn)
        lshouldernull_transform.setRotatePivotTranslation(jnt_lshoulder_t, om2.MSpace.kTransform)

        jnt_lshoulder_r = cmds.xform("LeftShoulder", query=True, rotation=True, worldSpace=True)

        radian_lshoulder_x = (jnt_lshoulder_r[0]/180)*3.1415
        radian_lshoulder_y = (jnt_lshoulder_r[1]/180)*3.1415
        radian_lshoulder_z = (jnt_lshoulder_r[2]/180)*3.1415

        lshouldernull_transform_r = lshouldernull_transform.rotation(om2.MSpace.kTransform)
        lshouldernull_transform_r[0], lshouldernull_transform_r[1], lshouldernull_transform_r[2] = radian_lshoulder_x, radian_lshoulder_y, radian_lshoulder_z
        lshouldernull_transform.setRotation(lshouldernull_transform_r, om2.MSpace.kTransform)

        lshoulderctrl_transform = om2.MFnTransform(self.lshoulderctrl_tn)
        lshoulderctrl_transform_r = lshoulderctrl_transform.rotation(om2.MSpace.kTransform)
        lshoulderctrl_transform_r[0], lshoulderctrl_transform_r[1], lshoulderctrl_transform_r[2] = +1.57079, 2.5307, -1.57079
        lshoulderctrl_transform.setRotation(lshoulderctrl_transform_r, om2.MSpace.kTransform)

        lshoulderctrl_transform_s = lshoulderctrl_transform.findPlug("scale", False)

        if lshoulderctrl_transform_s.isCompound:
            for i in range(lshoulderctrl_transform_s.numChildren()):
                child_plug = lshoulderctrl_transform_s.child(i)
                attr_value = child_plug.setDouble(box_transform_s[0]/3)

        lshouldernullnull_transform_trans = lshouldernull_transform.transformation()
        lshouldernullnull_transform_worldmatrix = lshouldernullnull_transform_trans.asMatrix()

        lshouldernullnull_transform_localmatrix = lshouldernullnull_transform_worldmatrix * spinenull_parentinvtransform_matrix * spinenull_childtransform_localmatrix.inverse()

        lshouldernull_transform.setTransformation(om2.MTransformationMatrix(lshouldernullnull_transform_localmatrix))

        lshoulderctrl_path_n = om2.MDagPath()
        lshoulderctrl_path = lshoulderctrl_path_n.getAPathTo(self.lshoulderctrl_tn)
        lshoulderctrl_worldtransform = om2.MFnTransform(lshoulderctrl_path)

        lshoulderctrl_worldtransform.setRotatePivot(om2.MPoint(jnt_lshoulder_t), om2.MSpace.kWorld, False)

        self.ctrl_mod_n.commandToExecute('delete "Draw_shoulder_ctrl"')
        self.ctrl_mod_n.renameNode(ctrl_shoulder_comb_cv, "LeftShoulder_shape")
        self.ctrl_mod_n.commandToExecute('color -rgbColor 1 0 0 "Biped_LeftShoulder_ctrl"')
        self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftShoulder_ctrl"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_null.translateX"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_null.translateY"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_null.translateZ"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_null.rotateX"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_null.rotateY"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_null.rotateZ"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_null.scaleX"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_null.scaleY"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_null.scaleZ"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_null.visibility"')
        self.ctrl_mod_n.doIt()

        for index in range(fklarm_sl_ls.length()):
           jnt_lhand_obj = fklarm_sl_ls.getDependNode(index)
           lhand_path_n = om2.MDagPath()
           lhand_path = lhand_path_n.getAPathTo(jnt_lhand_obj)
           jnt_lhand_transform = om2.MFnTransform(lhand_path)
           jnt_lhand_t = jnt_lhand_transform.translation(om2.MSpace.kWorld)

           if index == 1:
               self.larmnull_tn = ctrl_tr_n.create("transform", "Biped_FkLeftArm_null", self.lshoulderctrl_tn)
               self.larmctrl_tn = ctrl_tr_n.create("transform", "Biped_FkLeftArm_ctrl", self.larmnull_tn )
               ctrl_larm_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.larmctrl_tn)

               larmnull_transform = om2.MFnTransform(self.larmnull_tn)
               larmnull_transform.setRotatePivotTranslation(jnt_lhand_t, om2.MSpace.kTransform)

               jnt_larm_r = cmds.xform("LeftArm", query=True, rotation=True, worldSpace=True)

               radian_larm_x = (jnt_larm_r[0]/180)*3.1415
               radian_larm_y = (jnt_larm_r[1]/180)*3.1415
               radian_larm_z = (jnt_larm_r[2]/180)*3.1415

               larmnull_transform_r = larmnull_transform.rotation(om2.MSpace.kTransform)
               larmnull_transform_r[0], larmnull_transform_r[1], larmnull_transform_r[2] = radian_larm_x, radian_larm_y, radian_larm_z
               larmnull_transform.setRotation(larmnull_transform_r, om2.MSpace.kTransform)

               larmctrl_transform = om2.MFnTransform(self.larmctrl_tn)

               # larmctrl_transform_r = larmctrl_transform.rotation(om2.MSpace.kTransform)
               # larmctrl_transform_r[1] = 0
               # larmctrl_transform.setRotation(larmctrl_transform_r, om2.MSpace.kTransform)

               larmctrl_transform_s = larmctrl_transform.findPlug("scale", False)
               if larmctrl_transform_s.isCompound:
                   for i in range(larmctrl_transform_s.numChildren()):
                       child_plug = larmctrl_transform_s.child(i)
                       attr_value = child_plug.setDouble(box_transform_s[0]/2)

               larmnull_transform_trans = larmnull_transform.transformation()
               larmnull_transform_worldmatrix = larmnull_transform_trans.asMatrix()

               larmnull_transform_localmatrix = larmnull_transform_worldmatrix * spinenull_parentinvtransform_matrix * spinenull_childtransform_localmatrix.inverse() * lshouldernullnull_transform_localmatrix.inverse()

               larmnull_transform.setTransformation(om2.MTransformationMatrix(larmnull_transform_localmatrix))

               self.ctrl_mod_n.renameNode(ctrl_larm_comb_cv, "FkLeftArm_shape")
               self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 1 "Biped_FkLeftArm_ctrl"')
               self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkLeftArm_ctrl"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_null.translateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_null.translateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_null.translateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_null.rotateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_null.rotateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_null.rotateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_null.scaleX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_null.scaleY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_null.scaleZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_null.visibility"')
               self.ctrl_mod_n.doIt()

           elif index == 2:
               self.lforearmnull_tn = ctrl_tr_n.create("transform", "Biped_FkLeftForeArm_null", self.larmctrl_tn)
               self.lforearmctrl_tn = ctrl_tr_n.create("transform", "Biped_FkLeftForeArm_ctrl", self.lforearmnull_tn )
               ctrl_lforearm_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.lforearmctrl_tn)

               lforearmnull_transform = om2.MFnTransform(self.lforearmnull_tn)
               lforearmnull_transform.setRotatePivotTranslation(jnt_lhand_t, om2.MSpace.kTransform)

               jnt_lforearm_r = cmds.xform("LeftForeArm", query=True, rotation=True, worldSpace=True)

               radian_lforearm_x = (jnt_lforearm_r[0]/180)*3.1415
               radian_lforearm_y = (jnt_lforearm_r[1]/180)*3.1415
               radian_lforearm_z = (jnt_lforearm_r[2]/180)*3.1415

               lforearmnull_transform_r = lforearmnull_transform.rotation(om2.MSpace.kTransform)
               lforearmnull_transform_r[0], lforearmnull_transform_r[1], lforearmnull_transform_r[2] = radian_lforearm_x, radian_lforearm_y, radian_lforearm_z
               lforearmnull_transform.setRotation(lforearmnull_transform_r, om2.MSpace.kTransform)

               lforearmctrl_transform = om2.MFnTransform(self.lforearmctrl_tn)

               # lforearmctrl_transform_r = lforearmctrl_transform.rotation(om2.MSpace.kTransform)
               # lforearmctrl_transform_r[1] = -1.57079
               # lforearmctrl_transform.setRotation(lforearmctrl_transform_r, om2.MSpace.kTransform)

               lforearmctrl_transform_s = lforearmctrl_transform.findPlug("scale", False)
               if lforearmctrl_transform_s.isCompound:
                   for i in range(lforearmctrl_transform_s.numChildren()):
                       child_plug = lforearmctrl_transform_s.child(i)
                       attr_value = child_plug.setDouble(box_transform_s[0]/2)

               lforearmnull_transform_trans = lforearmnull_transform.transformation()
               lforearmnull_transform_worldmatrix = lforearmnull_transform_trans.asMatrix()

               lforearmnull_transform_localmatrix = lforearmnull_transform_worldmatrix * spinenull_parentinvtransform_matrix * spinenull_childtransform_localmatrix.inverse() * lshouldernullnull_transform_localmatrix.inverse() * larmnull_transform_localmatrix.inverse()

               lforearmnull_transform.setTransformation(om2.MTransformationMatrix(lforearmnull_transform_localmatrix))

               self.ctrl_mod_n.renameNode(ctrl_lforearm_comb_cv, "FkLeftForeArm_shape")
               self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 1 "Biped_FkLeftForeArm_ctrl"')
               self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkLeftForeArm_ctrl"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_null.translateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_null.translateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_null.translateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_null.rotateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_null.rotateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_null.rotateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_null.scaleX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_null.scaleY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_null.scaleZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_null.visibility"')
               self.ctrl_mod_n.doIt()

           elif index == 3:
               ctrl_lhand_line_up_points = [om2.MPoint(0.00, 0.05, 0.02), om2.MPoint(-0.60, 0.05, 0.02)]
               ctrl_lhand_star_up_points = [om2.MPoint(-0.60, 0.05, 0.02), om2.MPoint(-0.70, 0.15, 0.20), om2.MPoint(-0.70, 0.09, 0.20), om2.MPoint(-0.70, 0.06, 0.13), om2.MPoint(-0.60, 0.00, 0.00), om2.MPoint(-0.70, 0.05, -0.13), om2.MPoint(-0.70, 0.09, -0.20), om2.MPoint(-0.70, 0.15, -0.20), om2.MPoint(-0.60, 0.05, -0.02)]
               ctrl_lhand_line_down_points = [om2.MPoint(-0.60, 0.05, -0.02), om2.MPoint(-0.00, 0.05, -0.02)]

               self.draw_lhand_tn = ctrl_tr_n.create("transform", "Draw_lefthand_ctrl")
               crv_ctrl_lhand_line_up = ctrl_cv_n.createWithEditPoints(ctrl_lhand_line_up_points, 1, 1, False, True, True, self.draw_lhand_tn)
               crv_ctrl_lhand_star = ctrl_cv_n.createWithEditPoints(ctrl_lhand_star_up_points, 1, 1, False, True, True, self.draw_lhand_tn)
               crv_ctrl_lhand_line_down = ctrl_cv_n.createWithEditPoints(ctrl_lhand_line_down_points, 1, 1, False, True, True, self.draw_lhand_tn)

               self.lhandnull_tn = ctrl_tr_n.create("transform", "Biped_FkLeftHand_null", self.lforearmctrl_tn)
               self.lhandctrl_tn = ctrl_tr_n.create("transform", "Biped_FkLeftHand_ctrl", self.lhandnull_tn )
               ctrl_lhandpositive_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.lhandctrl_tn)
               ctrl_lhandnegative_comb_cv = ctrl_cv_n.create([crv_ctrl_lhand_line_up, crv_ctrl_lhand_star, crv_ctrl_lhand_line_down], self.lhandctrl_tn)

               ctrl_lhandoption_line = [om2.MPoint(1.00, 0.00), om2.MPoint(0.00, 0.00, 1.50), om2.MPoint(-1.00, 0.00, 0.00), om2.MPoint(1.00, 0.00)]

               self.lfingernull_tn = ctrl_tr_n.create("transform", "Biped_LeftFingers_null", self.masterctrl_tn)
               self.lhandoption_tn = ctrl_tr_n.create("transform", "Biped_LeftHandOptions_ctrl", larm_sl_ls.getDependNode(2))
               ctrl_lhandoption_cv = ctrl_cv_n.createWithEditPoints(ctrl_lhandoption_line, 1, 1, False, True, True, self.lhandoption_tn)

               lhandnull_transform = om2.MFnTransform(self.lhandnull_tn)
               lhandnull_transform.setRotatePivotTranslation(jnt_lhand_t, om2.MSpace.kTransform)

               lhandoptionctrl_transform = om2.MFnTransform(self.lhandoption_tn)
               lhandoptionctrl_transform.setRotatePivotTranslation(jnt_lhand_t, om2.MSpace.kTransform)

               lfingernull_transform = om2.MFnTransform(self.lfingernull_tn)
               lfingernull_transform.setTranslation(jnt_lhand_t, om2.MSpace.kTransform)

               jnt_lhand_r = cmds.xform("LeftHand", query=True, rotation=True, worldSpace=True)

               radian_lhand_x = (jnt_lhand_r[0]/180)*3.1415
               radian_lhand_y = (jnt_lhand_r[1]/180)*3.1415
               radian_lhand_z = (jnt_lhand_r[2]/180)*3.1415

               lhandnull_transform_r = lhandnull_transform.rotation(om2.MSpace.kTransform)
               lhandnull_transform_r[0], lhandnull_transform_r[1], lhandnull_transform_r[2] = radian_lhand_x, radian_lhand_y, radian_lhand_z
               lhandnull_transform.setRotation(lhandnull_transform_r, om2.MSpace.kTransform)

               lfingernull_transform_r = lfingernull_transform.rotation(om2.MSpace.kTransform)
               lfingernull_transform_r[0], lfingernull_transform_r[1], lfingernull_transform_r[2] = radian_lhand_x, radian_lhand_y, radian_lhand_z
               lfingernull_transform.setRotation(lfingernull_transform_r, om2.MSpace.kTransform)

               lhandctrl_transform = om2.MFnTransform(self.lhandctrl_tn)

               lhandctrl_transform_r = lhandctrl_transform.rotation(om2.MSpace.kTransform)
               lhandctrl_transform_r[1] = 1.57079
               lhandctrl_transform.setRotation(lhandctrl_transform_r, om2.MSpace.kTransform)

               lhandoptionctrl_transform_t = lhandoptionctrl_transform.translation(om2.MSpace.kTransform)
               lhandoptionctrl_transform_t[2] = jnt_lhand_t[2]-3
               lhandoptionctrl_transform.setTranslation(lhandoptionctrl_transform_t, om2.MSpace.kTransform)

               lhandoptionctrl_transform_r = lhandoptionctrl_transform.rotation(om2.MSpace.kTransform)
               lhandoptionctrl_transform_r[0], lhandoptionctrl_transform_r[1], lhandoptionctrl_transform_r[2] = radian_lhand_x-1.57079, radian_lhand_y, radian_lhand_z
               lhandoptionctrl_transform.setRotation(lhandoptionctrl_transform_r, om2.MSpace.kTransform)

               lhandctrl_transform_s = lhandctrl_transform.findPlug("scale", False)
               if lhandctrl_transform_s.isCompound:
                   for i in range(lhandctrl_transform_s.numChildren()):
                       child_plug = lhandctrl_transform_s.child(i)
                       attr_value = child_plug.setDouble(box_transform_s[0]/4)

               lhandnull_transform_trans = lhandnull_transform.transformation()
               lhandnull_transform_worldmatrix = lhandnull_transform_trans.asMatrix()

               lhandnull_transform_localmatrix = lhandnull_transform_worldmatrix * spinenull_parentinvtransform_matrix * spinenull_childtransform_localmatrix.inverse() * lshouldernullnull_transform_localmatrix.inverse() * larmnull_transform_localmatrix.inverse() * lforearmnull_transform_localmatrix.inverse()

               lhandnull_transform.setTransformation(om2.MTransformationMatrix(lhandnull_transform_localmatrix))

               lhandoptionctrl_transform_trans = lhandoptionctrl_transform.transformation()
               lhandoptionctrl_transform_worldmatrix = lhandoptionctrl_transform_trans.asMatrix()

               lhandoptionctrl_transform_localmatrix = lhandoptionctrl_transform_worldmatrix * spinenull_parentinvtransform_matrix * spinenull_childtransform_localmatrix.inverse() * lshouldernullnull_transform_localmatrix.inverse() * larmnull_transform_localmatrix.inverse() * lforearmnull_transform_localmatrix.inverse() * lhandnull_transform_localmatrix.inverse()

               lhandoptionctrl_transform.setTransformation(om2.MTransformationMatrix(lhandoptionctrl_transform_localmatrix))

               self.ctrl_mod_n.renameNode(ctrl_lhandpositive_comb_cv, "FkLeftHand_shape1")
               self.ctrl_mod_n.renameNode(ctrl_lhandnegative_comb_cv, "FkLeftHand_shape2")
               self.ctrl_mod_n.renameNode(ctrl_lhandoption_cv, "LeftHandOptions_shape")
               self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 1 "Biped_FkLeftHand_ctrl"')
               self.ctrl_mod_n.commandToExecute('color -rgbColor 1 1 0 "Biped_LeftHandOptions_ctrl"')
               self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkLeftHand_ctrl"')
               self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftHandOptions_ctrl"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_null.translateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_null.translateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_null.translateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_null.rotateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_null.rotateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_null.rotateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_null.scaleX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_null.scaleY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_null.scaleZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_null.visibility"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftHandOptions_ctrl.translateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftHandOptions_ctrl.translateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftHandOptions_ctrl.translateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftHandOptions_ctrl.rotateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftHandOptions_ctrl.rotateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftHandOptions_ctrl.rotateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftHandOptions_ctrl.scaleX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftHandOptions_ctrl.scaleY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftHandOptions_ctrl.scaleZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftHandOptions_ctrl.visibility"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingers_null.translateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingers_null.translateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingers_null.translateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingers_null.rotateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingers_null.rotateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingers_null.rotateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingers_null.scaleX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingers_null.scaleY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingers_null.scaleZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingers_null.visibility"')
               self.ctrl_mod_n.doIt()

               ctrl_hand_line_l = [om2.MPoint(1.20, 0.15), om2.MPoint(1.10, 0.00, 0.20), om2.MPoint(0.90, 0.15, 0.35)]
               ctrl_hand_line = [om2.MPoint(0.90, 0.15, 0.35), om2.MPoint(0.30, 0.30, 0.35), om2.MPoint(0.25, 0.35, 0.30), om2.MPoint(0.25, 0.35, -0.30), om2.MPoint(0.30, 0.30, -0.35), om2.MPoint(0.90, 0.15, -0.35)]
               ctrl_hand_line_r = [om2.MPoint(0.90, 0.15, -0.35), om2.MPoint(1.10, 0.00, -0.20), om2.MPoint(1.20, 0.15)]

               self.draw_lhand_tn = ctrl_tr_n.create("transform", "Draw_iklefthand_ctrl")
               crv_ctrl_hand_line_l = ctrl_cv_n.createWithEditPoints(ctrl_hand_line_l, 1, 1, False, True, True, self.draw_lhand_tn)
               crv_ctrl_hand_line = ctrl_cv_n.createWithEditPoints(ctrl_hand_line, 1, 1, False, True, True, self.draw_lhand_tn)
               crv_ctrl_hand_line_r = ctrl_cv_n.createWithEditPoints(ctrl_hand_line_r, 1, 1, False, True, True, self.draw_lhand_tn)

               self.likhandnull_tn = ctrl_tr_n.create("transform", "Biped_IkLeftHand_null", self.masterctrl_tn)
               self.likhandctrl_tn = ctrl_tr_n.create("transform", "Biped_IkLeftHand_ctrl", self.likhandnull_tn)
               ctrl_likhand_comb_cv = ctrl_cv_n.create([crv_ctrl_hand_line_l, crv_ctrl_hand_line, crv_ctrl_hand_line_r], self.likhandctrl_tn)

               likhandnull_transform = om2.MFnTransform(self.likhandnull_tn)
               likhandnull_transform.setRotatePivotTranslation(jnt_lhand_t, om2.MSpace.kTransform)

               likhandnull_transform_r = likhandnull_transform.rotation(om2.MSpace.kTransform)
               likhandnull_transform_r[0], likhandnull_transform_r[1], likhandnull_transform_r[2] = radian_lhand_x, radian_lhand_y, radian_lhand_z
               likhandnull_transform.setRotation(likhandnull_transform_r, om2.MSpace.kTransform)

               likhandctrl_transform = om2.MFnTransform(self.likhandctrl_tn)

               likhandctrl_transform_t = likhandctrl_transform.translation(om2.MSpace.kTransform)
               likhandctrl_transform_t[2] = -((jnt_lhand_t[1]+4)-jnt_lhand_t[1])
               likhandctrl_transform.setTranslation(likhandctrl_transform_t, om2.MSpace.kTransform)

               likhandctrl_transform_r = likhandctrl_transform.rotation(om2.MSpace.kTransform)
               likhandctrl_transform_r[0], likhandctrl_transform_r[2] = 1.57079, 1.57079
               likhandctrl_transform.setRotation(likhandctrl_transform_r, om2.MSpace.kTransform)

               likhandctrl_transform_s = likhandctrl_transform.findPlug("scale", False)
               if likhandctrl_transform_s.isCompound:
                   for i in range(likhandctrl_transform_s.numChildren()):
                       child_plug = likhandctrl_transform_s.child(i)
                       attr_value = child_plug.setDouble(box_transform_s[0]/3)

               self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_IkLeftHand_ctrl"')
               self.ctrl_mod_n.doIt()

               # likhandnull_transform_trans = likhandnull_transform.transformation()
               # likhandnull_transform_worldmatrix = likhandnull_transform_trans.asMatrix()
               #
               # likhandnull_transform_localmatrix = likhandnull_transform_worldmatrix * spinenull_parentinvtransform_matrix * spinenull_childtransform_localmatrix.inverse() * lshouldernullnull_transform_localmatrix.inverse() * larmnull_transform_localmatrix.inverse() * lforearmnull_transform_localmatrix.inverse()
               #
               # likhandnull_transform.setTransformation(om2.MTransformationMatrix(likhandnull_transform_localmatrix))

               likhandnull_path_n = om2.MDagPath()
               likhandnull_path = likhandnull_path_n.getAPathTo(self.likhandctrl_tn)
               likhandnull_worldtransform = om2.MFnTransform(likhandnull_path)

               likhandnull_worldtransform.setRotatePivot(om2.MPoint(jnt_lhand_t), om2.MSpace.kWorld, False)

               self.ctrl_mod_n.renameNode(ctrl_likhand_comb_cv, "IkLeftHand_shape")
               self.ctrl_mod_n.commandToExecute('color -rgbColor 1 0 0 "Biped_IkLeftHand_ctrl"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_null.translateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_null.translateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_null.translateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_null.rotateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_null.rotateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_null.rotateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_null.scaleX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_null.scaleY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_null.scaleZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_null.visibility"')
               self.ctrl_mod_n.doIt()

        try:
            lhandthumb_sl_ls = om2.MSelectionList()
            lhandthumb_sl_ls.add("LeftFingerThumb*")

            for index in range(lhandthumb_sl_ls.length()):
                jnt_lhandthumb_obj = lhandthumb_sl_ls.getDependNode(index)
                jnt_lhandthumb_path_n = om2.MDagPath()
                jnt_lhandthumb_path = jnt_lhandthumb_path_n.getAPathTo(jnt_lhandthumb_obj)
                jnt_lhandthumb_transform = om2.MFnTransform(jnt_lhandthumb_path)
                jnt_lhandthumb_t = jnt_lhandthumb_transform.translation(om2.MSpace.kWorld)

                self.lhandthumbnull_tn = ctrl_tr_n.create("transform", "Biped_LeftFingerThumb{0}_null".format(index+1))
                self.lhandthumbctrl_tn = ctrl_tr_n.create("transform", "Biped_LeftFingerThumb{0}_ctrl".format(index+1), self.lhandthumbnull_tn )
                ctrl_lhandthumbpositive_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.lhandthumbctrl_tn)
                ctrl_lhandthumbnegative_comb_cv = ctrl_cv_n.create([crv_ctrl_lhand_line_up, crv_ctrl_lhand_star, crv_ctrl_lhand_line_down], self.lhandthumbctrl_tn)

                lhandthumbnull_transform = om2.MFnTransform(self.lhandthumbnull_tn)
                lhandthumbnull_transform.setRotatePivotTranslation(jnt_lhandthumb_t, om2.MSpace.kTransform)

                jnt_lhandthumb_r = cmds.xform("LeftFingerThumb{0}".format(index+1), query=True, rotation=True, worldSpace=True)

                radian_lhandthumb_x = (jnt_lhandthumb_r[0]/180)*3.1415
                radian_lhandthumb_y = (jnt_lhandthumb_r[1]/180)*3.1415
                radian_lhandthumb_z = (jnt_lhandthumb_r[2]/180)*3.1415

                lhandthumbnull_transform_r = lhandthumbnull_transform.rotation(om2.MSpace.kTransform)
                lhandthumbnull_transform_r[0], lhandthumbnull_transform_r[1], lhandthumbnull_transform_r[2] = radian_lhandthumb_x, radian_lhandthumb_y, radian_lhandthumb_z
                lhandthumbnull_transform.setRotation(lhandthumbnull_transform_r, om2.MSpace.kTransform)

                lhandthumbctrl_transform = om2.MFnTransform(self.lhandthumbctrl_tn)

                lhandthumbctrl_transform_r = lhandthumbctrl_transform.rotation(om2.MSpace.kTransform)
                lhandthumbctrl_transform_r[1] = 1.57079
                lhandthumbctrl_transform.setRotation(lhandthumbctrl_transform_r, om2.MSpace.kTransform)

                lhandthumbctrl_transform_s = lhandthumbctrl_transform.findPlug("scale", False)
                if lhandthumbctrl_transform_s.isCompound:
                    for i in range(lhandthumbctrl_transform_s.numChildren()):
                        child_plug = lhandthumbctrl_transform_s.child(i)
                        attr_value = child_plug.setDouble(box_transform_s[0]/14)

                if index == 0:
                    lhand_tr_n = om2.MFnDagNode(self.lfingernull_tn)
                    lhand_tr_n.addChild(self.lhandthumbnull_tn)

                    lfingernull_transform_trans = lfingernull_transform.transformation()
                    lfingernull_transform_worldmatrix = lfingernull_transform_trans.asMatrixInverse()

                    lhandthumbnull_transform_trans = lhandthumbnull_transform.transformation()
                    lhandthumbnull_transform_worldmatrix = lhandthumbnull_transform_trans.asMatrix()

                    lhandthumbnull_transform_localmatrix = lhandthumbnull_transform_worldmatrix * lfingernull_transform_worldmatrix

                    lhandthumbnull_transform.setTransformation(om2.MTransformationMatrix(lhandthumbnull_transform_localmatrix))

                else:
                    lhandthumbctrl_sl_ls = om2.MSelectionList()
                    lhandthumbctrl_sl_ls.add("Biped_LeftFingerThumb*_ctrl")
                    lhandthumbctrl_obj = lhandthumbctrl_sl_ls.getDependNode(index-1)

                    lhandthumbnull_sl_ls = om2.MSelectionList()
                    lhandthumbnull_sl_ls.add("Biped_LeftFingerThumb*_null")

                    lhandthumb_tr_n = om2.MFnDagNode(lhandthumbctrl_obj)
                    lhandthumb_tr_n.addChild(self.lhandthumbnull_tn)

                    lhandthumbnull_parentinvtransform_matrix = om2.MMatrix()
                    for i in range(lhandthumbnull_sl_ls.length()-1):
                        parentobj = lhandthumbnull_sl_ls.getDependNode(i)
                        parentinvtransform = om2.MFnTransform(parentobj)
                        parentinvtransform_trans = parentinvtransform.transformation()
                        null_Matrix = parentinvtransform_trans.asMatrixInverse()

                        lhandthumbnull_parentinvtransform_matrix = lhandthumbnull_parentinvtransform_matrix * null_Matrix

                    lhandthumbnull_childtransform_trans = lhandthumbnull_transform.transformation()
                    lhandthumbnull_childtransform_worldmatrix = lhandthumbnull_childtransform_trans.asMatrix()

                    lhandthumbnull_childtransform_localmatrix = lhandthumbnull_childtransform_worldmatrix * lfingernull_transform_worldmatrix * lhandthumbnull_parentinvtransform_matrix

                    lhandthumbnull_transform.setTransformation(om2.MTransformationMatrix(lhandthumbnull_childtransform_localmatrix))

                self.ctrl_mod_n.renameNode(ctrl_lhandthumbpositive_comb_cv, "LeftFingerThumb{0}_shape1".format(index+1))
                self.ctrl_mod_n.renameNode(ctrl_lhandthumbnegative_comb_cv, "LeftFingerThumb{0}_shape2".format(index+1))
                self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 0 "Biped_LeftFingerThumb{0}_ctrl"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftFingerThumb{0}_ctrl"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_null.translateX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_null.translateY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_null.translateZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_null.rotateX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_null.rotateY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_null.rotateZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_null.scaleX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_null.scaleY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_null.scaleZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_null.visibility"'.format(index+1))
                self.ctrl_mod_n.doIt()

        except:
            pass

        try:
            lhandindex_sl_ls = om2.MSelectionList()
            lhandindex_sl_ls.add("LeftFingerIndex*")

            for index in range(lhandindex_sl_ls.length()):
                jnt_lhandindex_obj = lhandindex_sl_ls.getDependNode(index)
                jnt_lhandindex_path_n = om2.MDagPath()
                jnt_lhandindex_path = jnt_lhandindex_path_n.getAPathTo(jnt_lhandindex_obj)
                jnt_lhandindex_transform = om2.MFnTransform(jnt_lhandindex_path)
                jnt_lhandindex_t = jnt_lhandindex_transform.translation(om2.MSpace.kWorld)

                self.lhandindexnull_tn = ctrl_tr_n.create("transform", "Biped_LeftFingerIndex{0}_null".format(index + 1))
                self.lhandindexctrl_tn = ctrl_tr_n.create("transform", "Biped_LeftFingerIndex{0}_ctrl".format(index + 1), self.lhandindexnull_tn)
                ctrl_lhandIndexpositive_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.lhandindexctrl_tn)
                ctrl_lhandIndexnegative_comb_cv = ctrl_cv_n.create([crv_ctrl_lhand_line_up, crv_ctrl_lhand_star, crv_ctrl_lhand_line_down], self.lhandindexctrl_tn)

                lhandindexnull_transform = om2.MFnTransform(self.lhandindexnull_tn)
                lhandindexnull_transform.setRotatePivotTranslation(jnt_lhandindex_t, om2.MSpace.kTransform)

                jnt_lhandindex_r = cmds.xform("LeftFingerIndex{0}".format(index+1), query=True, rotation=True, worldSpace=True)

                radian_lhandIndex_x = (jnt_lhandindex_r[0]/180)*3.1415
                radian_lhandIndex_y = (jnt_lhandindex_r[1]/180)*3.1415
                radian_lhandIndex_z = (jnt_lhandindex_r[2]/180)*3.1415

                lhandindexnull_transform_r = lhandindexnull_transform.rotation(om2.MSpace.kTransform)
                lhandindexnull_transform_r[0], lhandindexnull_transform_r[1], lhandindexnull_transform_r[2] = radian_lhandIndex_x, radian_lhandIndex_y, radian_lhandIndex_z
                lhandindexnull_transform.setRotation(lhandindexnull_transform_r, om2.MSpace.kTransform)

                lhandindexctrl_transform = om2.MFnTransform(self.lhandindexctrl_tn)

                lhandindexctrl_transform_r = lhandindexctrl_transform.rotation(om2.MSpace.kTransform)
                lhandindexctrl_transform_r[1] = 1.57079
                lhandindexctrl_transform.setRotation(lhandindexctrl_transform_r, om2.MSpace.kTransform)

                lhandindexctrl_transform_s = lhandindexctrl_transform.findPlug("scale", False)
                if lhandindexctrl_transform_s.isCompound:
                    for i in range(lhandindexctrl_transform_s.numChildren()):
                        child_plug = lhandindexctrl_transform_s.child(i)
                        attr_value = child_plug.setDouble(box_transform_s[0]/14)

                if index == 0:
                    lhand_tr_n = om2.MFnDagNode(self.lfingernull_tn)
                    lhand_tr_n.addChild(self.lhandindexnull_tn)

                    lhandindexnull_transform_trans = lhandindexnull_transform.transformation()
                    lhandindexnull_transform_worldmatrix = lhandindexnull_transform_trans.asMatrix()

                    lhandindexnull_transform_localmatrix = lhandindexnull_transform_worldmatrix * lfingernull_transform_worldmatrix

                    lhandindexnull_transform.setTransformation(om2.MTransformationMatrix(lhandindexnull_transform_localmatrix))

                else:
                    lhandIndexctrl_sl_ls = om2.MSelectionList()
                    lhandIndexctrl_sl_ls.add("Biped_LeftFingerIndex*_ctrl")
                    lhandIndexctrl_obj = lhandIndexctrl_sl_ls.getDependNode(index-1)

                    lhandIndexnull_sl_ls = om2.MSelectionList()
                    lhandIndexnull_sl_ls.add("Biped_LeftFingerIndex*_null")

                    lhandIndex_tr_n = om2.MFnDagNode(lhandIndexctrl_obj)
                    lhandIndex_tr_n.addChild(self.lhandindexnull_tn)

                    lhandIndexnull_parentinvtransform_matrix = om2.MMatrix()
                    for i in range(lhandIndexnull_sl_ls.length()-1):
                        parentobj = lhandIndexnull_sl_ls.getDependNode(i)
                        parentinvtransform = om2.MFnTransform(parentobj)
                        parentinvtransform_trans = parentinvtransform.transformation()
                        null_Matrix = parentinvtransform_trans.asMatrixInverse()

                        lhandIndexnull_parentinvtransform_matrix = lhandIndexnull_parentinvtransform_matrix * null_Matrix

                    lhandindexnull_childtransform_trans = lhandindexnull_transform.transformation()
                    lhandindexnull_childtransform_worldmatrix = lhandindexnull_childtransform_trans.asMatrix()

                    lhandindexnull_childtransform_localmatrix = lhandindexnull_childtransform_worldmatrix * lfingernull_transform_worldmatrix * lhandIndexnull_parentinvtransform_matrix

                    lhandindexnull_transform.setTransformation(om2.MTransformationMatrix(lhandindexnull_childtransform_localmatrix))

                self.ctrl_mod_n.renameNode(ctrl_lhandIndexpositive_comb_cv, "LeftFingerIndex{0}_shape1".format(index+1))
                self.ctrl_mod_n.renameNode(ctrl_lhandIndexnegative_comb_cv, "LeftFingerIndex{0}_shape2".format(index+1))
                self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 0 "Biped_LeftFingerIndex{0}_ctrl"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftFingerIndex{0}_ctrl"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_null.translateX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_null.translateY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_null.translateZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_null.rotateX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_null.rotateY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_null.rotateZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_null.scaleX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_null.scaleY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_null.scaleZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_null.visibility"'.format(index+1))
                self.ctrl_mod_n.doIt()

        except:
            pass

        try:
            lhandmiddle_sl_ls = om2.MSelectionList()
            lhandmiddle_sl_ls.add("LeftFingerMiddle*")

            for index in range(lhandmiddle_sl_ls.length()):
                jnt_lhandmiddle_obj = lhandmiddle_sl_ls.getDependNode(index)
                jnt_lhandmiddle_path_n = om2.MDagPath()
                jnt_lhandmiddle_path = jnt_lhandmiddle_path_n.getAPathTo(jnt_lhandmiddle_obj)
                jnt_lhandmiddle_transform = om2.MFnTransform(jnt_lhandmiddle_path)
                jnt_lhandmiddle_t = jnt_lhandmiddle_transform.translation(om2.MSpace.kWorld)

                self.lhandmiddlenull_tn = ctrl_tr_n.create("transform", "Biped_LeftFingerMiddle{0}_null".format(index + 1))
                self.lhandmiddlectrl_tn = ctrl_tr_n.create("transform", "Biped_LeftFingerMiddle{0}_ctrl".format(index + 1), self.lhandmiddlenull_tn)
                ctrl_lhandmiddlepositive_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.lhandmiddlectrl_tn)
                ctrl_lhandmiddlenegative_comb_cv = ctrl_cv_n.create([crv_ctrl_lhand_line_up, crv_ctrl_lhand_star, crv_ctrl_lhand_line_down], self.lhandmiddlectrl_tn)

                lhandmiddlenull_transform = om2.MFnTransform(self.lhandmiddlenull_tn)
                lhandmiddlenull_transform.setRotatePivotTranslation(jnt_lhandmiddle_t, om2.MSpace.kTransform)

                jnt_lhandmiddle_r = cmds.xform("LeftFingerMiddle{0}".format(index+1), query=True, rotation=True, worldSpace=True)

                radian_lhandmiddle_x = (jnt_lhandmiddle_r[0]/180)*3.1415
                radian_lhandmiddle_y = (jnt_lhandmiddle_r[1]/180)*3.1415
                radian_lhandmiddle_z = (jnt_lhandmiddle_r[2]/180)*3.1415

                lhandmiddlenull_transform_r = lhandmiddlenull_transform.rotation(om2.MSpace.kTransform)
                lhandmiddlenull_transform_r[0], lhandmiddlenull_transform_r[1], lhandmiddlenull_transform_r[2] = radian_lhandmiddle_x, radian_lhandmiddle_y, radian_lhandmiddle_z
                lhandmiddlenull_transform.setRotation(lhandmiddlenull_transform_r, om2.MSpace.kTransform)

                lhandmiddlectrl_transform = om2.MFnTransform(self.lhandmiddlectrl_tn)

                lhandmiddlectrl_transform_s = lhandmiddlectrl_transform.findPlug("scale", False)
                if lhandmiddlectrl_transform_s.isCompound:
                    for i in range(lhandmiddlectrl_transform_s.numChildren()):
                        child_plug = lhandmiddlectrl_transform_s.child(i)
                        attr_value = child_plug.setDouble(box_transform_s[0]/14)

                lhandmiddlectrl_transform_r = lhandmiddlectrl_transform.rotation(om2.MSpace.kTransform)
                lhandmiddlectrl_transform_r[1] = 1.57079
                lhandmiddlectrl_transform.setRotation(lhandmiddlectrl_transform_r, om2.MSpace.kTransform)

                if index == 0:
                    lhand_tr_n = om2.MFnDagNode(self.lfingernull_tn)
                    lhand_tr_n.addChild(self.lhandmiddlenull_tn)

                    lhandmiddlenull_transform_trans = lhandmiddlenull_transform.transformation()
                    lhandmiddlenull_transform_worldmatrix = lhandmiddlenull_transform_trans.asMatrix()

                    lhandmiddlenull_transform_localmatrix = lhandmiddlenull_transform_worldmatrix * lfingernull_transform_worldmatrix

                    lhandmiddlenull_transform.setTransformation(om2.MTransformationMatrix(lhandmiddlenull_transform_localmatrix))

                else:
                    lhandmiddlectrl_sl_ls = om2.MSelectionList()
                    lhandmiddlectrl_sl_ls.add("Biped_LeftFingerMiddle*_ctrl")
                    lhandmiddlectrl_obj = lhandmiddlectrl_sl_ls.getDependNode(index-1)

                    lhandmiddlenull_sl_ls = om2.MSelectionList()
                    lhandmiddlenull_sl_ls.add("Biped_LeftFingerMiddle*_null")

                    lhandmiddle_tr_n = om2.MFnDagNode(lhandmiddlectrl_obj)
                    lhandmiddle_tr_n.addChild(self.lhandmiddlenull_tn)

                    lhandmiddlenull_parentinvtransform_matrix = om2.MMatrix()
                    for i in range(lhandmiddlenull_sl_ls.length()-1):
                        parentobj = lhandmiddlenull_sl_ls.getDependNode(i)
                        parentinvtransform = om2.MFnTransform(parentobj)
                        parentinvtransform_trans = parentinvtransform.transformation()
                        null_Matrix = parentinvtransform_trans.asMatrixInverse()

                        lhandmiddlenull_parentinvtransform_matrix = lhandmiddlenull_parentinvtransform_matrix * null_Matrix

                    lhandmiddlenull_childtransform_trans = lhandmiddlenull_transform.transformation()
                    lhandmiddlenull_childtransform_worldmatrix = lhandmiddlenull_childtransform_trans.asMatrix()

                    lhandmiddlenull_childtransform_localmatrix = lhandmiddlenull_childtransform_worldmatrix * lfingernull_transform_worldmatrix * lhandmiddlenull_parentinvtransform_matrix

                    lhandmiddlenull_transform.setTransformation(om2.MTransformationMatrix(lhandmiddlenull_childtransform_localmatrix))

                self.ctrl_mod_n.renameNode(ctrl_lhandmiddlepositive_comb_cv, "LeftFingerMiddle{0}_shape1".format(index+1))
                self.ctrl_mod_n.renameNode(ctrl_lhandmiddlenegative_comb_cv, "LeftFingerMiddle{0}_shape2".format(index+1))
                self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 0 "Biped_LeftFingerMiddle{0}_ctrl"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftFingerMiddle{0}_ctrl"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_null.translateX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_null.translateY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_null.translateZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_null.rotateX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_null.rotateY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_null.rotateZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_null.scaleX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_null.scaleY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_null.scaleZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_null.visibility"'.format(index+1))
                self.ctrl_mod_n.doIt()

        except:
            pass

        try:
            lhandring_sl_ls = om2.MSelectionList()
            lhandring_sl_ls.add("LeftFingerRing*")

            for index in range(lhandring_sl_ls.length()):
                jnt_lhandring_obj = lhandring_sl_ls.getDependNode(index)
                jnt_lhandring_path_n = om2.MDagPath()
                jnt_lhandring_path = jnt_lhandring_path_n.getAPathTo(jnt_lhandring_obj)
                jnt_lhandring_transform = om2.MFnTransform(jnt_lhandring_path)
                jnt_lhandring_t = jnt_lhandring_transform.translation(om2.MSpace.kWorld)

                self.lhandringnull_tn = ctrl_tr_n.create("transform", "Biped_LeftFingerRing{0}_null".format(index + 1))
                self.lhandringctrl_tn = ctrl_tr_n.create("transform", "Biped_LeftFingerRing{0}_ctrl".format(index + 1), self.lhandringnull_tn)
                ctrl_lhandringpositive_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.lhandringctrl_tn)
                ctrl_lhandringnegative_comb_cv = ctrl_cv_n.create([crv_ctrl_lhand_line_up, crv_ctrl_lhand_star, crv_ctrl_lhand_line_down], self.lhandringctrl_tn)

                lhandringnull_transform = om2.MFnTransform(self.lhandringnull_tn)
                lhandringnull_transform.setRotatePivotTranslation(jnt_lhandring_t, om2.MSpace.kTransform)

                jnt_lhandring_r = cmds.xform("LeftFingerRing{0}".format(index+1), query=True, rotation=True, worldSpace=True)

                radian_lhandring_x = (jnt_lhandring_r[0]/180)*3.1415
                radian_lhandring_y = (jnt_lhandring_r[1]/180)*3.1415
                radian_lhandring_z = (jnt_lhandring_r[2]/180)*3.1415

                lhandringnull_transform_r = lhandringnull_transform.rotation(om2.MSpace.kTransform)
                lhandringnull_transform_r[0], lhandringnull_transform_r[1], lhandringnull_transform_r[2] = radian_lhandring_x, radian_lhandring_y, radian_lhandring_z
                lhandringnull_transform.setRotation(lhandringnull_transform_r, om2.MSpace.kTransform)

                lhandringctrl_transform = om2.MFnTransform(self.lhandringctrl_tn)

                lhandringctrl_transform_s = lhandringctrl_transform.findPlug("scale", False)
                if lhandringctrl_transform_s.isCompound:
                    for i in range(lhandringctrl_transform_s.numChildren()):
                        child_plug = lhandringctrl_transform_s.child(i)
                        attr_value = child_plug.setDouble(box_transform_s[0]/14)

                lhandringctrl_transform_r = lhandringctrl_transform.rotation(om2.MSpace.kTransform)
                lhandringctrl_transform_r[1] = 1.57079
                lhandringctrl_transform.setRotation(lhandringctrl_transform_r, om2.MSpace.kTransform)

                if index == 0:
                    lhand_tr_n = om2.MFnDagNode(self.lfingernull_tn)
                    lhand_tr_n.addChild(self.lhandringnull_tn)

                    lhandringnull_transform_trans = lhandringnull_transform.transformation()
                    lhandringnull_transform_worldmatrix = lhandringnull_transform_trans.asMatrix()

                    lhandringnull_transform_localmatrix = lhandringnull_transform_worldmatrix * lfingernull_transform_worldmatrix

                    lhandringnull_transform.setTransformation(om2.MTransformationMatrix(lhandringnull_transform_localmatrix))

                else:
                    lhandringctrl_sl_ls = om2.MSelectionList()
                    lhandringctrl_sl_ls.add("Biped_LeftFingerRing*_ctrl")
                    lhandringctrl_obj = lhandringctrl_sl_ls.getDependNode(index-1)

                    lhandringnull_sl_ls = om2.MSelectionList()
                    lhandringnull_sl_ls.add("Biped_LeftFingerRing*_null")

                    lhandring_tr_n = om2.MFnDagNode(lhandringctrl_obj)
                    lhandring_tr_n.addChild(self.lhandringnull_tn)

                    lhandringnull_parentinvtransform_matrix = om2.MMatrix()
                    for i in range(lhandringnull_sl_ls.length()-1):
                        parentobj = lhandringnull_sl_ls.getDependNode(i)
                        parentinvtransform = om2.MFnTransform(parentobj)
                        parentinvtransform_trans = parentinvtransform.transformation()
                        null_Matrix = parentinvtransform_trans.asMatrixInverse()

                        lhandringnull_parentinvtransform_matrix = lhandringnull_parentinvtransform_matrix * null_Matrix

                    lhandringnull_childtransform_trans = lhandringnull_transform.transformation()
                    lhandringnull_childtransform_worldmatrix = lhandringnull_childtransform_trans.asMatrix()

                    lhandringnull_childtransform_localmatrix = lhandringnull_childtransform_worldmatrix * lfingernull_transform_worldmatrix * lhandringnull_parentinvtransform_matrix

                    lhandringnull_transform.setTransformation(om2.MTransformationMatrix(lhandringnull_childtransform_localmatrix))

                self.ctrl_mod_n.renameNode(ctrl_lhandringpositive_comb_cv, "LeftFingerRing{0}_shape1".format(index+1))
                self.ctrl_mod_n.renameNode(ctrl_lhandringnegative_comb_cv, "LeftFingerRing{0}_shape2".format(index+1))
                self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 0 "Biped_LeftFingerRing{0}_ctrl"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftFingerRing{0}_ctrl"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_null.translateX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_null.translateY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_null.translateZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_null.rotateX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_null.rotateY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_null.rotateZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_null.scaleX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_null.scaleY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_null.scaleZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_null.visibility"'.format(index+1))
                self.ctrl_mod_n.doIt()

        except:
            pass

        try:
            lhandpinky_sl_ls = om2.MSelectionList()
            lhandpinky_sl_ls.add("LeftFingerPinky*")

            for index in range(lhandpinky_sl_ls.length()):
                jnt_lhandpinky_obj = lhandpinky_sl_ls.getDependNode(index)
                jnt_lhandpinky_path_n = om2.MDagPath()
                jnt_lhandpinky_path = jnt_lhandpinky_path_n.getAPathTo(jnt_lhandpinky_obj)
                jnt_lhandpinky_transform = om2.MFnTransform(jnt_lhandpinky_path)
                jnt_lhandpinky_t = jnt_lhandpinky_transform.translation(om2.MSpace.kWorld)

                self.lhandpinkynull_tn = ctrl_tr_n.create("transform", "Biped_LeftFingerPinky{0}_null".format(index + 1))
                self.lhandpinkyctrl_tn = ctrl_tr_n.create("transform", "Biped_LeftFingerPinky{0}_ctrl".format(index + 1), self.lhandpinkynull_tn)
                ctrl_lhandpinkypositive_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.lhandpinkyctrl_tn)
                ctrl_lhandpinkynegative_comb_cv = ctrl_cv_n.create([crv_ctrl_lhand_line_up, crv_ctrl_lhand_star, crv_ctrl_lhand_line_down], self.lhandpinkyctrl_tn)

                lhandpinkynull_transform = om2.MFnTransform(self.lhandpinkynull_tn)
                lhandpinkynull_transform.setRotatePivotTranslation(jnt_lhandpinky_t, om2.MSpace.kTransform)

                jnt_lhandpinky_r = cmds.xform("LeftFingerPinky{0}".format(index+1), query=True, rotation=True, worldSpace=True)

                radian_lhandpinky_x = (jnt_lhandpinky_r[0]/180)*3.1415
                radian_lhandpinky_y = (jnt_lhandpinky_r[1]/180)*3.1415
                radian_lhandpinky_z = (jnt_lhandpinky_r[2]/180)*3.1415

                lhandpinkynull_transform_r = lhandpinkynull_transform.rotation(om2.MSpace.kTransform)
                lhandpinkynull_transform_r[0], lhandpinkynull_transform_r[1], lhandpinkynull_transform_r[2] = radian_lhandpinky_x, radian_lhandpinky_y, radian_lhandpinky_z
                lhandpinkynull_transform.setRotation(lhandpinkynull_transform_r, om2.MSpace.kTransform)

                lhandpinkyctrl_transform = om2.MFnTransform(self.lhandpinkyctrl_tn)

                lhandpinkyctrl_transform_s = lhandpinkyctrl_transform.findPlug("scale", False)
                if lhandpinkyctrl_transform_s.isCompound:
                    for i in range(lhandpinkyctrl_transform_s.numChildren()):
                        child_plug = lhandpinkyctrl_transform_s.child(i)
                        attr_value = child_plug.setDouble(box_transform_s[0]/14)

                lhandpinkyctrl_transform_r = lhandpinkyctrl_transform.rotation(om2.MSpace.kTransform)
                lhandpinkyctrl_transform_r[1] = 1.57079
                lhandpinkyctrl_transform.setRotation(lhandpinkyctrl_transform_r, om2.MSpace.kTransform)

                if index == 0:
                    lhand_tr_n = om2.MFnDagNode(self.lfingernull_tn)
                    lhand_tr_n.addChild(self.lhandpinkynull_tn)

                    lhandpinkynull_transform_trans = lhandpinkynull_transform.transformation()
                    lhandpinkynull_transform_worldmatrix = lhandpinkynull_transform_trans.asMatrix()

                    lhandpinkynull_transform_localmatrix = lhandpinkynull_transform_worldmatrix * lfingernull_transform_worldmatrix

                    lhandpinkynull_transform.setTransformation(om2.MTransformationMatrix(lhandpinkynull_transform_localmatrix))

                else:
                    lhandpinkyctrl_sl_ls = om2.MSelectionList()
                    lhandpinkyctrl_sl_ls.add("Biped_LeftFingerPinky*_ctrl")
                    lhandpinkyctrl_obj = lhandpinkyctrl_sl_ls.getDependNode(index-1)

                    lhandpinkynull_sl_ls = om2.MSelectionList()
                    lhandpinkynull_sl_ls.add("Biped_LeftFingerPinky*_null")

                    lhandpinky_tr_n = om2.MFnDagNode(lhandpinkyctrl_obj)
                    lhandpinky_tr_n.addChild(self.lhandpinkynull_tn)

                    lhandpinkynull_parentinvtransform_matrix = om2.MMatrix()
                    for i in range(lhandpinkynull_sl_ls.length()-1):
                        parentobj = lhandpinkynull_sl_ls.getDependNode(i)
                        parentinvtransform = om2.MFnTransform(parentobj)
                        parentinvtransform_trans = parentinvtransform.transformation()
                        null_Matrix = parentinvtransform_trans.asMatrixInverse()

                        lhandpinkynull_parentinvtransform_matrix = lhandpinkynull_parentinvtransform_matrix * null_Matrix

                    lhandpinkynull_childtransform_trans = lhandpinkynull_transform.transformation()
                    lhandpinkynull_childtransform_worldmatrix = lhandpinkynull_childtransform_trans.asMatrix()

                    lhandpinkynull_childtransform_localmatrix = lhandpinkynull_childtransform_worldmatrix * lfingernull_transform_worldmatrix * lhandpinkynull_parentinvtransform_matrix

                    lhandpinkynull_transform.setTransformation(om2.MTransformationMatrix(lhandpinkynull_childtransform_localmatrix))

                self.ctrl_mod_n.renameNode(ctrl_lhandpinkypositive_comb_cv, "LeftFingerPinky{0}_shape1".format(index+1))
                self.ctrl_mod_n.renameNode(ctrl_lhandpinkynegative_comb_cv, "LeftFingerPinky{0}_shape2".format(index+1))
                self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 0 "Biped_LeftFingerPinky{0}_ctrl"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftFingerPinky{0}_ctrl"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_null.translateX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_null.translateY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_null.translateZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_null.rotateX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_null.rotateY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_null.rotateZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_null.scaleX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_null.scaleY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_null.scaleZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_null.visibility"'.format(index+1))
                self.ctrl_mod_n.doIt()

        except:
            pass

        lleg_sl_ls = om2.MSelectionList()
        lleg_sl_ls.add("LeftUpLeg")
        lleg_sl_ls.add("LeftLeg")
        lleg_sl_ls.add("LeftFoot")
        lleg_sl_ls.add("LeftToeBase")

        fklleg_sl_ls = om2.MSelectionList()
        fklleg_sl_ls.add("FkLeftUpLeg")
        fklleg_sl_ls.add("FkLeftLeg")
        fklleg_sl_ls.add("FkLeftFoot")
        fklleg_sl_ls.add("FkLeftToeBase")

        for index in range(fklleg_sl_ls.length()):
                jnt_lleg_obj = fklleg_sl_ls.getDependNode(index)
                jnt_lleg_path_n = om2.MDagPath()
                jnt_lleg_path = jnt_lleg_path_n.getAPathTo(jnt_lleg_obj)
                jnt_lleg_transform = om2.MFnTransform(jnt_lleg_path)
                jnt_lleg_t = jnt_lleg_transform.translation(om2.MSpace.kWorld)

                if index == 0:
                    self.luplegnull_tn = ctrl_tr_n.create("transform", "Biped_FkLeftUpLeg_null", self.rootctrl_tn)
                    self.luplegupctrl_tn = ctrl_tr_n.create("transform", "Biped_FkLeftUpLeg_ctrl", self.luplegnull_tn)
                    ctrl_luplegpositive_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.luplegupctrl_tn)

                    luplegnull_transform = om2.MFnTransform(self.luplegnull_tn)
                    luplegnull_transform.setTranslation(jnt_lleg_t, om2.MSpace.kTransform)

                    jnt_lupleg_r = cmds.xform("LeftUpLeg", query=True, rotation=True, worldSpace=True)

                    radian_llegtoebasenull_x = (jnt_lupleg_r[0]/180)*3.1415
                    radian_llegtoebasenull_y = (jnt_lupleg_r[1]/180)*3.1415
                    radian_llegtoebasenull_z = (jnt_lupleg_r[2]/180)*3.1415

                    luplegnull_transform_r = luplegnull_transform.rotation(om2.MSpace.kTransform)
                    luplegnull_transform_r[0], luplegnull_transform_r[1], luplegnull_transform_r[2] = radian_llegtoebasenull_x, radian_llegtoebasenull_y, radian_llegtoebasenull_z
                    luplegnull_transform.setRotation(luplegnull_transform_r, om2.MSpace.kTransform)

                    luplegnctrl_transform = om2.MFnTransform(self.luplegupctrl_tn)

                    luplegnctrl_transform_r = luplegnull_transform.rotation(om2.MSpace.kTransform)
                    luplegnctrl_transform_r[0], luplegnctrl_transform_r[1], luplegnctrl_transform_r[2] = 0, 1.57079, 0
                    luplegnctrl_transform.setRotation(luplegnctrl_transform_r, om2.MSpace.kTransform)

                    luplegnctrl_transform_s = luplegnctrl_transform.findPlug("scale", False)
                    if luplegnctrl_transform_s.isCompound:
                        for i in range(luplegnctrl_transform_s.numChildren()):
                            child_plug = luplegnctrl_transform_s.child(i)
                            attr_value = child_plug.setDouble(box_transform_s[0]/2)

                    luplegnull_transform_trans = luplegnull_transform.transformation()
                    luplegnull_transform_worldmatrix = luplegnull_transform_trans.asMatrix()

                    luplegnull_transform_localmatrix = luplegnull_transform_worldmatrix * rootctrl_transform_worldmatrix

                    luplegnull_transform.setTransformation(om2.MTransformationMatrix(luplegnull_transform_localmatrix))

                    self.ctrl_mod_n.renameNode(ctrl_luplegpositive_comb_cv, "LeftUpLeg_shape")
                    self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 1 "Biped_FkLeftUpLeg_ctrl"')
                    self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkLeftUpLeg_ctrl"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_null.translateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_null.translateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_null.translateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_null.rotateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_null.rotateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_null.rotateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_null.scaleX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_null.scaleY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_null.scaleZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_null.visibility"')
                    self.ctrl_mod_n.doIt()

                elif index == 1:
                    self.llegnull_tn = ctrl_tr_n.create("transform", "Biped_FkLeftLeg_null", self.luplegupctrl_tn)
                    self.llegctrl_tn = ctrl_tr_n.create("transform", "Biped_FkLeftLeg_ctrl", self.llegnull_tn)
                    ctrl_llegpositive_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.llegctrl_tn)
                    
                    ctrl_knee_triangle_points = [om2.MPoint(1.0, 0.0), om2.MPoint(0.0, 0.0, 1.0), om2.MPoint(-1.0, 0.0), om2.MPoint(0.0, 0.0, -1.0), om2.MPoint(1.0, 0.0)]
                    ctrl_knee_arrow_points = [om2.MPoint(0.0, 0.0), om2.MPoint(0.0, 1.0), om2.MPoint(0.0, 0.8, 0.1), om2.MPoint(0.0, 1.0), om2.MPoint(-0.1, 0.8), om2.MPoint(0.0, 1.0), om2.MPoint(0.0, 0.8, -0.1), om2.MPoint(0.0, 1.0), om2.MPoint(0.1, 0.8)]

                    self.pvllegkneenull_tn = ctrl_tr_n.create("transform", "Biped_PVLeftKnee_null", self.masterctrl_tn)
                    self.pvllegknectrl_tn = ctrl_tr_n.create("transform", "Biped_PVLeftKnee_ctrl", self.pvllegkneenull_tn)
                    crv_ctrl_knee_triangle_l = ctrl_cv_n.createWithEditPoints(ctrl_knee_triangle_points, 1, 1, False, True, True, self.pvllegknectrl_tn)
                    crv_ctrl_knee_arrow_l = ctrl_cv_n.createWithEditPoints(ctrl_knee_arrow_points, 1, 1, False, True, True, self.pvllegknectrl_tn)

                    llegnull_transform = om2.MFnTransform(self.llegnull_tn)
                    llegnull_transform.setRotatePivotTranslation(jnt_lleg_t, om2.MSpace.kTransform)

                    pvllegkneenull_transform = om2.MFnTransform(self.pvllegkneenull_tn)
                    pvllegkneenull_transform.setTranslation(jnt_lleg_t, om2.MSpace.kTransform)

                    jnt_lleg_r = cmds.xform("LeftLeg", query=True, rotation=True, worldSpace=True)

                    radian_llegnull_x = (jnt_lleg_r[0]/180)*3.1415
                    radian_llegnull_y = (jnt_lleg_r[1]/180)*3.1415
                    radian_llegnull_z = (jnt_lleg_r[2]/180)*3.1415

                    llegnull_transform_r = llegnull_transform.rotation(om2.MSpace.kTransform)
                    llegnull_transform_r[0], llegnull_transform_r[1], llegnull_transform_r[2] = radian_llegnull_x, radian_llegnull_y, radian_llegnull_z
                    llegnull_transform.setRotation(llegnull_transform_r, om2.MSpace.kTransform)

                    llegctrl_transform = om2.MFnTransform(self.llegctrl_tn)

                    pvllegknectrl_transform = om2.MFnTransform(self.pvllegknectrl_tn)

                    llegctrl_transform_r = llegnull_transform.rotation(om2.MSpace.kTransform)
                    llegctrl_transform_r[0], llegctrl_transform_r[1], llegctrl_transform_r[2] = 0, 1.57079, 0
                    llegctrl_transform.setRotation(llegctrl_transform_r, om2.MSpace.kTransform)

                    pvllegkneenull_transform_t = pvllegkneenull_transform.translation(om2.MSpace.kTransform)
                    pvllegkneenull_transform_t[2] = pvllegkneenull_transform_t[2]+8
                    pvllegkneenull_transform.setTranslation(pvllegkneenull_transform_t, om2.MSpace.kTransform)

                    pvllegknectrl_transform_r = pvllegknectrl_transform.rotation(om2.MSpace.kTransform)
                    pvllegknectrl_transform_r[0] = 1.57079
                    pvllegknectrl_transform.setRotation(pvllegknectrl_transform_r, om2.MSpace.kTransform)

                    llegctrl_transform_s = llegctrl_transform.findPlug("scale", False)
                    if llegctrl_transform_s.isCompound:
                        for i in range(llegctrl_transform_s.numChildren()):
                            child_plug = llegctrl_transform_s.child(i)
                            attr_value = child_plug.setDouble(box_transform_s[0]/2)

                    llegnull_transform_trans = llegnull_transform.transformation()
                    llegnull_transform_worldmatrix = llegnull_transform_trans.asMatrix()

                    llegnull_transform_localmatrix = llegnull_transform_worldmatrix * rootctrl_transform_worldmatrix * luplegnull_transform_localmatrix.inverse()

                    llegnull_transform.setTransformation(om2.MTransformationMatrix(llegnull_transform_localmatrix))

                    self.ctrl_mod_n.renameNode(ctrl_llegpositive_comb_cv, "LeftLeg_shape")
                    self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 1 "Biped_FkLeftLeg_ctrl"')
                    self.ctrl_mod_n.commandToExecute('color -rgbColor 1 1 0 "Biped_PVLeftKnee_ctrl"')
                    self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkLeftLeg_ctrl"')
                    self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_PVLeftKnee_ctrl"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_null.translateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_null.translateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_null.translateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_null.rotateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_null.rotateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_null.rotateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_null.scaleX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_null.scaleY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_null.scaleZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_null.visibility"')
                    self.ctrl_mod_n.doIt()

                elif index == 2:
                    self.llegfootnull_tn = ctrl_tr_n.create("transform", "Biped_FkLeftFoot_null", self.llegctrl_tn)
                    self.llegfootctrl_tn = ctrl_tr_n.create("transform", "Biped_FkLeftFoot_ctrl", self.llegfootnull_tn)
                    ctrl_llegfootpositive_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.llegfootctrl_tn)

                    self.liklegfootnull_tn = ctrl_tr_n.create("transform", "Biped_IkLeftFoot_null", self.masterctrl_tn)
                    self.liklegfootoffsetnull_tn = ctrl_tr_n.create("transform", "Biped_IkLeftFootOffset_null", self.liklegfootnull_tn)
                    self.liklegfootctrl_tn = ctrl_tr_n.create("transform", "Biped_IkLeftFoot_ctrl", self.liklegfootoffsetnull_tn)
                    ctrl_liklegfootpositive_comb_cv = ctrl_cv_n.create([crv_ctrl_hand_line_l, crv_ctrl_hand_line, crv_ctrl_hand_line_r], self.liklegfootctrl_tn)

                    self.lfootoption_tn = ctrl_tr_n.create("transform", "Biped_LeftFootOptions_ctrl", lleg_sl_ls.getDependNode(2))
                    ctrl_lfootoption_cv = ctrl_cv_n.createWithEditPoints(ctrl_lhandoption_line, 1, 1, False, True, True, self.lfootoption_tn)

                    self.noflipllegkneenull_tn = ctrl_tr_n.create("transform", "Biped_NoFlipLeftKnee_null", self.liklegfootoffsetnull_tn)
                    self.noflipllegkneectrl_tn = ctrl_tr_n.create("transform", "Biped_NoFlipLeftKnee_ctrl", self.noflipllegkneenull_tn)
                    self.noflipllegknectrl_tn = ctrl_tr_n.create("locator", "NoFlipLeftKnee_shape", self.noflipllegkneectrl_tn)

                    llegfootnull_transform = om2.MFnTransform(self.llegfootnull_tn)
                    llegfootnull_transform.setRotatePivotTranslation(jnt_lleg_t, om2.MSpace.kTransform)

                    liklegfootnull_transform = om2.MFnTransform(self.liklegfootnull_tn)
                    liklegfootnull_transform.setTranslation(jnt_lleg_t, om2.MSpace.kTransform)

                    liklegfootoffsetnull_transform = om2.MFnTransform(self.liklegfootoffsetnull_tn)

                    lfootoptionctrl_transform = om2.MFnTransform(self.lfootoption_tn)
                    lfootoptionctrl_transform.setRotatePivotTranslation(jnt_lleg_t, om2.MSpace.kTransform)

                    jnt_llegfoot_r = cmds.xform("LeftFoot", query=True, rotation=True, worldSpace=True)

                    radian_llegfootnull_x = (jnt_llegfoot_r[0]/180)*3.1415
                    radian_llegfootnull_y = (jnt_llegfoot_r[1]/180)*3.1415
                    radian_llegfootnull_z = (jnt_llegfoot_r[2]/180)*3.1415

                    llegfootnull_transform_r = llegfootnull_transform.rotation(om2.MSpace.kTransform)
                    llegfootnull_transform_r[0], llegfootnull_transform_r[1], llegfootnull_transform_r[2] = radian_llegfootnull_x, radian_llegfootnull_y, radian_llegfootnull_z
                    llegfootnull_transform.setRotation(llegfootnull_transform_r, om2.MSpace.kTransform)

                    liklegfootnull_transform.setRotation(llegfootnull_transform_r, om2.MSpace.kTransform)

                    liklegfootoffsetnull_transform.setRotation(llegfootnull_transform_r, om2.MSpace.kTransform)

                    llegfootctrl_transform = om2.MFnTransform(self.llegfootctrl_tn)

                    liklegfootctrl_transform = om2.MFnTransform(self.liklegfootctrl_tn)

                    noflipllegkneenull_transform = om2.MFnTransform(self.noflipllegkneectrl_tn)

                    llegfootctrl_transform_r = llegfootnull_transform.rotation(om2.MSpace.kTransform)
                    llegfootctrl_transform_r[0], llegfootctrl_transform_r[1], llegfootctrl_transform_r[2] = -1.57079, 0, -1.57079
                    llegfootctrl_transform.setRotation(llegfootctrl_transform_r, om2.MSpace.kTransform)

                    liklegfootctrl_transform_t = liklegfootctrl_transform.translation(om2.MSpace.kTransform)
                    liklegfootctrl_transform_t[1], liklegfootctrl_transform_t[2] = -1, -(jnt_lleg_t[2]+2)
                    liklegfootctrl_transform.setTranslation(liklegfootctrl_transform_t, om2.MSpace.kTransform)

                    liklegfootctrl_transform_r = liklegfootctrl_transform.rotation(om2.MSpace.kTransform)
                    liklegfootctrl_transform_r[1] = -1.57079
                    liklegfootctrl_transform.setRotation(liklegfootctrl_transform_r, om2.MSpace.kTransform)

                    lfootoptionctrl_transform_t = lfootoptionctrl_transform.translation(om2.MSpace.kTransform)
                    lfootoptionctrl_transform_t[0] = jnt_lleg_t[0]+7
                    lfootoptionctrl_transform.setTranslation(lfootoptionctrl_transform_t, om2.MSpace.kTransform)

                    lfootoptionctrl_transform_r = lfootoptionctrl_transform.rotation(om2.MSpace.kTransform)
                    lfootoptionctrl_transform_r[0] = -1.57079
                    lfootoptionctrl_transform.setRotation(lfootoptionctrl_transform_r, om2.MSpace.kTransform)

                    noflipllegkneenull_transform_t = noflipllegkneenull_transform.translation(om2.MSpace.kTransform)
                    noflipllegkneenull_transform_t[0] = 7
                    noflipllegkneenull_transform.setTranslation(noflipllegkneenull_transform_t, om2.MSpace.kTransform)

                    llegfootctrl_transform_s = llegfootctrl_transform.findPlug("scale", False)
                    if llegfootctrl_transform_s.isCompound:
                        for i in range(llegfootctrl_transform_s.numChildren()):
                            child_plug = llegfootctrl_transform_s.child(i)
                            attr_value = child_plug.setDouble(box_transform_s[0]/2)

                    liklegfootctrl_transform_s = liklegfootctrl_transform.findPlug("scale", False)
                    if liklegfootctrl_transform_s.isCompound:
                        for i in range(liklegfootctrl_transform_s.numChildren()):
                            child_plug = liklegfootctrl_transform_s.child(i)
                            attr_value = child_plug.setDouble(box_transform_s[0]/2)

                    llegfootnull_transform_trans = llegfootnull_transform.transformation()
                    llegfootnull_transform_worldmatrix = llegfootnull_transform_trans.asMatrix()

                    llegfootnull_transform_localmatrix = llegfootnull_transform_worldmatrix * rootctrl_transform_worldmatrix * luplegnull_transform_localmatrix.inverse() * llegnull_transform_localmatrix.inverse()

                    llegfootnull_transform.setTransformation(om2.MTransformationMatrix(llegfootnull_transform_localmatrix))

                    lfootoptionctrl_transform_trans = lfootoptionctrl_transform.transformation()
                    lfootoptionctrl_transform_worldmatrix = lfootoptionctrl_transform_trans.asMatrix()

                    lfootoptionctrl_transform_localmatrix = lfootoptionctrl_transform_worldmatrix * rootctrl_transform_worldmatrix * luplegnull_transform_localmatrix.inverse() * llegnull_transform_localmatrix.inverse() * llegfootnull_transform_localmatrix.inverse()

                    lfootoptionctrl_transform.setTransformation(om2.MTransformationMatrix(lfootoptionctrl_transform_localmatrix))

                    self.ctrl_mod_n.renameNode(ctrl_llegfootpositive_comb_cv, "LeftLegFoot_shape")
                    self.ctrl_mod_n.renameNode(ctrl_liklegfootpositive_comb_cv, "LeftIkLegFoot_shape")
                    self.ctrl_mod_n.renameNode(ctrl_lfootoption_cv, "LeftFootOptions_shape")
                    self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 1 "Biped_FkLeftFoot_ctrl"')
                    self.ctrl_mod_n.commandToExecute('color -rgbColor 1 0 1 "Biped_IkLeftFoot_ctrl"')
                    self.ctrl_mod_n.commandToExecute('color -rgbColor 1 1 0 "Biped_LeftFootOptions_ctrl"')
                    self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkLeftFoot_ctrl"')
                    self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_IkLeftFoot_ctrl"')
                    self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftFootOptions_ctrl"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_null.translateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_null.translateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_null.translateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_null.rotateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_null.rotateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_null.rotateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_null.scaleX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_null.scaleY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_null.scaleZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_null.visibility"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_null.translateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_null.translateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_null.translateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_null.rotateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_null.rotateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_null.rotateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_null.scaleX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_null.scaleY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_null.scaleZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_null.visibility"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFootOffset_null.translateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFootOffset_null.translateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFootOffset_null.translateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFootOffset_null.rotateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFootOffset_null.rotateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFootOffset_null.rotateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFootOffset_null.scaleX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFootOffset_null.scaleY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFootOffset_null.scaleZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFootOffset_null.visibility"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFootOptions_ctrl.translateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFootOptions_ctrl.translateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFootOptions_ctrl.translateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFootOptions_ctrl.rotateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFootOptions_ctrl.rotateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFootOptions_ctrl.rotateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFootOptions_ctrl.scaleX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFootOptions_ctrl.scaleY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFootOptions_ctrl.scaleZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFootOptions_ctrl.visibility"')
                    self.ctrl_mod_n.doIt()

                    liklegfootctrl_path_n = om2.MDagPath()
                    liklegfootctrl_path = liklegfootctrl_path_n.getAPathTo(self.liklegfootctrl_tn)
                    liklegfootctrl_worldtransform = om2.MFnTransform(liklegfootctrl_path)

                    liklegfootctrl_worldtransform.setRotatePivot(om2.MPoint(jnt_lleg_t), om2.MSpace.kWorld, False)

                elif index == 3:
                    self.llegtoebasenull_tn = ctrl_tr_n.create("transform", "Biped_FkLeftToeBase_null", self.llegfootctrl_tn)
                    self.llegtoebasectrl_tn = ctrl_tr_n.create("transform", "Biped_FkLeftToeBase_ctrl", self.llegtoebasenull_tn)
                    ctrl_llegtoepositive_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.llegtoebasectrl_tn)

                    llegtoebasenull_transform = om2.MFnTransform(self.llegtoebasenull_tn)
                    llegtoebasenull_transform.setRotatePivotTranslation(jnt_lleg_t, om2.MSpace.kTransform)

                    jnt_llegtoebase_r = cmds.xform("LeftToeBase", query=True, rotation=True, worldSpace=True)

                    radian_llegtoebasenull_x = (jnt_llegtoebase_r[0]/180)*3.1415
                    radian_llegtoebasenull_y = (jnt_llegtoebase_r[1]/180)*3.1415
                    radian_llegtoebasenull_z = (jnt_llegtoebase_r[2]/180)*3.1415

                    llegtoebasenull_transform_r = llegtoebasenull_transform.rotation(om2.MSpace.kTransform)
                    llegtoebasenull_transform_r[0], llegtoebasenull_transform_r[1], llegtoebasenull_transform_r[2] = radian_llegtoebasenull_x, radian_llegtoebasenull_y, radian_llegtoebasenull_z
                    llegtoebasenull_transform.setRotation(llegtoebasenull_transform_r, om2.MSpace.kTransform)

                    llegtoebasectrl_transform = om2.MFnTransform(self.llegtoebasectrl_tn)

                    llegtoebasectrl_transform_r = llegtoebasectrl_transform.rotation(om2.MSpace.kTransform)
                    llegtoebasectrl_transform_r[1] = -1.57079
                    llegtoebasectrl_transform.setRotation(llegtoebasectrl_transform_r, om2.MSpace.kTransform)

                    llegtoebasectrl_transform_s = llegtoebasectrl_transform.findPlug("scale", False)
                    if llegtoebasectrl_transform_s.isCompound:
                        for i in range(llegtoebasectrl_transform_s.numChildren()):
                            child_plug = llegtoebasectrl_transform_s.child(i)
                            attr_value = child_plug.setDouble(box_transform_s[0]/4)

                    llegtoebasenull_transform_trans = llegtoebasenull_transform.transformation()
                    llegtoebasenull_transform_worldmatrix = llegtoebasenull_transform_trans.asMatrix()

                    llegtoebasenull_transform_localmatrix = llegtoebasenull_transform_worldmatrix * rootctrl_transform_worldmatrix * luplegnull_transform_localmatrix.inverse() * llegnull_transform_localmatrix.inverse() * llegfootnull_transform_localmatrix.inverse()

                    llegtoebasenull_transform.setTransformation(om2.MTransformationMatrix(llegtoebasenull_transform_localmatrix))

                    self.ctrl_mod_n.renameNode(ctrl_llegtoepositive_comb_cv, "LeftLegToeBase_shape")
                    self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 1 "Biped_FkLeftToeBase_ctrl"')
                    self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkLeftToeBase_ctrl"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_null.translateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_null.translateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_null.translateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_null.rotateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_null.rotateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_null.rotateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_null.scaleX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_null.scaleY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_null.scaleZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_null.visibility"')
                    self.ctrl_mod_n.doIt()

        rarm_sl_ls = om2.MSelectionList()
        rarm_sl_ls.add("RightArm")
        rarm_sl_ls.add("RightForeArm")
        rarm_sl_ls.add("RightHand")

        fkrarm_sl_ls = om2.MSelectionList()
        fkrarm_sl_ls.add("RightShoulder")
        fkrarm_sl_ls.add("FkRightArm")
        fkrarm_sl_ls.add("FkRightForeArm")
        fkrarm_sl_ls.add("FkRightHand")

        ctrl_rshoulder_arc_l = [om2.MPoint(1.20, 0.15), om2.MPoint(1.10, 0.28, 0.10), om2.MPoint(0.90, 0.35, 0.25)]
        ctrl_rshoulder_line = [om2.MPoint(0.90, 0.35, 0.25), om2.MPoint(0.30, 0.50, 0.25), om2.MPoint(0.25, 0.55, 0.20), om2.MPoint(0.25, 0.55, -0.20), om2.MPoint(0.30, 0.50, -0.25), om2.MPoint(0.90, 0.35, -0.25)]
        ctrl_rshoulder_arc_r = [om2.MPoint(0.90, 0.35, -0.25), om2.MPoint(1.10, 0.28, -0.10), om2.MPoint(1.20, 0.15)]

        self.draw_shoulder_tn = ctrl_tr_n.create("transform", "Draw_shoulder_ctrl")
        crv_ctrl_rshoulder_arc_l = ctrl_cv_n.createWithEditPoints(ctrl_rshoulder_arc_l, 3, 1, False, True, True, self.draw_shoulder_tn)
        crv_ctrl_rshoulder_line = ctrl_cv_n.createWithEditPoints(ctrl_rshoulder_line, 1, 1, False, True, True, self.draw_shoulder_tn)
        crv_ctrl_rshoulder_arc_r = ctrl_cv_n.createWithEditPoints(ctrl_rshoulder_arc_r, 3, 1, False, True, True, self.draw_shoulder_tn)

        if self.autostretch.currentIndex() == 1:
            self.rshouldernull_tn = ctrl_tr_n.create("transform", "Biped_RightShoulder_null", self.stretchyspine_tn)
        else:
            self.rshouldernull_tn = ctrl_tr_n.create("transform", "Biped_RightShoulder_null", self.spinectrl_tn)

        self.rshoulderctrl_tn = ctrl_tr_n.create("transform", "Biped_RightShoulder_ctrl", self.rshouldernull_tn)
        ctrl_rshoulder_comb_cv = ctrl_cv_n.create([crv_ctrl_rshoulder_arc_l, crv_ctrl_rshoulder_line, crv_ctrl_rshoulder_arc_r], self.rshoulderctrl_tn)

        jnt_rshoulder_obj = fkrarm_sl_ls.getDependNode(0)
        rshoulder_path_n = om2.MDagPath()
        rshoulder_path = rshoulder_path_n.getAPathTo(jnt_rshoulder_obj)
        jnt_rshoulder_transform = om2.MFnTransform(rshoulder_path)
        jnt_rshoulder_t = jnt_rshoulder_transform.translation(om2.MSpace.kWorld)

        rshouldernull_transform = om2.MFnTransform(self.rshouldernull_tn)
        rshouldernull_transform.setRotatePivotTranslation(jnt_rshoulder_t, om2.MSpace.kTransform)

        jnt_rshoulder_r = cmds.xform("RightShoulder", query=True, rotation=True, worldSpace=True)

        radian_rshoulder_x = (jnt_rshoulder_r[0]/180)*3.1415
        radian_rshoulder_y = (jnt_rshoulder_r[1]/180)*3.1415
        radian_rshoulder_z = (jnt_rshoulder_r[2]/180)*3.1415

        rshouldernull_transform_r = rshouldernull_transform.rotation(om2.MSpace.kTransform)
        rshouldernull_transform_r[0], rshouldernull_transform_r[1], rshouldernull_transform_r[2] = radian_rshoulder_x, radian_rshoulder_y, radian_rshoulder_z
        rshouldernull_transform.setRotation(rshouldernull_transform_r, om2.MSpace.kTransform)

        rshoulderctrl_transform = om2.MFnTransform(self.rshoulderctrl_tn)

        rshoulderctrl_transform_r = rshoulderctrl_transform.rotation(om2.MSpace.kTransform)
        rshoulderctrl_transform_r[0], rshoulderctrl_transform_r[1], rshoulderctrl_transform_r[2] = -1.57079, 0.7853, 1.57079
        rshoulderctrl_transform.setRotation(rshoulderctrl_transform_r, om2.MSpace.kTransform)

        rshoulderctrl_transform_s = rshoulderctrl_transform.findPlug("scale", False)
        if rshoulderctrl_transform_s.isCompound:
            for i in range(rshoulderctrl_transform_s.numChildren()):
                child_plug = rshoulderctrl_transform_s.child(i)
                attr_value = child_plug.setDouble(box_transform_s[0]/3)

        rshouldernullnull_transform_trans = rshouldernull_transform.transformation()
        rshouldernullnull_transform_worldmatrix = rshouldernullnull_transform_trans.asMatrix()

        rshouldernullnull_transform_localmatrix = rshouldernullnull_transform_worldmatrix * spinenull_parentinvtransform_matrix * spinenull_childtransform_localmatrix.inverse()

        rshouldernull_transform.setTransformation(om2.MTransformationMatrix(rshouldernullnull_transform_localmatrix))

        rshoulderctrl_path_n = om2.MDagPath()
        rshoulderctrl_path = rshoulderctrl_path_n.getAPathTo(self.rshoulderctrl_tn)
        rshoulderctrl_worldtransform = om2.MFnTransform(rshoulderctrl_path)

        rshoulderctrl_worldtransform.setRotatePivot(om2.MPoint(jnt_rshoulder_t), om2.MSpace.kWorld, False)

        self.ctrl_mod_n.commandToExecute('delete "Draw_shoulder_ctrl"')
        self.ctrl_mod_n.renameNode(ctrl_rshoulder_comb_cv, "RightShoulder_shape")
        self.ctrl_mod_n.commandToExecute('color -rgbColor 1 0 0 "Biped_RightShoulder_ctrl"')
        self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightShoulder_ctrl"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_null.translateX"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_null.translateY"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_null.translateZ"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_null.rotateX"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_null.rotateY"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_null.rotateZ"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_null.scaleX"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_null.scaleY"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_null.scaleZ"')
        self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_null.visibility"')
        self.ctrl_mod_n.doIt()

        for index in range(fkrarm_sl_ls.length()):
           jnt_rhand_obj = fkrarm_sl_ls.getDependNode(index)
           rhand_path_n = om2.MDagPath()
           rhand_path = rhand_path_n.getAPathTo(jnt_rhand_obj)
           jnt_rhand_transform = om2.MFnTransform(rhand_path)
           jnt_rhand_t = jnt_rhand_transform.translation(om2.MSpace.kWorld)

           if index == 1:
               self.rarmnull_tn = ctrl_tr_n.create("transform", "Biped_FkRightArm_null", self.rshoulderctrl_tn)
               self.rarmctrl_tn = ctrl_tr_n.create("transform", "Biped_FkRightArm_ctrl", self.rarmnull_tn)
               ctrl_larm_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rarmctrl_tn)

               rarmnull_transform = om2.MFnTransform(self.rarmnull_tn)
               rarmnull_transform.setRotatePivotTranslation(jnt_rhand_t, om2.MSpace.kTransform)

               jnt_rarm_r = cmds.xform("RightArm", query=True, rotation=True, worldSpace=True)

               radian_rarm_x = (jnt_rarm_r[0]/180)*3.1415
               radian_rarm_y = (jnt_rarm_r[1]/180)*3.1415
               radian_rarm_z = (jnt_rarm_r[2]/180)*3.1415

               rarmnull_transform_r = rarmnull_transform.rotation(om2.MSpace.kTransform)
               rarmnull_transform_r[0], rarmnull_transform_r[1], rarmnull_transform_r[2] = radian_rarm_x, radian_rarm_y, radian_rarm_z
               rarmnull_transform.setRotation(rarmnull_transform_r, om2.MSpace.kTransform)

               rarmctrl_transform = om2.MFnTransform(self.rarmctrl_tn)

               rarmctrl_transform_r = rarmctrl_transform.rotation(om2.MSpace.kTransform)
               rarmctrl_transform_r[1] = 3.1415
               rarmctrl_transform.setRotation(rarmctrl_transform_r, om2.MSpace.kTransform)

               rarmctrl_transform_s = rarmctrl_transform.findPlug("scale", False)
               if rarmctrl_transform_s.isCompound:
                   for i in range(rarmctrl_transform_s.numChildren()):
                       child_plug = rarmctrl_transform_s.child(i)
                       attr_value = child_plug.setDouble(box_transform_s[0]/2)

               rarmnull_transform_trans = rarmnull_transform.transformation()
               rarmnull_transform_worldmatrix = rarmnull_transform_trans.asMatrix()

               rarmnull_transform_localmatrix = rarmnull_transform_worldmatrix * spinenull_parentinvtransform_matrix * spinenull_childtransform_localmatrix.inverse() * rshouldernullnull_transform_localmatrix.inverse()

               rarmnull_transform.setTransformation(om2.MTransformationMatrix(rarmnull_transform_localmatrix))

               self.ctrl_mod_n.renameNode(ctrl_larm_comb_cv, "FkRightArm_shape")
               self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 1 "Biped_FkRightArm_ctrl"')
               self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkRightArm_ctrl"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.translateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.translateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.translateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.rotateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.rotateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.rotateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.scaleX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.scaleY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.scaleZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.visibility"')
               self.ctrl_mod_n.doIt()

           elif index == 2:
               self.rforearmnull_tn = ctrl_tr_n.create("transform", "Biped_FkRightForeArm_null", self.rarmctrl_tn)
               self.rforearmctrl_tn = ctrl_tr_n.create("transform", "Biped_FkRightForeArm_ctrl", self.rforearmnull_tn)
               ctrl_rforearm_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rforearmctrl_tn)

               rforearmnull_transform = om2.MFnTransform(self.rforearmnull_tn)
               rforearmnull_transform.setRotatePivotTranslation(jnt_rhand_t, om2.MSpace.kTransform)

               jnt_rforearm_r = cmds.xform("RightForeArm", query=True, rotation=True, worldSpace=True)

               radian_rforearm_x = (jnt_rforearm_r[0]/180)*3.1415
               radian_rforearm_y = (jnt_rforearm_r[1]/180)*3.1415
               radian_rforearm_z = (jnt_rforearm_r[2]/180)*3.1415

               rforearmnull_transform_r = rforearmnull_transform.rotation(om2.MSpace.kTransform)
               rforearmnull_transform_r[0], rforearmnull_transform_r[1], rforearmnull_transform_r[2] = radian_rforearm_x, radian_rforearm_y, radian_rforearm_z
               rforearmnull_transform.setRotation(rforearmnull_transform_r, om2.MSpace.kTransform)

               rforearmctrl_transform = om2.MFnTransform(self.rforearmctrl_tn)

               rforearmctrl_transform_r = rforearmctrl_transform.rotation(om2.MSpace.kTransform)
               rforearmctrl_transform_r[1] = 3.1415
               rforearmctrl_transform.setRotation(rforearmctrl_transform_r, om2.MSpace.kTransform)

               rforearmctrl_transform_s = rforearmctrl_transform.findPlug("scale", False)
               if rforearmctrl_transform_s.isCompound:
                   for i in range(rforearmctrl_transform_s.numChildren()):
                       child_plug = rforearmctrl_transform_s.child(i)
                       attr_value = child_plug.setDouble(box_transform_s[0]/2)

               rforearmnull_transform_trans = rforearmnull_transform.transformation()
               rforearmnull_transform_worldmatrix = rforearmnull_transform_trans.asMatrix()

               rforearmnull_transform_localmatrix = rforearmnull_transform_worldmatrix * spinenull_parentinvtransform_matrix * spinenull_childtransform_localmatrix.inverse() * rshouldernullnull_transform_localmatrix.inverse() * rarmnull_transform_localmatrix.inverse()

               rforearmnull_transform.setTransformation(om2.MTransformationMatrix(rforearmnull_transform_localmatrix))

               self.ctrl_mod_n.renameNode(ctrl_rforearm_comb_cv, "FkRightForeArm_shape")
               self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 1 "Biped_FkRightForeArm_ctrl"')
               self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkRightForeArm_ctrl"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_null.translateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_null.translateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_null.translateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_null.rotateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_null.rotateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_null.rotateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_null.scaleX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_null.scaleY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_null.scaleZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_null.visibility"')
               self.ctrl_mod_n.doIt()
        #
           elif index == 3:
               ctrl_rhand_line_up_points = [om2.MPoint(0.00, 0.05, 0.02), om2.MPoint(-0.60, 0.05, 0.02)]
               ctrl_rhand_star_up_points = [om2.MPoint(-0.60, 0.05, 0.02), om2.MPoint(-0.70, 0.15, 0.20), om2.MPoint(-0.70, 0.09, 0.20), om2.MPoint(-0.70, 0.06, 0.13), om2.MPoint(-0.60, 0.00, 0.00), om2.MPoint(-0.70, 0.05, -0.13), om2.MPoint(-0.70, 0.09, -0.20), om2.MPoint(-0.70, 0.15, -0.20), om2.MPoint(-0.60, 0.05, -0.02)]
               ctrl_rhand_line_down_points = [om2.MPoint(-0.60, 0.05, -0.02), om2.MPoint(-0.00, 0.05, -0.02)]

               self.draw_rhand_tn = ctrl_tr_n.create("transform", "Draw_righthand_ctrl")
               crv_ctrl_rhand_line_up = ctrl_cv_n.createWithEditPoints(ctrl_rhand_line_up_points, 1, 1, False, True, True, self.draw_rhand_tn)
               crv_ctrl_rhand_star = ctrl_cv_n.createWithEditPoints(ctrl_rhand_star_up_points, 1, 1, False, True, True, self.draw_rhand_tn)
               crv_ctrl_rhand_line_down = ctrl_cv_n.createWithEditPoints(ctrl_rhand_line_down_points, 1, 1, False, True, True, self.draw_rhand_tn)

               self.rhandnull_tn = ctrl_tr_n.create("transform", "Biped_FkRightHand_null", self.rforearmctrl_tn)
               self.rhandctrl_tn = ctrl_tr_n.create("transform", "Biped_FkRightHand_ctrl", self.rhandnull_tn)
               ctrl_rhandpositive_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rhandctrl_tn)
               ctrl_rhandnegative_comb_cv = ctrl_cv_n.create([crv_ctrl_rhand_line_up, crv_ctrl_rhand_star, crv_ctrl_rhand_line_down], self.rhandctrl_tn)

               self.rfingernull_tn = ctrl_tr_n.create("transform", "Biped_RightFingers_null", self.masterctrl_tn)
               self.rhandoption_tn = ctrl_tr_n.create("transform", "Biped_RightHandOptions_ctrl", rarm_sl_ls.getDependNode(2))
               ctrl_rhandoption_cv = ctrl_cv_n.createWithEditPoints(ctrl_lhandoption_line, 1, 1, False, True, True, self.rhandoption_tn)

               rhandnull_transform = om2.MFnTransform(self.rhandnull_tn)
               rhandnull_transform.setRotatePivotTranslation(jnt_rhand_t, om2.MSpace.kTransform)

               rfingernull_transform = om2.MFnTransform(self.rfingernull_tn)
               rfingernull_transform.setTranslation(jnt_rhand_t, om2.MSpace.kTransform)

               rhandoptionctrl_transform = om2.MFnTransform(self.rhandoption_tn)
               rhandoptionctrl_transform.setRotatePivotTranslation(jnt_rhand_t, om2.MSpace.kTransform)

               jnt_rhand_r = cmds.xform("RightHand", query=True, rotation=True, worldSpace=True)

               radian_rhand_x = (jnt_rhand_r[0]/180)*3.1415
               radian_rhand_y = (jnt_rhand_r[1]/180)*3.1415
               radian_rhand_z = (jnt_rhand_r[2]/180)*3.1415

               rhandnull_transform_r = rhandnull_transform.rotation(om2.MSpace.kTransform)
               rhandnull_transform_r[0], rhandnull_transform_r[1], rhandnull_transform_r[2] = radian_rhand_x, radian_rhand_y, radian_rhand_z
               rhandnull_transform.setRotation(rhandnull_transform_r, om2.MSpace.kTransform)

               rfingernull_transform_r = rfingernull_transform.rotation(om2.MSpace.kTransform)
               rfingernull_transform_r[0], rfingernull_transform_r[1], rfingernull_transform_r[2] = radian_rhand_x, radian_rhand_y, radian_rhand_z
               rfingernull_transform.setRotation(rfingernull_transform_r, om2.MSpace.kTransform)

               rhandctrl_transform = om2.MFnTransform(self.rhandctrl_tn)

               rhandctrl_transform_r = rhandctrl_transform.rotation(om2.MSpace.kTransform)
               rhandctrl_transform_r[1] = 1.57079
               rhandctrl_transform.setRotation(rhandctrl_transform_r, om2.MSpace.kTransform)

               rhandoptionctrl_transform_t = rhandoptionctrl_transform.translation(om2.MSpace.kTransform)
               rhandoptionctrl_transform_t[2] = jnt_lhand_t[2]-3
               rhandoptionctrl_transform.setTranslation(rhandoptionctrl_transform_t, om2.MSpace.kTransform)

               rhandoptionctrl_transform_r = rhandoptionctrl_transform.rotation(om2.MSpace.kTransform)
               rhandoptionctrl_transform_r[0], rhandoptionctrl_transform_r[1], rhandoptionctrl_transform_r[2] = radian_rhand_x-1.57079, radian_rhand_y, radian_rhand_z
               rhandoptionctrl_transform.setRotation(rhandoptionctrl_transform_r, om2.MSpace.kTransform)

               rhandctrl_transform_s = rhandctrl_transform.findPlug("scale", False)
               if rhandctrl_transform_s.isCompound:
                   for i in range(rhandctrl_transform_s.numChildren()):
                       child_plug = rhandctrl_transform_s.child(i)
                       attr_value = child_plug.setDouble(box_transform_s[0]/4)

               rhandnull_transform_trans = rhandnull_transform.transformation()
               rhandnull_transform_worldmatrix = rhandnull_transform_trans.asMatrix()

               rhandnull_transform_localmatrix = rhandnull_transform_worldmatrix * spinenull_parentinvtransform_matrix * spinenull_childtransform_localmatrix.inverse() * rshouldernullnull_transform_localmatrix.inverse() * rarmnull_transform_localmatrix.inverse() * rforearmnull_transform_localmatrix.inverse()

               rhandnull_transform.setTransformation(om2.MTransformationMatrix(rhandnull_transform_localmatrix))

               rhandoptionctrl_transform_trans = rhandoptionctrl_transform.transformation()
               rhandoptionctrl_transform_worldmatrix = rhandoptionctrl_transform_trans.asMatrix()

               rhandoptionctrl_transform_localmatrix = rhandoptionctrl_transform_worldmatrix * spinenull_parentinvtransform_matrix * spinenull_childtransform_localmatrix.inverse() * rshouldernullnull_transform_localmatrix.inverse() * rarmnull_transform_localmatrix.inverse() * rforearmnull_transform_localmatrix.inverse() * rhandnull_transform_localmatrix.inverse()

               rhandoptionctrl_transform.setTransformation(om2.MTransformationMatrix(rhandoptionctrl_transform_localmatrix))

               self.ctrl_mod_n.renameNode(ctrl_rhandpositive_comb_cv, "FkRightHand_shape1")
               self.ctrl_mod_n.renameNode(ctrl_rhandnegative_comb_cv, "FkRightHand_shape2")
               self.ctrl_mod_n.renameNode(ctrl_rhandoption_cv, "RightHandOptions_shape")
               self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 1 "Biped_FkRightHand_ctrl"')
               self.ctrl_mod_n.commandToExecute('color -rgbColor 1 1 0 "Biped_RightHandOptions_ctrl"')
               self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkRightHand_ctrl"')
               self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightHandOptions_ctrl"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_null.translateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_null.translateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_null.translateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_null.rotateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_null.rotateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_null.rotateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_null.scaleX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_null.scaleY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_null.scaleZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_null.visibility"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingers_null.translateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingers_null.translateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingers_null.translateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingers_null.rotateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingers_null.rotateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingers_null.rotateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingers_null.scaleX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingers_null.scaleY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingers_null.scaleZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingers_null.visibility"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightHandOptions_ctrl.translateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightHandOptions_ctrl.translateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightHandOptions_ctrl.translateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightHandOptions_ctrl.rotateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightHandOptions_ctrl.rotateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightHandOptions_ctrl.rotateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightHandOptions_ctrl.scaleX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightHandOptions_ctrl.scaleY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightHandOptions_ctrl.scaleZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightHandOptions_ctrl.visibility"')
               self.ctrl_mod_n.doIt()

               self.rikhandnull_tn = ctrl_tr_n.create("transform", "Biped_IkRightHand_null", self.masterctrl_tn)
               self.rikhandctrl_tn = ctrl_tr_n.create("transform", "Biped_IkRightHand_ctrl", self.rikhandnull_tn)
               ctrl_rikhand_comb_cv = ctrl_cv_n.create([crv_ctrl_hand_line_l, crv_ctrl_hand_line, crv_ctrl_hand_line_r], self.rikhandctrl_tn)

               rikhandnull_transform = om2.MFnTransform(self.rikhandnull_tn)
               rikhandnull_transform.setRotatePivotTranslation(jnt_rhand_t, om2.MSpace.kTransform)

               rikhandnull_transform_r = rikhandnull_transform.rotation(om2.MSpace.kTransform)
               rikhandnull_transform_r[0], rikhandnull_transform_r[1], rikhandnull_transform_r[2] = radian_rhand_x, radian_rhand_y, radian_rhand_z
               rikhandnull_transform.setRotation(rikhandnull_transform_r, om2.MSpace.kTransform)

               rikhandctrl_transform = om2.MFnTransform(self.rikhandctrl_tn)

               rikhandctrl_transform_t = rikhandctrl_transform.rotatePivotTranslation(om2.MSpace.kTransform)
               rikhandctrl_transform_t[2] = -((jnt_rhand_t[1]+4)-jnt_rhand_t[1])
               rikhandctrl_transform.setRotatePivotTranslation(rikhandctrl_transform_t, om2.MSpace.kTransform)

               rikhandctrl_transform_r = rikhandctrl_transform.rotation(om2.MSpace.kTransform)
               rikhandctrl_transform_r[0], rikhandctrl_transform_r[2] = 1.57079, 1.57079
               rikhandctrl_transform.setRotation(rikhandctrl_transform_r, om2.MSpace.kTransform)

               rikhandctrl_transform_s = rikhandctrl_transform.findPlug("scale", False)
               if rikhandctrl_transform_s.isCompound:
                   for i in range(rikhandctrl_transform_s.numChildren()):
                       child_plug = rikhandctrl_transform_s.child(i)
                       attr_value = child_plug.setDouble(box_transform_s[0]/3)

               self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_IkRightHand_ctrl"')
               self.ctrl_mod_n.doIt()

               # rikhandnull_transform_trans = rikhandnull_transform.transformation()
               # rikhandnull_transform_worldmatrix = rikhandnull_transform_trans.asMatrix()
               #
               # rikhandnull_transform_localmatrix = rikhandnull_transform_worldmatrix * spinenull_parentinvtransform_matrix * spinenull_childtransform_localmatrix.inverse() * rshouldernullnull_transform_localmatrix.inverse() * rarmnull_transform_localmatrix.inverse() * rforearmnull_transform_localmatrix.inverse() * rhandnull_transform_localmatrix.inverse()
               #
               # rikhandnull_transform.setTransformation(om2.MTransformationMatrix(rikhandnull_transform_localmatrix))

               rikhandnull_path_n = om2.MDagPath()
               rikhandnull_path = rikhandnull_path_n.getAPathTo(self.rikhandctrl_tn)
               rikhandnull_worldtransform = om2.MFnTransform(rikhandnull_path)

               rikhandnull_worldtransform.setRotatePivot(om2.MPoint(jnt_rhand_t), om2.MSpace.kWorld, False)

               self.ctrl_mod_n.renameNode(ctrl_rikhand_comb_cv, "IkRightHand_shape")
               self.ctrl_mod_n.commandToExecute('color -rgbColor 1 0 0 "Biped_IkRightHand_ctrl"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_null.translateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_null.translateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_null.translateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_null.rotateX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_null.rotateY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_null.rotateZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_null.scaleX"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_null.scaleY"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_null.scaleZ"')
               self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_null.visibility"')
               self.ctrl_mod_n.doIt()

        try:
            rhandthumb_sl_ls = om2.MSelectionList()
            rhandthumb_sl_ls.add("RightFingerThumb*")

            for index in range(rhandthumb_sl_ls.length()):
                jnt_rhandthumb_obj = rhandthumb_sl_ls.getDependNode(index)
                jnt_rhandthumb_path_n = om2.MDagPath()
                jnt_rhandthumb_path = jnt_rhandthumb_path_n.getAPathTo(jnt_rhandthumb_obj)
                jnt_rhandthumb_transform = om2.MFnTransform(jnt_rhandthumb_path)
                jnt_rhandthumb_t = jnt_rhandthumb_transform.translation(om2.MSpace.kWorld)

                self.rhandthumbnull_tn = ctrl_tr_n.create("transform", "Biped_RightFingerThumb{0}_null".format(index + 1))
                self.rhandthumbctrl_tn = ctrl_tr_n.create("transform", "Biped_RightFingerThumb{0}_ctrl".format(index + 1), self.rhandthumbnull_tn)
                ctrl_rhandthumbpositive_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rhandthumbctrl_tn)
                ctrl_rhandthumbnegative_comb_cv = ctrl_cv_n.create([crv_ctrl_rhand_line_up, crv_ctrl_rhand_star, crv_ctrl_rhand_line_down], self.rhandthumbctrl_tn)

                rhandthumbnull_transform = om2.MFnTransform(self.rhandthumbnull_tn)
                rhandthumbnull_transform.setRotatePivotTranslation(jnt_rhandthumb_t, om2.MSpace.kTransform)

                jnt_rhandthumb_r = cmds.xform("RightFingerThumb{0}".format(index+1), query=True, rotation=True, worldSpace=True)

                radian_rhandthumb_x = (jnt_rhandthumb_r[0]/180)*3.1415
                radian_rhandthumb_y = (jnt_rhandthumb_r[1]/180)*3.1415
                radian_rhandthumb_z = (jnt_rhandthumb_r[2]/180)*3.1415

                rhandthumbnull_transform_r = rhandthumbnull_transform.rotation(om2.MSpace.kTransform)
                rhandthumbnull_transform_r[0], rhandthumbnull_transform_r[1], rhandthumbnull_transform_r[2] = radian_rhandthumb_x, radian_rhandthumb_y, radian_rhandthumb_z
                rhandthumbnull_transform.setRotation(rhandthumbnull_transform_r, om2.MSpace.kTransform)

                rhandthumbctrl_transform = om2.MFnTransform(self.rhandthumbctrl_tn)

                rhandthumbctrl_transform_s = rhandthumbctrl_transform.findPlug("scale", False)
                if rhandthumbctrl_transform_s.isCompound:
                    for i in range(rhandthumbctrl_transform_s.numChildren()):
                        child_plug = rhandthumbctrl_transform_s.child(i)
                        attr_value = child_plug.setDouble(box_transform_s[0]/14)

                rhandthumbctrl_transform_r = rhandthumbctrl_transform.rotation(om2.MSpace.kTransform)
                rhandthumbctrl_transform_r[1] = 1.57079
                rhandthumbctrl_transform.setRotation(rhandthumbctrl_transform_r, om2.MSpace.kTransform)

                if index == 0:
                    rhand_tr_n = om2.MFnDagNode(self.rfingernull_tn)
                    rhand_tr_n.addChild(self.rhandthumbnull_tn)

                    rfingernull_transform_trans = rfingernull_transform.transformation()
                    rfingernull_transform_worldmatrix = rfingernull_transform_trans.asMatrixInverse()

                    rhandthumbnull_transform_trans = rhandthumbnull_transform.transformation()
                    rhandthumbnull_transform_worldmatrix = rhandthumbnull_transform_trans.asMatrix()

                    rhandthumbnull_transform_localmatrix = rhandthumbnull_transform_worldmatrix * rfingernull_transform_worldmatrix

                    rhandthumbnull_transform.setTransformation(om2.MTransformationMatrix(rhandthumbnull_transform_localmatrix))

                else:
                    rhandthumbctrl_sl_ls = om2.MSelectionList()
                    rhandthumbctrl_sl_ls.add("Biped_RightFingerThumb*_ctrl")
                    rhandthumbctrl_obj = rhandthumbctrl_sl_ls.getDependNode(index-1)

                    rhandthumbnull_sl_ls = om2.MSelectionList()
                    rhandthumbnull_sl_ls.add("Biped_RightFingerThumb*_null")

                    rhandthumb_tr_n = om2.MFnDagNode(rhandthumbctrl_obj)
                    rhandthumb_tr_n.addChild(self.rhandthumbnull_tn)

                    rhandthumbnull_parentinvtransform_matrix = om2.MMatrix()
                    for i in range(rhandthumbnull_sl_ls.length()-1):
                        parentobj = rhandthumbnull_sl_ls.getDependNode(i)
                        parentinvtransform = om2.MFnTransform(parentobj)
                        parentinvtransform_trans = parentinvtransform.transformation()
                        null_Matrix = parentinvtransform_trans.asMatrixInverse()

                        rhandthumbnull_parentinvtransform_matrix = rhandthumbnull_parentinvtransform_matrix * null_Matrix

                    rhandthumbnull_childtransform_trans = rhandthumbnull_transform.transformation()
                    rhandthumbnull_childtransform_worldmatrix = rhandthumbnull_childtransform_trans.asMatrix()

                    lhandthumbnull_childtransform_localmatrix = rhandthumbnull_childtransform_worldmatrix * rfingernull_transform_worldmatrix * rhandthumbnull_parentinvtransform_matrix

                    rhandthumbnull_transform.setTransformation(om2.MTransformationMatrix(lhandthumbnull_childtransform_localmatrix))

                self.ctrl_mod_n.renameNode(ctrl_rhandthumbpositive_comb_cv, "RightFingerThumb{0}_shape1".format(index+1))
                self.ctrl_mod_n.renameNode(ctrl_rhandthumbnegative_comb_cv, "RightFingerThumb{0}_shape2".format(index+1))
                self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 0 "Biped_RightFingerThumb{0}_ctrl"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightFingerThumb{0}_ctrl"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_null.translateX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_null.translateY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_null.translateZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_null.rotateX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_null.rotateY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_null.rotateZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_null.scaleX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_null.scaleY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_null.scaleZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_null.visibility"'.format(index+1))
                self.ctrl_mod_n.doIt()

        except:
            pass

        try:
            rhandindex_sl_ls = om2.MSelectionList()
            rhandindex_sl_ls.add("RightFingerIndex*")

            for index in range(rhandindex_sl_ls.length()):
                jnt_rhandindex_obj = rhandindex_sl_ls.getDependNode(index)
                jnt_rhandindex_path_n = om2.MDagPath()
                jnt_rhandindex_path = jnt_rhandindex_path_n.getAPathTo(jnt_rhandindex_obj)
                jnt_rhandindex_transform = om2.MFnTransform(jnt_rhandindex_path)
                jnt_rhandindex_t = jnt_rhandindex_transform.translation(om2.MSpace.kWorld)

                self.rhandindexnull_tn = ctrl_tr_n.create("transform", "Biped_RightFingerIndex{0}_null".format(index + 1))
                self.rhandindexctrl_tn = ctrl_tr_n.create("transform", "Biped_RightFingerIndex{0}_ctrl".format(index + 1), self.rhandindexnull_tn)
                ctrl_rhandIndexpositive_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rhandindexctrl_tn)
                ctrl_rhandIndexnegative_comb_cv = ctrl_cv_n.create([crv_ctrl_rhand_line_up, crv_ctrl_rhand_star, crv_ctrl_rhand_line_down], self.rhandindexctrl_tn)

                rhandindexnull_transform = om2.MFnTransform(self.rhandindexnull_tn)
                rhandindexnull_transform.setRotatePivotTranslation(jnt_rhandindex_t, om2.MSpace.kTransform)

                jnt_rhandindex_r = cmds.xform("RightFingerIndex{0}".format(index+1), query=True, rotation=True, worldSpace=True)

                radian_rhandIndex_x = (jnt_rhandindex_r[0]/180)*3.1415
                radian_rhandIndex_y = (jnt_rhandindex_r[1]/180)*3.1415
                radian_rhandIndex_z = (jnt_rhandindex_r[2]/180)*3.1415

                rhandindexnull_transform_r = rhandindexnull_transform.rotation(om2.MSpace.kTransform)
                rhandindexnull_transform_r[0], rhandindexnull_transform_r[1], rhandindexnull_transform_r[2] = radian_rhandIndex_x, radian_rhandIndex_y, radian_rhandIndex_z
                rhandindexnull_transform.setRotation(rhandindexnull_transform_r, om2.MSpace.kTransform)

                rhandindexctrl_transform = om2.MFnTransform(self.rhandindexctrl_tn)

                rhandindexctrl_transform_s = rhandindexctrl_transform.findPlug("scale", False)
                if rhandindexctrl_transform_s.isCompound:
                    for i in range(rhandindexctrl_transform_s.numChildren()):
                        child_plug = rhandindexctrl_transform_s.child(i)
                        attr_value = child_plug.setDouble(box_transform_s[0]/14)

                rhandindexctrl_transform_r = rhandindexctrl_transform.rotation(om2.MSpace.kTransform)
                rhandindexctrl_transform_r[1] = 1.57079
                rhandindexctrl_transform.setRotation(rhandindexctrl_transform_r, om2.MSpace.kTransform)

                if index == 0:
                    rhand_tr_n = om2.MFnDagNode(self.rfingernull_tn)
                    rhand_tr_n.addChild(self.rhandindexnull_tn)

                    rhandindexnull_transform_trans = rhandindexnull_transform.transformation()
                    rhandindexnull_transform_worldmatrix = rhandindexnull_transform_trans.asMatrix()

                    rhandindexnull_transform_localmatrix = rhandindexnull_transform_worldmatrix * rfingernull_transform_worldmatrix

                    rhandindexnull_transform.setTransformation(om2.MTransformationMatrix(rhandindexnull_transform_localmatrix))

                else:
                    rhandIndexctrl_sl_ls = om2.MSelectionList()
                    rhandIndexctrl_sl_ls.add("Biped_RightFingerIndex*_ctrl")
                    rhandIndexctrl_obj = rhandIndexctrl_sl_ls.getDependNode(index-1)

                    rhandIndexnull_sl_ls = om2.MSelectionList()
                    rhandIndexnull_sl_ls.add("Biped_RightFingerIndex*_null")

                    rhandIndex_tr_n = om2.MFnDagNode(rhandIndexctrl_obj)
                    rhandIndex_tr_n.addChild(self.rhandindexnull_tn)

                    rhandIndexnull_parentinvtransform_matrix = om2.MMatrix()
                    for i in range(rhandIndexnull_sl_ls.length()-1):
                        parentobj = rhandIndexnull_sl_ls.getDependNode(i)
                        parentinvtransform = om2.MFnTransform(parentobj)
                        parentinvtransform_trans = parentinvtransform.transformation()
                        null_Matrix = parentinvtransform_trans.asMatrixInverse()

                        rhandIndexnull_parentinvtransform_matrix = rhandIndexnull_parentinvtransform_matrix * null_Matrix

                    rhandindexnull_childtransform_trans = rhandindexnull_transform.transformation()
                    rhandindexnull_childtransform_worldmatrix = rhandindexnull_childtransform_trans.asMatrix()

                    rhandindexnull_childtransform_localmatrix = rhandindexnull_childtransform_worldmatrix * rfingernull_transform_worldmatrix * rhandIndexnull_parentinvtransform_matrix

                    rhandindexnull_transform.setTransformation(om2.MTransformationMatrix(rhandindexnull_childtransform_localmatrix))

                self.ctrl_mod_n.renameNode(ctrl_rhandIndexpositive_comb_cv, "RightFingerIndex{0}_shape1".format(index+1))
                self.ctrl_mod_n.renameNode(ctrl_rhandIndexnegative_comb_cv, "RightFingerIndex{0}_shape2".format(index+1))
                self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 0 "Biped_RightFingerIndex{0}_ctrl"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightFingerIndex{0}_ctrl"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_null.translateX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_null.translateY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_null.translateZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_null.rotateX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_null.rotateY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_null.rotateZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_null.scaleX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_null.scaleY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_null.scaleZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_null.visibility"'.format(index+1))
                self.ctrl_mod_n.doIt()

        except:
            pass

        try:
            rhandmiddle_sl_ls = om2.MSelectionList()
            rhandmiddle_sl_ls.add("RightFingerMiddle*")

            for index in range(rhandmiddle_sl_ls.length()):
                jnt_rhandmiddle_obj = rhandmiddle_sl_ls.getDependNode(index)
                jnt_rhandmiddle_path_n = om2.MDagPath()
                jnt_rhandmiddle_path = jnt_rhandmiddle_path_n.getAPathTo(jnt_rhandmiddle_obj)
                jnt_rhandmiddle_transform = om2.MFnTransform(jnt_rhandmiddle_path)
                jnt_rhandmiddle_t = jnt_rhandmiddle_transform.translation(om2.MSpace.kWorld)

                self.rhandmiddlenull_tn = ctrl_tr_n.create("transform", "Biped_RightFingerMiddle{0}_null".format(index + 1))
                self.rhandmiddlectrl_tn = ctrl_tr_n.create("transform", "Biped_RightFingerMiddle{0}_ctrl".format(index + 1), self.rhandmiddlenull_tn)
                ctrl_rhandmiddlepositive_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rhandmiddlectrl_tn)
                ctrl_rhandmiddlenegative_comb_cv = ctrl_cv_n.create([crv_ctrl_rhand_line_up, crv_ctrl_rhand_star, crv_ctrl_rhand_line_down], self.rhandmiddlectrl_tn)

                rhandmiddlenull_transform = om2.MFnTransform(self.rhandmiddlenull_tn)
                rhandmiddlenull_transform.setRotatePivotTranslation(jnt_rhandmiddle_t, om2.MSpace.kTransform)

                jnt_rhandmiddle_r = cmds.xform("RightFingerMiddle{0}".format(index+1), query=True, rotation=True, worldSpace=True)

                radian_rhandmiddle_x = (jnt_rhandmiddle_r[0]/180)*3.1415
                radian_rhandmiddle_y = (jnt_rhandmiddle_r[1]/180)*3.1415
                radian_rhandmiddle_z = (jnt_rhandmiddle_r[2]/180)*3.1415

                rhandmiddlenull_transform_r = rhandmiddlenull_transform.rotation(om2.MSpace.kTransform)
                rhandmiddlenull_transform_r[0], rhandmiddlenull_transform_r[1], rhandmiddlenull_transform_r[2] = radian_rhandmiddle_x, radian_rhandmiddle_y, radian_rhandmiddle_z
                rhandmiddlenull_transform.setRotation(rhandmiddlenull_transform_r, om2.MSpace.kTransform)

                rhandmiddlectrl_transform = om2.MFnTransform(self.rhandmiddlectrl_tn)

                rhandmiddlectrl_transform_s = rhandmiddlectrl_transform.findPlug("scale", False)
                if rhandmiddlectrl_transform_s.isCompound:
                    for i in range(rhandmiddlectrl_transform_s.numChildren()):
                        child_plug = rhandmiddlectrl_transform_s.child(i)
                        attr_value = child_plug.setDouble(box_transform_s[0]/14)

                rhandmiddlectrl_transform_r = rhandmiddlectrl_transform.rotation(om2.MSpace.kTransform)
                rhandmiddlectrl_transform_r[1] = 1.57079
                rhandmiddlectrl_transform.setRotation(rhandmiddlectrl_transform_r, om2.MSpace.kTransform)

                if index == 0:
                    rhand_tr_n = om2.MFnDagNode(self.rfingernull_tn)
                    rhand_tr_n.addChild(self.rhandmiddlenull_tn)

                    rhandmiddlenull_transform_trans = rhandmiddlenull_transform.transformation()
                    rhandmiddlenull_transform_worldmatrix = rhandmiddlenull_transform_trans.asMatrix()

                    rhandmiddlenull_transform_localmatrix = rhandmiddlenull_transform_worldmatrix * rfingernull_transform_worldmatrix

                    rhandmiddlenull_transform.setTransformation(om2.MTransformationMatrix(rhandmiddlenull_transform_localmatrix))

                else:
                    rhandmiddlectrl_sl_ls = om2.MSelectionList()
                    rhandmiddlectrl_sl_ls.add("Biped_RightFingerMiddle*_ctrl")
                    rhandmiddlectrl_obj = rhandmiddlectrl_sl_ls.getDependNode(index-1)

                    rhandmiddlenull_sl_ls = om2.MSelectionList()
                    rhandmiddlenull_sl_ls.add("Biped_RightFingerMiddle*_null")

                    rhandmiddle_tr_n = om2.MFnDagNode(rhandmiddlectrl_obj)
                    rhandmiddle_tr_n.addChild(self.rhandmiddlenull_tn)

                    rhandmiddlenull_parentinvtransform_matrix = om2.MMatrix()
                    for i in range(rhandmiddlenull_sl_ls.length()-1):
                        parentobj = rhandmiddlenull_sl_ls.getDependNode(i)
                        parentinvtransform = om2.MFnTransform(parentobj)
                        parentinvtransform_trans = parentinvtransform.transformation()
                        null_Matrix = parentinvtransform_trans.asMatrixInverse()

                        rhandmiddlenull_parentinvtransform_matrix = rhandmiddlenull_parentinvtransform_matrix * null_Matrix

                    rhandmiddlenull_childtransform_trans = rhandmiddlenull_transform.transformation()
                    rhandmiddlenull_childtransform_worldmatrix = rhandmiddlenull_childtransform_trans.asMatrix()

                    rhandmiddlenull_childtransform_localmatrix = rhandmiddlenull_childtransform_worldmatrix * rfingernull_transform_worldmatrix * rhandmiddlenull_parentinvtransform_matrix

                    rhandmiddlenull_transform.setTransformation(om2.MTransformationMatrix(rhandmiddlenull_childtransform_localmatrix))

                self.ctrl_mod_n.renameNode(ctrl_rhandmiddlepositive_comb_cv, "RightFingerMiddle{0}_shape1".format(index+1))
                self.ctrl_mod_n.renameNode(ctrl_rhandmiddlenegative_comb_cv, "RightFingerMiddle{0}_shape2".format(index+1))
                self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 0 "Biped_RightFingerMiddle{0}_ctrl"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightFingerMiddle{0}_ctrl"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_null.translateX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_null.translateY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_null.translateZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_null.rotateX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_null.rotateY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_null.rotateZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_null.scaleX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_null.scaleY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_null.scaleZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_null.visibility"'.format(index+1))
                self.ctrl_mod_n.doIt()

        except:
            pass

        try:
            rhandring_sl_ls = om2.MSelectionList()
            rhandring_sl_ls.add("RightFingerRing*")

            for index in range(rhandring_sl_ls.length()):
                jnt_rhandring_obj = rhandring_sl_ls.getDependNode(index)
                jnt_rhandring_path_n = om2.MDagPath()
                jnt_rhandring_path = jnt_rhandring_path_n.getAPathTo(jnt_rhandring_obj)
                jnt_rhandring_transform = om2.MFnTransform(jnt_rhandring_path)
                jnt_rhandring_t = jnt_rhandring_transform.translation(om2.MSpace.kWorld)

                self.rhandringnull_tn = ctrl_tr_n.create("transform", "Biped_RightFingerRing{0}_null".format(index + 1))
                self.rhandringctrl_tn = ctrl_tr_n.create("transform", "Biped_RightFingerRing{0}_ctrl".format(index + 1), self.rhandringnull_tn)
                ctrl_rhandringpositive_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rhandringctrl_tn)
                ctrl_rhandringnegative_comb_cv = ctrl_cv_n.create([crv_ctrl_rhand_line_up, crv_ctrl_rhand_star, crv_ctrl_rhand_line_down], self.rhandringctrl_tn)

                rhandringnull_transform = om2.MFnTransform(self.rhandringnull_tn)
                rhandringnull_transform.setRotatePivotTranslation(jnt_rhandring_t, om2.MSpace.kTransform)

                jnt_rhandring_r = cmds.xform("RightFingerRing{0}".format(index+1), query=True, rotation=True, worldSpace=True)

                radian_rhandring_x = (jnt_rhandring_r[0]/180)*3.1415
                radian_rhandring_y = (jnt_rhandring_r[1]/180)*3.1415
                radian_rhandring_z = (jnt_rhandring_r[2]/180)*3.1415

                rhandringnull_transform_r = rhandringnull_transform.rotation(om2.MSpace.kTransform)
                rhandringnull_transform_r[0], rhandringnull_transform_r[1], rhandringnull_transform_r[2] = radian_rhandring_x, radian_rhandring_y, radian_rhandring_z
                rhandringnull_transform.setRotation(rhandringnull_transform_r, om2.MSpace.kTransform)

                rhandringctrl_transform = om2.MFnTransform(self.rhandringctrl_tn)

                rhandringctrl_transform_s = rhandringctrl_transform.findPlug("scale", False)
                if rhandringctrl_transform_s.isCompound:
                    for i in range(rhandringctrl_transform_s.numChildren()):
                        child_plug = rhandringctrl_transform_s.child(i)
                        attr_value = child_plug.setDouble(box_transform_s[0]/14)

                rhandringctrl_transform_r = rhandringctrl_transform.rotation(om2.MSpace.kTransform)
                rhandringctrl_transform_r[1] = 1.57079
                rhandringctrl_transform.setRotation(rhandringctrl_transform_r, om2.MSpace.kTransform)

                if index == 0:
                    rhand_tr_n = om2.MFnDagNode(self.rfingernull_tn)
                    rhand_tr_n.addChild(self.rhandringnull_tn)

                    rhandringnull_transform_trans = rhandringnull_transform.transformation()
                    rhandringnull_transform_worldmatrix = rhandringnull_transform_trans.asMatrix()

                    rhandringnull_transform_localmatrix = rhandringnull_transform_worldmatrix * rfingernull_transform_worldmatrix

                    rhandringnull_transform.setTransformation(om2.MTransformationMatrix(rhandringnull_transform_localmatrix))

                else:
                    rhandringctrl_sl_ls = om2.MSelectionList()
                    rhandringctrl_sl_ls.add("Biped_RightFingerRing*_ctrl")
                    rhandringctrl_obj = rhandringctrl_sl_ls.getDependNode(index-1)

                    rhandringnull_sl_ls = om2.MSelectionList()
                    rhandringnull_sl_ls.add("Biped_RightFingerRing*_null")

                    rhandring_tr_n = om2.MFnDagNode(rhandringctrl_obj)
                    rhandring_tr_n.addChild(self.rhandringnull_tn)

                    rhandringnull_parentinvtransform_matrix = om2.MMatrix()
                    for i in range(rhandringnull_sl_ls.length()-1):
                        parentobj = rhandringnull_sl_ls.getDependNode(i)
                        parentinvtransform = om2.MFnTransform(parentobj)
                        parentinvtransform_trans = parentinvtransform.transformation()
                        null_Matrix = parentinvtransform_trans.asMatrixInverse()

                        rhandringnull_parentinvtransform_matrix = rhandringnull_parentinvtransform_matrix * null_Matrix

                    rhandringnull_childtransform_trans = rhandringnull_transform.transformation()
                    rhandringnull_childtransform_worldmatrix = rhandringnull_childtransform_trans.asMatrix()

                    rhandringnull_childtransform_localmatrix = rhandringnull_childtransform_worldmatrix * rfingernull_transform_worldmatrix * rhandringnull_parentinvtransform_matrix

                    rhandringnull_transform.setTransformation(om2.MTransformationMatrix(rhandringnull_childtransform_localmatrix))

                self.ctrl_mod_n.renameNode(ctrl_rhandringpositive_comb_cv, "RightFingerRing{0}_shape1".format(index+1))
                self.ctrl_mod_n.renameNode(ctrl_rhandringnegative_comb_cv, "RightFingerRing{0}_shape2".format(index+1))
                self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 0 "Biped_RightFingerRing{0}_ctrl"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightFingerRing{0}_ctrl"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_null.translateX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_null.translateY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_null.translateZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_null.rotateX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_null.rotateY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_null.rotateZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_null.scaleX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_null.scaleY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_null.scaleZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_null.visibility"'.format(index+1))
                self.ctrl_mod_n.doIt()

        except:
            pass

        try:
            rhandpinky_sl_ls = om2.MSelectionList()
            rhandpinky_sl_ls.add("RightFingerPinky*")

            for index in range(rhandpinky_sl_ls.length()):
                jnt_rhandpinky_obj = rhandpinky_sl_ls.getDependNode(index)
                jnt_rhandpinky_path_n = om2.MDagPath()
                jnt_rhandpinky_path = jnt_rhandpinky_path_n.getAPathTo(jnt_rhandpinky_obj)
                jnt_rhandpinky_transform = om2.MFnTransform(jnt_rhandpinky_path)
                jnt_rhandpinky_t = jnt_rhandpinky_transform.translation(om2.MSpace.kWorld)

                self.rhandpinkynull_tn = ctrl_tr_n.create("transform", "Biped_RightFingerPinky{0}_null".format(index + 1))
                self.rhandpinkyctrl_tn = ctrl_tr_n.create("transform", "Biped_RightFingerPinky{0}_ctrl".format(index + 1), self.rhandpinkynull_tn)
                ctrl_rhandpinkypositive_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rhandpinkyctrl_tn)
                ctrl_rhandpinkynegative_comb_cv = ctrl_cv_n.create([crv_ctrl_rhand_line_up, crv_ctrl_rhand_star, crv_ctrl_rhand_line_down], self.rhandpinkyctrl_tn)

                rhandpinkynull_transform = om2.MFnTransform(self.rhandpinkynull_tn)
                rhandpinkynull_transform.setRotatePivotTranslation(jnt_rhandpinky_t, om2.MSpace.kTransform)

                jnt_rhandpinky_r = cmds.xform("RightFingerPinky{0}".format(index+1), query=True, rotation=True, worldSpace=True)

                radian_rhandpinky_x = (jnt_rhandpinky_r[0]/180)*3.1415
                radian_rhandpinky_y = (jnt_rhandpinky_r[1]/180)*3.1415
                radian_rhandpinky_z = (jnt_rhandpinky_r[2]/180)*3.1415

                rhandpinkynull_transform_r = rhandpinkynull_transform.rotation(om2.MSpace.kTransform)
                rhandpinkynull_transform_r[0], rhandpinkynull_transform_r[1], rhandpinkynull_transform_r[2] = radian_rhandpinky_x, radian_rhandpinky_y, radian_rhandpinky_z
                rhandpinkynull_transform.setRotation(rhandpinkynull_transform_r, om2.MSpace.kTransform)

                rhandpinkyctrl_transform = om2.MFnTransform(self.rhandpinkyctrl_tn)

                rhandpinkyctrl_transform_s = rhandpinkyctrl_transform.findPlug("scale", False)
                if rhandpinkyctrl_transform_s.isCompound:
                    for i in range(rhandpinkyctrl_transform_s.numChildren()):
                        child_plug = rhandpinkyctrl_transform_s.child(i)
                        attr_value = child_plug.setDouble(box_transform_s[0]/14)

                rhandpinkyctrl_transform_r = rhandpinkyctrl_transform.rotation(om2.MSpace.kTransform)
                rhandpinkyctrl_transform_r[1] = 1.57079
                rhandpinkyctrl_transform.setRotation(rhandpinkyctrl_transform_r, om2.MSpace.kTransform)

                if index == 0:
                    rhand_tr_n = om2.MFnDagNode(self.rfingernull_tn)
                    rhand_tr_n.addChild(self.rhandpinkynull_tn)

                    rhandpinkynull_transform_trans = rhandpinkynull_transform.transformation()
                    rhandpinkynull_transform_worldmatrix = rhandpinkynull_transform_trans.asMatrix()

                    rhandpinkynull_transform_localmatrix = rhandpinkynull_transform_worldmatrix * rfingernull_transform_worldmatrix

                    rhandpinkynull_transform.setTransformation(om2.MTransformationMatrix(rhandpinkynull_transform_localmatrix))

                else:
                    rhandpinkyctrl_sl_ls = om2.MSelectionList()
                    rhandpinkyctrl_sl_ls.add("Biped_RightFingerPinky*_ctrl")
                    rhandpinkyctrl_obj = rhandpinkyctrl_sl_ls.getDependNode(index-1)

                    rhandpinkynull_sl_ls = om2.MSelectionList()
                    rhandpinkynull_sl_ls.add("Biped_RightFingerPinky*_null")

                    rhandpinky_tr_n = om2.MFnDagNode(rhandpinkyctrl_obj)
                    rhandpinky_tr_n.addChild(self.rhandpinkynull_tn)

                    rhandpinkynull_parentinvtransform_matrix = om2.MMatrix()
                    for i in range(rhandpinkynull_sl_ls.length()-1):
                        parentobj = rhandpinkynull_sl_ls.getDependNode(i)
                        parentinvtransform = om2.MFnTransform(parentobj)
                        parentinvtransform_trans = parentinvtransform.transformation()
                        null_Matrix = parentinvtransform_trans.asMatrixInverse()

                        rhandpinkynull_parentinvtransform_matrix = rhandpinkynull_parentinvtransform_matrix * null_Matrix

                    rhandpinkynull_childtransform_trans = rhandpinkynull_transform.transformation()
                    rhandpinkynull_childtransform_worldmatrix = rhandpinkynull_childtransform_trans.asMatrix()

                    rhandpinkynull_childtransform_localmatrix = rhandpinkynull_childtransform_worldmatrix * rfingernull_transform_worldmatrix * rhandpinkynull_parentinvtransform_matrix

                    rhandpinkynull_transform.setTransformation(om2.MTransformationMatrix(rhandpinkynull_childtransform_localmatrix))

                self.ctrl_mod_n.renameNode(ctrl_rhandpinkypositive_comb_cv, "RightFingerPinky{0}_shape1".format(index+1))
                self.ctrl_mod_n.renameNode(ctrl_rhandpinkynegative_comb_cv, "RightFingerPinky{0}_shape2".format(index+1))
                self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 0 "Biped_RightFingerPinky{0}_ctrl"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightFingerPinky{0}_ctrl"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_null.translateX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_null.translateY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_null.translateZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_null.rotateX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_null.rotateY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_null.rotateZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_null.scaleX"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_null.scaleY"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_null.scaleZ"'.format(index+1))
                self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_null.visibility"'.format(index+1))
                self.ctrl_mod_n.doIt()

        except:
            pass

        rleg_sl_ls = om2.MSelectionList()
        rleg_sl_ls.add("RightUpLeg")
        rleg_sl_ls.add("RightLeg")
        rleg_sl_ls.add("RightFoot")
        rleg_sl_ls.add("RightToeBase")

        fkrleg_sl_ls = om2.MSelectionList()
        fkrleg_sl_ls.add("FkRightUpLeg")
        fkrleg_sl_ls.add("FkRightLeg")
        fkrleg_sl_ls.add("FkRightFoot")
        fkrleg_sl_ls.add("FkRightToeBase")

        for index in range(fkrleg_sl_ls.length()):
                jnt_rleg_obj = fkrleg_sl_ls.getDependNode(index)
                jnt_rleg_path_n = om2.MDagPath()
                jnt_rleg_path = jnt_rleg_path_n.getAPathTo(jnt_rleg_obj)
                jnt_rleg_transform = om2.MFnTransform(jnt_rleg_path)
                jnt_rleg_t = jnt_rleg_transform.translation(om2.MSpace.kWorld)

                if index == 0:
                    self.ruplegnull_tn = ctrl_tr_n.create("transform", "Biped_FkRightUpLeg_null", self.rootctrl_tn)
                    self.ruplegupctrl_tn = ctrl_tr_n.create("transform", "Biped_FkRightUpLeg_ctrl", self.ruplegnull_tn)
                    ctrl_ruplegpositive_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.ruplegupctrl_tn)

                    ruplegnull_transform = om2.MFnTransform(self.ruplegnull_tn)
                    ruplegnull_transform.setRotatePivotTranslation(jnt_rleg_t, om2.MSpace.kTransform)

                    jnt_rupleg_r = cmds.xform("RightUpLeg", query=True, rotation=True, worldSpace=True)

                    radian_rlegtoebasenull_x = (jnt_rupleg_r[0]/180)*3.1415
                    radian_rlegtoebasenull_y = (jnt_rupleg_r[1]/180)*3.1415
                    radian_rlegtoebasenull_z = (jnt_rupleg_r[2]/180)*3.1415

                    ruplegnull_transform_r = ruplegnull_transform.rotation(om2.MSpace.kTransform)
                    ruplegnull_transform_r[0], ruplegnull_transform_r[1], ruplegnull_transform_r[2] = radian_rlegtoebasenull_x, radian_rlegtoebasenull_y, radian_rlegtoebasenull_z
                    ruplegnull_transform.setRotation(ruplegnull_transform_r, om2.MSpace.kTransform)

                    ruplegnctrl_transform = om2.MFnTransform(self.ruplegupctrl_tn)

                    ruplegnctrl_transform_r = ruplegnull_transform.rotation(om2.MSpace.kTransform)
                    ruplegnctrl_transform_r[0], ruplegnctrl_transform_r[1], ruplegnctrl_transform_r[2] = 0, 1.57079, 0
                    ruplegnctrl_transform.setRotation(ruplegnctrl_transform_r, om2.MSpace.kTransform)

                    ruplegnctrl_transform_s = ruplegnctrl_transform.findPlug("scale", False)
                    if ruplegnctrl_transform_s.isCompound:
                        for i in range(ruplegnctrl_transform_s.numChildren()):
                            child_plug = ruplegnctrl_transform_s.child(i)
                            attr_value = child_plug.setDouble(box_transform_s[0]/2)

                    ruplegnull_transform_trans = ruplegnull_transform.transformation()
                    ruplegnull_transform_worldmatrix = ruplegnull_transform_trans.asMatrix()

                    ruplegnull_transform_localmatrix = ruplegnull_transform_worldmatrix * rootctrl_transform_worldmatrix

                    ruplegnull_transform.setTransformation(om2.MTransformationMatrix(ruplegnull_transform_localmatrix))

                    self.ctrl_mod_n.renameNode(ctrl_ruplegpositive_comb_cv, "FkRightUpLeg_shape")
                    self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 1 "Biped_FkRightUpLeg_ctrl"')
                    self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkRightUpLeg_ctrl"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_null.translateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_null.translateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_null.translateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_null.rotateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_null.rotateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_null.rotateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_null.scaleX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_null.scaleY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_null.scaleZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_null.visibility"')
                    self.ctrl_mod_n.doIt()

                elif index == 1:
                    self.rlegnull_tn = ctrl_tr_n.create("transform", "Biped_FkRightLeg_null", self.ruplegupctrl_tn)
                    self.rlegctrl_tn = ctrl_tr_n.create("transform", "Biped_FkRightLeg_ctrl", self.rlegnull_tn)
                    ctrl_rlegpositive_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rlegctrl_tn)

                    rlegnull_transform = om2.MFnTransform(self.rlegnull_tn)
                    rlegnull_transform.setRotatePivotTranslation(jnt_rleg_t, om2.MSpace.kTransform)

                    jnt_rleg_r = cmds.xform("RightLeg", query=True, rotation=True, worldSpace=True)

                    radian_rlegnull_x = (jnt_rleg_r[0]/180)*3.1415
                    radian_rlegnull_y = (jnt_rleg_r[1]/180)*3.1415
                    radian_rlegnull_z = (jnt_rleg_r[2]/180)*3.1415

                    rlegnull_transform_r = rlegnull_transform.rotation(om2.MSpace.kTransform)
                    rlegnull_transform_r[0], rlegnull_transform_r[1], rlegnull_transform_r[2] = radian_rlegnull_x, radian_rlegnull_y, radian_rlegnull_z
                    rlegnull_transform.setRotation(rlegnull_transform_r, om2.MSpace.kTransform)

                    rlegctrl_transform = om2.MFnTransform(self.rlegctrl_tn)

                    rlegctrl_transform_r = rlegnull_transform.rotation(om2.MSpace.kTransform)
                    rlegctrl_transform_r[0], rlegctrl_transform_r[1], rlegctrl_transform_r[2] = 0, 1.57079, 0
                    rlegctrl_transform.setRotation(rlegctrl_transform_r, om2.MSpace.kTransform)

                    rlegctrl_transform_s = rlegctrl_transform.findPlug("scale", False)
                    if rlegctrl_transform_s.isCompound:
                        for i in range(rlegctrl_transform_s.numChildren()):
                            child_plug = rlegctrl_transform_s.child(i)
                            attr_value = child_plug.setDouble(box_transform_s[0]/2)

                    rlegnull_transform_trans = rlegnull_transform.transformation()
                    rlegnull_transform_worldmatrix = rlegnull_transform_trans.asMatrix()

                    rlegnull_transform_localmatrix = rlegnull_transform_worldmatrix * rootctrl_transform_worldmatrix * ruplegnull_transform_localmatrix.inverse()

                    rlegnull_transform.setTransformation(om2.MTransformationMatrix(rlegnull_transform_localmatrix))

                    self.ctrl_mod_n.renameNode(ctrl_rlegpositive_comb_cv, "FkRightLeg_shape")
                    self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 1 "Biped_FkRightLeg_ctrl"')
                    self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkRightLeg_ctrl"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_null.translateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_null.translateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_null.translateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_null.rotateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_null.rotateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_null.rotateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_null.scaleX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_null.scaleY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_null.scaleZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_null.visibility"')
                    self.ctrl_mod_n.doIt()

                elif index == 2:
                    self.rlegfootnull_tn = ctrl_tr_n.create("transform", "Biped_FkRightFoot_null", self.rlegctrl_tn)
                    self.rlegfootctrl_tn = ctrl_tr_n.create("transform", "Biped_FkRightFoot_ctrl", self.rlegfootnull_tn)
                    ctrl_rlegfootpositive_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rlegfootctrl_tn)

                    self.riklegfootnull_tn = ctrl_tr_n.create("transform", "Biped_IkRightFoot_null", self.masterctrl_tn)
                    self.riklegfootoffsetnull_tn = ctrl_tr_n.create("transform", "Biped_IkRightFootOffset_null", self.riklegfootnull_tn)
                    self.riklegfootctrl_tn = ctrl_tr_n.create("transform", "Biped_IkRightFoot_ctrl", self.riklegfootoffsetnull_tn)
                    ctrl_riklegfootpositive_comb_cv = ctrl_cv_n.create([crv_ctrl_hand_line_l, crv_ctrl_hand_line, crv_ctrl_hand_line_r], self.riklegfootctrl_tn)

                    self.rfootoption_tn = ctrl_tr_n.create("transform", "Biped_RightFootOptions_ctrl", rleg_sl_ls.getDependNode(2))
                    ctrl_rfootoption_cv = ctrl_cv_n.createWithEditPoints(ctrl_lhandoption_line, 1, 1, False, True, True, self.rfootoption_tn)

                    rlegfootnull_transform = om2.MFnTransform(self.rlegfootnull_tn)
                    rlegfootnull_transform.setRotatePivotTranslation(jnt_rleg_t, om2.MSpace.kTransform)

                    riklegfootnull_transform = om2.MFnTransform(self.riklegfootnull_tn)
                    riklegfootnull_transform.setRotatePivotTranslation(jnt_rleg_t, om2.MSpace.kTransform)

                    riklegfootoffsetnull_transform = om2.MFnTransform(self.riklegfootoffsetnull_tn)

                    rfootoptionctrl_transform = om2.MFnTransform(self.rfootoption_tn)
                    rfootoptionctrl_transform.setRotatePivotTranslation(jnt_rleg_t, om2.MSpace.kTransform)

                    jnt_rlegfoot_r = cmds.xform("RightFoot", query=True, rotation=True, worldSpace=True)

                    radian_rlegfootnull_x = (jnt_rlegfoot_r[0]/180)*3.1415
                    radian_rlegfootnull_y = (jnt_rlegfoot_r[1]/180)*3.1415
                    radian_rlegfootnull_z = (jnt_rlegfoot_r[2]/180)*3.1415

                    rlegfootnull_transform_r = rlegfootnull_transform.rotation(om2.MSpace.kTransform)
                    rlegfootnull_transform_r[0], rlegfootnull_transform_r[1], rlegfootnull_transform_r[2] = radian_rlegfootnull_x, radian_rlegfootnull_y, radian_rlegfootnull_z
                    rlegfootnull_transform.setRotation(rlegfootnull_transform_r, om2.MSpace.kTransform)

                    riklegfootnull_transform.setRotation(rlegfootnull_transform_r, om2.MSpace.kTransform)

                    riklegfootoffsetnull_transform.setRotation(rlegfootnull_transform_r, om2.MSpace.kTransform)

                    rlegfootctrl_transform = om2.MFnTransform(self.rlegfootctrl_tn)

                    riklegfootctrl_transform = om2.MFnTransform(self.riklegfootctrl_tn)

                    rlegfootctrl_transform_r = rlegfootctrl_transform.rotation(om2.MSpace.kTransform)
                    rlegfootctrl_transform_r[0], rlegfootctrl_transform_r[1], rlegfootctrl_transform_r[2] = -1.57079, 0, -1.57079
                    rlegfootctrl_transform.setRotation(rlegfootctrl_transform_r, om2.MSpace.kTransform)

                    riklegfootctrl_transform_t = riklegfootctrl_transform.translation(om2.MSpace.kTransform)
                    riklegfootctrl_transform_t[1], riklegfootctrl_transform_t[2] = -1, -(jnt_rleg_t[2]+2)
                    riklegfootctrl_transform.setTranslation(riklegfootctrl_transform_t, om2.MSpace.kTransform)

                    riklegfootctrl_transform_r = riklegfootctrl_transform.rotation(om2.MSpace.kTransform)
                    riklegfootctrl_transform_r[1] = -1.57079
                    riklegfootctrl_transform.setRotation(riklegfootctrl_transform_r, om2.MSpace.kTransform)

                    rfootoptionctrl_transform_t = rfootoptionctrl_transform.translation(om2.MSpace.kTransform)
                    rfootoptionctrl_transform_t[0] = jnt_rleg_t[0]-7
                    rfootoptionctrl_transform.setTranslation(rfootoptionctrl_transform_t, om2.MSpace.kTransform)

                    rfootoptionctrl_transform_r = rfootoptionctrl_transform.rotation(om2.MSpace.kTransform)
                    rfootoptionctrl_transform_r[0] = -1.57079
                    rfootoptionctrl_transform.setRotation(rfootoptionctrl_transform_r, om2.MSpace.kTransform)

                    rlegfootctrl_transform_s = rlegfootctrl_transform.findPlug("scale", False)
                    if rlegfootctrl_transform_s.isCompound:
                        for i in range(rlegfootctrl_transform_s.numChildren()):
                            child_plug = rlegfootctrl_transform_s.child(i)
                            attr_value = child_plug.setDouble(box_transform_s[0]/2)

                    riklegfootctrl_transform_s = riklegfootctrl_transform.findPlug("scale", False)
                    if riklegfootctrl_transform_s.isCompound:
                        for i in range(riklegfootctrl_transform_s.numChildren()):
                            child_plug = riklegfootctrl_transform_s.child(i)
                            attr_value = child_plug.setDouble(box_transform_s[0]/2)

                    rlegfootnull_transform_trans = rlegfootnull_transform.transformation()
                    rlegfootnull_transform_worldmatrix = rlegfootnull_transform_trans.asMatrix()

                    rlegfootnull_transform_localmatrix = rlegfootnull_transform_worldmatrix * rootctrl_transform_worldmatrix * ruplegnull_transform_localmatrix.inverse() * rlegnull_transform_localmatrix.inverse()

                    rlegfootnull_transform.setTransformation(om2.MTransformationMatrix(rlegfootnull_transform_localmatrix))

                    rfootoptionctrl_transform_trans = rfootoptionctrl_transform.transformation()
                    rfootoptionctrl_transform_worldmatrix = rfootoptionctrl_transform_trans.asMatrix()

                    rfootoptionctrl_transform_localmatrix = rfootoptionctrl_transform_worldmatrix * rootctrl_transform_worldmatrix * ruplegnull_transform_localmatrix.inverse() * rlegnull_transform_localmatrix.inverse() * rlegfootnull_transform_localmatrix.inverse()

                    rfootoptionctrl_transform.setTransformation(om2.MTransformationMatrix(rfootoptionctrl_transform_localmatrix))

                    self.ctrl_mod_n.renameNode(ctrl_rlegfootpositive_comb_cv, "RightLegFoot_shape")
                    self.ctrl_mod_n.renameNode(ctrl_riklegfootpositive_comb_cv, "RightIkLegFoot_shape")
                    self.ctrl_mod_n.renameNode(ctrl_rfootoption_cv, "RightFootOptions_shape")
                    self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 1 "Biped_FkRightFoot_ctrl"')
                    self.ctrl_mod_n.commandToExecute('color -rgbColor 1 0 1 "Biped_IkRightFoot_ctrl"')
                    self.ctrl_mod_n.commandToExecute('color -rgbColor 1 1 0 "Biped_RightFootOptions_ctrl"')
                    self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkRightFoot_ctrl"')
                    self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_IkRightFoot_ctrl"')
                    self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightFootOptions_ctrl"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_null.translateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_null.translateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_null.translateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_null.rotateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_null.rotateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_null.rotateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_null.scaleX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_null.scaleY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_null.scaleZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_null.visibility"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_null.translateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_null.translateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_null.translateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_null.rotateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_null.rotateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_null.rotateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_null.scaleX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_null.scaleY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_null.scaleZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_null.visibility"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFootOffset_null.translateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFootOffset_null.translateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFootOffset_null.translateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFootOffset_null.rotateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFootOffset_null.rotateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFootOffset_null.rotateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFootOffset_null.scaleX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFootOffset_null.scaleY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFootOffset_null.scaleZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFootOffset_null.visibility"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFootOptions_ctrl.translateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFootOptions_ctrl.translateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFootOptions_ctrl.translateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFootOptions_ctrl.rotateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFootOptions_ctrl.rotateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFootOptions_ctrl.rotateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFootOptions_ctrl.scaleX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFootOptions_ctrl.scaleY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFootOptions_ctrl.scaleZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFootOptions_ctrl.visibility"')
                    self.ctrl_mod_n.doIt()

                    riklegfootctrl_path_n = om2.MDagPath()
                    riklegfootctrl_path = riklegfootctrl_path_n.getAPathTo(self.riklegfootctrl_tn)
                    riklegfootctrl_worldtransform = om2.MFnTransform(riklegfootctrl_path)

                    riklegfootctrl_worldtransform.setRotatePivot(om2.MPoint(jnt_rleg_t), om2.MSpace.kWorld, False)


                elif index == 3:
                    self.rlegtoebasenull_tn = ctrl_tr_n.create("transform", "Biped_FkRightToeBase_null", self.rlegfootctrl_tn)
                    self.rlegtoebasectrl_tn = ctrl_tr_n.create("transform", "Biped_FkRightToeBase_ctrl", self.rlegtoebasenull_tn)
                    ctrl_rlegtoepositive_comb_cv = ctrl_cv_n.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rlegtoebasectrl_tn)

                    rlegtoebasenull_transform = om2.MFnTransform(self.rlegtoebasenull_tn)
                    rlegtoebasenull_transform.setRotatePivotTranslation(jnt_rleg_t, om2.MSpace.kTransform)

                    jnt_rlegtoebase_r = cmds.xform("RightToeBase", query=True, rotation=True, worldSpace=True)

                    radian_rlegtoebasenull_x = (jnt_rlegtoebase_r[0]/180)*3.1415
                    radian_rlegtoebasenull_y = (jnt_rlegtoebase_r[1]/180)*3.1415
                    radian_rlegtoebasenull_z = (jnt_rlegtoebase_r[2]/180)*3.1415

                    rlegtoebasenull_transform_r = rlegtoebasenull_transform.rotation(om2.MSpace.kTransform)
                    rlegtoebasenull_transform_r[0], rlegtoebasenull_transform_r[1], rlegtoebasenull_transform_r[2] = radian_rlegtoebasenull_x, radian_rlegtoebasenull_y, radian_rlegtoebasenull_z
                    rlegtoebasenull_transform.setRotation(rlegtoebasenull_transform_r, om2.MSpace.kTransform)

                    rlegtoebasectrl_transform = om2.MFnTransform(self.rlegtoebasectrl_tn)

                    rlegtoebasectrl_transform_r = rlegtoebasectrl_transform.rotation(om2.MSpace.kTransform)
                    rlegtoebasectrl_transform_r[1] = -1.57079
                    rlegtoebasectrl_transform.setRotation(rlegtoebasectrl_transform_r, om2.MSpace.kTransform)

                    rlegtoebasectrl_transform_s = rlegtoebasectrl_transform.findPlug("scale", False)
                    if rlegtoebasectrl_transform_s.isCompound:
                        for i in range(rlegtoebasectrl_transform_s.numChildren()):
                            child_plug = rlegtoebasectrl_transform_s.child(i)
                            attr_value = child_plug.setDouble(box_transform_s[0]/4)

                    rlegtoebasenull_transform_trans = rlegtoebasenull_transform.transformation()
                    rlegtoebasenull_transform_worldmatrix = rlegtoebasenull_transform_trans.asMatrix()

                    rlegtoebasenull_transform_localmatrix = rlegtoebasenull_transform_worldmatrix * rootctrl_transform_worldmatrix * ruplegnull_transform_localmatrix.inverse() * rlegnull_transform_localmatrix.inverse() * rlegfootnull_transform_localmatrix.inverse()

                    rlegtoebasenull_transform.setTransformation(om2.MTransformationMatrix(rlegtoebasenull_transform_localmatrix))

                    self.ctrl_mod_n.renameNode(ctrl_rlegtoepositive_comb_cv, "FkRightLegToeBase_shape")
                    self.ctrl_mod_n.commandToExecute('color -rgbColor 0 1 1 "Biped_FkRightToeBase_ctrl"')
                    self.ctrl_mod_n.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkRightToeBase_ctrl"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_null.translateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_null.translateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_null.translateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_null.rotateX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_null.rotateY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_null.rotateZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_null.scaleX"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_null.scaleY"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_null.scaleZ"')
                    self.ctrl_mod_n.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_null.visibility"')
                    self.ctrl_mod_n.doIt()

        obj_root = om1.MObject()
        obj_endspine = om1.MObject()
        obj_masterctrl1 = om1.MObject()
        ik_system = omanim1.MIkSystem()
        ik_effector = omanim1.MFnIkEffector()
        ik_handle = omanim1.MFnIkHandle()
        ikspline_cv_n = om1.MFnNurbsCurve()

        masterctrl_sl_lst2 = om2.MSelectionList()
        masterctrl_sl_lst2.add("Biped_Master_ctrl")
        obj_masterctrl2 = masterctrl_sl_lst2.getDependNode(0)

        if self.autostretch.currentIndex() == 1:
            if cmds.objExists("IkHip") and cmds.objExists("IkCvHip") and cmds.objExists("IkCvSpine"):
                ikspineiksolver_lst = om1.MSelectionList()
                ikspinedag_n = om1.MFnDagNode()
                ikspineobj_path_n = om1.MDagPath()
                ikspinedg_modifier = om1.MDGModifier()

                ikspine_sl_lst = om1.MSelectionList()
                ikspine_sl_lst.add("IkHip")
                ikspine_sl_lst.add("IkSpin*")
                ikspine_sl_lst.getDependNode(0, obj_root)
                ikspine_sl_lst.getDependNode(ikspine_sl_lst.length()-1, obj_endspine)

                masterctrl_sl_lst1 = om1.MSelectionList()
                masterctrl_sl_lst1.add("Biped_Master_ctrl")
                masterctrl_sl_lst1.getDependNode(0, obj_masterctrl1)

                spine_pathnode = om1.MDagPath()
                rootspine_path = spine_pathnode.getAPathTo(obj_root)

                try:
                    ikspineiksolver_lst.add("ikSplineSolver")
                except:
                    cmds.createNode("ikSplineSolver")

                self.ikspline_effector = ik_effector.create(obj_endspine)
                ikspine_effector_path = spine_pathnode.getAPathTo(self.ikspline_effector)

                self.spine_ik = ik_handle.create(rootspine_path, ikspine_effector_path)

                obj_array = om1.MPointArray()
                obj_lst_mpoint = []
                obj = om1.MObject()
                for index in range(ikspine_sl_lst.length()):
                    ikspine_sl_lst.getDependNode(index, obj)
                    obj_path = ikspineobj_path_n.getAPathTo(obj)
                    obj_tn = om1.MFnTransform(obj_path)
                    obj_t = obj_tn.translation(om1.MSpace.kWorld)
                    obj_lst_mpoint.append(om1.MPoint(obj_t))
                    obj_array.append(obj_lst_mpoint[index])

                self.ikspline_cv_tn = ikspinedag_n.create("transform", "BackBone_SplineCv")
                ikspline_cv = ikspline_cv_n.createWithEditPoints(obj_array, 1, 1, False, True, True, self.ikspline_cv_tn)
                cmds.parent("BackBone_SplineCv", "DoNotTouch")

                spinecrv_info = ikspinedg_modifier.createNode("curveInfo")
                spinestretchpercent = ikspinedg_modifier.createNode("multiplyDivide")
                spinestretchpow = ikspinedg_modifier.createNode("multiplyDivide")
                spinestretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                spinescalediv = ikspinedg_modifier.createNode("multiplyDivide")

                spinecrvinfo_fs = om1.MFnDependencyNode(spinecrv_info)
                spinestretchpercent_fs = om1.MFnDependencyNode(spinestretchpercent)
                spinestretchpow_fs = om1.MFnDependencyNode(spinestretchpow)
                spinestretchdiv_fs = om1.MFnDependencyNode(spinestretchdiv)
                spinescalediv_fs = om1.MFnDependencyNode(spinescalediv)
                masterctrl_fs = om1.MFnDependencyNode(obj_masterctrl1)

                spinecrvinfoarc_plug = spinecrvinfo_fs.findPlug("arcLength")
                spinestretchpercentinp1y_plug = spinestretchpercent_fs.findPlug("input1Y")
                spinestretchpercentotp_plug = spinestretchpercent_fs.findPlug("outputY")
                spinestretchpowinp1x_plug = spinestretchpow_fs.findPlug("input1X")
                spinestretchpowinp1z_plug = spinestretchpow_fs.findPlug("input1Z")
                spinestretchpowotpx_plug = spinestretchpow_fs.findPlug("outputX")
                spinestretchpowotpz_plug = spinestretchpow_fs.findPlug("outputZ")
                spinestretchdivinp2x_plug = spinestretchdiv_fs.findPlug("input2X")
                spinestretchdivinp2z_plug = spinestretchdiv_fs.findPlug("input2Z")
                spinestretchdivotox_plug = spinestretchdiv_fs.findPlug("outputX")
                spinestretchdivotpz_plug = spinestretchdiv_fs.findPlug("outputZ")
                spinescaledivinp1y_plug = spinescalediv_fs.findPlug("input1Y")
                spinescaledivinp2y_plug = spinescalediv_fs.findPlug("input2Y")
                spinescaledivotpy_plug = spinescalediv_fs.findPlug("outputY")
                masterctrlsy_plug = masterctrl_fs.findPlug("scaleY")

                objparent = om1.MObject()
                objchild = om1.MObject()
                for index in range(ikspine_sl_lst.length()):
                    if index < ikspine_sl_lst.length()-1:
                        ikspine_sl_lst.getDependNode(index, objparent)
                        ikspine_sl_lst.getDependNode(index+1, objchild)
                        spineparentjnt_fs = om1.MFnDependencyNode(objparent)
                        spinechildjnt_fs = om1.MFnDependencyNode(objchild)
                        spinejnt_syplug = spineparentjnt_fs.findPlug("scaleY")
                        spinejnt_sxplug = spineparentjnt_fs.findPlug("scaleX")
                        spinejnt_szplug = spineparentjnt_fs.findPlug("scaleZ")
                        spinejnt_sotpplug = spineparentjnt_fs.findPlug("scale")
                        spinejnt_invsplug = spinechildjnt_fs.findPlug("inverseScale")
                        ikspinedg_modifier.connect(spinestretchpercentotp_plug, spinejnt_syplug)
                        ikspinedg_modifier.connect(spinestretchdivotox_plug, spinejnt_sxplug)
                        ikspinedg_modifier.connect(spinestretchdivotpz_plug, spinejnt_szplug)
                        ikspinedg_modifier.connect(spinejnt_sotpplug, spinejnt_invsplug)

                ikspinedg_modifier.renameNode(spinecrv_info, "BackBoneSpline_Info")
                ikspinedg_modifier.renameNode(spinestretchpercent, "BackBoneStretch_Percent")
                ikspinedg_modifier.renameNode(spinestretchpow, "BackBoneStretch_Power")
                ikspinedg_modifier.renameNode(spinestretchdiv, "BackBoneStretch_Divide")
                ikspinedg_modifier.renameNode(ikspline_cv, "BackBone_SplineCvShape")
                ikspinedg_modifier.renameNode(self.spine_ik, "BackBone_Ik")
                ikspinedg_modifier.renameNode(self.ikspline_effector, "BackBone_effector")
                ikspinedg_modifier.renameNode(spinescalediv, "IkSpineGlobalScale_Average")
                ikspinedg_modifier.commandToExecute('parent "BackBone_Ik" "DoNotTouch"')
                ikspinedg_modifier.commandToExecute('connectAttr -f BackBone_SplineCvShape.worldSpace[0] BackBone_Ik.inCurve')
                ikspinedg_modifier.commandToExecute('skinCluster -bm 3 -sm 1 -dr 2.0 -name "SpineIk_skin" IkCvHip IkCvSpine BackBone_SplineCv')
                ikspinedg_modifier.commandToExecute('setAttr "BackBone_Ik.dTwistControlEnable" 1')
                ikspinedg_modifier.commandToExecute('setAttr "BackBone_Ik.dWorldUpType" 4')
                ikspinedg_modifier.commandToExecute('setAttr "BackBone_Ik.dForwardAxis" 2')
                ikspinedg_modifier.commandToExecute('setAttr "BackBone_Ik.dWorldUpAxis" 4')
                ikspinedg_modifier.commandToExecute('setAttr "BackBone_Ik.dWorldUpVectorY" 0')
                ikspinedg_modifier.commandToExecute('setAttr "BackBone_Ik.dWorldUpVectorEndY" 0')
                ikspinedg_modifier.commandToExecute('setAttr "BackBone_Ik.dWorldUpVectorZ" -1')
                ikspinedg_modifier.commandToExecute('setAttr "BackBone_Ik.dWorldUpVectorEndZ" -1')
                ikspinedg_modifier.commandToExecute('connectAttr -f IkCvHip.worldMatrix[0] BackBone_Ik.dWorldUpMatrix')
                ikspinedg_modifier.commandToExecute('connectAttr -f IkCvSpine.worldMatrix[0] BackBone_Ik.dWorldUpMatrixEnd')
                ikspinedg_modifier.commandToExecute('connectAttr -f BackBone_SplineCvShape.worldSpace[0] BackBoneSpline_Info.inputCurve')
                ikspinedg_modifier.connect(spinecrvinfoarc_plug, spinescaledivinp1y_plug)
                ikspinedg_modifier.connect(masterctrlsy_plug, spinescaledivinp2y_plug)
                ikspinedg_modifier.connect(spinescaledivotpy_plug, spinestretchpercentinp1y_plug)
                ikspinedg_modifier.connect(spinestretchpercentotp_plug, spinestretchpowinp1x_plug)
                ikspinedg_modifier.connect(spinestretchpercentotp_plug, spinestretchpowinp1z_plug)
                ikspinedg_modifier.connect(spinestretchpowotpx_plug, spinestretchdivinp2x_plug)
                ikspinedg_modifier.connect(spinestretchpowotpz_plug, spinestretchdivinp2z_plug)
                ikspinedg_modifier.commandToExecute('float $backbonestretchinput1Y = `getAttr "BackBoneStretch_Percent.input1Y"`; setAttr "BackBoneStretch_Percent.input2Y" $backbonestretchinput1Y')
                ikspinedg_modifier.commandToExecute('setAttr "BackBoneStretch_Power.input2X" 0.5')
                ikspinedg_modifier.commandToExecute('setAttr "BackBoneStretch_Power.input2Z" 0.5')
                ikspinedg_modifier.commandToExecute('setAttr "BackBoneStretch_Divide.input1X" 1')
                ikspinedg_modifier.commandToExecute('setAttr "BackBoneStretch_Divide.input1Z" 1')
                ikspinedg_modifier.commandToExecute('setAttr "BackBoneStretch_Percent.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "BackBoneStretch_Power.operation" 3')
                ikspinedg_modifier.commandToExecute('setAttr "BackBoneStretch_Divide.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "IkSpineGlobalScale_Average.operation" 2')
                ikspinedg_modifier.doIt()

                ikspline_solver = ik_system.findSolver("ikSplineSolver")
                ik_handle.setSolver(ikspline_solver)

            # ikspine_sl_lst2 = om2.MSelectionList()
            # ikspine_sl_lst2.add("IkHip")
            # ikspine_sl_lst2.add("IkSpin*")
            #
            # for index in range(ikspine_sl_lst2.length()):
            #     jnt_obj = ikspine_sl_lst2.getDependNode(index)
            #     jnt_string = ikspine_sl_lst2.getSelectionStrings(index)
            #
            #     if jnt_obj.hasFn(om2.MFn.kJoint):
            #         if cmds.getAttr("{0}.jointOrientX".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientY".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientZ".format(str(jnt_string)[3:][:-3])) != 0:
            #             self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientX" 0'.format(str(jnt_string)[3:][:-3]))
            #             self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientY" 0'.format(str(jnt_string)[3:][:-3]))
            #             self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientZ" 0'.format(str(jnt_string)[3:][:-3]))

        iksplinegrp_sl_ls = om2.MSelectionList()
        iksplinegrp_sl_ls.add("SplineIk_grp")

        masterscale_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
        masterscale_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
        self.ctrl_mod_n.renameNode(masterscale_multMatrix, "MasterScale_multMatrix")
        self.ctrl_mod_n.renameNode(masterscale_decomposeMatrix, "MasterScale_decomposeMatrix")

        masterscalemultMatrix_fs = om2.MFnDependencyNode(masterscale_multMatrix)
        masterscaledecomposeMatrix_fs = om2.MFnDependencyNode(masterscale_decomposeMatrix)
        splineik_fs = om2.MFnDependencyNode(iksplinegrp_sl_ls.getDependNode(0))

        rootmultMatrixSum_plug = masterscalemultMatrix_fs.findPlug("matrixSum", False)
        rootdecomposeInpMatrix_plug = masterscaledecomposeMatrix_fs.findPlug("inputMatrix", False)
        rootdecomposeOtpScale_plug = masterscaledecomposeMatrix_fs.findPlug("outputScale", False)
        splineikScale_plug = splineik_fs.findPlug("scale", False)

        self.ctrl_mod_n.commandToExecute('connectAttr - force Biped_Master_ctrl.worldMatrix[0] MasterScale_multMatrix.matrixIn[0]')
        self.ctrl_mod_n.connect(rootmultMatrixSum_plug, rootdecomposeInpMatrix_plug)
        self.ctrl_mod_n.connect(rootdecomposeOtpScale_plug, splineikScale_plug)

        rootctrl_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
        rootctrl_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
        self.ctrl_mod_n.renameNode(rootctrl_multMatrix, "Hip_multMatrix")
        self.ctrl_mod_n.renameNode(rootctrl_decomposeMatrix, "Hip_decomposeMatrix")

        rootmultMatrix_fs = om2.MFnDependencyNode(rootctrl_multMatrix)
        rootdecomposeMatrix_fs = om2.MFnDependencyNode(rootctrl_decomposeMatrix)
        hipjnt_fs = om2.MFnDependencyNode(hip_obj)

        rootmultMatrixSum_plug = rootmultMatrix_fs.findPlug("matrixSum", False)
        rootdecomposeInpMatrix_plug = rootdecomposeMatrix_fs.findPlug("inputMatrix", False)
        rootdecomposeOtpTrans_plug = rootdecomposeMatrix_fs.findPlug("outputTranslate", False)
        rootdecomposeOtpRot_plug = rootdecomposeMatrix_fs.findPlug("outputRotate", False)
        hipjntTrans_plug = hipjnt_fs.findPlug("translate", False)
        hipjntRot_plug = hipjnt_fs.findPlug("rotate", False)

        self.ctrl_mod_n.commandToExecute('connectAttr - force Biped_Root_ctrl.worldMatrix[0] Hip_multMatrix.matrixIn[0]')
        self.ctrl_mod_n.commandToExecute('connectAttr -force Hip.parentInverseMatrix[0] Hip_multMatrix.matrixIn[1]')
        self.ctrl_mod_n.connect(rootmultMatrixSum_plug, rootdecomposeInpMatrix_plug)
        self.ctrl_mod_n.connect(rootdecomposeOtpTrans_plug, hipjntTrans_plug)
        self.ctrl_mod_n.connect(rootdecomposeOtpRot_plug, hipjntRot_plug)

        if self.autostretch.currentIndex() == 1:
            if cmds.objExists("IkHip") and cmds.objExists("IkCvHip") and cmds.objExists("IkCvSpine"):
                ikcvspinespline_sl_lst = om2.MSelectionList()
                ikcvspinespline_sl_lst.add("IkCvHip")
                ikcvspinespline_sl_lst.add("IkCvSpine")

                hipctrl_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
                hipctrl_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                self.ctrl_mod_n.renameNode(hipctrl_multMatrix, "Hiprot_multMatrix")
                self.ctrl_mod_n.renameNode(hipctrl_decomposeMatrix, "Hiprot_decomposeMatrix")

                hipmultMatrix_fs = om2.MFnDependencyNode(hipctrl_multMatrix)
                hipdecomposeMatrix_fs = om2.MFnDependencyNode(hipctrl_decomposeMatrix)
                hiprotjnt_fs = om2.MFnDependencyNode(ikcvspinespline_sl_lst.getDependNode(0))

                hipmultMatrixSum_plug = hipmultMatrix_fs.findPlug("matrixSum", False)
                hipdecomposeInpMatrix_plug = hipdecomposeMatrix_fs.findPlug("inputMatrix", False)
                hipdecomposeOtpTrans_plug = hipdecomposeMatrix_fs.findPlug("outputTranslate", False)
                hipdecomposeOtpRot_plug = hipdecomposeMatrix_fs.findPlug("outputRotate", False)
                hiprotjntTrans_plug = hiprotjnt_fs.findPlug("translate", False)
                hiprotjntRot_plug = hiprotjnt_fs.findPlug("rotate", False)

                self.ctrl_mod_n.commandToExecute('connectAttr - force Biped_Hip_ctrl.worldMatrix[0] Hiprot_multMatrix.matrixIn[0]')
                self.ctrl_mod_n.commandToExecute('connectAttr -force IkCvHip.parentInverseMatrix[0] Hiprot_multMatrix.matrixIn[1]')
                self.ctrl_mod_n.connect(hipmultMatrixSum_plug, hipdecomposeInpMatrix_plug)
                self.ctrl_mod_n.connect(hipdecomposeOtpTrans_plug, hiprotjntTrans_plug)
                self.ctrl_mod_n.connect(hipdecomposeOtpRot_plug, hiprotjntRot_plug)
                if cmds.getAttr("IkCvSpine.jointOrientX") != 0 or cmds.getAttr("IkCvSpine.jointOrientX") != 0 or cmds.getAttr("IkCvSpine.jointOrientX") != 0:
                    self.ctrl_mod_n.commandToExecute('setAttr "IkCvSpine.jointOrientX" 0')
                    self.ctrl_mod_n.commandToExecute('setAttr "IkCvSpine.jointOrientY" 0')
                    self.ctrl_mod_n.commandToExecute('setAttr "IkCvSpine.jointOrientZ" 0')

        elif cmds.objExists("IkCvHip"):
            self.ctrl_mod_n.commandToExecute('delete "IkCvHip"')
            self.ctrl_mod_n.commandToExecute('delete "IkHip"')
            self.ctrl_mod_n.commandToExecute('delete "Biped_Hip_ctrl"')
            self.ctrl_mod_n.commandToExecute('delete "Biped_StretchySpine_ctrl"')

        elif cmds.objExists("Biped_StretchySpine_ctrl"):
            self.ctrl_mod_n.commandToExecute('delete "Biped_StretchySpine_ctrl"')

        for index in range(spine_sl_lst.length()):
            spinectrl_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
            spinectrl_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
            self.ctrl_mod_n.renameNode(spinectrl_multMatrix, "Spine{0}_multMatrix".format(index))
            self.ctrl_mod_n.renameNode(spinectrl_decomposeMatrix, "Spine{0}_decomposeMatrix".format(index))

            spinemultMatrix_fs = om2.MFnDependencyNode(spinectrl_multMatrix)
            spinedecomposeMatrix_fs = om2.MFnDependencyNode(spinectrl_decomposeMatrix)
            spinejnt_fs = om2.MFnDependencyNode(spine_sl_lst.getDependNode(index))

            spinemultMatrixSum_plug = spinemultMatrix_fs.findPlug("matrixSum", False)
            spinedecomposeInpMatrix_plug = spinedecomposeMatrix_fs.findPlug("inputMatrix", False)
            spinedecomposeOtpTrans_plug = spinedecomposeMatrix_fs.findPlug("outputTranslate", False)
            spinedecomposeOtpRot_plug = spinedecomposeMatrix_fs.findPlug("outputRotate", False)
            spinejntTrans_plug = spinejnt_fs.findPlug("translate", False)
            spinejntRot_plug = spinejnt_fs.findPlug("rotate", False)

            self.ctrl_mod_n.commandToExecute('connectAttr -force Biped_Spine{0}_ctrl.worldMatrix[0] Spine{0}_multMatrix.matrixIn[0]'.format(index))
            self.ctrl_mod_n.commandToExecute('connectAttr -force Spine{0}.parentInverseMatrix[0] Spine{0}_multMatrix.matrixIn[1]'.format(index))
            self.ctrl_mod_n.connect(spinemultMatrixSum_plug, spinedecomposeInpMatrix_plug)
            self.ctrl_mod_n.connect(spinedecomposeOtpTrans_plug, spinejntTrans_plug)
            self.ctrl_mod_n.connect(spinedecomposeOtpRot_plug, spinejntRot_plug)

            jnt_string = spine_sl_lst.getSelectionStrings(index)
            if cmds.getAttr("{0}.jointOrientX".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientY".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientZ".format(str(jnt_string)[3:][:-3])) != 0:
                self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientX" 0'.format(str(jnt_string)[3:][:-3]))
                self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientY" 0'.format(str(jnt_string)[3:][:-3]))
                self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientZ" 0'.format(str(jnt_string)[3:][:-3]))

        if self.autostretch.currentIndex() == 1:
            if cmds.objExists("IkHip") and cmds.objExists("IkCvHip") and cmds.objExists("IkCvSpine"):
                ikspinectrl_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
                ikspinectrl_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                self.ctrl_mod_n.renameNode(ikspinectrl_multMatrix, "IkSpine_multMatrix")
                self.ctrl_mod_n.renameNode(ikspinectrl_decomposeMatrix, "IkSpine_decomposeMatrix")

                spinesplinemultMatrix_fs = om2.MFnDependencyNode(ikspinectrl_multMatrix)
                spinesplinedecomposeMatrix_fs = om2.MFnDependencyNode(ikspinectrl_decomposeMatrix)
                spinesplinejnt_fs = om2.MFnDependencyNode(ikcvspinespline_sl_lst.getDependNode(1))

                spinesplinemultMatrixSum_plug = spinesplinemultMatrix_fs.findPlug("matrixSum", False)
                spinesplinedecomposeInpMatrix_plug = spinesplinedecomposeMatrix_fs.findPlug("inputMatrix", False)
                spinesplinedecomposeOtpTrans_plug = spinesplinedecomposeMatrix_fs.findPlug("outputTranslate", False)
                spinesplinedecomposeOtpRot_plug = spinesplinedecomposeMatrix_fs.findPlug("outputRotate", False)
                spinesplinejntTrans_plug = spinesplinejnt_fs.findPlug("translate", False)
                spinesplinejntRot_plug = spinesplinejnt_fs.findPlug("rotate", False)

                self.ctrl_mod_n.commandToExecute('connectAttr -force Biped_StretchySpine_ctrl.worldMatrix[0] IkSpine_multMatrix.matrixIn[0]')
                self.ctrl_mod_n.commandToExecute('connectAttr -force IkCvSpine.parentInverseMatrix[0] IkSpine_multMatrix.matrixIn[1]')
                self.ctrl_mod_n.connect(spinesplinemultMatrixSum_plug, spinesplinedecomposeInpMatrix_plug)
                self.ctrl_mod_n.connect(spinesplinedecomposeOtpTrans_plug, spinesplinejntTrans_plug)
                self.ctrl_mod_n.connect(spinesplinedecomposeOtpRot_plug, spinesplinejntRot_plug)

        elif cmds.objExists("IkCvSpine"):
            self.ctrl_mod_n.commandToExecute('delete "IkCvSpine"')

        if self.autostretch.currentIndex() == 1:
            if cmds.objExists("IkNeck*") and cmds.objExists("IkCvNeck") and cmds.objExists("IkCvHead"):
                ikneckspline_sl_lst = om1.MSelectionList()
                ikneckspline_sl_lst.add("IkNeck*")
                ikneckspline_sl_lst.getDependNode(0, obj_root)
                ikneckspline_sl_lst.getDependNode(ikneckspline_sl_lst.length()-1, obj_endspine)

                neck_pathnode = om1.MDagPath()
                neck_path = neck_pathnode.getAPathTo(obj_root)

                self.ikneckspline_effector = ik_effector.create(obj_endspine)
                ikneckspine_effector_path = neck_pathnode.getAPathTo(self.ikneckspline_effector)

                self.neckspine_ik = ik_handle.create(neck_path, ikneckspine_effector_path)

                neckobj_array = om1.MPointArray()
                neckobj_lst_mpoint = []
                neckobj = om1.MObject()
                for index in range(ikneckspline_sl_lst.length()):
                    ikneckspline_sl_lst.getDependNode(index, neckobj)
                    obj_path = ikspineobj_path_n.getAPathTo(neckobj)
                    obj_tn = om1.MFnTransform(obj_path)
                    obj_t = obj_tn.translation(om1.MSpace.kWorld)
                    neckobj_lst_mpoint.append(om1.MPoint(obj_t))
                    neckobj_array.append(neckobj_lst_mpoint[index])

                self.ikneckspline_cv_tn = ikspinedag_n.create("transform", "Neck_SplineCv")
                ikneckspline_cv = ikspline_cv_n.createWithEditPoints(neckobj_array, 1, 1, False, True, True, self.ikneckspline_cv_tn)
                cmds.parent("Neck_SplineCv", "DoNotTouch")

                neckcrv_info = ikspinedg_modifier.createNode("curveInfo")
                neckstretchpercent = ikspinedg_modifier.createNode("multiplyDivide")
                neckstretchpow = ikspinedg_modifier.createNode("multiplyDivide")
                neckstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                neckscalediv = ikspinedg_modifier.createNode("multiplyDivide")

                neckcrvinfo_fs = om1.MFnDependencyNode(neckcrv_info)
                neckstretchpercent_fs = om1.MFnDependencyNode(neckstretchpercent)
                neckstretchpow_fs = om1.MFnDependencyNode(neckstretchpow)
                neckstretchdiv_fs = om1.MFnDependencyNode(neckstretchdiv)
                neckscale_fs = om1.MFnDependencyNode(neckscalediv)

                neckcrvinfoarc_plug = neckcrvinfo_fs.findPlug("arcLength")
                neckstretchpercentinp_plug = neckstretchpercent_fs.findPlug("input1Y")
                neckstretchpercentotp_plug = neckstretchpercent_fs.findPlug("outputY")
                neckstretchpowinpx_plug = neckstretchpow_fs.findPlug("input1X")
                neckstretchpowinpz_plug = neckstretchpow_fs.findPlug("input1Z")
                neckstretchpowotpx_plug = neckstretchpow_fs.findPlug("outputX")
                neckstretchpowotpz_plug = neckstretchpow_fs.findPlug("outputZ")
                neckstretchdivinpx_plug = neckstretchdiv_fs.findPlug("input2X")
                neckstretchdivinpz_plug = neckstretchdiv_fs.findPlug("input2Z")
                neckstretchdivotox_plug = neckstretchdiv_fs.findPlug("outputX")
                neckstretchdivotpz_plug = neckstretchdiv_fs.findPlug("outputZ")
                neckscaledivinp1y_plug = neckscale_fs.findPlug("input1Y")
                neckscaledivinp2y_plug = neckscale_fs.findPlug("input2Y")
                neckscaledivotpy_plug = neckscale_fs.findPlug("outputY")

                objparent = om1.MObject()
                objchild = om1.MObject()
                for index in range(ikneckspline_sl_lst.length()):
                    if index < ikneckspline_sl_lst.length()-1:
                        ikneckspline_sl_lst.getDependNode(index, objparent)
                        ikneckspline_sl_lst.getDependNode(index+1, objchild)
                        neckparentjnt_fs = om1.MFnDependencyNode(objparent)
                        neckchildjnt_fs = om1.MFnDependencyNode(objchild)
                        neckjnt_syplug = neckparentjnt_fs.findPlug("scaleY")
                        neckjnt_sxplug = neckparentjnt_fs.findPlug("scaleX")
                        neckjnt_szplug = neckparentjnt_fs.findPlug("scaleZ")
                        neckjnt_sotpplug = neckparentjnt_fs.findPlug("scale")
                        neckjnt_invsplug = neckchildjnt_fs.findPlug("inverseScale")
                        ikspinedg_modifier.connect(neckstretchpercentotp_plug, neckjnt_syplug)
                        ikspinedg_modifier.connect(neckstretchdivotox_plug, neckjnt_sxplug)
                        ikspinedg_modifier.connect(neckstretchdivotpz_plug, neckjnt_szplug)
                        ikspinedg_modifier.connect(neckjnt_sotpplug, neckjnt_invsplug)

                ikspinedg_modifier.renameNode(neckcrv_info, "NeckSpline_Info")
                ikspinedg_modifier.renameNode(neckstretchpercent, "NeckStretch_Percent")
                ikspinedg_modifier.renameNode(neckstretchpow, "NeckStretch_Power")
                ikspinedg_modifier.renameNode(neckstretchdiv, "NeckStretch_Divide")
                ikspinedg_modifier.renameNode(ikneckspline_cv, "Neck_SplineCvShape")
                ikspinedg_modifier.renameNode(self.neckspine_ik, "Neck_Ik")
                ikspinedg_modifier.renameNode(self.ikneckspline_effector, "Neck_effector")
                ikspinedg_modifier.renameNode(neckscalediv, "IkNeckGlobalScale_Average")
                ikspinedg_modifier.commandToExecute('parent "Neck_Ik" "DoNotTouch"')
                ikspinedg_modifier.commandToExecute('connectAttr -f Neck_SplineCvShape.worldSpace[0] Neck_Ik.inCurve')
                ikspinedg_modifier.commandToExecute('skinCluster -bm 3 -sm 1 -dr 2.0 -name "NeckIk_skin" IkCvNeck IkCvHead Neck_SplineCv')
                ikspinedg_modifier.commandToExecute('setAttr "Neck_Ik.dTwistControlEnable" 1')
                ikspinedg_modifier.commandToExecute('setAttr "Neck_Ik.dWorldUpType" 4')
                ikspinedg_modifier.commandToExecute('setAttr "Neck_Ik.dForwardAxis" 2')
                ikspinedg_modifier.commandToExecute('setAttr "Neck_Ik.dWorldUpAxis" 4')
                ikspinedg_modifier.commandToExecute('setAttr "Neck_Ik.dWorldUpVectorY" 0')
                ikspinedg_modifier.commandToExecute('setAttr "Neck_Ik.dWorldUpVectorEndY" 0')
                ikspinedg_modifier.commandToExecute('setAttr "Neck_Ik.dWorldUpVectorZ" -1')
                ikspinedg_modifier.commandToExecute('setAttr "Neck_Ik.dWorldUpVectorEndZ" -1')
                ikspinedg_modifier.commandToExecute('connectAttr -f IkCvNeck.worldMatrix[0] Neck_Ik.dWorldUpMatrix')
                ikspinedg_modifier.commandToExecute('connectAttr -f IkCvHead.worldMatrix[0] Neck_Ik.dWorldUpMatrixEnd')
                ikspinedg_modifier.commandToExecute('connectAttr -f Neck_SplineCvShape.worldSpace[0] NeckSpline_Info.inputCurve')
                ikspinedg_modifier.connect(neckcrvinfoarc_plug, neckscaledivinp1y_plug)
                ikspinedg_modifier.connect(masterctrlsy_plug, neckscaledivinp2y_plug)
                ikspinedg_modifier.connect(neckscaledivotpy_plug, neckstretchpercentinp_plug)
                ikspinedg_modifier.connect(neckstretchpercentotp_plug, neckstretchpowinpx_plug)
                ikspinedg_modifier.connect(neckstretchpercentotp_plug, neckstretchpowinpz_plug)
                ikspinedg_modifier.connect(neckstretchpowotpx_plug, neckstretchdivinpx_plug)
                ikspinedg_modifier.connect(neckstretchpowotpz_plug, neckstretchdivinpz_plug)
                ikspinedg_modifier.commandToExecute('float $neckstretchinput1Y = `getAttr "NeckStretch_Percent.input1Y"`; setAttr "NeckStretch_Percent.input2Y" $neckstretchinput1Y')
                ikspinedg_modifier.commandToExecute('setAttr "NeckStretch_Power.input2X" 0.5')
                ikspinedg_modifier.commandToExecute('setAttr "NeckStretch_Power.input2Z" 0.5')
                ikspinedg_modifier.commandToExecute('setAttr "NeckStretch_Divide.input1X" 1')
                ikspinedg_modifier.commandToExecute('setAttr "NeckStretch_Divide.input1Z" 1')
                ikspinedg_modifier.commandToExecute('setAttr "NeckStretch_Percent.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "NeckStretch_Power.operation" 3')
                ikspinedg_modifier.commandToExecute('setAttr "NeckStretch_Divide.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "IkNeckGlobalScale_Average.operation" 2')
                ikspinedg_modifier.doIt()

                ikspline_solver = ik_system.findSolver("ikSplineSolver")
                ik_handle.setSolver(ikspline_solver)

            # ikneckspline_sl_lst2 = om2.MSelectionList()
            # ikneckspline_sl_lst2.add("IkNeck*")
            #
            # for index in range(ikneckspline_sl_lst2.length()):
            #     jnt_obj = ikneckspline_sl_lst2.getDependNode(index)
            #     jnt_string = ikneckspline_sl_lst2.getSelectionStrings(index)
            #
            #     if jnt_obj.hasFn(om2.MFn.kJoint):
            #         if cmds.getAttr("{0}.jointOrientX".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientY".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientZ".format(str(jnt_string)[3:][:-3])) != 0:
            #             self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientX" 0'.format(str(jnt_string)[3:][:-3]))
            #             self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientY" 0'.format(str(jnt_string)[3:][:-3]))
            #             self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientZ" 0'.format(str(jnt_string)[3:][:-3]))

        neckctrl_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
        neckctrl_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
        self.ctrl_mod_n.renameNode(neckctrl_multMatrix, "Neck_multMatrix")
        self.ctrl_mod_n.renameNode(neckctrl_decomposeMatrix, "Neck_decomposeMatrix")

        neckmultMatrix_fs = om2.MFnDependencyNode(neckctrl_multMatrix)
        neckdecomposeMatrix_fs = om2.MFnDependencyNode(neckctrl_decomposeMatrix)
        neckjnt_fs = om2.MFnDependencyNode(jnt_neck_obj)

        neckmultMatrixSum_plug = neckmultMatrix_fs.findPlug("matrixSum", False)
        neckdecomposeInpMatrix_plug = neckdecomposeMatrix_fs.findPlug("inputMatrix", False)
        neckdecomposeOtpTrans_plug = neckdecomposeMatrix_fs.findPlug("outputTranslate", False)
        neckdecomposeOtpRot_plug = neckdecomposeMatrix_fs.findPlug("outputRotate", False)
        neckjntTrans_plug = neckjnt_fs.findPlug("translate", False)
        neckjntRot_plug = neckjnt_fs.findPlug("rotate", False)

        self.ctrl_mod_n.commandToExecute('connectAttr -force Biped_Neck_ctrl.worldMatrix[0] Neck_multMatrix.matrixIn[0]')
        self.ctrl_mod_n.commandToExecute('connectAttr -force Neck.parentInverseMatrix[0] Neck_multMatrix.matrixIn[1]')
        self.ctrl_mod_n.connect(neckmultMatrixSum_plug, neckdecomposeInpMatrix_plug)
        self.ctrl_mod_n.connect(neckdecomposeOtpTrans_plug, neckjntTrans_plug)
        self.ctrl_mod_n.connect(neckdecomposeOtpRot_plug, neckjntRot_plug)

        if self.autostretch.currentIndex() == 1:
            if cmds.objExists("IkNeck*") and cmds.objExists("IkCvNeck") and cmds.objExists("IkCvHead"):
                ikneckspline_sl_lst = om2.MSelectionList()
                ikneckspline_sl_lst.add("IkCvNeck")
                ikneckspline_sl_lst.add("IkCvHead")
                obj_first = ikneckspline_sl_lst.getDependNode(0)

                ikcvneck_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
                ikcvneck_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                self.ctrl_mod_n.renameNode(ikcvneck_multMatrix, "IkCvNeck_multMatrix")
                self.ctrl_mod_n.renameNode(ikcvneck_decomposeMatrix, "IkCvNeck_decomposeMatrix")

                ikcvneckmultMatrix_fs = om2.MFnDependencyNode(ikcvneck_multMatrix)
                ikcvneckdecomposeMatrix_fs = om2.MFnDependencyNode(ikcvneck_decomposeMatrix)
                ikcvneckjnt_fs = om2.MFnDependencyNode(obj_first)

                ikcvneckmultMatrixSum_plug = ikcvneckmultMatrix_fs.findPlug("matrixSum", False)
                ikcvneckdecomposeInpMatrix_plug = ikcvneckdecomposeMatrix_fs.findPlug("inputMatrix", False)
                ikcvneckdecomposeOtpTrans_plug = ikcvneckdecomposeMatrix_fs.findPlug("outputTranslate", False)
                ikcvneckdecomposeOtpRot_plug = ikcvneckdecomposeMatrix_fs.findPlug("outputRotate", False)
                ikcvneckjntTrans_plug = ikcvneckjnt_fs.findPlug("translate", False)
                ikcvneckjntRot_plug = ikcvneckjnt_fs.findPlug("rotate", False)

                self.ctrl_mod_n.commandToExecute('connectAttr -force Neck.worldMatrix[0] IkCvNeck_multMatrix.matrixIn[0]')
                self.ctrl_mod_n.connect(ikcvneckmultMatrixSum_plug, ikcvneckdecomposeInpMatrix_plug)
                self.ctrl_mod_n.connect(ikcvneckdecomposeOtpTrans_plug, ikcvneckjntTrans_plug)
                self.ctrl_mod_n.connect(ikcvneckdecomposeOtpRot_plug, ikcvneckjntRot_plug)

                obj_lastspine = ikneckspline_sl_lst.getDependNode(1)

                ikcvhead_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
                ikcvhead_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                self.ctrl_mod_n.renameNode(ikcvhead_multMatrix, "IkCvHead_multMatrix")
                self.ctrl_mod_n.renameNode(ikcvhead_decomposeMatrix, "IkCvHead_decomposeMatrix")

                ikcvheadmultMatrix_fs = om2.MFnDependencyNode(ikcvhead_multMatrix)
                ikcvheaddecomposeMatrix_fs = om2.MFnDependencyNode(ikcvhead_decomposeMatrix)
                ikcvheadjnt_fs = om2.MFnDependencyNode(obj_lastspine)

                ikcvheadmultMatrixSum_plug = ikcvheadmultMatrix_fs.findPlug("matrixSum", False)
                ikcvheaddecomposeInpMatrix_plug = ikcvheaddecomposeMatrix_fs.findPlug("inputMatrix", False)
                ikcvheaddecomposeOtpTrans_plug = ikcvheaddecomposeMatrix_fs.findPlug("outputTranslate", False)
                ikcvheaddecomposeOtpRot_plug = ikcvheaddecomposeMatrix_fs.findPlug("outputRotate", False)
                ikcvheadjntTrans_plug = ikcvheadjnt_fs.findPlug("translate", False)
                ikcvheadjntRot_plug = ikcvheadjnt_fs.findPlug("rotate", False)

                self.ctrl_mod_n.commandToExecute('connectAttr -force Biped_StretchyNeck_ctrl.worldMatrix[0] IkCvHead_multMatrix.matrixIn[0]')
                self.ctrl_mod_n.connect(ikcvheadmultMatrixSum_plug, ikcvheaddecomposeInpMatrix_plug)
                self.ctrl_mod_n.connect(ikcvheaddecomposeOtpTrans_plug, ikcvheadjntTrans_plug)
                self.ctrl_mod_n.connect(ikcvheaddecomposeOtpRot_plug, ikcvheadjntRot_plug)

        elif cmds.objExists("IkCvNeck") and cmds.objExists("IkCvHead"):
            self.ctrl_mod_n.commandToExecute('delete "IkCvNeck"')
            self.ctrl_mod_n.commandToExecute('delete "IkCvHead"')
            self.ctrl_mod_n.commandToExecute('delete "IkNeck0"')
            self.ctrl_mod_n.commandToExecute('delete "Biped_StretchyNeck_ctrl"')

        elif cmds.objExists("Biped_StretchyNeck_ctrl"):
            self.ctrl_mod_n.commandToExecute('delete "Biped_StretchyNeck_ctrl"')

        headctrl_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
        headctrl_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
        self.ctrl_mod_n.renameNode(headctrl_multMatrix, "Head_multMatrix")
        self.ctrl_mod_n.renameNode(headctrl_decomposeMatrix, "Head_decomposeMatrix")

        headmultMatrix_fs = om2.MFnDependencyNode(headctrl_multMatrix)
        headdecomposeMatrix_fs = om2.MFnDependencyNode(headctrl_decomposeMatrix)
        headjnt_fs = om2.MFnDependencyNode(jnt_head_obj)

        headmultMatrixSum_plug = headmultMatrix_fs.findPlug("matrixSum", False)
        headdecomposeInpMatrix_plug = headdecomposeMatrix_fs.findPlug("inputMatrix", False)
        headdecomposeOtpTrans_plug = headdecomposeMatrix_fs.findPlug("outputTranslate", False)
        headdecomposeOtpRot_plug = headdecomposeMatrix_fs.findPlug("outputRotate", False)
        headjntTrans_plug = headjnt_fs.findPlug("translate", False)
        headjntRot_plug = headjnt_fs.findPlug("rotate", False)

        self.ctrl_mod_n.commandToExecute('connectAttr -force Biped_Head_ctrl.worldMatrix[0] Head_multMatrix.matrixIn[0]')
        self.ctrl_mod_n.commandToExecute('connectAttr -force Head.parentInverseMatrix[0] Head_multMatrix.matrixIn[1]')
        self.ctrl_mod_n.connect(headmultMatrixSum_plug, headdecomposeInpMatrix_plug)
        self.ctrl_mod_n.connect(headdecomposeOtpTrans_plug, headjntTrans_plug)
        self.ctrl_mod_n.connect(headdecomposeOtpRot_plug, headjntRot_plug)

        for index in range(fklarm_sl_ls.length()):
            jnt_obj = fklarm_sl_ls.getDependNode(index)
            jnt_string = fklarm_sl_ls.getSelectionStrings(index)

            if jnt_obj.hasFn(om2.MFn.kJoint):
                larmctrl_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
                larmctrl_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                self.ctrl_mod_n.renameNode(larmctrl_multMatrix, str(jnt_string)[2:][:-3]+"_multMatrix")
                self.ctrl_mod_n.renameNode(larmctrl_decomposeMatrix, str(jnt_string)[2:][:-3]+"_decomposeMatrix")

                larmmultMatrix_fs = om2.MFnDependencyNode(larmctrl_multMatrix)
                larmdecomposeMatrix_fs = om2.MFnDependencyNode(larmctrl_decomposeMatrix)

                larmjnt_fs = om2.MFnDependencyNode(jnt_obj)

                larmmultMatrixSum_plug = larmmultMatrix_fs.findPlug("matrixSum", False)
                larmdecomposeInpMatrix_plug = larmdecomposeMatrix_fs.findPlug("inputMatrix", False)
                larmdecomposeOtpTrans_plug = larmdecomposeMatrix_fs.findPlug("outputTranslate", False)
                larmdecomposeOtpRot_plug = larmdecomposeMatrix_fs.findPlug("outputRotate", False)
                larmjntTrans_plug = larmjnt_fs.findPlug("translate", False)
                larmjntRot_plug = larmjnt_fs.findPlug("rotate", False)

                self.ctrl_mod_n.commandToExecute('connectAttr -force Biped_{0}_ctrl.worldMatrix[0] {0}_multMatrix.matrixIn[0]'.format(str(jnt_string)[3:][:-3]))
                self.ctrl_mod_n.commandToExecute('connectAttr -force {0}.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(jnt_string)[3:][:-3]))
                self.ctrl_mod_n.connect(larmmultMatrixSum_plug, larmdecomposeInpMatrix_plug)
                self.ctrl_mod_n.connect(larmdecomposeOtpTrans_plug, larmjntTrans_plug)
                self.ctrl_mod_n.connect(larmdecomposeOtpRot_plug, larmjntRot_plug)

                if cmds.getAttr("{0}.jointOrientX".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientY".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientZ".format(str(jnt_string)[3:][:-3])) != 0:
                    self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientX" 0'.format(str(jnt_string)[3:][:-3]))
                    self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientY" 0'.format(str(jnt_string)[3:][:-3]))
                    self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientZ" 0'.format(str(jnt_string)[3:][:-3]))

        fklarm_sl_ls = om2.MSelectionList()
        fklarm_sl_ls.add("FkLeftArm")
        fklarm_sl_ls.add("FkLeftForeArm")
        fklarm_sl_ls.add("FkLeftHand")

        iklarm_sl_ls = om2.MSelectionList()
        iklarm_sl_ls.add("IkLeftArm")
        iklarm_sl_ls.add("IkLeftForeArm")
        iklarm_sl_ls.add("IkLeftHand")

        lhandoptions_sl_ls = om2.MSelectionList()
        lhandoptions_sl_ls.add("Biped_LeftHandOptions_ctrl")
        lhandoptions_obj = lhandoptions_sl_ls.getDependNode(0)

        self.ctrl_mod_n.commandToExecute('addAttr -longName "fkik" -niceName "Fk/Ik" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_LeftHandOptions_ctrl')
        self.ctrl_mod_n.doIt()

        lhandoptions_fs = om2.MFnDependencyNode(lhandoptions_obj)
        lhandoptionsfkik_plug = lhandoptions_fs.findPlug("fkik", False)

        for index in range(larm_sl_ls.length()):
            fkjnt_obj = fklarm_sl_ls.getDependNode(index)

            ikjnt_obj = iklarm_sl_ls.getDependNode(index)
            ikjnt_string = iklarm_sl_ls.getSelectionStrings(index)

            bindjnt_obj = larm_sl_ls.getDependNode(index)
            bindjnt_string = larm_sl_ls.getSelectionStrings(index)

            if bindjnt_obj.hasFn(om2.MFn.kJoint):
                if cmds.getAttr("{0}.jointOrientX".format(str(bindjnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientY".format(str(bindjnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientZ".format(str(bindjnt_string)[3:][:-3])) != 0:
                    jointort_xattr = cmds.getAttr("{0}.jointOrientX".format(str(bindjnt_string)[3:][:-3]))
                    jointort_yattr = cmds.getAttr("{0}.jointOrientY".format(str(bindjnt_string)[3:][:-3]))
                    jointort_zattr = cmds.getAttr("{0}.jointOrientZ".format(str(bindjnt_string)[3:][:-3]))

                    cmds.setAttr("{0}.rotateX".format(str(bindjnt_string)[3:][:-3]), jointort_xattr)
                    cmds.setAttr("{0}.rotateY".format(str(bindjnt_string)[3:][:-3]), jointort_yattr)
                    cmds.setAttr("{0}.rotateZ".format(str(bindjnt_string)[3:][:-3]), jointort_zattr)

                    cmds.setAttr("{0}.jointOrientX".format(str(bindjnt_string)[3:][:-3]), 0)
                    cmds.setAttr("{0}.jointOrientY".format(str(bindjnt_string)[3:][:-3]), 0)
                    cmds.setAttr("{0}.jointOrientZ".format(str(bindjnt_string)[3:][:-3]), 0)

                armjoint_fs = om2.MFnDependencyNode(bindjnt_obj)
                fkarmjoint_fs = om2.MFnDependencyNode(fkjnt_obj)

                armjointrotinp_plug = armjoint_fs.findPlug("rotate", False)
                fkarmjointrototp_plug = fkarmjoint_fs.findPlug("rotate", False)

                if cmds.objExists("LeftHand_Ik"):
                    armblendnode = self.ctrl_mod_n.createNode("blendColors")
                    armjoint_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                    self.ctrl_mod_n.renameNode(armjoint_decomposeMatrix, str(bindjnt_string)[2:][:-3]+"Blend_decomposeMatrix")
                    self.ctrl_mod_n.renameNode(armblendnode, str(bindjnt_string)[2:][:-3]+"_blend")

                    armblendnode_fs = om2.MFnDependencyNode(armblendnode)
                    armdecomposeMatrix_fs = om2.MFnDependencyNode(armjoint_decomposeMatrix)
                    ikarmjoint_fs = om2.MFnDependencyNode(ikjnt_obj)

                    armdecomposeInpMatrix_plug = armdecomposeMatrix_fs.findPlug("inputMatrix", False)
                    armdecomposeOtpRot_plug = armdecomposeMatrix_fs.findPlug("outputRotate", False)
                    armblendnodeinp1_plug = armblendnode_fs.findPlug("color1", False)
                    armblendnodeinp2_plug = armblendnode_fs.findPlug("color2", False)
                    armblendnodeotp_plug = armblendnode_fs.findPlug("output", False)
                    armblendnodeblender_plug = armblendnode_fs.findPlug("blender", False)
                    ikarmjointrototp_plug = ikarmjoint_fs.findPlug("matrix", False)

                    self.ctrl_mod_n.connect(ikarmjointrototp_plug, armdecomposeInpMatrix_plug)
                    self.ctrl_mod_n.connect(armdecomposeOtpRot_plug, armblendnodeinp1_plug)
                    self.ctrl_mod_n.connect(fkarmjointrototp_plug, armblendnodeinp2_plug)
                    self.ctrl_mod_n.connect(armblendnodeotp_plug, armjointrotinp_plug)
                    self.ctrl_mod_n.connect(lhandoptionsfkik_plug, armblendnodeblender_plug)

            else:
                    self.ctrl_mod_n.connect(fkarmjointrototp_plug, armjointrotinp_plug)
                    self.ctrl_mod_n.commandToExecute('setAttr -keyable false -channelBox false Biped_LeftHandOptions_ctrl.fkik')
                    self.ctrl_mod_n.commandToExecute('setAttr "IkLeftArm.visibility" 0')

        if cmds.objExists("LeftHand_Ik"):
            lhandik_sl_ls = om2.MSelectionList()
            lhandik_sl_ls.add("LeftHand_Ik")
            likhandle_fs = om2.MFnDependencyNode(lhandik_sl_ls.getDependNode(0))
            likhand_fs = om2.MFnDependencyNode(iklarm_sl_ls.getDependNode(2))

            if self.typeofLHandIK.currentIndex() == 1 or 2:
                likhandctrl_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
                likhandctrl_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                likhandrot_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
                likhandrot_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                self.ctrl_mod_n.renameNode(likhandctrl_multMatrix, "IkLeftHand_multMatrix")
                self.ctrl_mod_n.renameNode(likhandctrl_decomposeMatrix, "IkLeftHand_decomposeMatrix")
                self.ctrl_mod_n.renameNode(likhandrot_multMatrix, "IkLeftHandRot_multMatrix")
                self.ctrl_mod_n.renameNode(likhandrot_decomposeMatrix, "IkLeftHandRot_decomposeMatrix")

                likhandmultMatrix_fs = om2.MFnDependencyNode(likhandctrl_multMatrix)
                likhanddecomposeMatrix_fs = om2.MFnDependencyNode(likhandctrl_decomposeMatrix)
                likhandrotmultMatrix_fs = om2.MFnDependencyNode(likhandrot_multMatrix)
                likhandrotdecomposeMatrix_fs = om2.MFnDependencyNode(likhandrot_decomposeMatrix)

                likhandmultMatrixSum_plug = likhandmultMatrix_fs.findPlug("matrixSum", False)
                likhanddecomposeInpMatrix_plug = likhanddecomposeMatrix_fs.findPlug("inputMatrix", False)
                likhanddecomposeOtpTrans_plug = likhanddecomposeMatrix_fs.findPlug("outputTranslate", False)
                likhanddecomposeOtpRot_plug = likhanddecomposeMatrix_fs.findPlug("outputRotate", False)
                likhandrotmultMatrixSum_plug = likhandrotmultMatrix_fs.findPlug("matrixSum", False)
                likhandrotdecomposeInpMatrix_plug = likhandrotdecomposeMatrix_fs.findPlug("inputMatrix", False)
                likhandrotdecomposeOtpRot_plug = likhandrotdecomposeMatrix_fs.findPlug("outputRotate", False)
                likhandlejntTrans_plug = likhandle_fs.findPlug("translate", False)
                likhandlejntRot_plug = likhandle_fs.findPlug("rotate", False)
                likhandRot_plug = likhand_fs.findPlug("rotate", False)

                self.ctrl_mod_n.commandToExecute('connectAttr -force Biped_IkLeftHand_ctrl.worldMatrix[0] IkLeftHand_multMatrix.matrixIn[0]')
                self.ctrl_mod_n.commandToExecute('connectAttr -force LeftHand_Ik.parentInverseMatrix[0] IkLeftHand_multMatrix.matrixIn[1]')
                self.ctrl_mod_n.commandToExecute('connectAttr -force Biped_IkLeftHand_ctrl.worldMatrix[0] IkLeftHandRot_multMatrix.matrixIn[0]')
                self.ctrl_mod_n.commandToExecute('connectAttr -force IkLeftHand.parentInverseMatrix[0] IkLeftHandRot_multMatrix.matrixIn[1]')
                self.ctrl_mod_n.connect(likhandmultMatrixSum_plug, likhanddecomposeInpMatrix_plug)
                self.ctrl_mod_n.connect(likhanddecomposeOtpTrans_plug, likhandlejntTrans_plug)
                self.ctrl_mod_n.connect(likhanddecomposeOtpRot_plug, likhandlejntRot_plug)
                self.ctrl_mod_n.connect(likhandrotmultMatrixSum_plug, likhandrotdecomposeInpMatrix_plug)
                self.ctrl_mod_n.connect(likhandrotdecomposeOtpRot_plug, likhandRot_plug)

        else:
            self.ctrl_mod_n.commandToExecute('delete "Biped_IkLeftHand_null"')
            self.ctrl_mod_n.commandToExecute('setAttr -keyable false -channelBox false Biped_LeftHandOptions_ctrl.fkik')
            self.ctrl_mod_n.commandToExecute('setAttr "IkLeftArm.visibility" 0')

        lfinger_sl_ls = om2.MSelectionList()
        lfinger_sl_ls.add("LeftFinger*")
        for index in range(lfinger_sl_ls.length()):
            jnt_obj = lfinger_sl_ls.getDependNode(index)
            jnt_string = lfinger_sl_ls.getSelectionStrings(index)

            if jnt_obj.hasFn(om2.MFn.kJoint):
                lfingerctrl_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
                lfingerctrl_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                self.ctrl_mod_n.renameNode(lfingerctrl_multMatrix, str(jnt_string)[2:][:-3]+"_multMatrix")
                self.ctrl_mod_n.renameNode(lfingerctrl_decomposeMatrix, str(jnt_string)[2:][:-3]+"_decomposeMatrix")

                lfingermultMatrix_fs = om2.MFnDependencyNode(lfingerctrl_multMatrix)
                lfingerdecomposeMatrix_fs = om2.MFnDependencyNode(lfingerctrl_decomposeMatrix)
                lfingerjnt_fs = om2.MFnDependencyNode(jnt_obj)

                lfingermultMatrixSum_plug = lfingermultMatrix_fs.findPlug("matrixSum", False)
                lfingerdecomposeInpMatrix_plug = lfingerdecomposeMatrix_fs.findPlug("inputMatrix", False)
                lfingerdecomposeOtpTrans_plug = lfingerdecomposeMatrix_fs.findPlug("outputTranslate", False)
                lfingerdecomposeOtpRot_plug = lfingerdecomposeMatrix_fs.findPlug("outputRotate", False)
                lfingerjntTrans_plug = lfingerjnt_fs.findPlug("translate", False)
                lfingerjntRot_plug = lfingerjnt_fs.findPlug("rotate", False)

                self.ctrl_mod_n.commandToExecute('connectAttr -force Biped_{0}_ctrl.worldMatrix[0] {0}_multMatrix.matrixIn[0]'.format(str(jnt_string)[3:][:-3]))
                self.ctrl_mod_n.commandToExecute('connectAttr -force {0}.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(jnt_string)[3:][:-3]))
                self.ctrl_mod_n.connect(lfingermultMatrixSum_plug, lfingerdecomposeInpMatrix_plug)
                self.ctrl_mod_n.connect(lfingerdecomposeOtpTrans_plug, lfingerjntTrans_plug)
                self.ctrl_mod_n.connect(lfingerdecomposeOtpRot_plug, lfingerjntRot_plug)
                if cmds.getAttr("{0}.jointOrientX".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientY".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientZ".format(str(jnt_string)[3:][:-3])) != 0:
                    self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientX" 0'.format(str(jnt_string)[3:][:-3]))
                    self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientY" 0'.format(str(jnt_string)[3:][:-3]))
                    self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientZ" 0'.format(str(jnt_string)[3:][:-3]))

                if cmds.objExists("Biped_{0}4_ctrl".format(str(jnt_string)[3:][:-4])):
                    self.ctrl_mod_n.commandToExecute('setAttr "Biped_{0}4_ctrl.visibility" 0'.format(str(jnt_string)[3:][:-4]))

        lfingergrp_sl_ls = om2.MSelectionList()
        lfingergrp_sl_ls.add("Biped_LeftFingers_null")
        grp_obj = lfingergrp_sl_ls.getDependNode(0)

        lfingergrp_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
        lfingergrp_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
        self.ctrl_mod_n.renameNode(lfingergrp_multMatrix, "LeftFingers_multMatrix")
        self.ctrl_mod_n.renameNode(lfingergrp_decomposeMatrix, "LeftFingers_decomposeMatrix")

        lfingergrpmultMatrix_fs = om2.MFnDependencyNode(lfingergrp_multMatrix)
        lfingergrpdecomposeMatrix_fs = om2.MFnDependencyNode(lfingergrp_decomposeMatrix)
        lfingergrp_fs = om2.MFnDependencyNode(grp_obj)

        lfingergrpmultMatrixSum_plug = lfingergrpmultMatrix_fs.findPlug("matrixSum", False)
        lfingergrpdecomposeInpMatrix_plug = lfingergrpdecomposeMatrix_fs.findPlug("inputMatrix", False)
        lfingergrpdecomposeOtpTrans_plug = lfingergrpdecomposeMatrix_fs.findPlug("outputTranslate", False)
        lfingergrpdecomposeOtpRot_plug = lfingergrpdecomposeMatrix_fs.findPlug("outputRotate", False)
        lfingergrpjntTrans_plug = lfingergrp_fs.findPlug("translate", False)
        lfingergrpjntRot_plug = lfingergrp_fs.findPlug("rotate", False)

        self.ctrl_mod_n.commandToExecute('connectAttr -force LeftHand.worldMatrix[0] LeftFingers_multMatrix.matrixIn[0]')
        self.ctrl_mod_n.commandToExecute('connectAttr -force Biped_LeftFingers_null.parentInverseMatrix[0] LeftFingers_multMatrix.matrixIn[1]')
        self.ctrl_mod_n.connect(lfingergrpmultMatrixSum_plug, lfingergrpdecomposeInpMatrix_plug)
        self.ctrl_mod_n.connect(lfingergrpdecomposeOtpTrans_plug, lfingergrpjntTrans_plug)
        self.ctrl_mod_n.connect(lfingergrpdecomposeOtpRot_plug, lfingergrpjntRot_plug)

        iklleg_sl_ls = om2.MSelectionList()
        iklleg_sl_ls.add("IkLeftUpLeg")
        iklleg_sl_ls.add("IkLeftLeg")
        iklleg_sl_ls.add("IkLeftFoot")
        iklleg_sl_ls.add("IkLeftToeBase")

        noflipiklleg_sl_ls = om2.MSelectionList()
        noflipiklleg_sl_ls.add("IkNoFlipLeftUpLeg")
        noflipiklleg_sl_ls.add("IkNoFlipLeftLeg")
        noflipiklleg_sl_ls.add("IkNoFlipLeftFoot")

        pviklleg_sl_ls = om2.MSelectionList()
        pviklleg_sl_ls.add("IkPVLeftUpLeg")
        pviklleg_sl_ls.add("IkPVLeftLeg")
        pviklleg_sl_ls.add("IkPVLeftFoot")

        llegoptions_sl_ls = om2.MSelectionList()
        llegoptions_sl_ls.add("Biped_LeftFootOptions_ctrl")
        llegoptions_obj = llegoptions_sl_ls.getDependNode(0)

        self.ctrl_mod_n.commandToExecute('addAttr -longName "stretchy" -niceName "Stretchy" -attributeType double -keyable true -defaultValue 0 Biped_FkLeftUpLeg_ctrl')
        self.ctrl_mod_n.commandToExecute('addAttr -longName "stretchy" -niceName "Stretchy" -attributeType double -keyable true -defaultValue 0 Biped_FkLeftLeg_ctrl')
        self.ctrl_mod_n.commandToExecute('addAttr -longName "fkik" -niceName "Fk/Ik" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_LeftFootOptions_ctrl')
        self.ctrl_mod_n.commandToExecute('addAttr -longName "kneeswitch" -niceName "Auto/Manual Knee" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_LeftFootOptions_ctrl')
        self.ctrl_mod_n.doIt()

        llegoptions_fs = om2.MFnDependencyNode(llegoptions_obj)
        llegoptionsfkik_plug = llegoptions_fs.findPlug("fkik", False)
        llegoptionskneeswitch_plug = llegoptions_fs.findPlug("kneeswitch", False)

        for index in range(fklleg_sl_ls.length()):
            jnt_obj = fklleg_sl_ls.getDependNode(index)
            jnt_string = fklleg_sl_ls.getSelectionStrings(index)

            ikjnt_obj = iklleg_sl_ls.getDependNode(index)
            ikjnt_string = fklleg_sl_ls.getSelectionStrings(index)

            bindjnt_obj = lleg_sl_ls.getDependNode(index)
            bindjnt_string = lleg_sl_ls.getSelectionStrings(index)

            if jnt_obj.hasFn(om2.MFn.kJoint):
                llegctrl_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
                llegctrl_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                self.ctrl_mod_n.renameNode(llegctrl_multMatrix, str(jnt_string)[2:][:-3]+"_multMatrix")
                self.ctrl_mod_n.renameNode(llegctrl_decomposeMatrix, str(jnt_string)[2:][:-3]+"_decomposeMatrix")

                llegmultMatrix_fs = om2.MFnDependencyNode(llegctrl_multMatrix)
                llegdecomposeMatrix_fs = om2.MFnDependencyNode(llegctrl_decomposeMatrix)
                llegjnt_fs = om2.MFnDependencyNode(jnt_obj)

                llegmultMatrixSum_plug = llegmultMatrix_fs.findPlug("matrixSum", False)
                llegdecomposeInpMatrix_plug = llegdecomposeMatrix_fs.findPlug("inputMatrix", False)
                llegdecomposeOtpTrans_plug = llegdecomposeMatrix_fs.findPlug("outputTranslate", False)
                llegdecomposeOtpRot_plug = llegdecomposeMatrix_fs.findPlug("outputRotate", False)
                llegjntTrans_plug = llegjnt_fs.findPlug("translate", False)
                llegjntRot_plug = llegjnt_fs.findPlug("rotate", False)

                self.ctrl_mod_n.commandToExecute('connectAttr -force Biped_{0}_ctrl.worldMatrix[0] {0}_multMatrix.matrixIn[0]'.format(str(jnt_string)[3:][:-3]))
                self.ctrl_mod_n.commandToExecute('connectAttr -force {0}.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(jnt_string)[3:][:-3]))
                self.ctrl_mod_n.connect(llegmultMatrixSum_plug, llegdecomposeInpMatrix_plug)
                self.ctrl_mod_n.connect(llegdecomposeOtpTrans_plug, llegjntTrans_plug)
                self.ctrl_mod_n.connect(llegdecomposeOtpRot_plug, llegjntRot_plug)

                if cmds.getAttr("{0}.jointOrientX".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientY".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientZ".format(str(jnt_string)[3:][:-3])) != 0:
                    self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientX" 0'.format(str(jnt_string)[3:][:-3]))
                    self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientY" 0'.format(str(jnt_string)[3:][:-3]))
                    self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientZ" 0'.format(str(jnt_string)[3:][:-3]))

            if bindjnt_obj.hasFn(om2.MFn.kJoint):
                if cmds.getAttr("{0}.jointOrientX".format(str(bindjnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientY".format(str(bindjnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientZ".format(str(bindjnt_string)[3:][:-3])) != 0:
                    jointort_xattr = cmds.getAttr("{0}.jointOrientX".format(str(bindjnt_string)[3:][:-3]))
                    jointort_yattr = cmds.getAttr("{0}.jointOrientY".format(str(bindjnt_string)[3:][:-3]))
                    jointort_zattr = cmds.getAttr("{0}.jointOrientZ".format(str(bindjnt_string)[3:][:-3]))

                    cmds.setAttr("{0}.rotateX".format(str(bindjnt_string)[3:][:-3]), jointort_xattr)
                    cmds.setAttr("{0}.rotateY".format(str(bindjnt_string)[3:][:-3]), jointort_yattr)
                    cmds.setAttr("{0}.rotateZ".format(str(bindjnt_string)[3:][:-3]), jointort_zattr)

                    cmds.setAttr("{0}.jointOrientX".format(str(bindjnt_string)[3:][:-3]), 0)
                    cmds.setAttr("{0}.jointOrientY".format(str(bindjnt_string)[3:][:-3]), 0)
                    cmds.setAttr("{0}.jointOrientZ".format(str(bindjnt_string)[3:][:-3]), 0)

                legjoint_fs = om2.MFnDependencyNode(bindjnt_obj)
                fklegjoint_fs = om2.MFnDependencyNode(jnt_obj)

                legjointtransinp_plug = legjoint_fs.findPlug("translate", False)
                legjointrotinp_plug = legjoint_fs.findPlug("rotate", False)
                fklegjointtransotp_plug = fklegjoint_fs.findPlug("translate", False)
                fklegjointrototp_plug = fklegjoint_fs.findPlug("rotate", False)

                if cmds.objExists("NoFlipLeftLeg_Ik") and cmds.objExists("PVLeftLeg_Ik"):
                    legrotblendnode = self.ctrl_mod_n.createNode("blendColors")
                    legtransblendnode = self.ctrl_mod_n.createNode("blendColors")
                    legjoint_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                    self.ctrl_mod_n.renameNode(legjoint_decomposeMatrix, str(bindjnt_string)[2:][:-3]+"Blend_decomposeMatrix")
                    self.ctrl_mod_n.renameNode(legrotblendnode, str(bindjnt_string)[2:][:-3]+"Rot_blend")
                    self.ctrl_mod_n.renameNode(legtransblendnode, str(bindjnt_string)[2:][:-3]+"Trans_blend")

                    legrotblendnode_fs = om2.MFnDependencyNode(legrotblendnode)
                    legtransblendnode_fs = om2.MFnDependencyNode(legtransblendnode)
                    legdecomposeMatrix_fs = om2.MFnDependencyNode(legjoint_decomposeMatrix)
                    iklegjoint_fs = om2.MFnDependencyNode(ikjnt_obj)

                    legdecomposeInpMatrix_plug = legdecomposeMatrix_fs.findPlug("inputMatrix", False)
                    legdecomposeOtpRot_plug = legdecomposeMatrix_fs.findPlug("outputRotate", False)
                    legdecomposeOtpTrans_plug = legdecomposeMatrix_fs.findPlug("outputTranslate", False)
                    legrotblendnodeinp1_plug = legrotblendnode_fs.findPlug("color1", False)
                    legrotblendnodeinp2_plug = legrotblendnode_fs.findPlug("color2", False)
                    legrotblendnodeotp_plug = legrotblendnode_fs.findPlug("output", False)
                    legrotblendnodeblender_plug = legrotblendnode_fs.findPlug("blender", False)
                    legtransblendnodeinp1_plug = legtransblendnode_fs.findPlug("color1", False)
                    legtransblendnodeinp2_plug = legtransblendnode_fs.findPlug("color2", False)
                    legtransblendnodeotp_plug = legtransblendnode_fs.findPlug("output", False)
                    legtransblendnodeblender_plug = legtransblendnode_fs.findPlug("blender", False)
                    iklegjointotp_plug = iklegjoint_fs.findPlug("matrix", False)

                    self.ctrl_mod_n.connect(iklegjointotp_plug, legdecomposeInpMatrix_plug)
                    self.ctrl_mod_n.connect(legdecomposeOtpRot_plug, legrotblendnodeinp1_plug)
                    self.ctrl_mod_n.connect(legdecomposeOtpTrans_plug, legtransblendnodeinp1_plug)
                    self.ctrl_mod_n.connect(fklegjointrototp_plug, legrotblendnodeinp2_plug)
                    self.ctrl_mod_n.connect(fklegjointtransotp_plug, legtransblendnodeinp2_plug)
                    self.ctrl_mod_n.connect(legrotblendnodeotp_plug, legjointrotinp_plug)
                    self.ctrl_mod_n.connect(legtransblendnodeotp_plug, legjointtransinp_plug)
                    self.ctrl_mod_n.connect(llegoptionsfkik_plug, legrotblendnodeblender_plug)
                    self.ctrl_mod_n.connect(llegoptionsfkik_plug, legtransblendnodeblender_plug)

                    if index < 3:
                        noflipjnt_obj = noflipiklleg_sl_ls.getDependNode(index)
                        noflipjnt_string = noflipiklleg_sl_ls.getSelectionStrings(index)

                        pvjnt_obj = pviklleg_sl_ls.getDependNode(index)
                        pvjnt_string = pviklleg_sl_ls.getSelectionStrings(index)

                        legrotblendnode = self.ctrl_mod_n.createNode("blendColors")
                        legtransblendnode = self.ctrl_mod_n.createNode("blendColors")
                        nofliplegjoint_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                        pvlegjoint_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                        self.ctrl_mod_n.renameNode(nofliplegjoint_decomposeMatrix, str(noflipjnt_string)[2:][:-3]+"Blend_decomposeMatrix")
                        self.ctrl_mod_n.renameNode(pvlegjoint_decomposeMatrix, str(pvjnt_string)[2:][:-3]+"Blend_decomposeMatrix")
                        self.ctrl_mod_n.renameNode(legrotblendnode, str(bindjnt_string)[2:][:-3]+"Rot_kneeblend")
                        self.ctrl_mod_n.renameNode(legtransblendnode, str(bindjnt_string)[2:][:-3]+"Trans_kneeblend")

                        legrotblendnode_fs = om2.MFnDependencyNode(legrotblendnode)
                        legtransblendnode_fs = om2.MFnDependencyNode(legtransblendnode)
                        nofliplegdecomposeMatrix_fs = om2.MFnDependencyNode(nofliplegjoint_decomposeMatrix)
                        pvlegdecomposeMatrix_fs = om2.MFnDependencyNode(pvlegjoint_decomposeMatrix)
                        noflipiklegjoint_fs = om2.MFnDependencyNode(noflipjnt_obj)
                        pviklegjoint_fs = om2.MFnDependencyNode(pvjnt_obj)

                        nofliplegdecomposeInpMatrix_plug = nofliplegdecomposeMatrix_fs.findPlug("inputMatrix", False)
                        nofliplegdecomposeOtpRot_plug = nofliplegdecomposeMatrix_fs.findPlug("outputRotate", False)
                        nofliplegdecomposeOtpTrans_plug = nofliplegdecomposeMatrix_fs.findPlug("outputTranslate", False)
                        pvlegdecomposeInpMatrix_plug = pvlegdecomposeMatrix_fs.findPlug("inputMatrix", False)
                        pvlegdecomposeOtpRot_plug = pvlegdecomposeMatrix_fs.findPlug("outputRotate", False)
                        pvlegdecomposeOtpTrans_plug = pvlegdecomposeMatrix_fs.findPlug("outputTranslate", False)
                        legrotblendnodeinp1_plug = legrotblendnode_fs.findPlug("color1", False)
                        legrotblendnodeinp2_plug = legrotblendnode_fs.findPlug("color2", False)
                        legrotblendnodeotp_plug = legrotblendnode_fs.findPlug("output", False)
                        legrotblendnodeblender_plug = legrotblendnode_fs.findPlug("blender", False)
                        legtransblendnodeinp1_plug = legtransblendnode_fs.findPlug("color1", False)
                        legtransblendnodeinp2_plug = legtransblendnode_fs.findPlug("color2", False)
                        legtransblendnodeotp_plug = legtransblendnode_fs.findPlug("output", False)
                        legtransblendnodeblender_plug = legtransblendnode_fs.findPlug("blender", False)
                        noflipiklegjointotp_plug = noflipiklegjoint_fs.findPlug("matrix", False)
                        pviklegjointotp_plug = pviklegjoint_fs.findPlug("matrix", False)
                        iklegjointinpTrans_plug = iklegjoint_fs.findPlug("translate", False)
                        iklegjointinpRot_plug = iklegjoint_fs.findPlug("jointOrient", False)

                        self.ctrl_mod_n.connect(noflipiklegjointotp_plug, nofliplegdecomposeInpMatrix_plug)
                        self.ctrl_mod_n.connect(pviklegjointotp_plug, pvlegdecomposeInpMatrix_plug)
                        self.ctrl_mod_n.connect(pvlegdecomposeOtpRot_plug, legrotblendnodeinp1_plug)
                        self.ctrl_mod_n.connect(pvlegdecomposeOtpTrans_plug, legtransblendnodeinp1_plug)
                        self.ctrl_mod_n.connect(nofliplegdecomposeOtpRot_plug, legrotblendnodeinp2_plug)
                        self.ctrl_mod_n.connect(nofliplegdecomposeOtpTrans_plug, legtransblendnodeinp2_plug)
                        self.ctrl_mod_n.connect(legrotblendnodeotp_plug, iklegjointinpRot_plug)
                        self.ctrl_mod_n.connect(legtransblendnodeotp_plug, iklegjointinpTrans_plug)
                        self.ctrl_mod_n.connect(llegoptionskneeswitch_plug, legrotblendnodeblender_plug)
                        self.ctrl_mod_n.connect(llegoptionskneeswitch_plug, legtransblendnodeblender_plug)

                else:
                    self.ctrl_mod_n.connect(fklegjointtransotp_plug, legjointtransinp_plug)
                    self.ctrl_mod_n.connect(fklegjointrototp_plug, legjointrotinp_plug)

            if index < 2:
                iklleggrp_sl_lst = om2.MSelectionList()
                iklleggrp_sl_lst.add("LeftUpperLegIkCluster_grp")
                iklleggrp_sl_lst.add("LeftUpperLegIkCluster2_grp")
                iklleggrp_sl_lst.add("LeftLowerLegIkCluster_grp")
                iklleggrp_sl_lst.add("LeftLowerLegIkCluster2_grp")
                grp_legupperikcluster = iklleggrp_sl_lst.getDependNode(0)
                grp_legupperikcluster2 = iklleggrp_sl_lst.getDependNode(1)
                grp_leglowerikcluster = iklleggrp_sl_lst.getDependNode(2)
                grp_leglowerikcluster2 = iklleggrp_sl_lst.getDependNode(3)

                llegjoint_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
                legjoint_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")

                llegmultMatrix_fs = om2.MFnDependencyNode(llegjoint_multMatrix)
                llegdecomposeMatrix_fs = om2.MFnDependencyNode(legjoint_decomposeMatrix)
                iklupperleggrp_fs = om2.MFnDependencyNode(grp_legupperikcluster)
                ikllowerleggrp_fs = om2.MFnDependencyNode(grp_leglowerikcluster)

                llegmultMatrixSum_plug = llegmultMatrix_fs.findPlug("matrixSum", False)
                llegdecomposeInpMatrix_plug = llegdecomposeMatrix_fs.findPlug("inputMatrix", False)
                llegdecomposeOtpTrans_plug = llegdecomposeMatrix_fs.findPlug("outputTranslate", False)
                llegdecomposeOtpRot_plug = llegdecomposeMatrix_fs.findPlug("outputRotate", False)
                iklupperleggrpTrans_plug = iklupperleggrp_fs.findPlug("translate", False)
                iklupperleggrpRot_plug = iklupperleggrp_fs.findPlug("rotate", False)
                ikllowerleggrpTrans_plug = ikllowerleggrp_fs.findPlug("translate", False)
                ikllowerleggrpRot_plug = ikllowerleggrp_fs.findPlug("rotate", False)

                self.ctrl_mod_n.renameNode(llegjoint_multMatrix, str(bindjnt_string)[2:][:-3]+"_multMatrix")
                self.ctrl_mod_n.renameNode(legjoint_decomposeMatrix, str(bindjnt_string)[2:][:-3]+"_decomposeMatrix")
                self.ctrl_mod_n.commandToExecute('connectAttr -force {0}.worldMatrix[0] {0}_multMatrix.matrixIn[0]'.format(str(bindjnt_string)[3:][:-3]))
                self.ctrl_mod_n.connect(llegmultMatrixSum_plug, llegdecomposeInpMatrix_plug)

                fkllegstretch_expression = om1.MFnExpression()

                if index == 0:
                    fkllegstretch_expression.create("Biped_FkLeftLeg_ctrl.translateY = Biped_FkLeftUpLeg_ctrl.stretchy")
                    fkllegstretch_expression.create("Biped_FkLeftLeg_ctrl.translateZ = Biped_FkLeftLeg_ctrl.translateY/10")

                    self.ctrl_mod_n.commandToExecute('connectAttr -force LeftUpperLegIkCluster_grp.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(bindjnt_string)[3:][:-3]))
                    self.ctrl_mod_n.connect(llegdecomposeOtpTrans_plug, iklupperleggrpTrans_plug)
                    self.ctrl_mod_n.connect(llegdecomposeOtpRot_plug, iklupperleggrpRot_plug)

                    lupperlegcluster2_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
                    lupperlegcluster2_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")

                    lupperlegcluster2multMatrix_fs = om2.MFnDependencyNode(lupperlegcluster2_multMatrix)
                    lupperlegcluster2decomposeMatrix_fs = om2.MFnDependencyNode(lupperlegcluster2_decomposeMatrix)
                    lupperlegcluster2_fs = om2.MFnDependencyNode(grp_legupperikcluster2)

                    lupperlegcluster2multMatrixSum_plug = lupperlegcluster2multMatrix_fs.findPlug("matrixSum", False)
                    lupperlegcluster2decomposeInpMatrix_plug = lupperlegcluster2decomposeMatrix_fs.findPlug("inputMatrix", False)
                    lupperlegcluster2decomposeOtpTrans_plug = lupperlegcluster2decomposeMatrix_fs.findPlug("outputTranslate", False)
                    lupperlegcluster2Trans_plug = lupperlegcluster2_fs.findPlug("translate", False)

                    self.ctrl_mod_n.renameNode(lupperlegcluster2_multMatrix, "LeftUpperLegCluster2_multMatrix")
                    self.ctrl_mod_n.renameNode(lupperlegcluster2_decomposeMatrix,"LeftUpperLegCluster2_decomposeMatrix")
                    self.ctrl_mod_n.connect(lupperlegcluster2multMatrixSum_plug, lupperlegcluster2decomposeInpMatrix_plug)
                    self.ctrl_mod_n.commandToExecute('connectAttr -force LeftLeg.worldMatrix[0] LeftUpperLegCluster2_multMatrix.matrixIn[0]')
                    self.ctrl_mod_n.commandToExecute('connectAttr -force LeftUpperLegIkCluster2_grp.parentInverseMatrix[0] LeftUpperLegCluster2_multMatrix.matrixIn[1]')
                    self.ctrl_mod_n.connect(lupperlegcluster2decomposeOtpTrans_plug, lupperlegcluster2Trans_plug)

                elif index == 1:
                    fkllegstretch_expression.create("Biped_FkLeftFoot_ctrl.translateY = Biped_FkLeftLeg_ctrl.stretchy")
                    fkllegstretch_expression.create("Biped_FkLeftFoot_ctrl.translateZ = Biped_FkLeftFoot_ctrl.translateY*(-1.5)")

                    self.ctrl_mod_n.commandToExecute('connectAttr -force LeftLowerLegIkCluster_grp.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(bindjnt_string)[3:][:-3]))
                    self.ctrl_mod_n.connect(llegdecomposeOtpTrans_plug, ikllowerleggrpTrans_plug)
                    self.ctrl_mod_n.connect(llegdecomposeOtpRot_plug, ikllowerleggrpRot_plug)

                    llowerlegcluster2_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
                    llowerlegcluster2_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")

                    llowerlegcluster2multMatrix_fs = om2.MFnDependencyNode(llowerlegcluster2_multMatrix)
                    llowerlegcluster2decomposeMatrix_fs = om2.MFnDependencyNode(llowerlegcluster2_decomposeMatrix)
                    llowerlegcluster2_fs = om2.MFnDependencyNode(grp_leglowerikcluster2)

                    llowerlegcluster2multMatrixSum_plug = llowerlegcluster2multMatrix_fs.findPlug("matrixSum", False)
                    llowerlegcluster2decomposeInpMatrix_plug = llowerlegcluster2decomposeMatrix_fs.findPlug("inputMatrix", False)
                    llowerlegcluster2decomposeOtpTrans_plug = llowerlegcluster2decomposeMatrix_fs.findPlug("outputTranslate", False)
                    llowerlegcluster2Trans_plug = llowerlegcluster2_fs.findPlug("translate", False)

                    self.ctrl_mod_n.renameNode(llowerlegcluster2_multMatrix, "LeftLowerLegCluster2_multMatrix")
                    self.ctrl_mod_n.renameNode(llowerlegcluster2_decomposeMatrix,"LeftLowerLegCluster2_decomposeMatrix")
                    self.ctrl_mod_n.commandToExecute('connectAttr -force LeftFoot.worldMatrix[0] LeftLowerLegCluster2_multMatrix.matrixIn[0]')
                    self.ctrl_mod_n.commandToExecute('connectAttr -force LeftLowerLegIkCluster2_grp.parentInverseMatrix[0] LeftLowerLegCluster2_multMatrix.matrixIn[1]')
                    self.ctrl_mod_n.connect(llowerlegcluster2multMatrixSum_plug, llowerlegcluster2decomposeInpMatrix_plug)
                    self.ctrl_mod_n.connect(llowerlegcluster2decomposeOtpTrans_plug, llowerlegcluster2Trans_plug)

        grp_legupperikcluster1 = om1.MObject()
        grp_legupperikcluster2 = om1.MObject()

        if self.autostretch.currentIndex() == 1:
            if cmds.objExists("IkSplineLeftUpperLeg0"):
                iklupperleg_sl_lst = om1.MSelectionList()
                iklupperleg_sl_lst.add("IkSplineLeftUpperLeg*")
                iklupperleg_sl_lst.getDependNode(0, obj_root)
                iklupperleg_sl_lst.getDependNode(iklupperleg_sl_lst.length()-1, obj_endspine)

                iklupperleggrp_sl_lst = om1.MSelectionList()
                iklupperleggrp_sl_lst.add("LeftUpperLegIkCluster1_grp")
                iklupperleggrp_sl_lst.add("LeftUpperLegIkCluster2_grp")
                iklupperleggrp_sl_lst.getDependNode(0, grp_legupperikcluster1)
                iklupperleggrp_sl_lst.getDependNode(1, grp_legupperikcluster2)

                lleg_pathnode = om1.MDagPath()
                rootspine_path = lleg_pathnode.getAPathTo(obj_root)

                try:
                    ikspineiksolver_lst.add("ikSplineSolver*")
                except:
                    cmds.createNode("ikSplineSolver")

                self.iklleg_effector = ik_effector.create(obj_endspine)
                iklleg_effector_path = lleg_pathnode.getAPathTo(self.iklleg_effector)

                self.lleg_ik = ik_handle.create(rootspine_path, iklleg_effector_path)

                obj_array = om1.MPointArray()
                obj_lst_mpoint = []
                obj = om1.MObject()
                for index in range(iklupperleg_sl_lst.length()):
                    iklupperleg_sl_lst.getDependNode(index, obj)
                    obj_path = ikspineobj_path_n.getAPathTo(obj)
                    obj_tn = om1.MFnTransform(obj_path)
                    obj_t = obj_tn.translation(om1.MSpace.kWorld)
                    obj_lst_mpoint.append(om1.MPoint(obj_t))
                    obj_array.append(obj_lst_mpoint[index])

                self.ikspline_cv_tn = ikspinedag_n.create("transform", "LeftUpperLeg_SplineCv")
                ikspline_cv = ikspline_cv_n.createWithEditPoints(obj_array, 1, 1, False, True, True, self.ikspline_cv_tn)
                cmds.parent("LeftUpperLeg_SplineCv", "DoNotTouch")

                llegcrv_info = ikspinedg_modifier.createNode("curveInfo")
                llegstretchpercent = ikspinedg_modifier.createNode("multiplyDivide")
                llegstretchpow = ikspinedg_modifier.createNode("multiplyDivide")
                llegstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                llegscalediv = ikspinedg_modifier.createNode("multiplyDivide")
                liklegstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                # liklegstretchsub = ikspinedg_modifier.createNode("plusMinusAverage")
                # liklegstretchsum = ikspinedg_modifier.createNode("plusMinusAverage")

                llegcrvinfo_fs = om1.MFnDependencyNode(llegcrv_info)
                llegstretchpercent_fs = om1.MFnDependencyNode(llegstretchpercent)
                llegstretchpow_fs = om1.MFnDependencyNode(llegstretchpow)
                llegstretchdiv_fs = om1.MFnDependencyNode(llegstretchdiv)
                llegscalediv_fs = om1.MFnDependencyNode(llegscalediv)
                liklegstretchdiv_fs = om1.MFnDependencyNode(liklegstretchdiv)
                # liklegstretchsub_fs = om1.MFnDependencyNode(liklegstretchsub)
                # liklegstretchsum_fs = om1.MFnDependencyNode(liklegstretchsum)
                liklegstretchcluster1_fs = om1.MFnDependencyNode(grp_legupperikcluster1)
                liklegstretchcluster2_fs = om1.MFnDependencyNode(grp_legupperikcluster2)

                llegcrvinfoarc_plug = llegcrvinfo_fs.findPlug("arcLength")
                llegstretchpercentinp1y_plug = llegstretchpercent_fs.findPlug("input1Y")
                llegstretchpercentotp_plug = llegstretchpercent_fs.findPlug("outputY")
                llegstretchpowinp1x_plug = llegstretchpow_fs.findPlug("input1X")
                llegstretchpowinp1z_plug = llegstretchpow_fs.findPlug("input1Z")
                llegstretchpowotpx_plug = llegstretchpow_fs.findPlug("outputX")
                llegstretchpowotpz_plug = llegstretchpow_fs.findPlug("outputZ")
                llegstretchdivinp2x_plug = llegstretchdiv_fs.findPlug("input2X")
                llegstretchdivinp2z_plug = llegstretchdiv_fs.findPlug("input2Z")
                llegstretchdivotox_plug = llegstretchdiv_fs.findPlug("outputX")
                llegstretchdivotpz_plug = llegstretchdiv_fs.findPlug("outputZ")
                llegscaledivinp1y_plug = llegscalediv_fs.findPlug("input1Y")
                llegscaledivinp2y_plug = llegscalediv_fs.findPlug("input2Y")
                llegscaledivotpy_plug = llegscalediv_fs.findPlug("outputY")
                # liklegstretchsubotp_plug = liklegstretchsub_fs.findPlug("output3D")
                liklegstretchdivinp1_plug = liklegstretchdiv_fs.findPlug("input1")
                liklegstretchdivotp_plug = liklegstretchdiv_fs.findPlug("output")
                # liklegstretchsumotp_plug = liklegstretchsum_fs.findPlug("output3D")
                liklegstretchclust1trans_plug = liklegstretchcluster1_fs.findPlug("translate")
                liklegstretchclust2trans_plug = liklegstretchcluster2_fs.findPlug("translate")

                objparent = om1.MObject()
                objchild = om1.MObject()
                for index in range(iklupperleg_sl_lst.length()):
                    if index < iklupperleg_sl_lst.length()-1:
                        iklupperleg_sl_lst.getDependNode(index, objparent)
                        iklupperleg_sl_lst.getDependNode(index+1, objchild)
                        llegparentjnt_fs = om1.MFnDependencyNode(objparent)
                        llegchildjnt_fs = om1.MFnDependencyNode(objchild)
                        llegjnt_syplug = llegparentjnt_fs.findPlug("scaleY")
                        llegjnt_sxplug = llegparentjnt_fs.findPlug("scaleX")
                        llegjnt_szplug = llegparentjnt_fs.findPlug("scaleZ")
                        llegjnt_sotpplug = llegparentjnt_fs.findPlug("scale")
                        llegjnt_invsplug = llegchildjnt_fs.findPlug("inverseScale")
                        ikspinedg_modifier.connect(llegstretchpercentotp_plug, llegjnt_syplug)
                        ikspinedg_modifier.connect(llegstretchdivotox_plug, llegjnt_sxplug)
                        ikspinedg_modifier.connect(llegstretchdivotpz_plug, llegjnt_szplug)
                        ikspinedg_modifier.connect(llegjnt_sotpplug, llegjnt_invsplug)


                ikspinedg_modifier.renameNode(llegcrv_info, "LeftUpperLegSpline_Info")
                ikspinedg_modifier.renameNode(llegstretchpercent, "LeftUpperLegStretch_Percent")
                ikspinedg_modifier.renameNode(llegstretchpow, "LeftUpperLegStretch_Power")
                ikspinedg_modifier.renameNode(llegstretchdiv, "LeftUpperLegStretch_Divide")
                ikspinedg_modifier.renameNode(ikspline_cv, "LeftUpperLeg_SplineCvShape")
                ikspinedg_modifier.renameNode(self.lleg_ik, "LeftUpperLeg_Ik")
                ikspinedg_modifier.renameNode(self.iklleg_effector, "LeftUpperLeg_effector")
                ikspinedg_modifier.renameNode(llegscalediv, "IkLeftUpperLegGlobalScale_Average")
                ikspinedg_modifier.renameNode(liklegstretchdiv, "LeftUpperLegStretch_Divide2")
                # ikspinedg_modifier.renameNode(liklegstretchsub, "LeftUpperLegStretch_Sub")
                # ikspinedg_modifier.renameNode(liklegstretchsum, "LeftUpperLegStretch_Sum")
                ikspinedg_modifier.commandToExecute('parent "LeftUpperLeg_Ik" "DoNotTouch"')
                ikspinedg_modifier.commandToExecute('connectAttr -force LeftUpperLeg_SplineCvShape.worldSpace[0] LeftUpperLeg_Ik.inCurve')
                ikspinedg_modifier.commandToExecute('skinCluster -bm 3 -sm 1 -dr 2.0 -name "LeftUpperLegIk_skin" IkCvSplineLeftUpperLeg0 IkCvSplineLeftUpperLeg1 IkCvSplineLeftUpperLeg2 LeftUpperLeg_SplineCv')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLeg_Ik.dTwistControlEnable" 1')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLeg_Ik.dWorldUpType" 4')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLeg_Ik.dForwardAxis" 3')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLeg_Ik.dWorldUpAxis" 4')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLeg_Ik.dWorldUpVectorY" 0')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLeg_Ik.dWorldUpVectorEndY" 0')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLeg_Ik.dWorldUpVectorZ" -1')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLeg_Ik.dWorldUpVectorEndZ" -1')
                ikspinedg_modifier.commandToExecute('connectAttr -force IkCvSplineLeftUpperLeg0.worldMatrix[0] LeftUpperLeg_Ik.dWorldUpMatrix')
                ikspinedg_modifier.commandToExecute('connectAttr -force IkCvSplineLeftUpperLeg2.worldMatrix[0] LeftUpperLeg_Ik.dWorldUpMatrixEnd')
                ikspinedg_modifier.commandToExecute('connectAttr -force LeftUpperLeg_SplineCvShape.worldSpace[0] LeftUpperLegSpline_Info.inputCurve')
                # ikspinedg_modifier.commandToExecute('connectAttr -force LeftUpperLegIkCluster1_grp.translate LeftUpperLegStretch_Sub.input3D[0]')
                # ikspinedg_modifier.commandToExecute('connectAttr -force LeftUpperLegIkCluster2_grp.translate LeftUpperLegStretch_Sub.input3D[1]')
                # ikspinedg_modifier.commandToExecute('connectAttr -force LeftUpperLegIkCluster2_grp.translate LeftUpperLegStretch_Sum.input3D[0]')
                # ikspinedg_modifier.commandToExecute('connectAttr -force LeftUpperLegStretch_Divide2.output LeftUpperLegStretch_Sum.input3D[1]')
                ikspinedg_modifier.connect(llegcrvinfoarc_plug, llegscaledivinp1y_plug)
                ikspinedg_modifier.connect(masterctrlsy_plug, llegscaledivinp2y_plug)
                ikspinedg_modifier.connect(llegscaledivotpy_plug, llegstretchpercentinp1y_plug)
                ikspinedg_modifier.connect(llegstretchpercentotp_plug, llegstretchpowinp1x_plug)
                ikspinedg_modifier.connect(llegstretchpercentotp_plug, llegstretchpowinp1z_plug)
                ikspinedg_modifier.connect(llegstretchpowotpx_plug, llegstretchdivinp2x_plug)
                ikspinedg_modifier.connect(llegstretchpowotpz_plug, llegstretchdivinp2z_plug)
                ikspinedg_modifier.connect(liklegstretchclust2trans_plug, liklegstretchdivinp1_plug)
                ikspinedg_modifier.connect(liklegstretchdivotp_plug, liklegstretchclust1trans_plug)
                ikspinedg_modifier.commandToExecute('float $leftupperlegstretchinput1Y = `getAttr "LeftUpperLegStretch_Percent.input1Y"`; setAttr "LeftUpperLegStretch_Percent.input2Y" $leftupperlegstretchinput1Y')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLegStretch_Power.input2X" 0.5')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLegStretch_Power.input2Z" 0.5')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLegStretch_Divide.input1X" 1')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLegStretch_Divide.input1Z" 1')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLegStretch_Percent.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLegStretch_Power.operation" 3')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLegStretch_Divide.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "IkLeftUpperLegGlobalScale_Average.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLegStretch_Divide2.operation" 2')
                # ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLegStretch_Sum.operation" 1')
                # ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLegStretch_Sub.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLegStretch_Divide2.input2X" 2')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLegStretch_Divide2.input2Y" 2')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLegStretch_Divide2.input2Z" 2')
                # ikspinedg_modifier.connect(liklegstretchsumotp_plug, liklegstretchclust1trans_plug)
                ikspinedg_modifier.doIt()

                ikspline_solver = ik_system.findSolver("ikSplineSolver")
                ik_handle.setSolver(ikspline_solver)

                grp_leglowerikcluster1 = om1.MObject()
                grp_leglowerikcluster2 = om1.MObject()

                if cmds.objExists("IkSplineLeftLowerLeg0"):
                    ikllowerleg_sl_lst = om1.MSelectionList()
                    ikllowerleg_sl_lst.add("IkSplineLeftLowerLeg*")
                    ikllowerleg_sl_lst.getDependNode(0, obj_root)
                    ikllowerleg_sl_lst.getDependNode(ikllowerleg_sl_lst.length()-1, obj_endspine)

                    ikllowerleggrp_sl_lst = om1.MSelectionList()
                    ikllowerleggrp_sl_lst.add("LeftLowerLegIkCluster1_grp")
                    ikllowerleggrp_sl_lst.add("LeftLowerLegIkCluster2_grp")
                    ikllowerleggrp_sl_lst.getDependNode(0, grp_leglowerikcluster1)
                    ikllowerleggrp_sl_lst.getDependNode(1, grp_leglowerikcluster2)

                    lleg_pathnode = om1.MDagPath()
                    rootspine_path = lleg_pathnode.getAPathTo(obj_root)

                    try:
                        ikspineiksolver_lst.add("ikSplineSolver*")
                    except:
                        cmds.createNode("ikSplineSolver")

                    self.iklleg_effector = ik_effector.create(obj_endspine)
                    iklleg_effector_path = lleg_pathnode.getAPathTo(self.iklleg_effector)

                    self.lleg_ik = ik_handle.create(rootspine_path, iklleg_effector_path)

                    obj_array = om1.MPointArray()
                    obj_lst_mpoint = []
                    obj = om1.MObject()
                    for index in range(ikllowerleg_sl_lst.length()):
                        ikllowerleg_sl_lst.getDependNode(index, obj)
                        obj_path = ikspineobj_path_n.getAPathTo(obj)
                        obj_tn = om1.MFnTransform(obj_path)
                        obj_t = obj_tn.translation(om1.MSpace.kWorld)
                        obj_lst_mpoint.append(om1.MPoint(obj_t))
                        obj_array.append(obj_lst_mpoint[index])

                    self.ikspline_cv_tn = ikspinedag_n.create("transform", "LeftLowerLeg_SplineCv")
                    ikspline_cv = ikspline_cv_n.createWithEditPoints(obj_array, 1, 1, False, True, True, self.ikspline_cv_tn)
                    cmds.parent("LeftLowerLeg_SplineCv", "DoNotTouch")

                    llegcrv_info = ikspinedg_modifier.createNode("curveInfo")
                    llegstretchpercent = ikspinedg_modifier.createNode("multiplyDivide")
                    llegstretchpow = ikspinedg_modifier.createNode("multiplyDivide")
                    llegstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                    llegscalediv = ikspinedg_modifier.createNode("multiplyDivide")
                    liklegstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                    # liklegstretchsub = ikspinedg_modifier.createNode("plusMinusAverage")
                    # liklegstretchsum = ikspinedg_modifier.createNode("plusMinusAverage")

                    llegcrvinfo_fs = om1.MFnDependencyNode(llegcrv_info)
                    llegstretchpercent_fs = om1.MFnDependencyNode(llegstretchpercent)
                    llegstretchpow_fs = om1.MFnDependencyNode(llegstretchpow)
                    llegstretchdiv_fs = om1.MFnDependencyNode(llegstretchdiv)
                    llegscalediv_fs = om1.MFnDependencyNode(llegscalediv)
                    liklegstretchdiv_fs = om1.MFnDependencyNode(liklegstretchdiv)
                    # liklegstretchsub_fs = om1.MFnDependencyNode(liklegstretchsub)
                    # liklegstretchsum_fs = om1.MFnDependencyNode(liklegstretchsum)
                    liklegstretchcluster1_fs = om1.MFnDependencyNode(grp_leglowerikcluster1)
                    liklegstretchcluster2_fs = om1.MFnDependencyNode(grp_leglowerikcluster2)

                    llegcrvinfoarc_plug = llegcrvinfo_fs.findPlug("arcLength")
                    llegstretchpercentinp1y_plug = llegstretchpercent_fs.findPlug("input1Y")
                    llegstretchpercentotp_plug = llegstretchpercent_fs.findPlug("outputY")
                    llegstretchpowinp1x_plug = llegstretchpow_fs.findPlug("input1X")
                    llegstretchpowinp1z_plug = llegstretchpow_fs.findPlug("input1Z")
                    llegstretchpowotpx_plug = llegstretchpow_fs.findPlug("outputX")
                    llegstretchpowotpz_plug = llegstretchpow_fs.findPlug("outputZ")
                    llegstretchdivinp2x_plug = llegstretchdiv_fs.findPlug("input2X")
                    llegstretchdivinp2z_plug = llegstretchdiv_fs.findPlug("input2Z")
                    llegstretchdivotox_plug = llegstretchdiv_fs.findPlug("outputX")
                    llegstretchdivotpz_plug = llegstretchdiv_fs.findPlug("outputZ")
                    llegscaledivinp1y_plug = llegscalediv_fs.findPlug("input1Y")
                    llegscaledivinp2y_plug = llegscalediv_fs.findPlug("input2Y")
                    llegscaledivotpy_plug = llegscalediv_fs.findPlug("outputY")
                    # liklegstretchsubotp_plug = liklegstretchsub_fs.findPlug("output3D")
                    liklegstretchdivinp1_plug = liklegstretchdiv_fs.findPlug("input1")
                    liklegstretchdivotp_plug = liklegstretchdiv_fs.findPlug("output")
                    # liklegstretchsumotp_plug = liklegstretchsum_fs.findPlug("output3D")
                    liklegstretchclust1trans_plug = liklegstretchcluster1_fs.findPlug("translate")
                    liklegstretchclust2trans_plug = liklegstretchcluster2_fs.findPlug("translate")

                    objparent = om1.MObject()
                    objchild = om1.MObject()
                    for index in range(ikllowerleg_sl_lst.length()):
                        if index < ikllowerleg_sl_lst.length()-1:
                            ikllowerleg_sl_lst.getDependNode(index, objparent)
                            ikllowerleg_sl_lst.getDependNode(index+1, objchild)
                            llegparentjnt_fs = om1.MFnDependencyNode(objparent)
                            llegchildjnt_fs = om1.MFnDependencyNode(objchild)
                            llegjnt_syplug = llegparentjnt_fs.findPlug("scaleY")
                            llegjnt_sxplug = llegparentjnt_fs.findPlug("scaleX")
                            llegjnt_szplug = llegparentjnt_fs.findPlug("scaleZ")
                            llegjnt_sotpplug = llegparentjnt_fs.findPlug("scale")
                            llegjnt_invsplug = llegchildjnt_fs.findPlug("inverseScale")
                            ikspinedg_modifier.connect(llegstretchpercentotp_plug, llegjnt_syplug)
                            ikspinedg_modifier.connect(llegstretchdivotox_plug, llegjnt_sxplug)
                            ikspinedg_modifier.connect(llegstretchdivotpz_plug, llegjnt_szplug)
                            ikspinedg_modifier.connect(llegjnt_sotpplug, llegjnt_invsplug)


                    ikspinedg_modifier.renameNode(llegcrv_info, "LeftLowerLegSpline_Info")
                    ikspinedg_modifier.renameNode(llegstretchpercent, "LeftLowerLegStretch_Percent")
                    ikspinedg_modifier.renameNode(llegstretchpow, "LeftLowerLegStretch_Power")
                    ikspinedg_modifier.renameNode(llegstretchdiv, "LeftLowerLegStretch_Divide")
                    ikspinedg_modifier.renameNode(ikspline_cv, "LeftLowerLeg_SplineCvShape")
                    ikspinedg_modifier.renameNode(self.lleg_ik, "LeftLowerLeg_Ik")
                    ikspinedg_modifier.renameNode(self.iklleg_effector, "LeftLowerLeg_effector")
                    ikspinedg_modifier.renameNode(llegscalediv, "IkLeftLowerLegGlobalScale_Average")
                    ikspinedg_modifier.renameNode(liklegstretchdiv, "LeftLowerLegStretch_Divide2")
                    # ikspinedg_modifier.renameNode(liklegstretchsub, "LeftLowerLegStretch_Sub")
                    # ikspinedg_modifier.renameNode(liklegstretchsum, "LeftLowerLegStretch_Sum")
                    ikspinedg_modifier.commandToExecute('parent "LeftLowerLeg_Ik" "DoNotTouch"')
                    ikspinedg_modifier.commandToExecute('connectAttr -f LeftLowerLeg_SplineCvShape.worldSpace[0] LeftLowerLeg_Ik.inCurve')
                    ikspinedg_modifier.commandToExecute('skinCluster -bm 3 -sm 1 -dr 2.0 -name "LeftLowerLegIk_skin" IkCvSplineLeftLowerLeg0 IkCvSplineLeftLowerLeg1 IkCvSplineLeftLowerLeg2 LeftLowerLeg_SplineCv')
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLeg_Ik.dTwistControlEnable" 1')
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLeg_Ik.dWorldUpType" 4')
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLeg_Ik.dForwardAxis" 3')
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLeg_Ik.dWorldUpAxis" 4')
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLeg_Ik.dWorldUpVectorY" 0')
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLeg_Ik.dWorldUpVectorEndY" 0')
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLeg_Ik.dWorldUpVectorZ" -1')
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLeg_Ik.dWorldUpVectorEndZ" -1')
                    ikspinedg_modifier.commandToExecute('connectAttr -f IkCvSplineLeftLowerLeg0.worldMatrix[0] LeftLowerLeg_Ik.dWorldUpMatrix')
                    ikspinedg_modifier.commandToExecute('connectAttr -f IkCvSplineLeftLowerLeg2.worldMatrix[0] LeftLowerLeg_Ik.dWorldUpMatrixEnd')
                    ikspinedg_modifier.commandToExecute('connectAttr -f LeftLowerLeg_SplineCvShape.worldSpace[0] LeftLowerLegSpline_Info.inputCurve')
                    # ikspinedg_modifier.commandToExecute('connectAttr -f LeftLowerLegIkCluster_grp.translate LeftLowerLegStretch_Sub.input3D[0]')
                    # ikspinedg_modifier.commandToExecute('connectAttr -f LeftLowerLegIkCluster2_grp.translate LeftLowerLegStretch_Sub.input3D[1]')
                    # ikspinedg_modifier.commandToExecute('connectAttr -f LeftLowerLegIkCluster2_grp.translate LeftLowerLegStretch_Sum.input3D[0]')
                    # ikspinedg_modifier.commandToExecute('connectAttr -f LeftLowerLegStretch_Divide2.output LeftLowerLegStretch_Sum.input3D[1]')
                    ikspinedg_modifier.connect(llegcrvinfoarc_plug, llegscaledivinp1y_plug)
                    ikspinedg_modifier.connect(masterctrlsy_plug, llegscaledivinp2y_plug)
                    ikspinedg_modifier.connect(llegscaledivotpy_plug, llegstretchpercentinp1y_plug)
                    ikspinedg_modifier.connect(llegstretchpercentotp_plug, llegstretchpowinp1x_plug)
                    ikspinedg_modifier.connect(llegstretchpercentotp_plug, llegstretchpowinp1z_plug)
                    ikspinedg_modifier.connect(llegstretchpowotpx_plug, llegstretchdivinp2x_plug)
                    ikspinedg_modifier.connect(llegstretchpowotpz_plug, llegstretchdivinp2z_plug)
                    ikspinedg_modifier.connect(liklegstretchclust2trans_plug, liklegstretchdivinp1_plug)
                    ikspinedg_modifier.connect(liklegstretchdivotp_plug, liklegstretchclust1trans_plug)
                    ikspinedg_modifier.commandToExecute('float $leftlowerlegstretchinput1Y = `getAttr "LeftLowerLegStretch_Percent.input1Y"`; setAttr "LeftLowerLegStretch_Percent.input2Y" $leftlowerlegstretchinput1Y')
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLegStretch_Power.input2X" 0.5')
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLegStretch_Power.input2Z" 0.5')
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLegStretch_Divide.input1X" 1')
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLegStretch_Divide.input1Z" 1')
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLegStretch_Percent.operation" 2')
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLegStretch_Power.operation" 3')
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLegStretch_Divide.operation" 2')
                    ikspinedg_modifier.commandToExecute('setAttr "IkLeftLowerLegGlobalScale_Average.operation" 2')
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLegStretch_Divide2.operation" 2')
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLegStretch_Divide2.input2X" 2')
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLegStretch_Divide2.input2Y" 2')
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLegStretch_Divide2.input2Z" 2')
                    ikspinedg_modifier.doIt()

                    ikspline_solver = ik_system.findSolver("ikSplineSolver")
                    ik_handle.setSolver(ikspline_solver)

        if cmds.objExists("NoFlipLeftLeg_Ik") and cmds.objExists("PVLeftLeg_Ik"):
            llegik_sl_ls = om2.MSelectionList()
            llegik_sl_ls.add("LeftLegIk_grp")
            llegik_sl_ls.add("Biped_NoFlipLeftKnee_null")
            llegik_sl_ls.add("Biped_IkLeftFoot_ctrl")
            llegik_sl_ls.add("IkLeftJointLeg_grp")
            llegik_sl_ls.add("IkStretchyLeftJointLeg_grp")
            likleggrpobj_fs = om2.MFnDependencyNode(llegik_sl_ls.getDependNode(0))
            noflipleftkneenullobj_fs = om2.MFnDependencyNode(llegik_sl_ls.getDependNode(1))
            iklegctrl_fs = om2.MFnDependencyNode(llegik_sl_ls.getDependNode(2))
            ikleftjointleggrp_fs = om2.MFnDependencyNode(llegik_sl_ls.getDependNode(3))

            if self.typeofLLegIK.currentIndex() == 1 or 2:
                liklegctrl_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
                liklegctrl_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                self.ctrl_mod_n.renameNode(liklegctrl_multMatrix, "IkLeftLegCtrl_multMatrix")
                self.ctrl_mod_n.renameNode(liklegctrl_decomposeMatrix, "IkLeftLegCtrl_decomposeMatrix")

                liklegmultMatrix_fs = om2.MFnDependencyNode(liklegctrl_multMatrix)
                liklegdecomposeMatrix_fs = om2.MFnDependencyNode(liklegctrl_decomposeMatrix)

                liklegmultMatrixSum_plug = liklegmultMatrix_fs.findPlug("matrixSum", False)
                liklegdecomposeInpMatrix_plug = liklegdecomposeMatrix_fs.findPlug("inputMatrix", False)
                liklegdecomposeOtpTrans_plug = liklegdecomposeMatrix_fs.findPlug("outputTranslate", False)
                liklegdecomposeOtpRot_plug = liklegdecomposeMatrix_fs.findPlug("outputRotate", False)
                likleggrpTrans_plug = likleggrpobj_fs.findPlug("translate", False)
                likleggrpRot_plug = likleggrpobj_fs.findPlug("rotate", False)
                noflipleftkneenullTrans_plug = noflipleftkneenullobj_fs.findPlug("translate", False)
                noflipleftkneenullRot_plug = noflipleftkneenullobj_fs.findPlug("rotate", False)
                niklegctrlTrans_plug = iklegctrl_fs.findPlug("translate", False)
                iklegctrlRot_plug = iklegctrl_fs.findPlug("rotate", False)

                self.ctrl_mod_n.commandToExecute('connectAttr -force Biped_IkLeftFoot_ctrl.worldMatrix[0] IkLeftLegCtrl_multMatrix.matrixIn[0]')
                self.ctrl_mod_n.commandToExecute('parent LeftReverseFootHeel LeftLegIk_grp')
                self.ctrl_mod_n.commandToExecute('poleVectorConstraint Biped_NoFlipLeftKnee_ctrl NoFlipLeftLeg_Ik')
                self.ctrl_mod_n.commandToExecute('poleVectorConstraint Biped_PVLeftKnee_ctrl PVLeftLeg_Ik')
                self.ctrl_mod_n.commandToExecute('setAttr "NoFlipLeftLeg_Ik.twist" 90')
                self.ctrl_mod_n.connect(liklegmultMatrixSum_plug, liklegdecomposeInpMatrix_plug)
                self.ctrl_mod_n.connect(liklegdecomposeOtpTrans_plug, likleggrpTrans_plug)
                self.ctrl_mod_n.connect(liklegdecomposeOtpRot_plug, likleggrpRot_plug)
                self.ctrl_mod_n.connect(niklegctrlTrans_plug, noflipleftkneenullTrans_plug)
                self.ctrl_mod_n.connect(iklegctrlRot_plug, noflipleftkneenullRot_plug)

                liklegdistloc = om2.MFnDagNode()

                likupperlegdistloc1_tn = liklegdistloc.create("transform", "distloc_L_upleg1", llegik_sl_ls.getDependNode(4))
                likupperlegdistloc_ln = liklegdistloc.create("locator", "L_upleg1_Shape", likupperlegdistloc1_tn)
                likfootlegdistloc1_tn = liklegdistloc.create("transform", "distloc_L_legfoot1")
                likfootlegdistloc_ln = liklegdistloc.create("locator", "L_foot1_Shape", likfootlegdistloc1_tn)
                self.ctrl_mod_n.commandToExecute('createNode "distanceDimShape"')
                self.ctrl_mod_n.commandToExecute('rename "distanceDimension1" "IkLeftLegDistance_Info"')
                self.ctrl_mod_n.doIt()

                luplegnull_transform_t = luplegnull_transform.translation(om2.MSpace.kTransform)
                likupperlegdistloc_transform = om2.MFnTransform(likupperlegdistloc1_tn)
                likupperlegdistloc_transform.setTranslation(luplegnull_transform_t, om2.MSpace.kTransform)

                IkLeftLegDistance_sl_ls = om2.MSelectionList()
                IkLeftLegDistance_sl_ls.add("IkLeftLegDistance_InfoShape")

                likfootlegDist_fs = om2.MFnDependencyNode(likfootlegdistloc1_tn)
                liklegjntDist_fs = om2.MFnDependencyNode(IkLeftLegDistance_sl_ls.getDependNode(0))

                liklegjntDistPoint2_plug = liklegjntDist_fs.findPlug("endPoint", False)
                likfootlegDistOtpTrans_plug = likfootlegDist_fs.findPlug("translate", False)

                self.ctrl_mod_n.commandToExecute('connectAttr -force L_upleg1_Shape.worldPosition[0] IkLeftLegDistance_InfoShape.startPoint')
                self.ctrl_mod_n.connect(likfootlegDistOtpTrans_plug, liklegjntDistPoint2_plug)
                self.ctrl_mod_n.connect(liklegdecomposeOtpTrans_plug, likfootlegDistOtpTrans_plug)
                self.ctrl_mod_n.commandToExecute('float $noflipikleftlegtranslateY = `getAttr "IkNoFlipLeftLeg.translateY"`; float $noflipikleftfoottranslateY = `getAttr "IkNoFlipLeftFoot.translateY"`; float $totalnoflipikleftlegtranslateY = $noflipikleftlegtranslateY + $noflipikleftfoottranslateY; setDrivenKeyframe -currentDriver IkLeftLegDistance_InfoShape.distance -driverValue $totalnoflipikleftlegtranslateY -attribute "translateY" -value $noflipikleftlegtranslateY IkNoFlipLeftLeg;')
                self.ctrl_mod_n.commandToExecute('float $noflipikleftlegtranslateY = `getAttr "IkNoFlipLeftLeg.translateY"`; float $noflipikleftfoottranslateY = `getAttr "IkNoFlipLeftFoot.translateY"`; float $totalnoflipikleftlegtranslateY = $noflipikleftlegtranslateY + $noflipikleftfoottranslateY; setDrivenKeyframe -currentDriver IkLeftLegDistance_InfoShape.distance -driverValue ($totalnoflipikleftlegtranslateY*2) -attribute "translateY" -value ($noflipikleftlegtranslateY*2) IkNoFlipLeftLeg;')
                self.ctrl_mod_n.commandToExecute('float $noflipikleftlegtranslateY = `getAttr "IkNoFlipLeftLeg.translateY"`; float $noflipikleftfoottranslateY = `getAttr "IkNoFlipLeftFoot.translateY"`; float $totalnoflipikleftlegtranslateY = $noflipikleftlegtranslateY + $noflipikleftfoottranslateY; setDrivenKeyframe -currentDriver IkLeftLegDistance_InfoShape.distance -driverValue $totalnoflipikleftlegtranslateY -attribute "translateY" -value $noflipikleftfoottranslateY IkNoFlipLeftFoot;')
                self.ctrl_mod_n.commandToExecute('float $noflipikleftlegtranslateY = `getAttr "IkNoFlipLeftLeg.translateY"`; float $noflipikleftfoottranslateY = `getAttr "IkNoFlipLeftFoot.translateY"`; float $totalnoflipikleftlegtranslateY = $noflipikleftlegtranslateY + $noflipikleftfoottranslateY; setDrivenKeyframe -currentDriver IkLeftLegDistance_InfoShape.distance -driverValue ($totalnoflipikleftlegtranslateY*2) -attribute "translateY" -value ($noflipikleftfoottranslateY*2) IkNoFlipLeftFoot;')
                self.ctrl_mod_n.commandToExecute('float $pvikleftlegtranslateY = `getAttr "IkPVLeftLeg.translateY"`; float $pvikleftfoottranslateY = `getAttr "IkPVLeftFoot.translateY"`; float $totalpvikleftlegtranslateY = $pvikleftlegtranslateY + $pvikleftfoottranslateY; setDrivenKeyframe -currentDriver IkLeftLegDistance_InfoShape.distance -driverValue $totalpvikleftlegtranslateY -attribute "translateY" -value $pvikleftlegtranslateY IkPVLeftLeg;')
                self.ctrl_mod_n.commandToExecute('float $pvikleftlegtranslateY = `getAttr "IkPVLeftLeg.translateY"`; float $pvikleftfoottranslateY = `getAttr "IkPVLeftFoot.translateY"`; float $totalpvikleftlegtranslateY = $pvikleftlegtranslateY + $pvikleftfoottranslateY; setDrivenKeyframe -currentDriver IkLeftLegDistance_InfoShape.distance -driverValue ($totalpvikleftlegtranslateY*2) -attribute "translateY" -value ($pvikleftlegtranslateY*2) IkPVLeftLeg;')
                self.ctrl_mod_n.commandToExecute('float $pvikleftlegtranslateY = `getAttr "IkPVLeftLeg.translateY"`; float $pvikleftfoottranslateY = `getAttr "IkPVLeftFoot.translateY"`; float $totalpvikleftlegtranslateY = $pvikleftlegtranslateY + $pvikleftfoottranslateY; setDrivenKeyframe -currentDriver IkLeftLegDistance_InfoShape.distance -driverValue $totalpvikleftlegtranslateY -attribute "translateY" -value $pvikleftfoottranslateY IkPVLeftFoot;')
                self.ctrl_mod_n.commandToExecute('float $pvikleftlegtranslateY = `getAttr "IkPVLeftLeg.translateY"`; float $pvikleftfoottranslateY = `getAttr "IkPVLeftFoot.translateY"`; float $totalpvikleftlegtranslateY = $pvikleftlegtranslateY + $pvikleftfoottranslateY; setDrivenKeyframe -currentDriver IkLeftLegDistance_InfoShape.distance -driverValue ($totalpvikleftlegtranslateY*2) -attribute "translateY" -value ($pvikleftfoottranslateY*2) IkPVLeftFoot;')
                self.ctrl_mod_n.commandToExecute('selectKey -attribute translateY IkNoFlipLeftLeg; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative')
                self.ctrl_mod_n.commandToExecute('selectKey -attribute translateY IkPVLeftLeg; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative')
                self.ctrl_mod_n.commandToExecute('selectKey -attribute translateY IkNoFlipLeftFoot; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative')
                self.ctrl_mod_n.commandToExecute('selectKey -attribute translateY IkPVLeftFoot; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative')
                self.ctrl_mod_n.commandToExecute('parent "IkLeftLegDistance_Info" "DoNotTouch"')
                self.ctrl_mod_n.commandToExecute('parent "distloc_L_legfoot1" "DoNotTouch"')

                self.ctrl_mod_n.commandToExecute('addAttr -longName "kneesnap" -niceName "Knee Snap" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_PVLeftKnee_ctrl')

                likupperlegdistloc2_tn = liklegdistloc.create("transform", "distloc_L_upleg2", llegik_sl_ls.getDependNode(4))
                likupperlegdistloc_ln = liklegdistloc.create("locator", "L_upleg2_Shape", likupperlegdistloc2_tn)
                likkneedistloc_tn = liklegdistloc.create("transform", "distloc_L_legknee")
                likkneedistloc_ln = liklegdistloc.create("locator", "L_legknee_Shape", likkneedistloc_tn)
                likfootlegdistloc2_tn = liklegdistloc.create("transform", "distloc_L_legfoot2")
                likfootlegdistloc_ln = liklegdistloc.create("locator", "L_legfoot2_Shape", likfootlegdistloc2_tn)
                pvleftkneectrl_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                likpvuppertransblendnode = self.ctrl_mod_n.createNode("blendColors")
                likpvlowertransblendnode = self.ctrl_mod_n.createNode("blendColors")
                self.ctrl_mod_n.commandToExecute('createNode "distanceDimShape"')
                self.ctrl_mod_n.commandToExecute('createNode "distanceDimShape"')
                self.ctrl_mod_n.renameNode(pvleftkneectrl_decomposeMatrix, "PVLeftKnee_decomposeMatrix")
                self.ctrl_mod_n.renameNode(likpvuppertransblendnode, "PVLeftUpperLegTrans_blend")
                self.ctrl_mod_n.renameNode(likpvlowertransblendnode, "PVLeftLowerLegTrans_blend")
                self.ctrl_mod_n.commandToExecute('rename "distanceDimension1" "LeftUpperLegDistance_Info"')
                self.ctrl_mod_n.commandToExecute('rename "distanceDimension2" "LeftLowerLegDistance_Info"')
                self.ctrl_mod_n.doIt()

                likupperlegdistloc2_transform = om2.MFnTransform(likupperlegdistloc2_tn)
                likupperlegdistloc2_transform.setTranslation(luplegnull_transform_t, om2.MSpace.kTransform)

                IkLeftLegDistance_sl_ls.add("LeftUpperLegDistance_InfoShape")
                IkLeftLegDistance_sl_ls.add("LeftLowerLegDistance_InfoShape")
                IkLeftLegDistance_sl_ls.add("IkPVLeftLeg_translateY")
                IkLeftLegDistance_sl_ls.add("IkPVLeftFoot_translateY")
                IkLeftLegDistance_sl_ls.add("Biped_PVLeftKnee_ctrl")
                IkLeftLegDistance_sl_ls.add("IkNoFlipLeftLeg_translateY")
                IkLeftLegDistance_sl_ls.add("IkNoFlipLeftFoot_translateY")

                likkneeDist_fs = om2.MFnDependencyNode(likkneedistloc_tn)
                likfootlegDist_fs = om2.MFnDependencyNode(likfootlegdistloc2_tn)
                likupperlegjntDist_fs = om2.MFnDependencyNode(IkLeftLegDistance_sl_ls.getDependNode(1))
                liklowerlegjntDist_fs = om2.MFnDependencyNode(IkLeftLegDistance_sl_ls.getDependNode(2))
                pvleftkneekey_fs = om2.MFnDependencyNode(IkLeftLegDistance_sl_ls.getDependNode(3))
                pvleftfootkey_fs = om2.MFnDependencyNode(IkLeftLegDistance_sl_ls.getDependNode(4))
                pvleftkneectrlDecomposeMatrix_fs = om2.MFnDependencyNode(pvleftkneectrl_decomposeMatrix)
                likpvuppertransblendnode_fs = om2.MFnDependencyNode(likpvuppertransblendnode)
                likpvlowertransblendnode_fs = om2.MFnDependencyNode(likpvlowertransblendnode)
                pvleftkneectrl_fs = om2.MFnDependencyNode(IkLeftLegDistance_sl_ls.getDependNode(5))
                pvlefkneejnt_fs = om2.MFnDependencyNode(pviklleg_sl_ls.getDependNode(1))
                pvleftfootjnt_fs = om2.MFnDependencyNode(pviklleg_sl_ls.getDependNode(2))

                likupperlegjntDistPoint2_plug = likupperlegjntDist_fs.findPlug("endPoint", False)
                liklowerlegjntDistPoint1_plug = liklowerlegjntDist_fs.findPlug("startPoint", False)
                liklowerlegjntDistPoint2_plug = liklowerlegjntDist_fs.findPlug("endPoint", False)
                likkneeDistOtpTrans_plug = likkneeDist_fs.findPlug("translate", False)
                likfootlegDistOtpTrans_plug = likfootlegDist_fs.findPlug("translate", False)
                pvleftkneectrlDecomposeMatrixOtpTrans_plug = pvleftkneectrlDecomposeMatrix_fs.findPlug("outputTranslate", False)
                pvleftkneekeyotp_plug = pvleftkneekey_fs.findPlug("output", False)
                pvleftfootkeyotp_plug = pvleftfootkey_fs.findPlug("output", False)
                likpvuppertransblendnodeinp1g_plug = likpvuppertransblendnode_fs.findPlug("color1G", False)
                likpvuppertransblendnodeinp2g_plug = likpvuppertransblendnode_fs.findPlug("color2G", False)
                likpvuppertransblendnodeotp_plug = likpvuppertransblendnode_fs.findPlug("outputG", False)
                likpvuppertransblendnodeblender_plug = likpvuppertransblendnode_fs.findPlug("blender", False)
                likpvlowertransblendnodeinp1g_plug = likpvlowertransblendnode_fs.findPlug("color1G", False)
                likpvlowertransblendnodeinp2g_plug = likpvlowertransblendnode_fs.findPlug("color2G", False)
                likpvlowertransblendnodeotp_plug = likpvlowertransblendnode_fs.findPlug("outputG", False)
                likpvlowertransblendnodeblender_plug = likpvlowertransblendnode_fs.findPlug("blender", False)
                pvleftkneectrl_fs_plug = pvleftkneectrl_fs.findPlug("kneesnap", False)
                pvlefkneejntTrans_plug = pvlefkneejnt_fs.findPlug("translateY", False)
                pvleftfootjntTrans_plug = pvleftfootjnt_fs.findPlug("translateY", False)

                self.ctrl_mod_n.commandToExecute('connectAttr -force L_upleg2_Shape.worldPosition[0] LeftUpperLegDistance_InfoShape.startPoint')
                self.ctrl_mod_n.commandToExecute('connectAttr -force Biped_PVLeftKnee_ctrl.worldMatrix[0] PVLeftKnee_decomposeMatrix.inputMatrix')
                self.ctrl_mod_n.connect(likkneeDistOtpTrans_plug, likupperlegjntDistPoint2_plug)
                self.ctrl_mod_n.connect(likkneeDistOtpTrans_plug, liklowerlegjntDistPoint1_plug)
                self.ctrl_mod_n.connect(likfootlegDistOtpTrans_plug, liklowerlegjntDistPoint2_plug)
                self.ctrl_mod_n.connect(liklegdecomposeOtpTrans_plug, likfootlegDistOtpTrans_plug)
                self.ctrl_mod_n.connect(pvleftkneectrlDecomposeMatrixOtpTrans_plug, likkneeDistOtpTrans_plug)

                self.ctrl_mod_n.disconnect(pvleftkneekeyotp_plug, pvlefkneejntTrans_plug)
                self.ctrl_mod_n.disconnect(pvleftfootkeyotp_plug, pvleftfootjntTrans_plug)
                self.ctrl_mod_n.connect(pvleftkneekeyotp_plug, likpvuppertransblendnodeinp2g_plug)
                self.ctrl_mod_n.connect(pvleftfootkeyotp_plug, likpvlowertransblendnodeinp2g_plug)
                self.ctrl_mod_n.connect(pvleftkneectrl_fs_plug, likpvuppertransblendnodeblender_plug)
                self.ctrl_mod_n.connect(pvleftkneectrl_fs_plug, likpvlowertransblendnodeblender_plug)
                self.ctrl_mod_n.connect(likpvuppertransblendnodeotp_plug, pvlefkneejntTrans_plug)
                self.ctrl_mod_n.connect(likpvlowertransblendnodeotp_plug, pvleftfootjntTrans_plug)
                self.ctrl_mod_n.commandToExecute('parent "distloc_L_legknee" "DoNotTouch"')
                self.ctrl_mod_n.commandToExecute('parent "distloc_L_legfoot2" "DoNotTouch"')
                self.ctrl_mod_n.commandToExecute('parent "LeftUpperLegDistance_Info" "DoNotTouch"')
                self.ctrl_mod_n.commandToExecute('parent "LeftLowerLegDistance_Info" "DoNotTouch"')

                self.ctrl_mod_n.commandToExecute('addAttr -longName "thighlength" -niceName "AutoKnee Thigh Length" -attributeType double -minValue 0 -keyable true -defaultValue 1 Biped_IkLeftFoot_ctrl')
                self.ctrl_mod_n.commandToExecute('addAttr -longName "calflength" -niceName "AutoKnee Calf Length" -attributeType double -minValue 0 -keyable true -defaultValue 1 Biped_IkLeftFoot_ctrl')
                self.ctrl_mod_n.doIt()

                likautokneeupperlegnode = self.ctrl_mod_n.createNode("multiplyDivide")
                likautokneelowerlegnode = self.ctrl_mod_n.createNode("multiplyDivide")
                self.ctrl_mod_n.renameNode(likautokneeupperlegnode, "NoFlipLeftLegTrans_multiply")
                self.ctrl_mod_n.renameNode(likautokneelowerlegnode, "NoFlipLeftFootTrans_multiply")

                likautokneeupperleg_fs = om2.MFnDependencyNode(likautokneeupperlegnode)
                likautokneelowerleg_fs = om2.MFnDependencyNode(likautokneelowerlegnode)
                noflipleftkneekey_fs = om2.MFnDependencyNode(IkLeftLegDistance_sl_ls.getDependNode(6))
                noflipleftfootkey_fs = om2.MFnDependencyNode(IkLeftLegDistance_sl_ls.getDependNode(7))
                nofliplefkneejntTrans_fs = om2.MFnDependencyNode(noflipiklleg_sl_ls.getDependNode(1))
                noflipleftfootjntTrans_fs = om2.MFnDependencyNode(noflipiklleg_sl_ls.getDependNode(2))

                ikautokneeupperlegInp1Y_plug = likautokneeupperleg_fs.findPlug("input1Y", False)
                ikautokneeupperlegInp2Y_plug = likautokneeupperleg_fs.findPlug("input2Y", False)
                ikautokneeupperlegOtp_plug = likautokneeupperleg_fs.findPlug("outputY", False)
                ikautokneelowerlegInp1Y_plug = likautokneelowerleg_fs.findPlug("input1Y", False)
                ikautokneelowerlegInp2Y_plug = likautokneelowerleg_fs.findPlug("input2Y", False)
                ikautokneelowerlegOtp_plug = likautokneelowerleg_fs.findPlug("outputY", False)
                noflipleftkneekeyotp_plug = noflipleftkneekey_fs.findPlug("output", False)
                noflipleftfootkeyotp_plug = noflipleftfootkey_fs.findPlug("output", False)
                nofliplefkneejnttty_plug = nofliplefkneejntTrans_fs.findPlug("translateY", False)
                noflipleftfootjntty_plug = noflipleftfootjntTrans_fs.findPlug("translateY", False)
                iklegctrlkneeupperleg_plug = iklegctrl_fs.findPlug("thighlength", False)
                iklegctrlkneelowerleg_plug = iklegctrl_fs.findPlug("calflength", False)

                self.ctrl_mod_n.disconnect(noflipleftkneekeyotp_plug, nofliplefkneejnttty_plug)
                self.ctrl_mod_n.disconnect(noflipleftfootkeyotp_plug, noflipleftfootjntty_plug)
                self.ctrl_mod_n.connect(iklegctrlkneeupperleg_plug, ikautokneeupperlegInp1Y_plug)
                self.ctrl_mod_n.connect(noflipleftkneekeyotp_plug, ikautokneeupperlegInp2Y_plug)
                self.ctrl_mod_n.connect(iklegctrlkneelowerleg_plug, ikautokneelowerlegInp1Y_plug)
                self.ctrl_mod_n.connect(noflipleftfootkeyotp_plug, ikautokneelowerlegInp2Y_plug)
                self.ctrl_mod_n.connect(ikautokneeupperlegOtp_plug, nofliplefkneejnttty_plug)
                self.ctrl_mod_n.connect(ikautokneelowerlegOtp_plug, noflipleftfootjntty_plug)
                self.ctrl_mod_n.commandToExecute('setAttr "NoFlipLeftLegTrans_multiply.operation" 1')
                self.ctrl_mod_n.commandToExecute('setAttr "NoFlipLeftFootTrans_multiply.operation" 1')

                leftlegglobalscalenode = self.ctrl_mod_n.createNode("multiplyDivide")
                noflipleftlegglobalscalenode = self.ctrl_mod_n.createNode("multiplyDivide")
                noflipleftfootlobalscalenode = self.ctrl_mod_n.createNode("multiplyDivide")
                self.ctrl_mod_n.renameNode(leftlegglobalscalenode, "IKLeftLegGlobalScale_Average")
                self.ctrl_mod_n.renameNode(noflipleftlegglobalscalenode, "IKNoFlipLeftLegGlobalScale_Average")
                self.ctrl_mod_n.renameNode(noflipleftfootlobalscalenode, "IKNoFlipLeftFootGlobalScale_Average")

                leftlegglobalscale_fs = om2.MFnDependencyNode(leftlegglobalscalenode)
                noflipleftlegglobalscale_fs = om2.MFnDependencyNode(noflipleftlegglobalscalenode)
                noflipleftfootlobalscale_fs = om2.MFnDependencyNode(noflipleftfootlobalscalenode)
                masterlctrl_fs = om2.MFnDependencyNode(obj_masterctrl2)

                likupperlegjntDist_plug = likupperlegjntDist_fs.findPlug("distance", False)
                liklowerlegjntDist_plug = liklowerlegjntDist_fs.findPlug("distance", False)
                liklegjntDist_plug = liklegjntDist_fs.findPlug("distance", False)
                masterlctrlsy_plug = masterlctrl_fs.findPlug("scaleY", False)
                leftlegglobalscaleInp1Y_plug = leftlegglobalscale_fs.findPlug("input1Y", False)
                leftlegglobalscaleInp2Y_plug = leftlegglobalscale_fs.findPlug("input2Y", False)
                leftlegglobalscaleOtpY_plug = leftlegglobalscale_fs.findPlug("outputY", False)
                noflipleftlegglobalscaleInp1Y_plug = noflipleftlegglobalscale_fs.findPlug("input1Y", False)
                noflipleftlegglobalscaleInp2Y_plug = noflipleftlegglobalscale_fs.findPlug("input2Y", False)
                noflipleftlegglobalscaleOtpY_plug = noflipleftlegglobalscale_fs.findPlug("outputY", False)
                noflipleftfootlobalscaleInp1Y_plug = noflipleftfootlobalscale_fs.findPlug("input1Y", False)
                noflipleftfootlobalscaleInp2Y_plug = noflipleftfootlobalscale_fs.findPlug("input2Y", False)
                noflipleftfootlobalscaleOtpY_plug = noflipleftfootlobalscale_fs.findPlug("outputY", False)
                noflipleftkneekeyinp_plug = noflipleftkneekey_fs.findPlug("input", False)
                noflipleftfootkeyinp_plug = noflipleftfootkey_fs.findPlug("input", False)
                pvleftkneekeyinp_plug = pvleftkneekey_fs.findPlug("input", False)
                pvleftfootkeyinp_plug = pvleftfootkey_fs.findPlug("input", False)
                ikleftjointleggrps_plug = ikleftjointleggrp_fs.findPlug("scale", False)

                self.ctrl_mod_n.disconnect(liklegjntDist_plug, noflipleftkneekeyinp_plug)
                self.ctrl_mod_n.disconnect(liklegjntDist_plug, noflipleftfootkeyinp_plug)
                self.ctrl_mod_n.disconnect(liklegjntDist_plug, pvleftkneekeyinp_plug)
                self.ctrl_mod_n.disconnect(liklegjntDist_plug, pvleftfootkeyinp_plug)
                self.ctrl_mod_n.connect(liklowerlegjntDist_plug, noflipleftfootlobalscaleInp1Y_plug)
                self.ctrl_mod_n.connect(likupperlegjntDist_plug, noflipleftlegglobalscaleInp1Y_plug)
                self.ctrl_mod_n.connect(liklowerlegjntDist_plug, noflipleftfootlobalscaleInp1Y_plug)
                self.ctrl_mod_n.connect(masterlctrlsy_plug, noflipleftlegglobalscaleInp2Y_plug)
                self.ctrl_mod_n.connect(masterlctrlsy_plug, noflipleftfootlobalscaleInp2Y_plug)
                self.ctrl_mod_n.connect(noflipleftlegglobalscaleOtpY_plug, likpvuppertransblendnodeinp1g_plug)
                self.ctrl_mod_n.connect(noflipleftfootlobalscaleOtpY_plug, likpvlowertransblendnodeinp1g_plug)
                self.ctrl_mod_n.connect(liklegjntDist_plug, leftlegglobalscaleInp1Y_plug)
                self.ctrl_mod_n.connect(masterlctrlsy_plug, leftlegglobalscaleInp2Y_plug)
                self.ctrl_mod_n.connect(leftlegglobalscaleOtpY_plug, noflipleftkneekeyinp_plug)
                self.ctrl_mod_n.connect(leftlegglobalscaleOtpY_plug, noflipleftfootkeyinp_plug)
                self.ctrl_mod_n.connect(leftlegglobalscaleOtpY_plug, pvleftkneekeyinp_plug)
                self.ctrl_mod_n.connect(leftlegglobalscaleOtpY_plug, pvleftfootkeyinp_plug)
                self.ctrl_mod_n.commandToExecute('setAttr "IKNoFlipLeftLegGlobalScale_Average.operation" 2')
                self.ctrl_mod_n.commandToExecute('setAttr "IKNoFlipLeftFootGlobalScale_Average.operation" 2')
                self.ctrl_mod_n.commandToExecute('setAttr "IKLeftLegGlobalScale_Average.operation" 2')
                self.ctrl_mod_n.connect(rootdecomposeOtpScale_plug, ikleftjointleggrps_plug)

                self.ctrl_mod_n.commandToExecute('addAttr -longName "footrollswitch" -niceName "Auto/Manual Foot Roll" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_LeftFootOptions_ctrl')

                self.ctrl_mod_n.commandToExecute('addAttr -longName "autoroll" -niceName "Auto Roll" -attributeType double -minValue -90 -keyable true -defaultValue 0 Biped_IkLeftFoot_ctrl')
                self.ctrl_mod_n.commandToExecute('addAttr -longName "bendlimitangle" -niceName "Bend Limit Angle" -attributeType double -keyable true -defaultValue 45 Biped_IkLeftFoot_ctrl')
                self.ctrl_mod_n.commandToExecute('addAttr -longName "toestraightangle" -niceName "Toe Straight Angle" -attributeType double -keyable true -defaultValue 70 Biped_IkLeftFoot_ctrl')
                self.ctrl_mod_n.commandToExecute('addAttr -longName "heelroll" -niceName "Heel Roll" -attributeType double -keyable true -defaultValue 0 Biped_IkLeftFoot_ctrl')
                self.ctrl_mod_n.doIt()

                likheelclampnode = self.ctrl_mod_n.createNode("clamp")
                self.ctrl_mod_n.renameNode(likheelclampnode, "LeftHeel_rotclamp")
                likheelblendernode = self.ctrl_mod_n.createNode("blendColors")
                self.ctrl_mod_n.renameNode(likheelblendernode, "LeftHeel_blend")
                leg_reverse_sl_ls = om2.MSelectionList()
                leg_reverse_sl_ls.add("LeftReverseFootHeel")
                reverse_heel_obj = leg_reverse_sl_ls.getDependNode(0)

                likheelclamp_fs = om2.MFnDependencyNode(likheelclampnode)
                likheelblender_fs = om2.MFnDependencyNode(likheelblendernode)
                reverseheel_fs = om2.MFnDependencyNode(reverse_heel_obj)

                llegoptionsfootrollswitch_plug = llegoptions_fs.findPlug("footrollswitch", False)
                likheelblender_plug = likheelblender_fs.findPlug("blender", False)
                iklegctrlRoll_plug = iklegctrl_fs.findPlug("autoroll", False)
                likheelclampInpR_plug = likheelclamp_fs.findPlug("inputR", False)
                likheelclampOtpR_plug = likheelclamp_fs.findPlug("outputR", False)
                likheelblendCol2R_plug = likheelblender_fs.findPlug("color2R", False)
                iklegctrlHeelRoll_plug = iklegctrl_fs.findPlug("heelroll", False)
                likheelblendCol1R_plug = likheelblender_fs.findPlug("color1R", False)
                likheelblendOtpR_plug = likheelblender_fs.findPlug("outputR", False)
                likheelclampInpX_plug = reverseheel_fs.findPlug("rotateX", False)

                self.ctrl_mod_n.connect(llegoptionsfootrollswitch_plug, likheelblender_plug)
                self.ctrl_mod_n.connect(iklegctrlRoll_plug, likheelclampInpR_plug)
                self.ctrl_mod_n.connect(likheelclampOtpR_plug, likheelblendCol2R_plug)
                self.ctrl_mod_n.connect(iklegctrlHeelRoll_plug, likheelblendCol1R_plug)
                self.ctrl_mod_n.connect(likheelblendOtpR_plug, likheelclampInpX_plug)
                self.ctrl_mod_n.commandToExecute('setAttr "LeftHeel_rotclamp.minR" -90')

                self.ctrl_mod_n.commandToExecute('addAttr -longName "footroll" -niceName "Foot Roll" -attributeType double -keyable true -defaultValue 0 Biped_IkLeftFoot_ctrl')
                self.ctrl_mod_n.doIt()

                likballclampnode = self.ctrl_mod_n.createNode("clamp")
                self.ctrl_mod_n.renameNode(likballclampnode, "LeftBall_rotclamp")
                likballrangenode = self.ctrl_mod_n.createNode("setRange")
                self.ctrl_mod_n.renameNode(likballrangenode, "LeftBall_range")
                likballblendernode = self.ctrl_mod_n.createNode("blendColors")
                self.ctrl_mod_n.renameNode(likballblendernode, "LeftBall_blend")
                likballminusnode = self.ctrl_mod_n.createNode("plusMinusAverage")
                self.ctrl_mod_n.renameNode(likballminusnode, "LeftBall_minus")
                likballmultnode = self.ctrl_mod_n.createNode("multiplyDivide")
                self.ctrl_mod_n.renameNode(likballmultnode, "LeftBall_percetmult")
                likballrollmultnode = self.ctrl_mod_n.createNode("multiplyDivide")
                self.ctrl_mod_n.renameNode(likballrollmultnode, "LeftBall_rollmult")
                leg_reverse_sl_ls.add("LeftReverseFootToe")
                reverse_toe_obj = leg_reverse_sl_ls.getDependNode(1)

                likballclamp_fs = om2.MFnDependencyNode(likballclampnode)
                likballrange_fs = om2.MFnDependencyNode(likballrangenode)
                likballsub_fs = om2.MFnDependencyNode(likballminusnode)
                likballmult_fs = om2.MFnDependencyNode(likballmultnode)
                likballrollmult_fs = om2.MFnDependencyNode(likballrollmultnode)
                likballblender_fs = om2.MFnDependencyNode(likballblendernode)
                reversetoe_fs = om2.MFnDependencyNode(reverse_toe_obj)

                likballblender_plug = likballblender_fs.findPlug("blender", False)
                likballclampInpR_plug = likballclamp_fs.findPlug("inputR", False)
                likballclampMinR_plug = likballclamp_fs.findPlug("minR", False)
                iklegctrlBendLimit_plug = iklegctrl_fs.findPlug("bendlimitangle", False)
                likballclampMaxR_plug = likballclamp_fs.findPlug("maxR", False)
                likballrangeValueX_plug = likballrange_fs.findPlug("valueX", False)
                likballrangeOldMinX_plug = likballrange_fs.findPlug("oldMinX", False)
                likballrangeOldMaxX_plug = likballrange_fs.findPlug("oldMaxX", False)
                likballrangeOutValueX_plug = likballrange_fs.findPlug("outValueX", False)
                likballmultInp1X_plug = likballmult_fs.findPlug("input1X", False)
                likballmultInp2X_plug = likballmult_fs.findPlug("input2X", False)
                likballmultOtpX_plug = likballmult_fs.findPlug("outputX", False)
                likballsubOtp1D_plug = likballsub_fs.findPlug("output1D", False)
                likballrollmultInp1X_plug = likballrollmult_fs.findPlug("input1X", False)
                likballrollmultInp2X_plug = likballrollmult_fs.findPlug("input2X", False)
                likballrollmultOtpX_plug = likballrollmult_fs.findPlug("outputX", False)
                likballblendCol2R_plug = likballblender_fs.findPlug("color2R", False)
                iklegctrlBallRoll_plug = iklegctrl_fs.findPlug("footroll", False)
                likballblendCol1R_plug = likballblender_fs.findPlug("color1R", False)
                likballblendOtpR_plug = likballblender_fs.findPlug("outputR", False)
                likballclampRotX_plug = reversetoe_fs.findPlug("rotateX", False)

                self.ctrl_mod_n.connect(llegoptionsfootrollswitch_plug, likballblender_plug)
                self.ctrl_mod_n.connect(iklegctrlRoll_plug, likballclampInpR_plug)
                self.ctrl_mod_n.connect(iklegctrlBendLimit_plug, likballclampMaxR_plug)
                self.ctrl_mod_n.connect(likballclampInpR_plug, likballrangeValueX_plug)
                self.ctrl_mod_n.connect(likballclampMinR_plug, likballrangeOldMinX_plug)
                self.ctrl_mod_n.connect(likballclampMaxR_plug, likballrangeOldMaxX_plug)
                self.ctrl_mod_n.connect(likballrangeOutValueX_plug, likballmultInp1X_plug)
                self.ctrl_mod_n.connect(likballsubOtp1D_plug, likballmultInp2X_plug)
                self.ctrl_mod_n.connect(likballmultOtpX_plug, likballrollmultInp1X_plug)
                self.ctrl_mod_n.connect(iklegctrlRoll_plug, likballrollmultInp2X_plug)
                self.ctrl_mod_n.connect(likballrollmultOtpX_plug, likballblendCol2R_plug)
                self.ctrl_mod_n.connect(iklegctrlBallRoll_plug, likballblendCol1R_plug)
                self.ctrl_mod_n.connect(likballblendOtpR_plug, likballclampRotX_plug)
                self.ctrl_mod_n.commandToExecute('setAttr "LeftBall_range.minX" 0')
                self.ctrl_mod_n.commandToExecute('setAttr "LeftBall_range.maxX" 1')
                self.ctrl_mod_n.commandToExecute('setAttr "LeftBall_minus.input1D[0]" 1')
                self.ctrl_mod_n.commandToExecute('setAttr "LeftBall_minus.operation" 2')
                self.ctrl_mod_n.commandToExecute('setAttr "LeftBall_percetmult.operation" 1')
                self.ctrl_mod_n.commandToExecute('setAttr "LeftBall_rollmult.operation" 1')

                self.ctrl_mod_n.commandToExecute('addAttr -longName "toeroll" -niceName "Toe Roll" -attributeType double -keyable true -defaultValue 0 Biped_IkLeftFoot_ctrl')
                self.ctrl_mod_n.doIt()

                liktoeclampnode = self.ctrl_mod_n.createNode("clamp")
                self.ctrl_mod_n.renameNode(liktoeclampnode, "LeftToe_rotclamp")
                liktoeblendernode = self.ctrl_mod_n.createNode("blendColors")
                self.ctrl_mod_n.renameNode(liktoeblendernode, "LeftToe_blend")
                liktoerangernode = self.ctrl_mod_n.createNode("setRange")
                self.ctrl_mod_n.renameNode(liktoerangernode, "LeftToe_range")
                liktoemultnode = self.ctrl_mod_n.createNode("multiplyDivide")
                self.ctrl_mod_n.renameNode(liktoemultnode, "LeftToe_percetmultiply")
                leg_reverse_sl_ls.add("LeftReverseFootToeEnd")
                reverse_toeend_obj = leg_reverse_sl_ls.getDependNode(2)

                liktoeclamp_fs = om2.MFnDependencyNode(liktoeclampnode)
                liktoerange_fs = om2.MFnDependencyNode(liktoerangernode)
                liktoemult_fs = om2.MFnDependencyNode(liktoemultnode)
                liktoeblender_fs = om2.MFnDependencyNode(liktoeblendernode)
                reversetoeend_fs = om2.MFnDependencyNode(reverse_toeend_obj)

                liktoeblender_plug = liktoeblender_fs.findPlug("blender", False)
                iklegctrlStraightLimit_plug = iklegctrl_fs.findPlug("toestraightangle", False)
                liktoeclampInpR_plug = liktoeclamp_fs.findPlug("inputR", False)
                liktoeclampMinR_plug = liktoeclamp_fs.findPlug("minR", False)
                liktoeclampMaxR_plug = liktoeclamp_fs.findPlug("maxR", False)
                liktoerangeValueX_plug = liktoerange_fs.findPlug("valueX", False)
                liktoerangeOldMinX_plug = liktoerange_fs.findPlug("oldMinX", False)
                liktoerangeOldMaxX_plug = liktoerange_fs.findPlug("oldMaxX", False)
                liktoerangeoOutValX_plug = liktoerange_fs.findPlug("outValueX", False)
                liktoemultInp1X_plug = liktoemult_fs.findPlug("input1X", False)
                liktoemultInp2X_plug = liktoemult_fs.findPlug("input2X", False)
                liktoemultOtpX_plug = liktoemult_fs.findPlug("outputX", False)
                liktoeblendCol2R_plug = liktoeblender_fs.findPlug("color2R", False)
                iklegctrlToeRoll_plug = iklegctrl_fs.findPlug("toeroll", False)
                liktoeblendCol1R_plug = liktoeblender_fs.findPlug("color1R", False)
                liktoeblendOtpR_plug = liktoeblender_fs.findPlug("outputR", False)
                liktoeclampRotX_plug = reversetoeend_fs.findPlug("rotateX", False)

                self.ctrl_mod_n.connect(llegoptionsfootrollswitch_plug, liktoeblender_plug)
                self.ctrl_mod_n.connect(iklegctrlRoll_plug, liktoeclampInpR_plug)
                self.ctrl_mod_n.connect(iklegctrlBendLimit_plug, liktoeclampMinR_plug)
                self.ctrl_mod_n.connect(iklegctrlStraightLimit_plug, liktoeclampMaxR_plug)
                self.ctrl_mod_n.connect(liktoeclampInpR_plug, liktoerangeValueX_plug)
                self.ctrl_mod_n.connect(liktoeclampMinR_plug, liktoerangeOldMinX_plug)
                self.ctrl_mod_n.connect(liktoeclampMaxR_plug, liktoerangeOldMaxX_plug)
                self.ctrl_mod_n.connect(liktoerangeoOutValX_plug, liktoemultInp1X_plug)
                self.ctrl_mod_n.connect(liktoeclampInpR_plug, liktoemultInp2X_plug)
                self.ctrl_mod_n.connect(liktoemultOtpX_plug, liktoeblendCol2R_plug)
                self.ctrl_mod_n.commandToExecute('connectAttr -force LeftToe_range.outValueX LeftBall_minus.input1D[1]')
                self.ctrl_mod_n.connect(iklegctrlToeRoll_plug, liktoeblendCol1R_plug)
                self.ctrl_mod_n.connect(liktoeblendOtpR_plug, liktoeclampRotX_plug)
                self.ctrl_mod_n.commandToExecute('setAttr "LeftToe_range.minX" 0')
                self.ctrl_mod_n.commandToExecute('setAttr "LeftToe_range.maxX" 1')
                self.ctrl_mod_n.commandToExecute('setAttr "LeftToe_percetmultiply.operation" 1')

                self.ctrl_mod_n.commandToExecute('addAttr -longName "tilt" -niceName "Tilt" -attributeType double -minValue -180 -maxValue 180 -keyable true -defaultValue 0 Biped_IkLeftFoot_ctrl')
                self.ctrl_mod_n.doIt()

                likinnerlegtiltclampnode = self.ctrl_mod_n.createNode("clamp")
                self.ctrl_mod_n.renameNode(likinnerlegtiltclampnode, "LeftInnerLegTilt_clamp")
                likouterlegtiltclampnode = self.ctrl_mod_n.createNode("clamp")
                self.ctrl_mod_n.renameNode(likouterlegtiltclampnode, "LeftOuterLegTilt_clamp")
                leg_reverse_sl_ls.add("LeftReverseInnerFoot")
                leg_reverse_sl_ls.add("LeftReverseOuterFoot")
                reverse_inner_obj = leg_reverse_sl_ls.getDependNode(3)
                reverse_outer_obj = leg_reverse_sl_ls.getDependNode(4)

                likinnerclamp_fs = om2.MFnDependencyNode(likinnerlegtiltclampnode)
                likouterclamp_fs = om2.MFnDependencyNode(likouterlegtiltclampnode)
                reverseinnerfoot_fs = om2.MFnDependencyNode(reverse_inner_obj)
                reverseouterfoot_fs = om2.MFnDependencyNode(reverse_outer_obj)

                iklegctrlTilt_plug = iklegctrl_fs.findPlug("tilt", False)
                likinnerclampInpB_plug = likinnerclamp_fs.findPlug("inputB", False)
                likouterclampInpB_plug = likouterclamp_fs.findPlug("inputB", False)
                likinnerclampOtpB_plug = likinnerclamp_fs.findPlug("outputB", False)
                likinnerclampRotZ_plug = reverseinnerfoot_fs.findPlug("rotateZ", False)
                likouterclampOtpB_plug = likouterclamp_fs.findPlug("outputB", False)
                likouterclampRotZ_plug = reverseouterfoot_fs.findPlug("rotateZ", False)

                self.ctrl_mod_n.connect(iklegctrlTilt_plug, likinnerclampInpB_plug)
                self.ctrl_mod_n.connect(iklegctrlTilt_plug, likouterclampInpB_plug)
                self.ctrl_mod_n.connect(likinnerclampOtpB_plug, likinnerclampRotZ_plug)
                self.ctrl_mod_n.connect(likouterclampOtpB_plug, likouterclampRotZ_plug)
                self.ctrl_mod_n.commandToExecute('setAttr "LeftInnerLegTilt_clamp.maxB" 180')
                self.ctrl_mod_n.commandToExecute('setAttr "LeftOuterLegTilt_clamp.minB" -180')

                self.ctrl_mod_n.commandToExecute('addAttr -longName "lean" -niceName "Lean" -attributeType double -keyable true -defaultValue 0 Biped_IkLeftFoot_ctrl')
                self.ctrl_mod_n.commandToExecute('addAttr -longName "toespin" -niceName "Toe Spin" -attributeType double -keyable true -defaultValue 0 Biped_IkLeftFoot_ctrl')
                self.ctrl_mod_n.commandToExecute('addAttr -longName "toewiggle" -niceName "Toe Wiggle" -attributeType double -keyable true -defaultValue 0 Biped_IkLeftFoot_ctrl')
                self.ctrl_mod_n.doIt()

                leg_reverse_sl_ls.add("LeftReverseFootToeWiggle")
                reverse_toewiggle_obj = leg_reverse_sl_ls.getDependNode(5)

                reversetoewiggle_fs = om2.MFnDependencyNode(reverse_toewiggle_obj)

                iklegctrlLean_plug = iklegctrl_fs.findPlug("lean", False)
                likballclampRotZ_plug = reversetoe_fs.findPlug("rotateZ", False)
                iklegctrlToeSpin_plug = iklegctrl_fs.findPlug("toespin", False)
                liktoeclampRotY_plug = reversetoeend_fs.findPlug("rotateY", False)
                iklegctrlToeWiggle_plug = iklegctrl_fs.findPlug("toewiggle", False)
                reversetoewiggleRotX_plug = reversetoewiggle_fs.findPlug("rotateX", False)

                self.ctrl_mod_n.connect(iklegctrlLean_plug, likballclampRotZ_plug)
                self.ctrl_mod_n.connect(iklegctrlToeSpin_plug, liktoeclampRotY_plug)
                self.ctrl_mod_n.connect(iklegctrlToeWiggle_plug, reversetoewiggleRotX_plug)
        else:
            self.ctrl_mod_n.commandToExecute('delete "Biped_IkLeftFoot_null"')
            self.ctrl_mod_n.commandToExecute('setAttr -keyable false -channelBox false Biped_LeftFootOptions_ctrl.fkik')
            self.ctrl_mod_n.commandToExecute('setAttr "IkLeftUpLeg.visibility" 0')

        for index in range(fkrarm_sl_ls.length()):
            jnt_obj = fkrarm_sl_ls.getDependNode(index)
            jnt_string = fkrarm_sl_ls.getSelectionStrings(index)

            if jnt_obj.hasFn(om2.MFn.kJoint):
                rarmctrl_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
                rarmctrl_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                self.ctrl_mod_n.renameNode(rarmctrl_multMatrix, str(jnt_string)[2:][:-3]+"_multMatrix")
                self.ctrl_mod_n.renameNode(rarmctrl_decomposeMatrix, str(jnt_string)[2:][:-3]+"_decomposeMatrix")

                rarmmultMatrix_fs = om2.MFnDependencyNode(rarmctrl_multMatrix)
                rarmdecomposeMatrix_fs = om2.MFnDependencyNode(rarmctrl_decomposeMatrix)
                rarmjnt_fs = om2.MFnDependencyNode(jnt_obj)

                rarmmultMatrixSum_plug = rarmmultMatrix_fs.findPlug("matrixSum", False)
                rarmdecomposeInpMatrix_plug = rarmdecomposeMatrix_fs.findPlug("inputMatrix", False)
                rarmdecomposeOtpTrans_plug = rarmdecomposeMatrix_fs.findPlug("outputTranslate", False)
                rarmdecomposeOtpRot_plug = rarmdecomposeMatrix_fs.findPlug("outputRotate", False)
                rarmjntTrans_plug = rarmjnt_fs.findPlug("translate", False)
                rarmjntRot_plug = rarmjnt_fs.findPlug("rotate", False)

                self.ctrl_mod_n.commandToExecute('connectAttr -force Biped_{0}_ctrl.worldMatrix[0] {0}_multMatrix.matrixIn[0]'.format(str(jnt_string)[3:][:-3]))
                self.ctrl_mod_n.commandToExecute('connectAttr -force {0}.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(jnt_string)[3:][:-3]))
                self.ctrl_mod_n.connect(rarmmultMatrixSum_plug, rarmdecomposeInpMatrix_plug)
                self.ctrl_mod_n.connect(rarmdecomposeOtpTrans_plug, rarmjntTrans_plug)
                self.ctrl_mod_n.connect(rarmdecomposeOtpRot_plug, rarmjntRot_plug)
                if cmds.getAttr("{0}.jointOrientX".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientY".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientZ".format(str(jnt_string)[3:][:-3])) != 0:
                    self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientX" 0'.format(str(jnt_string)[3:][:-3]))
                    self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientY" 0'.format(str(jnt_string)[3:][:-3]))
                    self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientZ" 0'.format(str(jnt_string)[3:][:-3]))

        fkrarm_sl_ls = om2.MSelectionList()
        fkrarm_sl_ls.add("FkRightArm")
        fkrarm_sl_ls.add("FkRightForeArm")
        fkrarm_sl_ls.add("FkRightHand")

        ikrarm_sl_ls = om2.MSelectionList()
        ikrarm_sl_ls.add("IkRightArm")
        ikrarm_sl_ls.add("IkRightForeArm")
        ikrarm_sl_ls.add("IkRightHand")

        rhandoptions_sl_ls = om2.MSelectionList()
        rhandoptions_sl_ls.add("Biped_RightHandOptions_ctrl")
        rhandoptions_obj = rhandoptions_sl_ls.getDependNode(0)

        self.ctrl_mod_n.commandToExecute('addAttr -longName "fkik" -niceName "Fk/Ik" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_RightHandOptions_ctrl')
        self.ctrl_mod_n.doIt()

        rhandoptions_fs = om2.MFnDependencyNode(rhandoptions_obj)
        rhandoptionsfkik_plug = rhandoptions_fs.findPlug("fkik", False)

        for index in range(rarm_sl_ls.length()):
            fkjnt_obj = fkrarm_sl_ls.getDependNode(index)

            ikjnt_obj = ikrarm_sl_ls.getDependNode(index)
            ikjnt_string = ikrarm_sl_ls.getSelectionStrings(index)

            bindjnt_obj = rarm_sl_ls.getDependNode(index)
            bindjnt_string = rarm_sl_ls.getSelectionStrings(index)

            if bindjnt_obj.hasFn(om2.MFn.kJoint):
                if cmds.getAttr("{0}.jointOrientX".format(str(bindjnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientY".format(str(bindjnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientZ".format(str(bindjnt_string)[3:][:-3])) != 0:
                    jointort_xattr = cmds.getAttr("{0}.jointOrientX".format(str(bindjnt_string)[3:][:-3]))
                    jointort_yattr = cmds.getAttr("{0}.jointOrientY".format(str(bindjnt_string)[3:][:-3]))
                    jointort_zattr = cmds.getAttr("{0}.jointOrientZ".format(str(bindjnt_string)[3:][:-3]))

                    cmds.setAttr("{0}.rotateX".format(str(bindjnt_string)[3:][:-3]), jointort_xattr)
                    cmds.setAttr("{0}.rotateY".format(str(bindjnt_string)[3:][:-3]), jointort_yattr)
                    cmds.setAttr("{0}.rotateZ".format(str(bindjnt_string)[3:][:-3]), jointort_zattr)

                    cmds.setAttr("{0}.jointOrientX".format(str(bindjnt_string)[3:][:-3]), 0)
                    cmds.setAttr("{0}.jointOrientY".format(str(bindjnt_string)[3:][:-3]), 0)
                    cmds.setAttr("{0}.jointOrientZ".format(str(bindjnt_string)[3:][:-3]), 0)

                armjoint_fs = om2.MFnDependencyNode(bindjnt_obj)
                fkarmjoint_fs = om2.MFnDependencyNode(fkjnt_obj)

                fkarmjointrototp_plug = fkarmjoint_fs.findPlug("rotate", False)
                armjointrotinp_plug = armjoint_fs.findPlug("rotate", False)

                if cmds.objExists("RightHand_Ik"):
                    armblendnode = self.ctrl_mod_n.createNode("blendColors")
                    armjoint_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                    self.ctrl_mod_n.renameNode(armjoint_decomposeMatrix, str(bindjnt_string)[2:][:-3]+"Blend_decomposeMatrix")
                    self.ctrl_mod_n.renameNode(armblendnode, str(bindjnt_string)[2:][:-3]+"_blend")

                    armblendnode_fs = om2.MFnDependencyNode(armblendnode)
                    armdecomposeMatrix_fs = om2.MFnDependencyNode(armjoint_decomposeMatrix)
                    ikarmjoint_fs = om2.MFnDependencyNode(ikjnt_obj)

                    armdecomposeInpMatrix_plug = armdecomposeMatrix_fs.findPlug("inputMatrix", False)
                    armdecomposeOtpRot_plug = armdecomposeMatrix_fs.findPlug("outputRotate", False)
                    armblendnodeinp1_plug = armblendnode_fs.findPlug("color1", False)
                    armblendnodeinp2_plug = armblendnode_fs.findPlug("color2", False)
                    armblendnodeotp_plug = armblendnode_fs.findPlug("output", False)
                    armblendnodeblender_plug = armblendnode_fs.findPlug("blender", False)
                    ikarmjointrototp_plug = ikarmjoint_fs.findPlug("matrix", False)

                    self.ctrl_mod_n.connect(ikarmjointrototp_plug, armdecomposeInpMatrix_plug)
                    self.ctrl_mod_n.connect(armdecomposeOtpRot_plug, armblendnodeinp1_plug)
                    self.ctrl_mod_n.connect(fkarmjointrototp_plug, armblendnodeinp2_plug)
                    self.ctrl_mod_n.connect(armblendnodeotp_plug, armjointrotinp_plug)
                    self.ctrl_mod_n.connect(rhandoptionsfkik_plug, armblendnodeblender_plug)

                else:
                    self.ctrl_mod_n.connect(fkarmjointrototp_plug, armjointrotinp_plug)
                    self.ctrl_mod_n.commandToExecute('setAttr -keyable false -channelBox false Biped_RightHandOptions_ctrl.fkik')
                    self.ctrl_mod_n.commandToExecute('setAttr "IkRightArm.visibility" 0')

        if cmds.objExists("RightHand_Ik"):
            rhandik_sl_ls = om2.MSelectionList()
            rhandik_sl_ls.add("RightHand_Ik")
            rikhandobj_fs = om2.MFnDependencyNode(rhandik_sl_ls.getDependNode(0))
            rikhand_fs = om2.MFnDependencyNode(ikrarm_sl_ls.getDependNode(2))

            if self.typeofRHandIK.currentIndex() == 1 or 2:
                rikhandctrl_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
                rikhandctrl_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                rikhandrot_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
                rikhandrot_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                self.ctrl_mod_n.renameNode(rikhandctrl_multMatrix, "IkRightHand_multMatrix")
                self.ctrl_mod_n.renameNode(rikhandctrl_decomposeMatrix, "IkRightHand_decomposeMatrix")
                self.ctrl_mod_n.renameNode(rikhandrot_multMatrix, "IkRightHandRot_multMatrix")
                self.ctrl_mod_n.renameNode(rikhandrot_decomposeMatrix, "IkRightHandRot_decomposeMatrix")

                rikhandmultMatrix_fs = om2.MFnDependencyNode(rikhandctrl_multMatrix)
                rikhanddecomposeMatrix_fs = om2.MFnDependencyNode(rikhandctrl_decomposeMatrix)
                rikhandrotmultMatrix_fs = om2.MFnDependencyNode(rikhandrot_multMatrix)
                rikhandrotdecomposeMatrix_fs = om2.MFnDependencyNode(rikhandrot_decomposeMatrix)

                rikhandmultMatrixSum_plug = rikhandmultMatrix_fs.findPlug("matrixSum", False)
                rikhanddecomposeInpMatrix_plug = rikhanddecomposeMatrix_fs.findPlug("inputMatrix", False)
                rikhanddecomposeOtpTrans_plug = rikhanddecomposeMatrix_fs.findPlug("outputTranslate", False)
                rikhanddecomposeOtpRot_plug = rikhanddecomposeMatrix_fs.findPlug("outputRotate", False)
                rikhandrotmultMatrixSum_plug = rikhandrotmultMatrix_fs.findPlug("matrixSum", False)
                rikhandrotdecomposeInpMatrix_plug = rikhandrotdecomposeMatrix_fs.findPlug("inputMatrix", False)
                rikhandrotdecomposeOtpRot_plug = rikhandrotdecomposeMatrix_fs.findPlug("outputRotate", False)
                rikhandjntTrans_plug = rikhandobj_fs.findPlug("translate", False)
                rikhandjntRot_plug = rikhandobj_fs.findPlug("rotate", False)
                rikhandRot_plug = rikhand_fs.findPlug("rotate", False)

                self.ctrl_mod_n.commandToExecute('connectAttr -force Biped_IkRightHand_ctrl.worldMatrix[0] IkRightHand_multMatrix.matrixIn[0]')
                self.ctrl_mod_n.commandToExecute('connectAttr -force RightHand_Ik.parentInverseMatrix[0] IkRightHand_multMatrix.matrixIn[1]')
                self.ctrl_mod_n.commandToExecute('connectAttr -force Biped_IkRightHand_ctrl.worldMatrix[0] IkRightHandRot_multMatrix.matrixIn[0]')
                self.ctrl_mod_n.commandToExecute('connectAttr -force IkRightHand.parentInverseMatrix[0] IkRightHandRot_multMatrix.matrixIn[1]')
                self.ctrl_mod_n.connect(rikhandmultMatrixSum_plug, rikhanddecomposeInpMatrix_plug)
                self.ctrl_mod_n.connect(rikhanddecomposeOtpTrans_plug, rikhandjntTrans_plug)
                self.ctrl_mod_n.connect(rikhanddecomposeOtpRot_plug, rikhandjntRot_plug)
                self.ctrl_mod_n.connect(rikhandrotmultMatrixSum_plug, rikhandrotdecomposeInpMatrix_plug)
                self.ctrl_mod_n.connect(rikhandrotdecomposeOtpRot_plug, rikhandRot_plug)

        else:
            self.ctrl_mod_n.commandToExecute('delete "Biped_IkRightHand_null"')
            self.ctrl_mod_n.commandToExecute('setAttr -keyable false -channelBox false Biped_RightHandOptions_ctrl.fkik')
            self.ctrl_mod_n.commandToExecute('setAttr "IkRightArm.visibility" 0')

        rfinger_sl_ls = om2.MSelectionList()
        rfinger_sl_ls.add("RightFinger*")
        for index in range(rfinger_sl_ls.length()):
            jnt_obj = rfinger_sl_ls.getDependNode(index)
            jnt_string = rfinger_sl_ls.getSelectionStrings(index)

            if jnt_obj.hasFn(om2.MFn.kJoint):
                rfingerctrl_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
                rfingerctrl_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                self.ctrl_mod_n.renameNode(rfingerctrl_multMatrix, str(jnt_string)[2:][:-3]+"_multMatrix")
                self.ctrl_mod_n.renameNode(rfingerctrl_decomposeMatrix, str(jnt_string)[2:][:-3]+"_decomposeMatrix")

                rfingermultMatrix_fs = om2.MFnDependencyNode(rfingerctrl_multMatrix)
                rfingerdecomposeMatrix_fs = om2.MFnDependencyNode(rfingerctrl_decomposeMatrix)
                rfingerjnt_fs = om2.MFnDependencyNode(jnt_obj)

                rfingermultMatrixSum_plug = rfingermultMatrix_fs.findPlug("matrixSum", False)
                rfingerdecomposeInpMatrix_plug = rfingerdecomposeMatrix_fs.findPlug("inputMatrix", False)
                rfingerdecomposeOtpTrans_plug = rfingerdecomposeMatrix_fs.findPlug("outputTranslate", False)
                rfingerdecomposeOtpRot_plug = rfingerdecomposeMatrix_fs.findPlug("outputRotate", False)
                rfingerjntTrans_plug = rfingerjnt_fs.findPlug("translate", False)
                rfingerjntRot_plug = rfingerjnt_fs.findPlug("rotate", False)

                self.ctrl_mod_n.commandToExecute('connectAttr -force Biped_{0}_ctrl.worldMatrix[0] {0}_multMatrix.matrixIn[0]'.format(str(jnt_string)[3:][:-3]))
                self.ctrl_mod_n.commandToExecute('connectAttr -force {0}.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(jnt_string)[3:][:-3]))
                self.ctrl_mod_n.connect(rfingermultMatrixSum_plug, rfingerdecomposeInpMatrix_plug)
                self.ctrl_mod_n.connect(rfingerdecomposeOtpTrans_plug, rfingerjntTrans_plug)
                self.ctrl_mod_n.connect(rfingerdecomposeOtpRot_plug, rfingerjntRot_plug)
                self.ctrl_mod_n.connect(lfingerdecomposeOtpRot_plug, lfingerjntRot_plug)
                if cmds.getAttr("{0}.jointOrientX".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientY".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientZ".format(str(jnt_string)[3:][:-3])) != 0:
                    self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientX" 0'.format(str(jnt_string)[3:][:-3]))
                    self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientY" 0'.format(str(jnt_string)[3:][:-3]))
                    self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientZ" 0'.format(str(jnt_string)[3:][:-3]))

                if cmds.objExists("Biped_{0}4_ctrl".format(str(jnt_string)[3:][:-4])):
                    self.ctrl_mod_n.commandToExecute('setAttr "Biped_{0}4_ctrl.visibility" 0'.format(str(jnt_string)[3:][:-4]))

        rfingergrp_sl_ls = om2.MSelectionList()
        rfingergrp_sl_ls.add("Biped_RightFingers_null")
        grp_obj = rfingergrp_sl_ls.getDependNode(0)

        rfingergrp_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
        rfingergrp_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
        self.ctrl_mod_n.renameNode(rfingergrp_multMatrix, "RightFingers_multMatrix")
        self.ctrl_mod_n.renameNode(rfingergrp_decomposeMatrix, "RightFingers_decomposeMatrix")

        rfingergrpmultMatrix_fs = om2.MFnDependencyNode(rfingergrp_multMatrix)
        rfingergrpdecomposeMatrix_fs = om2.MFnDependencyNode(rfingergrp_decomposeMatrix)
        rfingergrp_fs = om2.MFnDependencyNode(grp_obj)

        rfingergrpmultMatrixSum_plug = rfingergrpmultMatrix_fs.findPlug("matrixSum", False)
        rfingergrpdecomposeInpMatrix_plug = rfingergrpdecomposeMatrix_fs.findPlug("inputMatrix", False)
        rfingergrpdecomposeOtpTrans_plug = rfingergrpdecomposeMatrix_fs.findPlug("outputTranslate", False)
        rfingergrpdecomposeOtpRot_plug = rfingergrpdecomposeMatrix_fs.findPlug("outputRotate", False)
        rfingergrpjntTrans_plug = rfingergrp_fs.findPlug("translate", False)
        rfingergrpjntRot_plug = rfingergrp_fs.findPlug("rotate", False)

        self.ctrl_mod_n.commandToExecute('connectAttr -force RightHand.worldMatrix[0] RightFingers_multMatrix.matrixIn[0]')
        self.ctrl_mod_n.commandToExecute('connectAttr -force Biped_RightFingers_null.parentInverseMatrix[0] RightFingers_multMatrix.matrixIn[1]')
        self.ctrl_mod_n.connect(rfingergrpmultMatrixSum_plug, rfingergrpdecomposeInpMatrix_plug)
        self.ctrl_mod_n.connect(rfingergrpdecomposeOtpTrans_plug, rfingergrpjntTrans_plug)
        self.ctrl_mod_n.connect(rfingergrpdecomposeOtpRot_plug, rfingergrpjntRot_plug)

        ikrleg_sl_ls = om2.MSelectionList()
        ikrleg_sl_ls.add("IkRightUpLeg")
        ikrleg_sl_ls.add("IkRightLeg")
        ikrleg_sl_ls.add("IkRightFoot")
        ikrleg_sl_ls.add("IkRightToeBase")

        rlegoptions_sl_ls = om2.MSelectionList()
        rlegoptions_sl_ls.add("Biped_RightFootOptions_ctrl")
        rlegoptions_obj = rlegoptions_sl_ls.getDependNode(0)

        self.ctrl_mod_n.commandToExecute('addAttr -longName "fkik" -niceName "Fk/Ik" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_RightFootOptions_ctrl')
        self.ctrl_mod_n.doIt()

        rlegoptions_fs = om2.MFnDependencyNode(rlegoptions_obj)
        rlegoptionsfkik_plug = rlegoptions_fs.findPlug("fkik", False)

        for index in range(fkrleg_sl_ls.length()):
            jnt_obj = fkrleg_sl_ls.getDependNode(index)
            jnt_string = fkrleg_sl_ls.getSelectionStrings(index)

            ikjnt_obj = ikrleg_sl_ls.getDependNode(index)
            ikjnt_string = ikrleg_sl_ls.getSelectionStrings(index)

            bindjnt_obj = rleg_sl_ls.getDependNode(index)
            bindjnt_string = rleg_sl_ls.getSelectionStrings(index)

            if jnt_obj.hasFn(om2.MFn.kJoint):
                rlegctrl_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
                rlegctrl_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                self.ctrl_mod_n.renameNode(rlegctrl_multMatrix, str(jnt_string)[2:][:-3]+"_multMatrix")
                self.ctrl_mod_n.renameNode(rlegctrl_decomposeMatrix, str(jnt_string)[2:][:-3]+"_decomposeMatrix")

                rlegmultMatrix_fs = om2.MFnDependencyNode(rlegctrl_multMatrix)
                rlegdecomposeMatrix_fs = om2.MFnDependencyNode(rlegctrl_decomposeMatrix)
                rlegjnt_fs = om2.MFnDependencyNode(jnt_obj)

                rlegmultMatrixSum_plug = rlegmultMatrix_fs.findPlug("matrixSum", False)
                rlegdecomposeInpMatrix_plug = rlegdecomposeMatrix_fs.findPlug("inputMatrix", False)
                rlegdecomposeOtpTrans_plug = rlegdecomposeMatrix_fs.findPlug("outputTranslate", False)
                rlegdecomposeOtpRot_plug = rlegdecomposeMatrix_fs.findPlug("outputRotate", False)
                rlegjntTrans_plug = rlegjnt_fs.findPlug("translate", False)
                rlegjntRot_plug = rlegjnt_fs.findPlug("rotate", False)

                self.ctrl_mod_n.commandToExecute('connectAttr -force Biped_{0}_ctrl.worldMatrix[0] {0}_multMatrix.matrixIn[0]'.format(str(jnt_string)[3:][:-3]))
                self.ctrl_mod_n.commandToExecute('connectAttr -force {0}.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(jnt_string)[3:][:-3]))
                self.ctrl_mod_n.connect(rlegmultMatrixSum_plug, rlegdecomposeInpMatrix_plug)
                self.ctrl_mod_n.connect(rlegdecomposeOtpTrans_plug, rlegjntTrans_plug)
                self.ctrl_mod_n.connect(rlegdecomposeOtpRot_plug, rlegjntRot_plug)
                self.ctrl_mod_n.connect(lfingerdecomposeOtpRot_plug, lfingerjntRot_plug)

                if cmds.getAttr("{0}.jointOrientX".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientY".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientZ".format(str(jnt_string)[3:][:-3])) != 0:
                    self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientX" 0'.format(str(jnt_string)[3:][:-3]))
                    self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientY" 0'.format(str(jnt_string)[3:][:-3]))
                    self.ctrl_mod_n.commandToExecute('setAttr "{0}.jointOrientZ" 0'.format(str(jnt_string)[3:][:-3]))

            if bindjnt_obj.hasFn(om2.MFn.kJoint):
                if cmds.getAttr("{0}.jointOrientX".format(str(bindjnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientY".format(str(bindjnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientZ".format(str(bindjnt_string)[3:][:-3])) != 0:
                    jointort_xattr = cmds.getAttr("{0}.jointOrientX".format(str(bindjnt_string)[3:][:-3]))
                    jointort_yattr = cmds.getAttr("{0}.jointOrientY".format(str(bindjnt_string)[3:][:-3]))
                    jointort_zattr = cmds.getAttr("{0}.jointOrientZ".format(str(bindjnt_string)[3:][:-3]))

                    cmds.setAttr("{0}.rotateX".format(str(bindjnt_string)[3:][:-3]), jointort_xattr)
                    cmds.setAttr("{0}.rotateY".format(str(bindjnt_string)[3:][:-3]), jointort_yattr)
                    cmds.setAttr("{0}.rotateZ".format(str(bindjnt_string)[3:][:-3]), jointort_zattr)

                    cmds.setAttr("{0}.jointOrientX".format(str(bindjnt_string)[3:][:-3]), 0)
                    cmds.setAttr("{0}.jointOrientY".format(str(bindjnt_string)[3:][:-3]), 0)
                    cmds.setAttr("{0}.jointOrientZ".format(str(bindjnt_string)[3:][:-3]), 0)

                legjoint_fs = om2.MFnDependencyNode(bindjnt_obj)
                fklegjoint_fs = om2.MFnDependencyNode(jnt_obj)

                legjointrotinp_plug = legjoint_fs.findPlug("rotate", False)
                fklegjointrototp_plug = fklegjoint_fs.findPlug("rotate", False)

                if cmds.objExists("RightLeg_Ik"):
                    legrotblendnode = self.ctrl_mod_n.createNode("blendColors")
                    legjoint_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                    self.ctrl_mod_n.renameNode(legjoint_decomposeMatrix, str(bindjnt_string)[2:][:-3]+"Blend_decomposeMatrix")
                    self.ctrl_mod_n.renameNode(legrotblendnode, str(bindjnt_string)[2:][:-3]+"_blend")

                    legrotblendnode_fs = om2.MFnDependencyNode(legrotblendnode)
                    legdecomposeMatrix_fs = om2.MFnDependencyNode(legjoint_decomposeMatrix)
                    iklegjoint_fs = om2.MFnDependencyNode(ikjnt_obj)

                    nofliplegdecomposeInpMatrix_plug = legdecomposeMatrix_fs.findPlug("inputMatrix", False)
                    nofliplegdecomposeOtpRot_plug = legdecomposeMatrix_fs.findPlug("outputRotate", False)
                    legrotblendnodeinp1_plug = legrotblendnode_fs.findPlug("color1", False)
                    legrotblendnodeinp2_plug = legrotblendnode_fs.findPlug("color2", False)
                    legrotblendnodeotp_plug = legrotblendnode_fs.findPlug("output", False)
                    legrotblendnodeblender_plug = legrotblendnode_fs.findPlug("blender", False)
                    iklegjointotp_plug = iklegjoint_fs.findPlug("matrix", False)

                    self.ctrl_mod_n.connect(iklegjointotp_plug, nofliplegdecomposeInpMatrix_plug)
                    self.ctrl_mod_n.connect(nofliplegdecomposeOtpRot_plug, legrotblendnodeinp1_plug)
                    self.ctrl_mod_n.connect(fklegjointrototp_plug, legrotblendnodeinp2_plug)
                    self.ctrl_mod_n.connect(legrotblendnodeotp_plug, legjointrotinp_plug)
                    self.ctrl_mod_n.connect(rlegoptionsfkik_plug, legrotblendnodeblender_plug)

                else:
                    self.ctrl_mod_n.connect(fklegjointrototp_plug, legjointrotinp_plug)

        if cmds.objExists("RightLeg_Ik"):
            rlegik_sl_ls = om2.MSelectionList()
            rlegik_sl_ls.add("RightLeg_Ik")
            riklegobj_fs = om2.MFnDependencyNode(rlegik_sl_ls.getDependNode(0))

            if self.typeofRLegIK.currentIndex() == 1 or 2:
                riklegctrl_multMatrix = self.ctrl_mod_n.createNode("multMatrix")
                riklegctrl_decomposeMatrix = self.ctrl_mod_n.createNode("decomposeMatrix")
                self.ctrl_mod_n.renameNode(riklegctrl_multMatrix, "IkRightLegCtrl_multMatrix")
                self.ctrl_mod_n.renameNode(riklegctrl_decomposeMatrix, "IkRightLegCtrl_decomposeMatrix")

                riklegmultMatrix_fs = om2.MFnDependencyNode(riklegctrl_multMatrix)
                riklegdecomposeMatrix_fs = om2.MFnDependencyNode(riklegctrl_decomposeMatrix)

                riklegmultMatrixSum_plug = riklegmultMatrix_fs.findPlug("matrixSum", False)
                riklegdecomposeInpMatrix_plug = riklegdecomposeMatrix_fs.findPlug("inputMatrix", False)
                riklegdecomposeOtpTrans_plug = riklegdecomposeMatrix_fs.findPlug("outputTranslate", False)
                riklegdecomposeOtpRot_plug = riklegdecomposeMatrix_fs.findPlug("outputRotate", False)
                riklegjntTrans_plug = riklegobj_fs.findPlug("translate", False)
                riklegjntRot_plug = riklegobj_fs.findPlug("rotate", False)

                self.ctrl_mod_n.commandToExecute('connectAttr -force Biped_IkRightFoot_ctrl.worldMatrix[0] IkRightLegCtrl_multMatrix.matrixIn[0]')
                self.ctrl_mod_n.commandToExecute('connectAttr -force RightLeg_Ik.parentInverseMatrix[0] IkRightLegCtrl_multMatrix.matrixIn[1]')
                self.ctrl_mod_n.connect(riklegmultMatrixSum_plug, riklegdecomposeInpMatrix_plug)
                self.ctrl_mod_n.connect(riklegdecomposeOtpTrans_plug, riklegjntTrans_plug)
                self.ctrl_mod_n.connect(riklegdecomposeOtpRot_plug, riklegjntRot_plug)
                self.ctrl_mod_n.commandToExecute('parent RightLegFoot_Ik Biped_IkRightFoot_ctrl')
                self.ctrl_mod_n.commandToExecute('parent RightLegToe_Ik Biped_IkRightFoot_ctrl')
                self.ctrl_mod_n.doIt()

        else:
            self.ctrl_mod_n.commandToExecute('delete "Biped_IkRightFoot_null"')
            self.ctrl_mod_n.commandToExecute('setAttr -keyable false -channelBox false Biped_RightFootOptions_ctrl.fkik')
            self.ctrl_mod_n.commandToExecute('setAttr "IkRightUpLeg.visibility" 0')

        # jntort_sl_ls = om1.MSelectionList()
        # jntort_sl_ls.add("Left*")
        # jntort_sl_ls.add("IkLeft*")
        # jntort_sl_ls.add("FkLeft*")
        # jntort_sl_ls.add("Right*")
        # jntort_sl_ls.add("IkRight*")
        # jntort_sl_ls.add("FkRight*")
        # jntort_sl_ls.add("Spine*")
        # jntort_sl_ls.add("Neck*")
        # jntort_sl_ls.add("Head*")
        #
        # jnt_obj = om1.MObject()
        #
        # for index in range(jntort_sl_ls.length()):
        #     jntort_sl_ls.getDependNode(index, jnt_obj)
        #     jntort_value = om1.MEulerRotation(om1.MVector(0.0, 0.0, 0.0), 1)
        #     if jnt_obj.hasFn(om1.MFn.kJoint):
        #         print(jnt_obj)
        #         jnt_fn = omanim1.MFnIkJoint(jnt_obj)
        #         jnt_fn.setOrientation(jntort_value)

        self.ctrl_mod_n.commandToExecute('delete "Draw*"')
        self.ctrl_mod_n.doIt()

    def deleteRig(self):
        rig_mod_n = om2.MDGModifier()
        rig_mod_n.commandToExecute('delete "Biped*"')
        rig_mod_n.commandToExecute('delete "*Matrix*"')
        rig_mod_n.commandToExecute('delete "BackBone*"')
        rig_mod_n.commandToExecute('delete "Neck*"')
        rig_mod_n.commandToExecute('delete "*Left*"')
        rig_mod_n.commandToExecute('delete "NoFlip*"')
        rig_mod_n.commandToExecute('delete "PV*"')
        rig_mod_n.doIt()

try:
    display_dailog.close()
    display_dailog.deleteLater()
except:
    pass

display_dailog = MainWindow()
display_dailog.show()

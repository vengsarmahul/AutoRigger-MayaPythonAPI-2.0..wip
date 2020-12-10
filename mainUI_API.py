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

        self.MDG1_mod = om1.MDGModifier()
        self.IK_System = omanim1.MIkSystem()
        self.IK_Effector = omanim1.MFnIkEffector()
        self.IK_Handle = omanim1.MFnIkHandle()
        self.MDag_path = om1.MDagPath()
        self.MNurbs1_cv = om1.MFnNurbsCurve()
        self.IKSolver1_lst = om1.MSelectionList()

        self.MDG2_mod = om2.MDGModifier()
        self.MDag2_node = om2.MFnDagNode()
        self.MNurbs2_cv = om2.MFnNurbsCurve()

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

        self.hipjnt = QtWidgets.QComboBox()
        self.hipjnt.addItems(["No", "Yes"])

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

        form_layout_8 = QtWidgets.QFormLayout()
        form_layout_8.addRow("Include Hip-Controller", self.hipjnt)

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

        opt_HorizonLayout = QtWidgets.QHBoxLayout()
        opt_HorizonLayout.addLayout(form_layout_7)
        opt_HorizonLayout.addLayout(form_layout_8)

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
        mainLayoutV.addLayout(opt_HorizonLayout)
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
            self.splineik_grp = spinejnt_grp.create("transform", "SplineIk_grp", self.jnt_grp)
            self.jnt_root_tn = spinejnt_grp.create("joint", "Root", self.jnt_grp)
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

        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "DoNotTouch.translateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "DoNotTouch.translateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "DoNotTouch.translateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "DoNotTouch.rotateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "DoNotTouch.rotateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "DoNotTouch.rotateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "DoNotTouch.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "DoNotTouch.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "DoNotTouch.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "DoNotTouch.visibility" 0')
        self.MDG2_mod.commandToExecute('select -hierarchy "DoNotTouch"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('select -hierarchy "IkHip"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('select -hierarchy "IkNeck0"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('select -hierarchy "FkLeftArm"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('select -hierarchy "IkLeftArm"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('select -hierarchy "IkNoFlipLeftArm"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('select -hierarchy "IkPVLeftArm"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('select -hierarchy "LeftArmIk_grp"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "IkStretchyLeftJointArm_grp.translateX"')
        self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "IkStretchyLeftJointArm_grp.translateY"')
        self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "IkStretchyLeftJointArm_grp.translateZ"')
        self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "IkStretchyLeftJointArm_grp.rotateX"')
        self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "IkStretchyLeftJointArm_grp.rotateY"')
        self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "IkStretchyLeftJointArm_grp.rotateZ"')
        self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "IkStretchyLeftJointArm_grp.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "IkStretchyLeftJointArm_grp.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "IkStretchyLeftJointArm_grp.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "IkStretchyLeftJointArm_grp.visibility" 0')
        self.MDG2_mod.commandToExecute('select -hierarchy "IkStretchyLeftJointArm_grp"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "FkLeftJointLeg_grp.translateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "FkLeftJointLeg_grp.translateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "FkLeftJointLeg_grp.translateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "FkLeftJointLeg_grp.rotateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "FkLeftJointLeg_grp.rotateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "FkLeftJointLeg_grp.rotateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "FkLeftJointLeg_grp.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "FkLeftJointLeg_grp.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "FkLeftJointLeg_grp.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "FkLeftJointLeg_grp.visibility" 0')
        self.MDG2_mod.commandToExecute('select -hierarchy "FkLeftJointLeg_grp"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkLeftJointLeg_grp.translateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkLeftJointLeg_grp.translateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkLeftJointLeg_grp.translateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkLeftJointLeg_grp.rotateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkLeftJointLeg_grp.rotateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkLeftJointLeg_grp.rotateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkLeftJointLeg_grp.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkLeftJointLeg_grp.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkLeftJointLeg_grp.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkLeftJointLeg_grp.visibility" 0')
        self.MDG2_mod.commandToExecute('select -hierarchy "IkLeftJointLeg_grp"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "LeftLegIk_grp.translateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "LeftLegIk_grp.translateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "LeftLegIk_grp.translateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "LeftLegIk_grp.rotateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "LeftLegIk_grp.rotateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "LeftLegIk_grp.rotateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "LeftLegIk_grp.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "LeftLegIk_grp.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "LeftLegIk_grp.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "LeftLegIk_grp.visibility" 0')
        self.MDG2_mod.commandToExecute('select -hierarchy "LeftLegIk_grp"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkStretchyLeftJointLeg_grp.translateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkStretchyLeftJointLeg_grp.translateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkStretchyLeftJointLeg_grp.translateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkStretchyLeftJointLeg_grp.rotateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkStretchyLeftJointLeg_grp.rotateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkStretchyLeftJointLeg_grp.rotateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkStretchyLeftJointLeg_grp.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkStretchyLeftJointLeg_grp.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkStretchyLeftJointLeg_grp.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkStretchyLeftJointLeg_grp.visibility" 0')
        self.MDG2_mod.commandToExecute('select -hierarchy "IkStretchyLeftJointLeg_grp"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('select -hierarchy "FkRightArm"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('select -hierarchy "IkRightArm"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('select -hierarchy "IkNoFlipRightArm"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('select -hierarchy "IkPVRightArm"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('select -hierarchy "RightArmIk_grp"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "IkStretchyRightJointArm_grp.translateX"')
        self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "IkStretchyRightJointArm_grp.translateY"')
        self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "IkStretchyRightJointArm_grp.translateZ"')
        self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "IkStretchyRightJointArm_grp.rotateX"')
        self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "IkStretchyRightJointArm_grp.rotateY"')
        self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "IkStretchyRightJointArm_grp.rotateZ"')
        self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "IkStretchyRightJointArm_grp.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "IkStretchyRightJointArm_grp.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "IkStretchyRightJointArm_grp.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "IkStretchyRightJointArm_grp.visibility" 0')
        self.MDG2_mod.commandToExecute('select -hierarchy "IkStretchyRightJointArm_grp"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "FkRightJointLeg_grp.translateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "FkRightJointLeg_grp.translateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "FkRightJointLeg_grp.translateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "FkRightJointLeg_grp.rotateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "FkRightJointLeg_grp.rotateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "FkRightJointLeg_grp.rotateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "FkRightJointLeg_grp.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "FkRightJointLeg_grp.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "FkRightJointLeg_grp.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "FkRightJointLeg_grp.visibility" 0')
        self.MDG2_mod.commandToExecute('select -hierarchy "FkRightJointLeg_grp"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkRightJointLeg_grp.translateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkRightJointLeg_grp.translateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkRightJointLeg_grp.translateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkRightJointLeg_grp.rotateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkRightJointLeg_grp.rotateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkRightJointLeg_grp.rotateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkRightJointLeg_grp.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkRightJointLeg_grp.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkRightJointLeg_grp.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkRightJointLeg_grp.visibility" 0')
        self.MDG2_mod.commandToExecute('select -hierarchy "IkRightJointLeg_grp"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "RightLegIk_grp.translateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "RightLegIk_grp.translateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "RightLegIk_grp.translateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "RightLegIk_grp.rotateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "RightLegIk_grp.rotateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "RightLegIk_grp.rotateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "RightLegIk_grp.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "RightLegIk_grp.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "RightLegIk_grp.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "RightLegIk_grp.visibility" 0')
        self.MDG2_mod.commandToExecute('select -hierarchy "RightLegIk_grp"; hide -clearSelection;')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkStretchyRightJointLeg_grp.translateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkStretchyRightJointLeg_grp.translateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkStretchyRightJointLeg_grp.translateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkStretchyRightJointLeg_grp.rotateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkStretchyRightJointLeg_grp.rotateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkStretchyRightJointLeg_grp.rotateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkStretchyRightJointLeg_grp.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkStretchyRightJointLeg_grp.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkStretchyRightJointLeg_grp.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "IkStretchyRightJointLeg_grp.visibility" 0')
        self.MDG2_mod.commandToExecute('select -hierarchy "IkStretchyRightJointLeg_grp"; hide -clearSelection;')
        self.MDG2_mod.doIt()

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
        lshoulder_loc_transform1 = om2.MFnTransform(lshoulder_loc_obj)
        loc_lshoulder_transform = lshoulder_loc_transform1.transformation()

        lshoulder_loc_path_n = om2.MDagPath()
        lshoulder_loc_path = lshoulder_loc_path_n.getAPathTo(lshoulder_loc_obj)
        loc_lshoulder_transform2 = om2.MFnTransform(lshoulder_loc_path)
        self.loc_lshoulder_t = loc_lshoulder_transform2.translation(om2.MSpace.kWorld)

        rshoulder_loc_obj = shoulder_loc_ls.getDependNode(1)
        rshoulder_loc_transform = om2.MFnTransform(rshoulder_loc_obj)
        loc_rshoulder_transform = rshoulder_loc_transform.transformation()

        rshoulder_loc_path_n = om2.MDagPath()
        rshoulder_loc_path = rshoulder_loc_path_n.getAPathTo(rshoulder_loc_obj)
        loc_rshoulder_transform2 = om2.MFnTransform(rshoulder_loc_path)
        self.loc_rshoulder_t = loc_rshoulder_transform2.translation(om2.MSpace.kWorld)

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
            self.larmik_grp = armjnt_grp.create("transform", "LeftArmIk_grp", self.donttouchjnt_grp)
            self.larmikcluster_grp = armjnt_grp.create("transform", "LeftArmIkCluster_grp", self.splineik_grp)
            self.lupperarmikcluster_grp = armjnt_grp.create("transform", "LeftUpperArmIkCluster_grp", self.larmikcluster_grp)
            self.lupperarmikcluster0_grp = armjnt_grp.create("transform", "LeftUpperArmIkCluster0_grp", self.lupperarmikcluster_grp)
            self.lupperarmikcluster1_grp = armjnt_grp.create("transform", "LeftUpperArmIkCluster1_grp", self.lupperarmikcluster_grp)
            self.lupperarmikcluster2_grp = armjnt_grp.create("transform", "LeftUpperArmIkCluster2_grp", self.lupperarmikcluster_grp)
            self.llowerarmikcluster_grp = armjnt_grp.create("transform", "LeftLowerArmIkCluster_grp", self.larmikcluster_grp)
            self.llowerarmikcluster0_grp = armjnt_grp.create("transform", "LeftLowerArmIkCluster0_grp", self.llowerarmikcluster_grp)
            self.llowerarmikcluster1_grp = armjnt_grp.create("transform", "LeftLowerArmIkCluster1_grp", self.llowerarmikcluster_grp)
            self.llowerarmikcluster2_grp = armjnt_grp.create("transform", "LeftLowerArmIkCluster2_grp", self.llowerarmikcluster_grp)

            self.jnt_lupperarm = armjnt_grp.create("joint", "LeftArm", self.jnt_lshoulder)

            self.jnt_fklupperarm = armjnt_grp.create("joint", "FkLeftArm", self.jnt_lshoulder)

            self.jnt_iklupperarm = armjnt_grp.create("joint", "IkLeftArm", self.jnt_lshoulder)
            jnt_iknofliplupperarm = armjnt_grp.create("joint", "IkNoFlipLeftArm", self.jnt_lshoulder)
            jnt_ikpvlupperarm = armjnt_grp.create("joint", "IkPVLeftArm", self.jnt_lshoulder)

            hand_loc_ls.add(hand_loc[0])
            lupperarm_loc_obj = hand_loc_ls.getDependNode(0)
            lupperarm_loc_transform1 = om2.MFnTransform(lupperarm_loc_obj)
            loc_lupperarm_localtransform = lupperarm_loc_transform1.transformation()

            lupperarm_loc_path_n = om2.MDagPath()
            lupperarm_loc_path = lupperarm_loc_path_n.getAPathTo(lupperarm_loc_obj)
            loc_lupperarm_transform2 = om2.MFnTransform(lupperarm_loc_path)
            loc_lupperarm_t = loc_lupperarm_transform2.translation(om2.MSpace.kWorld)

            jnt_lupperarm_transform = om2.MFnTransform(self.jnt_lupperarm)
            jnt_lupperarm_transform.setTransformation(loc_lupperarm_localtransform)

            jnt_fklupperarm_transform = om2.MFnTransform(self.jnt_fklupperarm)
            jnt_fklupperarm_transform.setTransformation(loc_lupperarm_localtransform)

            jnt_iklupperarm_transform = om2.MFnTransform(self.jnt_iklupperarm)
            jnt_iklupperarm_transform.setTransformation(loc_lupperarm_localtransform)

            jnt_iknofliplupperarm_transform = om2.MFnTransform(jnt_iknofliplupperarm)
            jnt_iknofliplupperarm_transform.setTransformation(loc_lupperarm_localtransform)

            jnt_ikpvlupperarm_transform = om2.MFnTransform(jnt_ikpvlupperarm)
            jnt_ikpvlupperarm_transform.setTransformation(loc_lupperarm_localtransform)

            jnt_lelbow = armjnt_grp.create("joint", "LeftForeArm", self.jnt_lupperarm)
            jnt_fklelbow = armjnt_grp.create("joint", "FkLeftForeArm", self.jnt_fklupperarm)
            jnt_iklelbow = armjnt_grp.create("joint", "IkLeftForeArm", self.jnt_iklupperarm)
            jnt_iknofliplelbow = armjnt_grp.create("joint", "IkNoFlipLeftForeArm", jnt_iknofliplupperarm)
            jnt_ikpvlelbow = armjnt_grp.create("joint", "IkPVLeftForeArm", jnt_ikpvlupperarm)

            hand_loc_ls.add(hand_loc[1])
            lelbow_loc_obj = hand_loc_ls.getDependNode(1)
            lelbow_loc_transform1 = om2.MFnTransform(lelbow_loc_obj)
            loc_lelbow_localtransform = lelbow_loc_transform1.transformation()
            loc_lelbow_t1 = lelbow_loc_transform1.translation(om2.MSpace.kTransform)

            lelbow_loc_path_n = om2.MDagPath()
            lelbow_loc_path = lelbow_loc_path_n.getAPathTo(lelbow_loc_obj)
            lelbow_loc_transform2 = om2.MFnTransform(lelbow_loc_path)
            loc_lelbow_t2 = lelbow_loc_transform2.translation(om2.MSpace.kWorld)

            jnt_lelbow_transform = om2.MFnTransform(jnt_lelbow)
            jnt_lelbow_transform.setTransformation(loc_lelbow_localtransform)

            jnt_fklelbow_transform = om2.MFnTransform(jnt_fklelbow)
            jnt_fklelbow_transform.setTransformation(loc_lelbow_localtransform)

            jnt_iklelbow_transform = om2.MFnTransform(jnt_iklelbow)
            jnt_iklelbow_transform.setTransformation(loc_lelbow_localtransform)

            jnt_iknofliplelbow_transform = om2.MFnTransform(jnt_iknofliplelbow)
            jnt_iknofliplelbow_transform.setTransformation(loc_lelbow_localtransform)

            jnt_ikpvlelbow_transform = om2.MFnTransform(jnt_ikpvlelbow)
            jnt_ikpvlelbow_transform.setTransformation(loc_lelbow_localtransform)

            self.jnt_lwrist = armjnt_grp.create("joint", "LeftHand", jnt_lelbow)
            self.jnt_fklwrist = armjnt_grp.create("joint", "FkLeftHand", jnt_fklelbow)
            self.jnt_iklwrist = armjnt_grp.create("joint", "IkLeftHand", jnt_iklelbow)
            jnt_iknofliplwrist = armjnt_grp.create("joint", "IkNoFlipLeftHand", jnt_iknofliplelbow)
            jnt_ikpvlwrist = armjnt_grp.create("joint", "IkPVLeftHand", jnt_ikpvlelbow)

            hand_loc_ls.add(hand_loc[2])
            lwrist_loc_obj = hand_loc_ls.getDependNode(2)
            lwrist_loc_transform1 = om2.MFnTransform(lwrist_loc_obj)
            loc_lwrist_localtransform = lwrist_loc_transform1.transformation()
            loc_lwrist_t1 = lwrist_loc_transform1.translation(om2.MSpace.kTransform)

            lwrist_loc_path_n = om2.MDagPath()
            lwrist_loc_path = lwrist_loc_path_n.getAPathTo(lwrist_loc_obj)
            lwrist_loc_transform2 = om2.MFnTransform(lwrist_loc_path)
            loc_lwrist_t2 = lwrist_loc_transform2.translation(om2.MSpace.kWorld)

            jnt_lwrist_transform = om2.MFnTransform(self.jnt_lwrist)
            jnt_lwrist_transform.setTransformation(loc_lwrist_localtransform)

            jnt_fklwrist_transform = om2.MFnTransform(self.jnt_fklwrist)
            jnt_fklwrist_transform.setTransformation(loc_lwrist_localtransform)

            jnt_iklwrist_transform = om2.MFnTransform(self.jnt_iklwrist)
            jnt_iklwrist_transform.setTransformation(loc_lwrist_localtransform)

            jnt_iknofliplwrist_transform = om2.MFnTransform(jnt_iknofliplwrist)
            jnt_iknofliplwrist_transform.setTransformation(loc_lwrist_localtransform)

            jnt_ikpvlwrist_transform = om2.MFnTransform(jnt_ikpvlwrist)
            jnt_ikpvlwrist_transform.setTransformation(loc_lwrist_localtransform)

            grp_stretchyiklarm = armjnt_grp.create("transform", "IkStretchyLeftJointArm_grp", self.splineik_grp)

            grp_stretchyiklarm_transform = om2.MFnTransform(grp_stretchyiklarm)
            grp_stretchyiklarm_transform.setTranslation(self.loc_lshoulder_t, om2.MSpace.kTransform)

            jnt_stretchyiklupperarm0 = armjnt_grp.create("joint", "IkSplineLeftUpperArm0", grp_stretchyiklarm)
            jnt_stretchyikcvlupperarm0 = armjnt_grp.create("joint", "IkCvSplineLeftUpperArm0", self.lupperarmikcluster0_grp)

            jnt_stretchyiklupperarm0_transform = om2.MFnTransform(jnt_stretchyiklupperarm0)
            jnt_stretchyiklupperarm0_transform.setTransformation(loc_lupperarm_localtransform)

            jnt_stretchyikcvlupperarm0_transform = om2.MFnTransform(self.lupperarmikcluster_grp)
            jnt_stretchyikcvlupperarm0_transform.setTranslation(loc_lupperarm_t, om2.MSpace.kTransform)

            jnt_stretchyiklupperarm1 = armjnt_grp.create("joint", "IkSplineLeftUpperArm1", jnt_stretchyiklupperarm0)

            jnt_stretchyiklupperarm1_transform = om2.MFnTransform(jnt_stretchyiklupperarm1)
            jnt_stretchyiklupperarm1_transform_t = jnt_stretchyiklupperarm1_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyiklupperarm1_transform_t[0], jnt_stretchyiklupperarm1_transform_t[1], jnt_stretchyiklupperarm1_transform_t[2] = loc_lelbow_t1[0]/4, loc_lelbow_t1[1]/4, loc_lelbow_t1[2]/4
            jnt_stretchyiklupperarm1_transform.setTranslation(jnt_stretchyiklupperarm1_transform_t, om2.MSpace.kTransform)

            jnt_stretchyiklupperarm2 = armjnt_grp.create("joint", "IkSplineLeftUpperArm2", jnt_stretchyiklupperarm1)
            jnt_stretchyikcvlupperarm1 = armjnt_grp.create("joint", "IkCvSplineLeftUpperArm1", self.lupperarmikcluster1_grp)

            jnt_stretchyiklupperarm2_transform = om2.MFnTransform(jnt_stretchyiklupperarm2)
            jnt_stretchyiklupperarm2_transform_t = jnt_stretchyiklupperarm2_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyiklupperarm2_transform_t[0], jnt_stretchyiklupperarm2_transform_t[1], jnt_stretchyiklupperarm2_transform_t[2] = (loc_lelbow_t1[0]/2)-jnt_stretchyiklupperarm1_transform_t[0], (loc_lelbow_t1[1]/2)-jnt_stretchyiklupperarm1_transform_t[1], (loc_lelbow_t1[2]/2)-jnt_stretchyiklupperarm1_transform_t[2]
            jnt_stretchyiklupperarm2_transform.setTranslation(jnt_stretchyiklupperarm2_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikcvlupperarm0_transform_t = jnt_stretchyikcvlupperarm0_transform.translation(om2.MSpace.kTransform)

            jnt_stretchyikcvlupperarm1grp_transform = om2.MFnTransform(self.lupperarmikcluster1_grp)
            jnt_stretchyikcvlupperleg1grp_transform_t = jnt_stretchyikcvlupperarm1grp_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikcvlupperleg1grp_transform_t[0], jnt_stretchyikcvlupperleg1grp_transform_t[1], jnt_stretchyikcvlupperleg1grp_transform_t[2] = -(jnt_stretchyikcvlupperarm0_transform_t[0]-loc_lelbow_t2[0])/2, -(jnt_stretchyikcvlupperarm0_transform_t[1]-loc_lelbow_t2[1])/2, -(jnt_stretchyikcvlupperarm0_transform_t[2]-loc_lelbow_t2[2])/2 #loc_lkneeleg_t[0]+(loc_lupperleg_t[0]-loc_lkneeleg_t[0])/2, loc_lkneeleg_t[1]+(loc_lupperleg_t[1]-loc_lkneeleg_t[1])/2, loc_lkneeleg_t[2]+(loc_lupperleg_t[2]-loc_lkneeleg_t[2])/2
            jnt_stretchyikcvlupperarm1grp_transform.setTranslation(jnt_stretchyikcvlupperleg1grp_transform_t, om2.MSpace.kTransform)

            jnt_stretchyiklupperarm3 = armjnt_grp.create("joint", "IkSplineLeftUpperArm3", jnt_stretchyiklupperarm2)

            jnt_stretchyiklupperarm3_transform = om2.MFnTransform(jnt_stretchyiklupperarm3)
            jnt_stretchyiklupperarm3_transform_t = jnt_stretchyiklupperarm3_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyiklupperarm3_transform_t[0], jnt_stretchyiklupperarm3_transform_t[1], jnt_stretchyiklupperarm3_transform_t[2] = jnt_stretchyiklupperarm2_transform_t[0], jnt_stretchyiklupperarm2_transform_t[1], jnt_stretchyiklupperarm2_transform_t[2]
            jnt_stretchyiklupperarm3_transform.setTranslation(jnt_stretchyiklupperarm3_transform_t, om2.MSpace.kTransform)

            jnt_stretchyiklupperarm4 = armjnt_grp.create("joint", "IkSplineLeftUpperArm4", jnt_stretchyiklupperarm3)
            jnt_stretchyikcvlupperarm2 = armjnt_grp.create("joint", "IkCvSplineLeftUpperArm2", self.lupperarmikcluster2_grp)

            jnt_stretchyiklupperarm4_transform = om2.MFnTransform(jnt_stretchyiklupperarm4)
            jnt_stretchyiklupperarm4_transform_t = jnt_stretchyiklupperarm4_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyiklupperarm4_transform_t[0], jnt_stretchyiklupperarm4_transform_t[1], jnt_stretchyiklupperarm4_transform_t[2] = jnt_stretchyiklupperarm3_transform_t[0], jnt_stretchyiklupperarm3_transform_t[1], jnt_stretchyiklupperarm3_transform_t[2]
            jnt_stretchyiklupperarm4_transform.setTranslation(jnt_stretchyiklupperarm4_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikcvlupperarm2_transform = om2.MFnTransform(self.lupperarmikcluster2_grp)
            jnt_stretchyikcvlupperarm2_transform_t = jnt_stretchyikcvlupperarm2_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikcvlupperarm2_transform_t[0], jnt_stretchyikcvlupperarm2_transform_t[1], jnt_stretchyikcvlupperarm2_transform_t[2] = -(jnt_stretchyikcvlupperarm0_transform_t[0]-loc_lelbow_t2[0]), -(jnt_stretchyikcvlupperarm0_transform_t[1]-loc_lelbow_t2[1]), -(jnt_stretchyikcvlupperarm0_transform_t[2]-loc_lelbow_t2[2]) #loc_lkneeleg_t[0], loc_lkneeleg_t[1], loc_lkneeleg_t[2]
            jnt_stretchyikcvlupperarm2_transform.setTranslation(jnt_stretchyikcvlupperarm2_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikllowerarm0 = armjnt_grp.create("joint", "IkSplineLeftLowerArm0", grp_stretchyiklarm)
            jnt_stretchyikcvllowerarm0 = armjnt_grp.create("joint", "IkCvSplineLeftLowerArm0", self.llowerarmikcluster0_grp)

            jnt_stretchyikllowerarm0_transform = om2.MFnTransform(jnt_stretchyikllowerarm0)
            jnt_stretchyikllowerarm0_transform.setTranslation(loc_lelbow_t2-grp_stretchyiklarm_transform.translation(om2.MSpace.kTransform), om2.MSpace.kTransform)

            jnt_stretchyikcvllowerarm0_transform = om2.MFnTransform(self.llowerarmikcluster_grp)
            jnt_stretchyikcvllowerarm0_transform.setTranslation(loc_lelbow_t2, om2.MSpace.kTransform)

            jnt_stretchyikllowerarm1 = armjnt_grp.create("joint", "IkSplineLeftLowerArm1", jnt_stretchyikllowerarm0)

            jnt_stretchyikllowerarm1_transform = om2.MFnTransform(jnt_stretchyikllowerarm1)
            jnt_stretchyikllowerarm1_transform_t = jnt_stretchyikllowerarm1_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikllowerarm1_transform_t[0], jnt_stretchyikllowerarm1_transform_t[1], jnt_stretchyikllowerarm1_transform_t[2] = loc_lwrist_t1[0]/4, loc_lwrist_t1[1]/4, loc_lwrist_t1[2]/4
            jnt_stretchyikllowerarm1_transform.setTranslation(jnt_stretchyikllowerarm1_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikllowerarm2 = armjnt_grp.create("joint", "IkSplineLeftLowerArm2", jnt_stretchyikllowerarm1)
            jnt_stretchyikvcvllowerarm1 = armjnt_grp.create("joint", "IkCvSplineLeftLowerArm1", self.llowerarmikcluster1_grp)

            jnt_stretchyikllowerarm2_transform = om2.MFnTransform(jnt_stretchyikllowerarm2)
            jnt_stretchyikllowerarm2_transform_t = jnt_stretchyikllowerarm2_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikllowerarm2_transform_t[0], jnt_stretchyikllowerarm2_transform_t[1], jnt_stretchyikllowerarm2_transform_t[2] = (loc_lwrist_t1[0]/2)-jnt_stretchyikllowerarm1_transform_t[0], (loc_lwrist_t1[1]/2)-jnt_stretchyikllowerarm1_transform_t[1], (loc_lwrist_t1[2]/2)-jnt_stretchyikllowerarm1_transform_t[2]
            jnt_stretchyikllowerarm2_transform.setTranslation(jnt_stretchyikllowerarm2_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikcvllowerarm0_transform_t = jnt_stretchyikcvllowerarm0_transform.translation(om2.MSpace.kTransform)

            jnt_stretchyikcvllowerarm1_transform = om2.MFnTransform(self.llowerarmikcluster1_grp)
            jnt_stretchyikcvllowerarm1_transform_t = jnt_stretchyikcvllowerarm1_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikcvllowerarm1_transform_t[0], jnt_stretchyikcvllowerarm1_transform_t[1], jnt_stretchyikcvllowerarm1_transform_t[2] = -(jnt_stretchyikcvllowerarm0_transform_t[0]-loc_lwrist_t2[0])/2, -(jnt_stretchyikcvllowerarm0_transform_t[1]-loc_lwrist_t2[1])/2, -(jnt_stretchyikcvllowerarm0_transform_t[2]-loc_lwrist_t2[2])/2 #loc_lfootballleg_t[0]+((loc_lkneeleg_t[0]-loc_lfootballleg_t[0])/2), loc_lfootballleg_t[1]+((loc_lkneeleg_t[1]-loc_lfootballleg_t[1])/2), loc_lfootballleg_t[2]+((loc_lkneeleg_t[2]-loc_lfootballleg_t[2])/2)
            jnt_stretchyikcvllowerarm1_transform.setTranslation(jnt_stretchyikcvllowerarm1_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikllowerarm3 = armjnt_grp.create("joint", "IkSplineLeftLowerArm3", jnt_stretchyikllowerarm2)

            jnt_stretchyikllowerarm3_transform = om2.MFnTransform(jnt_stretchyikllowerarm3)
            jnt_stretchyikllowearm3_transform_t = jnt_stretchyikllowerarm3_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikllowearm3_transform_t[0], jnt_stretchyikllowearm3_transform_t[1], jnt_stretchyikllowearm3_transform_t[2] = jnt_stretchyikllowerarm2_transform_t[0], jnt_stretchyikllowerarm2_transform_t[1], jnt_stretchyikllowerarm2_transform_t[2]
            jnt_stretchyikllowerarm3_transform.setTranslation(jnt_stretchyikllowearm3_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikllowerarm4 = armjnt_grp.create("joint", "IkSplineLeftLowerArm4", jnt_stretchyikllowerarm3)
            jnt_stretchyikvcvllowerarm2 = armjnt_grp.create("joint", "IkCvSplineLeftLowerArm2", self.llowerarmikcluster2_grp)

            jnt_stretchyikllowerarm4_transform = om2.MFnTransform(jnt_stretchyikllowerarm4)
            jnt_stretchyikllowerarm4_transform_t = jnt_stretchyikllowerarm4_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikllowerarm4_transform_t[0], jnt_stretchyikllowerarm4_transform_t[1], jnt_stretchyikllowerarm4_transform_t[2] = jnt_stretchyikllowearm3_transform_t[0], jnt_stretchyikllowearm3_transform_t[1], jnt_stretchyikllowearm3_transform_t[2]
            jnt_stretchyikllowerarm4_transform.setTranslation(jnt_stretchyikllowerarm4_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikcvllowerarm4_transform = om2.MFnTransform(self.llowerarmikcluster2_grp)
            jnt_stretchyikcvllowerarm4_transform_t = jnt_stretchyikcvllowerarm4_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikcvllowerarm4_transform_t[0], jnt_stretchyikcvllowerarm4_transform_t[1], jnt_stretchyikcvllowerarm4_transform_t[2] = -(jnt_stretchyikcvllowerarm0_transform_t[0]-loc_lwrist_t2[0]), -(jnt_stretchyikcvllowerarm0_transform_t[1]-loc_lwrist_t2[1]), -(jnt_stretchyikcvllowerarm0_transform_t[2]-loc_lwrist_t2[2]) #loc_lfootballleg_t[0], loc_lfootballleg_t[1], loc_lfootballleg_t[2]
            jnt_stretchyikcvllowerarm4_transform.setTranslation(jnt_stretchyikcvllowerarm4_transform_t, om2.MSpace.kTransform)

        if side == -1:
            self.rarmik_grp = armjnt_grp.create("transform", "RightArmIk_grp", self.donttouchjnt_grp)
            self.rarmikcluster_grp = armjnt_grp.create("transform", "RightArmIkCluster_grp", self.splineik_grp)
            self.rupperarmikcluster_grp = armjnt_grp.create("transform", "RightUpperArmIkCluster_grp", self.rarmikcluster_grp)
            self.rupperarmikcluster0_grp = armjnt_grp.create("transform", "RightUpperArmIkCluster0_grp", self.rupperarmikcluster_grp)
            self.rupperarmikcluster1_grp = armjnt_grp.create("transform", "RightUpperArmIkCluster1_grp", self.rupperarmikcluster_grp)
            self.rupperarmikcluster2_grp = armjnt_grp.create("transform", "RightUpperArmIkCluster2_grp", self.rupperarmikcluster_grp)
            self.rlowerarmikcluster_grp = armjnt_grp.create("transform", "RightLowerArmIkCluster_grp", self.rarmikcluster_grp)
            self.rlowerarmikcluster0_grp = armjnt_grp.create("transform", "RightLowerArmIkCluster0_grp", self.rlowerarmikcluster_grp)
            self.rlowerarmikcluster1_grp = armjnt_grp.create("transform", "RightLowerArmIkCluster1_grp", self.rlowerarmikcluster_grp)
            self.rlowerarmikcluster2_grp = armjnt_grp.create("transform", "RightLowerArmIkCluster2_grp", self.rlowerarmikcluster_grp)

            self.jnt_rupperarm = armjnt_grp.create("joint", "RightArm", self.jnt_rshoulder)

            self.jnt_fkrupperarm = armjnt_grp.create("joint", "FkRightArm", self.jnt_rshoulder)

            self.jnt_ikrupperarm = armjnt_grp.create("joint", "IkRightArm", self.jnt_rshoulder)
            jnt_iknofliprupperarm = armjnt_grp.create("joint", "IkNoFlipRightArm", self.jnt_rshoulder)
            jnt_ikpvrupperarm = armjnt_grp.create("joint", "IkPVRightArm", self.jnt_rshoulder)

            hand_loc_ls.add(hand_loc[3])
            rupperarm_loc_obj = hand_loc_ls.getDependNode(0)
            rupperarm_loc_transform1 = om2.MFnTransform(rupperarm_loc_obj)
            loc_rupperarm_localtransform = rupperarm_loc_transform1.transformation()

            rupperarm_loc_path_n = om2.MDagPath()
            rupperarm_loc_path = rupperarm_loc_path_n.getAPathTo(rupperarm_loc_obj)
            rupperarm_loc_transform2 = om2.MFnTransform(rupperarm_loc_path)
            loc_rupperarm_t = rupperarm_loc_transform2.translation(om2.MSpace.kWorld)

            jnt_rupperarm_transform = om2.MFnTransform(self.jnt_rupperarm)
            jnt_rupperarm_transform.setTransformation(loc_rupperarm_localtransform)

            jnt_fkrupperarm_transform = om2.MFnTransform(self.jnt_fkrupperarm)
            jnt_fkrupperarm_transform.setTransformation(loc_rupperarm_localtransform)

            jnt_ikrupperarm_transform = om2.MFnTransform(self.jnt_ikrupperarm)
            jnt_ikrupperarm_transform.setTransformation(loc_rupperarm_localtransform)

            jnt_iknofliprupperarm_transform = om2.MFnTransform(jnt_iknofliprupperarm)
            jnt_iknofliprupperarm_transform.setTransformation(loc_rupperarm_localtransform)

            jnt_ikpvrupperarm_transform = om2.MFnTransform(jnt_ikpvrupperarm)
            jnt_ikpvrupperarm_transform.setTransformation(loc_rupperarm_localtransform)

            jnt_relbow = armjnt_grp.create("joint", "RightForeArm", self.jnt_rupperarm)
            jnt_fkrelbow = armjnt_grp.create("joint", "FkRightForeArm", self.jnt_fkrupperarm)
            jnt_ikrelbow = armjnt_grp.create("joint", "IkRightForeArm", self.jnt_ikrupperarm)
            jnt_iknofliprelbow = armjnt_grp.create("joint", "IkNoFlipRightForeArm", jnt_iknofliprupperarm)
            jnt_ikpvrelbow = armjnt_grp.create("joint", "IkPVRightForeArm", jnt_ikpvrupperarm)

            hand_loc_ls.add(hand_loc[4])
            relbow_loc_obj = hand_loc_ls.getDependNode(1)
            relbow_loc_transform1 = om2.MFnTransform(relbow_loc_obj)
            loc_relbow_localtransform = relbow_loc_transform1.transformation()
            loc_relbow_t1 = relbow_loc_transform1.translation(om2.MSpace.kTransform)

            relbowleg_loc_path_n = om2.MDagPath()
            relbowleg_loc_path = relbowleg_loc_path_n.getAPathTo(relbow_loc_obj)
            relbow_loc_transform2 = om2.MFnTransform(relbowleg_loc_path)
            loc_relbow_t2 = relbow_loc_transform2.translation(om2.MSpace.kWorld)

            jnt_relbow_transform = om2.MFnTransform(jnt_relbow)
            jnt_relbow_transform.setTransformation(loc_relbow_localtransform)

            jnt_fkrelbow_transform = om2.MFnTransform(jnt_fkrelbow)
            jnt_fkrelbow_transform.setTransformation(loc_relbow_localtransform)

            jnt_ikrelbow_transform = om2.MFnTransform(jnt_ikrelbow)
            jnt_ikrelbow_transform.setTransformation(loc_relbow_localtransform)

            jnt_iknofliprelbow_transform = om2.MFnTransform(jnt_iknofliprelbow)
            jnt_iknofliprelbow_transform.setTransformation(loc_relbow_localtransform)

            jnt_ikpvrelbow_transform = om2.MFnTransform(jnt_ikpvrelbow)
            jnt_ikpvrelbow_transform.setTransformation(loc_relbow_localtransform)

            self.jnt_rwrist = armjnt_grp.create("joint", "RightHand", jnt_relbow)
            self.jnt_fkrwrist = armjnt_grp.create("joint", "FkRightHand", jnt_fkrelbow)
            self.jnt_ikrwrist = armjnt_grp.create("joint", "IkRightHand", jnt_ikrelbow)
            jnt_iknofliprwrist = armjnt_grp.create("joint", "IkNoFlipRightHand", jnt_iknofliprelbow)
            jnt_ikpvrwrist = armjnt_grp.create("joint", "IkPVRightHand", jnt_ikpvrelbow)

            hand_loc_ls.add(hand_loc[5])
            rwrist_loc_obj = hand_loc_ls.getDependNode(2)
            loc_rwrist_transform1 = om2.MFnTransform(rwrist_loc_obj)
            loc_rwrist_localtransform = loc_rwrist_transform1.transformation()
            loc_rwrist_t1 = loc_rwrist_transform1.translation(om2.MSpace.kTransform)

            rwrist_loc_path_n = om2.MDagPath()
            rwrist_loc_path = rwrist_loc_path_n.getAPathTo(rwrist_loc_obj)
            loc_rwrist_transform2 = om2.MFnTransform(rwrist_loc_path)
            loc_rwrist_t2 = loc_rwrist_transform2.translation(om2.MSpace.kWorld)

            jnt_rwrist_transform = om2.MFnTransform(self.jnt_rwrist)
            jnt_rwrist_transform.setTransformation(loc_rwrist_localtransform)

            jnt_fkrwrist_transform = om2.MFnTransform(self.jnt_fkrwrist)
            jnt_fkrwrist_transform.setTransformation(loc_rwrist_localtransform)

            jnt_ikrwrist_transform = om2.MFnTransform(self.jnt_ikrwrist)
            jnt_ikrwrist_transform.setTransformation(loc_rwrist_localtransform)

            jnt_iknofliprwrist_transform = om2.MFnTransform(jnt_iknofliprwrist)
            jnt_iknofliprwrist_transform.setTransformation(loc_rwrist_localtransform)

            jnt_ikpvrwrist_transform = om2.MFnTransform(jnt_ikpvrwrist)
            jnt_ikpvrwrist_transform.setTransformation(loc_rwrist_localtransform)

            grp_stretchyikrarm = armjnt_grp.create("transform", "IkStretchyRightJointArm_grp", self.splineik_grp)

            grp_stretchyiklarm_transform = om2.MFnTransform(grp_stretchyikrarm)
            grp_stretchyiklarm_transform.setTranslation(self.loc_rshoulder_t, om2.MSpace.kTransform)

            jnt_stretchyikrupperarm0 = armjnt_grp.create("joint", "IkSplineRightUpperArm0", grp_stretchyikrarm)
            jnt_stretchyikcvrupperarm0 = armjnt_grp.create("joint", "IkCvSplineRightUpperArm0", self.rupperarmikcluster0_grp)

            jnt_stretchyikrupperarm0_transform = om2.MFnTransform(jnt_stretchyikrupperarm0)
            jnt_stretchyikrupperarm0_transform.setTransformation(loc_rupperarm_localtransform)

            jnt_stretchyikcvrupperarm0_transform = om2.MFnTransform(self.rupperarmikcluster_grp)
            jnt_stretchyikcvrupperarm0_transform.setTranslation(loc_rupperarm_t, om2.MSpace.kTransform)

            jnt_stretchyikrupperarm1 = armjnt_grp.create("joint", "IkSplineRightUpperArm1", jnt_stretchyikrupperarm0)

            jnt_stretchyikrupperarm1_transform = om2.MFnTransform(jnt_stretchyikrupperarm1)
            jnt_stretchyikrupperarm1_transform_t = jnt_stretchyikrupperarm1_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikrupperarm1_transform_t[0], jnt_stretchyikrupperarm1_transform_t[1], jnt_stretchyikrupperarm1_transform_t[2] = loc_relbow_t1[0]/4, loc_relbow_t1[1]/4, loc_relbow_t1[2]/4
            jnt_stretchyikrupperarm1_transform.setTranslation(jnt_stretchyikrupperarm1_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikrupperarm2 = armjnt_grp.create("joint", "IkSplineRightUpperArm2", jnt_stretchyikrupperarm1)
            jnt_stretchyikcvrupperarm1 = armjnt_grp.create("joint", "IkCvSplineRightUpperArm1", self.rupperarmikcluster1_grp)

            jnt_stretchyikrupperarm2_transform = om2.MFnTransform(jnt_stretchyikrupperarm2)
            jnt_stretchyikrupperarm2_transform_t = jnt_stretchyikrupperarm2_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikrupperarm2_transform_t[0], jnt_stretchyikrupperarm2_transform_t[1], jnt_stretchyikrupperarm2_transform_t[2] = (loc_relbow_t1[0]/2)-jnt_stretchyikrupperarm1_transform_t[0], (loc_relbow_t1[1]/2)-jnt_stretchyikrupperarm1_transform_t[1], (loc_relbow_t1[2]/2)-jnt_stretchyikrupperarm1_transform_t[2]
            jnt_stretchyikrupperarm2_transform.setTranslation(jnt_stretchyikrupperarm2_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikcvrupperarm0_transform_t = jnt_stretchyikcvrupperarm0_transform.translation(om2.MSpace.kTransform)

            jnt_stretchyikcvrupperarm1grp_transform = om2.MFnTransform(self.rupperarmikcluster1_grp)
            jnt_stretchyikcvrupperleg1grp_transform_t = jnt_stretchyikcvrupperarm1grp_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikcvrupperleg1grp_transform_t[0], jnt_stretchyikcvrupperleg1grp_transform_t[1], jnt_stretchyikcvrupperleg1grp_transform_t[2] = -(jnt_stretchyikcvrupperarm0_transform_t[0]-loc_relbow_t2[0])/2, -(jnt_stretchyikcvrupperarm0_transform_t[1]-loc_relbow_t2[1])/2, -(jnt_stretchyikcvrupperarm0_transform_t[2]-loc_relbow_t2[2])/2
            jnt_stretchyikcvrupperarm1grp_transform.setTranslation(jnt_stretchyikcvrupperleg1grp_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikrupperarm3 = armjnt_grp.create("joint", "IkSplineRightUpperArm3", jnt_stretchyikrupperarm2)

            jnt_stretchyikrupperarm3_transform = om2.MFnTransform(jnt_stretchyikrupperarm3)
            jnt_stretchyikrupperarm3_transform_t = jnt_stretchyikrupperarm3_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikrupperarm3_transform_t[0], jnt_stretchyikrupperarm3_transform_t[1], jnt_stretchyikrupperarm3_transform_t[2] = jnt_stretchyikrupperarm2_transform_t[0], jnt_stretchyikrupperarm2_transform_t[1], jnt_stretchyikrupperarm2_transform_t[2]
            jnt_stretchyikrupperarm3_transform.setTranslation(jnt_stretchyikrupperarm3_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikrupperarm4 = armjnt_grp.create("joint", "IkSplineRightUpperArm4", jnt_stretchyikrupperarm3)
            jnt_stretchyikcvrupperarm2 = armjnt_grp.create("joint", "IkCvSplineRightUpperArm2", self.rupperarmikcluster2_grp)

            jnt_stretchyikrupperarm4_transform = om2.MFnTransform(jnt_stretchyikrupperarm4)
            jnt_stretchyikrupperarm4_transform_t = jnt_stretchyikrupperarm4_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikrupperarm4_transform_t[0], jnt_stretchyikrupperarm4_transform_t[1], jnt_stretchyikrupperarm4_transform_t[2] = jnt_stretchyikrupperarm3_transform_t[0], jnt_stretchyikrupperarm3_transform_t[1], jnt_stretchyikrupperarm3_transform_t[2]
            jnt_stretchyikrupperarm4_transform.setTranslation(jnt_stretchyikrupperarm4_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikcvrupperarm2_transform = om2.MFnTransform(self.rupperarmikcluster2_grp)
            jnt_stretchyikcvrupperarm2_transform_t = jnt_stretchyikcvrupperarm2_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikcvrupperarm2_transform_t[0], jnt_stretchyikcvrupperarm2_transform_t[1], jnt_stretchyikcvrupperarm2_transform_t[2] = -(jnt_stretchyikcvrupperarm0_transform_t[0]-loc_relbow_t2[0]), -(jnt_stretchyikcvrupperarm0_transform_t[1]-loc_relbow_t2[1]), -(jnt_stretchyikcvrupperarm0_transform_t[2]-loc_relbow_t2[2])
            jnt_stretchyikcvrupperarm2_transform.setTranslation(jnt_stretchyikcvrupperarm2_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikrlowerarm0 = armjnt_grp.create("joint", "IkSplineRightLowerArm0", grp_stretchyikrarm)
            jnt_stretchyikcvrlowerarm0 = armjnt_grp.create("joint", "IkCvSplineRightLowerArm0", self.rlowerarmikcluster0_grp)

            jnt_stretchyikrlowerarm0_transform = om2.MFnTransform(jnt_stretchyikrlowerarm0)
            jnt_stretchyikrlowerarm0_transform.setTranslation(loc_relbow_t2-grp_stretchyiklarm_transform.translation(om2.MSpace.kTransform), om2.MSpace.kTransform)

            jnt_stretchyikcvrlowerarm0_transform = om2.MFnTransform(self.rlowerarmikcluster_grp)
            jnt_stretchyikcvrlowerarm0_transform.setTranslation(loc_relbow_t2, om2.MSpace.kTransform)

            jnt_stretchyikrlowerarm1 = armjnt_grp.create("joint", "IkSplineRightLowerArm1", jnt_stretchyikrlowerarm0)

            jnt_stretchyikrlowerarm1_transform = om2.MFnTransform(jnt_stretchyikrlowerarm1)
            jnt_stretchyikrlowerarm1_transform_t = jnt_stretchyikrlowerarm1_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikrlowerarm1_transform_t[0], jnt_stretchyikrlowerarm1_transform_t[1], jnt_stretchyikrlowerarm1_transform_t[2] = loc_rwrist_t1[0]/4, loc_rwrist_t1[1]/4, loc_rwrist_t1[2]/4
            jnt_stretchyikrlowerarm1_transform.setTranslation(jnt_stretchyikrlowerarm1_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikrlowerarm2 = armjnt_grp.create("joint", "IkSplineRightLowerArm2", jnt_stretchyikrlowerarm1)
            jnt_stretchyikvcvrlowerarm1 = armjnt_grp.create("joint", "IkCvSplineRightLowerArm1", self.rlowerarmikcluster1_grp)

            jnt_stretchyikrlowerarm2_transform = om2.MFnTransform(jnt_stretchyikrlowerarm2)
            jnt_stretchyikrlowerarm2_transform_t = jnt_stretchyikrlowerarm2_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikrlowerarm2_transform_t[0], jnt_stretchyikrlowerarm2_transform_t[1], jnt_stretchyikrlowerarm2_transform_t[2] = (loc_rwrist_t1[0]/2)-jnt_stretchyikrlowerarm1_transform_t[0], (loc_rwrist_t1[1]/2)-jnt_stretchyikrlowerarm1_transform_t[1], (loc_rwrist_t1[2]/2)-jnt_stretchyikrlowerarm1_transform_t[2]
            jnt_stretchyikrlowerarm2_transform.setTranslation(jnt_stretchyikrlowerarm2_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikcvrlowerarm0_transform_t = jnt_stretchyikcvrlowerarm0_transform.translation(om2.MSpace.kTransform)

            jnt_stretchyikcvrlowerarm1_transform = om2.MFnTransform(self.rlowerarmikcluster1_grp)
            jnt_stretchyikcvrlowerarm1_transform_t = jnt_stretchyikcvrlowerarm1_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikcvrlowerarm1_transform_t[0], jnt_stretchyikcvrlowerarm1_transform_t[1], jnt_stretchyikcvrlowerarm1_transform_t[2] = -(jnt_stretchyikcvrlowerarm0_transform_t[0]-loc_rwrist_t2[0])/2, -(jnt_stretchyikcvrlowerarm0_transform_t[1]-loc_rwrist_t2[1])/2, -(jnt_stretchyikcvrlowerarm0_transform_t[2]-loc_rwrist_t2[2])/2
            jnt_stretchyikcvrlowerarm1_transform.setTranslation(jnt_stretchyikcvrlowerarm1_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikrlowerarm3 = armjnt_grp.create("joint", "IkSplineRightLowerArm3", jnt_stretchyikrlowerarm2)

            jnt_stretchyikrlowerarm3_transform = om2.MFnTransform(jnt_stretchyikrlowerarm3)
            jnt_stretchyikrlowerarm3_transform_t = jnt_stretchyikrlowerarm3_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikrlowerarm3_transform_t[0], jnt_stretchyikrlowerarm3_transform_t[1], jnt_stretchyikrlowerarm3_transform_t[2] = jnt_stretchyikrlowerarm2_transform_t[0], jnt_stretchyikrlowerarm2_transform_t[1], jnt_stretchyikrlowerarm2_transform_t[2]
            jnt_stretchyikrlowerarm3_transform.setTranslation(jnt_stretchyikrlowerarm3_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikrlowerarm4 = armjnt_grp.create("joint", "IkSplineRightLowerArm4", jnt_stretchyikrlowerarm3)
            jnt_stretchyikvcvrlowerarm2 = armjnt_grp.create("joint", "IkCvSplineRightLowerArm2", self.rlowerarmikcluster2_grp)

            jnt_stretchyikrlowerarm4_transform = om2.MFnTransform(jnt_stretchyikrlowerarm4)
            jnt_stretchyikrlowerarm4_transform_t = jnt_stretchyikrlowerarm4_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikrlowerarm4_transform_t[0], jnt_stretchyikrlowerarm4_transform_t[1], jnt_stretchyikrlowerarm4_transform_t[2] = jnt_stretchyikrlowerarm3_transform_t[0], jnt_stretchyikrlowerarm3_transform_t[1], jnt_stretchyikrlowerarm3_transform_t[2]
            jnt_stretchyikrlowerarm4_transform.setTranslation(jnt_stretchyikrlowerarm4_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikcvrlowerarm4_transform = om2.MFnTransform(self.rlowerarmikcluster2_grp)
            jnt_stretchyikcvrlowerarm4_transform_t = jnt_stretchyikcvrlowerarm4_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikcvrlowerarm4_transform_t[0], jnt_stretchyikcvrlowerarm4_transform_t[1], jnt_stretchyikcvrlowerarm4_transform_t[2] = -(jnt_stretchyikcvrlowerarm0_transform_t[0]-loc_rwrist_t2[0]), -(jnt_stretchyikcvrlowerarm0_transform_t[1]-loc_rwrist_t2[1]), -(jnt_stretchyikcvrlowerarm0_transform_t[2]-loc_rwrist_t2[2])
            jnt_stretchyikcvrlowerarm4_transform.setTranslation(jnt_stretchyikcvrlowerarm4_transform_t, om2.MSpace.kTransform)

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
            jnt_iknofliplupperleg = legjnt_grp.create("joint", "IkNoFlipLeftUpLeg", grp_iklupperleg)
            jnt_ikpvlupperleg = legjnt_grp.create("joint", "IkPVLeftUpLeg", grp_iklupperleg)

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

            jnt_iknofliplupperleg_transform = om2.MFnTransform(jnt_iknofliplupperleg)
            jnt_iknofliplupperleg_transform.setTransformation(loc_lupperleg_transform)

            jnt_ikpvlupperleg_transform = om2.MFnTransform(jnt_ikpvlupperleg)
            jnt_ikpvlupperleg_transform.setTransformation(loc_lupperleg_transform)

            jnt_lknee = legjnt_grp.create("joint", "LeftLeg", jnt_lupperleg)
            jnt_fklknee = legjnt_grp.create("joint", "FkLeftLeg", jnt_fklupperleg)
            jnt_iklknee = legjnt_grp.create("joint", "IkLeftLeg", jnt_iklupperleg)
            jnt_iknofliplknee = legjnt_grp.create("joint", "IkNoFlipLeftLeg", jnt_iknofliplupperleg)
            jnt_ikpvlknee = legjnt_grp.create("joint", "IkPVLeftLeg", jnt_ikpvlupperleg)

            leg_loc_ls.add(leg_loc[1])
            lknee_loc_obj = leg_loc_ls.getDependNode(1)
            lknee_loc_transform = om2.MFnTransform(lknee_loc_obj)
            loc_lknee_transform = lknee_loc_transform.transformation()
            loc_lknee_transform_t = loc_lknee_transform.translation(om2.MSpace.kTransform)

            lkneeleg_loc_path_n = om2.MDagPath()
            lkneeleg_loc_path = lkneeleg_loc_path_n.getAPathTo(lknee_loc_obj)
            loc_lkneeleg_transform = om2.MFnTransform(lkneeleg_loc_path)
            loc_lkneeleg_t = loc_lkneeleg_transform.translation(om2.MSpace.kWorld)

            jnt_lknee_transform = om2.MFnTransform(jnt_lknee)
            jnt_lknee_transform.setTransformation(loc_lknee_transform)

            jnt_fklknee_transform = om2.MFnTransform(jnt_fklknee)
            jnt_fklknee_transform.setTransformation(loc_lknee_transform)

            jnt_iklknee_transform = om2.MFnTransform(jnt_iklknee)
            jnt_iklknee_transform.setTransformation(loc_lknee_transform)

            jnt_iknofliplknee_transform = om2.MFnTransform(jnt_iknofliplknee)
            jnt_iknofliplknee_transform.setTransformation(loc_lknee_transform)

            jnt_ikpvlknee_transform = om2.MFnTransform(jnt_ikpvlknee)
            jnt_ikpvlknee_transform.setTransformation(loc_lknee_transform)

            jnt_lfootball = legjnt_grp.create("joint", "LeftFoot", jnt_lknee)
            jnt_fklfootball = legjnt_grp.create("joint", "FkLeftFoot", jnt_fklknee)
            jnt_iklfootball = legjnt_grp.create("joint", "IkLeftFoot", jnt_iklknee)
            jnt_iknofliplfootball = legjnt_grp.create("joint", "IkNoFlipLeftFoot", jnt_iknofliplknee)
            jnt_ikpvlfootball = legjnt_grp.create("joint", "IkPVLeftFoot", jnt_ikpvlknee)
            lreversefoot_hell = legjnt_grp.create("transform", "LeftReverseFootHeel", self.donttouchjnt_grp)
            lreversefoot_hell_ln = legjnt_grp.create("locator", "LeftReverseFootHeelShape", lreversefoot_hell)

            leg_loc_ls.add(leg_loc[2])
            lfootball_loc_obj = leg_loc_ls.getDependNode(2)
            lfootball_loc_transform = om2.MFnTransform(lfootball_loc_obj)
            loc_lfootball_transform = lfootball_loc_transform.transformation()
            loc_lfootball_t = lfootball_loc_transform.translation(om2.MSpace.kTransform)

            lfootballleg_loc_path_n = om2.MDagPath()
            lfootballleg_loc_path = lfootballleg_loc_path_n.getAPathTo(lfootball_loc_obj)
            loc_lfootballleg_transform = om2.MFnTransform(lfootballleg_loc_path)
            loc_lfootballleg_t = loc_lfootballleg_transform.translation(om2.MSpace.kWorld)

            jnt_lfootball_transform = om2.MFnTransform(jnt_lfootball)
            jnt_lfootball_transform.setTransformation(loc_lfootball_transform)

            jnt_fklfootball_transform = om2.MFnTransform(jnt_fklfootball)
            jnt_fklfootball_transform.setTransformation(loc_lfootball_transform)

            jnt_iklfootball_transform = om2.MFnTransform(jnt_iklfootball)
            jnt_iklfootball_transform.setTransformation(loc_lfootball_transform)

            jnt_iknofliplfootball_transform = om2.MFnTransform(jnt_iknofliplfootball)
            jnt_iknofliplfootball_transform.setTransformation(loc_lfootball_transform)

            jnt_ikpvlfootball_transform = om2.MFnTransform(jnt_ikpvlfootball)
            jnt_ikpvlfootball_transform.setTransformation(loc_lfootball_transform)

            lreversefoot_hell_transform = om2.MFnTransform(lreversefoot_hell)
            lreversefoot_hell_transform_t = lreversefoot_hell_transform.translation(om2.MSpace.kTransform)
            lreversefoot_hell_transform_t[0], lreversefoot_hell_transform_t[1], lreversefoot_hell_transform_t[2] = loc_lfootballleg_t[0], loc_lfootballleg_t[1], -loc_lfootballleg_t[2]*10
            lreversefoot_hell_transform.setTranslation(lreversefoot_hell_transform_t, om2.MSpace.kTransform)

            grp_llegik_transform = om2.MFnTransform(self.llegik_grp)
            grp_llegik_transform.setTranslation(loc_lfootballleg_t, om2.MSpace.kTransform)

            jnt_lfoot = legjnt_grp.create("joint", "LeftToeBase", jnt_lfootball)
            jnt_fklfoot = legjnt_grp.create("joint", "FkLeftToeBase", jnt_fklfootball)
            jnt_iklfoot = legjnt_grp.create("joint", "IkLeftToeBase", jnt_iklfootball)
            lreversefoot_foot = legjnt_grp.create("transform", "LeftReverseFootToe", self.donttouchjnt_grp)
            lreversefoot_foot_ln = legjnt_grp.create("locator", "LeftReverseFootToeShape", lreversefoot_foot)
            lreverseinner_foot = legjnt_grp.create("transform", "LeftReverseInnerFoot", self.donttouchjnt_grp)
            lreverseinner_foot_ln = legjnt_grp.create("locator", "LeftReverseInnerFootShape", lreverseinner_foot)
            lreverseouter_foot = legjnt_grp.create("transform", "LeftReverseOuterFoot", self.donttouchjnt_grp)
            lreverseouter_foot_ln = legjnt_grp.create("locator", "LeftReverseOuterFootShape", lreverseouter_foot)

            leg_loc_ls.add(leg_loc[3])
            lfoot_loc_obj = leg_loc_ls.getDependNode(3)
            lfoot_loc_transform = om2.MFnTransform(lfoot_loc_obj)
            loc_lfoot_transform = lfoot_loc_transform.transformation()

            lfootleg_loc_path_n = om2.MDagPath()
            lfootleg_loc_path = lfootleg_loc_path_n.getAPathTo(lfoot_loc_obj)
            loc_lfootleg_transform = om2.MFnTransform(lfootleg_loc_path)
            loc_lfootleg_t = loc_lfootleg_transform.translation(om2.MSpace.kWorld)

            jnt_lfoot_transform = om2.MFnTransform(jnt_lfoot)
            jnt_lfoot_transform.setTransformation(loc_lfoot_transform)

            jnt_fklfoot_transform = om2.MFnTransform(jnt_fklfoot)
            jnt_fklfoot_transform.setTransformation(loc_lfoot_transform)

            jnt_iklfoot_transform = om2.MFnTransform(jnt_iklfoot)
            jnt_iklfoot_transform.setTransformation(loc_lfoot_transform)

            lreversefoot_foot_transform = om2.MFnTransform(lreversefoot_foot)
            lreversefoot_foot_transform.setTranslation(loc_lfootleg_t, om2.MSpace.kTransform)

            lreverseinner_foot_transform = om2.MFnTransform(lreverseinner_foot)
            lreverseinner_foot_transform_t = lreverseinner_foot_transform.translation(om2.MSpace.kTransform)
            lreverseinner_foot_transform_t[0], lreverseinner_foot_transform_t[2], lreverseinner_foot_transform_t[2] = loc_lfootleg_t[0]*0.1, loc_lfootleg_t[1], loc_lfootleg_t[2]
            lreverseinner_foot_transform.setTranslation(lreverseinner_foot_transform_t, om2.MSpace.kTransform)

            lreverseouter_foot_transform = om2.MFnTransform(lreverseouter_foot)
            lreverseouter_foot_transform_t = lreverseouter_foot_transform.translation(om2.MSpace.kTransform)
            lreverseouter_foot_transform_t[0], lreverseouter_foot_transform_t[2], lreverseouter_foot_transform_t[2] = loc_lfootleg_t[0]*1.9, loc_lfootleg_t[1], loc_lfootleg_t[2]
            lreverseouter_foot_transform.setTranslation(lreverseouter_foot_transform_t, om2.MSpace.kTransform)

            jnt_ltoe = legjnt_grp.create("joint", "LeftToeEnd", jnt_lfoot)
            jnt_fkltoe = legjnt_grp.create("joint", "FkLeftToeEnd", jnt_fklfoot)
            jnt_ikltoe = legjnt_grp.create("joint", "IkLeftToeEnd", jnt_iklfoot)
            lreversefoot_toe = legjnt_grp.create("transform", "LeftReverseFootToeEnd", self.donttouchjnt_grp)
            lreversefoot_toe_ln = legjnt_grp.create("locator", "LeftReverseFootToeEndShape", lreversefoot_toe)
            lreversefoot_toewiggle = legjnt_grp.create("transform", "LeftReverseFootToeWiggle", lreversefoot_toe)

            leg_loc_ls.add(leg_loc[4])
            ltoe_loc_obj = leg_loc_ls.getDependNode(4)
            ltoe_loc_transform = om2.MFnTransform(ltoe_loc_obj)
            loc_ltoe_transform = ltoe_loc_transform.transformation()

            ltoeleg_loc_path_n = om2.MDagPath()
            ltoeleg_loc_path = ltoeleg_loc_path_n.getAPathTo(ltoe_loc_obj)
            loc_ltoeleg_transform = om2.MFnTransform(ltoeleg_loc_path)
            loc_ltoeleg_t = loc_ltoeleg_transform.translation(om2.MSpace.kWorld)

            jnt_ltoe_transform = om2.MFnTransform(jnt_ltoe)
            jnt_ltoe_transform.setTransformation(loc_ltoe_transform)

            jnt_fkltoe_transform = om2.MFnTransform(jnt_fkltoe)
            jnt_fkltoe_transform.setTransformation(loc_ltoe_transform)

            jnt_ikltoe_transform = om2.MFnTransform(jnt_ikltoe)
            jnt_ikltoe_transform.setTransformation(loc_ltoe_transform)

            lreversefoot_toe_transform = om2.MFnTransform(lreversefoot_toe)
            lreversefoot_toe_transform.setTranslation(loc_ltoeleg_t, om2.MSpace.kTransform)

            lfoottoewiggle_path_n = om2.MDagPath()
            lfoottoewiggle_path = lfoottoewiggle_path_n.getAPathTo(lreversefoot_toewiggle)
            lfoottoewiggle_worldtransform = om2.MFnTransform(lfoottoewiggle_path)
            lfoottoewiggle_worldtransform.setRotatePivot(om2.MPoint(loc_lfootleg_t), om2.MSpace.kWorld, False)

            grp_stretchyiklleg = legjnt_grp.create("transform", "IkStretchyLeftJointLeg_grp", self.splineik_grp)

            grp_stretchyiklleg_transform = om2.MFnTransform(grp_stretchyiklleg)
            grp_stretchyiklleg_transform.setTransformation(self.loc_root_transform)

            jnt_stretchyiklupperleg0 = legjnt_grp.create("joint", "IkSplineLeftUpperLeg0", grp_stretchyiklleg)
            jnt_stretchyikcvlupperleg0 = legjnt_grp.create("joint", "IkCvSplineLeftUpperLeg0", self.lupperlegikcluster0_grp)

            jnt_stretchyiklupperleg0_transform = om2.MFnTransform(jnt_stretchyiklupperleg0)
            jnt_stretchyiklupperleg0_transform.setTransformation(loc_lupperleg_transform)

            jnt_stretchyikcvlupperleg0_transform = om2.MFnTransform(self.lupperlegikcluster_grp)
            jnt_stretchyikcvlupperleg0_transform.setTranslation(loc_lupperleg_t, om2.MSpace.kTransform)

            jnt_stretchyiklupperleg1 = legjnt_grp.create("joint", "IkSplineLeftUpperLeg1", jnt_stretchyiklupperleg0)

            jnt_stretchyiklupperleg1_transform = om2.MFnTransform(jnt_stretchyiklupperleg1)
            jnt_stretchyiklupperleg1_transform_t = jnt_stretchyiklupperleg1_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyiklupperleg1_transform_t[0], jnt_stretchyiklupperleg1_transform_t[1], jnt_stretchyiklupperleg1_transform_t[2] = loc_lknee_transform_t[0]/4, loc_lknee_transform_t[1]/4, loc_lknee_transform_t[2]/4
            jnt_stretchyiklupperleg1_transform.setTranslation(jnt_stretchyiklupperleg1_transform_t, om2.MSpace.kTransform)

            jnt_stretchyiklupperleg2 = legjnt_grp.create("joint", "IkSplineLeftUpperLeg2", jnt_stretchyiklupperleg1)
            jnt_stretchyikcvlupperleg1 = legjnt_grp.create("joint", "IkCvSplineLeftUpperLeg1", self.lupperlegikcluster1_grp)

            jnt_stretchyiklupperleg2_transform = om2.MFnTransform(jnt_stretchyiklupperleg2)
            jnt_stretchyiklupperleg2_transform_t = jnt_stretchyiklupperleg2_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyiklupperleg2_transform_t[0], jnt_stretchyiklupperleg2_transform_t[1], jnt_stretchyiklupperleg2_transform_t[2] = (loc_lknee_transform_t[0]/2)-jnt_stretchyiklupperleg1_transform_t[0], (loc_lknee_transform_t[1]/2)-jnt_stretchyiklupperleg1_transform_t[1], (loc_lknee_transform_t[2]/2)-jnt_stretchyiklupperleg1_transform_t[2]
            jnt_stretchyiklupperleg2_transform.setTranslation(jnt_stretchyiklupperleg2_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikcvlupperleg0_transform_t = jnt_stretchyikcvlupperleg0_transform.translation(om2.MSpace.kTransform)

            jnt_stretchyikcvlupperleg1grp_transform = om2.MFnTransform(self.lupperlegikcluster1_grp)
            jnt_stretchyikcvlupperleg1grp_transform_t = jnt_stretchyikcvlupperleg1grp_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikcvlupperleg1grp_transform_t[0], jnt_stretchyikcvlupperleg1grp_transform_t[1], jnt_stretchyikcvlupperleg1grp_transform_t[2] = -(jnt_stretchyikcvlupperleg0_transform_t[0]-loc_lkneeleg_t[0])/2, -(jnt_stretchyikcvlupperleg0_transform_t[1]-loc_lkneeleg_t[1])/2, -(jnt_stretchyikcvlupperleg0_transform_t[2]-loc_lkneeleg_t[2])/2 #loc_lkneeleg_t[0]+(loc_lupperleg_t[0]-loc_lkneeleg_t[0])/2, loc_lkneeleg_t[1]+(loc_lupperleg_t[1]-loc_lkneeleg_t[1])/2, loc_lkneeleg_t[2]+(loc_lupperleg_t[2]-loc_lkneeleg_t[2])/2
            jnt_stretchyikcvlupperleg1grp_transform.setTranslation(jnt_stretchyikcvlupperleg1grp_transform_t, om2.MSpace.kTransform)

            jnt_stretchyiklupperleg3 = legjnt_grp.create("joint", "IkSplineLeftUpperLeg3", jnt_stretchyiklupperleg2)

            jnt_stretchyiklupperleg3_transform = om2.MFnTransform(jnt_stretchyiklupperleg3)
            jnt_stretchyiklupperleg3_transform_t = jnt_stretchyiklupperleg3_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyiklupperleg3_transform_t[0], jnt_stretchyiklupperleg3_transform_t[1], jnt_stretchyiklupperleg3_transform_t[2] = jnt_stretchyiklupperleg2_transform_t[0], jnt_stretchyiklupperleg2_transform_t[1], jnt_stretchyiklupperleg2_transform_t[2]
            jnt_stretchyiklupperleg3_transform.setTranslation(jnt_stretchyiklupperleg3_transform_t, om2.MSpace.kTransform)

            jnt_stretchyiklupperleg4 = legjnt_grp.create("joint", "IkSplineLeftUpperLeg4", jnt_stretchyiklupperleg3)
            jnt_stretchyikcvlupperleg2 = legjnt_grp.create("joint", "IkCvSplineLeftUpperLeg2", self.lupperlegikcluster2_grp)

            jnt_stretchyiklupperleg4_transform = om2.MFnTransform(jnt_stretchyiklupperleg4)
            jnt_stretchyiklupperleg4_transform_t = jnt_stretchyiklupperleg4_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyiklupperleg4_transform_t[0], jnt_stretchyiklupperleg4_transform_t[1], jnt_stretchyiklupperleg4_transform_t[2] = jnt_stretchyiklupperleg3_transform_t[0], jnt_stretchyiklupperleg3_transform_t[1], jnt_stretchyiklupperleg3_transform_t[2]
            jnt_stretchyiklupperleg4_transform.setTranslation(jnt_stretchyiklupperleg4_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikcvlupperleg2_transform = om2.MFnTransform(self.lupperlegikcluster2_grp)
            jnt_stretchyikcvlupperleg2_transform_t = jnt_stretchyikcvlupperleg2_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikcvlupperleg2_transform_t[0], jnt_stretchyikcvlupperleg2_transform_t[1], jnt_stretchyikcvlupperleg2_transform_t[2] = -(jnt_stretchyikcvlupperleg0_transform_t[0]-loc_lkneeleg_t[0]), -(jnt_stretchyikcvlupperleg0_transform_t[1]-loc_lkneeleg_t[1]), -(jnt_stretchyikcvlupperleg0_transform_t[2]-loc_lkneeleg_t[2]) #loc_lkneeleg_t[0], loc_lkneeleg_t[1], loc_lkneeleg_t[2]
            jnt_stretchyikcvlupperleg2_transform.setTranslation(jnt_stretchyikcvlupperleg2_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikllowerleg0 = legjnt_grp.create("joint", "IkSplineLeftLowerLeg0", grp_stretchyiklleg)
            jnt_stretchyikcvllowerleg0 = legjnt_grp.create("joint", "IkCvSplineLeftLowerLeg0", self.llowerlegikcluster0_grp)

            jnt_stretchyikllowerleg0_transform = om2.MFnTransform(jnt_stretchyikllowerleg0)
            jnt_stretchyikllowerleg0_transform.setTranslation(loc_lkneeleg_t-grp_stretchyiklleg_transform.translation(om2.MSpace.kTransform), om2.MSpace.kTransform)

            jnt_stretchyikcvllowerleg0_transform = om2.MFnTransform(self.llowerlegikcluster_grp)
            jnt_stretchyikcvllowerleg0_transform.setTranslation(loc_lkneeleg_t, om2.MSpace.kTransform)

            jnt_stretchyikllowerleg1 = legjnt_grp.create("joint", "IkSplineLeftLowerLeg1", jnt_stretchyikllowerleg0)

            jnt_stretchyikllowerleg1_transform = om2.MFnTransform(jnt_stretchyikllowerleg1)
            jnt_stretchyikllowerleg1_transform_t = jnt_stretchyikllowerleg1_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikllowerleg1_transform_t[0], jnt_stretchyikllowerleg1_transform_t[1], jnt_stretchyikllowerleg1_transform_t[2] = loc_lfootball_t[0]/4, loc_lfootball_t[1]/4, loc_lfootball_t[2]/4
            jnt_stretchyikllowerleg1_transform.setTranslation(jnt_stretchyikllowerleg1_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikllowerleg2 = legjnt_grp.create("joint", "IkSplineLeftLowerLeg2", jnt_stretchyikllowerleg1)
            jnt_stretchyikvcvllowerleg1 = legjnt_grp.create("joint", "IkCvSplineLeftLowerLeg1", self.llowerlegikcluster1_grp)

            jnt_stretchyikllowerleg2_transform = om2.MFnTransform(jnt_stretchyikllowerleg2)
            jnt_stretchyikllowerleg2_transform_t = jnt_stretchyikllowerleg2_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikllowerleg2_transform_t[0], jnt_stretchyikllowerleg2_transform_t[1], jnt_stretchyikllowerleg2_transform_t[2] = (loc_lfootball_t[0]/2)-jnt_stretchyikllowerleg1_transform_t[0], (loc_lfootball_t[1]/2)-jnt_stretchyikllowerleg1_transform_t[1], (loc_lfootball_t[2]/2)-jnt_stretchyikllowerleg1_transform_t[2]
            jnt_stretchyikllowerleg2_transform.setTranslation(jnt_stretchyikllowerleg2_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikcvllowerleg0_transform_t = jnt_stretchyikcvllowerleg0_transform.translation(om2.MSpace.kTransform)

            jnt_stretchyikcvllowerleg1_transform = om2.MFnTransform(self.llowerlegikcluster1_grp)
            jnt_stretchyikcvllowerleg1_transform_t = jnt_stretchyikcvllowerleg1_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikcvllowerleg1_transform_t[0], jnt_stretchyikcvllowerleg1_transform_t[1], jnt_stretchyikcvllowerleg1_transform_t[2] = -(jnt_stretchyikcvllowerleg0_transform_t[0]-loc_lfootballleg_t[0])/2, -(jnt_stretchyikcvllowerleg0_transform_t[1]-loc_lfootballleg_t[1])/2, -(jnt_stretchyikcvllowerleg0_transform_t[2]-loc_lfootballleg_t[2])/2 #loc_lfootballleg_t[0]+((loc_lkneeleg_t[0]-loc_lfootballleg_t[0])/2), loc_lfootballleg_t[1]+((loc_lkneeleg_t[1]-loc_lfootballleg_t[1])/2), loc_lfootballleg_t[2]+((loc_lkneeleg_t[2]-loc_lfootballleg_t[2])/2)
            jnt_stretchyikcvllowerleg1_transform.setTranslation(jnt_stretchyikcvllowerleg1_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikllowerleg3 = legjnt_grp.create("joint", "IkSplineLeftLowerLeg3", jnt_stretchyikllowerleg2)

            jnt_stretchyikllowerleg3_transform = om2.MFnTransform(jnt_stretchyikllowerleg3)
            jnt_stretchyikllowerleg3_transform_t = jnt_stretchyikllowerleg3_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikllowerleg3_transform_t[0], jnt_stretchyikllowerleg3_transform_t[1], jnt_stretchyikllowerleg3_transform_t[2] = jnt_stretchyikllowerleg2_transform_t[0], jnt_stretchyikllowerleg2_transform_t[1], jnt_stretchyikllowerleg2_transform_t[2]
            jnt_stretchyikllowerleg3_transform.setTranslation(jnt_stretchyikllowerleg3_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikllowerleg4 = legjnt_grp.create("joint", "IkSplineLeftLowerLeg4", jnt_stretchyikllowerleg3)
            jnt_stretchyikvcvllowerleg2 = legjnt_grp.create("joint", "IkCvSplineLeftLowerLeg2", self.llowerlegikcluster2_grp)

            jnt_stretchyikllowerleg4_transform = om2.MFnTransform(jnt_stretchyikllowerleg4)
            jnt_stretchyikllowerleg4_transform_t = jnt_stretchyikllowerleg4_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikllowerleg4_transform_t[0], jnt_stretchyikllowerleg4_transform_t[1], jnt_stretchyikllowerleg4_transform_t[2] = jnt_stretchyikllowerleg3_transform_t[0], jnt_stretchyikllowerleg3_transform_t[1], jnt_stretchyikllowerleg3_transform_t[2]
            jnt_stretchyikllowerleg4_transform.setTranslation(jnt_stretchyikllowerleg4_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikcvllowerleg4_transform = om2.MFnTransform(self.llowerlegikcluster2_grp)
            jnt_stretchyikcvllowerleg4_transform_t = jnt_stretchyikcvllowerleg4_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikcvllowerleg4_transform_t[0], jnt_stretchyikcvllowerleg4_transform_t[1], jnt_stretchyikcvllowerleg4_transform_t[2] = -(jnt_stretchyikcvllowerleg0_transform_t[0]-loc_lfootballleg_t[0]), -(jnt_stretchyikcvllowerleg0_transform_t[1]-loc_lfootballleg_t[1]), -(jnt_stretchyikcvllowerleg0_transform_t[2]-loc_lfootballleg_t[2]) #loc_lfootballleg_t[0], loc_lfootballleg_t[1], loc_lfootballleg_t[2]
            jnt_stretchyikcvllowerleg4_transform.setTranslation(jnt_stretchyikcvllowerleg4_transform_t, om2.MSpace.kTransform)

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

            grp_fkrupperleg = legjnt_grp.create("transform", "FkRightJointLeg_grp", self.jnt_root_tn)
            jnt_fkrupperleg = legjnt_grp.create("joint", "FkRightUpLeg", grp_fkrupperleg)

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
            rreversefoot_hell = legjnt_grp.create("transform", "RightReverseFootHeel", self.donttouchjnt_grp)
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
            rreversefoot_foot = legjnt_grp.create("transform", "RightReverseFootToe", self.donttouchjnt_grp)
            rreversefoot_foot_ln = legjnt_grp.create("locator", "RightReverseFootToeShape", rreversefoot_foot)
            rreverseinner_foot = legjnt_grp.create("transform", "RightReverseInnerFoot", self.donttouchjnt_grp)
            rreverseinner_foot_ln = legjnt_grp.create("locator", "RightReverseInnerFootShape", rreverseinner_foot)
            rreverseouter_foot = legjnt_grp.create("transform", "RightReverseOuterFoot", self.donttouchjnt_grp)
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
            rreversefoot_toe = legjnt_grp.create("transform", "RightReverseFootToeEnd", self.donttouchjnt_grp)
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

            grp_stretchyikrleg = legjnt_grp.create("transform", "IkStretchyRightJointLeg_grp", self.splineik_grp)

            grp_stretchyikrleg_transform = om2.MFnTransform(grp_stretchyikrleg)
            grp_stretchyikrleg_transform.setTransformation(self.loc_root_transform)

            jnt_stretchyikrupperleg0 = legjnt_grp.create("joint", "IkSplineRightUpperLeg0", grp_stretchyikrleg)
            jnt_stretchyikcvrupperleg0 = legjnt_grp.create("joint", "IkCvSplineRightUpperLeg0", self.rupperlegikcluster0_grp)

            jnt_stretchyikrupperleg0_transform = om2.MFnTransform(jnt_stretchyikrupperleg0)
            jnt_stretchyikrupperleg0_transform.setTransformation(loc_rupperleg_transform)

            jnt_stretchyikcvrupperleg0_transform = om2.MFnTransform(self.rupperlegikcluster_grp)
            jnt_stretchyikcvrupperleg0_transform.setTranslation(loc_rupperleg_t, om2.MSpace.kTransform)

            jnt_stretchyikrupperleg1 = legjnt_grp.create("joint", "IkSplineRightUpperLeg1", jnt_stretchyikrupperleg0)

            jnt_stretchyikrupperleg1_transform = om2.MFnTransform(jnt_stretchyikrupperleg1)
            jnt_stretchyikrupperleg1_transform_t = jnt_stretchyikrupperleg1_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikrupperleg1_transform_t[0], jnt_stretchyikrupperleg1_transform_t[1], jnt_stretchyikrupperleg1_transform_t[2] = loc_rknee_transform_t[0]/4, loc_rknee_transform_t[1]/4, loc_rknee_transform_t[2]/4
            jnt_stretchyikrupperleg1_transform.setTranslation(jnt_stretchyikrupperleg1_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikrupperleg2 = legjnt_grp.create("joint", "IkSplineRightUpperLeg2", jnt_stretchyikrupperleg1)
            jnt_stretchyikcvlupperleg1 = legjnt_grp.create("joint", "IkCvSplineRightUpperLeg1", self.rupperlegikcluster1_grp)

            jnt_stretchyikrupperleg2_transform = om2.MFnTransform(jnt_stretchyikrupperleg2)
            jnt_stretchyikrupperleg2_transform_t = jnt_stretchyikrupperleg2_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikrupperleg2_transform_t[0], jnt_stretchyikrupperleg2_transform_t[1], jnt_stretchyikrupperleg2_transform_t[2] = (loc_rknee_transform_t[0]/2)-jnt_stretchyikrupperleg1_transform_t[0], (loc_rknee_transform_t[1]/2)-jnt_stretchyikrupperleg1_transform_t[1], (loc_rknee_transform_t[2]/2)-jnt_stretchyikrupperleg1_transform_t[2]
            jnt_stretchyikrupperleg2_transform.setTranslation(jnt_stretchyikrupperleg2_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikcvrupperleg0_transform_t = jnt_stretchyikcvrupperleg0_transform.translation(om2.MSpace.kTransform)

            jnt_stretchyikcvrupperleg1grp_transform = om2.MFnTransform(self.rupperlegikcluster1_grp)
            jnt_stretchyikcvrupperleg1grp_transform_t = jnt_stretchyikcvrupperleg1grp_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikcvrupperleg1grp_transform_t[0], jnt_stretchyikcvrupperleg1grp_transform_t[1], jnt_stretchyikcvrupperleg1grp_transform_t[2] = -(jnt_stretchyikcvrupperleg0_transform_t[0]-loc_rkneeleg_t[0])/2, -(jnt_stretchyikcvrupperleg0_transform_t[1]-loc_rkneeleg_t[1])/2, -(jnt_stretchyikcvrupperleg0_transform_t[2]-loc_rkneeleg_t[2])/2 #loc_lkneeleg_t[0]+(loc_lupperleg_t[0]-loc_lkneeleg_t[0])/2, loc_lkneeleg_t[1]+(loc_lupperleg_t[1]-loc_lkneeleg_t[1])/2, loc_lkneeleg_t[2]+(loc_lupperleg_t[2]-loc_lkneeleg_t[2])/2
            jnt_stretchyikcvrupperleg1grp_transform.setTranslation(jnt_stretchyikcvrupperleg1grp_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikrupperleg3 = legjnt_grp.create("joint", "IkSplineRightUpperLeg3", jnt_stretchyikrupperleg2)

            jnt_stretchyikrupperleg3_transform = om2.MFnTransform(jnt_stretchyikrupperleg3)
            jnt_stretchyikrupperleg3_transform_t = jnt_stretchyikrupperleg3_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikrupperleg3_transform_t[0], jnt_stretchyikrupperleg3_transform_t[1], jnt_stretchyikrupperleg3_transform_t[2] = jnt_stretchyikrupperleg2_transform_t[0], jnt_stretchyikrupperleg2_transform_t[1], jnt_stretchyikrupperleg2_transform_t[2]
            jnt_stretchyikrupperleg3_transform.setTranslation(jnt_stretchyikrupperleg3_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikrupperleg4 = legjnt_grp.create("joint", "IkSplineRightUpperLeg4", jnt_stretchyikrupperleg3)
            jnt_stretchyikcvrupperleg2 = legjnt_grp.create("joint", "IkCvSplineRightUpperLeg2", self.rupperlegikcluster2_grp)

            jnt_stretchyikrupperleg4_transform = om2.MFnTransform(jnt_stretchyikrupperleg4)
            jnt_stretchyikrupperleg4_transform_t = jnt_stretchyikrupperleg4_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikrupperleg4_transform_t[0], jnt_stretchyikrupperleg4_transform_t[1], jnt_stretchyikrupperleg4_transform_t[2] = jnt_stretchyikrupperleg3_transform_t[0], jnt_stretchyikrupperleg3_transform_t[1], jnt_stretchyikrupperleg3_transform_t[2]
            jnt_stretchyikrupperleg4_transform.setTranslation(jnt_stretchyikrupperleg4_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikcvrupperleg2_transform = om2.MFnTransform(self.rupperlegikcluster2_grp)
            jnt_stretchyikcvrupperleg2_transform_t = jnt_stretchyikcvrupperleg2_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikcvrupperleg2_transform_t[0], jnt_stretchyikcvrupperleg2_transform_t[1], jnt_stretchyikcvrupperleg2_transform_t[2] = -(jnt_stretchyikcvrupperleg0_transform_t[0]-loc_rkneeleg_t[0]), -(jnt_stretchyikcvrupperleg0_transform_t[1]-loc_rkneeleg_t[1]), -(jnt_stretchyikcvrupperleg0_transform_t[2]-loc_rkneeleg_t[2]) #loc_lkneeleg_t[0], loc_lkneeleg_t[1], loc_lkneeleg_t[2]
            jnt_stretchyikcvrupperleg2_transform.setTranslation(jnt_stretchyikcvrupperleg2_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikrlowerleg0 = legjnt_grp.create("joint", "IkSplineRightLowerLeg0", grp_stretchyikrleg)
            jnt_stretchyikcvrlowerleg0 = legjnt_grp.create("joint", "IkCvSplineRightLowerLeg0", self.rlowerlegikcluster0_grp)

            jnt_stretchyikrlowerleg0_transform = om2.MFnTransform(jnt_stretchyikrlowerleg0)
            jnt_stretchyikrlowerleg0_transform.setTranslation(loc_rkneeleg_t-grp_stretchyikrleg_transform.translation(om2.MSpace.kTransform), om2.MSpace.kTransform)

            jnt_stretchyikcvrlowerleg0_transform = om2.MFnTransform(self.rlowerlegikcluster_grp)
            jnt_stretchyikcvrlowerleg0_transform.setTranslation(loc_rkneeleg_t, om2.MSpace.kTransform)

            jnt_stretchyikrlowerleg1 = legjnt_grp.create("joint", "IkSplineRightLowerLeg1", jnt_stretchyikrlowerleg0)

            jnt_stretchyikrlowerleg1_transform = om2.MFnTransform(jnt_stretchyikrlowerleg1)
            jnt_stretchyikrlowerleg1_transform_t = jnt_stretchyikrlowerleg1_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikrlowerleg1_transform_t[0], jnt_stretchyikrlowerleg1_transform_t[1], jnt_stretchyikrlowerleg1_transform_t[2] = loc_rfootball_t[0]/4, loc_rfootball_t[1]/4, loc_rfootball_t[2]/4
            jnt_stretchyikrlowerleg1_transform.setTranslation(jnt_stretchyikrlowerleg1_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikrlowerleg2 = legjnt_grp.create("joint", "IkSplineRightLowerLeg2", jnt_stretchyikrlowerleg1)
            jnt_stretchyikvcvrlowerleg1 = legjnt_grp.create("joint", "IkCvSplineRightLowerLeg1", self.rlowerlegikcluster1_grp)

            jnt_stretchyikrlowerleg2_transform = om2.MFnTransform(jnt_stretchyikrlowerleg2)
            jnt_stretchyikrlowerleg2_transform_t = jnt_stretchyikrlowerleg2_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikrlowerleg2_transform_t[0], jnt_stretchyikrlowerleg2_transform_t[1], jnt_stretchyikrlowerleg2_transform_t[2] = (loc_rfootball_t[0]/2)-jnt_stretchyikrlowerleg1_transform_t[0], (loc_rfootball_t[1]/2)-jnt_stretchyikrlowerleg1_transform_t[1], (loc_rfootball_t[2]/2)-jnt_stretchyikrlowerleg1_transform_t[2]
            jnt_stretchyikrlowerleg2_transform.setTranslation(jnt_stretchyikrlowerleg2_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikcvrlowerleg0_transform_t = jnt_stretchyikcvrlowerleg0_transform.translation(om2.MSpace.kTransform)

            jnt_stretchyikcvrlowerleg1_transform = om2.MFnTransform(self.rlowerlegikcluster1_grp)
            jnt_stretchyikcvrlowerleg1_transform_t = jnt_stretchyikcvrlowerleg1_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikcvrlowerleg1_transform_t[0], jnt_stretchyikcvrlowerleg1_transform_t[1], jnt_stretchyikcvrlowerleg1_transform_t[2] = -(jnt_stretchyikcvrlowerleg0_transform_t[0]-loc_rfootballleg_t[0])/2, -(jnt_stretchyikcvrlowerleg0_transform_t[1]-loc_rfootballleg_t[1])/2, -(jnt_stretchyikcvrlowerleg0_transform_t[2]-loc_rfootballleg_t[2])/2 #loc_lfootballleg_t[0]+((loc_lkneeleg_t[0]-loc_lfootballleg_t[0])/2), loc_lfootballleg_t[1]+((loc_lkneeleg_t[1]-loc_lfootballleg_t[1])/2), loc_lfootballleg_t[2]+((loc_lkneeleg_t[2]-loc_lfootballleg_t[2])/2)
            jnt_stretchyikcvrlowerleg1_transform.setTranslation(jnt_stretchyikcvrlowerleg1_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikrlowerleg3 = legjnt_grp.create("joint", "IkSplineRightLowerLeg3", jnt_stretchyikrlowerleg2)

            jnt_stretchyikrlowerleg3_transform = om2.MFnTransform(jnt_stretchyikrlowerleg3)
            jnt_stretchyikrlowerleg3_transform_t = jnt_stretchyikrlowerleg3_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikrlowerleg3_transform_t[0], jnt_stretchyikrlowerleg3_transform_t[1], jnt_stretchyikrlowerleg3_transform_t[2] = jnt_stretchyikrlowerleg2_transform_t[0], jnt_stretchyikrlowerleg2_transform_t[1], jnt_stretchyikrlowerleg2_transform_t[2]
            jnt_stretchyikrlowerleg3_transform.setTranslation(jnt_stretchyikrlowerleg3_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikrlowerleg4 = legjnt_grp.create("joint", "IkSplineRightLowerLeg4", jnt_stretchyikrlowerleg3)
            jnt_stretchyikvcvrlowerleg2 = legjnt_grp.create("joint", "IkCvSplineRightLowerLeg2", self.rlowerlegikcluster2_grp)

            jnt_stretchyikrlowerleg4_transform = om2.MFnTransform(jnt_stretchyikrlowerleg4)
            jnt_stretchyikrlowerleg4_transform_t = jnt_stretchyikrlowerleg4_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikrlowerleg4_transform_t[0], jnt_stretchyikrlowerleg4_transform_t[1], jnt_stretchyikrlowerleg4_transform_t[2] = jnt_stretchyikrlowerleg3_transform_t[0], jnt_stretchyikrlowerleg3_transform_t[1], jnt_stretchyikrlowerleg3_transform_t[2]
            jnt_stretchyikrlowerleg4_transform.setTranslation(jnt_stretchyikrlowerleg4_transform_t, om2.MSpace.kTransform)

            jnt_stretchyikcvrlowerleg4_transform = om2.MFnTransform(self.rlowerlegikcluster2_grp)
            jnt_stretchyikcvrlowerleg4_transform_t = jnt_stretchyikcvrlowerleg4_transform.translation(om2.MSpace.kTransform)
            jnt_stretchyikcvrlowerleg4_transform_t[0], jnt_stretchyikcvrlowerleg4_transform_t[1], jnt_stretchyikcvrlowerleg4_transform_t[2] = -(jnt_stretchyikcvrlowerleg0_transform_t[0]-loc_rfootballleg_t[0]), -(jnt_stretchyikcvrlowerleg0_transform_t[1]-loc_rfootballleg_t[1]), -(jnt_stretchyikcvrlowerleg0_transform_t[2]-loc_rfootballleg_t[2]) #loc_lfootballleg_t[0], loc_lfootballleg_t[1], loc_lfootballleg_t[2]
            jnt_stretchyikcvrlowerleg4_transform.setTranslation(jnt_stretchyikcvrlowerleg4_transform_t, om2.MSpace.kTransform)

    def setJointOrientation(self):
        dg_modifier = om2.MDGModifier()
        dg_n = om2.MFnDagNode()
        dg_transform = om2.MFnTransform()

        hipjoint_sl_lst = om2.MSelectionList()
        hipjoint_sl_lst.add("Root")

        spinejoint_sl_lst = om2.MSelectionList()
        spinejoint_sl_lst.add("Spine*")

        jnt_lastspine_obj = spinejoint_sl_lst.getDependNode(spinejoint_sl_lst.length()-1)

        ikspinejoint_sl_lst = om2.MSelectionList()
        ikspinejoint_sl_lst.add("IkSpine*")

        jnt_iklastspine_obj = ikspinejoint_sl_lst.getDependNode(ikspinejoint_sl_lst.length()-1)

        lhandjoint_sl_lst = om2.MSelectionList()
        lhandjoint_sl_lst.add("LeftShoulder")
        lhandjoint_sl_lst.add("LeftArm")
        lhandjoint_sl_lst.add("LeftForeArm")
        lhandjoint_sl_lst.add("LeftHand")

        jnt_lshoulder_obj = lhandjoint_sl_lst.getDependNode(0)
        jnt_lhand_obj = lhandjoint_sl_lst.getDependNode(lhandjoint_sl_lst.length()-1)

        fklhandjoint_sl_lst = om2.MSelectionList()
        fklhandjoint_sl_lst.add("LeftShoulder")
        fklhandjoint_sl_lst.add("FkLeftArm")
        fklhandjoint_sl_lst.add("FkLeftForeArm")
        fklhandjoint_sl_lst.add("FkLeftHand")

        jnt_fklhand_obj = fklhandjoint_sl_lst.getDependNode(fklhandjoint_sl_lst.length()-1)

        iklhandjoint_sl_lst = om2.MSelectionList()
        iklhandjoint_sl_lst.add("LeftShoulder")
        iklhandjoint_sl_lst.add("IkLeftArm")
        iklhandjoint_sl_lst.add("IkLeftForeArm")
        iklhandjoint_sl_lst.add("IkLeftHand")

        jnt_iklhand_obj = iklhandjoint_sl_lst.getDependNode(iklhandjoint_sl_lst.length()-1)

        iknofliplhandjoint_sl_lst = om2.MSelectionList()
        iknofliplhandjoint_sl_lst.add("LeftShoulder")
        iknofliplhandjoint_sl_lst.add("IkNoFlipLeftArm")
        iknofliplhandjoint_sl_lst.add("IkNoFlipLeftForeArm")
        iknofliplhandjoint_sl_lst.add("IkNoFlipLeftHand")

        jnt_iknofliplhand_obj = iknofliplhandjoint_sl_lst.getDependNode(iknofliplhandjoint_sl_lst.length()-1)

        ikpvlhandjoint_sl_lst = om2.MSelectionList()
        ikpvlhandjoint_sl_lst.add("LeftShoulder")
        ikpvlhandjoint_sl_lst.add("IkPVLeftArm")
        ikpvlhandjoint_sl_lst.add("IkPVLeftForeArm")
        ikpvlhandjoint_sl_lst.add("IkPVLeftHand")

        jnt_ikpvlhand_obj = ikpvlhandjoint_sl_lst.getDependNode(ikpvlhandjoint_sl_lst.length()-1)

        armupperikjoint_sl_lst = om2.MSelectionList()
        armupperikjoint_sl_lst.add("IkSplineLeftUpperArm*")
        armupperikjoint_sl_lst.add("IkSplineRightUpperArm*")

        armlowerikjoint_sl_lst = om2.MSelectionList()
        armlowerikjoint_sl_lst.add("IkSplineLeftLowerArm*")
        armlowerikjoint_sl_lst.add("IkSplineRightLowerArm*")

        lfingerjoint_sl_lst = om2.MSelectionList()
        lfingerjoint_sl_lst.add("LeftFinger*")

        rhandjoint_sl_lst = om2.MSelectionList()
        rhandjoint_sl_lst.add("RightShoulder")
        rhandjoint_sl_lst.add("RightArm")
        rhandjoint_sl_lst.add("RightForeArm")
        rhandjoint_sl_lst.add("RightHand")

        jnt_rshoulder_obj = rhandjoint_sl_lst.getDependNode(0)
        jnt_rhand_obj = rhandjoint_sl_lst.getDependNode(rhandjoint_sl_lst.length()-1)

        fkrhandjoint_sl_lst = om2.MSelectionList()
        fkrhandjoint_sl_lst.add("RightShoulder")
        fkrhandjoint_sl_lst.add("FkRightArm")
        fkrhandjoint_sl_lst.add("FkRightForeArm")
        fkrhandjoint_sl_lst.add("FkRightHand")

        jnt_fkrhand_obj = fkrhandjoint_sl_lst.getDependNode(fkrhandjoint_sl_lst.length()-1)

        ikrhandjoint_sl_lst = om2.MSelectionList()
        ikrhandjoint_sl_lst.add("RightShoulder")
        ikrhandjoint_sl_lst.add("IkRightArm")
        ikrhandjoint_sl_lst.add("IkRightForeArm")
        ikrhandjoint_sl_lst.add("IkRightHand")

        jnt_ikrhand_obj = ikrhandjoint_sl_lst.getDependNode(ikrhandjoint_sl_lst.length()-1)

        iknofliprhandjoint_sl_lst = om2.MSelectionList()
        iknofliprhandjoint_sl_lst.add("RightShoulder")
        iknofliprhandjoint_sl_lst.add("IkNoFlipRightArm")
        iknofliprhandjoint_sl_lst.add("IkNoFlipRightForeArm")
        iknofliprhandjoint_sl_lst.add("IkNoFlipRightHand")

        jnt_iknofliprhand_obj = iknofliprhandjoint_sl_lst.getDependNode(iknofliprhandjoint_sl_lst.length()-1)

        ikpvrhandjoint_sl_lst = om2.MSelectionList()
        ikpvrhandjoint_sl_lst.add("RightShoulder")
        ikpvrhandjoint_sl_lst.add("IkPVRightArm")
        ikpvrhandjoint_sl_lst.add("IkPVRightForeArm")
        ikpvrhandjoint_sl_lst.add("IkPVRightHand")

        jnt_ikpvrhand_obj = ikpvrhandjoint_sl_lst.getDependNode(ikpvrhandjoint_sl_lst.length()-1)

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
        legjoint_sl_lst.add("IkNoFlipRightUpLeg*")
        legjoint_sl_lst.add("IkNoFlipRightFoot*")
        legjoint_sl_lst.add("IkPVRightUpLeg*")
        legjoint_sl_lst.add("IkPVRightFoot*")

        legupperikjoint_sl_lst = om2.MSelectionList()
        legupperikjoint_sl_lst.add("IkSplineLeftUpperLeg*")
        legupperikjoint_sl_lst.add("IkSplineRightUpperLeg*")

        leglowerikjoint_sl_lst = om2.MSelectionList()
        leglowerikjoint_sl_lst.add("IkSplineLeftLowerLeg*")
        leglowerikjoint_sl_lst.add("IkSplineRightLowerLeg*")

        legjointknee_sl_lst = om2.MSelectionList()
        legjointknee_sl_lst.add("LeftLeg*")
        legjointknee_sl_lst.add("RightLeg*")
        legjointknee_sl_lst.add("FkLeftLeg*")
        legjointknee_sl_lst.add("FkRightLeg*")
        legjointknee_sl_lst.add("IkLeftLeg*")
        legjointknee_sl_lst.add("IkRightLeg*")
        legjointknee_sl_lst.add("IkNoFlipLeftLeg*")
        legjointknee_sl_lst.add("IkPVLeftLeg*")
        legjointknee_sl_lst.add("IkNoFlipRightLeg*")
        legjointknee_sl_lst.add("IkPVRightLeg*")

        endjoint_sl_lst = om2.MSelectionList()
        endjoint_sl_lst.add("*End")
        endjoint_sl_lst.add("RightFinger*4")
        endjoint_sl_lst.add("LeftFinger*4")
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

            for index in range(armupperikjoint_sl_lst.length()):
                jnt_active_obj = armupperikjoint_sl_lst.getDependNode(index)
                if jnt_active_obj.hasFn(om2.MFn.kJoint):
                    jnt_active_string = armupperikjoint_sl_lst.getSelectionStrings(index)
                    dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(jnt_active_string)[3:][:-3]))

            for index in range(armlowerikjoint_sl_lst.length()):
                jnt_active_obj = armlowerikjoint_sl_lst.getDependNode(index)
                if jnt_active_obj.hasFn(om2.MFn.kJoint):
                    jnt_active_string = armlowerikjoint_sl_lst.getSelectionStrings(index)
                    dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(jnt_active_string)[3:][:-3]))

            for index in range(lfingerjoint_sl_lst.length()-1):
                dg_n.setObject(jnt_lhand_obj)

                if index%4 == 0:
                    jnt_lparentfinger_obj = lfingerjoint_sl_lst.getDependNode(index)
                    dg_n.removeChild(jnt_lparentfinger_obj)

            dg_n.create("joint", "lnull", jnt_lhand_obj)
            dg_n.create("joint", "fklnull", jnt_fklhand_obj)
            dg_n.create("joint", "iklnull", jnt_iklhand_obj)
            dg_n.create("joint", "iknofliplnull", jnt_iknofliplhand_obj)
            dg_n.create("joint", "ikpvlnull", jnt_ikpvlhand_obj)
            for index in range(lhandjoint_sl_lst.length()):
                jnt_active_string = lhandjoint_sl_lst.getSelectionStrings(index)
                fkjnt_active_string = fklhandjoint_sl_lst.getSelectionStrings(index)
                ikjnt_active_string = iklhandjoint_sl_lst.getSelectionStrings(index)
                iknoflipjnt_active_string = iknofliplhandjoint_sl_lst.getSelectionStrings(index)
                ikpvjnt_active_string = ikpvlhandjoint_sl_lst.getSelectionStrings(index)
                dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(jnt_active_string)[3:][:-3]))
                dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(fkjnt_active_string)[3:][:-3]))
                dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(ikjnt_active_string)[3:][:-3]))
                dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(iknoflipjnt_active_string)[3:][:-3]))
                dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(ikpvjnt_active_string)[3:][:-3]))


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
            dg_n.create("joint", "iknofliprnull", jnt_iknofliprhand_obj)
            dg_n.create("joint", "ikpvrnull", jnt_ikpvrhand_obj)
            for index in range(rhandjoint_sl_lst.length()):
                jnt_active_string = rhandjoint_sl_lst.getSelectionStrings(index)
                fkjnt_active_string = fkrhandjoint_sl_lst.getSelectionStrings(index)
                ikjnt_active_string = ikrhandjoint_sl_lst.getSelectionStrings(index)
                iknoflipjnt_active_string = iknofliprhandjoint_sl_lst.getSelectionStrings(index)
                ikpvjnt_active_string = ikpvrhandjoint_sl_lst.getSelectionStrings(index)
                dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(jnt_active_string)[3:][:-3]))
                dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(fkjnt_active_string)[3:][:-3]))
                dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(ikjnt_active_string)[3:][:-3]))
                dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(iknoflipjnt_active_string)[3:][:-3]))
                dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient ydown -zeroScaleOrient {0}'.format(str(ikpvjnt_active_string)[3:][:-3]))

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

            for index in range(legupperikjoint_sl_lst.length()):
                jnt_active_obj = legupperikjoint_sl_lst.getDependNode(index)
                if jnt_active_obj.hasFn(om2.MFn.kJoint):
                    jnt_active_string = legupperikjoint_sl_lst.getSelectionStrings(index)
                    dg_modifier.commandToExecute('joint -e -orientJoint yzx -secondaryAxisOrient yup -zeroScaleOrient {0}'.format(str(jnt_active_string)[3:][:-3]))

            for index in range(leglowerikjoint_sl_lst.length()):
                jnt_active_obj = leglowerikjoint_sl_lst.getDependNode(index)
                if jnt_active_obj.hasFn(om2.MFn.kJoint):
                    jnt_active_string = leglowerikjoint_sl_lst.getSelectionStrings(index)
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
            dg_modifier.commandToExecute('delete "iknofliplnull"')
            dg_modifier.commandToExecute('delete "ikpvlnull"')
            dg_modifier.commandToExecute('delete "rnull"')
            dg_modifier.commandToExecute('delete "fkrnull"')
            dg_modifier.commandToExecute('delete "ikrnull"')
            dg_modifier.commandToExecute('delete "iknofliprnull"')
            dg_modifier.commandToExecute('delete "ikpvrnull"')
            dg_modifier.doIt()

            leftshoulder_r = cmds.xform("LeftShoulder", query=True, rotation=True, worldSpace=True)

            try:
                cmds.parent("IkSplineLeftUpperArm0", world=True)
                cmds.parent("IkSplineLeftLowerArm0", world=True)
            except:
                pass

            cmds.setAttr("IkStretchyLeftJointArm_grp.rotateX", leftshoulder_r[0])
            cmds.setAttr("IkStretchyLeftJointArm_grp.rotateY", leftshoulder_r[1])
            cmds.setAttr("IkStretchyLeftJointArm_grp.rotateZ", leftshoulder_r[2])

            try:
                cmds.parent("IkSplineLeftUpperArm0", "IkStretchyLeftJointArm_grp")
                cmds.parent("IkSplineLeftLowerArm0", "IkStretchyLeftJointArm_grp")
            except:
                pass

            leftarm_r = cmds.xform("LeftArm", query=True, rotation=True, worldSpace=True)

            try:
                cmds.parent("LeftUpperArmIkCluster1_grp", world=True)
                cmds.parent("LeftUpperArmIkCluster2_grp", world=True)
            except:
                pass

            cmds.setAttr("LeftUpperArmIkCluster_grp.rotateX", leftarm_r[0])
            cmds.setAttr("LeftUpperArmIkCluster_grp.rotateY", leftarm_r[1])
            cmds.setAttr("LeftUpperArmIkCluster_grp.rotateZ", leftarm_r[2])

            try:
                cmds.parent("LeftUpperArmIkCluster1_grp", "LeftUpperArmIkCluster_grp")
                cmds.parent("LeftUpperArmIkCluster2_grp", "LeftUpperArmIkCluster_grp")
            except:
                pass

            cmds.setAttr("LeftUpperArmIkCluster1_grp.rotateX", 0)
            cmds.setAttr("LeftUpperArmIkCluster1_grp.rotateY", 0)
            cmds.setAttr("LeftUpperArmIkCluster1_grp.rotateZ", 0)

            leftforearm_rx = cmds.getAttr("LeftForeArm.jointOrientX")
            leftforearm_ry = cmds.getAttr("LeftForeArm.jointOrientY")
            leftforearm_rz = cmds.getAttr("LeftForeArm.jointOrientZ")
            cmds.setAttr("LeftUpperArmIkCluster2_grp.rotateX", leftforearm_rx)
            cmds.setAttr("LeftUpperArmIkCluster2_grp.rotateY", leftforearm_ry)
            cmds.setAttr("LeftUpperArmIkCluster2_grp.rotateZ", leftforearm_rz)
            cmds.setAttr("IkSplineLeftUpperArm4.jointOrientX", 0)
            cmds.setAttr("IkSplineLeftUpperArm4.jointOrientY", 0)
            cmds.setAttr("IkSplineLeftUpperArm4.jointOrientZ", 0)

            leftforearm_r = cmds.xform("LeftForeArm", query=True, rotation=True, worldSpace=True)

            try:
                cmds.parent("LeftLowerArmIkCluster1_grp", world=True)
                cmds.parent("LeftLowerArmIkCluster2_grp", world=True)
            except:
                pass

            cmds.setAttr("LeftLowerArmIkCluster_grp.rotateX", leftforearm_r[0])
            cmds.setAttr("LeftLowerArmIkCluster_grp.rotateY", leftforearm_r[1])
            cmds.setAttr("LeftLowerArmIkCluster_grp.rotateZ", leftforearm_r[2])

            try:
                cmds.parent("LeftLowerArmIkCluster1_grp", "LeftLowerArmIkCluster_grp")
                cmds.parent("LeftLowerArmIkCluster2_grp", "LeftLowerArmIkCluster_grp")
            except:
                pass

            cmds.setAttr("LeftLowerArmIkCluster1_grp.rotateX", 0)
            cmds.setAttr("LeftLowerArmIkCluster1_grp.rotateY", 0)
            cmds.setAttr("LeftLowerArmIkCluster1_grp.rotateZ", 0)

            lefthand_rx = cmds.getAttr("LeftHand.jointOrientX")
            lefthand_ry = cmds.getAttr("LeftHand.jointOrientY")
            lefthand_rz = cmds.getAttr("LeftHand.jointOrientZ")
            cmds.setAttr("LeftLowerArmIkCluster2_grp.rotateX", lefthand_rx)
            cmds.setAttr("LeftLowerArmIkCluster2_grp.rotateY", lefthand_ry)
            cmds.setAttr("LeftLowerArmIkCluster2_grp.rotateZ", lefthand_rz)
            cmds.setAttr("IkNoFlipLeftHand.jointOrientX", lefthand_rx)
            cmds.setAttr("IkNoFlipLeftHand.jointOrientY", lefthand_ry)
            cmds.setAttr("IkNoFlipLeftHand.jointOrientZ", lefthand_rz)
            cmds.setAttr("IkPVLeftHand.jointOrientX", lefthand_rx)
            cmds.setAttr("IkPVLeftHand.jointOrientY", lefthand_ry)
            cmds.setAttr("IkPVLeftHand.jointOrientZ", lefthand_rz)
            cmds.setAttr("IkSplineLeftLowerArm4.jointOrientX", 0)
            cmds.setAttr("IkSplineLeftLowerArm4.jointOrientY", 0)
            cmds.setAttr("IkSplineLeftLowerArm4.jointOrientZ", 0)

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

            rightshoulder_r = cmds.xform("RightShoulder", query=True, rotation=True, worldSpace=True)

            try:
                cmds.parent("IkSplineRightUpperArm0", world=True)
                cmds.parent("IkSplineRightLowerArm0", world=True)
            except:
                pass

            cmds.setAttr("IkStretchyRightJointArm_grp.rotateX", rightshoulder_r[0])
            cmds.setAttr("IkStretchyRightJointArm_grp.rotateY", rightshoulder_r[1])
            cmds.setAttr("IkStretchyRightJointArm_grp.rotateZ", rightshoulder_r[2])

            try:
                cmds.parent("IkSplineRightUpperArm0", "IkStretchyRightJointArm_grp")
                cmds.parent("IkSplineRightLowerArm0", "IkStretchyRightJointArm_grp")
            except:
                pass

            rightarm_r = cmds.xform("RightArm", query=True, rotation=True, worldSpace=True)

            try:
                cmds.parent("RightUpperArmIkCluster1_grp", world=True)
                cmds.parent("RightUpperArmIkCluster2_grp", world=True)
            except:
                pass

            cmds.setAttr("RightUpperArmIkCluster_grp.rotateX", rightarm_r[0])
            cmds.setAttr("RightUpperArmIkCluster_grp.rotateY", rightarm_r[1])
            cmds.setAttr("RightUpperArmIkCluster_grp.rotateZ", rightarm_r[2])

            try:
                cmds.parent("RightUpperArmIkCluster1_grp", "RightUpperArmIkCluster_grp")
                cmds.parent("RightUpperArmIkCluster2_grp", "RightUpperArmIkCluster_grp")
            except:
                pass

            cmds.setAttr("RightUpperArmIkCluster1_grp.rotateX", 0)
            cmds.setAttr("RightUpperArmIkCluster1_grp.rotateY", 0)
            cmds.setAttr("RightUpperArmIkCluster1_grp.rotateZ", 0)

            rightforearm_rx = cmds.getAttr("RightForeArm.jointOrientX")
            rightforearm_ry = cmds.getAttr("RightForeArm.jointOrientY")
            rightforearm_rz = cmds.getAttr("RightForeArm.jointOrientZ")
            cmds.setAttr("RightUpperArmIkCluster2_grp.rotateX", rightforearm_rx)
            cmds.setAttr("RightUpperArmIkCluster2_grp.rotateY", rightforearm_ry)
            cmds.setAttr("RightUpperArmIkCluster2_grp.rotateZ", rightforearm_rz)
            cmds.setAttr("IkSplineRightUpperArm4.jointOrientX", 0)
            cmds.setAttr("IkSplineRightUpperArm4.jointOrientY", 0)
            cmds.setAttr("IkSplineRightUpperArm4.jointOrientZ", 0)

            rightforearm_r = cmds.xform("RightForeArm", query=True, rotation=True, worldSpace=True)

            try:
                cmds.parent("RightLowerArmIkCluster1_grp", world=True)
                cmds.parent("RightLowerArmIkCluster2_grp", world=True)
            except:
                pass

            cmds.setAttr("RightLowerArmIkCluster_grp.rotateX", rightforearm_r[0])
            cmds.setAttr("RightLowerArmIkCluster_grp.rotateY", rightforearm_r[1])
            cmds.setAttr("RightLowerArmIkCluster_grp.rotateZ", rightforearm_r[2])

            try:
                cmds.parent("RightLowerArmIkCluster1_grp", "RightLowerArmIkCluster_grp")
                cmds.parent("RightLowerArmIkCluster2_grp", "RightLowerArmIkCluster_grp")
            except:
                pass

            cmds.setAttr("RightLowerArmIkCluster1_grp.rotateX", 0)
            cmds.setAttr("RightLowerArmIkCluster1_grp.rotateY", 0)
            cmds.setAttr("RightLowerArmIkCluster1_grp.rotateZ", 0)

            righthand_rx = cmds.getAttr("RightHand.jointOrientX")
            righthand_ry = cmds.getAttr("RightHand.jointOrientY")
            righthand_rz = cmds.getAttr("RightHand.jointOrientZ")
            cmds.setAttr("RightLowerArmIkCluster2_grp.rotateX", righthand_rx)
            cmds.setAttr("RightLowerArmIkCluster2_grp.rotateY", righthand_ry)
            cmds.setAttr("RightLowerArmIkCluster2_grp.rotateZ", righthand_rz)
            cmds.setAttr("IkNoFlipRightHand.jointOrientX", righthand_rx)
            cmds.setAttr("IkNoFlipRightHand.jointOrientY", righthand_ry)
            cmds.setAttr("IkNoFlipRightHand.jointOrientZ", righthand_rz)
            cmds.setAttr("IkPVRightHand.jointOrientX", righthand_rx)
            cmds.setAttr("IkPVRightHand.jointOrientY", righthand_ry)
            cmds.setAttr("IkPVRightHand.jointOrientZ", righthand_rz)
            cmds.setAttr("IkSplineRightLowerArm4.jointOrientX", 0)
            cmds.setAttr("IkSplineRightLowerArm4.jointOrientY", 0)
            cmds.setAttr("IkSplineRightLowerArm4.jointOrientZ", 0)

            rightupperlegikcluster_r = cmds.xform("RightUpLeg", query=True, rotation=True, worldSpace=True)

            try:
                cmds.parent("RightUpperLegIkCluster1_grp", world=True)
                cmds.parent("RightUpperLegIkCluster2_grp", world=True)
            except:
                pass

            cmds.setAttr("RightUpperLegIkCluster_grp.rotateX", rightupperlegikcluster_r[0])
            cmds.setAttr("RightUpperLegIkCluster_grp.rotateY", rightupperlegikcluster_r[1])
            cmds.setAttr("RightUpperLegIkCluster_grp.rotateZ", rightupperlegikcluster_r[2])

            try:
                cmds.parent("RightUpperLegIkCluster1_grp", "RightUpperLegIkCluster_grp")
                cmds.parent("RightUpperLegIkCluster2_grp", "RightUpperLegIkCluster_grp")
            except:
                pass

            cmds.setAttr("RightUpperLegIkCluster1_grp.rotateX", 0)
            cmds.setAttr("RightUpperLegIkCluster1_grp.rotateY", 0)
            cmds.setAttr("RightUpperLegIkCluster1_grp.rotateZ", 0)

            ikcvsplinerightupperleg2_rx = cmds.getAttr("RightLeg.jointOrientX")
            ikcvsplinerightupperleg2_ry = cmds.getAttr("RightLeg.jointOrientY")
            ikcvsplinerightupperleg2_rz = cmds.getAttr("RightLeg.jointOrientZ")
            cmds.setAttr("RightUpperLegIkCluster2_grp.rotateX", ikcvsplinerightupperleg2_rx)
            cmds.setAttr("RightUpperLegIkCluster2_grp.rotateY", ikcvsplinerightupperleg2_ry)
            cmds.setAttr("RightUpperLegIkCluster2_grp.rotateZ", ikcvsplinerightupperleg2_rz)
            cmds.setAttr("IkSplineRightUpperLeg4.jointOrientX", 0)
            cmds.setAttr("IkSplineRightUpperLeg4.jointOrientY", 0)
            cmds.setAttr("IkSplineRightUpperLeg4.jointOrientZ", 0)

            rightlowerlegikcluster_r = cmds.xform("RightLeg", query=True, rotation=True, worldSpace=True)

            try:
                cmds.parent("RightLowerLegIkCluster1_grp", world=True)
                cmds.parent("RightLowerLegIkCluster2_grp", world=True)
            except:
                pass

            cmds.setAttr("RightLowerLegIkCluster_grp.rotateX", rightlowerlegikcluster_r[0])
            cmds.setAttr("RightLowerLegIkCluster_grp.rotateY", rightlowerlegikcluster_r[1])
            cmds.setAttr("RightLowerLegIkCluster_grp.rotateZ", rightlowerlegikcluster_r[2])

            try:
                cmds.parent("RightLowerLegIkCluster1_grp", "RightLowerLegIkCluster_grp")
                cmds.parent("RightLowerLegIkCluster2_grp", "RightLowerLegIkCluster_grp")
            except:
                pass

            cmds.setAttr("RightLowerLegIkCluster1_grp.rotateX", 0)
            cmds.setAttr("RightLowerLegIkCluster1_grp.rotateY", 0)
            cmds.setAttr("RightLowerLegIkCluster1_grp.rotateZ", 0)

            ikcvsplinerightlowerleg2_rx = cmds.getAttr("RightFoot.jointOrientX")
            ikcvsplinerightlowerleg2_ry = cmds.getAttr("RightFoot.jointOrientY")
            ikcvsplinerightlowerleg2_rz = cmds.getAttr("RightFoot.jointOrientZ")
            cmds.setAttr("RightLowerLegIkCluster2_grp.rotateX", ikcvsplinerightlowerleg2_rx)
            cmds.setAttr("RightLowerLegIkCluster2_grp.rotateY", ikcvsplinerightlowerleg2_ry)
            cmds.setAttr("RightLowerLegIkCluster2_grp.rotateZ", ikcvsplinerightlowerleg2_rz)
            cmds.setAttr("IkNoFlipRightFoot.jointOrientX", ikcvsplinerightlowerleg2_rx)
            cmds.setAttr("IkNoFlipRightFoot.jointOrientY", ikcvsplinerightlowerleg2_ry)
            cmds.setAttr("IkNoFlipRightFoot.jointOrientZ", ikcvsplinerightlowerleg2_rz)
            cmds.setAttr("IkPVRightFoot.jointOrientX", ikcvsplinerightlowerleg2_rx)
            cmds.setAttr("IkPVRightFoot.jointOrientY", ikcvsplinerightlowerleg2_ry)
            cmds.setAttr("IkPVRightFoot.jointOrientZ", ikcvsplinerightlowerleg2_rz)
            cmds.setAttr("IkSplineRightLowerLeg4.jointOrientX", 0)
            cmds.setAttr("IkSplineRightLowerLeg4.jointOrientY", 0)
            cmds.setAttr("IkSplineRightLowerLeg4.jointOrientZ", 0)

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

        try:
            if cmds.objExists("NoFlipLeftHand_Ik") and cmds.objExists("NoFlipLeftHand_effector"):

                cmds.delete("NoFlipLeftHand_Ik")
                cmds.delete("PVLeftHand_Ik")
        except:
            pass

        if index == 0 :

            try:
                cmds.delete("NoFlipLeftHand_effector")
                cmds.delete("PVLeftHand_effector")
            except:
                pass

            print("All Ik Removed")

        elif index == 1 :

            try:
                self.IKSolver1_lst.add("ikRPsolver*")
            except:
                cmds.createNode("ikRPsolver")

            self.MDG1_mod.commandToExecute('ikHandle -name "NoFlipLeftHand_Ik" -startJoint "IkNoFlipLeftArm" -endEffector "IkNoFlipLeftHand" -solver "ikRPsolver"')
            self.MDG1_mod.commandToExecute('rename effector1 NoFlipLeftHand_effector')
            self.MDG1_mod.commandToExecute('ikHandle -name "PVLeftHand_Ik" -startJoint "IkPVLeftArm" -endEffector "IkPVLeftHand" -solver "ikRPsolver"')
            self.MDG1_mod.commandToExecute('rename effector1 PVLeftHand_effector')
            self.MDG1_mod.commandToExecute('parent NoFlipLeftHand_Ik DoNotTouch')
            self.MDG1_mod.commandToExecute('parent PVLeftHand_Ik DoNotTouch')
            self.MDG1_mod.doIt()

    def createRHandIK(self, index):

        try:
            if cmds.objExists("RightHand_Ik") and cmds.objExists("RightHand_effector"):

                cmds.delete("NoFlipRightHand_Ik")
                cmds.delete("PVRightHand_Ik")
        except:
            pass

        if index == 0 :

            try:
                cmds.delete("NoFlipRightHand_effector")
                cmds.delete("PVRightHand_effector")
            except:
                pass

            print("All Ik Removed")

        elif index == 1 :

            try:
                self.IKSolver1_lst.add("ikRPsolver*")
            except:
                cmds.createNode("ikRPsolver")

            self.MDG1_mod.commandToExecute('ikHandle -name "NoFlipRightHand_Ik" -startJoint "IkNoFlipRightArm" -endEffector "IkNoFlipRightHand" -solver "ikRPsolver"')
            self.MDG1_mod.commandToExecute('rename effector1 NoFlipRightHand_effector')
            self.MDG1_mod.commandToExecute('ikHandle -name "PVRightHand_Ik" -startJoint "IkPVRightArm" -endEffector "IkPVRightHand" -solver "ikRPsolver"')
            self.MDG1_mod.commandToExecute('rename effector1 PVRightHand_effector')
            self.MDG1_mod.commandToExecute('parent NoFlipRightHand_Ik DoNotTouch')
            self.MDG1_mod.commandToExecute('parent PVRightHand_Ik DoNotTouch')
            self.MDG1_mod.doIt()

    def createLlegIk(self, index):

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
        llegfoot_path = lleg_pathnode.getAPathTo(obj_foot)
        llegtoe_path = lleg_pathnode.getAPathTo(obj_toe)

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

            self.MDG1_mod.commandToExecute('parent LeftReverseFootToe DoNotTouch')
            self.MDG1_mod.commandToExecute('parent LeftReverseFootToeEnd DoNotTouch')
            self.MDG1_mod.commandToExecute('parent LeftReverseInnerFoot DoNotTouch')
            self.MDG1_mod.commandToExecute('parent LeftReverseOuterFoot DoNotTouch')
            self.MDG1_mod.doIt()

            print("All Ik Removed")

        elif index == 1:
            try:
                self.IKSolver1_lst.add("ikRPsolver*")
            except:
                cmds.createNode("ikRPsolver")

            rp_solver = self.IK_System.findSolver("ikRPsolver")

            self.llegtoe_effector = self.IK_Effector.create(obj_toe)
            llegtoe_effector_path = lleg_pathnode.getAPathTo(self.llegtoe_effector)

            self.llegtoeend_effector = self.IK_Effector.create(obj_toeend)
            llegtoeend_effector_path = lleg_pathnode.getAPathTo(self.llegtoeend_effector)

            self.llegtoe_ik = self.IK_Handle.create(llegfoot_path, llegtoe_effector_path)
            self.IK_Handle.setSolver(rp_solver)

            self.llegtoeend_ik = self.IK_Handle.create(llegtoe_path, llegtoeend_effector_path)
            self.IK_Handle.setSolver(rp_solver)

            self.MDG1_mod.renameNode(self.llegtoe_ik, "LeftLegFoot_Ik")
            self.MDG1_mod.renameNode(self.llegtoeend_ik, "LeftLegToe_Ik")
            self.MDG1_mod.renameNode(self.llegtoe_effector, "LeftFoot_effector")
            self.MDG1_mod.renameNode(self.llegtoeend_effector, "LeftToe_effector")
            self.MDG1_mod.commandToExecute('ikHandle -name "PVLeftLeg_Ik" -startJoint "IkPVLeftUpLeg" -endEffector "IkPVLeftFoot" -solver "ikRPsolver"')
            self.MDG1_mod.commandToExecute('rename effector1 PVLeftLeg_effector')
            self.MDG1_mod.commandToExecute('ikHandle -name "NoFlipLeftLeg_Ik" -startJoint "IkNoFlipLeftUpLeg" -endEffector "IkNoFlipLeftFoot" -solver "ikRPsolver"')
            self.MDG1_mod.commandToExecute('rename effector1 NoFlipLeftLeg_effector')
            self.MDG1_mod.commandToExecute('parent LeftReverseFootToe LeftReverseFootToeEnd')
            self.MDG1_mod.commandToExecute('parent LeftReverseFootToeEnd LeftReverseInnerFoot')
            self.MDG1_mod.commandToExecute('parent LeftReverseInnerFoot LeftReverseOuterFoot')
            self.MDG1_mod.commandToExecute('parent LeftReverseOuterFoot LeftReverseFootHeel')
            self.MDG1_mod.commandToExecute('parent PVLeftLeg_Ik LeftReverseFootToe')
            self.MDG1_mod.commandToExecute('parent NoFlipLeftLeg_Ik LeftReverseFootToe')
            self.MDG1_mod.commandToExecute('parent LeftLegFoot_Ik LeftReverseFootToe')
            self.MDG1_mod.commandToExecute('parent LeftLegToe_Ik LeftReverseFootToeWiggle')
            self.MDG1_mod.commandToExecute('parent LeftFoot_effector IkLeftFoot')
            self.MDG1_mod.commandToExecute('parent LeftToe_effector IkLeftToeBase')
            self.MDG1_mod.doIt()

    def createRlegIk(self, index):

        obj_upleg = om1.MObject()
        obj_foot = om1.MObject()
        obj_toe = om1.MObject()
        obj_toeend = om1.MObject()

        rleg_sl_lst = om1.MSelectionList()
        rleg_sl_lst.add("IkRightFoot")
        rleg_sl_lst.add("IkRightToeBase")
        rleg_sl_lst.add("IkRightToeEnd")
        rleg_sl_lst.getDependNode(0, obj_foot)
        rleg_sl_lst.getDependNode(1, obj_toe)
        rleg_sl_lst.getDependNode(rleg_sl_lst.length()-1, obj_toeend)

        rleg_pathnode = om1.MDagPath()
        rlegfoot_path = rleg_pathnode.getAPathTo(obj_foot)
        rlegtoe_path = rleg_pathnode.getAPathTo(obj_toe)

        try:
            if cmds.objExists("NoFlipRightLeg_Ik") and cmds.objExists("NoFlipRightLeg_effector"):

                cmds.delete("NoFlipRightLeg_Ik")
                cmds.delete("PVRightLeg_Ik")
                cmds.delete("RightLegFoot_Ik")
                cmds.delete("RightLegToe_Ik")

        except:
            pass

        if index == 0:
            try:
                cmds.delete("NoFlipRightLeg_effector")
                cmds.delete("PVRightLeg_effector")
            except:
                pass

            self.MDG1_mod.commandToExecute('parent RightReverseFootToe DoNotTouch')
            self.MDG1_mod.commandToExecute('parent RightReverseFootToeEnd DoNotTouch')
            self.MDG1_mod.commandToExecute('parent RightReverseInnerFoot DoNotTouch')
            self.MDG1_mod.commandToExecute('parent RightReverseOuterFoot DoNotTouch')
            self.MDG1_mod.doIt()

            print("All Ik Removed")

        elif index == 1:
            try:
                self.IKSolver1_lst.add("ikRPsolver*")
            except:
                cmds.createNode("ikRPsolver")

            rp_solver = self.IK_System.findSolver("ikRPsolver")

            self.rlegtoe_effector = self.IK_Effector.create(obj_toe)
            rlegtoe_effector_path = rleg_pathnode.getAPathTo(self.rlegtoe_effector)

            self.rlegtoeend_effector = self.IK_Effector.create(obj_toeend)
            rlegtoeend_effector_path = rleg_pathnode.getAPathTo(self.rlegtoeend_effector)

            self.rlegtoe_ik = self.IK_Handle.create(rlegfoot_path, rlegtoe_effector_path)
            self.IK_Handle.setSolver(rp_solver)

            self.rlegtoeend_ik = self.IK_Handle.create(rlegtoe_path, rlegtoeend_effector_path)
            self.IK_Handle.setSolver(rp_solver)

            self.MDG1_mod.renameNode(self.rlegtoe_ik, "RightLegFoot_Ik")
            self.MDG1_mod.renameNode(self.rlegtoeend_ik, "RightLegToe_Ik")
            self.MDG1_mod.renameNode(self.rlegtoe_effector, "RightFoot_effector")
            self.MDG1_mod.renameNode(self.rlegtoeend_effector, "RightToe_effector")
            self.MDG1_mod.commandToExecute('ikHandle -name "PVRightLeg_Ik" -startJoint "IkPVRightUpLeg" -endEffector "IkPVRightFoot" -solver "ikRPsolver"')
            self.MDG1_mod.commandToExecute('rename effector1 PVRightLeg_effector')
            self.MDG1_mod.commandToExecute('ikHandle -name "NoFlipRightLeg_Ik" -startJoint "IkNoFlipRightUpLeg" -endEffector "IkNoFlipRightFoot" -solver "ikRPsolver"')
            self.MDG1_mod.commandToExecute('rename effector1 NoFlipRightLeg_effector')
            self.MDG1_mod.commandToExecute('parent RightReverseFootToe RightReverseFootToeEnd')
            self.MDG1_mod.commandToExecute('parent RightReverseFootToeEnd RightReverseInnerFoot')
            self.MDG1_mod.commandToExecute('parent RightReverseInnerFoot RightReverseOuterFoot')
            self.MDG1_mod.commandToExecute('parent RightReverseOuterFoot RightReverseFootHeel')
            self.MDG1_mod.commandToExecute('parent PVRightLeg_Ik RightReverseFootToe')
            self.MDG1_mod.commandToExecute('parent NoFlipRightLeg_Ik RightReverseFootToe')
            self.MDG1_mod.commandToExecute('parent RightLegFoot_Ik RightReverseFootToe')
            self.MDG1_mod.commandToExecute('parent RightLegToe_Ik RightReverseFootToeWiggle')
            self.MDG1_mod.commandToExecute('parent RightFoot_effector IkRightFoot')
            self.MDG1_mod.commandToExecute('parent RightToe_effector IkRightToeBase')
            self.MDG1_mod.doIt()

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
        self.MNurbs2_cv = om2.MFnNurbsCurve()
        self.MDG2_mod = om2.MDGModifier()
        self.MDag2_node = om2.MFnDagNode()

        obj_sl_lst = om2.MSelectionList()
        obj_sl_lst.add("boundingBox")
        box_obj = obj_sl_lst.getDependNode(0)

        self.box_transform = om2.MFnTransform(box_obj)
        box_transform_s = self.box_transform.scale()

        ctrl_master_circle_points = [om2.MPoint(0.75, 0.0, 0.25), om2.MPoint(0.0, 0.0, 1.0), om2.MPoint(-1.0, 0.0), om2.MPoint(0.0, 0.0, -1.0), om2.MPoint(0.75, 0.0, -0.25)]
        ctrl_master_arrow_points = [om2.MPoint(0.75, 0.0, -0.25), om2.MPoint(1.50, 0.0, -0.50), om2.MPoint(1.50, 0.0, -0.65), om2.MPoint(2.0, 0.0, 0.0), om2.MPoint(1.50, 0.0, 0.65), om2.MPoint(1.50, 0.0, 0.50), om2.MPoint(0.75, 0.0, 0.25)]

        self.globalctrl_tn =  self.MDag2_node.create("transform", "Biped_ctrl_grp")
        self.draw_global_tn = self.MDag2_node.create("transform", "Draw_global_ctrl")
        crv_ctrl_master_circle = self.MNurbs2_cv.createWithEditPoints(ctrl_master_circle_points, 3, 1, False, True, True, self.draw_global_tn)
        crv_ctrl_master_arrow = self.MNurbs2_cv.createWithEditPoints(ctrl_master_arrow_points, 1, 1, False, True, True, self.draw_global_tn)

        self.masterctrl_tn = self.MDag2_node.create("transform", "Biped_Master_ctrl", self.globalctrl_tn)
        ctrl_global_comb_cv = self.MNurbs2_cv.create([crv_ctrl_master_circle, crv_ctrl_master_arrow], self.masterctrl_tn)

        masctrl_transform = om2.MFnTransform(self.masterctrl_tn)
        masctrl_transform_s = masctrl_transform.findPlug("scale", False)

        if masctrl_transform_s.isCompound:
            for i in range(masctrl_transform_s.numChildren()):
                child_plug = masctrl_transform_s.child(i)
                attr_value = child_plug.setDouble(box_transform_s[2])

        masctrl_transform_r = masctrl_transform.rotation(om2.MSpace.kTransform)
        masctrl_transform_r[1] = -1.57079
        masctrl_transform.setRotation(masctrl_transform_r, om2.MSpace.kTransform)

        self.MDG2_mod.commandToExecute('delete "Draw_global_ctrl"')
        self.MDG2_mod.renameNode(ctrl_global_comb_cv, "Master_shape")
        self.MDG2_mod.commandToExecute('color -rgbColor 0.5 1 0 "Biped_Master_ctrl"')
        self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_Master_ctrl"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_ctrl_grp.translateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_ctrl_grp.translateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_ctrl_grp.translateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_ctrl_grp.rotateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_ctrl_grp.rotateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_ctrl_grp.rotateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_ctrl_grp.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_ctrl_grp.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_ctrl_grp.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_ctrl_grp.visibility"')
        self.MDG2_mod.commandToExecute('addAttr -longName "globalscale" -niceName "Global Scale" -attributeType double -keyable true -defaultValue 1 Biped_Master_ctrl')
        self.MDG2_mod.commandToExecute('connectAttr -force Biped_Master_ctrl.globalscale Biped_Master_ctrl.scaleX')
        self.MDG2_mod.commandToExecute('connectAttr -force Biped_Master_ctrl.globalscale Biped_Master_ctrl.scaleY')
        self.MDG2_mod.commandToExecute('connectAttr -force Biped_Master_ctrl.globalscale Biped_Master_ctrl.scaleZ')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Master_ctrl.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Master_ctrl.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Master_ctrl.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_Master_ctrl.visibility"')
        self.MDG2_mod.doIt()

        ctrl_root_points = [om2.MPoint(0.75, 0.2, 0.0), om2.MPoint(0.75, 0.0, 0.50), om2.MPoint(0.0, 1, 1), om2.MPoint(-0.75, 0.0, 0.50), om2.MPoint(-0.75, 0.2, 0.0), om2.MPoint(-0.75, 0.0, -0.50), om2.MPoint(0.0, 1, -1), om2.MPoint(0.75, 0.0, -0.50), om2.MPoint(0.75, 0.2, 0.0)]

        self.rootnull_tn = self.MDag2_node.create("transform", "Biped_Root_null", self.masterctrl_tn)
        self.rootctrl_tn = self.MDag2_node.create("transform", "Biped_Root_ctrl", self.rootnull_tn)
        crv_ctrl_root = self.MNurbs2_cv.createWithEditPoints(ctrl_root_points, 3, 1, False, True, True, self.rootctrl_tn)

        ctrl_hip_line_points = [om2.MPoint(0.75, 0.00, -0.75), om2.MPoint(0.75, 0.00, 0.75), om2.MPoint(0.75, 0.00, 0.00), om2.MPoint(-0.75, 0.00), om2.MPoint(-0.75, 0.00, 0.75), om2.MPoint(-0.75, 0.00, -0.75)]
        ctrl_hip_arcback_points = [om2.MPoint(0.75, 0.00, -0.75), om2.MPoint(1, 0.5, 0.00), om2.MPoint(0.75, 0.00, 0.75)]
        ctrl_hip_linefront_points = [om2.MPoint(-0.75, 0.00, -0.75), om2.MPoint(-1, 0.5, 0.00), om2.MPoint(-0.75, 0.00, 0.75)]

        obj_sl_lst.add("Root")
        root_obj = obj_sl_lst.getDependNode(1)
        jnt_root_transform = om2.MFnTransform(root_obj)
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

        self.MDG2_mod.renameNode(crv_ctrl_root, "Root_shape")
        self.MDG2_mod.commandToExecute('color -rgbColor 1 0 0 "Biped_Root_ctrl"')
        self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_Root_ctrl"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_null.translateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_null.translateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_null.translateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_null.rotateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_null.rotateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_null.rotateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_null.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_null.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_null.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_null.visibility"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_ctrl.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_ctrl.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Root_ctrl.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_Root_ctrl.visibility"')
        self.MDG2_mod.doIt()

        if self.hipjnt.currentIndex() == 1:
            jnt_hip = self.MDag2_node.create("joint", "Hip", root_obj)

            self.hipctrl_tn = self.MDag2_node.create("transform", "Biped_Hip_ctrl", self.rootctrl_tn)
            crv_ctrl_hip_line = self.MNurbs2_cv.createWithEditPoints(ctrl_hip_line_points, 1, 1, False, True, True, self.hipctrl_tn)
            crv_ctrl_hip_arcback = self.MNurbs2_cv.createWithEditPoints(ctrl_hip_arcback_points, 3, 1, False, True, True, self.hipctrl_tn)
            crv_ctrl_hip_linefront = self.MNurbs2_cv.createWithEditPoints(ctrl_hip_linefront_points, 3, 1, False, True, True, self.hipctrl_tn)

            hipctrl_transform = om2.MFnTransform(self.hipctrl_tn)
            hipctrl_transform_r = hipctrl_transform.rotation(om2.MSpace.kTransform)
            hipctrl_transform_r[0] = 3.1415
            hipctrl_transform.setRotation(hipctrl_transform_r, om2.MSpace.kTransform)

            hipctrl_transform_s = hipctrl_transform.findPlug("scale", False)
            if hipctrl_transform_s.isCompound:
                for i in range(hipctrl_transform_s.numChildren()):
                    child_plug = hipctrl_transform_s.child(i)
                    attr_value = child_plug.setDouble(box_transform_s[0]/2)

            self.MDG2_mod.renameNode(crv_ctrl_hip_line, "HipLine_shape")
            self.MDG2_mod.renameNode(crv_ctrl_hip_arcback, "HipArcRight_shape")
            self.MDG2_mod.renameNode(crv_ctrl_hip_linefront, "HipArcLeft_shape")
            self.MDG2_mod.commandToExecute('color -rgbColor 0 1 0 "Biped_Hip_ctrl"')
            self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_Hip_ctrl"')
            self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Hip_ctrl.translateX"')
            self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Hip_ctrl.translateY"')
            self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Hip_ctrl.translateZ"')
            self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Hip_ctrl.scaleX"')
            self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Hip_ctrl.scaleY"')
            self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Hip_ctrl.scaleZ"')
            self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Hip_ctrl.visibility"')
            self.MDG2_mod.commandToExecute('parent LeftJointLeg_grp Hip')
            self.MDG2_mod.commandToExecute('parent FkLeftJointLeg_grp Hip')
            self.MDG2_mod.commandToExecute('parent IkLeftJointLeg_grp Hip')
            self.MDG2_mod.commandToExecute('parent RightJointLeg_grp Hip')
            self.MDG2_mod.commandToExecute('parent FkRightJointLeg_grp Hip')
            self.MDG2_mod.commandToExecute('parent IkRightJointLeg_grp Hip')
            self.MDG2_mod.doIt()

        spine_sl_lst = om2.MSelectionList()
        spine_sl_lst.add("Spine*")

        ctrl_spine_line_l_points = [om2.MPoint(0.50, 0.00, 0.25), om2.MPoint(0.50, 0.05, 0.25), om2.MPoint(0.50, 0.00, 0.20), om2.MPoint(-0.50, 0.00, 0.20), om2.MPoint(-0.50, 0.05, 0.25), om2.MPoint(-0.50, 0.00, 0.25)]
        ctrl_spine_line_r_points = [om2.MPoint(-0.50, 0.00, -0.25), om2.MPoint(-0.50, 0.05, -0.25), om2.MPoint(-0.50, 0.00, -0.20), om2.MPoint(0.50, 0.00, -0.20), om2.MPoint(0.50, 0.05, -0.25), om2.MPoint(0.50, 0.00, -0.25) ]
        ctrl_spine_curve_fl_points = [om2.MPoint(0.50, -0.15, 0.00), om2.MPoint(0.50, -0.06, 0.10), om2.MPoint(0.50, 0.00, 0.25)]
        ctrl_spine_curve_fr_points = [om2.MPoint(0.50, 0.00, -0.25), om2.MPoint(0.50, -0.06, -0.10), om2.MPoint(0.50, -0.15, 0.00)]
        ctrl_spine_curve_b_points = [om2.MPoint(-0.50, 0.00, 0.25), om2.MPoint(-0.50, -0.06, 0.10), om2.MPoint(-0.50, -0.15, 0.00), om2.MPoint(-0.50, -0.06, -0.10),  om2.MPoint(-0.50, 0.00, -0.25)]

        self.draw_spine_tn = self.MDag2_node.create("transform", "Draw_Spine_ctrl")
        crv_ctrl_spine_line_l = self.MNurbs2_cv.createWithEditPoints(ctrl_spine_line_l_points, 1, 1, False, True, True, self.draw_spine_tn)
        crv_ctrl_spine_line_r = self.MNurbs2_cv.createWithEditPoints(ctrl_spine_line_r_points, 1, 1, False, True, True, self.draw_spine_tn)
        crv_ctrl_spine_curve_fl = self.MNurbs2_cv.createWithEditPoints(ctrl_spine_curve_fl_points, 3, 1, False, True, True, self.draw_spine_tn)
        crv_ctrl_spine_curve_fr = self.MNurbs2_cv.createWithEditPoints(ctrl_spine_curve_fr_points, 3, 1, False, True, True, self.draw_spine_tn)
        crv_ctrl_spine_curve_b = self.MNurbs2_cv.createWithEditPoints(ctrl_spine_curve_b_points, 3, 1, False, True, True, self.draw_spine_tn)

        ctrl_stretchyspine_circle_points = [om2.MPoint(0.70, 0.00, 0.00), om2.MPoint(0.00, -0.20, 0.70), om2.MPoint(-0.70, 0.00, 0.00), om2.MPoint(0.00, -0.20, -0.70), om2.MPoint(0.70, 0.00, 0.00)]

        for index in range(spine_sl_lst.length()):
            if index == 0:
                self.spinenull_tn = self.MDag2_node.create("transform", "Biped_Spine"+str(index)+"_null", self.rootctrl_tn)
                self.spinectrl_tn = self.MDag2_node.create("transform", "Biped_Spine"+str(index)+"_ctrl", self.spinenull_tn)
                ctrl_spine_comb_cv = self.MNurbs2_cv.create([crv_ctrl_spine_curve_fl, crv_ctrl_spine_line_l, crv_ctrl_spine_curve_b, crv_ctrl_spine_line_r, crv_ctrl_spine_curve_fr], self.spinectrl_tn)

            else:
                self.spinenull_tn = self.MDag2_node.create("transform", "Biped_Spine"+str(index)+"_null")
                self.spinectrl_tn = self.MDag2_node.create("transform", "Biped_Spine"+str(index)+"_ctrl", self.spinenull_tn)
                ctrl_spine_comb_cv = self.MNurbs2_cv.create([crv_ctrl_spine_curve_fl, crv_ctrl_spine_line_l, crv_ctrl_spine_curve_b, crv_ctrl_spine_line_r, crv_ctrl_spine_curve_fr], self.spinectrl_tn)

            if index == spine_sl_lst.length()-1:
                self.stretchyspine_tn = self.MDag2_node.create("transform", "Biped_StretchySpine_ctrl", self.spinectrl_tn)
                crv_ctrl_stretchyspine = self.MNurbs2_cv.createWithEditPoints(ctrl_stretchyspine_circle_points, 3, 1, False, True, True, self.stretchyspine_tn)

                self.MDG2_mod.renameNode(crv_ctrl_stretchyspine, "StretchySpine_shape")

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
            self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_Spine{0}_ctrl"'.format(index))
            self.MDG2_mod.doIt()

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

            self.MDG2_mod.renameNode(ctrl_spine_comb_cv, "Spine" + str(index) + "_shape")
            self.MDG2_mod.commandToExecute('color -rgbColor 1 1 0 "Biped_Spine{0}_ctrl"'.format(index))
            self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_Spine{0}_ctrl"'.format(index))
            self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_null.translateX"'.format(index))
            self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_null.translateY"'.format(index))
            self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_null.translateZ"'.format(index))
            self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_null.rotateX"'.format(index))
            self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_null.rotateY"'.format(index))
            self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_null.rotateZ"'.format(index))
            self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_null.scaleX"'.format(index))
            self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_null.scaleY"'.format(index))
            self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_null.scaleZ"'.format(index))
            self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_null.visibility"'.format(index))
            self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_ctrl.scaleX"'.format(index))
            self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_ctrl.scaleY"'.format(index))
            self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Spine{0}_ctrl.scaleZ"'.format(index))
            self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_Spine{0}_ctrl.visibility"'.format(index))

        self.MDG2_mod.commandToExecute('color -rgbColor 1 0 0 "Biped_StretchySpine_ctrl"')
        self.MDG2_mod.commandToExecute('delete "Draw_Spine_ctrl"')
        self.MDG2_mod.doIt()

        head_sl_ls = om2.MSelectionList()
        head_sl_ls.add("Neck")
        head_sl_ls.add("Head")
        head_sl_ls.add("HeadTopEnd")

        ctrl_neck_line_up_points = [om2.MPoint(0.00, 0.05, 0.02), om2.MPoint(0.60, 0.05, 0.02)]
        ctrl_neck_star_up_points = [om2.MPoint(0.60, 0.05, 0.02), om2.MPoint(0.70, 0.15, 0.20), om2.MPoint(0.70, 0.09, 0.20), om2.MPoint(0.70, 0.06, 0.13), om2.MPoint(0.60, 0.00, 0.00), om2.MPoint(0.70, 0.05, -0.13), om2.MPoint(0.70, 0.09, -0.20), om2.MPoint(0.70, 0.15, -0.20), om2.MPoint(0.60, 0.05, -0.02)]
        ctrl_neck_line_down_points = [om2.MPoint(0.60, 0.05, -0.02), om2.MPoint(0.00, 0.05, -0.02)]

        self.draw_neck_tn = self.MDag2_node.create("transform", "Draw_neck_ctrl")
        crv_ctrl_neck_line_up = self.MNurbs2_cv.createWithEditPoints(ctrl_neck_line_up_points, 1, 1, False, True, True, self.draw_neck_tn)
        crv_ctrl_neck_star = self.MNurbs2_cv.createWithEditPoints(ctrl_neck_star_up_points, 1, 1, False, True, True, self.draw_neck_tn)
        crv_ctrl_neck_line_down = self.MNurbs2_cv.createWithEditPoints(ctrl_neck_line_down_points, 1, 1, False, True, True, self.draw_neck_tn)

        if self.autostretch.currentIndex() == 1:
            self.necknull_tn = self.MDag2_node.create("transform", "Biped_Neck_null", self.stretchyspine_tn)
        else:
            self.necknull_tn = self.MDag2_node.create("transform", "Biped_Neck_null", self.spinectrl_tn)

        self.neckctrl_tn = self.MDag2_node.create("transform", "Biped_Neck_ctrl", self.necknull_tn)
        ctrl_neck_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.neckctrl_tn)

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

        self.MDG2_mod.renameNode(ctrl_neck_comb_cv, "Neck_shape")
        self.MDG2_mod.commandToExecute('color -rgbColor 0 1 1 "Biped_Neck_ctrl"')
        self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_Neck_ctrl"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_null.translateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_null.translateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_null.translateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_null.rotateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_null.rotateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_null.rotateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_null.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_null.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_null.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_null.visibility"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_ctrl.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_ctrl.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Neck_ctrl.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_Neck_ctrl.visibility"')
        self.MDG2_mod.doIt()

        ctrl_head_arcl_points = [om2.MPoint(-0.70, -0.1), om2.MPoint(-0.65, -0.03, 0.04), om2.MPoint(-0.50, 0.00, 0.1)]
        ctrl_head_sq_points = [om2.MPoint(-0.50, 0.00, 0.1), om2.MPoint(-0.30, 0.00, 0.25),  om2.MPoint(0.10, 0.00, 0.25),  om2.MPoint(0.20, 0.00, 0.05), om2.MPoint(0.20, 0.00, -0.05), om2.MPoint(0.10, 0.00, -0.25), om2.MPoint(-0.30, 0.00, -0.25), om2.MPoint(-0.50, 0.00, -0.1)]
        ctrl_head_arcr_points = [om2.MPoint(-0.50, 0.00, -0.1), om2.MPoint(-0.65, -0.03, -0.04), om2.MPoint(-0.70, -0.1)]

        self.draw_head_tn = self.MDag2_node.create("transform", "Draw_head_ctrl")
        crv_ctrl_head_line_l = self.MNurbs2_cv.createWithEditPoints(ctrl_head_sq_points, 1, 1, False, True, True, self.draw_head_tn)
        crv_ctrl_arc_l = self.MNurbs2_cv.createWithEditPoints(ctrl_head_arcl_points, 3, 1, False, True, True, self.draw_head_tn)
        crv_ctrl_arc_r = self.MNurbs2_cv.createWithEditPoints(ctrl_head_arcr_points, 3, 1, False, True, True, self.draw_head_tn)

        self.headnull_tn = self.MDag2_node.create("transform", "Biped_Head_null", self.neckctrl_tn)
        self.headrot_tn = self.MDag2_node.create("transform", "Biped_HeadRot_null", self.headnull_tn)
        self.headctrl_tn = self.MDag2_node.create("transform", "Biped_Head_ctrl", self.headrot_tn)
        ctrl_head_comb_cv = self.MNurbs2_cv.create([crv_ctrl_head_line_l, crv_ctrl_arc_l, crv_ctrl_arc_r], self.headctrl_tn)

        ctrl_stretchyspine_circle_points = [om2.MPoint(0.30, 0.00, 0.00), om2.MPoint(0.00, 0.20, 0.30), om2.MPoint(-0.30, 0.00, 0.00), om2.MPoint(0.00, 0.20, -0.30), om2.MPoint(0.30, 0.00, 0.00)]

        self.stretchyheadctrl_tn = self.MDag2_node.create("transform", "Biped_StretchyNeck_ctrl", self.headctrl_tn)
        crv_ctrl_stretchyhead = self.MNurbs2_cv.createWithEditPoints(ctrl_stretchyspine_circle_points, 3, 1, False, True, True, self.stretchyheadctrl_tn)

        jnt_head_obj = head_sl_ls.getDependNode(1)
        head_path_n = om2.MDagPath()
        head_path = head_path_n.getAPathTo(jnt_head_obj)
        jnt_head_transform = om2.MFnTransform(head_path)
        jnt_head_t = jnt_head_transform.translation(om2.MSpace.kWorld)

        jnt_headtop_obj = head_sl_ls.getDependNode(2)
        jnt_headtop_transform = om2.MFnTransform(jnt_headtop_obj)
        jnt_headtop_t = jnt_headtop_transform.translation(om2.MSpace.kTransform)

        headtopnull_transform = om2.MFnTransform(self.headnull_tn)
        headtopnull_transform.setTranslation(jnt_head_t, om2.MSpace.kTransform)

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

        self.MDG2_mod.commandToExecute('delete "Draw_head_ctrl"')
        self.MDG2_mod.renameNode(ctrl_head_comb_cv, "Head_shape")
        self.MDG2_mod.renameNode(crv_ctrl_stretchyhead, "StretchyNeck_shape")
        self.MDG2_mod.commandToExecute('color -rgbColor 0 1 0 "Biped_Head_ctrl"')
        self.MDG2_mod.commandToExecute('color -rgbColor 1 0 0 "Biped_StretchyNeck_ctrl"')
        self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_Head_ctrl"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_null.translateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_null.translateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_null.translateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_null.rotateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_null.rotateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_null.rotateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_null.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_null.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_null.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_null.visibility"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_ctrl.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_ctrl.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_Head_ctrl.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_Head_ctrl.visibility"')
        self.MDG2_mod.doIt()

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

        self.draw_shoulder_tn = self.MDag2_node.create("transform", "Draw_shoulder_ctrl")
        crv_ctrl_shoulder_arc_l = self.MNurbs2_cv.createWithEditPoints(ctrl_shoulder_arc_l, 3, 1, False, True, True, self.draw_shoulder_tn)
        crv_ctrl_shoulder_line = self.MNurbs2_cv.createWithEditPoints(ctrl_shoulder_line, 1, 1, False, True, True, self.draw_shoulder_tn)
        crv_ctrl_shoulder_arc_r = self.MNurbs2_cv.createWithEditPoints(ctrl_shoulder_arc_r, 3, 1, False, True, True, self.draw_shoulder_tn)

        if self.autostretch.currentIndex() == 1:
            self.lshouldernull_tn = self.MDag2_node.create("transform", "Biped_LeftShoulder_null", self.stretchyspine_tn)
        else:
            self.lshouldernull_tn = self.MDag2_node.create("transform", "Biped_LeftShoulder_null", self.spinectrl_tn)

        self.lshoulderctrl_tn = self.MDag2_node.create("transform", "Biped_LeftShoulder_ctrl", self.lshouldernull_tn)
        ctrl_shoulder_comb_cv = self.MNurbs2_cv.create([crv_ctrl_shoulder_arc_l, crv_ctrl_shoulder_line, crv_ctrl_shoulder_arc_r], self.lshoulderctrl_tn)

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

        self.MDG2_mod.commandToExecute('delete "Draw_shoulder_ctrl"')
        self.MDG2_mod.renameNode(ctrl_shoulder_comb_cv, "LeftShoulder_shape")
        self.MDG2_mod.commandToExecute('color -rgbColor 1 0 0 "Biped_LeftShoulder_ctrl"')
        self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftShoulder_ctrl"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_null.translateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_null.translateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_null.translateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_null.rotateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_null.rotateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_null.rotateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_null.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_null.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_null.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_null.visibility"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_ctrl.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_ctrl.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftShoulder_ctrl.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_LeftShoulder_ctrl.visibility"')
        self.MDG2_mod.doIt()

        for index in range(fklarm_sl_ls.length()):
           jnt_lhand_obj = fklarm_sl_ls.getDependNode(index)
           lhand_path_n = om2.MDagPath()
           lhand_path = lhand_path_n.getAPathTo(jnt_lhand_obj)
           jnt_lhand_transform = om2.MFnTransform(lhand_path)
           jnt_lhand_t = jnt_lhand_transform.translation(om2.MSpace.kWorld)

           if index == 1:
               self.larmnull_tn = self.MDag2_node.create("transform", "Biped_FkLeftArm_null", self.lshoulderctrl_tn)
               self.larmctrl_tn = self.MDag2_node.create("transform", "Biped_FkLeftArm_ctrl", self.larmnull_tn )
               ctrl_larm_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.larmctrl_tn)

               larmnull_transform = om2.MFnTransform(self.larmnull_tn)
               larmnull_transform.setTranslation(jnt_lhand_t, om2.MSpace.kTransform)

               jnt_larm_r = cmds.xform("LeftArm", query=True, rotation=True, worldSpace=True)

               radian_larm_x = (jnt_larm_r[0]/180)*3.1415
               radian_larm_y = (jnt_larm_r[1]/180)*3.1415
               radian_larm_z = (jnt_larm_r[2]/180)*3.1415

               larmnull_transform_r = larmnull_transform.rotation(om2.MSpace.kTransform)
               larmnull_transform_r[0], larmnull_transform_r[1], larmnull_transform_r[2] = radian_larm_x, radian_larm_y, radian_larm_z
               larmnull_transform.setRotation(larmnull_transform_r, om2.MSpace.kTransform)

               larmctrl_transform = om2.MFnTransform(self.larmctrl_tn)

               larmctrl_transform_s = larmctrl_transform.findPlug("scale", False)
               if larmctrl_transform_s.isCompound:
                   for i in range(larmctrl_transform_s.numChildren()):
                       child_plug = larmctrl_transform_s.child(i)
                       attr_value = child_plug.setDouble(box_transform_s[0]/2)

               larmnull_transform_trans = larmnull_transform.transformation()
               larmnull_transform_worldmatrix = larmnull_transform_trans.asMatrix()

               larmnull_transform_localmatrix = larmnull_transform_worldmatrix * spinenull_parentinvtransform_matrix * spinenull_childtransform_localmatrix.inverse() * lshouldernullnull_transform_localmatrix.inverse()

               larmnull_transform.setTransformation(om2.MTransformationMatrix(larmnull_transform_localmatrix))

               self.MDG2_mod.renameNode(ctrl_larm_comb_cv, "FkLeftArm_shape")
               self.MDG2_mod.commandToExecute('color -rgbColor 0 1 1 "Biped_FkLeftArm_ctrl"')
               self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkLeftArm_ctrl"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_null.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_null.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_null.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_null.rotateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_null.rotateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_null.rotateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_null.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_null.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_null.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_null.visibility"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_ctrl.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_ctrl.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_ctrl.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_ctrl.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_ctrl.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftArm_ctrl.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkLeftArm_ctrl.visibility"')
               self.MDG2_mod.doIt()

           elif index == 2:
               self.lforearmnull_tn = self.MDag2_node.create("transform", "Biped_FkLeftForeArm_null", self.larmctrl_tn)
               self.lforearmctrl_tn = self.MDag2_node.create("transform", "Biped_FkLeftForeArm_ctrl", self.lforearmnull_tn )
               ctrl_lforearm_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.lforearmctrl_tn)

               ctrl_elbow_triangle_points = [om2.MPoint(1.0, 0.0), om2.MPoint(0.0, 0.0, 1.0), om2.MPoint(-1.0, 0.0), om2.MPoint(0.0, 0.0, -1.0), om2.MPoint(1.0, 0.0)]
               ctrl_elbow_arrow_points = [om2.MPoint(0.0, 0.0), om2.MPoint(0.0, 1.0), om2.MPoint(0.0, 0.8, 0.1), om2.MPoint(0.0, 1.0), om2.MPoint(-0.1, 0.8), om2.MPoint(0.0, 1.0), om2.MPoint(0.0, 0.8, -0.1), om2.MPoint(0.0, 1.0), om2.MPoint(0.1, 0.8)]

               self.pvlelbownull_tn = self.MDag2_node.create("transform", "Biped_PVLeftElbow_null", self.masterctrl_tn)
               self.pvlelbowctrl_tn = self.MDag2_node.create("transform", "Biped_PVLeftElbow_ctrl", self.pvlelbownull_tn)
               crv_ctrl_elbow_triangle_l = self.MNurbs2_cv.createWithEditPoints(ctrl_elbow_triangle_points, 1, 1, False, True, True, self.pvlelbowctrl_tn)
               crv_ctrl_elbow_arrow_l = self.MNurbs2_cv.createWithEditPoints(ctrl_elbow_arrow_points, 1, 1, False, True, True, self.pvlelbowctrl_tn)

               lforearmnull_transform = om2.MFnTransform(self.lforearmnull_tn)
               lforearmnull_transform.setTranslation(jnt_lhand_t, om2.MSpace.kTransform)

               pvlelbownull_transform = om2.MFnTransform(self.pvlelbownull_tn)
               pvlelbownull_transform.setTranslation(jnt_lhand_t, om2.MSpace.kTransform)

               jnt_lforearm_r = cmds.xform("LeftForeArm", query=True, rotation=True, worldSpace=True)

               radian_lforearm_x = (jnt_lforearm_r[0]/180)*3.1415
               radian_lforearm_y = (jnt_lforearm_r[1]/180)*3.1415
               radian_lforearm_z = (jnt_lforearm_r[2]/180)*3.1415

               lforearmnull_transform_r = lforearmnull_transform.rotation(om2.MSpace.kTransform)
               lforearmnull_transform_r[0], lforearmnull_transform_r[1], lforearmnull_transform_r[2] = radian_lforearm_x, radian_lforearm_y, radian_lforearm_z
               lforearmnull_transform.setRotation(lforearmnull_transform_r, om2.MSpace.kTransform)

               lforearmctrl_transform = om2.MFnTransform(self.lforearmctrl_tn)

               pvlelbowctrl_transform = om2.MFnTransform(self.pvlelbowctrl_tn)

               lforearmctrl_transform_s = lforearmctrl_transform.findPlug("scale", False)
               if lforearmctrl_transform_s.isCompound:
                   for i in range(lforearmctrl_transform_s.numChildren()):
                       child_plug = lforearmctrl_transform_s.child(i)
                       attr_value = child_plug.setDouble(box_transform_s[0]/2)

               pvlelbownull_transform_t = pvlelbownull_transform.translation(om2.MSpace.kTransform)
               pvlelbownull_transform_t[2] = -(pvlelbownull_transform_t[2]+8)
               pvlelbownull_transform.setTranslation(pvlelbownull_transform_t, om2.MSpace.kTransform)

               pvlelbowctrl_transform_r = pvlelbowctrl_transform.rotation(om2.MSpace.kTransform)
               pvlelbowctrl_transform_r[0] = -1.57079
               pvlelbowctrl_transform.setRotation(pvlelbowctrl_transform_r, om2.MSpace.kTransform)

               lforearmnull_transform_trans = lforearmnull_transform.transformation()
               lforearmnull_transform_worldmatrix = lforearmnull_transform_trans.asMatrix()

               lforearmnull_transform_localmatrix = lforearmnull_transform_worldmatrix * spinenull_parentinvtransform_matrix * spinenull_childtransform_localmatrix.inverse() * lshouldernullnull_transform_localmatrix.inverse() * larmnull_transform_localmatrix.inverse()

               lforearmnull_transform.setTransformation(om2.MTransformationMatrix(lforearmnull_transform_localmatrix))

               self.MDG2_mod.renameNode(ctrl_lforearm_comb_cv, "FkLeftForeArm_shape")
               self.MDG2_mod.renameNode(crv_ctrl_elbow_triangle_l, "PVLeftElbow_shape1")
               self.MDG2_mod.renameNode(crv_ctrl_elbow_arrow_l, "PVLeftElbow_shape2")
               self.MDG2_mod.commandToExecute('color -rgbColor 0 1 1 "Biped_FkLeftForeArm_ctrl"')
               self.MDG2_mod.commandToExecute('color -rgbColor 1 1 0 "Biped_PVLeftElbow_ctrl"')
               self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkLeftForeArm_ctrl"')
               self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_PVLeftElbow_ctrl"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_null.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_null.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_null.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_null.rotateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_null.rotateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_null.rotateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_null.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_null.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_null.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_null.visibility"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkLeftForeArm_ctrl.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkLeftForeArm_ctrl.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkLeftForeArm_ctrl.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_ctrl.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_ctrl.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftForeArm_ctrl.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkLeftForeArm_ctrl.visibility"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVLeftElbow_null.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVLeftElbow_null.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVLeftElbow_null.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVLeftElbow_null.rotateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVLeftElbow_null.rotateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVLeftElbow_null.rotateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVLeftElbow_null.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVLeftElbow_null.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVLeftElbow_null.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVLeftElbow_null.visibility"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVLeftElbow_ctrl.rotateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVLeftElbow_ctrl.rotateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVLeftElbow_ctrl.rotateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVLeftElbow_ctrl.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVLeftElbow_ctrl.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVLeftElbow_ctrl.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVLeftElbow_ctrl.visibility"')
               self.MDG2_mod.doIt()

           elif index == 3:
               ctrl_lhand_line_up_points = [om2.MPoint(0.00, 0.05, 0.02), om2.MPoint(-0.60, 0.05, 0.02)]
               ctrl_lhand_star_up_points = [om2.MPoint(-0.60, 0.05, 0.02), om2.MPoint(-0.70, 0.15, 0.20), om2.MPoint(-0.70, 0.09, 0.20), om2.MPoint(-0.70, 0.06, 0.13), om2.MPoint(-0.60, 0.00, 0.00), om2.MPoint(-0.70, 0.05, -0.13), om2.MPoint(-0.70, 0.09, -0.20), om2.MPoint(-0.70, 0.15, -0.20), om2.MPoint(-0.60, 0.05, -0.02)]
               ctrl_lhand_line_down_points = [om2.MPoint(-0.60, 0.05, -0.02), om2.MPoint(-0.00, 0.05, -0.02)]

               self.draw_lhand_tn = self.MDag2_node.create("transform", "Draw_lefthand_ctrl")
               crv_ctrl_lhand_line_up = self.MNurbs2_cv.createWithEditPoints(ctrl_lhand_line_up_points, 1, 1, False, True, True, self.draw_lhand_tn)
               crv_ctrl_lhand_star = self.MNurbs2_cv.createWithEditPoints(ctrl_lhand_star_up_points, 1, 1, False, True, True, self.draw_lhand_tn)
               crv_ctrl_lhand_line_down = self.MNurbs2_cv.createWithEditPoints(ctrl_lhand_line_down_points, 1, 1, False, True, True, self.draw_lhand_tn)

               self.lhandnull_tn = self.MDag2_node.create("transform", "Biped_FkLeftHand_null", self.lforearmctrl_tn)
               self.lhandctrl_tn = self.MDag2_node.create("transform", "Biped_FkLeftHand_ctrl", self.lhandnull_tn )
               ctrl_lhandpositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.lhandctrl_tn)
               ctrl_lhandnegative_comb_cv = self.MNurbs2_cv.create([crv_ctrl_lhand_line_up, crv_ctrl_lhand_star, crv_ctrl_lhand_line_down], self.lhandctrl_tn)

               ctrl_lhandoption_line = [om2.MPoint(1.00, 0.00), om2.MPoint(0.00, 0.00, 1.50), om2.MPoint(-1.00, 0.00, 0.00), om2.MPoint(1.00, 0.00)]

               self.lfingernull_tn = self.MDag2_node.create("transform", "Biped_LeftFingers_null", self.masterctrl_tn)

               self.lhandoption_tn = self.MDag2_node.create("transform", "Biped_LeftHandOptions_ctrl", larm_sl_ls.getDependNode(2))
               ctrl_lhandoption_cv = self.MNurbs2_cv.createWithEditPoints(ctrl_lhandoption_line, 1, 1, False, True, True, self.lhandoption_tn)

               lhandnull_transform = om2.MFnTransform(self.lhandnull_tn)
               lhandnull_transform.setTranslation(jnt_lhand_t, om2.MSpace.kTransform)

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
               lhandoptionctrl_transform_t[2] = jnt_lhand_t[2]-5
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

               self.MDG2_mod.renameNode(ctrl_lhandpositive_comb_cv, "FkLeftHand_shape1")
               self.MDG2_mod.renameNode(ctrl_lhandnegative_comb_cv, "FkLeftHand_shape2")
               self.MDG2_mod.renameNode(ctrl_lhandoption_cv, "LeftHandOptions_shape")
               self.MDG2_mod.commandToExecute('color -rgbColor 0 1 1 "Biped_FkLeftHand_ctrl"')
               self.MDG2_mod.commandToExecute('color -rgbColor 1 1 0 "Biped_LeftHandOptions_ctrl"')
               self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkLeftHand_ctrl"')
               self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftHandOptions_ctrl"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_null.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_null.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_null.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_null.rotateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_null.rotateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_null.rotateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_null.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_null.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_null.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_null.visibility"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkLeftHand_ctrl.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkLeftHand_ctrl.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkLeftHand_ctrl.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_ctrl.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_ctrl.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftHand_ctrl.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkLeftHand_ctrl.visibility"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftHandOptions_ctrl.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftHandOptions_ctrl.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftHandOptions_ctrl.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftHandOptions_ctrl.rotateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftHandOptions_ctrl.rotateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftHandOptions_ctrl.rotateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftHandOptions_ctrl.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftHandOptions_ctrl.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftHandOptions_ctrl.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftHandOptions_ctrl.visibility"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingers_null.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingers_null.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingers_null.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingers_null.rotateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingers_null.rotateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingers_null.rotateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingers_null.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingers_null.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingers_null.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingers_null.visibility"')
               self.MDG2_mod.doIt()

               ctrl_hand_line_l = [om2.MPoint(1.20, 0.15), om2.MPoint(1.10, 0.00, 0.20), om2.MPoint(0.90, 0.15, 0.35)]
               ctrl_hand_line = [om2.MPoint(0.90, 0.15, 0.35), om2.MPoint(0.30, 0.30, 0.35), om2.MPoint(0.25, 0.35, 0.30), om2.MPoint(0.25, 0.35, -0.30), om2.MPoint(0.30, 0.30, -0.35), om2.MPoint(0.90, 0.15, -0.35)]
               ctrl_hand_line_r = [om2.MPoint(0.90, 0.15, -0.35), om2.MPoint(1.10, 0.00, -0.20), om2.MPoint(1.20, 0.15)]

               self.draw_lhand_tn = self.MDag2_node.create("transform", "Draw_iklefthand_ctrl")
               crv_ctrl_hand_line_l = self.MNurbs2_cv.createWithEditPoints(ctrl_hand_line_l, 1, 1, False, True, True, self.draw_lhand_tn)
               crv_ctrl_hand_line = self.MNurbs2_cv.createWithEditPoints(ctrl_hand_line, 1, 1, False, True, True, self.draw_lhand_tn)
               crv_ctrl_hand_line_r = self.MNurbs2_cv.createWithEditPoints(ctrl_hand_line_r, 1, 1, False, True, True, self.draw_lhand_tn)

               self.likhandnull_tn = self.MDag2_node.create("transform", "Biped_IkLeftHand_null", self.masterctrl_tn)
               self.lhandrotnull_tn = self.MDag2_node.create("transform", "Biped_IkLeftHandRot_null", self.likhandnull_tn)
               self.likhandctrl_tn = self.MDag2_node.create("transform", "Biped_IkLeftHand_ctrl", self.lhandrotnull_tn)
               ctrl_likhand_comb_cv = self.MNurbs2_cv.create([crv_ctrl_hand_line_l, crv_ctrl_hand_line, crv_ctrl_hand_line_r], self.likhandctrl_tn)

               self.nofliplelbownull_tn = self.MDag2_node.create("transform", "Biped_NoFlipLeftElbow_null", self.likhandnull_tn)
               self.nofliplelbowctrl_tn = self.MDag2_node.create("transform", "Biped_NoFlipLeftElbow_ctrl", self.nofliplelbownull_tn)
               self.nofliplelbowctrl_ln = self.MDag2_node.create("locator", "NoFlipLeftElbow_shape", self.nofliplelbowctrl_tn)

               likhandnull_transform = om2.MFnTransform(self.likhandnull_tn)
               likhandnull_transform.setTranslation(jnt_lhand_t, om2.MSpace.kTransform)

               likhandnull_transform_r = likhandnull_transform.rotation(om2.MSpace.kTransform)
               likhandnull_transform_r[0], likhandnull_transform_r[1], likhandnull_transform_r[2] = radian_lhand_x, radian_lhand_y, radian_lhand_z
               likhandnull_transform.setRotation(likhandnull_transform_r, om2.MSpace.kTransform)

               likhandctrl_transform = om2.MFnTransform(self.likhandctrl_tn)

               lelbowctrl_transform = om2.MFnTransform(self.nofliplelbowctrl_tn)

               likhandctrl_transform_t = likhandctrl_transform.translation(om2.MSpace.kTransform)
               likhandctrl_transform_t[2] = -((jnt_lhand_t[1]+4)-jnt_lhand_t[1])
               likhandctrl_transform.setTranslation(likhandctrl_transform_t, om2.MSpace.kTransform)

               likhandctrl_transform_r = likhandctrl_transform.rotation(om2.MSpace.kTransform)
               likhandctrl_transform_r[0], likhandctrl_transform_r[2] = 1.57079, 1.57079
               likhandctrl_transform.setRotation(likhandctrl_transform_r, om2.MSpace.kTransform)

               lelbowctrl_transform_t = lelbowctrl_transform.translation(om2.MSpace.kTransform)
               lelbowctrl_transform_t[2] = -7
               lelbowctrl_transform.setTranslation(lelbowctrl_transform_t, om2.MSpace.kTransform)

               likhandctrl_transform_s = likhandctrl_transform.findPlug("scale", False)
               if likhandctrl_transform_s.isCompound:
                   for i in range(likhandctrl_transform_s.numChildren()):
                       child_plug = likhandctrl_transform_s.child(i)
                       attr_value = child_plug.setDouble(box_transform_s[0]/3)

               self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_IkLeftHand_ctrl"')
               self.MDG2_mod.doIt()

               likhandnull_path_n = om2.MDagPath()
               likhandnull_path = likhandnull_path_n.getAPathTo(self.likhandctrl_tn)
               likhandnull_worldtransform = om2.MFnTransform(likhandnull_path)

               likhandnull_worldtransform.setRotatePivot(om2.MPoint(jnt_lhand_t), om2.MSpace.kWorld, False)

               self.MDG2_mod.renameNode(ctrl_likhand_comb_cv, "IkLeftHand_shape")
               self.MDG2_mod.commandToExecute('color -rgbColor 1 0 0 "Biped_IkLeftHand_ctrl"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_null.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_null.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_null.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_null.rotateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_null.rotateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_null.rotateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_null.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_null.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_null.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_null.visibility"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_ctrl.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_ctrl.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftHand_ctrl.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_IkLeftHand_ctrl.visibility"')
               self.MDG2_mod.doIt()

               ctrl_master_circle_points = [om2.MPoint(0.75, 0.0, 0.25), om2.MPoint(0.0, 0.0, 1.0), om2.MPoint(-1.0, 0.0), om2.MPoint(0.0, 0.0, -1.0), om2.MPoint(0.75, 0.0, -0.25), om2.MPoint(0.75, 0.0, 0.25)]

               self.lfingerctrl_tn = self.MDag2_node.create("transform", "Biped_LeftFingerOptions_ctrl", larm_sl_ls.getDependNode(2))
               ctrl_lfingerpositive_comb_cv = self.MNurbs2_cv.createWithEditPoints(ctrl_master_circle_points, 1, 1, False, True, True, self.lfingerctrl_tn)

               lfingerctrl_transform = om2.MFnTransform(self.lfingerctrl_tn)

               lfingerctrl_transform_s = lfingerctrl_transform.findPlug("scale", False)
               if lfingerctrl_transform_s.isCompound:
                   for i in range(lfingerctrl_transform_s.numChildren()):
                       child_plug = lfingerctrl_transform_s.child(i)
                       attr_value = child_plug.setDouble(box_transform_s[0]/3)

               self.MDG2_mod.renameNode(ctrl_lfingerpositive_comb_cv, "LeftFingerOptions_shape")
               self.MDG2_mod.commandToExecute('color -rgbColor 1 1 0.5 "Biped_LeftFingerOptions_ctrl"')
               self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftFingerOptions_ctrl"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerOptions_ctrl.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerOptions_ctrl.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerOptions_ctrl.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerOptions_ctrl.rotateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerOptions_ctrl.rotateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerOptions_ctrl.rotateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerOptions_ctrl.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerOptions_ctrl.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerOptions_ctrl.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerOptions_ctrl.visibility"')
               self.MDG2_mod.doIt()

        try:
            lhandthumb_sl_ls = om2.MSelectionList()
            lhandthumb_sl_ls.add("LeftFingerThumb*")

            for index in range(lhandthumb_sl_ls.length()):
                jnt_lhandthumb_obj = lhandthumb_sl_ls.getDependNode(index)
                jnt_lhandthumb_path_n = om2.MDagPath()
                jnt_lhandthumb_path = jnt_lhandthumb_path_n.getAPathTo(jnt_lhandthumb_obj)
                jnt_lhandthumb_transform = om2.MFnTransform(jnt_lhandthumb_path)
                jnt_lhandthumb_t = jnt_lhandthumb_transform.translation(om2.MSpace.kWorld)

                self.lhandthumbnull_tn = self.MDag2_node.create("transform", "Biped_LeftFingerThumb{0}_null".format(index+1))
                self.lhandthumbglobalcurl_tn = self.MDag2_node.create("transform", "Biped_LeftFingerThumb{0}_globalcurl".format(index+1), self.lhandthumbnull_tn)
                self.lhandthumbcurl_tn = self.MDag2_node.create("transform", "Biped_LeftFingerThumb{0}_curl".format(index+1), self.lhandthumbglobalcurl_tn)
                self.lhandthumbctrl_tn = self.MDag2_node.create("transform", "Biped_LeftFingerThumb{0}_ctrl".format(index+1), self.lhandthumbcurl_tn)
                ctrl_lhandthumbpositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.lhandthumbctrl_tn)
                ctrl_lhandthumbnegative_comb_cv = self.MNurbs2_cv.create([crv_ctrl_lhand_line_up, crv_ctrl_lhand_star, crv_ctrl_lhand_line_down], self.lhandthumbctrl_tn)

                lhandthumbnull_transform = om2.MFnTransform(self.lhandthumbnull_tn)
                lhandthumbnull_transform.setTranslation(jnt_lhandthumb_t, om2.MSpace.kTransform)

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

                    self.lfingerthumbctrl_tn = self.MDag2_node.create("transform", "Biped_LeftThumbOptions_ctrl")
                    ctrl_lfingerthumbpositive_comb_cv = self.MNurbs2_cv.createWithEditPoints(ctrl_master_circle_points, 1, 1, False, True, True, self.lfingerthumbctrl_tn)

                    lfingerthumbctrl_transform = om2.MFnTransform(self.lfingerthumbctrl_tn)

                    lfingerthumbctrl_transform_t = lfingerthumbctrl_transform.translation(om2.MSpace.kTransform)
                    lfingerthumbctrl_transform_t[0], lfingerthumbctrl_transform_t[1], lfingerthumbctrl_transform_t[2] = jnt_lhandthumb_t[0], jnt_lhandthumb_t[1], jnt_lhandthumb_t[2]
                    lfingerthumbctrl_transform.setTranslation(lfingerthumbctrl_transform_t, om2.MSpace.kTransform)

                    lfingerthumbctrl_transform_r= lfingerthumbctrl_transform.rotation(om2.MSpace.kTransform)
                    lfingerthumbctrl_transform_r[0], lfingerthumbctrl_transform_r[1], lfingerthumbctrl_transform_r[2] = lhandthumbnull_transform_r[0], lhandthumbnull_transform_r[1], lhandthumbnull_transform_r[2]
                    lfingerthumbctrl_transform.setRotation(lfingerthumbctrl_transform_r, om2.MSpace.kTransform)

                    lfingerthumbctrl_transform_s = lfingerthumbctrl_transform.findPlug("scale", False)
                    if lfingerthumbctrl_transform_s.isCompound:
                        for i in range(lfingerthumbctrl_transform_s.numChildren()):
                            child_plug = lfingerthumbctrl_transform_s.child(i)
                            attr_value = child_plug.setDouble(box_transform_s[0]/9)

                    lhandjnt_tr_n = om2.MFnDagNode(larm_sl_ls.getDependNode(2))
                    lhandjnt_tr_n.addChild(self.lfingerthumbctrl_tn)

                    lfingerthumbctrl_transform_trans = lfingerthumbctrl_transform.transformation()
                    lfingerthumbctrl_transform_worldmatrix = lfingerthumbctrl_transform_trans.asMatrix()

                    lfingerthumbctrl_transform_localmatrix = lfingerthumbctrl_transform_worldmatrix * lfingernull_transform_worldmatrix

                    lfingerthumbctrl_transform.setTransformation(om2.MTransformationMatrix(lfingerthumbctrl_transform_localmatrix))

                    self.MDG2_mod.renameNode(ctrl_lfingerthumbpositive_comb_cv, "LeftThumbOptions_shape")
                    self.MDG2_mod.commandToExecute('color -rgbColor 1 1 0.5 "Biped_LeftThumbOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftThumbOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftThumbOptions_ctrl.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftThumbOptions_ctrl.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftThumbOptions_ctrl.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftThumbOptions_ctrl.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftThumbOptions_ctrl.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftThumbOptions_ctrl.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftThumbOptions_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftThumbOptions_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftThumbOptions_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftThumbOptions_ctrl.visibility"')

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

                self.MDG2_mod.renameNode(ctrl_lhandthumbpositive_comb_cv, "LeftFingerThumb{0}_shape1".format(index + 1))
                self.MDG2_mod.renameNode(ctrl_lhandthumbnegative_comb_cv, "LeftFingerThumb{0}_shape2".format(index + 1))
                self.MDG2_mod.commandToExecute('color -rgbColor 0 1 0 "Biped_LeftFingerThumb{0}_ctrl"'.format(index + 1))
                self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftFingerThumb{0}_ctrl"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_null.translateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_null.translateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_null.translateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_null.rotateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_null.rotateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_null.rotateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_null.scaleX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_null.scaleY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_null.scaleZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_null.visibility"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "Biped_LeftFingerThumb{0}_ctrl.translateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "Biped_LeftFingerThumb{0}_ctrl.translateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false "Biped_LeftFingerThumb{0}_ctrl.translateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_ctrl.scaleX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_ctrl.scaleY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerThumb{0}_ctrl.scaleZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_LeftFingerThumb{0}_ctrl.visibility"'.format(index + 1))
                self.MDG2_mod.doIt()

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

                self.lhandindexnull_tn = self.MDag2_node.create("transform", "Biped_LeftFingerIndex{0}_null".format(index + 1))
                self.lhandindexglobalcurl_tn = self.MDag2_node.create("transform", "Biped_LeftFingerIndex{0}_globalcurl".format(index+1), self.lhandindexnull_tn)
                self.lhandindexcurl_tn = self.MDag2_node.create("transform", "Biped_LeftFingerIndex{0}_curl".format(index+1), self.lhandindexglobalcurl_tn)
                self.lhandindexctrl_tn = self.MDag2_node.create("transform", "Biped_LeftFingerIndex{0}_ctrl".format(index + 1), self.lhandindexcurl_tn)
                ctrl_lhandIndexpositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.lhandindexctrl_tn)
                ctrl_lhandIndexnegative_comb_cv = self.MNurbs2_cv.create([crv_ctrl_lhand_line_up, crv_ctrl_lhand_star, crv_ctrl_lhand_line_down], self.lhandindexctrl_tn)

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

                    self.lfingerindexctrl_tn = self.MDag2_node.create("transform", "Biped_LeftIndexOptions_ctrl")
                    ctrl_lfingerindexpositive_comb_cv = self.MNurbs2_cv.createWithEditPoints(ctrl_master_circle_points, 1, 1, False, True, True, self.lfingerindexctrl_tn)

                    lfingerindexctrl_transform = om2.MFnTransform(self.lfingerindexctrl_tn)

                    lfingerindexctrl_transform_t = lfingerindexctrl_transform.translation(om2.MSpace.kTransform)
                    lfingerindexctrl_transform_t[0], lfingerindexctrl_transform_t[1], lfingerindexctrl_transform_t[2] = jnt_lhandindex_t[0], jnt_lhandindex_t[1], jnt_lhandindex_t[2]
                    lfingerindexctrl_transform.setTranslation(lfingerindexctrl_transform_t, om2.MSpace.kTransform)

                    lfingerindexctrl_transform_r= lfingerindexctrl_transform.rotation(om2.MSpace.kTransform)
                    lfingerindexctrl_transform_r[0], lfingerindexctrl_transform_r[1], lfingerindexctrl_transform_r[2] = lhandindexnull_transform_r[0], lhandindexnull_transform_r[1], lhandindexnull_transform_r[2]
                    lfingerindexctrl_transform.setRotation(lfingerindexctrl_transform_r, om2.MSpace.kTransform)

                    lfingerindexctrl_transform_s = lfingerindexctrl_transform.findPlug("scale", False)
                    if lfingerindexctrl_transform_s.isCompound:
                        for i in range(lfingerindexctrl_transform_s.numChildren()):
                            child_plug = lfingerindexctrl_transform_s.child(i)
                            attr_value = child_plug.setDouble(box_transform_s[0]/9)

                    lhandjnt_tr_n.addChild(self.lfingerindexctrl_tn)

                    lfingerindexctrl_transform_trans = lfingerindexctrl_transform.transformation()
                    lfingerindexctrl_transform_worldmatrix = lfingerindexctrl_transform_trans.asMatrix()

                    lfingerindexctrl_transform_localmatrix = lfingerindexctrl_transform_worldmatrix * lfingernull_transform_worldmatrix

                    lfingerindexctrl_transform.setTransformation(om2.MTransformationMatrix(lfingerindexctrl_transform_localmatrix))

                    self.MDG2_mod.renameNode(ctrl_lfingerindexpositive_comb_cv, "LeftIndexOptions_shape")
                    self.MDG2_mod.commandToExecute('color -rgbColor 1 1 0.5 "Biped_LeftIndexOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftIndexOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftIndexOptions_ctrl.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftIndexOptions_ctrl.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftIndexOptions_ctrl.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftIndexOptions_ctrl.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftIndexOptions_ctrl.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftIndexOptions_ctrl.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftIndexOptions_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftIndexOptions_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftIndexOptions_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftIndexOptions_ctrl.visibility"')

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

                self.MDG2_mod.renameNode(ctrl_lhandIndexpositive_comb_cv, "LeftFingerIndex{0}_shape1".format(index + 1))
                self.MDG2_mod.renameNode(ctrl_lhandIndexnegative_comb_cv, "LeftFingerIndex{0}_shape2".format(index + 1))
                self.MDG2_mod.commandToExecute('color -rgbColor 0 1 0 "Biped_LeftFingerIndex{0}_ctrl"'.format(index + 1))
                self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftFingerIndex{0}_ctrl"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_null.translateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_null.translateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_null.translateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_null.rotateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_null.rotateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_null.rotateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_null.scaleX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_null.scaleY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_null.scaleZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_null.visibility"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_LeftFingerIndex{0}_ctrl.translateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_LeftFingerIndex{0}_ctrl.translateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_LeftFingerIndex{0}_ctrl.translateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_ctrl.scaleX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_ctrl.scaleY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerIndex{0}_ctrl.scaleZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_LeftFingerIndex{0}_ctrl.visibility"'.format(index + 1))
                self.MDG2_mod.doIt()

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

                self.lhandmiddlenull_tn = self.MDag2_node.create("transform", "Biped_LeftFingerMiddle{0}_null".format(index + 1))
                self.lhandmiddleglobalcurl_tn = self.MDag2_node.create("transform", "Biped_LeftFingerMiddle{0}_globalcurl".format(index+1), self.lhandmiddlenull_tn)
                self.lhandmiddlecurl_tn = self.MDag2_node.create("transform", "Biped_LeftFingerMiddle{0}_curl".format(index+1), self.lhandmiddleglobalcurl_tn)
                self.lhandmiddlectrl_tn = self.MDag2_node.create("transform", "Biped_LeftFingerMiddle{0}_ctrl".format(index + 1), self.lhandmiddlecurl_tn)
                ctrl_lhandmiddlepositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.lhandmiddlectrl_tn)
                ctrl_lhandmiddlenegative_comb_cv = self.MNurbs2_cv.create([crv_ctrl_lhand_line_up, crv_ctrl_lhand_star, crv_ctrl_lhand_line_down], self.lhandmiddlectrl_tn)

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

                    self.lfingermiddlectrl_tn = self.MDag2_node.create("transform", "Biped_LeftMiddleOptions_ctrl")
                    ctrl_lfingermiddlepositive_comb_cv = self.MNurbs2_cv.createWithEditPoints(ctrl_master_circle_points, 1, 1, False, True, True, self.lfingermiddlectrl_tn)

                    lfingermiddlectrl_transform = om2.MFnTransform(self.lfingermiddlectrl_tn)

                    lfingermiddlectrl_transform_t = lfingermiddlectrl_transform.translation(om2.MSpace.kTransform)
                    lfingermiddlectrl_transform_t[0], lfingermiddlectrl_transform_t[1], lfingermiddlectrl_transform_t[2] = jnt_lhandmiddle_t[0], jnt_lhandmiddle_t[1], jnt_lhandmiddle_t[2]
                    lfingermiddlectrl_transform.setTranslation(lfingermiddlectrl_transform_t, om2.MSpace.kTransform)

                    lfingermiddlectrl_transform_r= lfingermiddlectrl_transform.rotation(om2.MSpace.kTransform)
                    lfingermiddlectrl_transform_r[0], lfingermiddlectrl_transform_r[1], lfingermiddlectrl_transform_r[2] = lhandmiddlenull_transform_r[0], lhandmiddlenull_transform_r[1], lhandmiddlenull_transform_r[2]
                    lfingermiddlectrl_transform.setRotation(lfingermiddlectrl_transform_r, om2.MSpace.kTransform)

                    lfingermiddlectrl_transform_s = lfingermiddlectrl_transform.findPlug("scale", False)
                    if lfingermiddlectrl_transform_s.isCompound:
                        for i in range(lfingermiddlectrl_transform_s.numChildren()):
                            child_plug = lfingermiddlectrl_transform_s.child(i)
                            attr_value = child_plug.setDouble(box_transform_s[0]/9)

                    lhandjnt_tr_n.addChild(self.lfingermiddlectrl_tn)

                    lfingermiddlectrl_transform_trans = lfingermiddlectrl_transform.transformation()
                    lfingermiddlectrl_transform_worldmatrix = lfingermiddlectrl_transform_trans.asMatrix()

                    lfingermiddlectrl_transform_localmatrix = lfingermiddlectrl_transform_worldmatrix * lfingernull_transform_worldmatrix

                    lfingermiddlectrl_transform.setTransformation(om2.MTransformationMatrix(lfingermiddlectrl_transform_localmatrix))

                    self.MDG2_mod.renameNode(ctrl_lfingermiddlepositive_comb_cv, "LeftMiddleOptions_shape")
                    self.MDG2_mod.commandToExecute('color -rgbColor 1 1 0.5 "Biped_LeftMiddleOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftMiddleOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftMiddleOptions_ctrl.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftMiddleOptions_ctrl.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftMiddleOptions_ctrl.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftMiddleOptions_ctrl.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftMiddleOptions_ctrl.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftMiddleOptions_ctrl.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftMiddleOptions_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftMiddleOptions_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftMiddleOptions_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftMiddleOptions_ctrl.visibility"')

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

                self.MDG2_mod.renameNode(ctrl_lhandmiddlepositive_comb_cv, "LeftFingerMiddle{0}_shape1".format(index + 1))
                self.MDG2_mod.renameNode(ctrl_lhandmiddlenegative_comb_cv, "LeftFingerMiddle{0}_shape2".format(index + 1))
                self.MDG2_mod.commandToExecute('color -rgbColor 0 1 0 "Biped_LeftFingerMiddle{0}_ctrl"'.format(index + 1))
                self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftFingerMiddle{0}_ctrl"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_null.translateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_null.translateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_null.translateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_null.rotateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_null.rotateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_null.rotateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_null.scaleX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_null.scaleY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_null.scaleZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_null.visibility"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox true "Biped_LeftFingerMiddle{0}_ctrl.translateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox true "Biped_LeftFingerMiddle{0}_ctrl.translateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox true "Biped_LeftFingerMiddle{0}_ctrl.translateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_ctrl.scaleX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_ctrl.scaleY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_ctrl.scaleZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_LeftFingerMiddle{0}_ctrl.visibility"'.format(index + 1))
                self.MDG2_mod.doIt()

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

                self.lhandringnull_tn = self.MDag2_node.create("transform", "Biped_LeftFingerRing{0}_null".format(index + 1))
                self.lhandringglobalcurl_tn = self.MDag2_node.create("transform", "Biped_LeftFingerRing{0}_globalcurl".format(index+1), self.lhandringnull_tn)
                self.lhandringcurl_tn = self.MDag2_node.create("transform", "Biped_LeftFingerRing{0}_curl".format(index+1), self.lhandringglobalcurl_tn)
                self.lhandringctrl_tn = self.MDag2_node.create("transform", "Biped_LeftFingerRing{0}_ctrl".format(index + 1), self.lhandringcurl_tn)
                ctrl_lhandringpositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.lhandringctrl_tn)
                ctrl_lhandringnegative_comb_cv = self.MNurbs2_cv.create([crv_ctrl_lhand_line_up, crv_ctrl_lhand_star, crv_ctrl_lhand_line_down], self.lhandringctrl_tn)

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

                    self.lfingerringctrl_tn = self.MDag2_node.create("transform", "Biped_LeftRingOptions_ctrl")
                    ctrl_lfingerringpositive_comb_cv = self.MNurbs2_cv.createWithEditPoints(ctrl_master_circle_points, 1, 1, False, True, True, self.lfingerringctrl_tn)

                    lfingerringctrl_transform = om2.MFnTransform(self.lfingerringctrl_tn)

                    lfingerringctrl_transform_t = lfingerringctrl_transform.translation(om2.MSpace.kTransform)
                    lfingerringctrl_transform_t[0], lfingerringctrl_transform_t[1], lfingerringctrl_transform_t[2] = jnt_lhandring_t[0], jnt_lhandring_t[1], jnt_lhandring_t[2]
                    lfingerringctrl_transform.setTranslation(lfingerringctrl_transform_t, om2.MSpace.kTransform)

                    lfingerringctrl_transform_r= lfingerringctrl_transform.rotation(om2.MSpace.kTransform)
                    lfingerringctrl_transform_r[0], lfingerringctrl_transform_r[1], lfingerringctrl_transform_r[2] = lhandringnull_transform_r[0], lhandringnull_transform_r[1], lhandringnull_transform_r[2]
                    lfingerringctrl_transform.setRotation(lfingerringctrl_transform_r, om2.MSpace.kTransform)

                    lfingerringctrl_transform_s = lfingerringctrl_transform.findPlug("scale", False)
                    if lfingerringctrl_transform_s.isCompound:
                        for i in range(lfingerringctrl_transform_s.numChildren()):
                            child_plug = lfingerringctrl_transform_s.child(i)
                            attr_value = child_plug.setDouble(box_transform_s[0]/9)

                    lhandjnt_tr_n.addChild(self.lfingerringctrl_tn)

                    lfingerringctrl_transform_trans = lfingerringctrl_transform.transformation()
                    lfingerringctrl_transform_worldmatrix = lfingerringctrl_transform_trans.asMatrix()

                    lfingerringctrl_transform_localmatrix = lfingerringctrl_transform_worldmatrix * lfingernull_transform_worldmatrix

                    lfingerringctrl_transform.setTransformation(om2.MTransformationMatrix(lfingerringctrl_transform_localmatrix))

                    self.MDG2_mod.renameNode(ctrl_lfingerringpositive_comb_cv, "LeftRingOptions_shape")
                    self.MDG2_mod.commandToExecute('color -rgbColor 1 1 0.5 "Biped_LeftRingOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftRingOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftRingOptions_ctrl.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftRingOptions_ctrl.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftRingOptions_ctrl.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftRingOptions_ctrl.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftRingOptions_ctrl.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftRingOptions_ctrl.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftRingOptions_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftRingOptions_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftRingOptions_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftRingOptions_ctrl.visibility"')

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

                self.MDG2_mod.renameNode(ctrl_lhandringpositive_comb_cv, "LeftFingerRing{0}_shape1".format(index + 1))
                self.MDG2_mod.renameNode(ctrl_lhandringnegative_comb_cv, "LeftFingerRing{0}_shape2".format(index + 1))
                self.MDG2_mod.commandToExecute('color -rgbColor 0 1 0 "Biped_LeftFingerRing{0}_ctrl"'.format(index + 1))
                self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftFingerRing{0}_ctrl"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_null.translateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_null.translateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_null.translateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_null.rotateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_null.rotateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_null.rotateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_null.scaleX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_null.scaleY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_null.scaleZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_null.visibility"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox true "Biped_LeftFingerRing{0}_ctrl.translateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox true "Biped_LeftFingerRing{0}_ctrl.translateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox true "Biped_LeftFingerRing{0}_ctrl.translateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_ctrl.scaleX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_ctrl.scaleY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerRing{0}_ctrl.scaleZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_LeftFingerRing{0}_ctrl.visibility"'.format(index + 1))
                self.MDG2_mod.doIt()

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

                self.lhandpinkynull_tn = self.MDag2_node.create("transform", "Biped_LeftFingerPinky{0}_null".format(index + 1))
                self.lhandpinkyglobalcurl_tn = self.MDag2_node.create("transform", "Biped_LeftFingerPinky{0}_globalcurl".format(index+1), self.lhandpinkynull_tn)
                self.lhandpinkycurl_tn = self.MDag2_node.create("transform", "Biped_LeftFingerPinky{0}_curl".format(index+1), self.lhandpinkyglobalcurl_tn)
                self.lhandpinkyctrl_tn = self.MDag2_node.create("transform", "Biped_LeftFingerPinky{0}_ctrl".format(index + 1), self.lhandpinkycurl_tn)
                ctrl_lhandpinkypositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.lhandpinkyctrl_tn)
                ctrl_lhandpinkynegative_comb_cv = self.MNurbs2_cv.create([crv_ctrl_lhand_line_up, crv_ctrl_lhand_star, crv_ctrl_lhand_line_down], self.lhandpinkyctrl_tn)

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

                    self.lfingerpinkyctrl_tn = self.MDag2_node.create("transform", "Biped_LeftPinkyOptions_ctrl")
                    ctrl_lfingerpinkypositive_comb_cv = self.MNurbs2_cv.createWithEditPoints(ctrl_master_circle_points, 1, 1, False, True, True, self.lfingerpinkyctrl_tn)

                    lfingerpinkyctrl_transform = om2.MFnTransform(self.lfingerpinkyctrl_tn)

                    lfingerpinkyctrl_transform_t = lfingerpinkyctrl_transform.translation(om2.MSpace.kTransform)
                    lfingerpinkyctrl_transform_t[0], lfingerpinkyctrl_transform_t[1], lfingerpinkyctrl_transform_t[2] = jnt_lhandpinky_t[0], jnt_lhandpinky_t[1], jnt_lhandpinky_t[2]
                    lfingerpinkyctrl_transform.setTranslation(lfingerpinkyctrl_transform_t, om2.MSpace.kTransform)

                    lfingerpinkyctrl_transform_r= lfingerpinkyctrl_transform.rotation(om2.MSpace.kTransform)
                    lfingerpinkyctrl_transform_r[0], lfingerpinkyctrl_transform_r[1], lfingerpinkyctrl_transform_r[2] = lhandpinkynull_transform_r[0], lhandpinkynull_transform_r[1], lhandpinkynull_transform_r[2]
                    lfingerpinkyctrl_transform.setRotation(lfingerpinkyctrl_transform_r, om2.MSpace.kTransform)

                    lfingerpinkyctrl_transform_s = lfingerpinkyctrl_transform.findPlug("scale", False)
                    if lfingerpinkyctrl_transform_s.isCompound:
                        for i in range(lfingerpinkyctrl_transform_s.numChildren()):
                            child_plug = lfingerpinkyctrl_transform_s.child(i)
                            attr_value = child_plug.setDouble(box_transform_s[0]/9)

                    lhandjnt_tr_n.addChild(self.lfingerpinkyctrl_tn)

                    lfingerpinkyctrl_transform_trans = lfingerpinkyctrl_transform.transformation()
                    lfingerpinkyctrl_transform_worldmatrix = lfingerpinkyctrl_transform_trans.asMatrix()

                    lfingerpinkyctrl_transform_localmatrix = lfingerpinkyctrl_transform_worldmatrix * lfingernull_transform_worldmatrix

                    lfingerpinkyctrl_transform.setTransformation(om2.MTransformationMatrix(lfingerpinkyctrl_transform_localmatrix))

                    self.MDG2_mod.renameNode(ctrl_lfingerpinkypositive_comb_cv, "LeftPinkyOptions_shape")
                    self.MDG2_mod.commandToExecute('color -rgbColor 1 1 0.5 "Biped_LeftPinkyOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftPinkyOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftPinkyOptions_ctrl.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftPinkyOptions_ctrl.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftPinkyOptions_ctrl.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftPinkyOptions_ctrl.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftPinkyOptions_ctrl.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftPinkyOptions_ctrl.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftPinkyOptions_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftPinkyOptions_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftPinkyOptions_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftPinkyOptions_ctrl.visibility"')

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

                self.MDG2_mod.renameNode(ctrl_lhandpinkypositive_comb_cv, "LeftFingerPinky{0}_shape1".format(index + 1))
                self.MDG2_mod.renameNode(ctrl_lhandpinkynegative_comb_cv, "LeftFingerPinky{0}_shape2".format(index + 1))
                self.MDG2_mod.commandToExecute('color -rgbColor 0 1 0 "Biped_LeftFingerPinky{0}_ctrl"'.format(index + 1))
                self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftFingerPinky{0}_ctrl"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_null.translateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_null.translateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_null.translateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_null.rotateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_null.rotateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_null.rotateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_null.scaleX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_null.scaleY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_null.scaleZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_null.visibility"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox true "Biped_LeftFingerPinky{0}_ctrl.translateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox true "Biped_LeftFingerPinky{0}_ctrl.translateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox true "Biped_LeftFingerPinky{0}_ctrl.translateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_ctrl.scaleX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_ctrl.scaleY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFingerPinky{0}_ctrl.scaleZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_LeftFingerPinky{0}_ctrl.visibility"'.format(index + 1))
                self.MDG2_mod.doIt()

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
                    if self.hipjnt.currentIndex() == 1:
                        self.luplegnull_tn = self.MDag2_node.create("transform", "Biped_FkLeftUpLeg_null", self.hipctrl_tn)
                    else:
                        self.luplegnull_tn = self.MDag2_node.create("transform", "Biped_FkLeftUpLeg_null", self.rootctrl_tn)

                    self.luplegupctrl_tn = self.MDag2_node.create("transform", "Biped_FkLeftUpLeg_ctrl", self.luplegnull_tn)
                    ctrl_luplegpositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.luplegupctrl_tn)

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

                    self.MDG2_mod.renameNode(ctrl_luplegpositive_comb_cv, "LeftUpLeg_shape")
                    self.MDG2_mod.commandToExecute('color -rgbColor 0 1 1 "Biped_FkLeftUpLeg_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkLeftUpLeg_ctrl"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_null.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_null.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_null.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_null.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_null.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_null.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_null.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_null.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_null.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_null.visibility"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_ctrl.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_ctrl.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_ctrl.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftUpLeg_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkLeftUpLeg_ctrl.visibility"')
                    self.MDG2_mod.doIt()

                elif index == 1:
                    self.llegnull_tn = self.MDag2_node.create("transform", "Biped_FkLeftLeg_null", self.luplegupctrl_tn)
                    self.llegctrl_tn = self.MDag2_node.create("transform", "Biped_FkLeftLeg_ctrl", self.llegnull_tn)
                    ctrl_llegpositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.llegctrl_tn)

                    self.pvllegkneenull_tn = self.MDag2_node.create("transform", "Biped_PVLeftKnee_null", self.masterctrl_tn)
                    self.pvllegkneectrl_tn = self.MDag2_node.create("transform", "Biped_PVLeftKnee_ctrl", self.pvllegkneenull_tn)
                    crv_ctrl_knee_triangle_l = self.MNurbs2_cv.createWithEditPoints(ctrl_elbow_triangle_points, 1, 1, False, True, True, self.pvllegkneectrl_tn)
                    crv_ctrl_knee_arrow_l = self.MNurbs2_cv.createWithEditPoints(ctrl_elbow_arrow_points, 1, 1, False, True, True, self.pvllegkneectrl_tn)

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

                    pvllegkneectrl_transform = om2.MFnTransform(self.pvllegkneectrl_tn)

                    llegctrl_transform_r = llegnull_transform.rotation(om2.MSpace.kTransform)
                    llegctrl_transform_r[0], llegctrl_transform_r[1], llegctrl_transform_r[2] = 0, 1.57079, 0
                    llegctrl_transform.setRotation(llegctrl_transform_r, om2.MSpace.kTransform)

                    pvllegkneenull_transform_t = pvllegkneenull_transform.translation(om2.MSpace.kTransform)
                    pvllegkneenull_transform_t[2] = pvllegkneenull_transform_t[2]+8
                    pvllegkneenull_transform.setTranslation(pvllegkneenull_transform_t, om2.MSpace.kTransform)

                    pvllegknectrl_transform_r = pvllegkneectrl_transform.rotation(om2.MSpace.kTransform)
                    pvllegknectrl_transform_r[0] = 1.57079
                    pvllegkneectrl_transform.setRotation(pvllegknectrl_transform_r, om2.MSpace.kTransform)

                    llegctrl_transform_s = llegctrl_transform.findPlug("scale", False)
                    if llegctrl_transform_s.isCompound:
                        for i in range(llegctrl_transform_s.numChildren()):
                            child_plug = llegctrl_transform_s.child(i)
                            attr_value = child_plug.setDouble(box_transform_s[0]/2)

                    llegnull_transform_trans = llegnull_transform.transformation()
                    llegnull_transform_worldmatrix = llegnull_transform_trans.asMatrix()

                    llegnull_transform_localmatrix = llegnull_transform_worldmatrix * rootctrl_transform_worldmatrix * luplegnull_transform_localmatrix.inverse()

                    llegnull_transform.setTransformation(om2.MTransformationMatrix(llegnull_transform_localmatrix))

                    self.MDG2_mod.renameNode(ctrl_llegpositive_comb_cv, "LeftLeg_shape")
                    self.MDG2_mod.renameNode(crv_ctrl_knee_triangle_l, "PVLeftKnee_shape1")
                    self.MDG2_mod.renameNode(crv_ctrl_knee_arrow_l, "PVLeftKnee_shape2")
                    self.MDG2_mod.commandToExecute('color -rgbColor 0 1 1 "Biped_FkLeftLeg_ctrl"')
                    self.MDG2_mod.commandToExecute('color -rgbColor 1 1 0 "Biped_PVLeftKnee_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkLeftLeg_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_PVLeftKnee_ctrl"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_null.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_null.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_null.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_null.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_null.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_null.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_null.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_null.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_null.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_null.visibility"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox true "Biped_FkLeftLeg_ctrl.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox true "Biped_FkLeftLeg_ctrl.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox true "Biped_FkLeftLeg_ctrl.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftLeg_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkLeftLeg_ctrl.visibility"')
                    self.MDG2_mod.doIt()

                elif index == 2:
                    self.llegfootnull_tn = self.MDag2_node.create("transform", "Biped_FkLeftFoot_null", self.llegctrl_tn)
                    self.llegfootctrl_tn = self.MDag2_node.create("transform", "Biped_FkLeftFoot_ctrl", self.llegfootnull_tn)
                    ctrl_llegfootpositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.llegfootctrl_tn)

                    self.liklegfootnull_tn = self.MDag2_node.create("transform", "Biped_IkLeftFoot_null", self.masterctrl_tn)
                    self.liklegfootoffsetnull_tn = self.MDag2_node.create("transform", "Biped_IkLeftFootOffset_null", self.liklegfootnull_tn)
                    self.liklegfootRotnull_tn = self.MDag2_node.create("transform", "Biped_IkLeftFootRot_null", self.liklegfootoffsetnull_tn)
                    self.liklegfootctrl_tn = self.MDag2_node.create("transform", "Biped_IkLeftFoot_ctrl", self.liklegfootRotnull_tn)
                    ctrl_liklegfootpositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_hand_line_l, crv_ctrl_hand_line, crv_ctrl_hand_line_r], self.liklegfootctrl_tn)

                    self.lfootoption_tn = self.MDag2_node.create("transform", "Biped_LeftFootOptions_ctrl", lleg_sl_ls.getDependNode(2))
                    ctrl_lfootoption_cv = self.MNurbs2_cv.createWithEditPoints(ctrl_lhandoption_line, 1, 1, False, True, True, self.lfootoption_tn)

                    self.noflipllegkneenull_tn = self.MDag2_node.create("transform", "Biped_NoFlipLeftKnee_null", self.liklegfootoffsetnull_tn)
                    self.noflipllegkneectrl_tn = self.MDag2_node.create("transform", "Biped_NoFlipLeftKnee_ctrl", self.noflipllegkneenull_tn)
                    self.noflipllegknectrl_tn = self.MDag2_node.create("locator", "NoFlipLeftKnee_shape", self.noflipllegkneectrl_tn)

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

                    self.MDG2_mod.renameNode(ctrl_llegfootpositive_comb_cv, "LeftLegFoot_shape")
                    self.MDG2_mod.renameNode(ctrl_liklegfootpositive_comb_cv, "LeftIkLegFoot_shape")
                    self.MDG2_mod.renameNode(ctrl_lfootoption_cv, "LeftFootOptions_shape")
                    self.MDG2_mod.commandToExecute('color -rgbColor 0 1 1 "Biped_FkLeftFoot_ctrl"')
                    self.MDG2_mod.commandToExecute('color -rgbColor 1 0 1 "Biped_IkLeftFoot_ctrl"')
                    self.MDG2_mod.commandToExecute('color -rgbColor 1 1 0 "Biped_LeftFootOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkLeftFoot_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_IkLeftFoot_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_LeftFootOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_null.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_null.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_null.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_null.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_null.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_null.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_null.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_null.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_null.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_null.visibility"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox true "Biped_FkLeftFoot_ctrl.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox true "Biped_FkLeftFoot_ctrl.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox true "Biped_FkLeftFoot_ctrl.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftFoot_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkLeftFoot_ctrl.visibility"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_null.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_null.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_null.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_null.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_null.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_null.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_null.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_null.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_null.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_null.visibility"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFoot_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_IkLeftFoot_ctrl.visibility"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFootOffset_null.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFootOffset_null.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFootOffset_null.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFootOffset_null.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFootOffset_null.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFootOffset_null.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFootOffset_null.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFootOffset_null.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFootOffset_null.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkLeftFootOffset_null.visibility"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFootOptions_ctrl.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFootOptions_ctrl.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFootOptions_ctrl.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFootOptions_ctrl.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFootOptions_ctrl.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFootOptions_ctrl.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFootOptions_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFootOptions_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFootOptions_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_LeftFootOptions_ctrl.visibility"')
                    self.MDG2_mod.doIt()

                    liklegfootctrl_path_n = om2.MDagPath()
                    liklegfootctrl_path = liklegfootctrl_path_n.getAPathTo(self.liklegfootctrl_tn)
                    liklegfootctrl_worldtransform = om2.MFnTransform(liklegfootctrl_path)

                    liklegfootctrl_worldtransform.setRotatePivot(om2.MPoint(jnt_lleg_t), om2.MSpace.kWorld, False)

                elif index == 3:
                    self.llegtoebasenull_tn = self.MDag2_node.create("transform", "Biped_FkLeftToeBase_null", self.llegfootctrl_tn)
                    self.llegtoebasectrl_tn = self.MDag2_node.create("transform", "Biped_FkLeftToeBase_ctrl", self.llegtoebasenull_tn)
                    ctrl_llegtoepositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.llegtoebasectrl_tn)

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

                    self.MDG2_mod.renameNode(ctrl_llegtoepositive_comb_cv, "LeftLegToeBase_shape")
                    self.MDG2_mod.commandToExecute('color -rgbColor 0 1 1 "Biped_FkLeftToeBase_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkLeftToeBase_ctrl"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_null.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_null.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_null.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_null.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_null.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_null.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_null.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_null.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_null.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_null.visibility"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_ctrl.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_ctrl.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_ctrl.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkLeftToeBase_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkLeftToeBase_ctrl.visibility"')
                    self.MDG2_mod.doIt()

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

        self.draw_shoulder_tn = self.MDag2_node.create("transform", "Draw_shoulder_ctrl")
        crv_ctrl_rshoulder_arc_l = self.MNurbs2_cv.createWithEditPoints(ctrl_rshoulder_arc_l, 3, 1, False, True, True, self.draw_shoulder_tn)
        crv_ctrl_rshoulder_line = self.MNurbs2_cv.createWithEditPoints(ctrl_rshoulder_line, 1, 1, False, True, True, self.draw_shoulder_tn)
        crv_ctrl_rshoulder_arc_r = self.MNurbs2_cv.createWithEditPoints(ctrl_rshoulder_arc_r, 3, 1, False, True, True, self.draw_shoulder_tn)

        if self.autostretch.currentIndex() == 1:
            self.rshouldernull_tn = self.MDag2_node.create("transform", "Biped_RightShoulder_null", self.stretchyspine_tn)
        else:
            self.rshouldernull_tn = self.MDag2_node.create("transform", "Biped_RightShoulder_null", self.spinectrl_tn)

        self.rshoulderctrl_tn = self.MDag2_node.create("transform", "Biped_RightShoulder_ctrl", self.rshouldernull_tn)
        ctrl_rshoulder_comb_cv = self.MNurbs2_cv.create([crv_ctrl_rshoulder_arc_l, crv_ctrl_rshoulder_line, crv_ctrl_rshoulder_arc_r], self.rshoulderctrl_tn)

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

        self.MDG2_mod.commandToExecute('delete "Draw_shoulder_ctrl"')
        self.MDG2_mod.renameNode(ctrl_rshoulder_comb_cv, "RightShoulder_shape")
        self.MDG2_mod.commandToExecute('color -rgbColor 1 0 0 "Biped_RightShoulder_ctrl"')
        self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightShoulder_ctrl"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_null.translateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_null.translateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_null.translateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_null.rotateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_null.rotateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_null.rotateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_null.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_null.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_null.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_null.visibility"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_ctrl.translateX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_ctrl.translateY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_ctrl.translateZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_ctrl.scaleX"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_ctrl.scaleY"')
        self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightShoulder_ctrl.scaleZ"')
        self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_RightShoulder_ctrl.visibility"')
        self.MDG2_mod.doIt()

        for index in range(fkrarm_sl_ls.length()):
           jnt_rhand_obj = fkrarm_sl_ls.getDependNode(index)
           rhand_path_n = om2.MDagPath()
           rhand_path = rhand_path_n.getAPathTo(jnt_rhand_obj)
           jnt_rhand_transform = om2.MFnTransform(rhand_path)
           jnt_rhand_t = jnt_rhand_transform.translation(om2.MSpace.kWorld)

           if index == 1:
               self.rarmnull_tn = self.MDag2_node.create("transform", "Biped_FkRightArm_null", self.rshoulderctrl_tn)
               self.rarmctrl_tn = self.MDag2_node.create("transform", "Biped_FkRightArm_ctrl", self.rarmnull_tn)
               ctrl_larm_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rarmctrl_tn)

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

               self.MDG2_mod.renameNode(ctrl_larm_comb_cv, "FkRightArm_shape")
               self.MDG2_mod.commandToExecute('color -rgbColor 0 1 1 "Biped_FkRightArm_ctrl"')
               self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkRightArm_ctrl"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.rotateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.rotateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.rotateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.visibility"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_null.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_ctrl.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_ctrl.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightArm_ctrl.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkRightArm_ctrl.visibility"')
               self.MDG2_mod.doIt()

           elif index == 2:
               self.rforearmnull_tn = self.MDag2_node.create("transform", "Biped_FkRightForeArm_null", self.rarmctrl_tn)
               self.rforearmctrl_tn = self.MDag2_node.create("transform", "Biped_FkRightForeArm_ctrl", self.rforearmnull_tn)
               ctrl_rforearm_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rforearmctrl_tn)

               self.pvrelbownull_tn = self.MDag2_node.create("transform", "Biped_PVRightElbow_null", self.masterctrl_tn)
               self.pvrelbowctrl_tn = self.MDag2_node.create("transform", "Biped_PVRightElbow_ctrl", self.pvrelbownull_tn)
               crv_ctrl_elbow_triangle_l = self.MNurbs2_cv.createWithEditPoints(ctrl_elbow_triangle_points, 1, 1, False, True, True, self.pvrelbowctrl_tn)
               crv_ctrl_elbow_arrow_l = self.MNurbs2_cv.createWithEditPoints(ctrl_elbow_arrow_points, 1, 1, False, True, True, self.pvrelbowctrl_tn)

               rforearmnull_transform = om2.MFnTransform(self.rforearmnull_tn)
               rforearmnull_transform.setRotatePivotTranslation(jnt_rhand_t, om2.MSpace.kTransform)

               pvrelbownull_transform = om2.MFnTransform(self.pvrelbownull_tn)
               pvrelbownull_transform.setTranslation(jnt_rhand_t, om2.MSpace.kTransform)

               jnt_rforearm_r = cmds.xform("RightForeArm", query=True, rotation=True, worldSpace=True)

               radian_rforearm_x = (jnt_rforearm_r[0]/180)*3.1415
               radian_rforearm_y = (jnt_rforearm_r[1]/180)*3.1415
               radian_rforearm_z = (jnt_rforearm_r[2]/180)*3.1415

               rforearmnull_transform_r = rforearmnull_transform.rotation(om2.MSpace.kTransform)
               rforearmnull_transform_r[0], rforearmnull_transform_r[1], rforearmnull_transform_r[2] = radian_rforearm_x, radian_rforearm_y, radian_rforearm_z
               rforearmnull_transform.setRotation(rforearmnull_transform_r, om2.MSpace.kTransform)

               rforearmctrl_transform = om2.MFnTransform(self.rforearmctrl_tn)

               pvrelbowctrl_transform = om2.MFnTransform(self.pvrelbowctrl_tn)

               rforearmctrl_transform_r = rforearmctrl_transform.rotation(om2.MSpace.kTransform)
               rforearmctrl_transform_r[1] = 3.1415
               rforearmctrl_transform.setRotation(rforearmctrl_transform_r, om2.MSpace.kTransform)

               rforearmctrl_transform_s = rforearmctrl_transform.findPlug("scale", False)
               if rforearmctrl_transform_s.isCompound:
                   for i in range(rforearmctrl_transform_s.numChildren()):
                       child_plug = rforearmctrl_transform_s.child(i)
                       attr_value = child_plug.setDouble(box_transform_s[0]/2)

               pvrelbownull_transform_t = pvrelbownull_transform.translation(om2.MSpace.kTransform)
               pvrelbownull_transform_t[2] = -(pvrelbownull_transform_t[2]+8)
               pvrelbownull_transform.setTranslation(pvrelbownull_transform_t, om2.MSpace.kTransform)

               pvrelbowctrl_transform_r = pvrelbowctrl_transform.rotation(om2.MSpace.kTransform)
               pvrelbowctrl_transform_r[0] = -1.57079
               pvrelbowctrl_transform.setRotation(pvrelbowctrl_transform_r, om2.MSpace.kTransform)

               rforearmnull_transform_trans = rforearmnull_transform.transformation()
               rforearmnull_transform_worldmatrix = rforearmnull_transform_trans.asMatrix()

               rforearmnull_transform_localmatrix = rforearmnull_transform_worldmatrix * spinenull_parentinvtransform_matrix * spinenull_childtransform_localmatrix.inverse() * rshouldernullnull_transform_localmatrix.inverse() * rarmnull_transform_localmatrix.inverse()

               rforearmnull_transform.setTransformation(om2.MTransformationMatrix(rforearmnull_transform_localmatrix))

               self.MDG2_mod.renameNode(ctrl_rforearm_comb_cv, "FkRightForeArm_shape")
               self.MDG2_mod.renameNode(crv_ctrl_elbow_triangle_l, "PVRightElbow_shape1")
               self.MDG2_mod.renameNode(crv_ctrl_elbow_arrow_l, "PVRightElbow_shape2")
               self.MDG2_mod.commandToExecute('color -rgbColor 0 1 1 "Biped_FkRightForeArm_ctrl"')
               self.MDG2_mod.commandToExecute('color -rgbColor 1 1 0 "Biped_PVRightElbow_ctrl"')
               self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkRightForeArm_ctrl"')
               self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_PVRightElbow_ctrl"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_null.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_null.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_null.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_null.rotateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_null.rotateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_null.rotateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_null.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_null.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_null.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_null.visibility"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkRightForeArm_ctrl.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkRightForeArm_ctrl.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkRightForeArm_ctrl.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_ctrl.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_ctrl.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightForeArm_ctrl.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkRightForeArm_ctrl.visibility"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightElbow_null.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightElbow_null.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightElbow_null.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightElbow_null.rotateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightElbow_null.rotateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightElbow_null.rotateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightElbow_null.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightElbow_null.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightElbow_null.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightElbow_null.visibility"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightElbow_ctrl.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightElbow_ctrl.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightElbow_ctrl.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightElbow_ctrl.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightElbow_ctrl.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightElbow_ctrl.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_PVRightElbow_ctrl.visibility"')
               self.MDG2_mod.doIt()
        #
           elif index == 3:
               ctrl_rhand_line_up_points = [om2.MPoint(0.00, 0.05, 0.02), om2.MPoint(-0.60, 0.05, 0.02)]
               ctrl_rhand_star_up_points = [om2.MPoint(-0.60, 0.05, 0.02), om2.MPoint(-0.70, 0.15, 0.20), om2.MPoint(-0.70, 0.09, 0.20), om2.MPoint(-0.70, 0.06, 0.13), om2.MPoint(-0.60, 0.00, 0.00), om2.MPoint(-0.70, 0.05, -0.13), om2.MPoint(-0.70, 0.09, -0.20), om2.MPoint(-0.70, 0.15, -0.20), om2.MPoint(-0.60, 0.05, -0.02)]
               ctrl_rhand_line_down_points = [om2.MPoint(-0.60, 0.05, -0.02), om2.MPoint(-0.00, 0.05, -0.02)]

               self.draw_rhand_tn = self.MDag2_node.create("transform", "Draw_righthand_ctrl")
               crv_ctrl_rhand_line_up = self.MNurbs2_cv.createWithEditPoints(ctrl_rhand_line_up_points, 1, 1, False, True, True, self.draw_rhand_tn)
               crv_ctrl_rhand_star = self.MNurbs2_cv.createWithEditPoints(ctrl_rhand_star_up_points, 1, 1, False, True, True, self.draw_rhand_tn)
               crv_ctrl_rhand_line_down = self.MNurbs2_cv.createWithEditPoints(ctrl_rhand_line_down_points, 1, 1, False, True, True, self.draw_rhand_tn)

               self.rhandnull_tn = self.MDag2_node.create("transform", "Biped_FkRightHand_null", self.rforearmctrl_tn)
               self.rhandctrl_tn = self.MDag2_node.create("transform", "Biped_FkRightHand_ctrl", self.rhandnull_tn)
               ctrl_rhandpositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rhandctrl_tn)
               ctrl_rhandnegative_comb_cv = self.MNurbs2_cv.create([crv_ctrl_rhand_line_up, crv_ctrl_rhand_star, crv_ctrl_rhand_line_down], self.rhandctrl_tn)

               self.rfingernull_tn = self.MDag2_node.create("transform", "Biped_RightFingers_null", self.masterctrl_tn)
               self.rhandoption_tn = self.MDag2_node.create("transform", "Biped_RightHandOptions_ctrl", rarm_sl_ls.getDependNode(2))
               ctrl_rhandoption_cv = self.MNurbs2_cv.createWithEditPoints(ctrl_lhandoption_line, 1, 1, False, True, True, self.rhandoption_tn)

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
               rhandoptionctrl_transform_t[2] = jnt_lhand_t[2]-5
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

               self.MDG2_mod.renameNode(ctrl_rhandpositive_comb_cv, "FkRightHand_shape1")
               self.MDG2_mod.renameNode(ctrl_rhandnegative_comb_cv, "FkRightHand_shape2")
               self.MDG2_mod.renameNode(ctrl_rhandoption_cv, "RightHandOptions_shape")
               self.MDG2_mod.commandToExecute('color -rgbColor 0 1 1 "Biped_FkRightHand_ctrl"')
               self.MDG2_mod.commandToExecute('color -rgbColor 1 1 0 "Biped_RightHandOptions_ctrl"')
               self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkRightHand_ctrl"')
               self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightHandOptions_ctrl"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_null.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_null.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_null.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_null.rotateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_null.rotateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_null.rotateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_null.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_null.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_null.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_null.visibility"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkRightHand_ctrl.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkRightHand_ctrl.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkRightHand_ctrl.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_ctrl.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_ctrl.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightHand_ctrl.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkRightHand_ctrl.visibility"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingers_null.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingers_null.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingers_null.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingers_null.rotateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingers_null.rotateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingers_null.rotateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingers_null.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingers_null.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingers_null.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingers_null.visibility"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightHandOptions_ctrl.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightHandOptions_ctrl.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightHandOptions_ctrl.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightHandOptions_ctrl.rotateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightHandOptions_ctrl.rotateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightHandOptions_ctrl.rotateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightHandOptions_ctrl.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightHandOptions_ctrl.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightHandOptions_ctrl.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightHandOptions_ctrl.visibility"')
               self.MDG2_mod.doIt()

               self.rikhandnull_tn = self.MDag2_node.create("transform", "Biped_IkRightHand_null", self.masterctrl_tn)
               self.rhandrotnull_tn = self.MDag2_node.create("transform", "Biped_IkRightHandRot_null", self.rikhandnull_tn)
               self.rikhandctrl_tn = self.MDag2_node.create("transform", "Biped_IkRightHand_ctrl", self.rhandrotnull_tn)
               ctrl_rikhand_comb_cv = self.MNurbs2_cv.create([crv_ctrl_hand_line_l, crv_ctrl_hand_line, crv_ctrl_hand_line_r], self.rikhandctrl_tn)

               self.nofliprelbownull_tn = self.MDag2_node.create("transform", "Biped_NoFlipRightElbow_null", self.rikhandnull_tn)
               self.nofliprelbowctrl_tn = self.MDag2_node.create("transform", "Biped_NoFlipRightElbow_ctrl", self.nofliprelbownull_tn)
               self.nofliprelbowctrl_ln = self.MDag2_node.create("locator", "NoFlipRightElbow_shape", self.nofliprelbowctrl_tn)

               rikhandnull_transform = om2.MFnTransform(self.rikhandnull_tn)
               rikhandnull_transform.setRotatePivotTranslation(jnt_rhand_t, om2.MSpace.kTransform)

               rikhandnull_transform_r = rikhandnull_transform.rotation(om2.MSpace.kTransform)
               rikhandnull_transform_r[0], rikhandnull_transform_r[1], rikhandnull_transform_r[2] = radian_rhand_x, radian_rhand_y, radian_rhand_z
               rikhandnull_transform.setRotation(rikhandnull_transform_r, om2.MSpace.kTransform)

               rikhandctrl_transform = om2.MFnTransform(self.rikhandctrl_tn)

               relbowctrl_transform = om2.MFnTransform(self.nofliprelbowctrl_tn)

               rikhandctrl_transform_t = rikhandctrl_transform.rotatePivotTranslation(om2.MSpace.kTransform)
               rikhandctrl_transform_t[2] = -((jnt_rhand_t[1]+4)-jnt_rhand_t[1])
               rikhandctrl_transform.setRotatePivotTranslation(rikhandctrl_transform_t, om2.MSpace.kTransform)

               rikhandctrl_transform_r = rikhandctrl_transform.rotation(om2.MSpace.kTransform)
               rikhandctrl_transform_r[0], rikhandctrl_transform_r[2] = 1.57079, 1.57079
               rikhandctrl_transform.setRotation(rikhandctrl_transform_r, om2.MSpace.kTransform)

               relbowctrl_transform_t = relbowctrl_transform.translation(om2.MSpace.kTransform)
               relbowctrl_transform_t[2] = -7
               relbowctrl_transform.setTranslation(relbowctrl_transform_t, om2.MSpace.kTransform)

               rikhandctrl_transform_s = rikhandctrl_transform.findPlug("scale", False)
               if rikhandctrl_transform_s.isCompound:
                   for i in range(rikhandctrl_transform_s.numChildren()):
                       child_plug = rikhandctrl_transform_s.child(i)
                       attr_value = child_plug.setDouble(box_transform_s[0]/3)

               self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_IkRightHand_ctrl"')
               self.MDG2_mod.doIt()

               rikhandnull_path_n = om2.MDagPath()
               rikhandnull_path = rikhandnull_path_n.getAPathTo(self.rikhandctrl_tn)
               rikhandnull_worldtransform = om2.MFnTransform(rikhandnull_path)

               rikhandnull_worldtransform.setRotatePivot(om2.MPoint(jnt_rhand_t), om2.MSpace.kWorld, False)

               self.MDG2_mod.renameNode(ctrl_rikhand_comb_cv, "IkRightHand_shape")
               self.MDG2_mod.commandToExecute('color -rgbColor 1 0 0 "Biped_IkRightHand_ctrl"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_null.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_null.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_null.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_null.rotateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_null.rotateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_null.rotateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_null.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_null.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_null.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_null.visibility"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_IkRightHand_ctrl.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_IkRightHand_ctrl.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_IkRightHand_ctrl.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_ctrl.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_ctrl.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightHand_ctrl.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_IkRightHand_ctrl.visibility"')
               self.MDG2_mod.doIt()

               self.rfingerctrl_tn = self.MDag2_node.create("transform", "Biped_RightFingerOptions_ctrl", rarm_sl_ls.getDependNode(2))
               ctrl_rfingerpositive_comb_cv = self.MNurbs2_cv.createWithEditPoints(ctrl_master_circle_points, 1, 1, False, True, True, self.rfingerctrl_tn)

               rfingerctrl_transform = om2.MFnTransform(self.rfingerctrl_tn)

               rfingerctrl_transform_r = rfingerctrl_transform.rotation(om2.MSpace.kTransform)
               rfingerctrl_transform_r[1] = 3.1415
               rfingerctrl_transform.setRotation(rfingerctrl_transform_r, om2.MSpace.kTransform)

               rfingerctrl_transform_s = rfingerctrl_transform.findPlug("scale", False)
               if rfingerctrl_transform_s.isCompound:
                   for i in range(rfingerctrl_transform_s.numChildren()):
                       child_plug = rfingerctrl_transform_s.child(i)
                       attr_value = child_plug.setDouble(box_transform_s[0]/3)

               self.MDG2_mod.renameNode(ctrl_rfingerpositive_comb_cv, "RightFingerOptions_shape")
               self.MDG2_mod.commandToExecute('color -rgbColor 1 1 0.5 "Biped_RightFingerOptions_ctrl"')
               self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightFingerOptions_ctrl"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerOptions_ctrl.translateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerOptions_ctrl.translateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerOptions_ctrl.translateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerOptions_ctrl.rotateX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerOptions_ctrl.rotateY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerOptions_ctrl.rotateZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerOptions_ctrl.scaleX"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerOptions_ctrl.scaleY"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerOptions_ctrl.scaleZ"')
               self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerOptions_ctrl.visibility"')
               self.MDG2_mod.doIt()

        try:
            rhandthumb_sl_ls = om2.MSelectionList()
            rhandthumb_sl_ls.add("RightFingerThumb*")

            for index in range(rhandthumb_sl_ls.length()):
                jnt_rhandthumb_obj = rhandthumb_sl_ls.getDependNode(index)
                jnt_rhandthumb_path_n = om2.MDagPath()
                jnt_rhandthumb_path = jnt_rhandthumb_path_n.getAPathTo(jnt_rhandthumb_obj)
                jnt_rhandthumb_transform = om2.MFnTransform(jnt_rhandthumb_path)
                jnt_rhandthumb_t = jnt_rhandthumb_transform.translation(om2.MSpace.kWorld)

                self.rhandthumbnull_tn = self.MDag2_node.create("transform", "Biped_RightFingerThumb{0}_null".format(index+1))
                self.rhandthumbglobalcurl_tn = self.MDag2_node.create("transform", "Biped_RightFingerThumb{0}_globalcurl".format(index+1), self.rhandthumbnull_tn)
                self.rhandthumbcurl_tn = self.MDag2_node.create("transform", "Biped_RightFingerThumb{0}_curl".format(index+1), self.rhandthumbglobalcurl_tn)
                self.rhandthumbctrl_tn = self.MDag2_node.create("transform", "Biped_RightFingerThumb{0}_ctrl".format(index+1), self.rhandthumbcurl_tn)
                ctrl_rhandthumbpositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rhandthumbctrl_tn)
                ctrl_rhandthumbnegative_comb_cv = self.MNurbs2_cv.create([crv_ctrl_rhand_line_up, crv_ctrl_rhand_star, crv_ctrl_rhand_line_down], self.rhandthumbctrl_tn)

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

                    self.rfingerthumbctrl_tn = self.MDag2_node.create("transform", "Biped_RightThumbOptions_ctrl")
                    ctrl_rfingerthumbpositive_comb_cv = self.MNurbs2_cv.createWithEditPoints(ctrl_master_circle_points, 1, 1, False, True, True, self.rfingerthumbctrl_tn)

                    rfingerthumbctrl_transform = om2.MFnTransform(self.rfingerthumbctrl_tn)

                    rfingerthumbctrl_transform_t = rfingerthumbctrl_transform.translation(om2.MSpace.kTransform)
                    rfingerthumbctrl_transform_t[0], rfingerthumbctrl_transform_t[1], rfingerthumbctrl_transform_t[2] = jnt_rhandthumb_t[0], jnt_rhandthumb_t[1], jnt_rhandthumb_t[2]
                    rfingerthumbctrl_transform.setTranslation(rfingerthumbctrl_transform_t, om2.MSpace.kTransform)

                    rfingerthumbctrl_transform_r= rfingerthumbctrl_transform.rotation(om2.MSpace.kTransform)
                    rfingerthumbctrl_transform_r[0], rfingerthumbctrl_transform_r[1], rfingerthumbctrl_transform_r[2] = rhandthumbnull_transform_r[0], rhandthumbnull_transform_r[1], rhandthumbnull_transform_r[2]
                    rfingerthumbctrl_transform.setRotation(rfingerthumbctrl_transform_r, om2.MSpace.kTransform)

                    rfingerthumbctrl_transform_s = rfingerthumbctrl_transform.findPlug("scale", False)
                    if rfingerthumbctrl_transform_s.isCompound:
                        for i in range(rfingerthumbctrl_transform_s.numChildren()):
                            child_plug = rfingerthumbctrl_transform_s.child(i)
                            if i == 0:
                                attr_value = child_plug.setDouble(-(box_transform_s[0]/9))
                            else:
                                attr_value = child_plug.setDouble(box_transform_s[0]/9)

                    rhandjnt_tr_n = om2.MFnDagNode(rarm_sl_ls.getDependNode(2))
                    rhandjnt_tr_n.addChild(self.rfingerthumbctrl_tn)

                    rfingerthumbctrl_transform_trans = rfingerthumbctrl_transform.transformation()
                    rfingerthumbctrl_transform_worldmatrix = rfingerthumbctrl_transform_trans.asMatrix()

                    rfingerthumbctrl_transform_localmatrix = rfingerthumbctrl_transform_worldmatrix * rfingernull_transform_worldmatrix

                    rfingerthumbctrl_transform.setTransformation(om2.MTransformationMatrix(rfingerthumbctrl_transform_localmatrix))

                    self.MDG2_mod.renameNode(ctrl_rfingerthumbpositive_comb_cv, "RightThumbOptions_shape")
                    self.MDG2_mod.commandToExecute('color -rgbColor 1 1 0.5 "Biped_RightThumbOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightThumbOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightThumbOptions_ctrl.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightThumbOptions_ctrl.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightThumbOptions_ctrl.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightThumbOptions_ctrl.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightThumbOptions_ctrl.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightThumbOptions_ctrl.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightThumbOptions_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightThumbOptions_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightThumbOptions_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightThumbOptions_ctrl.visibility"')

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

                self.MDG2_mod.renameNode(ctrl_rhandthumbpositive_comb_cv, "RightFingerThumb{0}_shape1".format(index + 1))
                self.MDG2_mod.renameNode(ctrl_rhandthumbnegative_comb_cv, "RightFingerThumb{0}_shape2".format(index + 1))
                self.MDG2_mod.commandToExecute('color -rgbColor 0 1 0 "Biped_RightFingerThumb{0}_ctrl"'.format(index + 1))
                self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightFingerThumb{0}_ctrl"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_null.translateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_null.translateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_null.translateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_null.rotateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_null.rotateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_null.rotateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_null.scaleX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_null.scaleY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_null.scaleZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_null.visibility"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_RightFingerThumb{0}_ctrl.translateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_RightFingerThumb{0}_ctrl.translateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_RightFingerThumb{0}_ctrl.translateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_ctrl.scaleX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_ctrl.scaleY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerThumb{0}_ctrl.scaleZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_RightFingerThumb{0}_ctrl.visibility"'.format(index + 1))
                self.MDG2_mod.doIt()

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

                self.rhandindexnull_tn = self.MDag2_node.create("transform", "Biped_RightFingerIndex{0}_null".format(index+1))
                self.rhandindexglobalcurl_tn = self.MDag2_node.create("transform", "Biped_RightFingerIndex{0}_globalcurl".format(index+1), self.rhandindexnull_tn)
                self.rhandindexcurl_tn = self.MDag2_node.create("transform", "Biped_RightFingerIndex{0}_curl".format(index+1), self.rhandindexglobalcurl_tn)
                self.rhandindexctrl_tn = self.MDag2_node.create("transform", "Biped_RightFingerIndex{0}_ctrl".format(index+1), self.rhandindexcurl_tn)
                ctrl_rhandIndexpositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rhandindexctrl_tn)
                ctrl_rhandIndexnegative_comb_cv = self.MNurbs2_cv.create([crv_ctrl_rhand_line_up, crv_ctrl_rhand_star, crv_ctrl_rhand_line_down], self.rhandindexctrl_tn)

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

                    self.rfingerindexctrl_tn = self.MDag2_node.create("transform", "Biped_RightIndexOptions_ctrl")
                    ctrl_rfingerindexpositive_comb_cv = self.MNurbs2_cv.createWithEditPoints(ctrl_master_circle_points, 1, 1, False, True, True, self.rfingerindexctrl_tn)

                    rfingerindexctrl_transform = om2.MFnTransform(self.rfingerindexctrl_tn)

                    rfingerindexctrl_transform_t = rfingerindexctrl_transform.translation(om2.MSpace.kTransform)
                    rfingerindexctrl_transform_t[0], rfingerindexctrl_transform_t[1], rfingerindexctrl_transform_t[2] = jnt_rhandindex_t[0], jnt_rhandindex_t[1], jnt_rhandindex_t[2]
                    rfingerindexctrl_transform.setTranslation(rfingerindexctrl_transform_t, om2.MSpace.kTransform)

                    rfingerindexctrl_transform_r= rfingerindexctrl_transform.rotation(om2.MSpace.kTransform)
                    rfingerindexctrl_transform_r[0], rfingerindexctrl_transform_r[1], rfingerindexctrl_transform_r[2] = rhandindexnull_transform_r[0], rhandindexnull_transform_r[1], rhandindexnull_transform_r[2]
                    rfingerindexctrl_transform.setRotation(rfingerindexctrl_transform_r, om2.MSpace.kTransform)

                    rfingerindexctrl_transform_s = rfingerindexctrl_transform.findPlug("scale", False)
                    if rfingerindexctrl_transform_s.isCompound:
                        for i in range(rfingerindexctrl_transform_s.numChildren()):
                            child_plug = rfingerindexctrl_transform_s.child(i)
                            if i == 0:
                                attr_value = child_plug.setDouble(-(box_transform_s[0]/9))
                            else:
                                attr_value = child_plug.setDouble(box_transform_s[0]/9)

                    rhandjnt_tr_n.addChild(self.rfingerindexctrl_tn)

                    rfingerindexctrl_transform_trans = rfingerindexctrl_transform.transformation()
                    rfingerindexctrl_transform_worldmatrix = rfingerindexctrl_transform_trans.asMatrix()

                    rfingerindexctrl_transform_localmatrix = rfingerindexctrl_transform_worldmatrix * rfingernull_transform_worldmatrix

                    rfingerindexctrl_transform.setTransformation(om2.MTransformationMatrix(rfingerindexctrl_transform_localmatrix))

                    self.MDG2_mod.renameNode(ctrl_rfingerindexpositive_comb_cv, "RightIndexOptions_shape")
                    self.MDG2_mod.commandToExecute('color -rgbColor 1 1 0.5 "Biped_RightIndexOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightIndexOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightIndexOptions_ctrl.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightIndexOptions_ctrl.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightIndexOptions_ctrl.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightIndexOptions_ctrl.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightIndexOptions_ctrl.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightIndexOptions_ctrl.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightIndexOptions_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightIndexOptions_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightIndexOptions_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightIndexOptions_ctrl.visibility"')

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

                self.MDG2_mod.renameNode(ctrl_rhandIndexpositive_comb_cv, "RightFingerIndex{0}_shape1".format(index + 1))
                self.MDG2_mod.renameNode(ctrl_rhandIndexnegative_comb_cv, "RightFingerIndex{0}_shape2".format(index + 1))
                self.MDG2_mod.commandToExecute('color -rgbColor 0 1 0 "Biped_RightFingerIndex{0}_ctrl"'.format(index + 1))
                self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightFingerIndex{0}_ctrl"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_null.translateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_null.translateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_null.translateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_null.rotateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_null.rotateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_null.rotateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_null.scaleX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_null.scaleY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_null.scaleZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_null.visibility"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_RightFingerIndex{0}_ctrl.translateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_RightFingerIndex{0}_ctrl.translateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_RightFingerIndex{0}_ctrl.translateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_ctrl.scaleX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_ctrl.scaleY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerIndex{0}_ctrl.scaleZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_RightFingerIndex{0}_ctrl.visibility"'.format(index + 1))
                self.MDG2_mod.doIt()

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

                self.rhandmiddlenull_tn = self.MDag2_node.create("transform", "Biped_RightFingerMiddle{0}_null".format(index + 1))
                self.rhandmiddleglobalcurl_tn = self.MDag2_node.create("transform", "Biped_RightFingerMiddle{0}_globalcurl".format(index+1), self.rhandmiddlenull_tn)
                self.rhandmiddlecurl_tn = self.MDag2_node.create("transform", "Biped_RightFingerMiddle{0}_curl".format(index+1), self.rhandmiddleglobalcurl_tn)
                self.rhandmiddlectrl_tn = self.MDag2_node.create("transform", "Biped_RightFingerMiddle{0}_ctrl".format(index + 1), self.rhandmiddlecurl_tn)
                ctrl_rhandmiddlepositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rhandmiddlectrl_tn)
                ctrl_rhandmiddlenegative_comb_cv = self.MNurbs2_cv.create([crv_ctrl_rhand_line_up, crv_ctrl_rhand_star, crv_ctrl_rhand_line_down], self.rhandmiddlectrl_tn)

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

                    self.rfingermiddlectrl_tn = self.MDag2_node.create("transform", "Biped_RightMiddleOptions_ctrl")
                    ctrl_rfingermiddlepositive_comb_cv = self.MNurbs2_cv.createWithEditPoints(ctrl_master_circle_points, 1, 1, False, True, True, self.rfingermiddlectrl_tn)

                    rfingermiddlectrl_transform = om2.MFnTransform(self.rfingermiddlectrl_tn)

                    rfingermiddlectrl_transform_t = rfingermiddlectrl_transform.translation(om2.MSpace.kTransform)
                    rfingermiddlectrl_transform_t[0], rfingermiddlectrl_transform_t[1], rfingermiddlectrl_transform_t[2] = jnt_rhandmiddle_t[0], jnt_rhandmiddle_t[1], jnt_rhandmiddle_t[2]
                    rfingermiddlectrl_transform.setTranslation(rfingermiddlectrl_transform_t, om2.MSpace.kTransform)

                    rfingermiddlectrl_transform_r= rfingermiddlectrl_transform.rotation(om2.MSpace.kTransform)
                    rfingermiddlectrl_transform_r[0], rfingermiddlectrl_transform_r[1], rfingermiddlectrl_transform_r[2] = rhandmiddlenull_transform_r[0], rhandmiddlenull_transform_r[1], rhandmiddlenull_transform_r[2]
                    rfingermiddlectrl_transform.setRotation(rfingermiddlectrl_transform_r, om2.MSpace.kTransform)

                    rfingermiddlectrl_transform_s = rfingermiddlectrl_transform.findPlug("scale", False)
                    if rfingermiddlectrl_transform_s.isCompound:
                        for i in range(rfingermiddlectrl_transform_s.numChildren()):
                            child_plug = rfingermiddlectrl_transform_s.child(i)
                            if i == 0:
                                attr_value = child_plug.setDouble(-(box_transform_s[0]/9))
                            else:
                                attr_value = child_plug.setDouble(box_transform_s[0]/9)

                    rhandjnt_tr_n.addChild(self.rfingermiddlectrl_tn)

                    rfingermiddlectrl_transform_trans = rfingermiddlectrl_transform.transformation()
                    rfingermiddlectrl_transform_worldmatrix = rfingermiddlectrl_transform_trans.asMatrix()

                    rfingermiddlectrl_transform_localmatrix = rfingermiddlectrl_transform_worldmatrix * rfingernull_transform_worldmatrix

                    rfingermiddlectrl_transform.setTransformation(om2.MTransformationMatrix(rfingermiddlectrl_transform_localmatrix))

                    self.MDG2_mod.renameNode(ctrl_rfingermiddlepositive_comb_cv, "RightMiddleOptions_shape")
                    self.MDG2_mod.commandToExecute('color -rgbColor 1 1 0.5 "Biped_RightMiddleOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightMiddleOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightMiddleOptions_ctrl.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightMiddleOptions_ctrl.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightMiddleOptions_ctrl.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightMiddleOptions_ctrl.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightMiddleOptions_ctrl.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightMiddleOptions_ctrl.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightMiddleOptions_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightMiddleOptions_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightMiddleOptions_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightMiddleOptions_ctrl.visibility"')

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

                self.MDG2_mod.renameNode(ctrl_rhandmiddlepositive_comb_cv, "RightFingerMiddle{0}_shape1".format(index + 1))
                self.MDG2_mod.renameNode(ctrl_rhandmiddlenegative_comb_cv, "RightFingerMiddle{0}_shape2".format(index + 1))
                self.MDG2_mod.commandToExecute('color -rgbColor 0 1 0 "Biped_RightFingerMiddle{0}_ctrl"'.format(index + 1))
                self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightFingerMiddle{0}_ctrl"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_null.translateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_null.translateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_null.translateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_null.rotateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_null.rotateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_null.rotateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_null.scaleX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_null.scaleY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_null.scaleZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_null.visibility"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_RightFingerMiddle{0}_ctrl.translateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_RightFingerMiddle{0}_ctrl.translateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_RightFingerMiddle{0}_ctrl.translateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_ctrl.scaleX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_ctrl.scaleY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerMiddle{0}_ctrl.scaleZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_RightFingerMiddle{0}_ctrl.visibility"'.format(index + 1))
                self.MDG2_mod.doIt()

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

                self.rhandringnull_tn = self.MDag2_node.create("transform", "Biped_RightFingerRing{0}_null".format(index + 1))
                self.rhandringglobalcurl_tn = self.MDag2_node.create("transform", "Biped_RightFingerRing{0}_globalcurl".format(index+1), self.rhandringnull_tn)
                self.rhandringcurl_tn = self.MDag2_node.create("transform", "Biped_RightFingerRing{0}_curl".format(index+1), self.rhandringglobalcurl_tn)
                self.rhandringctrl_tn = self.MDag2_node.create("transform", "Biped_RightFingerRing{0}_ctrl".format(index + 1), self.rhandringcurl_tn)
                ctrl_rhandringpositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rhandringctrl_tn)
                ctrl_rhandringnegative_comb_cv = self.MNurbs2_cv.create([crv_ctrl_rhand_line_up, crv_ctrl_rhand_star, crv_ctrl_rhand_line_down], self.rhandringctrl_tn)

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

                    self.rfingerringctrl_tn = self.MDag2_node.create("transform", "Biped_RightRingOptions_ctrl")
                    ctrl_rfingerringpositive_comb_cv = self.MNurbs2_cv.createWithEditPoints(ctrl_master_circle_points, 1, 1, False, True, True, self.rfingerringctrl_tn)

                    rfingerringctrl_transform = om2.MFnTransform(self.rfingerringctrl_tn)

                    rfingerringctrl_transform_t = rfingerringctrl_transform.translation(om2.MSpace.kTransform)
                    rfingerringctrl_transform_t[0], rfingerringctrl_transform_t[1], rfingerringctrl_transform_t[2] = jnt_rhandring_t[0], jnt_rhandring_t[1], jnt_rhandring_t[2]
                    rfingerringctrl_transform.setTranslation(rfingerringctrl_transform_t, om2.MSpace.kTransform)

                    rfingerringctrl_transform_r= rfingerringctrl_transform.rotation(om2.MSpace.kTransform)
                    rfingerringctrl_transform_r[0], rfingerringctrl_transform_r[1], rfingerringctrl_transform_r[2] = rhandringnull_transform_r[0], rhandringnull_transform_r[1], rhandringnull_transform_r[2]
                    rfingerringctrl_transform.setRotation(rfingerringctrl_transform_r, om2.MSpace.kTransform)

                    rfingerringctrl_transform_s = rfingerringctrl_transform.findPlug("scale", False)
                    if rfingerringctrl_transform_s.isCompound:
                        for i in range(rfingerringctrl_transform_s.numChildren()):
                            child_plug = rfingerringctrl_transform_s.child(i)
                            if i == 0:
                                attr_value = child_plug.setDouble(-(box_transform_s[0]/9))
                            else:
                                attr_value = child_plug.setDouble(box_transform_s[0]/9)

                    rhandjnt_tr_n.addChild(self.rfingerringctrl_tn)

                    rfingerringctrl_transform_trans = rfingerringctrl_transform.transformation()
                    rfingerringctrl_transform_worldmatrix = rfingerringctrl_transform_trans.asMatrix()

                    rfingerringctrl_transform_localmatrix = rfingerringctrl_transform_worldmatrix * rfingernull_transform_worldmatrix

                    rfingerringctrl_transform.setTransformation(om2.MTransformationMatrix(rfingerringctrl_transform_localmatrix))

                    self.MDG2_mod.renameNode(ctrl_rfingerringpositive_comb_cv, "RightRingOptions_shape")
                    self.MDG2_mod.commandToExecute('color -rgbColor 1 1 0.5 "Biped_RightRingOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightRingOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightRingOptions_ctrl.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightRingOptions_ctrl.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightRingOptions_ctrl.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightRingOptions_ctrl.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightRingOptions_ctrl.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightRingOptions_ctrl.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightRingOptions_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightRingOptions_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightRingOptions_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightRingOptions_ctrl.visibility"')

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

                self.MDG2_mod.renameNode(ctrl_rhandringpositive_comb_cv, "RightFingerRing{0}_shape1".format(index + 1))
                self.MDG2_mod.renameNode(ctrl_rhandringnegative_comb_cv, "RightFingerRing{0}_shape2".format(index + 1))
                self.MDG2_mod.commandToExecute('color -rgbColor 0 1 0 "Biped_RightFingerRing{0}_ctrl"'.format(index + 1))
                self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightFingerRing{0}_ctrl"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_null.translateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_null.translateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_null.translateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_null.rotateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_null.rotateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_null.rotateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_null.scaleX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_null.scaleY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_null.scaleZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_null.visibility"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_RightFingerRing{0}_ctrl.translateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_RightFingerRing{0}_ctrl.translateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_RightFingerRing{0}_ctrl.translateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_ctrl.scaleX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_ctrl.scaleY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerRing{0}_ctrl.scaleZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_RightFingerRing{0}_ctrl.visibility"'.format(index + 1))
                self.MDG2_mod.doIt()

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

                self.rhandpinkynull_tn = self.MDag2_node.create("transform", "Biped_RightFingerPinky{0}_null".format(index + 1))
                self.rhandpinkyglobalcurl_tn = self.MDag2_node.create("transform", "Biped_RightFingerPinky{0}_globalcurl".format(index+1), self.rhandpinkynull_tn)
                self.rhandpinkycurl_tn = self.MDag2_node.create("transform", "Biped_RightFingerPinky{0}_curl".format(index+1), self.rhandpinkyglobalcurl_tn)
                self.rhandpinkyctrl_tn = self.MDag2_node.create("transform", "Biped_RightFingerPinky{0}_ctrl".format(index + 1), self.rhandpinkycurl_tn)
                ctrl_rhandpinkypositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rhandpinkyctrl_tn)
                ctrl_rhandpinkynegative_comb_cv = self.MNurbs2_cv.create([crv_ctrl_rhand_line_up, crv_ctrl_rhand_star, crv_ctrl_rhand_line_down], self.rhandpinkyctrl_tn)

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

                    self.rfingerpinkyctrl_tn = self.MDag2_node.create("transform", "Biped_RightPinkyOptions_ctrl")
                    ctrl_rfingerpinkypositive_comb_cv = self.MNurbs2_cv.createWithEditPoints(ctrl_master_circle_points, 1, 1, False, True, True, self.rfingerpinkyctrl_tn)

                    rfingerpinkyctrl_transform = om2.MFnTransform(self.rfingerpinkyctrl_tn)

                    rfingerpinkyctrl_transform_t = rfingerpinkyctrl_transform.translation(om2.MSpace.kTransform)
                    rfingerpinkyctrl_transform_t[0], rfingerpinkyctrl_transform_t[1], rfingerpinkyctrl_transform_t[2] = jnt_rhandpinky_t[0], jnt_rhandpinky_t[1], jnt_rhandpinky_t[2]
                    rfingerpinkyctrl_transform.setTranslation(rfingerpinkyctrl_transform_t, om2.MSpace.kTransform)

                    rfingerpinkyctrl_transform_r= rfingerpinkyctrl_transform.rotation(om2.MSpace.kTransform)
                    rfingerpinkyctrl_transform_r[0], rfingerpinkyctrl_transform_r[1], rfingerpinkyctrl_transform_r[2] = rhandpinkynull_transform_r[0], rhandpinkynull_transform_r[1], rhandpinkynull_transform_r[2]
                    rfingerpinkyctrl_transform.setRotation(rfingerpinkyctrl_transform_r, om2.MSpace.kTransform)

                    rfingerpinkyctrl_transform_s = rfingerpinkyctrl_transform.findPlug("scale", False)
                    if rfingerpinkyctrl_transform_s.isCompound:
                        for i in range(rfingerpinkyctrl_transform_s.numChildren()):
                            child_plug = rfingerpinkyctrl_transform_s.child(i)
                            if i == 0:
                                attr_value = child_plug.setDouble(-(box_transform_s[0]/9))
                            else:
                                attr_value = child_plug.setDouble(box_transform_s[0]/9)

                    rhandjnt_tr_n.addChild(self.rfingerpinkyctrl_tn)

                    rfingerpinkyctrl_transform_trans = rfingerpinkyctrl_transform.transformation()
                    rfingerpinkyctrl_transform_worldmatrix = rfingerpinkyctrl_transform_trans.asMatrix()

                    rfingerpinkyctrl_transform_localmatrix = rfingerpinkyctrl_transform_worldmatrix * rfingernull_transform_worldmatrix

                    rfingerpinkyctrl_transform.setTransformation(om2.MTransformationMatrix(rfingerpinkyctrl_transform_localmatrix))

                    self.MDG2_mod.renameNode(ctrl_rfingerpinkypositive_comb_cv, "RightPinkyOptions_shape")
                    self.MDG2_mod.commandToExecute('color -rgbColor 1 1 0.5 "Biped_RightPinkyOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightPinkyOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightPinkyOptions_ctrl.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightPinkyOptions_ctrl.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightPinkyOptions_ctrl.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightPinkyOptions_ctrl.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightPinkyOptions_ctrl.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightPinkyOptions_ctrl.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightPinkyOptions_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightPinkyOptions_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightPinkyOptions_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightPinkyOptions_ctrl.visibility"')

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

                self.MDG2_mod.renameNode(ctrl_rhandpinkypositive_comb_cv, "RightFingerPinky{0}_shape1".format(index + 1))
                self.MDG2_mod.renameNode(ctrl_rhandpinkynegative_comb_cv, "RightFingerPinky{0}_shape2".format(index + 1))
                self.MDG2_mod.commandToExecute('color -rgbColor 0 1 0 "Biped_RightFingerPinky{0}_ctrl"'.format(index + 1))
                self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightFingerPinky{0}_ctrl"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_null.translateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_null.translateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_null.translateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_null.rotateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_null.rotateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_null.rotateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_null.scaleX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_null.scaleY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_null.scaleZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_null.visibility"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_RightFingerPinky{0}_ctrl.translateX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_RightFingerPinky{0}_ctrl.translateY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_RightFingerPinky{0}_ctrl.translateZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_ctrl.scaleX"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_ctrl.scaleY"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFingerPinky{0}_ctrl.scaleZ"'.format(index + 1))
                self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_RightFingerPinky{0}_ctrl.visibility"'.format(index + 1))
                self.MDG2_mod.doIt()

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
                    if self.hipjnt.currentIndex() == 1:
                        self.ruplegnull_tn = self.MDag2_node.create("transform", "Biped_FkRightUpLeg_null", self.hipctrl_tn)
                    else:
                        self.ruplegnull_tn = self.MDag2_node.create("transform", "Biped_FkRightUpLeg_null", self.rootctrl_tn)

                    self.ruplegupctrl_tn = self.MDag2_node.create("transform", "Biped_FkRightUpLeg_ctrl", self.ruplegnull_tn)
                    ctrl_ruplegpositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.ruplegupctrl_tn)

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

                    self.MDG2_mod.renameNode(ctrl_ruplegpositive_comb_cv, "FkRightUpLeg_shape")
                    self.MDG2_mod.commandToExecute('color -rgbColor 0 1 1 "Biped_FkRightUpLeg_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkRightUpLeg_ctrl"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_null.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_null.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_null.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_null.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_null.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_null.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_null.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_null.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_null.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_null.visibility"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_ctrl.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_ctrl.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_ctrl.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightUpLeg_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkRightUpLeg_ctrl.visibility"')
                    self.MDG2_mod.doIt()

                elif index == 1:
                    self.rlegnull_tn = self.MDag2_node.create("transform", "Biped_FkRightLeg_null", self.ruplegupctrl_tn)
                    self.rlegctrl_tn = self.MDag2_node.create("transform", "Biped_FkRightLeg_ctrl", self.rlegnull_tn)
                    ctrl_rlegpositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rlegctrl_tn)

                    self.pvrlegkneenull_tn = self.MDag2_node.create("transform", "Biped_PVRightKnee_null", self.masterctrl_tn)
                    self.pvrlegknectrl_tn = self.MDag2_node.create("transform", "Biped_PVRightKnee_ctrl", self.pvrlegkneenull_tn)
                    crv_ctrl_knee_triangle_l = self.MNurbs2_cv.createWithEditPoints(ctrl_elbow_triangle_points, 1, 1, False, True, True, self.pvrlegknectrl_tn)
                    crv_ctrl_knee_arrow_l = self.MNurbs2_cv.createWithEditPoints(ctrl_elbow_arrow_points, 1, 1, False, True, True, self.pvrlegknectrl_tn)

                    rlegnull_transform = om2.MFnTransform(self.rlegnull_tn)
                    rlegnull_transform.setRotatePivotTranslation(jnt_rleg_t, om2.MSpace.kTransform)

                    pvrlegkneenull_transform = om2.MFnTransform(self.pvrlegkneenull_tn)
                    pvrlegkneenull_transform.setTranslation(jnt_rleg_t, om2.MSpace.kTransform)

                    jnt_rleg_r = cmds.xform("RightLeg", query=True, rotation=True, worldSpace=True)

                    radian_rlegnull_x = (jnt_rleg_r[0]/180)*3.1415
                    radian_rlegnull_y = (jnt_rleg_r[1]/180)*3.1415
                    radian_rlegnull_z = (jnt_rleg_r[2]/180)*3.1415

                    rlegnull_transform_r = rlegnull_transform.rotation(om2.MSpace.kTransform)
                    rlegnull_transform_r[0], rlegnull_transform_r[1], rlegnull_transform_r[2] = radian_rlegnull_x, radian_rlegnull_y, radian_rlegnull_z
                    rlegnull_transform.setRotation(rlegnull_transform_r, om2.MSpace.kTransform)

                    rlegctrl_transform = om2.MFnTransform(self.rlegctrl_tn)

                    pvrlegknectrl_transform = om2.MFnTransform(self.pvrlegknectrl_tn)

                    rlegctrl_transform_r = rlegnull_transform.rotation(om2.MSpace.kTransform)
                    rlegctrl_transform_r[0], rlegctrl_transform_r[1], rlegctrl_transform_r[2] = 0, 1.57079, 0
                    rlegctrl_transform.setRotation(rlegctrl_transform_r, om2.MSpace.kTransform)

                    pvrlegkneenull_transform_t = pvrlegkneenull_transform.translation(om2.MSpace.kTransform)
                    pvrlegkneenull_transform_t[2] = pvrlegkneenull_transform_t[2]+8
                    pvrlegkneenull_transform.setTranslation(pvrlegkneenull_transform_t, om2.MSpace.kTransform)

                    pvrlegknectrl_transform_r = pvrlegknectrl_transform.rotation(om2.MSpace.kTransform)
                    pvrlegknectrl_transform_r[0] = 1.57079
                    pvrlegknectrl_transform.setRotation(pvrlegknectrl_transform_r, om2.MSpace.kTransform)

                    rlegctrl_transform_s = rlegctrl_transform.findPlug("scale", False)
                    if rlegctrl_transform_s.isCompound:
                        for i in range(rlegctrl_transform_s.numChildren()):
                            child_plug = rlegctrl_transform_s.child(i)
                            attr_value = child_plug.setDouble(box_transform_s[0]/2)

                    rlegnull_transform_trans = rlegnull_transform.transformation()
                    rlegnull_transform_worldmatrix = rlegnull_transform_trans.asMatrix()

                    rlegnull_transform_localmatrix = rlegnull_transform_worldmatrix * rootctrl_transform_worldmatrix * ruplegnull_transform_localmatrix.inverse()

                    rlegnull_transform.setTransformation(om2.MTransformationMatrix(rlegnull_transform_localmatrix))

                    self.MDG2_mod.renameNode(ctrl_rlegpositive_comb_cv, "FkRightLeg_shape")
                    self.MDG2_mod.commandToExecute('color -rgbColor 0 1 1 "Biped_FkRightLeg_ctrl"')
                    self.MDG2_mod.commandToExecute('color -rgbColor 1 1 0 "Biped_PVRightKnee_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkRightLeg_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_PVRightKnee_ctrl"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_null.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_null.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_null.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_null.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_null.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_null.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_null.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_null.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_null.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_null.visibility"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkRightLeg_ctrl.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkRightLeg_ctrl.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkRightLeg_ctrl.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightLeg_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkRightLeg_ctrl.visibility"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightKnee_null.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightKnee_null.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightKnee_null.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightKnee_null.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightKnee_null.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightKnee_null.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightKnee_null.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightKnee_null.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightKnee_null.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightKnee_null.visibility"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightKnee_ctrl.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightKnee_ctrl.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightKnee_ctrl.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightKnee_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightKnee_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_PVRightKnee_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_PVRightKnee_ctrl.visibility"')
                    self.MDG2_mod.doIt()

                elif index == 2:
                    self.rlegfootnull_tn = self.MDag2_node.create("transform", "Biped_FkRightFoot_null", self.rlegctrl_tn)
                    self.rlegfootctrl_tn = self.MDag2_node.create("transform", "Biped_FkRightFoot_ctrl", self.rlegfootnull_tn)
                    ctrl_rlegfootpositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rlegfootctrl_tn)

                    self.riklegfootnull_tn = self.MDag2_node.create("transform", "Biped_IkRightFoot_null", self.masterctrl_tn)
                    self.riklegfootoffsetnull_tn = self.MDag2_node.create("transform", "Biped_IkRightFootOffset_null", self.riklegfootnull_tn)
                    self.riklegfootrotnull_tn = self.MDag2_node.create("transform", "Biped_IkRightFootRot_null", self.riklegfootoffsetnull_tn)
                    self.riklegfootctrl_tn = self.MDag2_node.create("transform", "Biped_IkRightFoot_ctrl", self.riklegfootrotnull_tn)
                    ctrl_riklegfootpositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_hand_line_l, crv_ctrl_hand_line, crv_ctrl_hand_line_r], self.riklegfootctrl_tn)

                    self.rfootoption_tn = self.MDag2_node.create("transform", "Biped_RightFootOptions_ctrl", rleg_sl_ls.getDependNode(2))
                    ctrl_rfootoption_cv = self.MNurbs2_cv.createWithEditPoints(ctrl_lhandoption_line, 1, 1, False, True, True, self.rfootoption_tn)

                    self.nofliprlegkneenull_tn = self.MDag2_node.create("transform", "Biped_NoFlipRightKnee_null", self.riklegfootoffsetnull_tn)
                    self.nofliprlegkneectrl_tn = self.MDag2_node.create("transform", "Biped_NoFlipRightKnee_ctrl", self.nofliprlegkneenull_tn)
                    self.nofliprlegknectrl_tn = self.MDag2_node.create("locator", "NoFlipRightKnee_shape", self.nofliprlegkneectrl_tn)

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

                    nofliprlegkneenull_transform = om2.MFnTransform(self.nofliprlegkneectrl_tn)

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

                    nofliprlegkneenull_transform_t = nofliprlegkneenull_transform.translation(om2.MSpace.kTransform)
                    nofliprlegkneenull_transform_t[0] = 7
                    nofliprlegkneenull_transform.setTranslation(nofliprlegkneenull_transform_t, om2.MSpace.kTransform)

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

                    self.MDG2_mod.renameNode(ctrl_rlegfootpositive_comb_cv, "RightLegFoot_shape")
                    self.MDG2_mod.renameNode(ctrl_riklegfootpositive_comb_cv, "RightIkLegFoot_shape")
                    self.MDG2_mod.renameNode(ctrl_rfootoption_cv, "RightFootOptions_shape")
                    self.MDG2_mod.commandToExecute('color -rgbColor 0 1 1 "Biped_FkRightFoot_ctrl"')
                    self.MDG2_mod.commandToExecute('color -rgbColor 1 0 1 "Biped_IkRightFoot_ctrl"')
                    self.MDG2_mod.commandToExecute('color -rgbColor 1 1 0 "Biped_RightFootOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkRightFoot_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_IkRightFoot_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_RightFootOptions_ctrl"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_null.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_null.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_null.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_null.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_null.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_null.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_null.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_null.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_null.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_null.visibility"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkRightFoot_ctrl.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkRightFoot_ctrl.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkRightFoot_ctrl.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightFoot_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkRightFoot_ctrl.visibility"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_null.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_null.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_null.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_null.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_null.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_null.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_null.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_null.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_null.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_IkRightFoot_null.visibility"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFoot_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_IkRightFoot_ctrl.visibility"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFootOffset_null.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFootOffset_null.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFootOffset_null.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFootOffset_null.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFootOffset_null.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFootOffset_null.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFootOffset_null.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFootOffset_null.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFootOffset_null.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_IkRightFootOffset_null.visibility"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFootOptions_ctrl.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFootOptions_ctrl.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFootOptions_ctrl.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFootOptions_ctrl.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFootOptions_ctrl.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFootOptions_ctrl.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFootOptions_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFootOptions_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFootOptions_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_RightFootOptions_ctrl.visibility"')
                    self.MDG2_mod.doIt()

                    riklegfootctrl_path_n = om2.MDagPath()
                    riklegfootctrl_path = riklegfootctrl_path_n.getAPathTo(self.riklegfootctrl_tn)
                    riklegfootctrl_worldtransform = om2.MFnTransform(riklegfootctrl_path)

                    riklegfootctrl_worldtransform.setRotatePivot(om2.MPoint(jnt_rleg_t), om2.MSpace.kWorld, False)

                elif index == 3:
                    self.rlegtoebasenull_tn = self.MDag2_node.create("transform", "Biped_FkRightToeBase_null", self.rlegfootctrl_tn)
                    self.rlegtoebasectrl_tn = self.MDag2_node.create("transform", "Biped_FkRightToeBase_ctrl", self.rlegtoebasenull_tn)
                    ctrl_rlegtoepositive_comb_cv = self.MNurbs2_cv.create([crv_ctrl_neck_line_up, crv_ctrl_neck_star, crv_ctrl_neck_line_down], self.rlegtoebasectrl_tn)

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

                    self.MDG2_mod.renameNode(ctrl_rlegtoepositive_comb_cv, "FkRightLegToeBase_shape")
                    self.MDG2_mod.commandToExecute('color -rgbColor 0 1 1 "Biped_FkRightToeBase_ctrl"')
                    self.MDG2_mod.commandToExecute('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 "Biped_FkRightToeBase_ctrl"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_null.translateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_null.translateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_null.translateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_null.rotateX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_null.rotateY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_null.rotateZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_null.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_null.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_null.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_null.visibility"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_ctrl.scaleX"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_ctrl.scaleY"')
                    self.MDG2_mod.commandToExecute('setAttr -lock true -keyable false -channelBox false "Biped_FkRightToeBase_ctrl.scaleZ"')
                    self.MDG2_mod.commandToExecute('setAttr -lock false -keyable false -channelBox false "Biped_FkRightToeBase_ctrl.visibility"')
                    self.MDG2_mod.doIt()

        obj_root = om1.MObject()
        obj_endspine = om1.MObject()
        obj_masterctrl1 = om1.MObject()
        obj_stretchyspine = om1.MObject()

        masterctrl_sl_lst2 = om2.MSelectionList()
        masterctrl_sl_lst2.add("Biped_Master_ctrl")
        obj_masterctrl2 = masterctrl_sl_lst2.getDependNode(0)

        if self.autostretch.currentIndex() == 1:

            self.MDG2_mod.commandToExecute('addAttr -longName "stretchable" -niceName "Stretchable" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_StretchySpine_ctrl')
            self.MDG2_mod.doIt()

            stretchy_sl_lst1 = om1.MSelectionList()
            stretchy_sl_lst1.add("Biped_StretchySpine_ctrl")
            stretchy_sl_lst1.getDependNode(0, obj_stretchyspine)

            if cmds.objExists("IkHip") and cmds.objExists("IkCvHip") and cmds.objExists("IkCvSpine"):
                ikspineiksolver_lst = om1.MSelectionList()
                ikspinedag_n = om1.MFnDagNode()
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

                self.ikspline_effector = self.IK_Effector.create(obj_endspine)
                ikspine_effector_path = spine_pathnode.getAPathTo(self.ikspline_effector)

                self.spine_ik = self.IK_Handle.create(rootspine_path, ikspine_effector_path)

                obj_array = om1.MPointArray()
                obj_lst_mpoint = []
                obj = om1.MObject()
                for index in range(ikspine_sl_lst.length()):
                    ikspine_sl_lst.getDependNode(index, obj)
                    obj_path = self.MDag_path.getAPathTo(obj)
                    obj_tn = om1.MFnTransform(obj_path)
                    obj_t = obj_tn.translation(om1.MSpace.kWorld)
                    obj_lst_mpoint.append(om1.MPoint(obj_t))
                    obj_array.append(obj_lst_mpoint[index])

                self.ikspline_cv_tn = ikspinedag_n.create("transform", "BackBone_SplineCv")
                ikspline_cv = self.MNurbs1_cv.createWithEditPoints(obj_array, 1, 1, False, True, True, self.ikspline_cv_tn)
                cmds.parent("BackBone_SplineCv", "DoNotTouch")

                spinecrv_info = ikspinedg_modifier.createNode("curveInfo")
                spinestretchpercent = ikspinedg_modifier.createNode("multiplyDivide")
                spinestretchpow = ikspinedg_modifier.createNode("multiplyDivide")
                spinestretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                spinescalediv = ikspinedg_modifier.createNode("multiplyDivide")
                blendstretch = ikspinedg_modifier.createNode("blendColors")

                spinecrvinfo_fs = om1.MFnDependencyNode(spinecrv_info)
                spinestretchpercent_fs = om1.MFnDependencyNode(spinestretchpercent)
                spinestretchpow_fs = om1.MFnDependencyNode(spinestretchpow)
                spinestretchdiv_fs = om1.MFnDependencyNode(spinestretchdiv)
                spinescalediv_fs = om1.MFnDependencyNode(spinescalediv)
                blendstretch_fs = om1.MFnDependencyNode(blendstretch)
                masterctrl_fs = om1.MFnDependencyNode(obj_masterctrl1)
                backbonestretchctrl_fs = om1.MFnDependencyNode(obj_stretchyspine)

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
                blendstretchinp1r_plug = blendstretch_fs.findPlug("color1R")
                blendstretchinp1g_plug = blendstretch_fs.findPlug("color1G")
                blendstretchinp1b_plug = blendstretch_fs.findPlug("color1B")
                blendstretchotpr_plug = blendstretch_fs.findPlug("outputR")
                blendstretchotpg_plug = blendstretch_fs.findPlug("outputG")
                blendstretchotpb_plug = blendstretch_fs.findPlug("outputB")
                blendstretch_plug = blendstretch_fs.findPlug("blender")
                masterctrlsy_plug = masterctrl_fs.findPlug("scaleY")
                backbonestretchctrl_plug = backbonestretchctrl_fs.findPlug("stretchable")

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
                        ikspinedg_modifier.connect(spinestretchpercentotp_plug, blendstretchinp1g_plug)
                        ikspinedg_modifier.connect(spinestretchdivotox_plug, blendstretchinp1r_plug)
                        ikspinedg_modifier.connect(spinestretchdivotpz_plug, blendstretchinp1b_plug)
                        ikspinedg_modifier.connect(blendstretchotpg_plug, spinejnt_syplug)
                        ikspinedg_modifier.connect(blendstretchotpr_plug, spinejnt_sxplug)
                        ikspinedg_modifier.connect(blendstretchotpb_plug, spinejnt_szplug)
                        ikspinedg_modifier.connect(spinejnt_sotpplug, spinejnt_invsplug)

                ikspinedg_modifier.renameNode(spinecrv_info, "BackBoneSpline_Info")
                ikspinedg_modifier.renameNode(spinestretchpercent, "BackBoneStretch_Percent")
                ikspinedg_modifier.renameNode(spinestretchpow, "BackBoneStretch_Power")
                ikspinedg_modifier.renameNode(spinestretchdiv, "BackBoneStretch_Divide")
                ikspinedg_modifier.renameNode(ikspline_cv, "BackBone_SplineCvShape")
                ikspinedg_modifier.renameNode(self.spine_ik, "BackBone_Ik")
                ikspinedg_modifier.renameNode(self.ikspline_effector, "BackBone_effector")
                ikspinedg_modifier.renameNode(spinescalediv, "IkSpineGlobalScale_Average")
                ikspinedg_modifier.renameNode(blendstretch, "BackBoneStretch_Blend")
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
                ikspinedg_modifier.connect(backbonestretchctrl_plug, blendstretch_plug)
                ikspinedg_modifier.commandToExecute('float $backbonestretchinput1Y = `getAttr "BackBoneStretch_Percent.input1Y"`; setAttr "BackBoneStretch_Percent.input2Y" $backbonestretchinput1Y')
                ikspinedg_modifier.commandToExecute('setAttr "BackBoneStretch_Power.input2X" 0.5')
                ikspinedg_modifier.commandToExecute('setAttr "BackBoneStretch_Power.input2Z" 0.5')
                ikspinedg_modifier.commandToExecute('setAttr "BackBoneStretch_Divide.input1X" 1')
                ikspinedg_modifier.commandToExecute('setAttr "BackBoneStretch_Divide.input1Z" 1')
                ikspinedg_modifier.commandToExecute('setAttr "BackBoneStretch_Percent.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "BackBoneStretch_Power.operation" 3')
                ikspinedg_modifier.commandToExecute('setAttr "BackBoneStretch_Divide.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "IkSpineGlobalScale_Average.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "BackBoneStretch_Blend.color2R" 1')
                ikspinedg_modifier.commandToExecute('setAttr "BackBoneStretch_Blend.color2G" 1')
                ikspinedg_modifier.commandToExecute('setAttr "BackBoneStretch_Blend.color2B" 1')
                ikspinedg_modifier.doIt()

                ikspline_solver = self.IK_System.findSolver("ikSplineSolver")
                self.IK_Handle.setSolver(ikspline_solver)

        iksplinegrp_sl_ls = om2.MSelectionList()
        iksplinegrp_sl_ls.add("SplineIk_grp")

        masterscale_multMatrix = self.MDG2_mod.createNode("multMatrix")
        masterscale_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
        self.MDG2_mod.renameNode(masterscale_multMatrix, "MasterScale_multMatrix")
        self.MDG2_mod.renameNode(masterscale_decomposeMatrix, "MasterScale_decomposeMatrix")

        masterscalemultMatrix_fs = om2.MFnDependencyNode(masterscale_multMatrix)
        masterscaledecomposeMatrix_fs = om2.MFnDependencyNode(masterscale_decomposeMatrix)
        splineik_fs = om2.MFnDependencyNode(iksplinegrp_sl_ls.getDependNode(0))

        mastermultMatrixSum_plug = masterscalemultMatrix_fs.findPlug("matrixSum", False)
        masterdecomposeInpMatrix_plug = masterscaledecomposeMatrix_fs.findPlug("inputMatrix", False)
        masterdecomposeOtpScale_plug = masterscaledecomposeMatrix_fs.findPlug("outputScale", False)
        splineikScale_plug = splineik_fs.findPlug("scale", False)

        self.MDG2_mod.commandToExecute('connectAttr - force Biped_Master_ctrl.worldMatrix[0] MasterScale_multMatrix.matrixIn[0]')
        self.MDG2_mod.connect(mastermultMatrixSum_plug, masterdecomposeInpMatrix_plug)
        self.MDG2_mod.connect(masterdecomposeOtpScale_plug, splineikScale_plug)

        rootctrl_multMatrix = self.MDG2_mod.createNode("multMatrix")
        rootctrl_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
        self.MDG2_mod.renameNode(rootctrl_multMatrix, "Root_multMatrix")
        self.MDG2_mod.renameNode(rootctrl_decomposeMatrix, "Root_decomposeMatrix")

        rootmultMatrix_fs = om2.MFnDependencyNode(rootctrl_multMatrix)
        rootdecomposeMatrix_fs = om2.MFnDependencyNode(rootctrl_decomposeMatrix)
        hipjnt_fs = om2.MFnDependencyNode(root_obj)

        mastermultMatrixSum_plug = rootmultMatrix_fs.findPlug("matrixSum", False)
        masterdecomposeInpMatrix_plug = rootdecomposeMatrix_fs.findPlug("inputMatrix", False)
        rootdecomposeOtpTrans_plug = rootdecomposeMatrix_fs.findPlug("outputTranslate", False)
        rootdecomposeOtpRot_plug = rootdecomposeMatrix_fs.findPlug("outputRotate", False)
        hipjntTrans_plug = hipjnt_fs.findPlug("translate", False)
        hipjntRot_plug = hipjnt_fs.findPlug("rotate", False)

        self.MDG2_mod.commandToExecute('connectAttr - force Biped_Root_ctrl.worldMatrix[0] Root_multMatrix.matrixIn[0]')
        self.MDG2_mod.commandToExecute('connectAttr -force Root.parentInverseMatrix[0] Root_multMatrix.matrixIn[1]')
        self.MDG2_mod.connect(mastermultMatrixSum_plug, masterdecomposeInpMatrix_plug)
        self.MDG2_mod.connect(rootdecomposeOtpTrans_plug, hipjntTrans_plug)
        self.MDG2_mod.connect(rootdecomposeOtpRot_plug, hipjntRot_plug)

        if self.autostretch.currentIndex() == 1:
            if cmds.objExists("IkHip") and cmds.objExists("IkCvHip") and cmds.objExists("IkCvSpine"):
                ikcvspinespline_sl_lst = om2.MSelectionList()
                ikcvspinespline_sl_lst.add("IkCvHip")
                ikcvspinespline_sl_lst.add("IkCvSpine")

                if self.hipjnt.currentIndex() == 1:
                    ikcvspinespline_sl_lst.add("Hip")

                    hipctrl_multMatrix = self.MDG2_mod.createNode("multMatrix")
                    hipctrl_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                    self.MDG2_mod.renameNode(hipctrl_multMatrix, "Hiprot_multMatrix")
                    self.MDG2_mod.renameNode(hipctrl_decomposeMatrix, "Hiprot_decomposeMatrix")

                    hipmultMatrix_fs = om2.MFnDependencyNode(hipctrl_multMatrix)
                    hipdecomposeMatrix_fs = om2.MFnDependencyNode(hipctrl_decomposeMatrix)
                    ikhiprotjnt_fs = om2.MFnDependencyNode(ikcvspinespline_sl_lst.getDependNode(0))
                    hiprotjnt_fs = om2.MFnDependencyNode(ikcvspinespline_sl_lst.getDependNode(2))

                    hipmultMatrixSum_plug = hipmultMatrix_fs.findPlug("matrixSum", False)
                    hipdecomposeInpMatrix_plug = hipdecomposeMatrix_fs.findPlug("inputMatrix", False)
                    hipdecomposeOtpTrans_plug = hipdecomposeMatrix_fs.findPlug("outputTranslate", False)
                    hipdecomposeOtpRot_plug = hipdecomposeMatrix_fs.findPlug("outputRotate", False)
                    ikhiprotjntTrans_plug = ikhiprotjnt_fs.findPlug("translate", False)
                    ikhiprotjntRot_plug = ikhiprotjnt_fs.findPlug("rotate", False)
                    hiprotjntRot_plug = hiprotjnt_fs.findPlug("rotate", False)

                    self.MDG2_mod.commandToExecute('connectAttr - force Biped_Hip_ctrl.worldMatrix[0] Hiprot_multMatrix.matrixIn[0]')
                    self.MDG2_mod.commandToExecute('connectAttr -force IkCvHip.parentInverseMatrix[0] Hiprot_multMatrix.matrixIn[1]')
                    self.MDG2_mod.connect(hipmultMatrixSum_plug, hipdecomposeInpMatrix_plug)
                    self.MDG2_mod.connect(hipdecomposeOtpTrans_plug, ikhiprotjntTrans_plug)
                    self.MDG2_mod.connect(hipdecomposeOtpRot_plug, ikhiprotjntRot_plug)
                    self.MDG2_mod.connect(ikhiprotjntRot_plug, hiprotjntRot_plug)


        elif cmds.objExists("IkCvHip"):
            self.MDG2_mod.commandToExecute('delete "IkCvHip"')
            self.MDG2_mod.commandToExecute('delete "IkHip"')

            if self.hipjnt.currentIndex() == 1: 
                hipjnt_fs = om2.MFnDependencyNode(jnt_hip)
                hipctrlRot_fs = om2.MFnDependencyNode(self.hipctrl_tn)

                hipjntRot_plug = hipjnt_fs.findPlug("rotate", False)
                hipctrlRot_plug = hipctrlRot_fs.findPlug("rotate", False)

                self.MDG2_mod.connect(hipctrlRot_plug, hipjntRot_plug)

        for index in range(spine_sl_lst.length()):
            spinectrl_multMatrix = self.MDG2_mod.createNode("multMatrix")
            spinectrl_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
            self.MDG2_mod.renameNode(spinectrl_multMatrix, "Spine{0}_multMatrix".format(index))
            self.MDG2_mod.renameNode(spinectrl_decomposeMatrix, "Spine{0}_decomposeMatrix".format(index))

            spinemultMatrix_fs = om2.MFnDependencyNode(spinectrl_multMatrix)
            spinedecomposeMatrix_fs = om2.MFnDependencyNode(spinectrl_decomposeMatrix)
            spinejnt_fs = om2.MFnDependencyNode(spine_sl_lst.getDependNode(index))

            spinemultMatrixSum_plug = spinemultMatrix_fs.findPlug("matrixSum", False)
            spinedecomposeInpMatrix_plug = spinedecomposeMatrix_fs.findPlug("inputMatrix", False)
            spinedecomposeOtpTrans_plug = spinedecomposeMatrix_fs.findPlug("outputTranslate", False)
            spinedecomposeOtpRot_plug = spinedecomposeMatrix_fs.findPlug("outputRotate", False)
            spinejntTrans_plug = spinejnt_fs.findPlug("translate", False)
            spinejntRot_plug = spinejnt_fs.findPlug("rotate", False)

            self.MDG2_mod.commandToExecute('connectAttr -force Biped_Spine{0}_ctrl.worldMatrix[0] Spine{0}_multMatrix.matrixIn[0]'.format(index))
            self.MDG2_mod.commandToExecute('connectAttr -force Spine{0}.parentInverseMatrix[0] Spine{0}_multMatrix.matrixIn[1]'.format(index))
            self.MDG2_mod.connect(spinemultMatrixSum_plug, spinedecomposeInpMatrix_plug)
            self.MDG2_mod.connect(spinedecomposeOtpTrans_plug, spinejntTrans_plug)
            self.MDG2_mod.connect(spinedecomposeOtpRot_plug, spinejntRot_plug)

            if index == 0:
                spinejntScale_plug = spinejnt_fs.findPlug("scale", False)
                self.MDG2_mod.connect(masterdecomposeOtpScale_plug, spinejntScale_plug)

            jnt_string = spine_sl_lst.getSelectionStrings(index)
            if cmds.getAttr("{0}.jointOrientX".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientY".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientZ".format(str(jnt_string)[3:][:-3])) != 0:
                self.MDG2_mod.commandToExecute('setAttr "{0}.jointOrientX" 0'.format(str(jnt_string)[3:][:-3]))
                self.MDG2_mod.commandToExecute('setAttr "{0}.jointOrientY" 0'.format(str(jnt_string)[3:][:-3]))
                self.MDG2_mod.commandToExecute('setAttr "{0}.jointOrientZ" 0'.format(str(jnt_string)[3:][:-3]))

        if self.autostretch.currentIndex() == 1:
            if cmds.objExists("IkHip") and cmds.objExists("IkCvHip") and cmds.objExists("IkCvSpine"):

                if cmds.getAttr("IkCvSpine.jointOrientX") != 0 or cmds.getAttr("IkCvSpine.jointOrientX") != 0 or cmds.getAttr("IkCvSpine.jointOrientX") != 0:
                    self.MDG2_mod.commandToExecute('setAttr "IkCvSpine.jointOrientX" 0')
                    self.MDG2_mod.commandToExecute('setAttr "IkCvSpine.jointOrientY" 0')
                    self.MDG2_mod.commandToExecute('setAttr "IkCvSpine.jointOrientZ" 0')

                ikspinectrl_multMatrix = self.MDG2_mod.createNode("multMatrix")
                ikspinectrl_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                self.MDG2_mod.renameNode(ikspinectrl_multMatrix, "IkSpine_multMatrix")
                self.MDG2_mod.renameNode(ikspinectrl_decomposeMatrix, "IkSpine_decomposeMatrix")

                spinesplinemultMatrix_fs = om2.MFnDependencyNode(ikspinectrl_multMatrix)
                spinesplinedecomposeMatrix_fs = om2.MFnDependencyNode(ikspinectrl_decomposeMatrix)
                spinesplinejnt_fs = om2.MFnDependencyNode(ikcvspinespline_sl_lst.getDependNode(1))

                spinesplinemultMatrixSum_plug = spinesplinemultMatrix_fs.findPlug("matrixSum", False)
                spinesplinedecomposeInpMatrix_plug = spinesplinedecomposeMatrix_fs.findPlug("inputMatrix", False)
                spinesplinedecomposeOtpTrans_plug = spinesplinedecomposeMatrix_fs.findPlug("outputTranslate", False)
                spinesplinedecomposeOtpRot_plug = spinesplinedecomposeMatrix_fs.findPlug("outputRotate", False)
                spinesplinejntTrans_plug = spinesplinejnt_fs.findPlug("translate", False)
                spinesplinejntRot_plug = spinesplinejnt_fs.findPlug("rotate", False)

                self.MDG2_mod.commandToExecute('connectAttr -force Biped_StretchySpine_ctrl.worldMatrix[0] IkSpine_multMatrix.matrixIn[0]')
                self.MDG2_mod.commandToExecute('connectAttr -force IkCvSpine.parentInverseMatrix[0] IkSpine_multMatrix.matrixIn[1]')
                self.MDG2_mod.connect(spinesplinemultMatrixSum_plug, spinesplinedecomposeInpMatrix_plug)
                self.MDG2_mod.connect(spinesplinedecomposeOtpTrans_plug, spinesplinejntTrans_plug)
                self.MDG2_mod.connect(spinesplinedecomposeOtpRot_plug, spinesplinejntRot_plug)

        elif cmds.objExists("IkCvSpine"):
            self.MDG2_mod.commandToExecute('delete "IkCvSpine"')
            self.MDG2_mod.commandToExecute('delete "Biped_StretchySpine_ctrl"')

        obj_stretchyneck = om1.MObject()

        if self.autostretch.currentIndex() == 1:

            self.MDG2_mod.commandToExecute('addAttr -longName "stretchable" -niceName "Stretchable" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_StretchyNeck_ctrl')
            self.MDG2_mod.doIt()

            stretchy_sl_lst1.add("Biped_StretchyNeck_ctrl")
            stretchy_sl_lst1.getDependNode(1, obj_stretchyneck)

            if cmds.objExists("IkNeck*") and cmds.objExists("IkCvNeck") and cmds.objExists("IkCvHead"):
                ikneckspline_sl_lst = om1.MSelectionList()
                ikneckspline_sl_lst.add("IkNeck*")
                ikneckspline_sl_lst.getDependNode(0, obj_root)
                ikneckspline_sl_lst.getDependNode(ikneckspline_sl_lst.length()-1, obj_endspine)

                neck_pathnode = om1.MDagPath()
                neck_path = neck_pathnode.getAPathTo(obj_root)

                self.ikneckspline_effector = self.IK_Effector.create(obj_endspine)
                ikneckspine_effector_path = neck_pathnode.getAPathTo(self.ikneckspline_effector)

                self.neckspine_ik = self.IK_Handle.create(neck_path, ikneckspine_effector_path)

                neckobj_array = om1.MPointArray()
                neckobj_lst_mpoint = []
                neckobj = om1.MObject()
                for index in range(ikneckspline_sl_lst.length()):
                    ikneckspline_sl_lst.getDependNode(index, neckobj)
                    obj_path = self.MDag_path.getAPathTo(neckobj)
                    obj_tn = om1.MFnTransform(obj_path)
                    obj_t = obj_tn.translation(om1.MSpace.kWorld)
                    neckobj_lst_mpoint.append(om1.MPoint(obj_t))
                    neckobj_array.append(neckobj_lst_mpoint[index])

                self.ikneckspline_cv_tn = ikspinedag_n.create("transform", "Neck_SplineCv")
                ikneckspline_cv = self.MNurbs1_cv.createWithEditPoints(neckobj_array, 1, 1, False, True, True, self.ikneckspline_cv_tn)
                cmds.parent("Neck_SplineCv", "DoNotTouch")

                neckcrv_info = ikspinedg_modifier.createNode("curveInfo")
                neckstretchpercent = ikspinedg_modifier.createNode("multiplyDivide")
                neckstretchpow = ikspinedg_modifier.createNode("multiplyDivide")
                neckstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                neckscalediv = ikspinedg_modifier.createNode("multiplyDivide")
                blendstretch = ikspinedg_modifier.createNode("blendColors")

                neckcrvinfo_fs = om1.MFnDependencyNode(neckcrv_info)
                neckstretchpercent_fs = om1.MFnDependencyNode(neckstretchpercent)
                neckstretchpow_fs = om1.MFnDependencyNode(neckstretchpow)
                neckstretchdiv_fs = om1.MFnDependencyNode(neckstretchdiv)
                neckscale_fs = om1.MFnDependencyNode(neckscalediv)
                blendstretch_fs = om1.MFnDependencyNode(blendstretch)
                neckstretchctrl_fs = om1.MFnDependencyNode(obj_stretchyneck)

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
                blendstretchinp1r_plug = blendstretch_fs.findPlug("color1R")
                blendstretchinp1g_plug = blendstretch_fs.findPlug("color1G")
                blendstretchinp1b_plug = blendstretch_fs.findPlug("color1B")
                blendstretchotpr_plug = blendstretch_fs.findPlug("outputR")
                blendstretchotpg_plug = blendstretch_fs.findPlug("outputG")
                blendstretchotpb_plug = blendstretch_fs.findPlug("outputB")
                blendstretch_plug = blendstretch_fs.findPlug("blender")
                neckstretchctrl_plug = neckstretchctrl_fs.findPlug("stretchable")

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
                        ikspinedg_modifier.connect(neckstretchpercentotp_plug, blendstretchinp1g_plug)
                        ikspinedg_modifier.connect(neckstretchdivotox_plug, blendstretchinp1r_plug)
                        ikspinedg_modifier.connect(neckstretchdivotpz_plug, blendstretchinp1b_plug)
                        ikspinedg_modifier.connect(blendstretchotpg_plug, neckjnt_syplug)
                        ikspinedg_modifier.connect(blendstretchotpr_plug, neckjnt_sxplug)
                        ikspinedg_modifier.connect(blendstretchotpb_plug, neckjnt_szplug)
                        ikspinedg_modifier.connect(neckjnt_sotpplug, neckjnt_invsplug)

                ikspinedg_modifier.renameNode(neckcrv_info, "NeckSpline_Info")
                ikspinedg_modifier.renameNode(neckstretchpercent, "NeckStretch_Percent")
                ikspinedg_modifier.renameNode(neckstretchpow, "NeckStretch_Power")
                ikspinedg_modifier.renameNode(neckstretchdiv, "NeckStretch_Divide")
                ikspinedg_modifier.renameNode(ikneckspline_cv, "Neck_SplineCvShape")
                ikspinedg_modifier.renameNode(self.neckspine_ik, "Neck_Ik")
                ikspinedg_modifier.renameNode(self.ikneckspline_effector, "Neck_effector")
                ikspinedg_modifier.renameNode(neckscalediv, "IkNeckGlobalScale_Average")
                ikspinedg_modifier.renameNode(blendstretch, "NeckStretch_Blend")
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
                ikspinedg_modifier.connect(neckstretchctrl_plug, blendstretch_plug)
                ikspinedg_modifier.commandToExecute('float $neckstretchinput1Y = `getAttr "NeckStretch_Percent.input1Y"`; setAttr "NeckStretch_Percent.input2Y" $neckstretchinput1Y')
                ikspinedg_modifier.commandToExecute('setAttr "NeckStretch_Power.input2X" 0.5')
                ikspinedg_modifier.commandToExecute('setAttr "NeckStretch_Power.input2Z" 0.5')
                ikspinedg_modifier.commandToExecute('setAttr "NeckStretch_Divide.input1X" 1')
                ikspinedg_modifier.commandToExecute('setAttr "NeckStretch_Divide.input1Z" 1')
                ikspinedg_modifier.commandToExecute('setAttr "NeckStretch_Percent.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "NeckStretch_Power.operation" 3')
                ikspinedg_modifier.commandToExecute('setAttr "NeckStretch_Divide.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "IkNeckGlobalScale_Average.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "NeckStretch_Blend.color2R" 1')
                ikspinedg_modifier.commandToExecute('setAttr "NeckStretch_Blend.color2G" 1')
                ikspinedg_modifier.commandToExecute('setAttr "NeckStretch_Blend.color2B" 1')
                ikspinedg_modifier.doIt()

                ikspline_solver = self.IK_System.findSolver("ikSplineSolver")
                self.IK_Handle.setSolver(ikspline_solver)

        neckctrl_multMatrix = self.MDG2_mod.createNode("multMatrix")
        neckctrl_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
        self.MDG2_mod.renameNode(neckctrl_multMatrix, "Neck_multMatrix")
        self.MDG2_mod.renameNode(neckctrl_decomposeMatrix, "Neck_decomposeMatrix")

        neckmultMatrix_fs = om2.MFnDependencyNode(neckctrl_multMatrix)
        neckdecomposeMatrix_fs = om2.MFnDependencyNode(neckctrl_decomposeMatrix)
        neckjnt_fs = om2.MFnDependencyNode(jnt_neck_obj)

        neckmultMatrixSum_plug = neckmultMatrix_fs.findPlug("matrixSum", False)
        neckdecomposeInpMatrix_plug = neckdecomposeMatrix_fs.findPlug("inputMatrix", False)
        neckdecomposeOtpTrans_plug = neckdecomposeMatrix_fs.findPlug("outputTranslate", False)
        neckdecomposeOtpRot_plug = neckdecomposeMatrix_fs.findPlug("outputRotate", False)
        neckjntTrans_plug = neckjnt_fs.findPlug("translate", False)
        neckjntRot_plug = neckjnt_fs.findPlug("rotate", False)

        self.MDG2_mod.commandToExecute('connectAttr -force Biped_Neck_ctrl.worldMatrix[0] Neck_multMatrix.matrixIn[0]')
        self.MDG2_mod.commandToExecute('connectAttr -force Neck.parentInverseMatrix[0] Neck_multMatrix.matrixIn[1]')
        self.MDG2_mod.connect(neckmultMatrixSum_plug, neckdecomposeInpMatrix_plug)
        self.MDG2_mod.connect(neckdecomposeOtpTrans_plug, neckjntTrans_plug)
        self.MDG2_mod.connect(neckdecomposeOtpRot_plug, neckjntRot_plug)

        if self.autostretch.currentIndex() == 1:
            if cmds.objExists("IkNeck*") and cmds.objExists("IkCvNeck") and cmds.objExists("IkCvHead"):
                ikneckspline_sl_lst = om2.MSelectionList()
                ikneckspline_sl_lst.add("IkCvNeck")
                ikneckspline_sl_lst.add("IkCvHead")
                obj_first = ikneckspline_sl_lst.getDependNode(0)

                ikcvneck_multMatrix = self.MDG2_mod.createNode("multMatrix")
                ikcvneck_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                self.MDG2_mod.renameNode(ikcvneck_multMatrix, "IkCvNeck_multMatrix")
                self.MDG2_mod.renameNode(ikcvneck_decomposeMatrix, "IkCvNeck_decomposeMatrix")

                ikcvneckmultMatrix_fs = om2.MFnDependencyNode(ikcvneck_multMatrix)
                ikcvneckdecomposeMatrix_fs = om2.MFnDependencyNode(ikcvneck_decomposeMatrix)
                ikcvneckjnt_fs = om2.MFnDependencyNode(obj_first)

                ikcvneckmultMatrixSum_plug = ikcvneckmultMatrix_fs.findPlug("matrixSum", False)
                ikcvneckdecomposeInpMatrix_plug = ikcvneckdecomposeMatrix_fs.findPlug("inputMatrix", False)
                ikcvneckdecomposeOtpTrans_plug = ikcvneckdecomposeMatrix_fs.findPlug("outputTranslate", False)
                ikcvneckdecomposeOtpRot_plug = ikcvneckdecomposeMatrix_fs.findPlug("outputRotate", False)
                ikcvneckjntTrans_plug = ikcvneckjnt_fs.findPlug("translate", False)
                ikcvneckjntRot_plug = ikcvneckjnt_fs.findPlug("rotate", False)

                self.MDG2_mod.commandToExecute('connectAttr -force Neck.worldMatrix[0] IkCvNeck_multMatrix.matrixIn[0]')
                self.MDG2_mod.connect(ikcvneckmultMatrixSum_plug, ikcvneckdecomposeInpMatrix_plug)
                self.MDG2_mod.connect(ikcvneckdecomposeOtpTrans_plug, ikcvneckjntTrans_plug)
                self.MDG2_mod.connect(ikcvneckdecomposeOtpRot_plug, ikcvneckjntRot_plug)

                obj_lastspine = ikneckspline_sl_lst.getDependNode(1)

                ikcvhead_multMatrix = self.MDG2_mod.createNode("multMatrix")
                ikcvhead_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                self.MDG2_mod.renameNode(ikcvhead_multMatrix, "IkCvHead_multMatrix")
                self.MDG2_mod.renameNode(ikcvhead_decomposeMatrix, "IkCvHead_decomposeMatrix")

                ikcvheadmultMatrix_fs = om2.MFnDependencyNode(ikcvhead_multMatrix)
                ikcvheaddecomposeMatrix_fs = om2.MFnDependencyNode(ikcvhead_decomposeMatrix)
                ikcvheadjnt_fs = om2.MFnDependencyNode(obj_lastspine)

                ikcvheadmultMatrixSum_plug = ikcvheadmultMatrix_fs.findPlug("matrixSum", False)
                ikcvheaddecomposeInpMatrix_plug = ikcvheaddecomposeMatrix_fs.findPlug("inputMatrix", False)
                ikcvheaddecomposeOtpTrans_plug = ikcvheaddecomposeMatrix_fs.findPlug("outputTranslate", False)
                ikcvheaddecomposeOtpRot_plug = ikcvheaddecomposeMatrix_fs.findPlug("outputRotate", False)
                ikcvheadjntTrans_plug = ikcvheadjnt_fs.findPlug("translate", False)
                ikcvheadjntRot_plug = ikcvheadjnt_fs.findPlug("rotate", False)

                self.MDG2_mod.commandToExecute('connectAttr -force Biped_StretchyNeck_ctrl.worldMatrix[0] IkCvHead_multMatrix.matrixIn[0]')
                self.MDG2_mod.connect(ikcvheadmultMatrixSum_plug, ikcvheaddecomposeInpMatrix_plug)
                self.MDG2_mod.connect(ikcvheaddecomposeOtpTrans_plug, ikcvheadjntTrans_plug)
                self.MDG2_mod.connect(ikcvheaddecomposeOtpRot_plug, ikcvheadjntRot_plug)

        elif cmds.objExists("IkCvNeck") and cmds.objExists("IkCvHead"):
            self.MDG2_mod.commandToExecute('delete "IkCvNeck"')
            self.MDG2_mod.commandToExecute('delete "IkCvHead"')
            self.MDG2_mod.commandToExecute('delete "IkNeck0"')
            self.MDG2_mod.commandToExecute('delete "Biped_StretchyNeck_ctrl"')

        elif cmds.objExists("Biped_StretchyNeck_ctrl"):
            self.MDG2_mod.commandToExecute('delete "Biped_StretchyNeck_ctrl"')

        headctrl_multMatrix = self.MDG2_mod.createNode("multMatrix")
        headctrl_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
        self.MDG2_mod.renameNode(headctrl_multMatrix, "Head_multMatrix")
        self.MDG2_mod.renameNode(headctrl_decomposeMatrix, "Head_decomposeMatrix")

        headmultMatrix_fs = om2.MFnDependencyNode(headctrl_multMatrix)
        headdecomposeMatrix_fs = om2.MFnDependencyNode(headctrl_decomposeMatrix)
        headjnt_fs = om2.MFnDependencyNode(jnt_head_obj)

        headmultMatrixSum_plug = headmultMatrix_fs.findPlug("matrixSum", False)
        headdecomposeInpMatrix_plug = headdecomposeMatrix_fs.findPlug("inputMatrix", False)
        headdecomposeOtpTrans_plug = headdecomposeMatrix_fs.findPlug("outputTranslate", False)
        headdecomposeOtpRot_plug = headdecomposeMatrix_fs.findPlug("outputRotate", False)
        headjntTrans_plug = headjnt_fs.findPlug("translate", False)
        headjntRot_plug = headjnt_fs.findPlug("rotate", False)

        self.MDG2_mod.commandToExecute('connectAttr -force Biped_Head_ctrl.worldMatrix[0] Head_multMatrix.matrixIn[0]')
        self.MDG2_mod.commandToExecute('connectAttr -force Head.parentInverseMatrix[0] Head_multMatrix.matrixIn[1]')
        self.MDG2_mod.connect(headmultMatrixSum_plug, headdecomposeInpMatrix_plug)
        self.MDG2_mod.connect(headdecomposeOtpTrans_plug, headjntTrans_plug)
        self.MDG2_mod.connect(headdecomposeOtpRot_plug, headjntRot_plug)

        self.MDG2_mod.commandToExecute('addAttr -longName "world" -niceName "World" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_Head_ctrl')
        self.MDG2_mod.doIt()

        headrotate_multMatrix = self.MDG2_mod.createNode("multMatrix")
        headrotate_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
        headrotblendnode = self.MDG2_mod.createNode("blendColors")
        self.MDG2_mod.renameNode(headrotate_multMatrix, "HeadRotate_multMatrix")
        self.MDG2_mod.renameNode(headrotate_decomposeMatrix, "HeadRotate_decomposeMatrix")
        self.MDG2_mod.renameNode(headrotblendnode, "HeadRotate_blend")

        headrotatemultMatrix_fs = om2.MFnDependencyNode(headrotate_multMatrix)
        headrotatedecomposeMatrix_fs = om2.MFnDependencyNode(headrotate_decomposeMatrix)
        headrotblend_fs = om2.MFnDependencyNode(headrotblendnode)
        headrot_fs = om2.MFnDependencyNode(self.headrot_tn)
        headctrl_fs = om2.MFnDependencyNode(self.headctrl_tn)

        headrotatemultMatrixSum_plug = headrotatemultMatrix_fs.findPlug("matrixSum", False)
        headrotatedecomposeInpMatrix_plug = headrotatedecomposeMatrix_fs.findPlug("inputMatrix", False)
        headrotatedecomposeOtpRot_plug = headrotatedecomposeMatrix_fs.findPlug("outputRotate", False)
        headrotblendnodeblender_plug = headrotblend_fs.findPlug("blender", False)
        headrotblendnodeinp1_plug = headrotblend_fs.findPlug("color1", False)
        headrotblendnodeotp_plug = headrotblend_fs.findPlug("output", False)
        headRot_plug = headrot_fs.findPlug("rotate", False)
        headctrl_plug = headctrl_fs.findPlug("world", False)

        self.MDG2_mod.commandToExecute('connectAttr -force Biped_Head_null.worldInverseMatrix[0] HeadRotate_multMatrix.matrixIn[0]')
        self.MDG2_mod.commandToExecute('connectAttr -force Biped_Root_ctrl.worldMatrix[0] HeadRotate_multMatrix.matrixIn[1]')
        self.MDG2_mod.connect(headrotatemultMatrixSum_plug, headrotatedecomposeInpMatrix_plug)
        self.MDG2_mod.connect(headrotatedecomposeOtpRot_plug, headrotblendnodeinp1_plug)
        self.MDG2_mod.connect(headrotblendnodeotp_plug, headRot_plug)
        self.MDG2_mod.connect(headctrl_plug, headrotblendnodeblender_plug)
        self.MDG2_mod.commandToExecute('setAttr "HeadRotate_blend.color2R" 0')
        self.MDG2_mod.commandToExecute('setAttr "HeadRotate_blend.color2G" 0')
        self.MDG2_mod.commandToExecute('setAttr "HeadRotate_blend.color2B" 0')


        for index in range(fklarm_sl_ls.length()):
            jnt_obj = fklarm_sl_ls.getDependNode(index)
            jnt_string = fklarm_sl_ls.getSelectionStrings(index)

            if jnt_obj.hasFn(om2.MFn.kJoint):
                larmctrl_multMatrix = self.MDG2_mod.createNode("multMatrix")
                larmctrl_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                self.MDG2_mod.renameNode(larmctrl_multMatrix, str(jnt_string)[2:][:-3] + "_multMatrix")
                self.MDG2_mod.renameNode(larmctrl_decomposeMatrix, str(jnt_string)[2:][:-3] + "_decomposeMatrix")

                rarmmultMatrix_fs = om2.MFnDependencyNode(larmctrl_multMatrix)
                rarmdecomposeMatrix_fs = om2.MFnDependencyNode(larmctrl_decomposeMatrix)
                larmjnt_fs = om2.MFnDependencyNode(jnt_obj)

                rarmmultMatrixSum_plug = rarmmultMatrix_fs.findPlug("matrixSum", False)
                rarmdecomposeInpMatrix_plug = rarmdecomposeMatrix_fs.findPlug("inputMatrix", False)
                rarmdecomposeOtpTrans_plug = rarmdecomposeMatrix_fs.findPlug("outputTranslate", False)
                rarmdecomposeOtpRot_plug = rarmdecomposeMatrix_fs.findPlug("outputRotate", False)
                larmjntTrans_plug = larmjnt_fs.findPlug("translate", False)
                larmjntRot_plug = larmjnt_fs.findPlug("rotate", False)

                self.MDG2_mod.commandToExecute('connectAttr -force Biped_{0}_ctrl.worldMatrix[0] {0}_multMatrix.matrixIn[0]'.format(str(jnt_string)[3:][:-3]))
                self.MDG2_mod.commandToExecute('connectAttr -force {0}.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(jnt_string)[3:][:-3]))
                self.MDG2_mod.connect(rarmmultMatrixSum_plug, rarmdecomposeInpMatrix_plug)
                self.MDG2_mod.connect(rarmdecomposeOtpTrans_plug, larmjntTrans_plug)
                self.MDG2_mod.connect(rarmdecomposeOtpRot_plug, larmjntRot_plug)

                if cmds.getAttr("{0}.jointOrientX".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientY".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientZ".format(str(jnt_string)[3:][:-3])) != 0:
                    self.MDG2_mod.commandToExecute('setAttr "{0}.jointOrientX" 0'.format(str(jnt_string)[3:][:-3]))
                    self.MDG2_mod.commandToExecute('setAttr "{0}.jointOrientY" 0'.format(str(jnt_string)[3:][:-3]))
                    self.MDG2_mod.commandToExecute('setAttr "{0}.jointOrientZ" 0'.format(str(jnt_string)[3:][:-3]))

        fklarm_sl_ls = om2.MSelectionList()
        fklarm_sl_ls.add("FkLeftArm")
        fklarm_sl_ls.add("FkLeftForeArm")
        fklarm_sl_ls.add("FkLeftHand")

        iklarm_sl_ls = om2.MSelectionList()
        iklarm_sl_ls.add("IkLeftArm")
        iklarm_sl_ls.add("IkLeftForeArm")
        iklarm_sl_ls.add("IkLeftHand")

        noflipiklarm_sl_ls = om2.MSelectionList()
        noflipiklarm_sl_ls.add("IkNoFlipLeftArm")
        noflipiklarm_sl_ls.add("IkNoFlipLeftForeArm")
        noflipiklarm_sl_ls.add("IkNoFlipLeftHand")

        pviklarm_sl_ls = om2.MSelectionList()
        pviklarm_sl_ls.add("IkPVLeftArm")
        pviklarm_sl_ls.add("IkPVLeftForeArm")
        pviklarm_sl_ls.add("IkPVLeftHand")

        lhandoptions_sl_ls = om2.MSelectionList()
        lhandoptions_sl_ls.add("Biped_LeftHandOptions_ctrl")
        lhandoptions_obj = lhandoptions_sl_ls.getDependNode(0)

        self.MDG2_mod.commandToExecute('addAttr -longName "stretchy" -niceName "Stretchy" -attributeType double -keyable true -defaultValue 0 Biped_FkLeftArm_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "stretchy" -niceName "Stretchy" -attributeType double -keyable true -defaultValue 0 Biped_FkLeftForeArm_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "fkik" -niceName "Fk/Ik" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_LeftHandOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "kneeswitch" -niceName "Auto/Manual Knee" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_LeftHandOptions_ctrl')
        self.MDG2_mod.doIt()

        lhandoptions_fs = om2.MFnDependencyNode(lhandoptions_obj)
        lhandoptionsfkik_plug = lhandoptions_fs.findPlug("fkik", False)
        lhandoptionskneeswitch_plug = lhandoptions_fs.findPlug("kneeswitch", False)

        for index in range(larm_sl_ls.length()):
            fkjnt_obj = fklarm_sl_ls.getDependNode(index)

            ikjnt_obj = iklarm_sl_ls.getDependNode(index)
            ikjnt_string = iklarm_sl_ls.getSelectionStrings(index)

            bindjnt_obj = larm_sl_ls.getDependNode(index)
            bindjnt_string = larm_sl_ls.getSelectionStrings(index)

            noflipjnt_obj = noflipiklarm_sl_ls.getDependNode(index)
            noflipjnt_string = noflipiklarm_sl_ls.getSelectionStrings(index)

            pvjnt_obj = pviklarm_sl_ls.getDependNode(index)
            pvjnt_string = pviklarm_sl_ls.getSelectionStrings(index)

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

                armjointtransinp_plug = armjoint_fs.findPlug("translate", False)
                armjointrotinp_plug = armjoint_fs.findPlug("rotate", False)
                fkarmjointtransotp_plug = fkarmjoint_fs.findPlug("translate", False)
                fkarmjointrototp_plug = fkarmjoint_fs.findPlug("rotate", False)

                if cmds.objExists("NoFlipLeftHand_Ik") and cmds.objExists("PVLeftHand_Ik"):
                    armrotblendnode = self.MDG2_mod.createNode("blendColors")
                    armtransblendnode = self.MDG2_mod.createNode("blendColors")
                    armjoint_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                    self.MDG2_mod.renameNode(armjoint_decomposeMatrix, str(bindjnt_string)[2:][:-3] + "Blend_decomposeMatrix")
                    self.MDG2_mod.renameNode(armrotblendnode, str(bindjnt_string)[2:][:-3] + "_blend")
                    self.MDG2_mod.renameNode(armtransblendnode, str(bindjnt_string)[2:][:-3]+"Trans_blend")

                    armrotblendnode_fs = om2.MFnDependencyNode(armrotblendnode)
                    armtransblendnode_fs = om2.MFnDependencyNode(armtransblendnode)
                    armdecomposeMatrix_fs = om2.MFnDependencyNode(armjoint_decomposeMatrix)
                    ikarmjoint_fs = om2.MFnDependencyNode(ikjnt_obj)

                    armdecomposeInpMatrix_plug = armdecomposeMatrix_fs.findPlug("inputMatrix", False)
                    armdecomposeOtpRot_plug = armdecomposeMatrix_fs.findPlug("outputRotate", False)
                    armdecomposeOtpTrans_plug = armdecomposeMatrix_fs.findPlug("outputTranslate", False)
                    armrotblendnodeinp1_plug = armrotblendnode_fs.findPlug("color1", False)
                    armrotblendnodeinp2_plug = armrotblendnode_fs.findPlug("color2", False)
                    armrotblendnodeotp_plug = armrotblendnode_fs.findPlug("output", False)
                    armrotblendnodeblender_plug = armrotblendnode_fs.findPlug("blender", False)
                    armtransblendnodeinp1_plug = armtransblendnode_fs.findPlug("color1", False)
                    armtransblendnodeinp2_plug = armtransblendnode_fs.findPlug("color2", False)
                    armtransblendnodeotp_plug = armtransblendnode_fs.findPlug("output", False)
                    armtransblendnodeblender_plug = armtransblendnode_fs.findPlug("blender", False)
                    ikarmjointrototp_plug = ikarmjoint_fs.findPlug("matrix", False)

                    self.MDG2_mod.connect(ikarmjointrototp_plug, armdecomposeInpMatrix_plug)
                    self.MDG2_mod.connect(armdecomposeOtpRot_plug, armrotblendnodeinp1_plug)
                    self.MDG2_mod.connect(armdecomposeOtpTrans_plug, armtransblendnodeinp1_plug)
                    self.MDG2_mod.connect(fkarmjointrototp_plug, armrotblendnodeinp2_plug)
                    self.MDG2_mod.connect(fkarmjointtransotp_plug, armtransblendnodeinp2_plug)
                    self.MDG2_mod.connect(armrotblendnodeotp_plug, armjointrotinp_plug)
                    self.MDG2_mod.connect(armtransblendnodeotp_plug, armjointtransinp_plug)
                    self.MDG2_mod.connect(lhandoptionsfkik_plug, armrotblendnodeblender_plug)
                    self.MDG2_mod.connect(lhandoptionsfkik_plug, armtransblendnodeblender_plug)

                    armrotblendnode = self.MDG2_mod.createNode("blendColors")
                    armtransblendnode = self.MDG2_mod.createNode("blendColors")
                    nofliparmjoint_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                    pvarmjoint_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                    self.MDG2_mod.renameNode(nofliparmjoint_decomposeMatrix, str(noflipjnt_string)[2:][:-3]+"Blend_decomposeMatrix")
                    self.MDG2_mod.renameNode(pvarmjoint_decomposeMatrix, str(pvjnt_string)[2:][:-3]+"Blend_decomposeMatrix")
                    self.MDG2_mod.renameNode(armrotblendnode, str(bindjnt_string)[2:][:-3]+"Rot_kneeblend")
                    self.MDG2_mod.renameNode(armtransblendnode, str(bindjnt_string)[2:][:-3]+"Trans_kneeblend")

                    armrotblendnode_fs = om2.MFnDependencyNode(armrotblendnode)
                    armtransblendnode_fs = om2.MFnDependencyNode(armtransblendnode)
                    nofliparmdecomposeMatrix_fs = om2.MFnDependencyNode(nofliparmjoint_decomposeMatrix)
                    pvarmdecomposeMatrix_fs = om2.MFnDependencyNode(pvarmjoint_decomposeMatrix)
                    noflipikarmjoint_fs = om2.MFnDependencyNode(noflipjnt_obj)
                    pvikarmjoint_fs = om2.MFnDependencyNode(pvjnt_obj)

                    nofliparmdecomposeInpMatrix_plug = nofliparmdecomposeMatrix_fs.findPlug("inputMatrix", False)
                    nofliparmdecomposeOtpRot_plug = nofliparmdecomposeMatrix_fs.findPlug("outputRotate", False)
                    nofliparmdecomposeOtpTrans_plug = nofliparmdecomposeMatrix_fs.findPlug("outputTranslate", False)
                    pvarmdecomposeInpMatrix_plug = pvarmdecomposeMatrix_fs.findPlug("inputMatrix", False)
                    pvarmdecomposeOtpRot_plug = pvarmdecomposeMatrix_fs.findPlug("outputRotate", False)
                    pvarmdecomposeOtpTrans_plug = pvarmdecomposeMatrix_fs.findPlug("outputTranslate", False)
                    armrotblendnodeinp1_plug = armrotblendnode_fs.findPlug("color1", False)
                    armrotblendnodeinp2_plug = armrotblendnode_fs.findPlug("color2", False)
                    armrotblendnodeotp_plug = armrotblendnode_fs.findPlug("output", False)
                    armrotblendnodeblender_plug = armrotblendnode_fs.findPlug("blender", False)
                    armtransblendnodeinp1_plug = armtransblendnode_fs.findPlug("color1", False)
                    armtransblendnodeinp2_plug = armtransblendnode_fs.findPlug("color2", False)
                    armtransblendnodeotp_plug = armtransblendnode_fs.findPlug("output", False)
                    armtransblendnodeblender_plug = armtransblendnode_fs.findPlug("blender", False)
                    noflipikarmjointotp_plug = noflipikarmjoint_fs.findPlug("matrix", False)
                    pvikarmjointotp_plug = pvikarmjoint_fs.findPlug("matrix", False)
                    ikarmjointinpTrans_plug = ikarmjoint_fs.findPlug("translate", False)
                    ikarmjointinpRot_plug = ikarmjoint_fs.findPlug("jointOrient", False)

                    self.MDG2_mod.connect(noflipikarmjointotp_plug, nofliparmdecomposeInpMatrix_plug)
                    self.MDG2_mod.connect(pvikarmjointotp_plug, pvarmdecomposeInpMatrix_plug)
                    self.MDG2_mod.connect(pvarmdecomposeOtpRot_plug, armrotblendnodeinp1_plug)
                    self.MDG2_mod.connect(pvarmdecomposeOtpTrans_plug, armtransblendnodeinp1_plug)
                    self.MDG2_mod.connect(nofliparmdecomposeOtpRot_plug, armrotblendnodeinp2_plug)
                    self.MDG2_mod.connect(nofliparmdecomposeOtpTrans_plug, armtransblendnodeinp2_plug)
                    self.MDG2_mod.connect(armrotblendnodeotp_plug, ikarmjointinpRot_plug)
                    self.MDG2_mod.connect(armtransblendnodeotp_plug, ikarmjointinpTrans_plug)
                    self.MDG2_mod.connect(lhandoptionskneeswitch_plug, armrotblendnodeblender_plug)
                    self.MDG2_mod.connect(lhandoptionskneeswitch_plug, armtransblendnodeblender_plug)

                else:
                    self.MDG2_mod.connect(fkarmjointtransotp_plug, armjointtransinp_plug)
                    self.MDG2_mod.connect(fkarmjointrototp_plug, armjointrotinp_plug)

            if self.autostretch.currentIndex() == 1:
                if index < 2:
                    iklarmgrp_sl_lst = om2.MSelectionList()
                    iklarmgrp_sl_lst.add("LeftUpperArmIkCluster_grp")
                    iklarmgrp_sl_lst.add("LeftUpperArmIkCluster2_grp")
                    iklarmgrp_sl_lst.add("LeftLowerArmIkCluster_grp")
                    iklarmgrp_sl_lst.add("LeftLowerArmIkCluster2_grp")
                    grp_armupperikcluster = iklarmgrp_sl_lst.getDependNode(0)
                    grp_armupperikcluster2 = iklarmgrp_sl_lst.getDependNode(1)
                    grp_armlowerikcluster = iklarmgrp_sl_lst.getDependNode(2)
                    grp_armlowerikcluster2 = iklarmgrp_sl_lst.getDependNode(3)

                    larmjoint_multMatrix = self.MDG2_mod.createNode("multMatrix")
                    armjoint_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")

                    larmmultMatrix_fs = om2.MFnDependencyNode(larmjoint_multMatrix)
                    larmdecomposeMatrix_fs = om2.MFnDependencyNode(armjoint_decomposeMatrix)
                    iklupperarmgrp_fs = om2.MFnDependencyNode(grp_armupperikcluster)
                    ikllowerarmgrp_fs = om2.MFnDependencyNode(grp_armlowerikcluster)

                    larmmultMatrixSum_plug = larmmultMatrix_fs.findPlug("matrixSum", False)
                    larmdecomposeInpMatrix_plug = larmdecomposeMatrix_fs.findPlug("inputMatrix", False)
                    larmdecomposeOtpTrans_plug = larmdecomposeMatrix_fs.findPlug("outputTranslate", False)
                    larmdecomposeOtpRot_plug = larmdecomposeMatrix_fs.findPlug("outputRotate", False)
                    iklupperarmgrpTrans_plug = iklupperarmgrp_fs.findPlug("translate", False)
                    iklupperarmgrpRot_plug = iklupperarmgrp_fs.findPlug("rotate", False)
                    ikllowerarmgrpTrans_plug = ikllowerarmgrp_fs.findPlug("translate", False)
                    ikllowerarmgrpRot_plug = ikllowerarmgrp_fs.findPlug("rotate", False)

                    self.MDG2_mod.renameNode(larmjoint_multMatrix, str(bindjnt_string)[2:][:-3]+"_multMatrix")
                    self.MDG2_mod.renameNode(armjoint_decomposeMatrix, str(bindjnt_string)[2:][:-3]+"_decomposeMatrix")
                    self.MDG2_mod.commandToExecute('connectAttr -force {0}.worldMatrix[0] {0}_multMatrix.matrixIn[0]'.format(str(bindjnt_string)[3:][:-3]))
                    self.MDG2_mod.connect(larmmultMatrixSum_plug, larmdecomposeInpMatrix_plug)

                    fklarmstretch_expression = om1.MFnExpression()

                    if index == 0:
                        fklarmstretch_expression.create("Biped_FkLeftForeArm_ctrl.translateY = Biped_FkLeftArm_ctrl.stretchy")
                        fklarmstretch_expression.create("Biped_FkLeftForeArm_ctrl.translateZ = Biped_FkLeftForeArm_ctrl.translateY/10")
                        fklarmstretch_expression.create("Biped_FkLeftForeArm_ctrl.translateX = Biped_FkLeftForeArm_ctrl.translateY/10")

                        self.MDG2_mod.commandToExecute('connectAttr -force LeftUpperArmIkCluster_grp.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(bindjnt_string)[3:][:-3]))
                        self.MDG2_mod.connect(larmdecomposeOtpTrans_plug, iklupperarmgrpTrans_plug)
                        self.MDG2_mod.connect(larmdecomposeOtpRot_plug, iklupperarmgrpRot_plug)

                        lupperarmcluster2_multMatrix = self.MDG2_mod.createNode("multMatrix")
                        lupperarmcluster2_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")

                        lupperarmcluster2multMatrix_fs = om2.MFnDependencyNode(lupperarmcluster2_multMatrix)
                        lupperarmcluster2decomposeMatrix_fs = om2.MFnDependencyNode(lupperarmcluster2_decomposeMatrix)
                        lupperarmcluster2_fs = om2.MFnDependencyNode(grp_armupperikcluster2)

                        lupperarmcluster2multMatrixSum_plug = lupperarmcluster2multMatrix_fs.findPlug("matrixSum", False)
                        lupperarmcluster2decomposeInpMatrix_plug = lupperarmcluster2decomposeMatrix_fs.findPlug("inputMatrix", False)
                        lupperarmcluster2decomposeOtpTrans_plug = lupperarmcluster2decomposeMatrix_fs.findPlug("outputTranslate", False)
                        lupperarmcluster2Trans_plug = lupperarmcluster2_fs.findPlug("translate", False)

                        self.MDG2_mod.renameNode(lupperarmcluster2_multMatrix, "LeftUpperArmCluster2_multMatrix")
                        self.MDG2_mod.renameNode(lupperarmcluster2_decomposeMatrix,"LeftUpperArmCluster2_decomposeMatrix")
                        self.MDG2_mod.connect(lupperarmcluster2multMatrixSum_plug, lupperarmcluster2decomposeInpMatrix_plug)
                        self.MDG2_mod.commandToExecute('connectAttr -force LeftForeArm.worldMatrix[0] LeftUpperArmCluster2_multMatrix.matrixIn[0]')
                        self.MDG2_mod.commandToExecute('connectAttr -force LeftUpperArmIkCluster2_grp.parentInverseMatrix[0] LeftUpperArmCluster2_multMatrix.matrixIn[1]')
                        self.MDG2_mod.connect(lupperarmcluster2decomposeOtpTrans_plug, lupperarmcluster2Trans_plug)

                    elif index == 1:
                        fklarmstretch_expression.create("Biped_FkLeftHand_ctrl.translateY = Biped_FkLeftForeArm_ctrl.stretchy")

                        self.MDG2_mod.commandToExecute('connectAttr -force LeftLowerArmIkCluster_grp.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(bindjnt_string)[3:][:-3]))
                        self.MDG2_mod.connect(larmdecomposeOtpTrans_plug, ikllowerarmgrpTrans_plug)
                        self.MDG2_mod.connect(larmdecomposeOtpRot_plug, ikllowerarmgrpRot_plug)

                        llowerarmcluster2_multMatrix = self.MDG2_mod.createNode("multMatrix")
                        llowerarmcluster2_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")

                        llowerarmcluster2multMatrix_fs = om2.MFnDependencyNode(llowerarmcluster2_multMatrix)
                        llowerarmcluster2decomposeMatrix_fs = om2.MFnDependencyNode(llowerarmcluster2_decomposeMatrix)
                        llowerarmcluster2_fs = om2.MFnDependencyNode(grp_armlowerikcluster2)

                        llowerarmcluster2multMatrixSum_plug = llowerarmcluster2multMatrix_fs.findPlug("matrixSum", False)
                        llowerarmcluster2decomposeInpMatrix_plug = llowerarmcluster2decomposeMatrix_fs.findPlug("inputMatrix", False)
                        llowerarmcluster2decomposeOtpTrans_plug = llowerarmcluster2decomposeMatrix_fs.findPlug("outputTranslate", False)
                        llowerarmcluster2Trans_plug = llowerarmcluster2_fs.findPlug("translate", False)

                        self.MDG2_mod.renameNode(llowerarmcluster2_multMatrix, "LeftLowerArmCluster2_multMatrix")
                        self.MDG2_mod.renameNode(llowerarmcluster2_decomposeMatrix,"LeftLowerArmCluster2_decomposeMatrix")
                        self.MDG2_mod.commandToExecute('connectAttr -force LeftHand.worldMatrix[0] LeftLowerArmCluster2_multMatrix.matrixIn[0]')
                        self.MDG2_mod.commandToExecute('connectAttr -force LeftLowerArmIkCluster2_grp.parentInverseMatrix[0] LeftLowerArmCluster2_multMatrix.matrixIn[1]')
                        self.MDG2_mod.connect(llowerarmcluster2multMatrixSum_plug, llowerarmcluster2decomposeInpMatrix_plug)
                        self.MDG2_mod.connect(llowerarmcluster2decomposeOtpTrans_plug, llowerarmcluster2Trans_plug)

            elif cmds.objExists("LeftArmIkCluster_grp") and cmds.objExists("IkStretchyLeftJointArm_grp"):
                self.MDG2_mod.commandToExecute('delete "LeftArmIkCluster_grp"')
                self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false Biped_FkLeftArm_ctrl.stretchy')
                self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false Biped_FkLeftForeArm_ctrl.stretchy')
                self.MDG2_mod.doIt()

        grp_armupperikcluster1 = om1.MObject()
        grp_armupperikcluster2 = om1.MObject()
        obj_stretchyleftarm1 = om1.MObject()

        if self.autostretch.currentIndex() == 1:

            self.MDG2_mod.commandToExecute('addAttr -longName "stretchable" -niceName "Stretchable" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_LeftHandOptions_ctrl')
            self.MDG2_mod.doIt()

            stretchy_sl_lst1.add("Biped_LeftHandOptions_ctrl")
            stretchy_sl_lst1.getDependNode(2, obj_stretchyleftarm1)

            if cmds.objExists("IkSplineLeftUpperArm0"):
                iklupperarm_sl_lst = om1.MSelectionList()
                iklupperarm_sl_lst.add("IkSplineLeftUpperArm*")
                iklupperarm_sl_lst.getDependNode(0, obj_root)
                iklupperarm_sl_lst.getDependNode(iklupperarm_sl_lst.length()-1, obj_endspine)

                iklupperarmgrp_sl_lst = om1.MSelectionList()
                iklupperarmgrp_sl_lst.add("LeftUpperArmIkCluster1_grp")
                iklupperarmgrp_sl_lst.add("LeftUpperArmIkCluster2_grp")
                iklupperarmgrp_sl_lst.getDependNode(0, grp_armupperikcluster1)
                iklupperarmgrp_sl_lst.getDependNode(1, grp_armupperikcluster2)

                self.MDag_path = om1.MDagPath()
                rootspine_path = self.MDag_path.getAPathTo(obj_root)

                try:
                    ikspineiksolver_lst.add("ikSplineSolver*")
                except:
                    cmds.createNode("ikSplineSolver")

                self.iklarm_effector = self.IK_Effector.create(obj_endspine)
                iklarm_effector_path = self.MDag_path.getAPathTo(self.iklarm_effector)

                self.larm_ik = self.IK_Handle.create(rootspine_path, iklarm_effector_path)

                obj_array = om1.MPointArray()
                obj_lst_mpoint = []
                obj = om1.MObject()
                for index in range(iklupperarm_sl_lst.length()):
                    iklupperarm_sl_lst.getDependNode(index, obj)
                    obj_path = self.MDag_path.getAPathTo(obj)
                    obj_tn = om1.MFnTransform(obj_path)
                    obj_t = obj_tn.translation(om1.MSpace.kWorld)
                    obj_lst_mpoint.append(om1.MPoint(obj_t))
                    obj_array.append(obj_lst_mpoint[index])

                self.ikspline_cv_tn = ikspinedag_n.create("transform", "LeftUpperArm_SplineCv")
                ikspline_cv = self.MNurbs1_cv.createWithEditPoints(obj_array, 1, 1, False, True, True, self.ikspline_cv_tn)
                cmds.parent("LeftUpperArm_SplineCv", "DoNotTouch")

                larmcrv_info = ikspinedg_modifier.createNode("curveInfo")
                larmstretchpercent = ikspinedg_modifier.createNode("multiplyDivide")
                larmstretchpow = ikspinedg_modifier.createNode("multiplyDivide")
                larmstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                larmscalediv = ikspinedg_modifier.createNode("multiplyDivide")
                likarmstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                blendstretch = ikspinedg_modifier.createNode("blendColors")

                larmcrvinfo_fs = om1.MFnDependencyNode(larmcrv_info)
                larmstretchpercent_fs = om1.MFnDependencyNode(larmstretchpercent)
                larmstretchpow_fs = om1.MFnDependencyNode(larmstretchpow)
                larmstretchdiv_fs = om1.MFnDependencyNode(larmstretchdiv)
                larmscalediv_fs = om1.MFnDependencyNode(larmscalediv)
                likarmstretchdiv_fs = om1.MFnDependencyNode(likarmstretchdiv)
                likarmstretchcluster1_fs = om1.MFnDependencyNode(grp_armupperikcluster1)
                likarmstretchcluster2_fs = om1.MFnDependencyNode(grp_armupperikcluster2)
                blendstretch_fs = om1.MFnDependencyNode(blendstretch)
                larmstretchoption_fs = om1.MFnDependencyNode(obj_stretchyleftarm1)

                larmcrvinfoarc_plug = larmcrvinfo_fs.findPlug("arcLength")
                larmstretchpercentinp1y_plug = larmstretchpercent_fs.findPlug("input1Y")
                larmstretchpercentotp_plug = larmstretchpercent_fs.findPlug("outputY")
                larmstretchpowinp1x_plug = larmstretchpow_fs.findPlug("input1X")
                larmstretchpowinp1z_plug = larmstretchpow_fs.findPlug("input1Z")
                larmstretchpowotpx_plug = larmstretchpow_fs.findPlug("outputX")
                larmstretchpowotpz_plug = larmstretchpow_fs.findPlug("outputZ")
                larmstretchdivinp2x_plug = larmstretchdiv_fs.findPlug("input2X")
                larmstretchdivinp2z_plug = larmstretchdiv_fs.findPlug("input2Z")
                larmstretchdivotox_plug = larmstretchdiv_fs.findPlug("outputX")
                larmstretchdivotpz_plug = larmstretchdiv_fs.findPlug("outputZ")
                larmscaledivinp1y_plug = larmscalediv_fs.findPlug("input1Y")
                larmscaledivinp2y_plug = larmscalediv_fs.findPlug("input2Y")
                larmscaledivotpy_plug = larmscalediv_fs.findPlug("outputY")
                likarmstretchdivinp1_plug = likarmstretchdiv_fs.findPlug("input1")
                likarmstretchdivotp_plug = likarmstretchdiv_fs.findPlug("output")
                likarmstretchclust1trans_plug = likarmstretchcluster1_fs.findPlug("translate")
                likarmstretchclust2trans_plug = likarmstretchcluster2_fs.findPlug("translate")
                blendstretchinp1r_plug = blendstretch_fs.findPlug("color1R")
                blendstretchinp1g_plug = blendstretch_fs.findPlug("color1G")
                blendstretchinp1b_plug = blendstretch_fs.findPlug("color1B")
                blendstretchotpr_plug = blendstretch_fs.findPlug("outputR")
                blendstretchotpg_plug = blendstretch_fs.findPlug("outputG")
                blendstretchotpb_plug = blendstretch_fs.findPlug("outputB")
                blendstretch_plug = blendstretch_fs.findPlug("blender")
                larmstretchoption_plug = larmstretchoption_fs.findPlug("stretchable")

                objparent = om1.MObject()
                objchild = om1.MObject()
                for index in range(iklupperarm_sl_lst.length()):
                    if index < iklupperarm_sl_lst.length()-1:
                        iklupperarm_sl_lst.getDependNode(index, objparent)
                        iklupperarm_sl_lst.getDependNode(index+1, objchild)
                        larmparentjnt_fs = om1.MFnDependencyNode(objparent)
                        larmchildjnt_fs = om1.MFnDependencyNode(objchild)
                        larmjnt_syplug = larmparentjnt_fs.findPlug("scaleY")
                        larmjnt_sxplug = larmparentjnt_fs.findPlug("scaleX")
                        larmjnt_szplug = larmparentjnt_fs.findPlug("scaleZ")
                        larmjnt_sotpplug = larmparentjnt_fs.findPlug("scale")
                        larmjnt_invsplug = larmchildjnt_fs.findPlug("inverseScale")
                        ikspinedg_modifier.connect(larmstretchpercentotp_plug, blendstretchinp1g_plug)
                        ikspinedg_modifier.connect(larmstretchdivotox_plug, blendstretchinp1r_plug)
                        ikspinedg_modifier.connect(larmstretchdivotpz_plug, blendstretchinp1b_plug)
                        ikspinedg_modifier.connect(blendstretchotpg_plug, larmjnt_syplug)
                        ikspinedg_modifier.connect(blendstretchotpr_plug, larmjnt_sxplug)
                        ikspinedg_modifier.connect(blendstretchotpb_plug, larmjnt_szplug)
                        ikspinedg_modifier.connect(larmjnt_sotpplug, larmjnt_invsplug)

                ikspinedg_modifier.renameNode(larmcrv_info, "LeftUpperArmSpline_Info")
                ikspinedg_modifier.renameNode(larmstretchpercent, "LeftUpperArmStretch_Percent")
                ikspinedg_modifier.renameNode(larmstretchpow, "LeftUpperArmStretch_Power")
                ikspinedg_modifier.renameNode(larmstretchdiv, "LeftUpperArmStretch_Divide")
                ikspinedg_modifier.renameNode(ikspline_cv, "LeftUpperArm_SplineCvShape")
                ikspinedg_modifier.renameNode(self.larm_ik, "LeftUpperArm_Ik")
                ikspinedg_modifier.renameNode(self.iklarm_effector, "LeftUpperArm_effector")
                ikspinedg_modifier.renameNode(larmscalediv, "IkLeftUpperArmGlobalScale_Average")
                ikspinedg_modifier.renameNode(likarmstretchdiv, "LeftUpperArmStretch_Divide2")
                ikspinedg_modifier.renameNode(blendstretch, "LeftUpperArmStretch_Blend")
                ikspinedg_modifier.commandToExecute('parent "LeftUpperArm_Ik" "DoNotTouch"')
                ikspinedg_modifier.commandToExecute('connectAttr -force LeftUpperArm_SplineCvShape.worldSpace[0] LeftUpperArm_Ik.inCurve')
                ikspinedg_modifier.commandToExecute('skinCluster -bm 3 -sm 1 -dr 2.0 -name "LeftUpperArmIk_skin" IkCvSplineLeftUpperArm0 IkCvSplineLeftUpperArm1 IkCvSplineLeftUpperArm2 LeftUpperArm_SplineCv')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArm_Ik.dTwistControlEnable" 1')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArm_Ik.dWorldUpType" 4')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArm_Ik.dForwardAxis" 3')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArm_Ik.dWorldUpAxis" 4')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArm_Ik.dWorldUpVectorY" 0')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArm_Ik.dWorldUpVectorEndY" 0')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArm_Ik.dWorldUpVectorZ" -1')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArm_Ik.dWorldUpVectorEndZ" -1')
                ikspinedg_modifier.commandToExecute('connectAttr -force IkCvSplineLeftUpperArm0.worldMatrix[0] LeftUpperArm_Ik.dWorldUpMatrix')
                ikspinedg_modifier.commandToExecute('connectAttr -force IkCvSplineLeftUpperArm2.worldMatrix[0] LeftUpperArm_Ik.dWorldUpMatrixEnd')
                ikspinedg_modifier.commandToExecute('connectAttr -force LeftUpperArm_SplineCvShape.worldSpace[0] LeftUpperArmSpline_Info.inputCurve')
                ikspinedg_modifier.connect(larmcrvinfoarc_plug, larmscaledivinp1y_plug)
                ikspinedg_modifier.connect(masterctrlsy_plug, larmscaledivinp2y_plug)
                ikspinedg_modifier.connect(larmscaledivotpy_plug, larmstretchpercentinp1y_plug)
                ikspinedg_modifier.connect(larmstretchpercentotp_plug, larmstretchpowinp1x_plug)
                ikspinedg_modifier.connect(larmstretchpercentotp_plug, larmstretchpowinp1z_plug)
                ikspinedg_modifier.connect(larmstretchpowotpx_plug, larmstretchdivinp2x_plug)
                ikspinedg_modifier.connect(larmstretchpowotpz_plug, larmstretchdivinp2z_plug)
                ikspinedg_modifier.connect(likarmstretchclust2trans_plug, likarmstretchdivinp1_plug)
                ikspinedg_modifier.connect(likarmstretchdivotp_plug, likarmstretchclust1trans_plug)
                ikspinedg_modifier.connect(larmstretchoption_plug, blendstretch_plug)
                ikspinedg_modifier.commandToExecute('float $leftupperarmstretchinput1Y = `getAttr "LeftUpperArmStretch_Percent.input1Y"`; setAttr "LeftUpperArmStretch_Percent.input2Y" $leftupperarmstretchinput1Y')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArmStretch_Power.input2X" 0.5')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArmStretch_Power.input2Z" 0.5')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArmStretch_Divide.input1X" 1')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArmStretch_Divide.input1Z" 1')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArmStretch_Percent.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArmStretch_Power.operation" 3')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArmStretch_Divide.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "IkLeftUpperArmGlobalScale_Average.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArmStretch_Divide2.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArmStretch_Divide2.input2X" 2')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArmStretch_Divide2.input2Y" 2')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArmStretch_Divide2.input2Z" 2')
                ikspinedg_modifier.commandToExecute('setAttr "IkNeckGlobalScale_Average.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArmStretch_Blend.color2R" 1')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArmStretch_Blend.color2G" 1')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperArmStretch_Blend.color2B" 1')
                ikspinedg_modifier.doIt()

                ikspline_solver = self.IK_System.findSolver("ikSplineSolver")
                self.IK_Handle.setSolver(ikspline_solver)

            grp_armlowerikcluster1 = om1.MObject()
            grp_armlowerikcluster2 = om1.MObject()

            if cmds.objExists("IkSplineLeftLowerArm0"):
                ikllowerarm_sl_lst = om1.MSelectionList()
                ikllowerarm_sl_lst.add("IkSplineLeftLowerArm*")
                ikllowerarm_sl_lst.getDependNode(0, obj_root)
                ikllowerarm_sl_lst.getDependNode(ikllowerarm_sl_lst.length()-1, obj_endspine)

                ikllowerarmgrp_sl_lst = om1.MSelectionList()
                ikllowerarmgrp_sl_lst.add("LeftLowerArmIkCluster1_grp")
                ikllowerarmgrp_sl_lst.add("LeftLowerArmIkCluster2_grp")
                ikllowerarmgrp_sl_lst.getDependNode(0, grp_armlowerikcluster1)
                ikllowerarmgrp_sl_lst.getDependNode(1, grp_armlowerikcluster2)

                rootspine_path = self.MDag_path.getAPathTo(obj_root)

                try:
                    ikspineiksolver_lst.add("ikSplineSolver*")
                except:
                    cmds.createNode("ikSplineSolver")

                self.iklarm_effector = self.IK_Effector.create(obj_endspine)
                iklarm_effector_path = self.MDag_path.getAPathTo(self.iklarm_effector)

                self.larm_ik = self.IK_Handle.create(rootspine_path, iklarm_effector_path)

                obj_array = om1.MPointArray()
                obj_lst_mpoint = []
                obj = om1.MObject()
                for index in range(ikllowerarm_sl_lst.length()):
                    ikllowerarm_sl_lst.getDependNode(index, obj)
                    obj_path = self.MDag_path.getAPathTo(obj)
                    obj_tn = om1.MFnTransform(obj_path)
                    obj_t = obj_tn.translation(om1.MSpace.kWorld)
                    obj_lst_mpoint.append(om1.MPoint(obj_t))
                    obj_array.append(obj_lst_mpoint[index])

                self.ikspline_cv_tn = ikspinedag_n.create("transform", "LeftLowerArm_SplineCv")
                ikspline_cv = self.MNurbs1_cv.createWithEditPoints(obj_array, 1, 1, False, True, True, self.ikspline_cv_tn)
                cmds.parent("LeftLowerArm_SplineCv", "DoNotTouch")

                larmcrv_info = ikspinedg_modifier.createNode("curveInfo")
                larmstretchpercent = ikspinedg_modifier.createNode("multiplyDivide")
                larmstretchpow = ikspinedg_modifier.createNode("multiplyDivide")
                larmstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                larmscalediv = ikspinedg_modifier.createNode("multiplyDivide")
                likarmstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                blendstretch = ikspinedg_modifier.createNode("blendColors")

                larmcrvinfo_fs = om1.MFnDependencyNode(larmcrv_info)
                larmstretchpercent_fs = om1.MFnDependencyNode(larmstretchpercent)
                larmstretchpow_fs = om1.MFnDependencyNode(larmstretchpow)
                larmstretchdiv_fs = om1.MFnDependencyNode(larmstretchdiv)
                larmscalediv_fs = om1.MFnDependencyNode(larmscalediv)
                likarmstretchdiv_fs = om1.MFnDependencyNode(likarmstretchdiv)
                likarmstretchcluster1_fs = om1.MFnDependencyNode(grp_armlowerikcluster1)
                likarmstretchcluster2_fs = om1.MFnDependencyNode(grp_armlowerikcluster2)
                blendstretch_fs = om1.MFnDependencyNode(blendstretch)

                larmcrvinfoarc_plug = larmcrvinfo_fs.findPlug("arcLength")
                larmstretchpercentinp1y_plug = larmstretchpercent_fs.findPlug("input1Y")
                larmstretchpercentotp_plug = larmstretchpercent_fs.findPlug("outputY")
                larmstretchpowinp1x_plug = larmstretchpow_fs.findPlug("input1X")
                larmstretchpowinp1z_plug = larmstretchpow_fs.findPlug("input1Z")
                larmstretchpowotpx_plug = larmstretchpow_fs.findPlug("outputX")
                larmstretchpowotpz_plug = larmstretchpow_fs.findPlug("outputZ")
                larmstretchdivinp2x_plug = larmstretchdiv_fs.findPlug("input2X")
                larmstretchdivinp2z_plug = larmstretchdiv_fs.findPlug("input2Z")
                larmstretchdivotox_plug = larmstretchdiv_fs.findPlug("outputX")
                larmstretchdivotpz_plug = larmstretchdiv_fs.findPlug("outputZ")
                larmscaledivinp1y_plug = larmscalediv_fs.findPlug("input1Y")
                larmscaledivinp2y_plug = larmscalediv_fs.findPlug("input2Y")
                larmscaledivotpy_plug = larmscalediv_fs.findPlug("outputY")
                likarmstretchdivinp1_plug = likarmstretchdiv_fs.findPlug("input1")
                likarmstretchdivotp_plug = likarmstretchdiv_fs.findPlug("output")
                likarmstretchclust1trans_plug = likarmstretchcluster1_fs.findPlug("translate")
                likarmstretchclust2trans_plug = likarmstretchcluster2_fs.findPlug("translate")
                blendstretchinp1r_plug = blendstretch_fs.findPlug("color1R")
                blendstretchinp1g_plug = blendstretch_fs.findPlug("color1G")
                blendstretchinp1b_plug = blendstretch_fs.findPlug("color1B")
                blendstretchotpr_plug = blendstretch_fs.findPlug("outputR")
                blendstretchotpg_plug = blendstretch_fs.findPlug("outputG")
                blendstretchotpb_plug = blendstretch_fs.findPlug("outputB")
                blendstretch_plug = blendstretch_fs.findPlug("blender")

                objparent = om1.MObject()
                objchild = om1.MObject()
                for index in range(ikllowerarm_sl_lst.length()):
                    if index < ikllowerarm_sl_lst.length()-1:
                        ikllowerarm_sl_lst.getDependNode(index, objparent)
                        ikllowerarm_sl_lst.getDependNode(index+1, objchild)
                        larmparentjnt_fs = om1.MFnDependencyNode(objparent)
                        larmchildjnt_fs = om1.MFnDependencyNode(objchild)
                        larmjnt_syplug = larmparentjnt_fs.findPlug("scaleY")
                        larmjnt_sxplug = larmparentjnt_fs.findPlug("scaleX")
                        larmjnt_szplug = larmparentjnt_fs.findPlug("scaleZ")
                        larmjnt_sotpplug = larmparentjnt_fs.findPlug("scale")
                        larmjnt_invsplug = larmchildjnt_fs.findPlug("inverseScale")
                        ikspinedg_modifier.connect(larmstretchpercentotp_plug, blendstretchinp1g_plug)
                        ikspinedg_modifier.connect(larmstretchdivotox_plug, blendstretchinp1r_plug)
                        ikspinedg_modifier.connect(larmstretchdivotpz_plug, blendstretchinp1b_plug)
                        ikspinedg_modifier.connect(blendstretchotpg_plug, larmjnt_syplug)
                        ikspinedg_modifier.connect(blendstretchotpr_plug, larmjnt_sxplug)
                        ikspinedg_modifier.connect(blendstretchotpb_plug, larmjnt_szplug)
                        ikspinedg_modifier.connect(larmjnt_sotpplug, larmjnt_invsplug)


                ikspinedg_modifier.renameNode(larmcrv_info, "LeftLowerArmSpline_Info")
                ikspinedg_modifier.renameNode(larmstretchpercent, "LeftLowerArmStretch_Percent")
                ikspinedg_modifier.renameNode(larmstretchpow, "LeftLowerArmStretch_Power")
                ikspinedg_modifier.renameNode(larmstretchdiv, "LeftLowerArmStretch_Divide")
                ikspinedg_modifier.renameNode(ikspline_cv, "LeftLowerArm_SplineCvShape")
                ikspinedg_modifier.renameNode(self.larm_ik, "LeftLowerArm_Ik")
                ikspinedg_modifier.renameNode(self.iklarm_effector, "LeftLowerArm_effector")
                ikspinedg_modifier.renameNode(larmscalediv, "IkLeftLowerArmGlobalScale_Average")
                ikspinedg_modifier.renameNode(likarmstretchdiv, "LeftLowerArmStretch_Divide2")
                ikspinedg_modifier.renameNode(blendstretch, "LeftLowerArmStretch_Blend")
                ikspinedg_modifier.commandToExecute('parent "LeftLowerArm_Ik" "DoNotTouch"')
                ikspinedg_modifier.commandToExecute('connectAttr -f LeftLowerArm_SplineCvShape.worldSpace[0] LeftLowerArm_Ik.inCurve')
                ikspinedg_modifier.commandToExecute('skinCluster -bm 3 -sm 1 -dr 2.0 -name "LeftLowerArmIk_skin" IkCvSplineLeftLowerArm0 IkCvSplineLeftLowerArm1 IkCvSplineLeftLowerArm2 LeftLowerArm_SplineCv')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArm_Ik.dTwistControlEnable" 1')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArm_Ik.dWorldUpType" 4')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArm_Ik.dForwardAxis" 3')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArm_Ik.dWorldUpAxis" 4')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArm_Ik.dWorldUpVectorY" 0')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArm_Ik.dWorldUpVectorEndY" 0')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArm_Ik.dWorldUpVectorZ" -1')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArm_Ik.dWorldUpVectorEndZ" -1')
                ikspinedg_modifier.commandToExecute('connectAttr -f IkCvSplineLeftLowerArm0.worldMatrix[0] LeftLowerArm_Ik.dWorldUpMatrix')
                ikspinedg_modifier.commandToExecute('connectAttr -f IkCvSplineLeftLowerArm2.worldMatrix[0] LeftLowerArm_Ik.dWorldUpMatrixEnd')
                ikspinedg_modifier.commandToExecute('connectAttr -f LeftLowerArm_SplineCvShape.worldSpace[0] LeftLowerArmSpline_Info.inputCurve')
                ikspinedg_modifier.connect(larmcrvinfoarc_plug, larmscaledivinp1y_plug)
                ikspinedg_modifier.connect(masterctrlsy_plug, larmscaledivinp2y_plug)
                ikspinedg_modifier.connect(larmscaledivotpy_plug, larmstretchpercentinp1y_plug)
                ikspinedg_modifier.connect(larmstretchpercentotp_plug, larmstretchpowinp1x_plug)
                ikspinedg_modifier.connect(larmstretchpercentotp_plug, larmstretchpowinp1z_plug)
                ikspinedg_modifier.connect(larmstretchpowotpx_plug, larmstretchdivinp2x_plug)
                ikspinedg_modifier.connect(larmstretchpowotpz_plug, larmstretchdivinp2z_plug)
                ikspinedg_modifier.connect(likarmstretchclust2trans_plug, likarmstretchdivinp1_plug)
                ikspinedg_modifier.connect(likarmstretchdivotp_plug, likarmstretchclust1trans_plug)
                ikspinedg_modifier.connect(larmstretchoption_plug, blendstretch_plug)
                ikspinedg_modifier.commandToExecute('float $leftlowerarmstretchinput1Y = `getAttr "LeftLowerArmStretch_Percent.input1Y"`; setAttr "LeftLowerArmStretch_Percent.input2Y" $leftlowerarmstretchinput1Y')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArmStretch_Power.input2X" 0.5')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArmStretch_Power.input2Z" 0.5')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArmStretch_Divide.input1X" 1')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArmStretch_Divide.input1Z" 1')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArmStretch_Percent.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArmStretch_Power.operation" 3')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArmStretch_Divide.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "IkLeftLowerArmGlobalScale_Average.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArmStretch_Divide2.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArmStretch_Divide2.input2X" 2')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArmStretch_Divide2.input2Y" 2')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArmStretch_Divide2.input2Z" 2')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArmStretch_Blend.color2R" 1')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArmStretch_Blend.color2G" 1')
                ikspinedg_modifier.commandToExecute('setAttr "LeftLowerArmStretch_Blend.color2B" 1')
                ikspinedg_modifier.doIt()

                ikspline_solver = self.IK_System.findSolver("ikSplineSolver")
                self.IK_Handle.setSolver(ikspline_solver)

        stretchy_sl_lst2 = om2.MSelectionList()
        stretchy_sl_lst2.add("Biped_LeftHandOptions_ctrl")
        obj_stretchyleftarm2 = stretchy_sl_lst2.getDependNode(0)

        if cmds.objExists("NoFlipLeftHand_Ik") and cmds.objExists("PVLeftHand_Ik"):

            self.MDG2_mod.commandToExecute('addAttr -longName "follow" -niceName "Follow Body" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_IkLeftHand_ctrl')
            self.MDG2_mod.commandToExecute('parentConstraint -mo -weight 1 Biped_Root_ctrl Biped_IkLeftHandRot_null')
            self.MDG2_mod.doIt()

            lhandik_sl_ls = om2.MSelectionList()
            lhandik_sl_ls.add("LeftArmIk_grp")
            lhandik_sl_ls.add("Biped_NoFlipLeftElbow_null")
            lhandik_sl_ls.add("Biped_IkLeftHand_ctrl")
            lhandik_sl_ls.add("IkStretchyLeftJointArm_grp")
            likhandlegrp_fs = om2.MFnDependencyNode(lhandik_sl_ls.getDependNode(0))
            noflipleftelbownullobj_fs = om2.MFnDependencyNode(lhandik_sl_ls.getDependNode(1))
            ikarmctrl_fs = om2.MFnDependencyNode(lhandik_sl_ls.getDependNode(2))
            likhand_fs = om2.MFnDependencyNode(iklarm_sl_ls.getDependNode(2))

            if self.typeofLHandIK.currentIndex() == 1 or 2:
                likhandctrl_multMatrix = self.MDG2_mod.createNode("multMatrix")
                likhandctrl_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                likhandrot_multMatrix = self.MDG2_mod.createNode("multMatrix")
                likhandrot_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                self.MDG2_mod.renameNode(likhandctrl_multMatrix, "IkLeftHand_multMatrix")
                self.MDG2_mod.renameNode(likhandctrl_decomposeMatrix, "IkLeftHand_decomposeMatrix")
                self.MDG2_mod.renameNode(likhandrot_multMatrix, "IkLeftHandRot_multMatrix")
                self.MDG2_mod.renameNode(likhandrot_decomposeMatrix, "IkLeftHandRot_decomposeMatrix")

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
                likhandgrpTrans_plug = likhandlegrp_fs.findPlug("translate", False)
                likhandgrpRot_plug = likhandlegrp_fs.findPlug("rotate", False)
                ikarmctrlTrans_plug = ikarmctrl_fs.findPlug("translate", False)
                ikarmctrlRot_plug = ikarmctrl_fs.findPlug("rotate", False)
                noflipleftelbownullTrans_plug = noflipleftelbownullobj_fs.findPlug("translate", False)
                noflipleftelbownullRot_plug = noflipleftelbownullobj_fs.findPlug("rotate", False)
                likhandRot_plug = likhand_fs.findPlug("rotate", False)

                self.MDG2_mod.commandToExecute('connectAttr -force Biped_IkLeftHand_ctrl.worldMatrix[0] IkLeftHand_multMatrix.matrixIn[0]')
                self.MDG2_mod.commandToExecute('connectAttr -force Biped_IkLeftHand_ctrl.worldMatrix[0] IkLeftHandRot_multMatrix.matrixIn[0]')
                self.MDG2_mod.commandToExecute('connectAttr -force IkLeftHand.parentInverseMatrix[0] IkLeftHandRot_multMatrix.matrixIn[1]')
                self.MDG2_mod.commandToExecute('connectAttr -force Biped_IkLeftHand_ctrl.follow Biped_IkLeftHandRot_null_parentConstraint1.Biped_Root_ctrlW0')
                self.MDG2_mod.connect(likhandmultMatrixSum_plug, likhanddecomposeInpMatrix_plug)
                self.MDG2_mod.connect(likhanddecomposeOtpTrans_plug, likhandgrpTrans_plug)
                self.MDG2_mod.connect(likhanddecomposeOtpRot_plug, likhandgrpRot_plug)
                self.MDG2_mod.connect(likhandrotmultMatrixSum_plug, likhandrotdecomposeInpMatrix_plug)
                self.MDG2_mod.connect(ikarmctrlTrans_plug, noflipleftelbownullTrans_plug)
                self.MDG2_mod.connect(ikarmctrlRot_plug, noflipleftelbownullRot_plug)
                self.MDG2_mod.connect(likhandrotdecomposeOtpRot_plug, likhandRot_plug)
                self.MDG2_mod.commandToExecute('parent NoFlipLeftHand_Ik LeftArmIk_grp')
                self.MDG2_mod.commandToExecute('parent PVLeftHand_Ik LeftArmIk_grp')
                self.MDG2_mod.commandToExecute('poleVectorConstraint Biped_NoFlipLeftElbow_ctrl NoFlipLeftHand_Ik')
                self.MDG2_mod.commandToExecute('poleVectorConstraint Biped_PVLeftElbow_ctrl PVLeftHand_Ik')
                self.MDG2_mod.commandToExecute('setAttr "NoFlipLeftHand_Ik.twist" -90')

                if self.autostretch.currentIndex() == 1:
                    likarmdistloc = om2.MFnDagNode()

                    likarmdistloc1_tn = likarmdistloc.create("transform", "distloc_L_arm1", lhandik_sl_ls.getDependNode(3))
                    likarmdistloc1_ln = likarmdistloc.create("locator", "L_arm1_Shape", likarmdistloc1_tn)
                    likhanddistloc1_tn = likarmdistloc.create("transform", "distloc_L_hand1")
                    likhanddistloc1_ln = likarmdistloc.create("locator", "L_hand1_Shape", likhanddistloc1_tn)
                    self.MDG2_mod.commandToExecute('createNode "distanceDimShape"')
                    self.MDG2_mod.commandToExecute('rename "distanceDimension1" "IkLeftArmDistance_Info"')
                    self.MDG2_mod.doIt()

                    larmnull_transform_t = larmnull_transform.translation(om2.MSpace.kTransform)
                    likupperarmdistloc_transform = om2.MFnTransform(likarmdistloc1_tn)
                    likupperarmdistloc_transform.setTranslation(larmnull_transform_t, om2.MSpace.kTransform)

                    IkLeftArmDistance_sl_ls = om2.MSelectionList()
                    IkLeftArmDistance_sl_ls.add("IkLeftArmDistance_InfoShape")

                    likhandDist_fs = om2.MFnDependencyNode(likhanddistloc1_tn)
                    likarmjntDist_fs = om2.MFnDependencyNode(IkLeftArmDistance_sl_ls.getDependNode(0))

                    likarmjntDistPoint2_plug = likarmjntDist_fs.findPlug("endPoint", False)
                    likhandDistOtpTrans_plug = likhandDist_fs.findPlug("translate", False)

                    self.MDG2_mod.commandToExecute('connectAttr -force L_arm1_Shape.worldPosition[0] IkLeftArmDistance_InfoShape.startPoint')
                    self.MDG2_mod.connect(likhandDistOtpTrans_plug, likarmjntDistPoint2_plug)
                    self.MDG2_mod.connect(likhanddecomposeOtpTrans_plug, likhandDistOtpTrans_plug)
                    self.MDG2_mod.commandToExecute('float $noflipikleftforearmtranslateY = `getAttr "IkNoFlipLeftForeArm.translateY"`; float $noflipiklefthandtranslateY = `getAttr "IkNoFlipLeftHand.translateY"`; float $totalnoflipikleftarmtranslateY = $noflipikleftforearmtranslateY + $noflipiklefthandtranslateY; setDrivenKeyframe -currentDriver IkLeftArmDistance_InfoShape.distance -driverValue $totalnoflipikleftarmtranslateY -attribute "translateY" -value $noflipikleftforearmtranslateY IkNoFlipLeftForeArm;')
                    self.MDG2_mod.commandToExecute('float $noflipikleftforearmtranslateY = `getAttr "IkNoFlipLeftForeArm.translateY"`; float $noflipiklefthandtranslateY = `getAttr "IkNoFlipLeftHand.translateY"`; float $totalnoflipikleftarmtranslateY = $noflipikleftforearmtranslateY + $noflipiklefthandtranslateY; setDrivenKeyframe -currentDriver IkLeftArmDistance_InfoShape.distance -driverValue ($totalnoflipikleftarmtranslateY*2) -attribute "translateY" -value ($noflipikleftforearmtranslateY*2) IkNoFlipLeftForeArm;')
                    self.MDG2_mod.commandToExecute('float $noflipikleftforearmtranslateY = `getAttr "IkNoFlipLeftForeArm.translateY"`; float $noflipiklefthandtranslateY = `getAttr "IkNoFlipLeftHand.translateY"`; float $totalnoflipikleftarmtranslateY = $noflipikleftforearmtranslateY + $noflipiklefthandtranslateY; setDrivenKeyframe -currentDriver IkLeftArmDistance_InfoShape.distance -driverValue $totalnoflipikleftarmtranslateY -attribute "translateY" -value $noflipiklefthandtranslateY IkNoFlipLeftHand;')
                    self.MDG2_mod.commandToExecute('float $noflipikleftforearmtranslateY = `getAttr "IkNoFlipLeftForeArm.translateY"`; float $noflipiklefthandtranslateY = `getAttr "IkNoFlipLeftHand.translateY"`; float $totalnoflipikleftarmtranslateY = $noflipikleftforearmtranslateY + $noflipiklefthandtranslateY; setDrivenKeyframe -currentDriver IkLeftArmDistance_InfoShape.distance -driverValue ($totalnoflipikleftarmtranslateY*2) -attribute "translateY" -value ($noflipiklefthandtranslateY*2) IkNoFlipLeftHand;')
                    self.MDG2_mod.commandToExecute('float $pvikleftforearmtranslateY = `getAttr "IkPVLeftForeArm.translateY"`; float $pviklefthandtranslateY = `getAttr "IkPVLeftHand.translateY"`; float $totalpvikleftarmtranslateY = $pvikleftforearmtranslateY + $pviklefthandtranslateY; setDrivenKeyframe -currentDriver IkLeftArmDistance_InfoShape.distance -driverValue $totalpvikleftarmtranslateY -attribute "translateY" -value $pvikleftforearmtranslateY IkPVLeftForeArm;')
                    self.MDG2_mod.commandToExecute('float $pvikleftforearmtranslateY = `getAttr "IkPVLeftForeArm.translateY"`; float $pviklefthandtranslateY = `getAttr "IkPVLeftHand.translateY"`; float $totalpvikleftarmtranslateY = $pvikleftforearmtranslateY + $pviklefthandtranslateY; setDrivenKeyframe -currentDriver IkLeftArmDistance_InfoShape.distance -driverValue ($totalpvikleftarmtranslateY*2) -attribute "translateY" -value ($pvikleftforearmtranslateY*2) IkPVLeftForeArm;')
                    self.MDG2_mod.commandToExecute('float $pvikleftforearmtranslateY = `getAttr "IkPVLeftForeArm.translateY"`; float $pviklefthandtranslateY = `getAttr "IkPVLeftHand.translateY"`; float $totalpvikleftarmtranslateY = $pvikleftforearmtranslateY + $pviklefthandtranslateY; setDrivenKeyframe -currentDriver IkLeftArmDistance_InfoShape.distance -driverValue $totalpvikleftarmtranslateY -attribute "translateY" -value $pviklefthandtranslateY IkPVLeftHand;')
                    self.MDG2_mod.commandToExecute('float $pvikleftforearmtranslateY = `getAttr "IkPVLeftForeArm.translateY"`; float $pviklefthandtranslateY = `getAttr "IkPVLeftHand.translateY"`; float $totalpvikleftarmtranslateY = $pvikleftforearmtranslateY + $pviklefthandtranslateY; setDrivenKeyframe -currentDriver IkLeftArmDistance_InfoShape.distance -driverValue ($totalpvikleftarmtranslateY*2) -attribute "translateY" -value ($pviklefthandtranslateY*2) IkPVLeftHand;')
                    self.MDG2_mod.commandToExecute('selectKey -attribute translateY IkNoFlipLeftForeArm; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative')
                    self.MDG2_mod.commandToExecute('selectKey -attribute translateY IkPVLeftForeArm; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative')
                    self.MDG2_mod.commandToExecute('selectKey -attribute translateY IkNoFlipLeftHand; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative')
                    self.MDG2_mod.commandToExecute('selectKey -attribute translateY IkPVLeftHand; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative')
                    self.MDG2_mod.commandToExecute('parent "IkLeftArmDistance_Info" "DoNotTouch"')
                    self.MDG2_mod.commandToExecute('parent "distloc_L_hand1" "DoNotTouch"')

                    self.MDG2_mod.commandToExecute('addAttr -longName "elbowsnap" -niceName "Elbow Snap" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_PVLeftElbow_ctrl')

                    likarmdistloc2_tn = likarmdistloc.create("transform", "distloc_L_uparm2", lhandik_sl_ls.getDependNode(3))
                    likarmdistloc2_ln = likarmdistloc.create("locator", "L_uparm2_Shape", likarmdistloc2_tn)
                    likelbowdistloc_tn = likarmdistloc.create("transform", "distloc_L_legelbow")
                    likelbowdistloc_ln = likarmdistloc.create("locator", "L_legelbow_Shape", likelbowdistloc_tn)
                    likhanddistloc2_tn = likarmdistloc.create("transform", "distloc_L_leghand2")
                    likhanddistloc2_ln = likarmdistloc.create("locator", "L_leghand2_Shape", likhanddistloc2_tn)
                    pvleftelbowctrl_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                    likpvupperarmtransblendnode = self.MDG2_mod.createNode("blendColors")
                    likpvlowerarmtransblendnode = self.MDG2_mod.createNode("blendColors")
                    likpvupperarmstretchblendnode = self.MDG2_mod.createNode("blendColors")
                    likpvlowerarmstretchblendnode = self.MDG2_mod.createNode("blendColors")
                    self.MDG2_mod.commandToExecute('createNode "distanceDimShape"')
                    self.MDG2_mod.commandToExecute('createNode "distanceDimShape"')
                    self.MDG2_mod.renameNode(pvleftelbowctrl_decomposeMatrix, "PVLeftElbow_decomposeMatrix")
                    self.MDG2_mod.renameNode(likpvupperarmtransblendnode, "PVLeftUpperArmTrans_blend")
                    self.MDG2_mod.renameNode(likpvlowerarmtransblendnode, "PVLeftLowerArmTrans_blend")
                    self.MDG2_mod.renameNode(likpvupperarmstretchblendnode, "PVLeftUpperArmStretch_blend")
                    self.MDG2_mod.renameNode(likpvlowerarmstretchblendnode, "PVLeftLowerArmStretch_blend")
                    self.MDG2_mod.commandToExecute('rename "distanceDimension1" "LeftUpperArmDistance_Info"')
                    self.MDG2_mod.commandToExecute('rename "distanceDimension2" "LeftLowerArmDistance_Info"')
                    self.MDG2_mod.doIt()

                    likupperarmdistloc2_transform = om2.MFnTransform(likarmdistloc2_tn)
                    likupperarmdistloc2_transform.setTranslation(larmnull_transform_t, om2.MSpace.kTransform)

                    IkLeftArmDistance_sl_ls.add("LeftUpperArmDistance_InfoShape")
                    IkLeftArmDistance_sl_ls.add("LeftLowerArmDistance_InfoShape")
                    IkLeftArmDistance_sl_ls.add("IkPVLeftForeArm_translateY")
                    IkLeftArmDistance_sl_ls.add("IkPVLeftHand_translateY")
                    IkLeftArmDistance_sl_ls.add("Biped_PVLeftElbow_ctrl")
                    IkLeftArmDistance_sl_ls.add("IkNoFlipLeftForeArm_translateY")
                    IkLeftArmDistance_sl_ls.add("IkNoFlipLeftHand_translateY")

                    likelbowDist_fs = om2.MFnDependencyNode(likelbowdistloc_tn)
                    likhandDist_fs = om2.MFnDependencyNode(likhanddistloc2_tn)
                    likupperarmjntDist_fs = om2.MFnDependencyNode(IkLeftArmDistance_sl_ls.getDependNode(1))
                    liklowerarmjntDist_fs = om2.MFnDependencyNode(IkLeftArmDistance_sl_ls.getDependNode(2))
                    pvleftelbowkey_fs = om2.MFnDependencyNode(IkLeftArmDistance_sl_ls.getDependNode(3))
                    pvlefthandkey_fs = om2.MFnDependencyNode(IkLeftArmDistance_sl_ls.getDependNode(4))
                    pvleftelbowctrlDecomposeMatrix_fs = om2.MFnDependencyNode(pvleftelbowctrl_decomposeMatrix)
                    likpvupperarmtransblendnode_fs = om2.MFnDependencyNode(likpvupperarmtransblendnode)
                    likpvlowerarmtransblendnode_fs = om2.MFnDependencyNode(likpvlowerarmtransblendnode)
                    pvleftelbowctrl_fs = om2.MFnDependencyNode(IkLeftArmDistance_sl_ls.getDependNode(5))
                    pvleftelbowjnt_fs = om2.MFnDependencyNode(pviklarm_sl_ls.getDependNode(1))
                    pvlefthandjnt_fs = om2.MFnDependencyNode(pviklarm_sl_ls.getDependNode(2))
                    likupperarmstretchblendnode_fs = om2.MFnDependencyNode(likpvupperarmstretchblendnode)
                    liklowerarmstretchblendnode_fs = om2.MFnDependencyNode(likpvlowerarmstretchblendnode)
                    lefthandoption_fs = om2.MFnDependencyNode(obj_stretchyleftarm2)

                    likupperarmjntDistPoint2_plug = likupperarmjntDist_fs.findPlug("endPoint", False)
                    liklowerarmjntDistPoint1_plug = liklowerarmjntDist_fs.findPlug("startPoint", False)
                    liklowerarmjntDistPoint2_plug = liklowerarmjntDist_fs.findPlug("endPoint", False)
                    likelbowDistOtpTrans_plug = likelbowDist_fs.findPlug("translate", False)
                    likhandDistOtpTrans_plug = likhandDist_fs.findPlug("translate", False)
                    pvleftelbowctrlDecomposeMatrixOtpTrans_plug = pvleftelbowctrlDecomposeMatrix_fs.findPlug("outputTranslate", False)
                    pvleftelbowkeyotp_plug = pvleftelbowkey_fs.findPlug("output", False)
                    pvlefthandkeyotp_plug = pvlefthandkey_fs.findPlug("output", False)
                    likpvupperarmtransblendnodeinp1g_plug = likpvupperarmtransblendnode_fs.findPlug("color1G", False)
                    likpvupperarmtransblendnodeinp2g_plug = likpvupperarmtransblendnode_fs.findPlug("color2G", False)
                    likpvupperarmtransblendnodeotp_plug = likpvupperarmtransblendnode_fs.findPlug("outputG", False)
                    likpvupperarmtransblendnodeblender_plug = likpvupperarmtransblendnode_fs.findPlug("blender", False)
                    likpvlowerarmtransblendnodeinp1g_plug = likpvlowerarmtransblendnode_fs.findPlug("color1G", False)
                    likpvlowerarmtransblendnodeinp2g_plug = likpvlowerarmtransblendnode_fs.findPlug("color2G", False)
                    likpvlowerarmtransblendnodeotp_plug = likpvlowerarmtransblendnode_fs.findPlug("outputG", False)
                    likpvlowerarmtransblendnodeblender_plug = likpvlowerarmtransblendnode_fs.findPlug("blender", False)
                    pvleftelbowctrl_fs_plug = pvleftelbowctrl_fs.findPlug("elbowsnap", False)
                    likpvupperarmstretchblendnodeinp1g_plug = likupperarmstretchblendnode_fs.findPlug("color1G", False)
                    likpvupperarmstretchblendnodeotp_plug = likupperarmstretchblendnode_fs.findPlug("outputG", False)
                    likpvupperarmstretchblendnodeblender_plug = likupperarmstretchblendnode_fs.findPlug("blender", False)
                    likpvlowerarmstretchblendnodeinp1g_plug = liklowerarmstretchblendnode_fs.findPlug("color1G", False)
                    likpvlowerarmstretchblendnodeotp_plug = liklowerarmstretchblendnode_fs.findPlug("outputG", False)
                    likpvlowerarmstretchblendnodeblender_plug = liklowerarmstretchblendnode_fs.findPlug("blender", False)
                    iklefthandstretch_plug = lefthandoption_fs.findPlug("stretchable", False)
                    pvleftelbowjntTrans_plug = pvleftelbowjnt_fs.findPlug("translateY", False)
                    pvlefthandjntTrans_plug = pvlefthandjnt_fs.findPlug("translateY", False)

                    self.MDG2_mod.commandToExecute('connectAttr -force L_uparm2_Shape.worldPosition[0] LeftUpperArmDistance_InfoShape.startPoint')
                    self.MDG2_mod.commandToExecute('connectAttr -force Biped_PVLeftElbow_ctrl.worldMatrix[0] PVLeftElbow_decomposeMatrix.inputMatrix')
                    self.MDG2_mod.connect(likelbowDistOtpTrans_plug, likupperarmjntDistPoint2_plug)
                    self.MDG2_mod.connect(likelbowDistOtpTrans_plug, liklowerarmjntDistPoint1_plug)
                    self.MDG2_mod.connect(likhandDistOtpTrans_plug, liklowerarmjntDistPoint2_plug)
                    self.MDG2_mod.connect(likhanddecomposeOtpTrans_plug, likhandDistOtpTrans_plug)
                    self.MDG2_mod.connect(pvleftelbowctrlDecomposeMatrixOtpTrans_plug, likelbowDistOtpTrans_plug)

                    self.MDG2_mod.disconnect(pvleftelbowkeyotp_plug, pvleftelbowjntTrans_plug)
                    self.MDG2_mod.disconnect(pvlefthandkeyotp_plug, pvlefthandjntTrans_plug)
                    self.MDG2_mod.connect(pvleftelbowkeyotp_plug, likpvupperarmtransblendnodeinp2g_plug)
                    self.MDG2_mod.connect(pvlefthandkeyotp_plug, likpvlowerarmtransblendnodeinp2g_plug)
                    self.MDG2_mod.connect(pvleftelbowctrl_fs_plug, likpvupperarmtransblendnodeblender_plug)
                    self.MDG2_mod.connect(pvleftelbowctrl_fs_plug, likpvlowerarmtransblendnodeblender_plug)
                    self.MDG2_mod.connect(likpvupperarmtransblendnodeotp_plug, likpvupperarmstretchblendnodeinp1g_plug)
                    self.MDG2_mod.connect(likpvlowerarmtransblendnodeotp_plug, likpvlowerarmstretchblendnodeinp1g_plug)
                    self.MDG2_mod.connect(likpvupperarmstretchblendnodeotp_plug, pvleftelbowjntTrans_plug)
                    self.MDG2_mod.connect(likpvlowerarmstretchblendnodeotp_plug, pvlefthandjntTrans_plug)
                    self.MDG2_mod.connect(iklefthandstretch_plug, likpvupperarmstretchblendnodeblender_plug)
                    self.MDG2_mod.connect(iklefthandstretch_plug, likpvlowerarmstretchblendnodeblender_plug)
                    self.MDG2_mod.commandToExecute('float $pvikleftforearmtranslateY = `getAttr "PVLeftUpperArmStretch_blend.color1G"`; setAttr "PVLeftUpperArmStretch_blend.color2G" $pvikleftforearmtranslateY;')
                    self.MDG2_mod.commandToExecute('float $pviklefthandtranslateY = `getAttr "PVLeftLowerArmStretch_blend.color1G"`; setAttr "PVLeftLowerArmStretch_blend.color2G" $pviklefthandtranslateY;')
                    self.MDG2_mod.commandToExecute('parent "distloc_L_legelbow" "DoNotTouch"')
                    self.MDG2_mod.commandToExecute('parent "distloc_L_leghand2" "DoNotTouch"')
                    self.MDG2_mod.commandToExecute('parent "LeftUpperArmDistance_Info" "DoNotTouch"')
                    self.MDG2_mod.commandToExecute('parent "LeftLowerArmDistance_Info" "DoNotTouch"')

                    self.MDG2_mod.commandToExecute('addAttr -longName "forearmlength" -niceName "AutoElbow ForeArm Length" -attributeType double -minValue 0 -keyable true -defaultValue 1 Biped_IkLeftHand_ctrl')
                    self.MDG2_mod.commandToExecute('addAttr -longName "wristlength" -niceName "AutoElbow Wrist Length" -attributeType double -minValue 0 -keyable true -defaultValue 1 Biped_IkLeftHand_ctrl')
                    self.MDG2_mod.doIt()

                    likautokneeupperlegnode = self.MDG2_mod.createNode("multiplyDivide")
                    likautokneelowerlegnode = self.MDG2_mod.createNode("multiplyDivide")
                    liknoflipupperarmtransblendnode = self.MDG2_mod.createNode("blendColors")
                    liknofliplowerarmtransblendnode = self.MDG2_mod.createNode("blendColors")
                    self.MDG2_mod.renameNode(likautokneeupperlegnode, "NoFlipLeftForeArmTrans_multiply")
                    self.MDG2_mod.renameNode(likautokneelowerlegnode, "NoFlipLeftHandTrans_multiply")
                    self.MDG2_mod.renameNode(liknoflipupperarmtransblendnode, "NoFlipLeftUpperArmStretch_blend")
                    self.MDG2_mod.renameNode(liknofliplowerarmtransblendnode, "NoFlipLeftLowerArmStretch_blend")

                    likautoelbowupperleg_fs = om2.MFnDependencyNode(likautokneeupperlegnode)
                    likautoelbowlowerleg_fs = om2.MFnDependencyNode(likautokneelowerlegnode)
                    noflipleftelbowkey_fs = om2.MFnDependencyNode(IkLeftArmDistance_sl_ls.getDependNode(6))
                    nofliplefthandkey_fs = om2.MFnDependencyNode(IkLeftArmDistance_sl_ls.getDependNode(7))
                    nofliplefelbowjntTrans_fs = om2.MFnDependencyNode(noflipiklarm_sl_ls.getDependNode(1))
                    nofliplefthandjntTrans_fs = om2.MFnDependencyNode(noflipiklarm_sl_ls.getDependNode(2))
                    liknoflipupperarmstretchblendnode_fs = om2.MFnDependencyNode(liknoflipupperarmtransblendnode)
                    liknofliplowerarmstretchblendnode_fs = om2.MFnDependencyNode(liknofliplowerarmtransblendnode)

                    ikautoelbowupperarmInp1Y_plug = likautoelbowupperleg_fs.findPlug("input1Y", False)
                    ikautoelbowupperarmInp2Y_plug = likautoelbowupperleg_fs.findPlug("input2Y", False)
                    likautoelbowupperarmOtp_plug = likautoelbowupperleg_fs.findPlug("outputY", False)
                    ikautoelbowlowerarmInp1Y_plug = likautoelbowlowerleg_fs.findPlug("input1Y", False)
                    ikautoelbowlowerarmInp2Y_plug = likautoelbowlowerleg_fs.findPlug("input2Y", False)
                    likautoelbowlowerarmOtp_plug = likautoelbowlowerleg_fs.findPlug("outputY", False)
                    noflipleftelbowkeyotp_plug = noflipleftelbowkey_fs.findPlug("output", False)
                    nofliplefthandkeyotp_plug = nofliplefthandkey_fs.findPlug("output", False)
                    noflipleftelbowjnttty_plug = nofliplefelbowjntTrans_fs.findPlug("translateY", False)
                    nofliplefthandjntty_plug = nofliplefthandjntTrans_fs.findPlug("translateY", False)
                    likctrlelbowupperarm_plug = ikarmctrl_fs.findPlug("forearmlength", False)
                    likctrlelbowlowerarm_plug = ikarmctrl_fs.findPlug("wristlength", False)
                    liknoflipupperarmstretchblendnodeinp1g_plug = liknoflipupperarmstretchblendnode_fs.findPlug("color1G", False)
                    liknoflipupperarmstretchblendnodeotp_plug = liknoflipupperarmstretchblendnode_fs.findPlug("outputG", False)
                    liknoflipupperarmstretchblendnodeblender_plug = liknoflipupperarmstretchblendnode_fs.findPlug("blender", False)
                    liknofliplowerarmstretchblendnodeinp1g_plug = liknofliplowerarmstretchblendnode_fs.findPlug("color1G", False)
                    liknofliplowerarmstretchblendnodeotp_plug = liknofliplowerarmstretchblendnode_fs.findPlug("outputG", False)
                    liknofliplowerarmstretchblendnodeblender_plug = liknofliplowerarmstretchblendnode_fs.findPlug("blender", False)

                    self.MDG2_mod.disconnect(noflipleftelbowkeyotp_plug, noflipleftelbowjnttty_plug)
                    self.MDG2_mod.disconnect(nofliplefthandkeyotp_plug, nofliplefthandjntty_plug)
                    self.MDG2_mod.connect(likctrlelbowupperarm_plug, ikautoelbowupperarmInp1Y_plug)
                    self.MDG2_mod.connect(noflipleftelbowkeyotp_plug, ikautoelbowupperarmInp2Y_plug)
                    self.MDG2_mod.connect(likctrlelbowlowerarm_plug, ikautoelbowlowerarmInp1Y_plug)
                    self.MDG2_mod.connect(nofliplefthandkeyotp_plug, ikautoelbowlowerarmInp2Y_plug)
                    self.MDG2_mod.connect(likautoelbowupperarmOtp_plug, liknoflipupperarmstretchblendnodeinp1g_plug)
                    self.MDG2_mod.connect(likautoelbowlowerarmOtp_plug, liknofliplowerarmstretchblendnodeinp1g_plug)
                    self.MDG2_mod.connect(liknoflipupperarmstretchblendnodeotp_plug, noflipleftelbowjnttty_plug)
                    self.MDG2_mod.connect(liknofliplowerarmstretchblendnodeotp_plug, nofliplefthandjntty_plug)
                    self.MDG2_mod.connect(iklefthandstretch_plug, liknoflipupperarmstretchblendnodeblender_plug)
                    self.MDG2_mod.connect(iklefthandstretch_plug, liknofliplowerarmstretchblendnodeblender_plug)
                    self.MDG2_mod.commandToExecute('float $noflipikleftforearmtranslateY = `getAttr "NoFlipLeftUpperArmStretch_blend.color1G"`; setAttr "NoFlipLeftUpperArmStretch_blend.color2G" $noflipikleftforearmtranslateY;')
                    self.MDG2_mod.commandToExecute('float $noflipiklefthandtranslateY = `getAttr "NoFlipLeftLowerArmStretch_blend.color1G"`; setAttr "NoFlipLeftLowerArmStretch_blend.color2G" $noflipiklefthandtranslateY;')
                    self.MDG2_mod.commandToExecute('setAttr "NoFlipLeftForeArmTrans_multiply.operation" 1')
                    self.MDG2_mod.commandToExecute('setAttr "NoFlipLeftHandTrans_multiply.operation" 1')

                    leftarmlobalscalenode = self.MDG2_mod.createNode("multiplyDivide")
                    noflipleftlegglobalscalenode = self.MDG2_mod.createNode("multiplyDivide")
                    noflipleftfootlobalscalenode = self.MDG2_mod.createNode("multiplyDivide")
                    self.MDG2_mod.renameNode(leftarmlobalscalenode, "IKLeftArmGlobalScale_Average")
                    self.MDG2_mod.renameNode(noflipleftlegglobalscalenode, "IKNoFlipLeftForeArmGlobalScale_Average")
                    self.MDG2_mod.renameNode(noflipleftfootlobalscalenode, "IKNoFlipLeftHandGlobalScale_Average")

                    leftarmglobalscale_fs = om2.MFnDependencyNode(leftarmlobalscalenode)
                    noflipleftarmglobalscale_fs = om2.MFnDependencyNode(noflipleftlegglobalscalenode)
                    nofliplefthandlobalscale_fs = om2.MFnDependencyNode(noflipleftfootlobalscalenode)
                    masterlctrl_fs = om2.MFnDependencyNode(obj_masterctrl2)

                    likupperarmjntDist_plug = likupperarmjntDist_fs.findPlug("distance", False)
                    liklowerarmjntDist_plug = liklowerarmjntDist_fs.findPlug("distance", False)
                    likarmjntDist_plug = likarmjntDist_fs.findPlug("distance", False)
                    masterlctrlsy_plug = masterlctrl_fs.findPlug("scaleY", False)
                    leftarmglobalscaleInp1Y_plug = leftarmglobalscale_fs.findPlug("input1Y", False)
                    leftarmglobalscaleInp2Y_plug = leftarmglobalscale_fs.findPlug("input2Y", False)
                    leftarmglobalscaleOtpY_plug = leftarmglobalscale_fs.findPlug("outputY", False)
                    noflipleftarmglobalscaleInp1Y_plug = noflipleftarmglobalscale_fs.findPlug("input1Y", False)
                    noflipleftarmglobalscaleInp2Y_plug = noflipleftarmglobalscale_fs.findPlug("input2Y", False)
                    noflipleftarmglobalscaleOtpY_plug = noflipleftarmglobalscale_fs.findPlug("outputY", False)
                    nofliplefthandlobalscaleInp1Y_plug = nofliplefthandlobalscale_fs.findPlug("input1Y", False)
                    nofliplefthandlobalscaleInp2Y_plug = nofliplefthandlobalscale_fs.findPlug("input2Y", False)
                    nofliplefthandlobalscaleOtpY_plug = nofliplefthandlobalscale_fs.findPlug("outputY", False)
                    noflipleftelbowkeyinp_plug = noflipleftelbowkey_fs.findPlug("input", False)
                    nofliplefthandkeyinp_plug = nofliplefthandkey_fs.findPlug("input", False)
                    pvleftelbowkeyinp_plug = pvleftelbowkey_fs.findPlug("input", False)
                    pvlefthandkeyinp_plug = pvlefthandkey_fs.findPlug("input", False)

                    self.MDG2_mod.disconnect(likarmjntDist_plug, noflipleftelbowkeyinp_plug)
                    self.MDG2_mod.disconnect(likarmjntDist_plug, nofliplefthandkeyinp_plug)
                    self.MDG2_mod.disconnect(likarmjntDist_plug, pvleftelbowkeyinp_plug)
                    self.MDG2_mod.disconnect(likarmjntDist_plug, pvlefthandkeyinp_plug)
                    self.MDG2_mod.connect(liklowerarmjntDist_plug, nofliplefthandlobalscaleInp1Y_plug)
                    self.MDG2_mod.connect(likupperarmjntDist_plug, noflipleftarmglobalscaleInp1Y_plug)
                    self.MDG2_mod.connect(liklowerarmjntDist_plug, nofliplefthandlobalscaleInp1Y_plug)
                    self.MDG2_mod.connect(masterlctrlsy_plug, noflipleftarmglobalscaleInp2Y_plug)
                    self.MDG2_mod.connect(masterlctrlsy_plug, nofliplefthandlobalscaleInp2Y_plug)
                    self.MDG2_mod.connect(noflipleftarmglobalscaleOtpY_plug, likpvupperarmtransblendnodeinp1g_plug)
                    self.MDG2_mod.connect(nofliplefthandlobalscaleOtpY_plug, likpvlowerarmtransblendnodeinp1g_plug)
                    self.MDG2_mod.connect(likarmjntDist_plug, leftarmglobalscaleInp1Y_plug)
                    self.MDG2_mod.connect(masterlctrlsy_plug, leftarmglobalscaleInp2Y_plug)
                    self.MDG2_mod.connect(leftarmglobalscaleOtpY_plug, noflipleftelbowkeyinp_plug)
                    self.MDG2_mod.connect(leftarmglobalscaleOtpY_plug, nofliplefthandkeyinp_plug)
                    self.MDG2_mod.connect(leftarmglobalscaleOtpY_plug, pvleftelbowkeyinp_plug)
                    self.MDG2_mod.connect(leftarmglobalscaleOtpY_plug, pvlefthandkeyinp_plug)
                    self.MDG2_mod.commandToExecute('setAttr "IKNoFlipLeftForeArmGlobalScale_Average.operation" 2')
                    self.MDG2_mod.commandToExecute('setAttr "IKNoFlipLeftHandGlobalScale_Average.operation" 2')
                    self.MDG2_mod.commandToExecute('setAttr "IKLeftArmGlobalScale_Average.operation" 2')

                # else:
                #     self.MDG2_mod.commandToExecute('delete "IkStretchyLeftJointArm_grp"')
                #     self.MDG2_mod.commandToExecute('delete "LeftArmIkCluster_grp"')
        else:
            self.MDG2_mod.commandToExecute('delete "Biped_IkLeftHand_null"')
            self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false Biped_LeftHandOptions_ctrl.fkik')
            self.MDG2_mod.commandToExecute('setAttr "IkLeftArm.visibility" 0')

        lfinger_sl_ls = om2.MSelectionList()
        lfinger_sl_ls.add("LeftFinger*")

        for index in range(lfinger_sl_ls.length()):
            jnt_obj = lfinger_sl_ls.getDependNode(index)
            jnt_string = lfinger_sl_ls.getSelectionStrings(index)

            if jnt_obj.hasFn(om2.MFn.kJoint):
                lfingerctrl_multMatrix = self.MDG2_mod.createNode("multMatrix")
                lfingerctrl_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                self.MDG2_mod.renameNode(lfingerctrl_multMatrix, str(jnt_string)[2:][:-3] + "_multMatrix")
                self.MDG2_mod.renameNode(lfingerctrl_decomposeMatrix, str(jnt_string)[2:][:-3] + "_decomposeMatrix")

                lfingermultMatrix_fs = om2.MFnDependencyNode(lfingerctrl_multMatrix)
                lfingerdecomposeMatrix_fs = om2.MFnDependencyNode(lfingerctrl_decomposeMatrix)
                lfingerjnt_fs = om2.MFnDependencyNode(jnt_obj)

                lfingermultMatrixSum_plug = lfingermultMatrix_fs.findPlug("matrixSum", False)
                lfingerdecomposeInpMatrix_plug = lfingerdecomposeMatrix_fs.findPlug("inputMatrix", False)
                lfingerdecomposeOtpTrans_plug = lfingerdecomposeMatrix_fs.findPlug("outputTranslate", False)
                lfingerdecomposeOtpRot_plug = lfingerdecomposeMatrix_fs.findPlug("outputRotate", False)
                lfingerjntTrans_plug = lfingerjnt_fs.findPlug("translate", False)
                lfingerjntRot_plug = lfingerjnt_fs.findPlug("rotate", False)

                self.MDG2_mod.commandToExecute('connectAttr -force Biped_{0}_ctrl.worldMatrix[0] {0}_multMatrix.matrixIn[0]'.format(str(jnt_string)[3:][:-3]))
                self.MDG2_mod.commandToExecute('connectAttr -force {0}.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(jnt_string)[3:][:-3]))
                self.MDG2_mod.connect(lfingermultMatrixSum_plug, lfingerdecomposeInpMatrix_plug)
                self.MDG2_mod.connect(lfingerdecomposeOtpTrans_plug, lfingerjntTrans_plug)
                self.MDG2_mod.connect(lfingerdecomposeOtpRot_plug, lfingerjntRot_plug)
                if cmds.getAttr("{0}.jointOrientX".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientY".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientZ".format(str(jnt_string)[3:][:-3])) != 0:
                    self.MDG2_mod.commandToExecute('setAttr "{0}.jointOrientX" 0'.format(str(jnt_string)[3:][:-3]))
                    self.MDG2_mod.commandToExecute('setAttr "{0}.jointOrientY" 0'.format(str(jnt_string)[3:][:-3]))
                    self.MDG2_mod.commandToExecute('setAttr "{0}.jointOrientZ" 0'.format(str(jnt_string)[3:][:-3]))

                if cmds.objExists("Biped_{0}4_ctrl".format(str(jnt_string)[3:][:-4])):
                    self.MDG2_mod.commandToExecute('setAttr "Biped_{0}4_ctrl.visibility" 0'.format(str(jnt_string)[3:][:-4]))

        self.MDG2_mod.commandToExecute('addAttr -longName "curl" -niceName "Curl" -attributeType double -keyable true -minValue -10 -maxValue 10 -defaultValue 0 Biped_LeftFingerOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "spread" -niceName "Spread" -attributeType double -keyable true -defaultValue 0 Biped_LeftFingerOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "relax" -niceName "Relax" -attributeType double -minValue -10 -maxValue 10 -keyable true -defaultValue 0 Biped_LeftFingerOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "curl" -niceName "Curl" -attributeType double -keyable true -minValue -10 -maxValue 10 -defaultValue 0 Biped_LeftThumbOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "curl" -niceName "Curl" -attributeType double -keyable true -minValue -10 -maxValue 10 -defaultValue 0 Biped_LeftIndexOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "curl" -niceName "Curl" -attributeType double -keyable true -minValue -10 -maxValue 10 -defaultValue 0 Biped_LeftMiddleOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "curl" -niceName "Curl" -attributeType double -keyable true -minValue -10 -maxValue 10 -defaultValue 0 Biped_LeftRingOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "curl" -niceName "Curl" -attributeType double -keyable true -minValue -10 -maxValue 10 -defaultValue 0 Biped_LeftPinkyOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "lean" -niceName "Lean" -attributeType double -keyable true -defaultValue 0 Biped_LeftThumbOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "lean" -niceName "Lean" -attributeType double -keyable true -defaultValue 0 Biped_LeftIndexOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "lean" -niceName "Lean" -attributeType double -keyable true -defaultValue 0 Biped_LeftMiddleOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "lean" -niceName "Lean" -attributeType double -keyable true -defaultValue 0 Biped_LeftRingOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "lean" -niceName "Lean" -attributeType double -keyable true -defaultValue 0 Biped_LeftPinkyOptions_ctrl')
        self.MDG2_mod.doIt()

        lfingercurl_sl_ls = om2.MSelectionList()
        lfingercurl_sl_ls.add("Biped_LeftFinger*_curl")

        self.MDG2_mod.commandToExecute('float $leftfingeroptionsspread = `getAttr "Biped_LeftFingerOptions_ctrl.spread"`; float $leftfingerthumbrotateZ = `getAttr "Biped_LeftFingerThumb1_globalcurl.rotateZ"`; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.spread -driverValue $leftfingeroptionsspread -attribute "rotateZ" -value $leftfingerthumbrotateZ Biped_LeftFingerThumb1_globalcurl;')
        self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 20.0; float $leftfingeroptionsspread = `getAttr "Biped_LeftFingerOptions_ctrl.spread"`; float $leftfingerthumbrotateZ = `getAttr "Biped_LeftFingerThumb1_globalcurl.rotateZ"`; float $totalleftfingeroptionsspread = $leftfingeroptionsspread + $add1; float $totalleftthumbrotateZ = $leftfingerthumbrotateZ + $add2; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.spread -driverValue $totalleftfingeroptionsspread -attribute "rotateZ" -value $totalleftthumbrotateZ Biped_LeftFingerThumb1_globalcurl;')
        self.MDG2_mod.commandToExecute('float $leftfingeroptionsspread = `getAttr "Biped_LeftFingerOptions_ctrl.spread"`; float $leftfingerindexrotateZ = `getAttr "Biped_LeftFingerIndex1_globalcurl.rotateZ"`; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.spread -driverValue $leftfingeroptionsspread -attribute "rotateZ" -value $leftfingerindexrotateZ Biped_LeftFingerIndex1_globalcurl;')
        self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 10.0; float $leftfingeroptionsspread = `getAttr "Biped_LeftFingerOptions_ctrl.spread"`; float $leftfingerindexrotateZ = `getAttr "Biped_LeftFingerIndex1_globalcurl.rotateZ"`; float $totalleftfingeroptionsspread = $leftfingeroptionsspread + $add1; float $totalleftindexrotateZ = $leftfingerindexrotateZ + $add2; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.spread -driverValue $totalleftfingeroptionsspread -attribute "rotateZ" -value $totalleftindexrotateZ Biped_LeftFingerIndex1_globalcurl;')
        self.MDG2_mod.commandToExecute('float $leftfingeroptionsspread = `getAttr "Biped_LeftFingerOptions_ctrl.spread"`; float $leftfingermiddlerotateZ = `getAttr "Biped_LeftFingerMiddle1_globalcurl.rotateZ"`; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.spread -driverValue $leftfingeroptionsspread -attribute "rotateZ" -value $leftfingermiddlerotateZ Biped_LeftFingerMiddle1_globalcurl;')
        self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 2.0; float $leftfingeroptionsspread = `getAttr "Biped_LeftFingerOptions_ctrl.spread"`; float $leftfingermiddlerotateZ = `getAttr "Biped_LeftFingerMiddle1_globalcurl.rotateZ"`; float $totalleftfingeroptionsspread = $leftfingeroptionsspread + $add1; float $totalleftmiddlerotateZ = $leftfingermiddlerotateZ + $add2; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.spread -driverValue $totalleftfingeroptionsspread -attribute "rotateZ" -value $totalleftmiddlerotateZ Biped_LeftFingerMiddle1_globalcurl;')
        self.MDG2_mod.commandToExecute('float $leftfingeroptionsspread = `getAttr "Biped_LeftFingerOptions_ctrl.spread"`; float $leftfingerringrotateZ = `getAttr "Biped_LeftFingerRing1_globalcurl.rotateZ"`; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.spread -driverValue $leftfingeroptionsspread -attribute "rotateZ" -value $leftfingerringrotateZ Biped_LeftFingerRing1_globalcurl;')
        self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = -8.0; float $leftfingeroptionsspread = `getAttr "Biped_LeftFingerOptions_ctrl.spread"`; float $leftfingerringrotateZ = `getAttr "Biped_LeftFingerRing1_globalcurl.rotateZ"`; float $totalleftfingeroptionsspread = $leftfingeroptionsspread + $add1; float $totalleftringrotateZ = $leftfingerringrotateZ + $add2; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.spread -driverValue $totalleftfingeroptionsspread -attribute "rotateZ" -value $totalleftringrotateZ Biped_LeftFingerRing1_globalcurl;')
        self.MDG2_mod.commandToExecute('float $leftfingeroptionsspread = `getAttr "Biped_LeftFingerOptions_ctrl.spread"`; float $leftfingerpinkyrotateZ = `getAttr "Biped_LeftFingerPinky1_globalcurl.rotateZ"`; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.spread -driverValue $leftfingeroptionsspread -attribute "rotateZ" -value $leftfingerpinkyrotateZ Biped_LeftFingerPinky1_globalcurl;')
        self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = -15.0; float $leftfingeroptionsspread = `getAttr "Biped_LeftFingerOptions_ctrl.spread"`; float $leftfingerpinkyrotateZ = `getAttr "Biped_LeftFingerPinky1_globalcurl.rotateZ"`; float $totalleftfingeroptionsspread = $leftfingeroptionsspread + $add1; float $totalleftpinkyrotateZ = $leftfingerpinkyrotateZ + $add2; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.spread -driverValue $totalleftfingeroptionsspread -attribute "rotateZ" -value $totalleftpinkyrotateZ Biped_LeftFingerPinky1_globalcurl;')

        for index in range(lfingercurl_sl_ls.length()):
            lfingercurl_obj = lfingercurl_sl_ls.getDependNode(index)
            lfingercurl_string = lfingercurl_sl_ls.getSelectionStrings(index)

            if lfingercurl_obj.hasFn(om2.MFn.kTransform):
                self.MDG2_mod.commandToExecute('connectAttr -force Biped_Left{0}Options_ctrl.curl Biped_LeftFinger{1}_curl.rotateX'.format(str(lfingercurl_string)[19:][:-9], str(lfingercurl_string)[19:][:-8]))
                self.MDG2_mod.commandToExecute('connectAttr -force Biped_Left{0}Options_ctrl.lean Biped_LeftFinger{1}_curl.rotateZ'.format(str(lfingercurl_string)[19:][:-9], str(lfingercurl_string)[19:][:-8]))
                # self.MDG2_mod.commandToExecute('connectAttr -force Biped_LeftFingerOptions_ctrl.curl Biped_LeftFinger{1}_globalcurl.rotateX'.format(str(lfingercurl_string)[19:][:-9], str(lfingercurl_string)[19:][:-8]))

            for index in range(1,5):
                self.MDG2_mod.commandToExecute('float $leftfingeroptionscurl = `getAttr "Biped_LeftFingerOptions_ctrl.curl"`; float $leftfingerindexrotateX = `getAttr "Biped_LeftFingerIndex{0}_globalcurl.rotateX"`; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.curl -driverValue $leftfingeroptionscurl -attribute "rotateX" -value $leftfingerindexrotateX Biped_LeftFingerIndex{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 90.0; float $leftfingeroptionscurl = `getAttr "Biped_LeftFingerOptions_ctrl.curl"`; float $leftfingerindexrotateX = `getAttr "Biped_LeftFingerIndex{0}_globalcurl.rotateX"`; float $totalleftfingeroptionscurl = $leftfingeroptionscurl + $add1; float $totalleftindexrotateX = $leftfingerindexrotateX + $add2; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.curl -driverValue $totalleftfingeroptionscurl -attribute "rotateX" -value $totalleftindexrotateX Biped_LeftFingerIndex{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = -10.0; float $add2 = -90.0; float $leftfingeroptionscurl = `getAttr "Biped_LeftFingerOptions_ctrl.curl"`; float $leftfingerindexrotateX = `getAttr "Biped_LeftFingerIndex{0}_globalcurl.rotateX"`; float $totalleftfingeroptionscurl = $leftfingeroptionscurl + $add1; float $totalleftindexrotateX = $leftfingerindexrotateX + $add2; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.curl -driverValue $totalleftfingeroptionscurl -attribute "rotateX" -value $totalleftindexrotateX Biped_LeftFingerIndex{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $leftfingeroptionscurl = `getAttr "Biped_LeftFingerOptions_ctrl.curl"`; float $leftfingermiddlerotateX = `getAttr "Biped_LeftFingerMiddle{0}_globalcurl.rotateX"`; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.curl -driverValue $leftfingeroptionscurl -attribute "rotateX" -value $leftfingermiddlerotateX Biped_LeftFingerMiddle{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 90.0; float $leftfingeroptionscurl = `getAttr "Biped_LeftFingerOptions_ctrl.curl"`; float $leftfingermiddlerotateX = `getAttr "Biped_LeftFingerMiddle{0}_globalcurl.rotateX"`; float $totalleftfingeroptionscurl = $leftfingeroptionscurl + $add1; float $totalleftmiddlerotateX = $leftfingermiddlerotateX + $add2; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.curl -driverValue $totalleftfingeroptionscurl -attribute "rotateX" -value $totalleftmiddlerotateX Biped_LeftFingerMiddle{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = -10.0; float $add2 = -90.0; float $leftfingeroptionscurl = `getAttr "Biped_LeftFingerOptions_ctrl.curl"`; float $leftfingermiddlerotateX = `getAttr "Biped_LeftFingerMiddle{0}_globalcurl.rotateX"`; float $totalleftfingeroptionscurl = $leftfingeroptionscurl + $add1; float $totalleftmiddlerotateX = $leftfingermiddlerotateX + $add2; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.curl -driverValue $totalleftfingeroptionscurl -attribute "rotateX" -value $totalleftmiddlerotateX Biped_LeftFingerMiddle{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $leftfingeroptionscurl = `getAttr "Biped_LeftFingerOptions_ctrl.curl"`; float $leftfingerringrotateX = `getAttr "Biped_LeftFingerRing{0}_globalcurl.rotateX"`; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.curl -driverValue $leftfingeroptionscurl -attribute "rotateX" -value $leftfingerringrotateX Biped_LeftFingerRing{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 90.0; float $leftfingeroptionscurl = `getAttr "Biped_LeftFingerOptions_ctrl.curl"`; float $leftfingerringrotateX = `getAttr "Biped_LeftFingerRing{0}_globalcurl.rotateX"`; float $totalleftfingeroptionscurl = $leftfingeroptionscurl + $add1; float $totalleftringrotateX = $leftfingerringrotateX + $add2; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.curl -driverValue $totalleftfingeroptionscurl -attribute "rotateX" -value $totalleftringrotateX Biped_LeftFingerRing{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = -10.0; float $add2 = -90.0; float $leftfingeroptionscurl = `getAttr "Biped_LeftFingerOptions_ctrl.curl"`; float $leftfingerringrotateX = `getAttr "Biped_LeftFingerRing{0}_globalcurl.rotateX"`; float $totalleftfingeroptionscurl = $leftfingeroptionscurl + $add1; float $totalleftringrotateX = $leftfingerringrotateX + $add2; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.curl -driverValue $totalleftfingeroptionscurl -attribute "rotateX" -value $totalleftringrotateX Biped_LeftFingerRing{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $leftfingeroptionscurl = `getAttr "Biped_LeftFingerOptions_ctrl.curl"`; float $leftfingerpinkyrotateX = `getAttr "Biped_LeftFingerPinky{0}_globalcurl.rotateX"`; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.curl -driverValue $leftfingeroptionscurl -attribute "rotateX" -value $leftfingerpinkyrotateX Biped_LeftFingerPinky{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 90.0; float $leftfingeroptionscurl = `getAttr "Biped_LeftFingerOptions_ctrl.curl"`; float $leftfingerpinkyrotateX = `getAttr "Biped_LeftFingerPinky{0}_globalcurl.rotateX"`; float $totalleftfingeroptionscurl = $leftfingeroptionscurl + $add1; float $totalleftpinkyrotateX = $leftfingerpinkyrotateX + $add2; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.curl -driverValue $totalleftfingeroptionscurl -attribute "rotateX" -value $totalleftpinkyrotateX Biped_LeftFingerPinky{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = -10.0; float $add2 = -90.0; float $leftfingeroptionscurl = `getAttr "Biped_LeftFingerOptions_ctrl.curl"`; float $leftfingerpinkyrotateX = `getAttr "Biped_LeftFingerPinky{0}_globalcurl.rotateX"`; float $totalleftfingeroptionscurl = $leftfingeroptionscurl + $add1; float $totalleftpinkyrotateX = $leftfingerpinkyrotateX + $add2; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.curl -driverValue $totalleftfingeroptionscurl -attribute "rotateX" -value $totalleftpinkyrotateX Biped_LeftFingerPinky{0}_globalcurl;'.format(index))

                self.MDG2_mod.commandToExecute('float $leftfingeroptionsrelax = `getAttr "Biped_LeftFingerOptions_ctrl.relax"`; float $leftfingerindexrotateX = `getAttr "Biped_LeftFingerIndex{0}_globalcurl.rotateX"`; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.relax -driverValue $leftfingeroptionsrelax -attribute "rotateX" -value $leftfingerindexrotateX Biped_LeftFingerIndex{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 15.0; float $leftfingeroptionsrelax = `getAttr "Biped_LeftFingerOptions_ctrl.relax"`; float $leftfingerindexrotateX = `getAttr "Biped_LeftFingerIndex{0}_globalcurl.rotateX"`; float $totalleftfingeroptionsrelax = $leftfingeroptionsrelax + $add1; float $totalleftindexrotateX = $leftfingerindexrotateX + $add2; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.relax -driverValue $totalleftfingeroptionsrelax -attribute "rotateX" -value $totalleftindexrotateX Biped_LeftFingerIndex{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = -10.0; float $add2 = 5.0; float $leftfingeroptionsrelax = `getAttr "Biped_LeftFingerOptions_ctrl.relax"`; float $leftfingerindexrotateX = `getAttr "Biped_LeftFingerIndex{0}_globalcurl.rotateX"`; float $totalleftfingeroptionsrelax = $leftfingeroptionsrelax + $add1; float $totalleftindexrotateX = $leftfingerindexrotateX + $add2; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.relax -driverValue $totalleftfingeroptionsrelax -attribute "rotateX" -value $totalleftindexrotateX Biped_LeftFingerIndex{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $leftfingeroptionsrelax = `getAttr "Biped_LeftFingerOptions_ctrl.relax"`; float $leftfingermiddlerotateX = `getAttr "Biped_LeftFingerMiddle{0}_globalcurl.rotateX"`; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.relax -driverValue $leftfingeroptionsrelax -attribute "rotateX" -value $leftfingermiddlerotateX Biped_LeftFingerMiddle{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 10.0; float $leftfingeroptionsrelax = `getAttr "Biped_LeftFingerOptions_ctrl.relax"`; float $leftfingermiddlerotateX = `getAttr "Biped_LeftFingerMiddle{0}_globalcurl.rotateX"`; float $totalleftfingeroptionsrelax = $leftfingeroptionsrelax + $add1; float $totalleftmiddlerotateX = $leftfingermiddlerotateX + $add2; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.relax -driverValue $totalleftfingeroptionsrelax -attribute "rotateX" -value $totalleftmiddlerotateX Biped_LeftFingerMiddle{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = -10.0; float $add2 = 8.0; float $leftfingeroptionsrelax = `getAttr "Biped_LeftFingerOptions_ctrl.relax"`; float $leftfingermiddlerotateX = `getAttr "Biped_LeftFingerMiddle{0}_globalcurl.rotateX"`; float $totalleftfingeroptionsrelax = $leftfingeroptionsrelax + $add1; float $totalleftmiddlerotateX = $leftfingermiddlerotateX + $add2; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.relax -driverValue $totalleftfingeroptionsrelax -attribute "rotateX" -value $totalleftmiddlerotateX Biped_LeftFingerMiddle{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $leftfingeroptionsrelax = `getAttr "Biped_LeftFingerOptions_ctrl.relax"`; float $leftfingerringrotateX = `getAttr "Biped_LeftFingerRing{0}_globalcurl.rotateX"`; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.relax -driverValue $leftfingeroptionsrelax -attribute "rotateX" -value $leftfingerringrotateX Biped_LeftFingerRing{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 8.0; float $leftfingeroptionsrelax = `getAttr "Biped_LeftFingerOptions_ctrl.relax"`; float $leftfingerringrotateX = `getAttr "Biped_LeftFingerRing{0}_globalcurl.rotateX"`; float $totalleftfingeroptionsrelax = $leftfingeroptionsrelax + $add1; float $totalleftringrotateX = $leftfingerringrotateX + $add2; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.relax -driverValue $totalleftfingeroptionsrelax -attribute "rotateX" -value $totalleftringrotateX Biped_LeftFingerRing{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = -10.0; float $add2 = 10.0; float $leftfingeroptionsrelax = `getAttr "Biped_LeftFingerOptions_ctrl.relax"`; float $leftfingerringrotateX = `getAttr "Biped_LeftFingerRing{0}_globalcurl.rotateX"`; float $totalleftfingeroptionsrelax = $leftfingeroptionsrelax + $add1; float $totalleftringrotateX = $leftfingerringrotateX + $add2; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.relax -driverValue $totalleftfingeroptionsrelax -attribute "rotateX" -value $totalleftringrotateX Biped_LeftFingerRing{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $leftfingeroptionsrelax = `getAttr "Biped_LeftFingerOptions_ctrl.relax"`; float $leftfingerpinkyrotateX = `getAttr "Biped_LeftFingerPinky{0}_globalcurl.rotateX"`; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.relax -driverValue $leftfingeroptionsrelax -attribute "rotateX" -value $leftfingerpinkyrotateX Biped_LeftFingerPinky{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 5.0; float $leftfingeroptionsrelax = `getAttr "Biped_LeftFingerOptions_ctrl.relax"`; float $leftfingerpinkyrotateX = `getAttr "Biped_LeftFingerPinky{0}_globalcurl.rotateX"`; float $totalleftfingeroptionsrelax = $leftfingeroptionsrelax + $add1; float $totalleftpinkyrotateX = $leftfingerpinkyrotateX + $add2; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.relax -driverValue $totalleftfingeroptionsrelax -attribute "rotateX" -value $totalleftpinkyrotateX Biped_LeftFingerPinky{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = -10.0; float $add2 = 15.0; float $leftfingeroptionsrelax = `getAttr "Biped_LeftFingerOptions_ctrl.relax"`; float $leftfingerpinkyrotateX = `getAttr "Biped_LeftFingerPinky{0}_globalcurl.rotateX"`; float $totalleftfingeroptionsrelax = $leftfingeroptionsrelax + $add1; float $totalleftpinkyrotateX = $leftfingerpinkyrotateX + $add2; setDrivenKeyframe -currentDriver Biped_LeftFingerOptions_ctrl.relax -driverValue $totalleftfingeroptionsrelax -attribute "rotateX" -value $totalleftpinkyrotateX Biped_LeftFingerPinky{0}_globalcurl;'.format(index))

                self.MDG2_mod.commandToExecute('selectKey Biped_LeftFingerThumb{0}_globalcurl; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative -preInfinite cycleRelative'.format(index))
                self.MDG2_mod.commandToExecute('selectKey Biped_LeftFingerIndex{0}_globalcurl; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative -preInfinite cycleRelative'.format(index))
                self.MDG2_mod.commandToExecute('selectKey Biped_LeftFingerMiddle{0}_globalcurl; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative -preInfinite cycleRelative'.format(index))
                self.MDG2_mod.commandToExecute('selectKey Biped_LeftFingerRing{0}_globalcurl; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative -preInfinite cycleRelative'.format(index))
                self.MDG2_mod.commandToExecute('selectKey Biped_LeftFingerPinky{0}_globalcurl; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative -preInfinite cycleRelative'.format(index))

        lfingergrp_sl_ls = om2.MSelectionList()
        lfingergrp_sl_ls.add("Biped_LeftFingers_null")
        grp_obj = lfingergrp_sl_ls.getDependNode(0)

        lfingergrp_multMatrix = self.MDG2_mod.createNode("multMatrix")
        lfingergrp_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
        self.MDG2_mod.renameNode(lfingergrp_multMatrix, "LeftFingers_multMatrix")
        self.MDG2_mod.renameNode(lfingergrp_decomposeMatrix, "LeftFingers_decomposeMatrix")

        lfingergrpmultMatrix_fs = om2.MFnDependencyNode(lfingergrp_multMatrix)
        lfingergrpdecomposeMatrix_fs = om2.MFnDependencyNode(lfingergrp_decomposeMatrix)
        lfingergrp_fs = om2.MFnDependencyNode(grp_obj)

        lfingergrpmultMatrixSum_plug = lfingergrpmultMatrix_fs.findPlug("matrixSum", False)
        lfingergrpdecomposeInpMatrix_plug = lfingergrpdecomposeMatrix_fs.findPlug("inputMatrix", False)
        lfingergrpdecomposeOtpTrans_plug = lfingergrpdecomposeMatrix_fs.findPlug("outputTranslate", False)
        lfingergrpdecomposeOtpRot_plug = lfingergrpdecomposeMatrix_fs.findPlug("outputRotate", False)
        lfingergrpjntTrans_plug = lfingergrp_fs.findPlug("translate", False)
        lfingergrpjntRot_plug = lfingergrp_fs.findPlug("rotate", False)

        self.MDG2_mod.commandToExecute('connectAttr -force LeftHand.worldMatrix[0] LeftFingers_multMatrix.matrixIn[0]')
        self.MDG2_mod.commandToExecute('connectAttr -force Biped_LeftFingers_null.parentInverseMatrix[0] LeftFingers_multMatrix.matrixIn[1]')
        self.MDG2_mod.connect(lfingergrpmultMatrixSum_plug, lfingergrpdecomposeInpMatrix_plug)
        self.MDG2_mod.connect(lfingergrpdecomposeOtpTrans_plug, lfingergrpjntTrans_plug)
        self.MDG2_mod.connect(lfingergrpdecomposeOtpRot_plug, lfingergrpjntRot_plug)

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
        llegoptions_sl_ls.add("FkLeftJointLeg_grp")
        llegoptions_sl_ls.add("LeftJointLeg_grp")
        llegoptions_obj = llegoptions_sl_ls.getDependNode(0)
        fklleggrp_obj = llegoptions_sl_ls.getDependNode(1)
        lleggrp_obj = llegoptions_sl_ls.getDependNode(2)

        self.MDG2_mod.commandToExecute('addAttr -longName "stretchy" -niceName "Stretchy" -attributeType double -keyable true -defaultValue 0 Biped_FkLeftUpLeg_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "stretchy" -niceName "Stretchy" -attributeType double -keyable true -defaultValue 0 Biped_FkLeftLeg_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "fkik" -niceName "Fk/Ik" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_LeftFootOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "kneeswitch" -niceName "Auto/Manual Knee" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_LeftFootOptions_ctrl')
        self.MDG2_mod.doIt()

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
                llegctrl_multMatrix = self.MDG2_mod.createNode("multMatrix")
                llegctrl_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                self.MDG2_mod.renameNode(llegctrl_multMatrix, str(jnt_string)[2:][:-3] + "_multMatrix")
                self.MDG2_mod.renameNode(llegctrl_decomposeMatrix, str(jnt_string)[2:][:-3] + "_decomposeMatrix")

                llegmultMatrix_fs = om2.MFnDependencyNode(llegctrl_multMatrix)
                llegdecomposeMatrix_fs = om2.MFnDependencyNode(llegctrl_decomposeMatrix)
                llegjnt_fs = om2.MFnDependencyNode(jnt_obj)

                llegmultMatrixSum_plug = llegmultMatrix_fs.findPlug("matrixSum", False)
                llegdecomposeInpMatrix_plug = llegdecomposeMatrix_fs.findPlug("inputMatrix", False)
                llegdecomposeOtpTrans_plug = llegdecomposeMatrix_fs.findPlug("outputTranslate", False)
                llegdecomposeOtpRot_plug = llegdecomposeMatrix_fs.findPlug("outputRotate", False)
                llegjntTrans_plug = llegjnt_fs.findPlug("translate", False)
                llegjntRot_plug = llegjnt_fs.findPlug("rotate", False)

                self.MDG2_mod.commandToExecute('connectAttr -force Biped_{0}_ctrl.worldMatrix[0] {0}_multMatrix.matrixIn[0]'.format(str(jnt_string)[3:][:-3]))
                self.MDG2_mod.commandToExecute('connectAttr -force {0}.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(jnt_string)[3:][:-3]))
                self.MDG2_mod.connect(llegmultMatrixSum_plug, llegdecomposeInpMatrix_plug)
                self.MDG2_mod.connect(llegdecomposeOtpTrans_plug, llegjntTrans_plug)
                self.MDG2_mod.connect(llegdecomposeOtpRot_plug, llegjntRot_plug)

                if cmds.getAttr("{0}.jointOrientX".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientY".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientZ".format(str(jnt_string)[3:][:-3])) != 0:
                    self.MDG2_mod.commandToExecute('setAttr "{0}.jointOrientX" 0'.format(str(jnt_string)[3:][:-3]))
                    self.MDG2_mod.commandToExecute('setAttr "{0}.jointOrientY" 0'.format(str(jnt_string)[3:][:-3]))
                    self.MDG2_mod.commandToExecute('setAttr "{0}.jointOrientZ" 0'.format(str(jnt_string)[3:][:-3]))

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
                    legrotblendnode = self.MDG2_mod.createNode("blendColors")
                    legtransblendnode = self.MDG2_mod.createNode("blendColors")
                    legjoint_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                    self.MDG2_mod.renameNode(legjoint_decomposeMatrix, str(bindjnt_string)[2:][:-3] + "Blend_decomposeMatrix")
                    self.MDG2_mod.renameNode(legrotblendnode, str(bindjnt_string)[2:][:-3] + "Rot_blend")
                    self.MDG2_mod.renameNode(legtransblendnode, str(bindjnt_string)[2:][:-3] + "Trans_blend")

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

                    self.MDG2_mod.connect(iklegjointotp_plug, legdecomposeInpMatrix_plug)
                    self.MDG2_mod.connect(legdecomposeOtpRot_plug, legrotblendnodeinp1_plug)
                    self.MDG2_mod.connect(legdecomposeOtpTrans_plug, legtransblendnodeinp1_plug)
                    self.MDG2_mod.connect(fklegjointrototp_plug, legrotblendnodeinp2_plug)
                    self.MDG2_mod.connect(fklegjointtransotp_plug, legtransblendnodeinp2_plug)
                    self.MDG2_mod.connect(legrotblendnodeotp_plug, legjointrotinp_plug)
                    self.MDG2_mod.connect(legtransblendnodeotp_plug, legjointtransinp_plug)
                    self.MDG2_mod.connect(llegoptionsfkik_plug, legrotblendnodeblender_plug)
                    self.MDG2_mod.connect(llegoptionsfkik_plug, legtransblendnodeblender_plug)

                    if index < 3:
                        noflipjnt_obj = noflipiklleg_sl_ls.getDependNode(index)
                        noflipjnt_string = noflipiklleg_sl_ls.getSelectionStrings(index)

                        pvjnt_obj = pviklleg_sl_ls.getDependNode(index)
                        pvjnt_string = pviklleg_sl_ls.getSelectionStrings(index)

                        legrotblendnode = self.MDG2_mod.createNode("blendColors")
                        legtransblendnode = self.MDG2_mod.createNode("blendColors")
                        nofliplegjoint_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                        pvlegjoint_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                        self.MDG2_mod.renameNode(nofliplegjoint_decomposeMatrix, str(noflipjnt_string)[2:][:-3] + "Blend_decomposeMatrix")
                        self.MDG2_mod.renameNode(pvlegjoint_decomposeMatrix, str(pvjnt_string)[2:][:-3] + "Blend_decomposeMatrix")
                        self.MDG2_mod.renameNode(legrotblendnode, str(bindjnt_string)[2:][:-3] + "Rot_kneeblend")
                        self.MDG2_mod.renameNode(legtransblendnode, str(bindjnt_string)[2:][:-3] + "Trans_kneeblend")

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

                        self.MDG2_mod.connect(noflipiklegjointotp_plug, nofliplegdecomposeInpMatrix_plug)
                        self.MDG2_mod.connect(pviklegjointotp_plug, pvlegdecomposeInpMatrix_plug)
                        self.MDG2_mod.connect(pvlegdecomposeOtpRot_plug, legrotblendnodeinp1_plug)
                        self.MDG2_mod.connect(pvlegdecomposeOtpTrans_plug, legtransblendnodeinp1_plug)
                        self.MDG2_mod.connect(nofliplegdecomposeOtpRot_plug, legrotblendnodeinp2_plug)
                        self.MDG2_mod.connect(nofliplegdecomposeOtpTrans_plug, legtransblendnodeinp2_plug)
                        self.MDG2_mod.connect(legrotblendnodeotp_plug, iklegjointinpRot_plug)
                        self.MDG2_mod.connect(legtransblendnodeotp_plug, iklegjointinpTrans_plug)
                        self.MDG2_mod.connect(llegoptionskneeswitch_plug, legrotblendnodeblender_plug)
                        self.MDG2_mod.connect(llegoptionskneeswitch_plug, legtransblendnodeblender_plug)

                else:
                    self.MDG2_mod.connect(fklegjointtransotp_plug, legjointtransinp_plug)
                    self.MDG2_mod.connect(fklegjointrototp_plug, legjointrotinp_plug)

            if self.autostretch.currentIndex() == 1:
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

                    llegjoint_multMatrix = self.MDG2_mod.createNode("multMatrix")
                    legjoint_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")

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

                    self.MDG2_mod.renameNode(llegjoint_multMatrix, str(bindjnt_string)[2:][:-3] + "_multMatrix")
                    self.MDG2_mod.renameNode(legjoint_decomposeMatrix, str(bindjnt_string)[2:][:-3] + "_decomposeMatrix")
                    self.MDG2_mod.commandToExecute('connectAttr -force {0}.worldMatrix[0] {0}_multMatrix.matrixIn[0]'.format(str(bindjnt_string)[3:][:-3]))
                    self.MDG2_mod.connect(llegmultMatrixSum_plug, llegdecomposeInpMatrix_plug)

                    fkllegstretch_expression = om1.MFnExpression()

                    if index == 0:
                        fkllegstretch_expression.create("Biped_FkLeftLeg_ctrl.translateY = Biped_FkLeftUpLeg_ctrl.stretchy")
                        fkllegstretch_expression.create("Biped_FkLeftLeg_ctrl.translateZ = Biped_FkLeftLeg_ctrl.translateY/10")

                        self.MDG2_mod.commandToExecute('connectAttr -force LeftUpperLegIkCluster_grp.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(bindjnt_string)[3:][:-3]))
                        self.MDG2_mod.connect(llegdecomposeOtpTrans_plug, iklupperleggrpTrans_plug)
                        self.MDG2_mod.connect(llegdecomposeOtpRot_plug, iklupperleggrpRot_plug)

                        lupperlegcluster2_multMatrix = self.MDG2_mod.createNode("multMatrix")
                        lupperlegcluster2_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")

                        lupperlegcluster2multMatrix_fs = om2.MFnDependencyNode(lupperlegcluster2_multMatrix)
                        lupperlegcluster2decomposeMatrix_fs = om2.MFnDependencyNode(lupperlegcluster2_decomposeMatrix)
                        lupperlegcluster2_fs = om2.MFnDependencyNode(grp_legupperikcluster2)

                        lupperlegcluster2multMatrixSum_plug = lupperlegcluster2multMatrix_fs.findPlug("matrixSum", False)
                        lupperlegcluster2decomposeInpMatrix_plug = lupperlegcluster2decomposeMatrix_fs.findPlug("inputMatrix", False)
                        lupperlegcluster2decomposeOtpTrans_plug = lupperlegcluster2decomposeMatrix_fs.findPlug("outputTranslate", False)
                        lupperlegcluster2Trans_plug = lupperlegcluster2_fs.findPlug("translate", False)

                        self.MDG2_mod.renameNode(lupperlegcluster2_multMatrix, "LeftUpperLegCluster2_multMatrix")
                        self.MDG2_mod.renameNode(lupperlegcluster2_decomposeMatrix, "LeftUpperLegCluster2_decomposeMatrix")
                        self.MDG2_mod.connect(lupperlegcluster2multMatrixSum_plug, lupperlegcluster2decomposeInpMatrix_plug)
                        self.MDG2_mod.commandToExecute('connectAttr -force LeftLeg.worldMatrix[0] LeftUpperLegCluster2_multMatrix.matrixIn[0]')
                        self.MDG2_mod.commandToExecute('connectAttr -force LeftUpperLegIkCluster2_grp.parentInverseMatrix[0] LeftUpperLegCluster2_multMatrix.matrixIn[1]')
                        self.MDG2_mod.connect(lupperlegcluster2decomposeOtpTrans_plug, lupperlegcluster2Trans_plug)

                    elif index == 1:
                        fkllegstretch_expression.create("Biped_FkLeftFoot_ctrl.translateY = Biped_FkLeftLeg_ctrl.stretchy")
                        fkllegstretch_expression.create("Biped_FkLeftFoot_ctrl.translateZ = Biped_FkLeftFoot_ctrl.translateY*(-1.5)")

                        self.MDG2_mod.commandToExecute('connectAttr -force LeftLowerLegIkCluster_grp.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(bindjnt_string)[3:][:-3]))
                        self.MDG2_mod.connect(llegdecomposeOtpTrans_plug, ikllowerleggrpTrans_plug)
                        self.MDG2_mod.connect(llegdecomposeOtpRot_plug, ikllowerleggrpRot_plug)

                        llowerlegcluster2_multMatrix = self.MDG2_mod.createNode("multMatrix")
                        llowerlegcluster2_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")

                        llowerlegcluster2multMatrix_fs = om2.MFnDependencyNode(llowerlegcluster2_multMatrix)
                        llowerlegcluster2decomposeMatrix_fs = om2.MFnDependencyNode(llowerlegcluster2_decomposeMatrix)
                        llowerlegcluster2_fs = om2.MFnDependencyNode(grp_leglowerikcluster2)

                        llowerlegcluster2multMatrixSum_plug = llowerlegcluster2multMatrix_fs.findPlug("matrixSum", False)
                        llowerlegcluster2decomposeInpMatrix_plug = llowerlegcluster2decomposeMatrix_fs.findPlug("inputMatrix", False)
                        llowerlegcluster2decomposeOtpTrans_plug = llowerlegcluster2decomposeMatrix_fs.findPlug("outputTranslate", False)
                        llowerlegcluster2Trans_plug = llowerlegcluster2_fs.findPlug("translate", False)

                        self.MDG2_mod.renameNode(llowerlegcluster2_multMatrix, "LeftLowerLegCluster2_multMatrix")
                        self.MDG2_mod.renameNode(llowerlegcluster2_decomposeMatrix, "LeftLowerLegCluster2_decomposeMatrix")
                        self.MDG2_mod.commandToExecute('connectAttr -force LeftFoot.worldMatrix[0] LeftLowerLegCluster2_multMatrix.matrixIn[0]')
                        self.MDG2_mod.commandToExecute('connectAttr -force LeftLowerLegIkCluster2_grp.parentInverseMatrix[0] LeftLowerLegCluster2_multMatrix.matrixIn[1]')
                        self.MDG2_mod.connect(llowerlegcluster2multMatrixSum_plug, llowerlegcluster2decomposeInpMatrix_plug)
                        self.MDG2_mod.connect(llowerlegcluster2decomposeOtpTrans_plug, llowerlegcluster2Trans_plug)

            elif cmds.objExists("LeftLegIkCluster_grp") and cmds.objExists("IkStretchyLeftJointLeg_grp"):
                self.MDG2_mod.commandToExecute('delete "LeftLegIkCluster_grp"')
                self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false Biped_FkLeftUpLeg_ctrl.stretchy')
                self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false Biped_FkLeftLeg_ctrl.stretchy')
                self.MDG2_mod.doIt()

        fklleggrp_fs = om2.MFnDependencyNode(fklleggrp_obj)
        lleggrp_fs = om2.MFnDependencyNode(lleggrp_obj)

        fklleggrpScal_plug = fklleggrp_fs.findPlug("scale", False)
        lleggrpScal_plug = lleggrp_fs.findPlug("scale", False)

        self.MDG2_mod.connect(masterdecomposeOtpScale_plug, fklleggrpScal_plug)
        self.MDG2_mod.connect(masterdecomposeOtpScale_plug, lleggrpScal_plug)

        grp_legupperikcluster1 = om1.MObject()
        grp_legupperikcluster2 = om1.MObject()
        obj_stretchyleftleg1 = om1.MObject()

        if self.autostretch.currentIndex() == 1:

            self.MDG2_mod.commandToExecute('addAttr -longName "stretchable" -niceName "Stretchable" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_LeftFootOptions_ctrl')
            self.MDG2_mod.doIt()

            stretchy_sl_lst1.add("Biped_LeftFootOptions_ctrl")
            stretchy_sl_lst1.getDependNode(3, obj_stretchyleftleg1)

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

                self.MDag_path = om1.MDagPath()
                rootspine_path = self.MDag_path.getAPathTo(obj_root)

                try:
                    ikspineiksolver_lst.add("ikSplineSolver*")
                except:
                    cmds.createNode("ikSplineSolver")

                self.iklleg_effector = self.IK_Effector.create(obj_endspine)
                iklleg_effector_path = self.MDag_path.getAPathTo(self.iklleg_effector)

                self.lleg_ik = self.IK_Handle.create(rootspine_path, iklleg_effector_path)

                obj_array = om1.MPointArray()
                obj_lst_mpoint = []
                obj = om1.MObject()
                for index in range(iklupperleg_sl_lst.length()):
                    iklupperleg_sl_lst.getDependNode(index, obj)
                    obj_path = self.MDag_path.getAPathTo(obj)
                    obj_tn = om1.MFnTransform(obj_path)
                    obj_t = obj_tn.translation(om1.MSpace.kWorld)
                    obj_lst_mpoint.append(om1.MPoint(obj_t))
                    obj_array.append(obj_lst_mpoint[index])

                self.ikspline_cv_tn = ikspinedag_n.create("transform", "LeftUpperLeg_SplineCv")
                ikspline_cv = self.MNurbs1_cv.createWithEditPoints(obj_array, 1, 1, False, True, True, self.ikspline_cv_tn)
                cmds.parent("LeftUpperLeg_SplineCv", "DoNotTouch")

                llegcrv_info = ikspinedg_modifier.createNode("curveInfo")
                llegstretchpercent = ikspinedg_modifier.createNode("multiplyDivide")
                llegstretchpow = ikspinedg_modifier.createNode("multiplyDivide")
                llegstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                llegscalediv = ikspinedg_modifier.createNode("multiplyDivide")
                liklegstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                blendstretch = ikspinedg_modifier.createNode("blendColors")

                llegcrvinfo_fs = om1.MFnDependencyNode(llegcrv_info)
                llegstretchpercent_fs = om1.MFnDependencyNode(llegstretchpercent)
                llegstretchpow_fs = om1.MFnDependencyNode(llegstretchpow)
                llegstretchdiv_fs = om1.MFnDependencyNode(llegstretchdiv)
                llegscalediv_fs = om1.MFnDependencyNode(llegscalediv)
                liklegstretchdiv_fs = om1.MFnDependencyNode(liklegstretchdiv)
                liklegstretchcluster1_fs = om1.MFnDependencyNode(grp_legupperikcluster1)
                liklegstretchcluster2_fs = om1.MFnDependencyNode(grp_legupperikcluster2)
                blendstretch_fs = om1.MFnDependencyNode(blendstretch)
                llegstretchoption_fs = om1.MFnDependencyNode(obj_stretchyleftleg1)

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
                liklegstretchdivinp1_plug = liklegstretchdiv_fs.findPlug("input1")
                liklegstretchdivotp_plug = liklegstretchdiv_fs.findPlug("output")
                liklegstretchclust1trans_plug = liklegstretchcluster1_fs.findPlug("translate")
                liklegstretchclust2trans_plug = liklegstretchcluster2_fs.findPlug("translate")
                blendstretchinp1r_plug = blendstretch_fs.findPlug("color1R")
                blendstretchinp1g_plug = blendstretch_fs.findPlug("color1G")
                blendstretchinp1b_plug = blendstretch_fs.findPlug("color1B")
                blendstretchotpr_plug = blendstretch_fs.findPlug("outputR")
                blendstretchotpg_plug = blendstretch_fs.findPlug("outputG")
                blendstretchotpb_plug = blendstretch_fs.findPlug("outputB")
                blendstretch_plug = blendstretch_fs.findPlug("blender")
                llegstretchoption_plug = llegstretchoption_fs.findPlug("stretchable")

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
                        ikspinedg_modifier.connect(llegstretchpercentotp_plug, blendstretchinp1g_plug)
                        ikspinedg_modifier.connect(llegstretchdivotox_plug, blendstretchinp1r_plug)
                        ikspinedg_modifier.connect(llegstretchdivotpz_plug, blendstretchinp1b_plug)
                        ikspinedg_modifier.connect(blendstretchotpg_plug, llegjnt_syplug)
                        ikspinedg_modifier.connect(blendstretchotpr_plug, llegjnt_sxplug)
                        ikspinedg_modifier.connect(blendstretchotpb_plug, llegjnt_szplug)
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
                ikspinedg_modifier.renameNode(blendstretch, "LeftUpperLegStretch_Blend")
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
                ikspinedg_modifier.connect(llegcrvinfoarc_plug, llegscaledivinp1y_plug)
                ikspinedg_modifier.connect(masterctrlsy_plug, llegscaledivinp2y_plug)
                ikspinedg_modifier.connect(llegscaledivotpy_plug, llegstretchpercentinp1y_plug)
                ikspinedg_modifier.connect(llegstretchpercentotp_plug, llegstretchpowinp1x_plug)
                ikspinedg_modifier.connect(llegstretchpercentotp_plug, llegstretchpowinp1z_plug)
                ikspinedg_modifier.connect(llegstretchpowotpx_plug, llegstretchdivinp2x_plug)
                ikspinedg_modifier.connect(llegstretchpowotpz_plug, llegstretchdivinp2z_plug)
                ikspinedg_modifier.connect(liklegstretchclust2trans_plug, liklegstretchdivinp1_plug)
                ikspinedg_modifier.connect(liklegstretchdivotp_plug, liklegstretchclust1trans_plug)
                ikspinedg_modifier.connect(llegstretchoption_plug, blendstretch_plug)
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
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLegStretch_Divide2.input2X" 2')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLegStretch_Divide2.input2Y" 2')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLegStretch_Divide2.input2Z" 2')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLegStretch_Blend.color2R" 1')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLegStretch_Blend.color2G" 1')
                ikspinedg_modifier.commandToExecute('setAttr "LeftUpperLegStretch_Blend.color2B" 1')
                ikspinedg_modifier.doIt()

                ikspline_solver = self.IK_System.findSolver("ikSplineSolver")
                self.IK_Handle.setSolver(ikspline_solver)

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

                    rootspine_path = self.MDag_path.getAPathTo(obj_root)

                    try:
                        ikspineiksolver_lst.add("ikSplineSolver*")
                    except:
                        cmds.createNode("ikSplineSolver")

                    self.iklleg_effector = self.IK_Effector.create(obj_endspine)
                    iklleg_effector_path = self.MDag_path.getAPathTo(self.iklleg_effector)

                    self.lleg_ik = self.IK_Handle.create(rootspine_path, iklleg_effector_path)

                    obj_array = om1.MPointArray()
                    obj_lst_mpoint = []
                    obj = om1.MObject()
                    for index in range(ikllowerleg_sl_lst.length()):
                        ikllowerleg_sl_lst.getDependNode(index, obj)
                        obj_path = self.MDag_path.getAPathTo(obj)
                        obj_tn = om1.MFnTransform(obj_path)
                        obj_t = obj_tn.translation(om1.MSpace.kWorld)
                        obj_lst_mpoint.append(om1.MPoint(obj_t))
                        obj_array.append(obj_lst_mpoint[index])

                    self.ikspline_cv_tn = ikspinedag_n.create("transform", "LeftLowerLeg_SplineCv")
                    ikspline_cv = self.MNurbs1_cv.createWithEditPoints(obj_array, 1, 1, False, True, True, self.ikspline_cv_tn)
                    cmds.parent("LeftLowerLeg_SplineCv", "DoNotTouch")

                    llegcrv_info = ikspinedg_modifier.createNode("curveInfo")
                    llegstretchpercent = ikspinedg_modifier.createNode("multiplyDivide")
                    llegstretchpow = ikspinedg_modifier.createNode("multiplyDivide")
                    llegstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                    llegscalediv = ikspinedg_modifier.createNode("multiplyDivide")
                    liklegstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                    blendstretch = ikspinedg_modifier.createNode("blendColors")

                    llegcrvinfo_fs = om1.MFnDependencyNode(llegcrv_info)
                    llegstretchpercent_fs = om1.MFnDependencyNode(llegstretchpercent)
                    llegstretchpow_fs = om1.MFnDependencyNode(llegstretchpow)
                    llegstretchdiv_fs = om1.MFnDependencyNode(llegstretchdiv)
                    llegscalediv_fs = om1.MFnDependencyNode(llegscalediv)
                    liklegstretchdiv_fs = om1.MFnDependencyNode(liklegstretchdiv)
                    liklegstretchcluster1_fs = om1.MFnDependencyNode(grp_leglowerikcluster1)
                    liklegstretchcluster2_fs = om1.MFnDependencyNode(grp_leglowerikcluster2)
                    blendstretch_fs = om1.MFnDependencyNode(blendstretch)

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
                    liklegstretchdivinp1_plug = liklegstretchdiv_fs.findPlug("input1")
                    liklegstretchdivotp_plug = liklegstretchdiv_fs.findPlug("output")
                    liklegstretchclust1trans_plug = liklegstretchcluster1_fs.findPlug("translate")
                    liklegstretchclust2trans_plug = liklegstretchcluster2_fs.findPlug("translate")
                    blendstretchinp1r_plug = blendstretch_fs.findPlug("color1R")
                    blendstretchinp1g_plug = blendstretch_fs.findPlug("color1G")
                    blendstretchinp1b_plug = blendstretch_fs.findPlug("color1B")
                    blendstretchotpr_plug = blendstretch_fs.findPlug("outputR")
                    blendstretchotpg_plug = blendstretch_fs.findPlug("outputG")
                    blendstretchotpb_plug = blendstretch_fs.findPlug("outputB")
                    blendstretch_plug = blendstretch_fs.findPlug("blender")

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
                            ikspinedg_modifier.connect(llegstretchpercentotp_plug, blendstretchinp1g_plug)
                            ikspinedg_modifier.connect(llegstretchdivotox_plug, blendstretchinp1r_plug)
                            ikspinedg_modifier.connect(llegstretchdivotpz_plug, blendstretchinp1b_plug)
                            ikspinedg_modifier.connect(blendstretchotpg_plug, llegjnt_syplug)
                            ikspinedg_modifier.connect(blendstretchotpr_plug, llegjnt_sxplug)
                            ikspinedg_modifier.connect(blendstretchotpb_plug, llegjnt_szplug)
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
                    ikspinedg_modifier.renameNode(blendstretch, "LeftLowerLegStretch_Blend")
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
                    ikspinedg_modifier.connect(llegcrvinfoarc_plug, llegscaledivinp1y_plug)
                    ikspinedg_modifier.connect(masterctrlsy_plug, llegscaledivinp2y_plug)
                    ikspinedg_modifier.connect(llegscaledivotpy_plug, llegstretchpercentinp1y_plug)
                    ikspinedg_modifier.connect(llegstretchpercentotp_plug, llegstretchpowinp1x_plug)
                    ikspinedg_modifier.connect(llegstretchpercentotp_plug, llegstretchpowinp1z_plug)
                    ikspinedg_modifier.connect(llegstretchpowotpx_plug, llegstretchdivinp2x_plug)
                    ikspinedg_modifier.connect(llegstretchpowotpz_plug, llegstretchdivinp2z_plug)
                    ikspinedg_modifier.connect(liklegstretchclust2trans_plug, liklegstretchdivinp1_plug)
                    ikspinedg_modifier.connect(liklegstretchdivotp_plug, liklegstretchclust1trans_plug)
                    ikspinedg_modifier.connect(llegstretchoption_plug, blendstretch_plug)
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
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLegStretch_Blend.color2R" 1')
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLegStretch_Blend.color2G" 1')
                    ikspinedg_modifier.commandToExecute('setAttr "LeftLowerLegStretch_Blend.color2B" 1')
                    ikspinedg_modifier.doIt()

                    ikspline_solver = self.IK_System.findSolver("ikSplineSolver")
                    self.IK_Handle.setSolver(ikspline_solver)

        stretchy_sl_lst2.add("Biped_LeftFootOptions_ctrl")
        obj_stretchyleftleg2 = stretchy_sl_lst2.getDependNode(1)

        if cmds.objExists("NoFlipLeftLeg_Ik") and cmds.objExists("PVLeftLeg_Ik"):

            self.MDG2_mod.commandToExecute('addAttr -longName "follow" -niceName "Follow Body" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_IkLeftFoot_ctrl')
            self.MDG2_mod.commandToExecute('parentConstraint -mo -weight 1 Biped_Root_ctrl Biped_IkLeftFootRot_null')
            self.MDG2_mod.doIt()

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
                liklegctrl_multMatrix = self.MDG2_mod.createNode("multMatrix")
                liklegctrl_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                self.MDG2_mod.renameNode(liklegctrl_multMatrix, "IkLeftLegCtrl_multMatrix")
                self.MDG2_mod.renameNode(liklegctrl_decomposeMatrix, "IkLeftLegCtrl_decomposeMatrix")

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
                iklegctrlTrans_plug = iklegctrl_fs.findPlug("translate", False)
                iklegctrlRot_plug = iklegctrl_fs.findPlug("rotate", False)
                liklegjntScal_plug = likleggrpobj_fs.findPlug("scale", False)

                self.MDG2_mod.commandToExecute('connectAttr -force Biped_IkLeftFoot_ctrl.worldMatrix[0] IkLeftLegCtrl_multMatrix.matrixIn[0]')
                self.MDG2_mod.commandToExecute('parent LeftReverseFootHeel LeftLegIk_grp')
                self.MDG2_mod.commandToExecute('poleVectorConstraint Biped_NoFlipLeftKnee_ctrl NoFlipLeftLeg_Ik')
                self.MDG2_mod.commandToExecute('poleVectorConstraint Biped_PVLeftKnee_ctrl PVLeftLeg_Ik')
                self.MDG2_mod.commandToExecute('setAttr "NoFlipLeftLeg_Ik.twist" 90')
                self.MDG2_mod.commandToExecute('connectAttr -force Biped_IkLeftFoot_ctrl.follow Biped_IkLeftFootRot_null_parentConstraint1.Biped_Root_ctrlW0')
                self.MDG2_mod.connect(liklegmultMatrixSum_plug, liklegdecomposeInpMatrix_plug)
                self.MDG2_mod.connect(liklegdecomposeOtpTrans_plug, likleggrpTrans_plug)
                self.MDG2_mod.connect(iklegctrlTrans_plug, noflipleftkneenullTrans_plug)
                self.MDG2_mod.connect(iklegctrlRot_plug, noflipleftkneenullRot_plug)
                self.MDG2_mod.connect(masterdecomposeOtpScale_plug, liklegjntScal_plug)

                if self.autostretch.currentIndex() == 1:
                    liklegdistloc = om2.MFnDagNode()

                    likupperlegdistloc1_tn = liklegdistloc.create("transform", "distloc_L_upleg1", llegik_sl_ls.getDependNode(4))
                    likupperlegdistloc_ln = liklegdistloc.create("locator", "L_upleg1_Shape", likupperlegdistloc1_tn)
                    likfootlegdistloc1_tn = liklegdistloc.create("transform", "distloc_L_legfoot1")
                    likfootlegdistloc_ln = liklegdistloc.create("locator", "L_foot1_Shape", likfootlegdistloc1_tn)
                    self.MDG2_mod.commandToExecute('createNode "distanceDimShape"')
                    self.MDG2_mod.commandToExecute('rename "distanceDimension1" "IkLeftLegDistance_Info"')
                    self.MDG2_mod.doIt()

                    luplegnull_transform_t = luplegnull_transform.translation(om2.MSpace.kTransform)
                    likupperlegdistloc_transform = om2.MFnTransform(likupperlegdistloc1_tn)
                    likupperlegdistloc_transform.setTranslation(luplegnull_transform_t, om2.MSpace.kTransform)

                    IkLeftLegDistance_sl_ls = om2.MSelectionList()
                    IkLeftLegDistance_sl_ls.add("IkLeftLegDistance_InfoShape")

                    likfootlegDist_fs = om2.MFnDependencyNode(likfootlegdistloc1_tn)
                    liklegjntDist_fs = om2.MFnDependencyNode(IkLeftLegDistance_sl_ls.getDependNode(0))

                    liklegjntDistPoint2_plug = liklegjntDist_fs.findPlug("endPoint", False)
                    likfootlegDistOtpTrans_plug = likfootlegDist_fs.findPlug("translate", False)

                    self.MDG2_mod.commandToExecute('connectAttr -force L_upleg1_Shape.worldPosition[0] IkLeftLegDistance_InfoShape.startPoint')
                    self.MDG2_mod.connect(likfootlegDistOtpTrans_plug, liklegjntDistPoint2_plug)
                    self.MDG2_mod.connect(liklegdecomposeOtpTrans_plug, likfootlegDistOtpTrans_plug)
                    self.MDG2_mod.commandToExecute('float $noflipikleftlegtranslateY = `getAttr "IkNoFlipLeftLeg.translateY"`; float $noflipikleftfoottranslateY = `getAttr "IkNoFlipLeftFoot.translateY"`; float $totalnoflipikleftlegtranslateY = $noflipikleftlegtranslateY + $noflipikleftfoottranslateY; setDrivenKeyframe -currentDriver IkLeftLegDistance_InfoShape.distance -driverValue $totalnoflipikleftlegtranslateY -attribute "translateY" -value $noflipikleftlegtranslateY IkNoFlipLeftLeg;')
                    self.MDG2_mod.commandToExecute('float $noflipikleftlegtranslateY = `getAttr "IkNoFlipLeftLeg.translateY"`; float $noflipikleftfoottranslateY = `getAttr "IkNoFlipLeftFoot.translateY"`; float $totalnoflipikleftlegtranslateY = $noflipikleftlegtranslateY + $noflipikleftfoottranslateY; setDrivenKeyframe -currentDriver IkLeftLegDistance_InfoShape.distance -driverValue ($totalnoflipikleftlegtranslateY*2) -attribute "translateY" -value ($noflipikleftlegtranslateY*2) IkNoFlipLeftLeg;')
                    self.MDG2_mod.commandToExecute('float $noflipikleftlegtranslateY = `getAttr "IkNoFlipLeftLeg.translateY"`; float $noflipikleftfoottranslateY = `getAttr "IkNoFlipLeftFoot.translateY"`; float $totalnoflipikleftlegtranslateY = $noflipikleftlegtranslateY + $noflipikleftfoottranslateY; setDrivenKeyframe -currentDriver IkLeftLegDistance_InfoShape.distance -driverValue $totalnoflipikleftlegtranslateY -attribute "translateY" -value $noflipikleftfoottranslateY IkNoFlipLeftFoot;')
                    self.MDG2_mod.commandToExecute('float $noflipikleftlegtranslateY = `getAttr "IkNoFlipLeftLeg.translateY"`; float $noflipikleftfoottranslateY = `getAttr "IkNoFlipLeftFoot.translateY"`; float $totalnoflipikleftlegtranslateY = $noflipikleftlegtranslateY + $noflipikleftfoottranslateY; setDrivenKeyframe -currentDriver IkLeftLegDistance_InfoShape.distance -driverValue ($totalnoflipikleftlegtranslateY*2) -attribute "translateY" -value ($noflipikleftfoottranslateY*2) IkNoFlipLeftFoot;')
                    self.MDG2_mod.commandToExecute('float $pvikleftlegtranslateY = `getAttr "IkPVLeftLeg.translateY"`; float $pvikleftfoottranslateY = `getAttr "IkPVLeftFoot.translateY"`; float $totalpvikleftlegtranslateY = $pvikleftlegtranslateY + $pvikleftfoottranslateY; setDrivenKeyframe -currentDriver IkLeftLegDistance_InfoShape.distance -driverValue $totalpvikleftlegtranslateY -attribute "translateY" -value $pvikleftlegtranslateY IkPVLeftLeg;')
                    self.MDG2_mod.commandToExecute('float $pvikleftlegtranslateY = `getAttr "IkPVLeftLeg.translateY"`; float $pvikleftfoottranslateY = `getAttr "IkPVLeftFoot.translateY"`; float $totalpvikleftlegtranslateY = $pvikleftlegtranslateY + $pvikleftfoottranslateY; setDrivenKeyframe -currentDriver IkLeftLegDistance_InfoShape.distance -driverValue ($totalpvikleftlegtranslateY*2) -attribute "translateY" -value ($pvikleftlegtranslateY*2) IkPVLeftLeg;')
                    self.MDG2_mod.commandToExecute('float $pvikleftlegtranslateY = `getAttr "IkPVLeftLeg.translateY"`; float $pvikleftfoottranslateY = `getAttr "IkPVLeftFoot.translateY"`; float $totalpvikleftlegtranslateY = $pvikleftlegtranslateY + $pvikleftfoottranslateY; setDrivenKeyframe -currentDriver IkLeftLegDistance_InfoShape.distance -driverValue $totalpvikleftlegtranslateY -attribute "translateY" -value $pvikleftfoottranslateY IkPVLeftFoot;')
                    self.MDG2_mod.commandToExecute('float $pvikleftlegtranslateY = `getAttr "IkPVLeftLeg.translateY"`; float $pvikleftfoottranslateY = `getAttr "IkPVLeftFoot.translateY"`; float $totalpvikleftlegtranslateY = $pvikleftlegtranslateY + $pvikleftfoottranslateY; setDrivenKeyframe -currentDriver IkLeftLegDistance_InfoShape.distance -driverValue ($totalpvikleftlegtranslateY*2) -attribute "translateY" -value ($pvikleftfoottranslateY*2) IkPVLeftFoot;')
                    self.MDG2_mod.commandToExecute('selectKey -attribute translateY IkNoFlipLeftLeg; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative')
                    self.MDG2_mod.commandToExecute('selectKey -attribute translateY IkPVLeftLeg; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative')
                    self.MDG2_mod.commandToExecute('selectKey -attribute translateY IkNoFlipLeftFoot; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative')
                    self.MDG2_mod.commandToExecute('selectKey -attribute translateY IkPVLeftFoot; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative')
                    self.MDG2_mod.commandToExecute('parent "IkLeftLegDistance_Info" "DoNotTouch"')
                    self.MDG2_mod.commandToExecute('parent "distloc_L_legfoot1" "DoNotTouch"')

                    self.MDG2_mod.commandToExecute('addAttr -longName "kneesnap" -niceName "Knee Snap" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_PVLeftKnee_ctrl')

                    likupperlegdistloc2_tn = liklegdistloc.create("transform", "distloc_L_upleg2", llegik_sl_ls.getDependNode(4))
                    likupperlegdistloc_ln = liklegdistloc.create("locator", "L_upleg2_Shape", likupperlegdistloc2_tn)
                    likkneedistloc_tn = liklegdistloc.create("transform", "distloc_L_legknee")
                    likkneedistloc_ln = liklegdistloc.create("locator", "L_legknee_Shape", likkneedistloc_tn)
                    likfootlegdistloc2_tn = liklegdistloc.create("transform", "distloc_L_legfoot2")
                    likfootlegdistloc_ln = liklegdistloc.create("locator", "L_legfoot2_Shape", likfootlegdistloc2_tn)
                    pvleftkneectrl_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                    likpvupperlegtransblendnode = self.MDG2_mod.createNode("blendColors")
                    likpvlowerlegtransblendnode = self.MDG2_mod.createNode("blendColors")
                    likpvupperlegstretchblendnode = self.MDG2_mod.createNode("blendColors")
                    likpvlowerlegstretchblendnode = self.MDG2_mod.createNode("blendColors")
                    self.MDG2_mod.commandToExecute('createNode "distanceDimShape"')
                    self.MDG2_mod.commandToExecute('createNode "distanceDimShape"')
                    self.MDG2_mod.renameNode(pvleftkneectrl_decomposeMatrix, "PVLeftKnee_decomposeMatrix")
                    self.MDG2_mod.renameNode(likpvupperlegtransblendnode, "PVLeftUpperLegTrans_blend")
                    self.MDG2_mod.renameNode(likpvlowerlegtransblendnode, "PVLeftLowerLegTrans_blend")
                    self.MDG2_mod.renameNode(likpvupperlegstretchblendnode, "PVLeftUpperLegStretch_blend")
                    self.MDG2_mod.renameNode(likpvlowerlegstretchblendnode, "PVLeftLowerLegStretch_blend")
                    self.MDG2_mod.commandToExecute('rename "distanceDimension1" "LeftUpperLegDistance_Info"')
                    self.MDG2_mod.commandToExecute('rename "distanceDimension2" "LeftLowerLegDistance_Info"')
                    self.MDG2_mod.doIt()

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
                    likpvuppertransblendnode_fs = om2.MFnDependencyNode(likpvupperlegtransblendnode)
                    likpvlowertransblendnode_fs = om2.MFnDependencyNode(likpvlowerlegtransblendnode)
                    pvleftkneectrl_fs = om2.MFnDependencyNode(IkLeftLegDistance_sl_ls.getDependNode(5))
                    pvlefkneejnt_fs = om2.MFnDependencyNode(pviklleg_sl_ls.getDependNode(1))
                    pvleftfootjnt_fs = om2.MFnDependencyNode(pviklleg_sl_ls.getDependNode(2))
                    likupperlegstretchblendnode_fs = om2.MFnDependencyNode(likpvupperlegstretchblendnode)
                    liklowerlegstretchblendnode_fs = om2.MFnDependencyNode(likpvlowerlegstretchblendnode)
                    leftlegoption_fs = om2.MFnDependencyNode(obj_stretchyleftleg2)

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
                    likpvupperlegstretchblendnodeinp1g_plug = likupperlegstretchblendnode_fs.findPlug("color1G", False)
                    likpvupperlegstretchblendnodeotp_plug = likupperlegstretchblendnode_fs.findPlug("outputG", False)
                    likpvupperlegstretchblendnodeblender_plug = likupperlegstretchblendnode_fs.findPlug("blender", False)
                    likpvlowerlegstretchblendnodeinp1g_plug = liklowerlegstretchblendnode_fs.findPlug("color1G", False)
                    likpvlowerlegstretchblendnodeotp_plug = liklowerlegstretchblendnode_fs.findPlug("outputG", False)
                    likpvlowerlegstretchblendnodeblender_plug = liklowerlegstretchblendnode_fs.findPlug("blender", False)
                    ikleftlegstretch_plug = leftlegoption_fs.findPlug("stretchable", False)
                    pvleftkneejntTrans_plug = pvlefkneejnt_fs.findPlug("translateY", False)
                    pvleftfootjntTrans_plug = pvleftfootjnt_fs.findPlug("translateY", False)

                    self.MDG2_mod.commandToExecute('connectAttr -force L_upleg2_Shape.worldPosition[0] LeftUpperLegDistance_InfoShape.startPoint')
                    self.MDG2_mod.commandToExecute('connectAttr -force Biped_PVLeftKnee_ctrl.worldMatrix[0] PVLeftKnee_decomposeMatrix.inputMatrix')
                    self.MDG2_mod.connect(likkneeDistOtpTrans_plug, likupperlegjntDistPoint2_plug)
                    self.MDG2_mod.connect(likkneeDistOtpTrans_plug, liklowerlegjntDistPoint1_plug)
                    self.MDG2_mod.connect(likfootlegDistOtpTrans_plug, liklowerlegjntDistPoint2_plug)
                    self.MDG2_mod.connect(liklegdecomposeOtpTrans_plug, likfootlegDistOtpTrans_plug)
                    self.MDG2_mod.connect(pvleftkneectrlDecomposeMatrixOtpTrans_plug, likkneeDistOtpTrans_plug)

                    self.MDG2_mod.disconnect(pvleftkneekeyotp_plug, pvleftkneejntTrans_plug)
                    self.MDG2_mod.disconnect(pvleftfootkeyotp_plug, pvleftfootjntTrans_plug)
                    self.MDG2_mod.connect(pvleftkneekeyotp_plug, likpvuppertransblendnodeinp2g_plug)
                    self.MDG2_mod.connect(pvleftfootkeyotp_plug, likpvlowertransblendnodeinp2g_plug)
                    self.MDG2_mod.connect(pvleftkneectrl_fs_plug, likpvuppertransblendnodeblender_plug)
                    self.MDG2_mod.connect(pvleftkneectrl_fs_plug, likpvlowertransblendnodeblender_plug)
                    self.MDG2_mod.connect(likpvuppertransblendnodeotp_plug, likpvupperlegstretchblendnodeinp1g_plug)
                    self.MDG2_mod.connect(likpvlowertransblendnodeotp_plug, likpvlowerlegstretchblendnodeinp1g_plug)
                    self.MDG2_mod.connect(likpvupperlegstretchblendnodeotp_plug, pvleftkneejntTrans_plug)
                    self.MDG2_mod.connect(likpvlowerlegstretchblendnodeotp_plug, pvleftfootjntTrans_plug)
                    self.MDG2_mod.connect(ikleftlegstretch_plug, likpvupperlegstretchblendnodeblender_plug)
                    self.MDG2_mod.connect(ikleftlegstretch_plug, likpvlowerlegstretchblendnodeblender_plug)
                    self.MDG2_mod.commandToExecute('float $pvikleftlegtranslateY = `getAttr "PVLeftUpperLegStretch_blend.color1G"`; setAttr "PVLeftUpperLegStretch_blend.color2G" $pvikleftlegtranslateY;')
                    self.MDG2_mod.commandToExecute('float $pvikleftfoottranslateY = `getAttr "PVLeftLowerLegStretch_blend.color1G"`; setAttr "PVLeftLowerLegStretch_blend.color2G" $pvikleftfoottranslateY;')
                    self.MDG2_mod.commandToExecute('parent "distloc_L_legknee" "DoNotTouch"')
                    self.MDG2_mod.commandToExecute('parent "distloc_L_legfoot2" "DoNotTouch"')
                    self.MDG2_mod.commandToExecute('parent "LeftUpperLegDistance_Info" "DoNotTouch"')
                    self.MDG2_mod.commandToExecute('parent "LeftLowerLegDistance_Info" "DoNotTouch"')

                    self.MDG2_mod.commandToExecute('addAttr -longName "thighlength" -niceName "AutoKnee Thigh Length" -attributeType double -minValue 0 -keyable true -defaultValue 1 Biped_IkLeftFoot_ctrl')
                    self.MDG2_mod.commandToExecute('addAttr -longName "calflength" -niceName "AutoKnee Calf Length" -attributeType double -minValue 0 -keyable true -defaultValue 1 Biped_IkLeftFoot_ctrl')
                    self.MDG2_mod.doIt()

                    rikautokneeupperlegnode = self.MDG2_mod.createNode("multiplyDivide")
                    rikautokneelowerlegnode = self.MDG2_mod.createNode("multiplyDivide")
                    liknoflipupperlegtransblendnode = self.MDG2_mod.createNode("blendColors")
                    liknofliplowerlegtransblendnode = self.MDG2_mod.createNode("blendColors")
                    self.MDG2_mod.renameNode(rikautokneeupperlegnode, "NoFlipLeftLegTrans_multiply")
                    self.MDG2_mod.renameNode(rikautokneelowerlegnode, "NoFlipLeftFootTrans_multiply")
                    self.MDG2_mod.renameNode(liknoflipupperlegtransblendnode, "NoFlipLeftUpperLegStretch_blend")
                    self.MDG2_mod.renameNode(liknofliplowerlegtransblendnode, "NoFlipLeftLowerLegStretch_blend")

                    likautokneeupperleg_fs = om2.MFnDependencyNode(rikautokneeupperlegnode)
                    likautokneelowerleg_fs = om2.MFnDependencyNode(rikautokneelowerlegnode)
                    noflipleftkneekey_fs = om2.MFnDependencyNode(IkLeftLegDistance_sl_ls.getDependNode(6))
                    noflipleftfootkey_fs = om2.MFnDependencyNode(IkLeftLegDistance_sl_ls.getDependNode(7))
                    nofliplefkneejntTrans_fs = om2.MFnDependencyNode(noflipiklleg_sl_ls.getDependNode(1))
                    noflipleftfootjntTrans_fs = om2.MFnDependencyNode(noflipiklleg_sl_ls.getDependNode(2))
                    liknoflipupperlegstretchblendnode_fs = om2.MFnDependencyNode(liknoflipupperlegtransblendnode)
                    liknofliplowerlegstretchblendnode_fs = om2.MFnDependencyNode(liknofliplowerlegtransblendnode)

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
                    liknoflipupperlegstretchblendnodeinp1g_plug = liknoflipupperlegstretchblendnode_fs.findPlug("color1G", False)
                    liknoflipupperlegstretchblendnodeotp_plug = liknoflipupperlegstretchblendnode_fs.findPlug("outputG", False)
                    liknoflipupperlegstretchblendnodeblender_plug = liknoflipupperlegstretchblendnode_fs.findPlug("blender", False)
                    liknofliplowerlegstretchblendnodeinp1g_plug = liknofliplowerlegstretchblendnode_fs.findPlug("color1G", False)
                    liknofliplowerlegstretchblendnodeotp_plug = liknofliplowerlegstretchblendnode_fs.findPlug("outputG", False)
                    liknofliplowerlegstretchblendnodeblender_plug = liknofliplowerlegstretchblendnode_fs.findPlug("blender", False)

                    self.MDG2_mod.disconnect(noflipleftkneekeyotp_plug, nofliplefkneejnttty_plug)
                    self.MDG2_mod.disconnect(noflipleftfootkeyotp_plug, noflipleftfootjntty_plug)
                    self.MDG2_mod.connect(iklegctrlkneeupperleg_plug, ikautokneeupperlegInp1Y_plug)
                    self.MDG2_mod.connect(noflipleftkneekeyotp_plug, ikautokneeupperlegInp2Y_plug)
                    self.MDG2_mod.connect(iklegctrlkneelowerleg_plug, ikautokneelowerlegInp1Y_plug)
                    self.MDG2_mod.connect(noflipleftfootkeyotp_plug, ikautokneelowerlegInp2Y_plug)
                    self.MDG2_mod.connect(ikautokneeupperlegOtp_plug, liknoflipupperlegstretchblendnodeinp1g_plug)
                    self.MDG2_mod.connect(ikautokneelowerlegOtp_plug, liknofliplowerlegstretchblendnodeinp1g_plug)
                    self.MDG2_mod.connect(liknoflipupperlegstretchblendnodeotp_plug, nofliplefkneejnttty_plug)
                    self.MDG2_mod.connect(liknofliplowerlegstretchblendnodeotp_plug, noflipleftfootjntty_plug)
                    self.MDG2_mod.connect(ikleftlegstretch_plug, liknoflipupperlegstretchblendnodeblender_plug)
                    self.MDG2_mod.connect(ikleftlegstretch_plug, liknofliplowerlegstretchblendnodeblender_plug)
                    self.MDG2_mod.commandToExecute('float $noflipikleftlegtranslateY = `getAttr "NoFlipLeftUpperLegStretch_blend.color1G"`; setAttr "NoFlipLeftUpperLegStretch_blend.color2G" $noflipikleftlegtranslateY;')
                    self.MDG2_mod.commandToExecute('float $noflipikleftfoottranslateY = `getAttr "NoFlipLeftLowerLegStretch_blend.color1G"`; setAttr "NoFlipLeftLowerLegStretch_blend.color2G" $noflipikleftfoottranslateY;')
                    self.MDG2_mod.commandToExecute('setAttr "NoFlipLeftLegTrans_multiply.operation" 1')
                    self.MDG2_mod.commandToExecute('setAttr "NoFlipLeftFootTrans_multiply.operation" 1')

                    rightlegglobalscalenode = self.MDG2_mod.createNode("multiplyDivide")
                    nofliprightlegglobalscalenode = self.MDG2_mod.createNode("multiplyDivide")
                    nofliprightfootlobalscalenode = self.MDG2_mod.createNode("multiplyDivide")
                    self.MDG2_mod.renameNode(rightlegglobalscalenode, "IKLeftLegGlobalScale_Average")
                    self.MDG2_mod.renameNode(nofliprightlegglobalscalenode, "IKNoFlipLeftLegGlobalScale_Average")
                    self.MDG2_mod.renameNode(nofliprightfootlobalscalenode, "IKNoFlipLeftFootGlobalScale_Average")

                    leftlegglobalscale_fs = om2.MFnDependencyNode(rightlegglobalscalenode)
                    noflipleftlegglobalscale_fs = om2.MFnDependencyNode(nofliprightlegglobalscalenode)
                    noflipleftfootlobalscale_fs = om2.MFnDependencyNode(nofliprightfootlobalscalenode)
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

                    self.MDG2_mod.disconnect(liklegjntDist_plug, noflipleftkneekeyinp_plug)
                    self.MDG2_mod.disconnect(liklegjntDist_plug, noflipleftfootkeyinp_plug)
                    self.MDG2_mod.disconnect(liklegjntDist_plug, pvleftkneekeyinp_plug)
                    self.MDG2_mod.disconnect(liklegjntDist_plug, pvleftfootkeyinp_plug)
                    self.MDG2_mod.connect(liklowerlegjntDist_plug, noflipleftfootlobalscaleInp1Y_plug)
                    self.MDG2_mod.connect(likupperlegjntDist_plug, noflipleftlegglobalscaleInp1Y_plug)
                    self.MDG2_mod.connect(liklowerlegjntDist_plug, noflipleftfootlobalscaleInp1Y_plug)
                    self.MDG2_mod.connect(masterlctrlsy_plug, noflipleftlegglobalscaleInp2Y_plug)
                    self.MDG2_mod.connect(masterlctrlsy_plug, noflipleftfootlobalscaleInp2Y_plug)
                    self.MDG2_mod.connect(noflipleftlegglobalscaleOtpY_plug, likpvuppertransblendnodeinp1g_plug)
                    self.MDG2_mod.connect(noflipleftfootlobalscaleOtpY_plug, likpvlowertransblendnodeinp1g_plug)
                    self.MDG2_mod.connect(liklegjntDist_plug, leftlegglobalscaleInp1Y_plug)
                    self.MDG2_mod.connect(masterlctrlsy_plug, leftlegglobalscaleInp2Y_plug)
                    self.MDG2_mod.connect(leftlegglobalscaleOtpY_plug, noflipleftkneekeyinp_plug)
                    self.MDG2_mod.connect(leftlegglobalscaleOtpY_plug, noflipleftfootkeyinp_plug)
                    self.MDG2_mod.connect(leftlegglobalscaleOtpY_plug, pvleftkneekeyinp_plug)
                    self.MDG2_mod.connect(leftlegglobalscaleOtpY_plug, pvleftfootkeyinp_plug)
                    self.MDG2_mod.commandToExecute('setAttr "IKNoFlipLeftLegGlobalScale_Average.operation" 2')
                    self.MDG2_mod.commandToExecute('setAttr "IKNoFlipLeftFootGlobalScale_Average.operation" 2')
                    self.MDG2_mod.commandToExecute('setAttr "IKLeftLegGlobalScale_Average.operation" 2')
                    self.MDG2_mod.connect(masterdecomposeOtpScale_plug, ikleftjointleggrps_plug)

                # else:
                #     self.MDG2_mod.commandToExecute('delete "IkStretchyLeftJointLeg_grp"')
                #     self.MDG2_mod.commandToExecute('delete "LeftLegIkCluster_grp"')

                self.MDG2_mod.commandToExecute('addAttr -longName "footrollswitch" -niceName "Auto/Manual Foot Roll" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_LeftFootOptions_ctrl')

                self.MDG2_mod.commandToExecute('addAttr -longName "autoroll" -niceName "Auto Roll" -attributeType "enum" -en "__________:" -keyable true Biped_IkLeftFoot_ctrl')
                self.MDG2_mod.commandToExecute('addAttr -longName "roll" -niceName "Roll" -attributeType double -minValue -90 -keyable true -defaultValue 0 Biped_IkLeftFoot_ctrl')
                self.MDG2_mod.commandToExecute('addAttr -longName "bendlimitangle" -niceName "Bend Limit Angle" -attributeType double -keyable true -defaultValue 45 Biped_IkLeftFoot_ctrl')
                self.MDG2_mod.commandToExecute('addAttr -longName "toestraightangle" -niceName "Toe Straight Angle" -attributeType double -keyable true -defaultValue 70 Biped_IkLeftFoot_ctrl')
                self.MDG2_mod.commandToExecute('addAttr -longName "manualroll" -niceName "Manual Roll" -attributeType "enum" -en "__________:" -keyable true Biped_IkLeftFoot_ctrl')
                self.MDG2_mod.commandToExecute('addAttr -longName "heelroll" -niceName "Heel Roll" -attributeType double -keyable true -defaultValue 0 Biped_IkLeftFoot_ctrl')
                self.MDG2_mod.doIt()

                likheelclampnode = self.MDG2_mod.createNode("clamp")
                self.MDG2_mod.renameNode(likheelclampnode, "LeftHeel_rotclamp")
                likheelblendernode = self.MDG2_mod.createNode("blendColors")
                self.MDG2_mod.renameNode(likheelblendernode, "LeftHeel_blend")
                leg_reverse_sl_ls = om2.MSelectionList()
                leg_reverse_sl_ls.add("LeftReverseFootHeel")
                reverse_heel_obj = leg_reverse_sl_ls.getDependNode(0)

                likheelclamp_fs = om2.MFnDependencyNode(likheelclampnode)
                likheelblender_fs = om2.MFnDependencyNode(likheelblendernode)
                reverseheel_fs = om2.MFnDependencyNode(reverse_heel_obj)

                llegoptionsfootrollswitch_plug = llegoptions_fs.findPlug("footrollswitch", False)
                likheelblender_plug = likheelblender_fs.findPlug("blender", False)
                iklegctrlRoll_plug = iklegctrl_fs.findPlug("roll", False)
                likheelclampInpR_plug = likheelclamp_fs.findPlug("inputR", False)
                likheelclampOtpR_plug = likheelclamp_fs.findPlug("outputR", False)
                likheelblendCol2R_plug = likheelblender_fs.findPlug("color2R", False)
                iklegctrlHeelRoll_plug = iklegctrl_fs.findPlug("heelroll", False)
                likheelblendCol1R_plug = likheelblender_fs.findPlug("color1R", False)
                likheelblendOtpR_plug = likheelblender_fs.findPlug("outputR", False)
                likheelclampInpX_plug = reverseheel_fs.findPlug("rotateX", False)

                self.MDG2_mod.connect(llegoptionsfootrollswitch_plug, likheelblender_plug)
                self.MDG2_mod.connect(iklegctrlRoll_plug, likheelclampInpR_plug)
                self.MDG2_mod.connect(likheelclampOtpR_plug, likheelblendCol2R_plug)
                self.MDG2_mod.connect(iklegctrlHeelRoll_plug, likheelblendCol1R_plug)
                self.MDG2_mod.connect(likheelblendOtpR_plug, likheelclampInpX_plug)
                self.MDG2_mod.commandToExecute('setAttr "LeftHeel_rotclamp.minR" -90')

                self.MDG2_mod.commandToExecute('addAttr -longName "footroll" -niceName "Foot Roll" -attributeType double -keyable true -defaultValue 0 Biped_IkLeftFoot_ctrl')
                self.MDG2_mod.doIt()

                likballclampnode = self.MDG2_mod.createNode("clamp")
                self.MDG2_mod.renameNode(likballclampnode, "LeftBall_rotclamp")
                likballrangenode = self.MDG2_mod.createNode("setRange")
                self.MDG2_mod.renameNode(likballrangenode, "LeftBall_range")
                likballblendernode = self.MDG2_mod.createNode("blendColors")
                self.MDG2_mod.renameNode(likballblendernode, "LeftBall_blend")
                likballminusnode = self.MDG2_mod.createNode("plusMinusAverage")
                self.MDG2_mod.renameNode(likballminusnode, "LeftBall_minus")
                likballmultnode = self.MDG2_mod.createNode("multiplyDivide")
                self.MDG2_mod.renameNode(likballmultnode, "LeftBall_percetmult")
                likballrollmultnode = self.MDG2_mod.createNode("multiplyDivide")
                self.MDG2_mod.renameNode(likballrollmultnode, "LeftBall_rollmult")
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

                self.MDG2_mod.connect(llegoptionsfootrollswitch_plug, likballblender_plug)
                self.MDG2_mod.connect(iklegctrlRoll_plug, likballclampInpR_plug)
                self.MDG2_mod.connect(iklegctrlBendLimit_plug, likballclampMaxR_plug)
                self.MDG2_mod.connect(likballclampInpR_plug, likballrangeValueX_plug)
                self.MDG2_mod.connect(likballclampMinR_plug, likballrangeOldMinX_plug)
                self.MDG2_mod.connect(likballclampMaxR_plug, likballrangeOldMaxX_plug)
                self.MDG2_mod.connect(likballrangeOutValueX_plug, likballmultInp1X_plug)
                self.MDG2_mod.connect(likballsubOtp1D_plug, likballmultInp2X_plug)
                self.MDG2_mod.connect(likballmultOtpX_plug, likballrollmultInp1X_plug)
                self.MDG2_mod.connect(iklegctrlRoll_plug, likballrollmultInp2X_plug)
                self.MDG2_mod.connect(likballrollmultOtpX_plug, likballblendCol2R_plug)
                self.MDG2_mod.connect(iklegctrlBallRoll_plug, likballblendCol1R_plug)
                self.MDG2_mod.connect(likballblendOtpR_plug, likballclampRotX_plug)
                self.MDG2_mod.commandToExecute('setAttr "LeftBall_range.minX" 0')
                self.MDG2_mod.commandToExecute('setAttr "LeftBall_range.maxX" 1')
                self.MDG2_mod.commandToExecute('setAttr "LeftBall_minus.input1D[0]" 1')
                self.MDG2_mod.commandToExecute('setAttr "LeftBall_minus.operation" 2')
                self.MDG2_mod.commandToExecute('setAttr "LeftBall_percetmult.operation" 1')
                self.MDG2_mod.commandToExecute('setAttr "LeftBall_rollmult.operation" 1')

                self.MDG2_mod.commandToExecute('addAttr -longName "toeroll" -niceName "Toe Roll" -attributeType double -keyable true -defaultValue 0 Biped_IkLeftFoot_ctrl')
                self.MDG2_mod.doIt()

                liktoeclampnode = self.MDG2_mod.createNode("clamp")
                self.MDG2_mod.renameNode(liktoeclampnode, "LeftToe_rotclamp")
                liktoeblendernode = self.MDG2_mod.createNode("blendColors")
                self.MDG2_mod.renameNode(liktoeblendernode, "LeftToe_blend")
                liktoerangernode = self.MDG2_mod.createNode("setRange")
                self.MDG2_mod.renameNode(liktoerangernode, "LeftToe_range")
                liktoemultnode = self.MDG2_mod.createNode("multiplyDivide")
                self.MDG2_mod.renameNode(liktoemultnode, "LeftToe_percetmultiply")
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

                self.MDG2_mod.connect(llegoptionsfootrollswitch_plug, liktoeblender_plug)
                self.MDG2_mod.connect(iklegctrlRoll_plug, liktoeclampInpR_plug)
                self.MDG2_mod.connect(iklegctrlBendLimit_plug, liktoeclampMinR_plug)
                self.MDG2_mod.connect(iklegctrlStraightLimit_plug, liktoeclampMaxR_plug)
                self.MDG2_mod.connect(liktoeclampInpR_plug, liktoerangeValueX_plug)
                self.MDG2_mod.connect(liktoeclampMinR_plug, liktoerangeOldMinX_plug)
                self.MDG2_mod.connect(liktoeclampMaxR_plug, liktoerangeOldMaxX_plug)
                self.MDG2_mod.connect(liktoerangeoOutValX_plug, liktoemultInp1X_plug)
                self.MDG2_mod.connect(liktoeclampInpR_plug, liktoemultInp2X_plug)
                self.MDG2_mod.connect(liktoemultOtpX_plug, liktoeblendCol2R_plug)
                self.MDG2_mod.commandToExecute('connectAttr -force LeftToe_range.outValueX LeftBall_minus.input1D[1]')
                self.MDG2_mod.connect(iklegctrlToeRoll_plug, liktoeblendCol1R_plug)
                self.MDG2_mod.connect(liktoeblendOtpR_plug, liktoeclampRotX_plug)
                self.MDG2_mod.commandToExecute('setAttr "LeftToe_range.minX" 0')
                self.MDG2_mod.commandToExecute('setAttr "LeftToe_range.maxX" 1')
                self.MDG2_mod.commandToExecute('setAttr "LeftToe_percetmultiply.operation" 1')

                self.MDG2_mod.commandToExecute('addAttr -longName "common" -niceName "Common" -attributeType "enum" -en "__________:" -keyable true Biped_IkLeftFoot_ctrl')
                self.MDG2_mod.commandToExecute('addAttr -longName "tilt" -niceName "Tilt" -attributeType double -minValue -180 -maxValue 180 -keyable true -defaultValue 0 Biped_IkLeftFoot_ctrl')
                self.MDG2_mod.doIt()

                likinnerlegtiltclampnode = self.MDG2_mod.createNode("clamp")
                self.MDG2_mod.renameNode(likinnerlegtiltclampnode, "LeftInnerLegTilt_clamp")
                likouterlegtiltclampnode = self.MDG2_mod.createNode("clamp")
                self.MDG2_mod.renameNode(likouterlegtiltclampnode, "LeftOuterLegTilt_clamp")
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

                self.MDG2_mod.connect(iklegctrlTilt_plug, likinnerclampInpB_plug)
                self.MDG2_mod.connect(iklegctrlTilt_plug, likouterclampInpB_plug)
                self.MDG2_mod.connect(likinnerclampOtpB_plug, likinnerclampRotZ_plug)
                self.MDG2_mod.connect(likouterclampOtpB_plug, likouterclampRotZ_plug)
                self.MDG2_mod.commandToExecute('setAttr "LeftInnerLegTilt_clamp.maxB" 180')
                self.MDG2_mod.commandToExecute('setAttr "LeftOuterLegTilt_clamp.minB" -180')

                self.MDG2_mod.commandToExecute('addAttr -longName "lean" -niceName "Lean" -attributeType double -keyable true -defaultValue 0 Biped_IkLeftFoot_ctrl')
                self.MDG2_mod.commandToExecute('addAttr -longName "toespin" -niceName "Toe Spin" -attributeType double -keyable true -defaultValue 0 Biped_IkLeftFoot_ctrl')
                self.MDG2_mod.commandToExecute('addAttr -longName "toewiggle" -niceName "Toe Wiggle" -attributeType double -keyable true -defaultValue 0 Biped_IkLeftFoot_ctrl')
                self.MDG2_mod.doIt()

                leg_reverse_sl_ls.add("LeftReverseFootToeWiggle")
                reverse_toewiggle_obj = leg_reverse_sl_ls.getDependNode(5)

                reversetoewiggle_fs = om2.MFnDependencyNode(reverse_toewiggle_obj)

                iklegctrlLean_plug = iklegctrl_fs.findPlug("lean", False)
                likballclampRotZ_plug = reversetoe_fs.findPlug("rotateZ", False)
                iklegctrlToeSpin_plug = iklegctrl_fs.findPlug("toespin", False)
                liktoeclampRotY_plug = reversetoeend_fs.findPlug("rotateY", False)
                iklegctrlToeWiggle_plug = iklegctrl_fs.findPlug("toewiggle", False)
                reversetoewiggleRotX_plug = reversetoewiggle_fs.findPlug("rotateX", False)

                self.MDG2_mod.connect(iklegctrlLean_plug, likballclampRotZ_plug)
                self.MDG2_mod.connect(iklegctrlToeSpin_plug, liktoeclampRotY_plug)
                self.MDG2_mod.connect(iklegctrlToeWiggle_plug, reversetoewiggleRotX_plug)
        else:
            self.MDG2_mod.commandToExecute('delete "Biped_IkLeftFoot_null"')
            self.MDG2_mod.commandToExecute('delete "IkLeftJointLeg_grp"')
            self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false Biped_LeftFootOptions_ctrl.fkik')

        for index in range(fkrarm_sl_ls.length()):
            jnt_obj = fkrarm_sl_ls.getDependNode(index)
            jnt_string = fkrarm_sl_ls.getSelectionStrings(index)

            if jnt_obj.hasFn(om2.MFn.kJoint):
                rarmctrl_multMatrix = self.MDG2_mod.createNode("multMatrix")
                rarmctrl_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                self.MDG2_mod.renameNode(rarmctrl_multMatrix, str(jnt_string)[2:][:-3] + "_multMatrix")
                self.MDG2_mod.renameNode(rarmctrl_decomposeMatrix, str(jnt_string)[2:][:-3] + "_decomposeMatrix")

                rarmmultMatrix_fs = om2.MFnDependencyNode(rarmctrl_multMatrix)
                rarmdecomposeMatrix_fs = om2.MFnDependencyNode(rarmctrl_decomposeMatrix)
                rarmjnt_fs = om2.MFnDependencyNode(jnt_obj)

                rarmmultMatrixSum_plug = rarmmultMatrix_fs.findPlug("matrixSum", False)
                rarmdecomposeInpMatrix_plug = rarmdecomposeMatrix_fs.findPlug("inputMatrix", False)
                rarmdecomposeOtpTrans_plug = rarmdecomposeMatrix_fs.findPlug("outputTranslate", False)
                rarmdecomposeOtpRot_plug = rarmdecomposeMatrix_fs.findPlug("outputRotate", False)
                rarmjntTrans_plug = rarmjnt_fs.findPlug("translate", False)
                rarmjntRot_plug = rarmjnt_fs.findPlug("rotate", False)

                self.MDG2_mod.commandToExecute('connectAttr -force Biped_{0}_ctrl.worldMatrix[0] {0}_multMatrix.matrixIn[0]'.format(str(jnt_string)[3:][:-3]))
                self.MDG2_mod.commandToExecute('connectAttr -force {0}.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(jnt_string)[3:][:-3]))
                self.MDG2_mod.connect(rarmmultMatrixSum_plug, rarmdecomposeInpMatrix_plug)
                self.MDG2_mod.connect(rarmdecomposeOtpTrans_plug, rarmjntTrans_plug)
                self.MDG2_mod.connect(rarmdecomposeOtpRot_plug, rarmjntRot_plug)
                if cmds.getAttr("{0}.jointOrientX".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientY".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientZ".format(str(jnt_string)[3:][:-3])) != 0:
                    self.MDG2_mod.commandToExecute('setAttr "{0}.jointOrientX" 0'.format(str(jnt_string)[3:][:-3]))
                    self.MDG2_mod.commandToExecute('setAttr "{0}.jointOrientY" 0'.format(str(jnt_string)[3:][:-3]))
                    self.MDG2_mod.commandToExecute('setAttr "{0}.jointOrientZ" 0'.format(str(jnt_string)[3:][:-3]))

        fkrarm_sl_ls = om2.MSelectionList()
        fkrarm_sl_ls.add("FkRightArm")
        fkrarm_sl_ls.add("FkRightForeArm")
        fkrarm_sl_ls.add("FkRightHand")

        ikrarm_sl_ls = om2.MSelectionList()
        ikrarm_sl_ls.add("IkRightArm")
        ikrarm_sl_ls.add("IkRightForeArm")
        ikrarm_sl_ls.add("IkRightHand")

        noflipikrarm_sl_ls = om2.MSelectionList()
        noflipikrarm_sl_ls.add("IkNoFlipRightArm")
        noflipikrarm_sl_ls.add("IkNoFlipRightForeArm")
        noflipikrarm_sl_ls.add("IkNoFlipRightHand")

        pvikrarm_sl_ls = om2.MSelectionList()
        pvikrarm_sl_ls.add("IkPVRightArm")
        pvikrarm_sl_ls.add("IkPVRightForeArm")
        pvikrarm_sl_ls.add("IkPVRightHand")

        rhandoptions_sl_ls = om2.MSelectionList()
        rhandoptions_sl_ls.add("Biped_RightHandOptions_ctrl")
        rhandoptions_obj = rhandoptions_sl_ls.getDependNode(0)

        self.MDG2_mod.commandToExecute('addAttr -longName "stretchy" -niceName "Stretchy" -attributeType double -keyable true -defaultValue 0 Biped_FkRightArm_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "stretchy" -niceName "Stretchy" -attributeType double -keyable true -defaultValue 0 Biped_FkRightForeArm_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "fkik" -niceName "Fk/Ik" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_RightHandOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "kneeswitch" -niceName "Auto/Manual Knee" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_RightHandOptions_ctrl')
        self.MDG2_mod.doIt()

        rhandoptions_fs = om2.MFnDependencyNode(rhandoptions_obj)
        rhandoptionsfkik_plug = rhandoptions_fs.findPlug("fkik", False)
        rhandoptionskneeswitch_plug = rhandoptions_fs.findPlug("kneeswitch", False)

        for index in range(rarm_sl_ls.length()):
            fkjnt_obj = fkrarm_sl_ls.getDependNode(index)

            ikjnt_obj = ikrarm_sl_ls.getDependNode(index)
            ikjnt_string = ikrarm_sl_ls.getSelectionStrings(index)

            bindjnt_obj = rarm_sl_ls.getDependNode(index)
            bindjnt_string = rarm_sl_ls.getSelectionStrings(index)

            noflipjnt_obj = noflipikrarm_sl_ls.getDependNode(index)
            noflipjnt_string = noflipikrarm_sl_ls.getSelectionStrings(index)

            pvjnt_obj = pvikrarm_sl_ls.getDependNode(index)
            pvjnt_string = pvikrarm_sl_ls.getSelectionStrings(index)

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

                fkarmjointtransotp_plug = fkarmjoint_fs.findPlug("translate", False)
                fkarmjointrototp_plug = fkarmjoint_fs.findPlug("rotate", False)
                armjointtransinp_plug = armjoint_fs.findPlug("translate", False)
                armjointrotinp_plug = armjoint_fs.findPlug("rotate", False)

                if cmds.objExists("NoFlipRightHand_Ik") and cmds.objExists("PVRightHand_Ik"):
                    armrotblendnode = self.MDG2_mod.createNode("blendColors")
                    armtransblendnode = self.MDG2_mod.createNode("blendColors")
                    armjoint_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                    self.MDG2_mod.renameNode(armjoint_decomposeMatrix, str(bindjnt_string)[2:][:-3] + "Blend_decomposeMatrix")
                    self.MDG2_mod.renameNode(armrotblendnode, str(bindjnt_string)[2:][:-3] + "_blend")

                    armrotblendnode_fs = om2.MFnDependencyNode(armrotblendnode)
                    armtransblendnode_fs = om2.MFnDependencyNode(armtransblendnode)
                    armdecomposeMatrix_fs = om2.MFnDependencyNode(armjoint_decomposeMatrix)
                    ikarmjoint_fs = om2.MFnDependencyNode(ikjnt_obj)

                    armdecomposeInpMatrix_plug = armdecomposeMatrix_fs.findPlug("inputMatrix", False)
                    armdecomposeOtpRot_plug = armdecomposeMatrix_fs.findPlug("outputRotate", False)
                    armdecomposeOtpTrans_plug = armdecomposeMatrix_fs.findPlug("outputTranslate", False)
                    armrotblendnodeinp1_plug = armrotblendnode_fs.findPlug("color1", False)
                    armrotblendnodeinp2_plug = armrotblendnode_fs.findPlug("color2", False)
                    armrotblendnodeotp_plug = armrotblendnode_fs.findPlug("output", False)
                    armrotblendnodeblender_plug = armrotblendnode_fs.findPlug("blender", False)
                    armtransblendnodeinp1_plug = armtransblendnode_fs.findPlug("color1", False)
                    armtransblendnodeinp2_plug = armtransblendnode_fs.findPlug("color2", False)
                    armtransblendnodeotp_plug = armtransblendnode_fs.findPlug("output", False)
                    armtransblendnodeblender_plug = armtransblendnode_fs.findPlug("blender", False)
                    ikarmjointrototp_plug = ikarmjoint_fs.findPlug("matrix", False)

                    self.MDG2_mod.connect(ikarmjointrototp_plug, armdecomposeInpMatrix_plug)
                    self.MDG2_mod.connect(armdecomposeOtpRot_plug, armrotblendnodeinp1_plug)
                    self.MDG2_mod.connect(armdecomposeOtpTrans_plug, armtransblendnodeinp1_plug)
                    self.MDG2_mod.connect(fkarmjointrototp_plug, armrotblendnodeinp2_plug)
                    self.MDG2_mod.connect(fkarmjointtransotp_plug, armtransblendnodeinp2_plug)
                    self.MDG2_mod.connect(armrotblendnodeotp_plug, armjointrotinp_plug)
                    self.MDG2_mod.connect(armtransblendnodeotp_plug, armjointtransinp_plug)
                    self.MDG2_mod.connect(rhandoptionsfkik_plug, armrotblendnodeblender_plug)
                    self.MDG2_mod.connect(rhandoptionsfkik_plug, armtransblendnodeblender_plug)

                    armrotblendnode = self.MDG2_mod.createNode("blendColors")
                    armtransblendnode = self.MDG2_mod.createNode("blendColors")
                    nofliparmjoint_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                    pvarmjoint_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                    self.MDG2_mod.renameNode(nofliparmjoint_decomposeMatrix, str(noflipjnt_string)[2:][:-3]+"Blend_decomposeMatrix")
                    self.MDG2_mod.renameNode(pvarmjoint_decomposeMatrix, str(pvjnt_string)[2:][:-3]+"Blend_decomposeMatrix")
                    self.MDG2_mod.renameNode(armrotblendnode, str(bindjnt_string)[2:][:-3]+"Rot_kneeblend")
                    self.MDG2_mod.renameNode(armtransblendnode, str(bindjnt_string)[2:][:-3]+"Trans_kneeblend")

                    armrotblendnode_fs = om2.MFnDependencyNode(armrotblendnode)
                    armtransblendnode_fs = om2.MFnDependencyNode(armtransblendnode)
                    nofliparmdecomposeMatrix_fs = om2.MFnDependencyNode(nofliparmjoint_decomposeMatrix)
                    pvarmdecomposeMatrix_fs = om2.MFnDependencyNode(pvarmjoint_decomposeMatrix)
                    noflipikarmjoint_fs = om2.MFnDependencyNode(noflipjnt_obj)
                    pvikarmjoint_fs = om2.MFnDependencyNode(pvjnt_obj)

                    nofliparmdecomposeInpMatrix_plug = nofliparmdecomposeMatrix_fs.findPlug("inputMatrix", False)
                    nofliparmdecomposeOtpRot_plug = nofliparmdecomposeMatrix_fs.findPlug("outputRotate", False)
                    nofliparmdecomposeOtpTrans_plug = nofliparmdecomposeMatrix_fs.findPlug("outputTranslate", False)
                    pvarmdecomposeInpMatrix_plug = pvarmdecomposeMatrix_fs.findPlug("inputMatrix", False)
                    pvarmdecomposeOtpRot_plug = pvarmdecomposeMatrix_fs.findPlug("outputRotate", False)
                    pvarmdecomposeOtpTrans_plug = pvarmdecomposeMatrix_fs.findPlug("outputTranslate", False)
                    armrotblendnodeinp1_plug = armrotblendnode_fs.findPlug("color1", False)
                    armrotblendnodeinp2_plug = armrotblendnode_fs.findPlug("color2", False)
                    armrotblendnodeotp_plug = armrotblendnode_fs.findPlug("output", False)
                    armrotblendnodeblender_plug = armrotblendnode_fs.findPlug("blender", False)
                    armtransblendnodeinp1_plug = armtransblendnode_fs.findPlug("color1", False)
                    armtransblendnodeinp2_plug = armtransblendnode_fs.findPlug("color2", False)
                    armtransblendnodeotp_plug = armtransblendnode_fs.findPlug("output", False)
                    armtransblendnodeblender_plug = armtransblendnode_fs.findPlug("blender", False)
                    noflipikarmjointotp_plug = noflipikarmjoint_fs.findPlug("matrix", False)
                    pvikarmjointotp_plug = pvikarmjoint_fs.findPlug("matrix", False)
                    ikarmjointinpTrans_plug = ikarmjoint_fs.findPlug("translate", False)
                    ikarmjointinpRot_plug = ikarmjoint_fs.findPlug("jointOrient", False)

                    self.MDG2_mod.connect(noflipikarmjointotp_plug, nofliparmdecomposeInpMatrix_plug)
                    self.MDG2_mod.connect(pvikarmjointotp_plug, pvarmdecomposeInpMatrix_plug)
                    self.MDG2_mod.connect(pvarmdecomposeOtpRot_plug, armrotblendnodeinp1_plug)
                    self.MDG2_mod.connect(pvarmdecomposeOtpTrans_plug, armtransblendnodeinp1_plug)
                    self.MDG2_mod.connect(nofliparmdecomposeOtpRot_plug, armrotblendnodeinp2_plug)
                    self.MDG2_mod.connect(nofliparmdecomposeOtpTrans_plug, armtransblendnodeinp2_plug)
                    self.MDG2_mod.connect(armrotblendnodeotp_plug, ikarmjointinpRot_plug)
                    self.MDG2_mod.connect(armtransblendnodeotp_plug, ikarmjointinpTrans_plug)
                    self.MDG2_mod.connect(rhandoptionskneeswitch_plug, armrotblendnodeblender_plug)
                    self.MDG2_mod.connect(rhandoptionskneeswitch_plug, armtransblendnodeblender_plug)

                else:
                    self.MDG2_mod.connect(fkarmjointtransotp_plug, armjointtransinp_plug)
                    self.MDG2_mod.connect(fkarmjointrototp_plug, armjointrotinp_plug)

            if self.autostretch.currentIndex() == 1:
                if index < 2:
                    ikrarmgrp_sl_lst = om2.MSelectionList()
                    ikrarmgrp_sl_lst.add("RightUpperArmIkCluster_grp")
                    ikrarmgrp_sl_lst.add("RightUpperArmIkCluster2_grp")
                    ikrarmgrp_sl_lst.add("RightLowerArmIkCluster_grp")
                    ikrarmgrp_sl_lst.add("RightLowerArmIkCluster2_grp")
                    grp_armupperikcluster = ikrarmgrp_sl_lst.getDependNode(0)
                    grp_armupperikcluster2 = ikrarmgrp_sl_lst.getDependNode(1)
                    grp_armlowerikcluster = ikrarmgrp_sl_lst.getDependNode(2)
                    grp_armlowerikcluster2 = ikrarmgrp_sl_lst.getDependNode(3)

                    rarmjoint_multMatrix = self.MDG2_mod.createNode("multMatrix")
                    armjoint_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")

                    rarmmultMatrix_fs = om2.MFnDependencyNode(rarmjoint_multMatrix)
                    rarmdecomposeMatrix_fs = om2.MFnDependencyNode(armjoint_decomposeMatrix)
                    ikrupperarmgrp_fs = om2.MFnDependencyNode(grp_armupperikcluster)
                    ikrlowerarmgrp_fs = om2.MFnDependencyNode(grp_armlowerikcluster)

                    rarmmultMatrixSum_plug = rarmmultMatrix_fs.findPlug("matrixSum", False)
                    rarmdecomposeInpMatrix_plug = rarmdecomposeMatrix_fs.findPlug("inputMatrix", False)
                    rarmdecomposeOtpTrans_plug = rarmdecomposeMatrix_fs.findPlug("outputTranslate", False)
                    rarmdecomposeOtpRot_plug = rarmdecomposeMatrix_fs.findPlug("outputRotate", False)
                    ikrupperarmgrpTrans_plug = ikrupperarmgrp_fs.findPlug("translate", False)
                    ikrupperarmgrpRot_plug = ikrupperarmgrp_fs.findPlug("rotate", False)
                    ikrlowerarmgrpTrans_plug = ikrlowerarmgrp_fs.findPlug("translate", False)
                    ikrlowerarmgrpRot_plug = ikrlowerarmgrp_fs.findPlug("rotate", False)

                    self.MDG2_mod.renameNode(rarmjoint_multMatrix, str(bindjnt_string)[2:][:-3]+"_multMatrix")
                    self.MDG2_mod.renameNode(armjoint_decomposeMatrix, str(bindjnt_string)[2:][:-3]+"_decomposeMatrix")
                    self.MDG2_mod.commandToExecute('connectAttr -force {0}.worldMatrix[0] {0}_multMatrix.matrixIn[0]'.format(str(bindjnt_string)[3:][:-3]))
                    self.MDG2_mod.connect(rarmmultMatrixSum_plug, rarmdecomposeInpMatrix_plug)

                    fkrarmstretch_expression = om1.MFnExpression()

                    if index == 0:
                        fkrarmstretch_expression.create("Biped_FkRightForeArm_ctrl.translateY = Biped_FkRightArm_ctrl.stretchy")
                        fkrarmstretch_expression.create("Biped_FkRightForeArm_ctrl.translateZ = Biped_FkRightForeArm_ctrl.translateY/10")
                        fkrarmstretch_expression.create("Biped_FkRightForeArm_ctrl.translateX = Biped_FkRightForeArm_ctrl.translateY/10")

                        self.MDG2_mod.commandToExecute('connectAttr -force RightUpperArmIkCluster_grp.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(bindjnt_string)[3:][:-3]))
                        self.MDG2_mod.connect(rarmdecomposeOtpTrans_plug, ikrupperarmgrpTrans_plug)
                        self.MDG2_mod.connect(rarmdecomposeOtpRot_plug, ikrupperarmgrpRot_plug)

                        rupperarmcluster2_multMatrix = self.MDG2_mod.createNode("multMatrix")
                        lupperarmcluster2_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")

                        rupperarmcluster2multMatrix_fs = om2.MFnDependencyNode(rupperarmcluster2_multMatrix)
                        rupperarmcluster2decomposeMatrix_fs = om2.MFnDependencyNode(lupperarmcluster2_decomposeMatrix)
                        rupperarmcluster2_fs = om2.MFnDependencyNode(grp_armupperikcluster2)

                        rupperarmcluster2multMatrixSum_plug = rupperarmcluster2multMatrix_fs.findPlug("matrixSum", False)
                        rupperarmcluster2decomposeInpMatrix_plug = rupperarmcluster2decomposeMatrix_fs.findPlug("inputMatrix", False)
                        rupperarmcluster2decomposeOtpTrans_plug = rupperarmcluster2decomposeMatrix_fs.findPlug("outputTranslate", False)
                        rupperarmcluster2Trans_plug = rupperarmcluster2_fs.findPlug("translate", False)

                        self.MDG2_mod.renameNode(rupperarmcluster2_multMatrix, "RightUpperArmCluster2_multMatrix")
                        self.MDG2_mod.renameNode(lupperarmcluster2_decomposeMatrix,"RightUpperArmCluster2_decomposeMatrix")
                        self.MDG2_mod.connect(rupperarmcluster2multMatrixSum_plug, rupperarmcluster2decomposeInpMatrix_plug)
                        self.MDG2_mod.commandToExecute('connectAttr -force RightForeArm.worldMatrix[0] RightUpperArmCluster2_multMatrix.matrixIn[0]')
                        self.MDG2_mod.commandToExecute('connectAttr -force RightUpperArmIkCluster2_grp.parentInverseMatrix[0] RightUpperArmCluster2_multMatrix.matrixIn[1]')
                        self.MDG2_mod.connect(rupperarmcluster2decomposeOtpTrans_plug, rupperarmcluster2Trans_plug)

                    elif index == 1:
                        fkrarmstretch_expression.create("Biped_FkRightHand_ctrl.translateY = Biped_FkRightForeArm_ctrl.stretchy")

                        self.MDG2_mod.commandToExecute('connectAttr -force RightLowerArmIkCluster_grp.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(bindjnt_string)[3:][:-3]))
                        self.MDG2_mod.connect(rarmdecomposeOtpTrans_plug, ikrlowerarmgrpTrans_plug)
                        self.MDG2_mod.connect(rarmdecomposeOtpRot_plug, ikrlowerarmgrpRot_plug)

                        rlowerarmcluster2_multMatrix = self.MDG2_mod.createNode("multMatrix")
                        rlowerarmcluster2_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")

                        rlowerarmcluster2multMatrix_fs = om2.MFnDependencyNode(rlowerarmcluster2_multMatrix)
                        rlowerarmcluster2decomposeMatrix_fs = om2.MFnDependencyNode(rlowerarmcluster2_decomposeMatrix)
                        rlowerarmcluster2_fs = om2.MFnDependencyNode(grp_armlowerikcluster2)

                        rlowerarmcluster2multMatrixSum_plug = rlowerarmcluster2multMatrix_fs.findPlug("matrixSum", False)
                        rlowerarmcluster2decomposeInpMatrix_plug = rlowerarmcluster2decomposeMatrix_fs.findPlug("inputMatrix", False)
                        rlowerarmcluster2decomposeOtpTrans_plug = rlowerarmcluster2decomposeMatrix_fs.findPlug("outputTranslate", False)
                        rlowerarmcluster2Trans_plug = rlowerarmcluster2_fs.findPlug("translate", False)

                        self.MDG2_mod.renameNode(rlowerarmcluster2_multMatrix, "RightLowerArmCluster2_multMatrix")
                        self.MDG2_mod.renameNode(rlowerarmcluster2_decomposeMatrix,"RightLowerArmCluster2_decomposeMatrix")
                        self.MDG2_mod.commandToExecute('connectAttr -force RightHand.worldMatrix[0] RightLowerArmCluster2_multMatrix.matrixIn[0]')
                        self.MDG2_mod.commandToExecute('connectAttr -force RightLowerArmIkCluster2_grp.parentInverseMatrix[0] RightLowerArmCluster2_multMatrix.matrixIn[1]')
                        self.MDG2_mod.connect(rlowerarmcluster2multMatrixSum_plug, rlowerarmcluster2decomposeInpMatrix_plug)
                        self.MDG2_mod.connect(rlowerarmcluster2decomposeOtpTrans_plug, rlowerarmcluster2Trans_plug)

            elif cmds.objExists("RightArmIkCluster_grp") and cmds.objExists("IkStretchyRightJointArm_grp"):
                self.MDG2_mod.commandToExecute('delete "RightArmIkCluster_grp"')
                self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false Biped_FkRightArm_ctrl.stretchy')
                self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false Biped_FkRightForeArm_ctrl.stretchy')
                self.MDG2_mod.doIt()

        grp_armupperikcluster1 = om1.MObject()
        grp_armupperikcluster2 = om1.MObject()
        obj_stretchyrightarm = om1.MObject()

        if self.autostretch.currentIndex() == 1:

            self.MDG2_mod.commandToExecute('addAttr -longName "stretchable" -niceName "Stretchable" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_RightHandOptions_ctrl')
            self.MDG2_mod.doIt()

            stretchy_sl_lst1.add("Biped_RightHandOptions_ctrl")
            stretchy_sl_lst1.getDependNode(4, obj_stretchyrightarm)

            if cmds.objExists("IkSplineRightUpperArm0"):
                ikrupperarm_sl_lst = om1.MSelectionList()
                ikrupperarm_sl_lst.add("IkSplineRightUpperArm*")
                ikrupperarm_sl_lst.getDependNode(0, obj_root)
                ikrupperarm_sl_lst.getDependNode(ikrupperarm_sl_lst.length()-1, obj_endspine)

                ikrupperarmgrp_sl_lst = om1.MSelectionList()
                ikrupperarmgrp_sl_lst.add("RightUpperArmIkCluster1_grp")
                ikrupperarmgrp_sl_lst.add("RightUpperArmIkCluster2_grp")
                ikrupperarmgrp_sl_lst.getDependNode(0, grp_armupperikcluster1)
                ikrupperarmgrp_sl_lst.getDependNode(1, grp_armupperikcluster2)

                self.MDag_path = om1.MDagPath()
                rootspine_path = self.MDag_path.getAPathTo(obj_root)

                try:
                    ikspineiksolver_lst.add("ikSplineSolver*")
                except:
                    cmds.createNode("ikSplineSolver")

                self.ikrarm_effector = self.IK_Effector.create(obj_endspine)
                ikrarm_effector_path = self.MDag_path.getAPathTo(self.ikrarm_effector)

                self.rarm_ik = self.IK_Handle.create(rootspine_path, ikrarm_effector_path)

                obj_array = om1.MPointArray()
                obj_lst_mpoint = []
                obj = om1.MObject()
                for index in range(ikrupperarm_sl_lst.length()):
                    ikrupperarm_sl_lst.getDependNode(index, obj)
                    obj_path = self.MDag_path.getAPathTo(obj)
                    obj_tn = om1.MFnTransform(obj_path)
                    obj_t = obj_tn.translation(om1.MSpace.kWorld)
                    obj_lst_mpoint.append(om1.MPoint(obj_t))
                    obj_array.append(obj_lst_mpoint[index])

                self.ikspline_cv_tn = ikspinedag_n.create("transform", "RightUpperArm_SplineCv")
                ikspline_cv = self.MNurbs1_cv.createWithEditPoints(obj_array, 1, 1, False, True, True, self.ikspline_cv_tn)
                cmds.parent("RightUpperArm_SplineCv", "DoNotTouch")

                rarmcrv_info = ikspinedg_modifier.createNode("curveInfo")
                rarmstretchpercent = ikspinedg_modifier.createNode("multiplyDivide")
                rarmstretchpow = ikspinedg_modifier.createNode("multiplyDivide")
                rarmstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                rarmscalediv = ikspinedg_modifier.createNode("multiplyDivide")
                rikarmstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                blendstretch = ikspinedg_modifier.createNode("blendColors")

                rarmcrvinfo_fs = om1.MFnDependencyNode(rarmcrv_info)
                rarmstretchpercent_fs = om1.MFnDependencyNode(rarmstretchpercent)
                rarmstretchpow_fs = om1.MFnDependencyNode(rarmstretchpow)
                rarmstretchdiv_fs = om1.MFnDependencyNode(rarmstretchdiv)
                rarmscalediv_fs = om1.MFnDependencyNode(rarmscalediv)
                rikarmstretchdiv_fs = om1.MFnDependencyNode(rikarmstretchdiv)
                rikarmstretchcluster1_fs = om1.MFnDependencyNode(grp_armupperikcluster1)
                rikarmstretchcluster2_fs = om1.MFnDependencyNode(grp_armupperikcluster2)
                blendstretch_fs = om1.MFnDependencyNode(blendstretch)
                rhandstretchoption_fs = om1.MFnDependencyNode(obj_stretchyrightarm)

                rarmcrvinfoarc_plug = rarmcrvinfo_fs.findPlug("arcLength")
                rarmstretchpercentinp1y_plug = rarmstretchpercent_fs.findPlug("input1Y")
                rarmstretchpercentotp_plug = rarmstretchpercent_fs.findPlug("outputY")
                rarmstretchpowinp1x_plug = rarmstretchpow_fs.findPlug("input1X")
                rarmstretchpowinp1z_plug = rarmstretchpow_fs.findPlug("input1Z")
                rarmstretchpowotpx_plug = rarmstretchpow_fs.findPlug("outputX")
                rarmstretchpowotpz_plug = rarmstretchpow_fs.findPlug("outputZ")
                rarmstretchdivinp2x_plug = rarmstretchdiv_fs.findPlug("input2X")
                rarmstretchdivinp2z_plug = rarmstretchdiv_fs.findPlug("input2Z")
                rarmstretchdivotox_plug = rarmstretchdiv_fs.findPlug("outputX")
                rarmstretchdivotpz_plug = rarmstretchdiv_fs.findPlug("outputZ")
                rarmscaledivinp1y_plug = rarmscalediv_fs.findPlug("input1Y")
                rarmscaledivinp2y_plug = rarmscalediv_fs.findPlug("input2Y")
                rarmscaledivotpy_plug = rarmscalediv_fs.findPlug("outputY")
                rikarmstretchdivinp1_plug = rikarmstretchdiv_fs.findPlug("input1")
                rikarmstretchdivotp_plug = rikarmstretchdiv_fs.findPlug("output")
                rikarmstretchclust1trans_plug = rikarmstretchcluster1_fs.findPlug("translate")
                rikarmstretchclust2trans_plug = rikarmstretchcluster2_fs.findPlug("translate")
                blendstretchinp1r_plug = blendstretch_fs.findPlug("color1R")
                blendstretchinp1g_plug = blendstretch_fs.findPlug("color1G")
                blendstretchinp1b_plug = blendstretch_fs.findPlug("color1B")
                blendstretchotpr_plug = blendstretch_fs.findPlug("outputR")
                blendstretchotpg_plug = blendstretch_fs.findPlug("outputG")
                blendstretchotpb_plug = blendstretch_fs.findPlug("outputB")
                blendstretch_plug = blendstretch_fs.findPlug("blender")
                rhandstretchoption_plug = rhandstretchoption_fs.findPlug("stretchable")

                objparent = om1.MObject()
                objchild = om1.MObject()
                for index in range(ikrupperarm_sl_lst.length()):
                    if index < ikrupperarm_sl_lst.length()-1:
                        ikrupperarm_sl_lst.getDependNode(index, objparent)
                        ikrupperarm_sl_lst.getDependNode(index+1, objchild)
                        rarmparentjnt_fs = om1.MFnDependencyNode(objparent)
                        rarmchildjnt_fs = om1.MFnDependencyNode(objchild)
                        rarmjnt_syplug = rarmparentjnt_fs.findPlug("scaleY")
                        rarmjnt_sxplug = rarmparentjnt_fs.findPlug("scaleX")
                        rarmjnt_szplug = rarmparentjnt_fs.findPlug("scaleZ")
                        rarmjnt_sotpplug = rarmparentjnt_fs.findPlug("scale")
                        rarmjnt_invsplug = rarmchildjnt_fs.findPlug("inverseScale")
                        ikspinedg_modifier.connect(rarmstretchpercentotp_plug, blendstretchinp1g_plug)
                        ikspinedg_modifier.connect(rarmstretchdivotox_plug, blendstretchinp1r_plug)
                        ikspinedg_modifier.connect(rarmstretchdivotpz_plug, blendstretchinp1b_plug)
                        ikspinedg_modifier.connect(blendstretchotpg_plug, rarmjnt_syplug)
                        ikspinedg_modifier.connect(blendstretchotpr_plug, rarmjnt_sxplug)
                        ikspinedg_modifier.connect(blendstretchotpb_plug, rarmjnt_szplug)
                        ikspinedg_modifier.connect(rarmjnt_sotpplug, rarmjnt_invsplug)

                ikspinedg_modifier.renameNode(rarmcrv_info, "RightUpperArmSpline_Info")
                ikspinedg_modifier.renameNode(rarmstretchpercent, "RightUpperArmStretch_Percent")
                ikspinedg_modifier.renameNode(rarmstretchpow, "RightUpperArmStretch_Power")
                ikspinedg_modifier.renameNode(rarmstretchdiv, "RightUpperArmStretch_Divide")
                ikspinedg_modifier.renameNode(ikspline_cv, "RightUpperArm_SplineCvShape")
                ikspinedg_modifier.renameNode(self.rarm_ik, "RightUpperArm_Ik")
                ikspinedg_modifier.renameNode(self.ikrarm_effector, "RightUpperArm_effector")
                ikspinedg_modifier.renameNode(rarmscalediv, "IkRightUpperArmGlobalScale_Average")
                ikspinedg_modifier.renameNode(rikarmstretchdiv, "RightUpperArmStretch_Divide2")
                ikspinedg_modifier.renameNode(blendstretch, "RightUpperArmStretch_Blend")
                ikspinedg_modifier.commandToExecute('parent "RightUpperArm_Ik" "DoNotTouch"')
                ikspinedg_modifier.commandToExecute('connectAttr -force RightUpperArm_SplineCvShape.worldSpace[0] RightUpperArm_Ik.inCurve')
                ikspinedg_modifier.commandToExecute('skinCluster -bm 3 -sm 1 -dr 2.0 -name "RightUpperArmIk_skin" IkCvSplineRightUpperArm0 IkCvSplineRightUpperArm1 IkCvSplineRightUpperArm2 RightUpperArm_SplineCv')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArm_Ik.dTwistControlEnable" 1')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArm_Ik.dWorldUpType" 4')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArm_Ik.dForwardAxis" 3')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArm_Ik.dWorldUpAxis" 4')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArm_Ik.dWorldUpVectorY" 0')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArm_Ik.dWorldUpVectorEndY" 0')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArm_Ik.dWorldUpVectorZ" -1')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArm_Ik.dWorldUpVectorEndZ" -1')
                ikspinedg_modifier.commandToExecute('connectAttr -force IkCvSplineRightUpperArm0.worldMatrix[0] RightUpperArm_Ik.dWorldUpMatrix')
                ikspinedg_modifier.commandToExecute('connectAttr -force IkCvSplineLeftUpperArm2.worldMatrix[0] RightUpperArm_Ik.dWorldUpMatrixEnd')
                ikspinedg_modifier.commandToExecute('connectAttr -force RightUpperArm_SplineCvShape.worldSpace[0] RightUpperArmSpline_Info.inputCurve')
                ikspinedg_modifier.connect(rarmcrvinfoarc_plug, rarmscaledivinp1y_plug)
                ikspinedg_modifier.connect(masterctrlsy_plug, rarmscaledivinp2y_plug)
                ikspinedg_modifier.connect(rarmscaledivotpy_plug, rarmstretchpercentinp1y_plug)
                ikspinedg_modifier.connect(rarmstretchpercentotp_plug, rarmstretchpowinp1x_plug)
                ikspinedg_modifier.connect(rarmstretchpercentotp_plug, rarmstretchpowinp1z_plug)
                ikspinedg_modifier.connect(rarmstretchpowotpx_plug, rarmstretchdivinp2x_plug)
                ikspinedg_modifier.connect(rarmstretchpowotpz_plug, rarmstretchdivinp2z_plug)
                ikspinedg_modifier.connect(rikarmstretchclust2trans_plug, rikarmstretchdivinp1_plug)
                ikspinedg_modifier.connect(rikarmstretchdivotp_plug, rikarmstretchclust1trans_plug)
                ikspinedg_modifier.connect(rhandstretchoption_plug, blendstretch_plug)
                ikspinedg_modifier.commandToExecute('float $rightupperarmstretchinput1Y = `getAttr "RightUpperArmStretch_Percent.input1Y"`; setAttr "RightUpperArmStretch_Percent.input2Y" $rightupperarmstretchinput1Y')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArmStretch_Power.input2X" 0.5')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArmStretch_Power.input2Z" 0.5')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArmStretch_Divide.input1X" 1')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArmStretch_Divide.input1Z" 1')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArmStretch_Percent.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArmStretch_Power.operation" 3')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArmStretch_Divide.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "IkRightUpperArmGlobalScale_Average.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArmStretch_Divide2.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArmStretch_Divide2.input2X" 2')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArmStretch_Divide2.input2Y" 2')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArmStretch_Divide2.input2Z" 2')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArmStretch_Blend.color2R" 1')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArmStretch_Blend.color2G" 1')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperArmStretch_Blend.color2B" 1')
                ikspinedg_modifier.doIt()

                ikspline_solver = self.IK_System.findSolver("ikSplineSolver")
                self.IK_Handle.setSolver(ikspline_solver)

            grp_armlowerikcluster1 = om1.MObject()
            grp_armlowerikcluster2 = om1.MObject()

            if cmds.objExists("IkSplineRightLowerArm0"):
                ikrlowerarm_sl_lst = om1.MSelectionList()
                ikrlowerarm_sl_lst.add("IkSplineRightLowerArm*")
                ikrlowerarm_sl_lst.getDependNode(0, obj_root)
                ikrlowerarm_sl_lst.getDependNode(ikrlowerarm_sl_lst.length()-1, obj_endspine)

                ikrlowerarmgrp_sl_lst = om1.MSelectionList()
                ikrlowerarmgrp_sl_lst.add("RightLowerArmIkCluster1_grp")
                ikrlowerarmgrp_sl_lst.add("RightLowerArmIkCluster2_grp")
                ikrlowerarmgrp_sl_lst.getDependNode(0, grp_armlowerikcluster1)
                ikrlowerarmgrp_sl_lst.getDependNode(1, grp_armlowerikcluster2)

                rootspine_path = self.MDag_path.getAPathTo(obj_root)

                try:
                    ikspineiksolver_lst.add("ikSplineSolver*")
                except:
                    cmds.createNode("ikSplineSolver")

                self.ikrarm_effector = self.IK_Effector.create(obj_endspine)
                ikrarm_effector_path = self.MDag_path.getAPathTo(self.ikrarm_effector)

                self.rarm_ik = self.IK_Handle.create(rootspine_path, ikrarm_effector_path)

                obj_array = om1.MPointArray()
                obj_lst_mpoint = []
                obj = om1.MObject()
                for index in range(ikrlowerarm_sl_lst.length()):
                    ikrlowerarm_sl_lst.getDependNode(index, obj)
                    obj_path = self.MDag_path.getAPathTo(obj)
                    obj_tn = om1.MFnTransform(obj_path)
                    obj_t = obj_tn.translation(om1.MSpace.kWorld)
                    obj_lst_mpoint.append(om1.MPoint(obj_t))
                    obj_array.append(obj_lst_mpoint[index])

                self.ikspline_cv_tn = ikspinedag_n.create("transform", "RightLowerArm_SplineCv")
                ikspline_cv = self.MNurbs1_cv.createWithEditPoints(obj_array, 1, 1, False, True, True, self.ikspline_cv_tn)
                cmds.parent("RightLowerArm_SplineCv", "DoNotTouch")

                rarmcrv_info = ikspinedg_modifier.createNode("curveInfo")
                rarmstretchpercent = ikspinedg_modifier.createNode("multiplyDivide")
                rarmstretchpow = ikspinedg_modifier.createNode("multiplyDivide")
                rarmstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                rarmscalediv = ikspinedg_modifier.createNode("multiplyDivide")
                rikarmstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                blendstretch = ikspinedg_modifier.createNode("blendColors")

                rarmcrvinfo_fs = om1.MFnDependencyNode(rarmcrv_info)
                rarmstretchpercent_fs = om1.MFnDependencyNode(rarmstretchpercent)
                rarmstretchpow_fs = om1.MFnDependencyNode(rarmstretchpow)
                rarmstretchdiv_fs = om1.MFnDependencyNode(rarmstretchdiv)
                rarmscalediv_fs = om1.MFnDependencyNode(rarmscalediv)
                rikarmstretchdiv_fs = om1.MFnDependencyNode(rikarmstretchdiv)
                rikarmstretchcluster1_fs = om1.MFnDependencyNode(grp_armlowerikcluster1)
                rikarmstretchcluster2_fs = om1.MFnDependencyNode(grp_armlowerikcluster2)
                blendstretch_fs = om1.MFnDependencyNode(blendstretch)

                rarmcrvinfoarc_plug = rarmcrvinfo_fs.findPlug("arcLength")
                rarmstretchpercentinp1y_plug = rarmstretchpercent_fs.findPlug("input1Y")
                rarmstretchpercentotp_plug = rarmstretchpercent_fs.findPlug("outputY")
                rarmstretchpowinp1x_plug = rarmstretchpow_fs.findPlug("input1X")
                rarmstretchpowinp1z_plug = rarmstretchpow_fs.findPlug("input1Z")
                rarmstretchpowotpx_plug = rarmstretchpow_fs.findPlug("outputX")
                rarmstretchpowotpz_plug = rarmstretchpow_fs.findPlug("outputZ")
                rarmstretchdivinp2x_plug = rarmstretchdiv_fs.findPlug("input2X")
                rarmstretchdivinp2z_plug = rarmstretchdiv_fs.findPlug("input2Z")
                rarmstretchdivotox_plug = rarmstretchdiv_fs.findPlug("outputX")
                rarmstretchdivotpz_plug = rarmstretchdiv_fs.findPlug("outputZ")
                rarmscaledivinp1y_plug = rarmscalediv_fs.findPlug("input1Y")
                rarmscaledivinp2y_plug = rarmscalediv_fs.findPlug("input2Y")
                rarmscaledivotpy_plug = rarmscalediv_fs.findPlug("outputY")
                rikarmstretchdivinp1_plug = rikarmstretchdiv_fs.findPlug("input1")
                rikarmstretchdivotp_plug = rikarmstretchdiv_fs.findPlug("output")
                rikarmstretchclust1trans_plug = rikarmstretchcluster1_fs.findPlug("translate")
                rikarmstretchclust2trans_plug = rikarmstretchcluster2_fs.findPlug("translate")
                blendstretchinp1r_plug = blendstretch_fs.findPlug("color1R")
                blendstretchinp1g_plug = blendstretch_fs.findPlug("color1G")
                blendstretchinp1b_plug = blendstretch_fs.findPlug("color1B")
                blendstretchotpr_plug = blendstretch_fs.findPlug("outputR")
                blendstretchotpg_plug = blendstretch_fs.findPlug("outputG")
                blendstretchotpb_plug = blendstretch_fs.findPlug("outputB")
                blendstretch_plug = blendstretch_fs.findPlug("blender")

                objparent = om1.MObject()
                objchild = om1.MObject()
                for index in range(ikrlowerarm_sl_lst.length()):
                    if index < ikrlowerarm_sl_lst.length()-1:
                        ikrlowerarm_sl_lst.getDependNode(index, objparent)
                        ikrlowerarm_sl_lst.getDependNode(index+1, objchild)
                        rarmparentjnt_fs = om1.MFnDependencyNode(objparent)
                        rarmchildjnt_fs = om1.MFnDependencyNode(objchild)
                        rarmjnt_syplug = rarmparentjnt_fs.findPlug("scaleY")
                        rarmjnt_sxplug = rarmparentjnt_fs.findPlug("scaleX")
                        rarmjnt_szplug = rarmparentjnt_fs.findPlug("scaleZ")
                        rarmjnt_sotpplug = rarmparentjnt_fs.findPlug("scale")
                        rarmjnt_invsplug = rarmchildjnt_fs.findPlug("inverseScale")
                        ikspinedg_modifier.connect(rarmstretchpercentotp_plug, blendstretchinp1g_plug)
                        ikspinedg_modifier.connect(rarmstretchdivotox_plug, blendstretchinp1r_plug)
                        ikspinedg_modifier.connect(rarmstretchdivotpz_plug, blendstretchinp1b_plug)
                        ikspinedg_modifier.connect(blendstretchotpg_plug, rarmjnt_syplug)
                        ikspinedg_modifier.connect(blendstretchotpr_plug, rarmjnt_sxplug)
                        ikspinedg_modifier.connect(blendstretchotpb_plug, rarmjnt_szplug)
                        ikspinedg_modifier.connect(rarmjnt_sotpplug, rarmjnt_invsplug)

                ikspinedg_modifier.renameNode(rarmcrv_info, "RightLowerArmSpline_Info")
                ikspinedg_modifier.renameNode(rarmstretchpercent, "RightLowerArmStretch_Percent")
                ikspinedg_modifier.renameNode(rarmstretchpow, "RightLowerArmStretch_Power")
                ikspinedg_modifier.renameNode(rarmstretchdiv, "RightLowerArmStretch_Divide")
                ikspinedg_modifier.renameNode(ikspline_cv, "RightLowerArm_SplineCvShape")
                ikspinedg_modifier.renameNode(self.rarm_ik, "RightLowerArm_Ik")
                ikspinedg_modifier.renameNode(self.ikrarm_effector, "RightLowerArm_effector")
                ikspinedg_modifier.renameNode(rarmscalediv, "IkRightLowerArmGlobalScale_Average")
                ikspinedg_modifier.renameNode(rikarmstretchdiv, "RightLowerArmStretch_Divide2")
                ikspinedg_modifier.renameNode(blendstretch, "RightLowerArmStretch_Blend")
                ikspinedg_modifier.commandToExecute('parent "RightLowerArm_Ik" "DoNotTouch"')
                ikspinedg_modifier.commandToExecute('connectAttr -f RightLowerArm_SplineCvShape.worldSpace[0] RightLowerArm_Ik.inCurve')
                ikspinedg_modifier.commandToExecute('skinCluster -bm 3 -sm 1 -dr 2.0 -name "RightLowerArmIk_skin" IkCvSplineRightLowerArm0 IkCvSplineRightLowerArm1 IkCvSplineRightLowerArm2 RightLowerArm_SplineCv')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArm_Ik.dTwistControlEnable" 1')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArm_Ik.dWorldUpType" 4')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArm_Ik.dForwardAxis" 3')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArm_Ik.dWorldUpAxis" 4')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArm_Ik.dWorldUpVectorY" 0')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArm_Ik.dWorldUpVectorEndY" 0')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArm_Ik.dWorldUpVectorZ" -1')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArm_Ik.dWorldUpVectorEndZ" -1')
                ikspinedg_modifier.commandToExecute('connectAttr -f IkCvSplineRightLowerArm0.worldMatrix[0] RightLowerArm_Ik.dWorldUpMatrix')
                ikspinedg_modifier.commandToExecute('connectAttr -f IkCvSplineRightLowerArm2.worldMatrix[0] RightLowerArm_Ik.dWorldUpMatrixEnd')
                ikspinedg_modifier.commandToExecute('connectAttr -f RightLowerArm_SplineCvShape.worldSpace[0] RightLowerArmSpline_Info.inputCurve')
                ikspinedg_modifier.connect(rarmcrvinfoarc_plug, rarmscaledivinp1y_plug)
                ikspinedg_modifier.connect(masterctrlsy_plug, rarmscaledivinp2y_plug)
                ikspinedg_modifier.connect(rarmscaledivotpy_plug, rarmstretchpercentinp1y_plug)
                ikspinedg_modifier.connect(rarmstretchpercentotp_plug, rarmstretchpowinp1x_plug)
                ikspinedg_modifier.connect(rarmstretchpercentotp_plug, rarmstretchpowinp1z_plug)
                ikspinedg_modifier.connect(rarmstretchpowotpx_plug, rarmstretchdivinp2x_plug)
                ikspinedg_modifier.connect(rarmstretchpowotpz_plug, rarmstretchdivinp2z_plug)
                ikspinedg_modifier.connect(rikarmstretchclust2trans_plug, rikarmstretchdivinp1_plug)
                ikspinedg_modifier.connect(rikarmstretchdivotp_plug, rikarmstretchclust1trans_plug)
                ikspinedg_modifier.connect(rhandstretchoption_plug, blendstretch_plug)
                ikspinedg_modifier.commandToExecute('float $rightlowerarmstretchinput1Y = `getAttr "RightLowerArmStretch_Percent.input1Y"`; setAttr "RightLowerArmStretch_Percent.input2Y" $rightlowerarmstretchinput1Y')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArmStretch_Power.input2X" 0.5')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArmStretch_Power.input2Z" 0.5')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArmStretch_Divide.input1X" 1')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArmStretch_Divide.input1Z" 1')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArmStretch_Percent.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArmStretch_Power.operation" 3')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArmStretch_Divide.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "IkRightLowerArmGlobalScale_Average.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArmStretch_Divide2.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArmStretch_Divide2.input2X" 2')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArmStretch_Divide2.input2Y" 2')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArmStretch_Divide2.input2Z" 2')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArmStretch_Blend.color2R" 1')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArmStretch_Blend.color2G" 1')
                ikspinedg_modifier.commandToExecute('setAttr "RightLowerArmStretch_Blend.color2B" 1')
                ikspinedg_modifier.doIt()

                ikspline_solver = self.IK_System.findSolver("ikSplineSolver")
                self.IK_Handle.setSolver(ikspline_solver)

        stretchy_sl_lst2.add("Biped_RightHandOptions_ctrl")
        obj_stretchyrightarm2 = stretchy_sl_lst2.getDependNode(2)

        if cmds.objExists("NoFlipRightHand_Ik") and cmds.objExists("PVRightHand_Ik"):

            self.MDG2_mod.commandToExecute('addAttr -longName "follow" -niceName "Follow Body" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_IkRightHand_ctrl')
            self.MDG2_mod.commandToExecute('parentConstraint -mo -weight 1 Biped_Root_ctrl Biped_IkRightHandRot_null')
            self.MDG2_mod.doIt()

            rhandik_sl_ls = om2.MSelectionList()
            rhandik_sl_ls.add("RightArmIk_grp")
            rhandik_sl_ls.add("Biped_NoFlipRightElbow_null")
            rhandik_sl_ls.add("Biped_IkRightHand_ctrl")
            rhandik_sl_ls.add("IkStretchyRightJointArm_grp")
            rikhandgrp_fs = om2.MFnDependencyNode(rhandik_sl_ls.getDependNode(0))
            nofliprightelbownullobj_fs = om2.MFnDependencyNode(rhandik_sl_ls.getDependNode(1))
            ikarmctrl_fs = om2.MFnDependencyNode(rhandik_sl_ls.getDependNode(2))
            rikhand_fs = om2.MFnDependencyNode(ikrarm_sl_ls.getDependNode(2))

            if self.typeofRHandIK.currentIndex() == 1 or 2:
                rikhandctrl_multMatrix = self.MDG2_mod.createNode("multMatrix")
                rikhandctrl_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                rikhandrot_multMatrix = self.MDG2_mod.createNode("multMatrix")
                rikhandrot_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                self.MDG2_mod.renameNode(rikhandctrl_multMatrix, "IkRightHand_multMatrix")
                self.MDG2_mod.renameNode(rikhandctrl_decomposeMatrix, "IkRightHand_decomposeMatrix")
                self.MDG2_mod.renameNode(rikhandrot_multMatrix, "IkRightHandRot_multMatrix")
                self.MDG2_mod.renameNode(rikhandrot_decomposeMatrix, "IkRightHandRot_decomposeMatrix")

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
                rikhandgrpTrans_plug = rikhandgrp_fs.findPlug("translate", False)
                rikhandgrpRot_plug = rikhandgrp_fs.findPlug("rotate", False)
                ikarmctrlTrans_plug = ikarmctrl_fs.findPlug("translate", False)
                ikarmctrlRot_plug = ikarmctrl_fs.findPlug("rotate", False)
                nofliprightelbownullTrans_plug = nofliprightelbownullobj_fs.findPlug("translate", False)
                nofliprightelbownullRot_plug = nofliprightelbownullobj_fs.findPlug("rotate", False)
                rikhandRot_plug = rikhand_fs.findPlug("rotate", False)

                self.MDG2_mod.commandToExecute('connectAttr -force Biped_IkRightHand_ctrl.worldMatrix[0] IkRightHand_multMatrix.matrixIn[0]')
                self.MDG2_mod.commandToExecute('connectAttr -force Biped_IkRightHand_ctrl.worldMatrix[0] IkRightHandRot_multMatrix.matrixIn[0]')
                self.MDG2_mod.commandToExecute('connectAttr -force IkRightHand.parentInverseMatrix[0] IkRightHandRot_multMatrix.matrixIn[1]')
                self.MDG2_mod.commandToExecute('connectAttr -force Biped_IkRightHand_ctrl.follow Biped_IkRightHandRot_null_parentConstraint1.Biped_Root_ctrlW0')
                self.MDG2_mod.connect(rikhandmultMatrixSum_plug, rikhanddecomposeInpMatrix_plug)
                self.MDG2_mod.connect(rikhanddecomposeOtpTrans_plug, rikhandgrpTrans_plug)
                self.MDG2_mod.connect(rikhandrotmultMatrixSum_plug, rikhandrotdecomposeInpMatrix_plug)
                self.MDG2_mod.connect(rikhanddecomposeOtpRot_plug, rikhandgrpRot_plug)
                self.MDG2_mod.connect(ikarmctrlTrans_plug, nofliprightelbownullTrans_plug)
                self.MDG2_mod.connect(ikarmctrlRot_plug, nofliprightelbownullRot_plug)
                self.MDG2_mod.connect(rikhandrotdecomposeOtpRot_plug, rikhandRot_plug)
                self.MDG2_mod.commandToExecute('parent NoFlipRightHand_Ik RightArmIk_grp')
                self.MDG2_mod.commandToExecute('parent PVRightHand_Ik RightArmIk_grp')
                self.MDG2_mod.commandToExecute('poleVectorConstraint Biped_NoFlipRightElbow_ctrl NoFlipRightHand_Ik')
                self.MDG2_mod.commandToExecute('poleVectorConstraint Biped_PVRightElbow_ctrl PVRightHand_Ik')
                self.MDG2_mod.commandToExecute('setAttr "NoFlipRightHand_Ik.twist" 90')

                if self.autostretch.currentIndex() == 1:
                    rikarmdistloc = om2.MFnDagNode()

                    rikarmdistloc1_tn = rikarmdistloc.create("transform", "distloc_R_arm1", rhandik_sl_ls.getDependNode(3))
                    rikarmdistloc1_ln = rikarmdistloc.create("locator", "R_arm1_Shape", rikarmdistloc1_tn)
                    rikhanddistloc1_tn = rikarmdistloc.create("transform", "distloc_R_hand1")
                    rikhanddistloc1_ln = rikarmdistloc.create("locator", "R_hand1_Shape", rikhanddistloc1_tn)
                    self.MDG2_mod.commandToExecute('createNode "distanceDimShape"')
                    self.MDG2_mod.commandToExecute('rename "distanceDimension1" "IkRightArmDistance_Info"')
                    self.MDG2_mod.doIt()

                    rarmnull_transform_t = larmnull_transform.translation(om2.MSpace.kTransform)
                    rikupperarmdistloc_transform = om2.MFnTransform(rikarmdistloc1_tn)
                    rikupperarmdistloc_transform.setTranslation(rarmnull_transform_t, om2.MSpace.kTransform)

                    IkRightArmDistance_sl_ls = om2.MSelectionList()
                    IkRightArmDistance_sl_ls.add("IkRightArmDistance_InfoShape")

                    rikhandDist_fs = om2.MFnDependencyNode(rikhanddistloc1_tn)
                    rikarmjntDist_fs = om2.MFnDependencyNode(IkRightArmDistance_sl_ls.getDependNode(0))

                    rikarmjntDistPoint2_plug = rikarmjntDist_fs.findPlug("endPoint", False)
                    rikhandDistOtpTrans_plug = rikhandDist_fs.findPlug("translate", False)

                    self.MDG2_mod.commandToExecute('connectAttr -force R_arm1_Shape.worldPosition[0] IkRightArmDistance_InfoShape.startPoint')
                    self.MDG2_mod.connect(rikhandDistOtpTrans_plug, rikarmjntDistPoint2_plug)
                    self.MDG2_mod.connect(rikhanddecomposeOtpTrans_plug, rikhandDistOtpTrans_plug)
                    self.MDG2_mod.commandToExecute('float $noflipikrightforearmtranslateY = `getAttr "IkNoFlipRightForeArm.translateY"`; float $noflipikrighthandtranslateY = `getAttr "IkNoFlipRightHand.translateY"`; float $totalnoflipikrightarmtranslateY = $noflipikrightforearmtranslateY + $noflipikrighthandtranslateY; setDrivenKeyframe -currentDriver IkRightArmDistance_InfoShape.distance -driverValue $totalnoflipikrightarmtranslateY -attribute "translateY" -value $noflipikrightforearmtranslateY IkNoFlipRightForeArm;')
                    self.MDG2_mod.commandToExecute('float $noflipikrightforearmtranslateY = `getAttr "IkNoFlipRightForeArm.translateY"`; float $noflipikrighthandtranslateY = `getAttr "IkNoFlipRightHand.translateY"`; float $totalnoflipikrightarmtranslateY = $noflipikrightforearmtranslateY + $noflipikrighthandtranslateY; setDrivenKeyframe -currentDriver IkRightArmDistance_InfoShape.distance -driverValue ($totalnoflipikrightarmtranslateY*2) -attribute "translateY" -value ($noflipikrightforearmtranslateY*2) IkNoFlipRightForeArm;')
                    self.MDG2_mod.commandToExecute('float $noflipikrightforearmtranslateY = `getAttr "IkNoFlipRightForeArm.translateY"`; float $noflipikrighthandtranslateY = `getAttr "IkNoFlipRightHand.translateY"`; float $totalnoflipikrightarmtranslateY = $noflipikrightforearmtranslateY + $noflipikrighthandtranslateY; setDrivenKeyframe -currentDriver IkRightArmDistance_InfoShape.distance -driverValue $totalnoflipikrightarmtranslateY -attribute "translateY" -value $noflipikrighthandtranslateY IkNoFlipRightHand;')
                    self.MDG2_mod.commandToExecute('float $noflipikrightforearmtranslateY = `getAttr "IkNoFlipRightForeArm.translateY"`; float $noflipikrighthandtranslateY = `getAttr "IkNoFlipRightHand.translateY"`; float $totalnoflipikrightarmtranslateY = $noflipikrightforearmtranslateY + $noflipikrighthandtranslateY; setDrivenKeyframe -currentDriver IkRightArmDistance_InfoShape.distance -driverValue ($totalnoflipikrightarmtranslateY*2) -attribute "translateY" -value ($noflipikrighthandtranslateY*2) IkNoFlipRightHand;')
                    self.MDG2_mod.commandToExecute('float $pvikrightforearmtranslateY = `getAttr "IkPVRightForeArm.translateY"`; float $pvikrighthandtranslateY = `getAttr "IkPVRightHand.translateY"`; float $totalpvikrightarmtranslateY = $pvikrightforearmtranslateY + $pvikrighthandtranslateY; setDrivenKeyframe -currentDriver IkRightArmDistance_InfoShape.distance -driverValue $totalpvikrightarmtranslateY -attribute "translateY" -value $pvikrightforearmtranslateY IkPVRightForeArm;')
                    self.MDG2_mod.commandToExecute('float $pvikrightforearmtranslateY = `getAttr "IkPVRightForeArm.translateY"`; float $pvikrighthandtranslateY = `getAttr "IkPVRightHand.translateY"`; float $totalpvikrightarmtranslateY = $pvikrightforearmtranslateY + $pvikrighthandtranslateY; setDrivenKeyframe -currentDriver IkRightArmDistance_InfoShape.distance -driverValue ($totalpvikrightarmtranslateY*2) -attribute "translateY" -value ($pvikrightforearmtranslateY*2) IkPVRightForeArm;')
                    self.MDG2_mod.commandToExecute('float $pvikrightforearmtranslateY = `getAttr "IkPVRightForeArm.translateY"`; float $pvikrighthandtranslateY = `getAttr "IkPVRightHand.translateY"`; float $totalpvikrightarmtranslateY = $pvikrightforearmtranslateY + $pvikrighthandtranslateY; setDrivenKeyframe -currentDriver IkRightArmDistance_InfoShape.distance -driverValue $totalpvikrightarmtranslateY -attribute "translateY" -value $pvikrighthandtranslateY IkPVRightHand;')
                    self.MDG2_mod.commandToExecute('float $pvikrightforearmtranslateY = `getAttr "IkPVRightForeArm.translateY"`; float $pvikrighthandtranslateY = `getAttr "IkPVRightHand.translateY"`; float $totalpvikrightarmtranslateY = $pvikrightforearmtranslateY + $pvikrighthandtranslateY; setDrivenKeyframe -currentDriver IkRightArmDistance_InfoShape.distance -driverValue ($totalpvikrightarmtranslateY*2) -attribute "translateY" -value ($pvikrighthandtranslateY*2) IkPVRightHand;')
                    self.MDG2_mod.commandToExecute('selectKey -attribute translateY IkNoFlipRightForeArm; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative')
                    self.MDG2_mod.commandToExecute('selectKey -attribute translateY IkPVRightForeArm; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative')
                    self.MDG2_mod.commandToExecute('selectKey -attribute translateY IkNoFlipRightHand; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative')
                    self.MDG2_mod.commandToExecute('selectKey -attribute translateY IkPVRightHand; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative')
                    self.MDG2_mod.commandToExecute('parent "IkRightArmDistance_Info" "DoNotTouch"')
                    self.MDG2_mod.commandToExecute('parent "distloc_R_hand1" "DoNotTouch"')

                    self.MDG2_mod.commandToExecute('addAttr -longName "elbowsnap" -niceName "Elbow Snap" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_PVRightElbow_ctrl')

                    rikarmdistloc2_tn = rikarmdistloc.create("transform", "distloc_R_arm2", rhandik_sl_ls.getDependNode(3))
                    rikarmdistloc2_ln = rikarmdistloc.create("locator", "R_arm2_Shape", rikarmdistloc2_tn)
                    rikelbowdistloc_tn = rikarmdistloc.create("transform", "distloc_R_elbow")
                    rikelbowdistloc_ln = rikarmdistloc.create("locator", "R_elbow_Shape", rikelbowdistloc_tn)
                    rikhanddistloc2_tn = rikarmdistloc.create("transform", "distloc_R_hand2")
                    rikhanddistloc2_ln = rikarmdistloc.create("locator", "R_hand2_Shape", rikhanddistloc2_tn)
                    pvrightelbowctrl_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                    rikpvupperarmtransblendnode = self.MDG2_mod.createNode("blendColors")
                    rikpvlowerlegtransblendnode = self.MDG2_mod.createNode("blendColors")
                    rikpvupperarmstretchblendnode = self.MDG2_mod.createNode("blendColors")
                    rikpvlowerarmstretchblendnode = self.MDG2_mod.createNode("blendColors")
                    self.MDG2_mod.commandToExecute('createNode "distanceDimShape"')
                    self.MDG2_mod.commandToExecute('createNode "distanceDimShape"')
                    self.MDG2_mod.renameNode(pvrightelbowctrl_decomposeMatrix, "PVRightElbow_decomposeMatrix")
                    self.MDG2_mod.renameNode(rikpvupperarmtransblendnode, "PVRightUpperArmTrans_blend")
                    self.MDG2_mod.renameNode(rikpvlowerlegtransblendnode, "PVRightLowerArmTrans_blend")
                    self.MDG2_mod.renameNode(rikpvupperarmstretchblendnode, "PVRightUpperArmStretch_blend")
                    self.MDG2_mod.renameNode(rikpvlowerarmstretchblendnode, "PVRightLowerArmStretch_blend")
                    self.MDG2_mod.commandToExecute('rename "distanceDimension1" "RightUpperArmDistance_Info"')
                    self.MDG2_mod.commandToExecute('rename "distanceDimension2" "RightLowerArmDistance_Info"')
                    self.MDG2_mod.doIt()

                    rikupperarmdistloc2_transform = om2.MFnTransform(rikarmdistloc2_tn)
                    rikupperarmdistloc2_transform.setTranslation(rarmnull_transform_t, om2.MSpace.kTransform)

                    IkRightArmDistance_sl_ls.add("RightUpperArmDistance_InfoShape")
                    IkRightArmDistance_sl_ls.add("RightLowerArmDistance_InfoShape")
                    IkRightArmDistance_sl_ls.add("IkPVRightForeArm_translateY")
                    IkRightArmDistance_sl_ls.add("IkPVRightHand_translateY")
                    IkRightArmDistance_sl_ls.add("Biped_PVRightElbow_ctrl")
                    IkRightArmDistance_sl_ls.add("IkNoFlipRightForeArm_translateY")
                    IkRightArmDistance_sl_ls.add("IkNoFlipRightHand_translateY")

                    rikelbowDist_fs = om2.MFnDependencyNode(rikelbowdistloc_tn)
                    rikhandDist_fs = om2.MFnDependencyNode(rikhanddistloc2_tn)
                    rikupperarmjntDist_fs = om2.MFnDependencyNode(IkRightArmDistance_sl_ls.getDependNode(1))
                    riklowerarmjntDist_fs = om2.MFnDependencyNode(IkRightArmDistance_sl_ls.getDependNode(2))
                    pvrightelbowkey_fs = om2.MFnDependencyNode(IkRightArmDistance_sl_ls.getDependNode(3))
                    pvrighthandkey_fs = om2.MFnDependencyNode(IkRightArmDistance_sl_ls.getDependNode(4))
                    pvrightelbowctrlDecomposeMatrix_fs = om2.MFnDependencyNode(pvrightelbowctrl_decomposeMatrix)
                    rikpvupperarmtransblendnode_fs = om2.MFnDependencyNode(rikpvupperarmtransblendnode)
                    rikpvlowerarmtransblendnode_fs = om2.MFnDependencyNode(rikpvlowerlegtransblendnode)
                    pvrightelbowctrl_fs = om2.MFnDependencyNode(IkRightArmDistance_sl_ls.getDependNode(5))
                    pvrightelbowjnt_fs = om2.MFnDependencyNode(pvikrarm_sl_ls.getDependNode(1))
                    pvrighthandjnt_fs = om2.MFnDependencyNode(pvikrarm_sl_ls.getDependNode(2))
                    rikupperarmstretchblendnode_fs = om2.MFnDependencyNode(rikpvupperarmstretchblendnode)
                    riklowerarmstretchblendnode_fs = om2.MFnDependencyNode(rikpvlowerarmstretchblendnode)
                    righthandoption_fs = om2.MFnDependencyNode(obj_stretchyrightarm2)

                    rikupperarmjntDistPoint2_plug = rikupperarmjntDist_fs.findPlug("endPoint", False)
                    riklowerarmjntDistPoint1_plug = riklowerarmjntDist_fs.findPlug("startPoint", False)
                    riklowerarmjntDistPoint2_plug = riklowerarmjntDist_fs.findPlug("endPoint", False)
                    rikelbowDistOtpTrans_plug = rikelbowDist_fs.findPlug("translate", False)
                    rikhandDistOtpTrans_plug = rikhandDist_fs.findPlug("translate", False)
                    pvrightelbowctrlDecomposeMatrixOtpTrans_plug = pvrightelbowctrlDecomposeMatrix_fs.findPlug("outputTranslate", False)
                    pvrightelbowkeyotp_plug = pvrightelbowkey_fs.findPlug("output", False)
                    pvrighthandkeyotp_plug = pvrighthandkey_fs.findPlug("output", False)
                    rikpvupperarmtransblendnodeinp1g_plug = rikpvupperarmtransblendnode_fs.findPlug("color1G", False)
                    rikpvupperarmtransblendnodeinp2g_plug = rikpvupperarmtransblendnode_fs.findPlug("color2G", False)
                    rikpvupperarmtransblendnodeotp_plug = rikpvupperarmtransblendnode_fs.findPlug("outputG", False)
                    rikpvupperarmtransblendnodeblender_plug = rikpvupperarmtransblendnode_fs.findPlug("blender", False)
                    rikpvlowerarmtransblendnodeinp1g_plug = rikpvlowerarmtransblendnode_fs.findPlug("color1G", False)
                    rikpvlowerarmtransblendnodeinp2g_plug = rikpvlowerarmtransblendnode_fs.findPlug("color2G", False)
                    rikpvlowerarmtransblendnodeotp_plug = rikpvlowerarmtransblendnode_fs.findPlug("outputG", False)
                    rikpvlowerarmtransblendnodeblender_plug = rikpvlowerarmtransblendnode_fs.findPlug("blender", False)
                    pvrightelbowctrl_fs_plug = pvrightelbowctrl_fs.findPlug("elbowsnap", False)
                    rikpvupperarmstretchblendnodeinp1g_plug = rikupperarmstretchblendnode_fs.findPlug("color1G", False)
                    rikpvupperarmstretchblendnodeotp_plug = rikupperarmstretchblendnode_fs.findPlug("outputG", False)
                    rikpvupperarmstretchblendnodeblender_plug = rikupperarmstretchblendnode_fs.findPlug("blender", False)
                    rikpvlowerarmstretchblendnodeinp1g_plug = riklowerarmstretchblendnode_fs.findPlug("color1G", False)
                    rikpvlowerarmstretchblendnodeotp_plug = riklowerarmstretchblendnode_fs.findPlug("outputG", False)
                    rikpvlowerarmstretchblendnodeblender_plug = riklowerarmstretchblendnode_fs.findPlug("blender", False)
                    ikrighthandstretch_plug = righthandoption_fs.findPlug("stretchable", False)
                    pvrightelbowjntTrans_plug = pvrightelbowjnt_fs.findPlug("translateY", False)
                    pvrighthandjntTrans_plug = pvrighthandjnt_fs.findPlug("translateY", False)

                    self.MDG2_mod.commandToExecute('connectAttr -force R_arm2_Shape.worldPosition[0] RightUpperArmDistance_InfoShape.startPoint')
                    self.MDG2_mod.commandToExecute('connectAttr -force Biped_PVRightElbow_ctrl.worldMatrix[0] PVRightElbow_decomposeMatrix.inputMatrix')
                    self.MDG2_mod.connect(rikelbowDistOtpTrans_plug, rikupperarmjntDistPoint2_plug)
                    self.MDG2_mod.connect(rikelbowDistOtpTrans_plug, riklowerarmjntDistPoint1_plug)
                    self.MDG2_mod.connect(rikhandDistOtpTrans_plug, riklowerarmjntDistPoint2_plug)
                    self.MDG2_mod.connect(rikhanddecomposeOtpTrans_plug, rikhandDistOtpTrans_plug)
                    self.MDG2_mod.connect(pvrightelbowctrlDecomposeMatrixOtpTrans_plug, rikelbowDistOtpTrans_plug)

                    self.MDG2_mod.disconnect(pvrightelbowkeyotp_plug, pvrightelbowjntTrans_plug)
                    self.MDG2_mod.disconnect(pvrighthandkeyotp_plug, pvrighthandjntTrans_plug)
                    self.MDG2_mod.connect(pvrightelbowkeyotp_plug, rikpvupperarmtransblendnodeinp2g_plug)
                    self.MDG2_mod.connect(pvrighthandkeyotp_plug, rikpvlowerarmtransblendnodeinp2g_plug)
                    self.MDG2_mod.connect(pvrightelbowctrl_fs_plug, rikpvupperarmtransblendnodeblender_plug)
                    self.MDG2_mod.connect(pvrightelbowctrl_fs_plug, rikpvlowerarmtransblendnodeblender_plug)
                    self.MDG2_mod.connect(rikpvupperarmtransblendnodeotp_plug, rikpvupperarmstretchblendnodeinp1g_plug)
                    self.MDG2_mod.connect(rikpvlowerarmtransblendnodeotp_plug, rikpvlowerarmstretchblendnodeinp1g_plug)
                    self.MDG2_mod.connect(rikpvupperarmstretchblendnodeotp_plug, pvrightelbowjntTrans_plug)
                    self.MDG2_mod.connect(rikpvlowerarmstretchblendnodeotp_plug, pvrighthandjntTrans_plug)
                    self.MDG2_mod.connect(ikrighthandstretch_plug, rikpvupperarmstretchblendnodeblender_plug)
                    self.MDG2_mod.connect(ikrighthandstretch_plug, rikpvlowerarmstretchblendnodeblender_plug)
                    self.MDG2_mod.commandToExecute('float $pvikrightforearmtranslateY = `getAttr "PVRightUpperArmStretch_blend.color1G"`; setAttr "PVRightUpperArmStretch_blend.color2G" $pvikrightforearmtranslateY;')
                    self.MDG2_mod.commandToExecute('float $pvikrighthandtranslateY = `getAttr "PVRightLowerArmStretch_blend.color1G"`; setAttr "PVRightLowerArmStretch_blend.color2G" $pvikrighthandtranslateY;')
                    self.MDG2_mod.commandToExecute('parent "distloc_R_elbow" "DoNotTouch"')
                    self.MDG2_mod.commandToExecute('parent "distloc_R_hand2" "DoNotTouch"')
                    self.MDG2_mod.commandToExecute('parent "RightUpperArmDistance_Info" "DoNotTouch"')
                    self.MDG2_mod.commandToExecute('parent "RightLowerArmDistance_Info" "DoNotTouch"')

                    self.MDG2_mod.commandToExecute('addAttr -longName "forearmlength" -niceName "AutoElbow ForeArm Length" -attributeType double -minValue 0 -keyable true -defaultValue 1 Biped_IkRightHand_ctrl')
                    self.MDG2_mod.commandToExecute('addAttr -longName "wristlength" -niceName "AutoElbow Wrist Length" -attributeType double -minValue 0 -keyable true -defaultValue 1 Biped_IkRightHand_ctrl')
                    self.MDG2_mod.doIt()

                    rikautokneeupperlegnode = self.MDG2_mod.createNode("multiplyDivide")
                    rikautokneelowerlegnode = self.MDG2_mod.createNode("multiplyDivide")
                    riknoflipupperarmtransblendnode = self.MDG2_mod.createNode("blendColors")
                    riknofliplowerarmtransblendnode = self.MDG2_mod.createNode("blendColors")
                    self.MDG2_mod.renameNode(rikautokneeupperlegnode, "NoFlipRightForeArmTrans_multiply")
                    self.MDG2_mod.renameNode(rikautokneelowerlegnode, "NoFlipRightHandTrans_multiply")
                    self.MDG2_mod.renameNode(riknoflipupperarmtransblendnode, "NoFlipRightUpperArmStretch_blend")
                    self.MDG2_mod.renameNode(riknofliplowerarmtransblendnode, "NoFlipRightLowerArmStretch_blend")

                    rikautoelbowupperleg_fs = om2.MFnDependencyNode(rikautokneeupperlegnode)
                    rikautoelbowlowerleg_fs = om2.MFnDependencyNode(rikautokneelowerlegnode)
                    nofliprightelbowkey_fs = om2.MFnDependencyNode(IkRightArmDistance_sl_ls.getDependNode(6))
                    nofliprighthandkey_fs = om2.MFnDependencyNode(IkRightArmDistance_sl_ls.getDependNode(7))
                    nofliprightelbowjntTrans_fs = om2.MFnDependencyNode(noflipikrarm_sl_ls.getDependNode(1))
                    nofliprighthandjntTrans_fs = om2.MFnDependencyNode(noflipikrarm_sl_ls.getDependNode(2))
                    riknoflipupperarmstretchblendnode_fs = om2.MFnDependencyNode(riknoflipupperarmtransblendnode)
                    riknofliplowerarmstretchblendnode_fs = om2.MFnDependencyNode(riknofliplowerarmtransblendnode)

                    ikautoelbowupperarmInp1Y_plug = rikautoelbowupperleg_fs.findPlug("input1Y", False)
                    ikautoelbowupperarmInp2Y_plug = rikautoelbowupperleg_fs.findPlug("input2Y", False)
                    rikautoelbowupperarmOtp_plug = rikautoelbowupperleg_fs.findPlug("outputY", False)
                    ikautoelbowlowerarmInp1Y_plug = rikautoelbowlowerleg_fs.findPlug("input1Y", False)
                    ikautoelbowlowerarmInp2Y_plug = rikautoelbowlowerleg_fs.findPlug("input2Y", False)
                    rikautoelbowlowerarmOtp_plug = rikautoelbowlowerleg_fs.findPlug("outputY", False)
                    nofliprightelbowkeyotp_plug = nofliprightelbowkey_fs.findPlug("output", False)
                    nofliprighthandkeyotp_plug = nofliprighthandkey_fs.findPlug("output", False)
                    nofliprightelbowjnttty_plug = nofliprightelbowjntTrans_fs.findPlug("translateY", False)
                    nofliprighthandjntty_plug = nofliprighthandjntTrans_fs.findPlug("translateY", False)
                    rikctrlelbowupperarm_plug = ikarmctrl_fs.findPlug("forearmlength", False)
                    rikctrlelbowlowerarm_plug = ikarmctrl_fs.findPlug("wristlength", False)
                    riknoflipupperarmstretchblendnodeinp1g_plug = riknoflipupperarmstretchblendnode_fs.findPlug("color1G", False)
                    riknoflipupperarmstretchblendnodeotp_plug = riknoflipupperarmstretchblendnode_fs.findPlug("outputG", False)
                    riknoflipupperarmstretchblendnodeblender_plug = riknoflipupperarmstretchblendnode_fs.findPlug("blender", False)
                    riknofliplowerarmstretchblendnodeinp1g_plug = riknofliplowerarmstretchblendnode_fs.findPlug("color1G", False)
                    riknofliplowerarmstretchblendnodeotp_plug = riknofliplowerarmstretchblendnode_fs.findPlug("outputG", False)
                    riknofliplowerarmstretchblendnodeblender_plug = riknofliplowerarmstretchblendnode_fs.findPlug("blender", False)

                    self.MDG2_mod.disconnect(nofliprightelbowkeyotp_plug, nofliprightelbowjnttty_plug)
                    self.MDG2_mod.disconnect(nofliprighthandkeyotp_plug, nofliprighthandjntty_plug)
                    self.MDG2_mod.connect(rikctrlelbowupperarm_plug, ikautoelbowupperarmInp1Y_plug)
                    self.MDG2_mod.connect(nofliprightelbowkeyotp_plug, ikautoelbowupperarmInp2Y_plug)
                    self.MDG2_mod.connect(rikctrlelbowlowerarm_plug, ikautoelbowlowerarmInp1Y_plug)
                    self.MDG2_mod.connect(nofliprighthandkeyotp_plug, ikautoelbowlowerarmInp2Y_plug)
                    self.MDG2_mod.connect(rikautoelbowupperarmOtp_plug, riknoflipupperarmstretchblendnodeinp1g_plug)
                    self.MDG2_mod.connect(rikautoelbowlowerarmOtp_plug, riknofliplowerarmstretchblendnodeinp1g_plug)
                    self.MDG2_mod.connect(riknoflipupperarmstretchblendnodeotp_plug, nofliprightelbowjnttty_plug)
                    self.MDG2_mod.connect(riknofliplowerarmstretchblendnodeotp_plug, nofliprighthandjntty_plug)
                    self.MDG2_mod.connect(ikrighthandstretch_plug, riknoflipupperarmstretchblendnodeblender_plug)
                    self.MDG2_mod.connect(ikrighthandstretch_plug, riknofliplowerarmstretchblendnodeblender_plug)
                    self.MDG2_mod.commandToExecute('float $noflipikrightforearmtranslateY = `getAttr "NoFlipRightUpperArmStretch_blend.color1G"`; setAttr "NoFlipRightUpperArmStretch_blend.color2G" $noflipikrightforearmtranslateY;')
                    self.MDG2_mod.commandToExecute('float $noflipikrighthandtranslateY = `getAttr "NoFlipRightLowerArmStretch_blend.color1G"`; setAttr "NoFlipRightLowerArmStretch_blend.color2G" $noflipikrighthandtranslateY;')
                    self.MDG2_mod.commandToExecute('setAttr "NoFlipRightForeArmTrans_multiply.operation" 1')
                    self.MDG2_mod.commandToExecute('setAttr "NoFlipRightHandTrans_multiply.operation" 1')

                    rightarmglobalscalenode = self.MDG2_mod.createNode("multiplyDivide")
                    nofliprightlegglobalscalenode = self.MDG2_mod.createNode("multiplyDivide")
                    nofliprightfootlobalscalenode = self.MDG2_mod.createNode("multiplyDivide")
                    self.MDG2_mod.renameNode(rightarmglobalscalenode, "IKRightArmGlobalScale_Average")
                    self.MDG2_mod.renameNode(nofliprightlegglobalscalenode, "IKNoFlipRightForeArmGlobalScale_Average")
                    self.MDG2_mod.renameNode(nofliprightfootlobalscalenode, "IKNoFlipRightHandGlobalScale_Average")

                    rightarmglobalscale_fs = om2.MFnDependencyNode(rightarmglobalscalenode)
                    nofliprightarmglobalscale_fs = om2.MFnDependencyNode(nofliprightlegglobalscalenode)
                    nofliprighthandlobalscale_fs = om2.MFnDependencyNode(nofliprightfootlobalscalenode)
                    masterlctrl_fs = om2.MFnDependencyNode(obj_masterctrl2)

                    rikupperarmjntDist_plug = rikupperarmjntDist_fs.findPlug("distance", False)
                    riklowerarmjntDist_plug = riklowerarmjntDist_fs.findPlug("distance", False)
                    rikarmjntDist_plug = rikarmjntDist_fs.findPlug("distance", False)
                    masterlctrlsy_plug = masterlctrl_fs.findPlug("scaleY", False)
                    rightarmglobalscaleInp1Y_plug = rightarmglobalscale_fs.findPlug("input1Y", False)
                    rightarmglobalscaleInp2Y_plug = rightarmglobalscale_fs.findPlug("input2Y", False)
                    rightarmglobalscaleOtpY_plug = rightarmglobalscale_fs.findPlug("outputY", False)
                    nofliprightarmglobalscaleInp1Y_plug = nofliprightarmglobalscale_fs.findPlug("input1Y", False)
                    nofliprightarmglobalscaleInp2Y_plug = nofliprightarmglobalscale_fs.findPlug("input2Y", False)
                    nofliprightarmglobalscaleOtpY_plug = nofliprightarmglobalscale_fs.findPlug("outputY", False)
                    nofliprighthandlobalscaleInp1Y_plug = nofliprighthandlobalscale_fs.findPlug("input1Y", False)
                    nofliprighthandlobalscaleInp2Y_plug = nofliprighthandlobalscale_fs.findPlug("input2Y", False)
                    nofliprighthandlobalscaleOtpY_plug = nofliprighthandlobalscale_fs.findPlug("outputY", False)
                    nofliprightelbowkeyinp_plug = nofliprightelbowkey_fs.findPlug("input", False)
                    nofliprighthandkeyinp_plug = nofliprighthandkey_fs.findPlug("input", False)
                    pvrightelbowkeyinp_plug = pvrightelbowkey_fs.findPlug("input", False)
                    pvrighthandkeyinp_plug = pvrighthandkey_fs.findPlug("input", False)

                    self.MDG2_mod.disconnect(rikarmjntDist_plug, nofliprightelbowkeyinp_plug)
                    self.MDG2_mod.disconnect(rikarmjntDist_plug, nofliprighthandkeyinp_plug)
                    self.MDG2_mod.disconnect(rikarmjntDist_plug, pvrightelbowkeyinp_plug)
                    self.MDG2_mod.disconnect(rikarmjntDist_plug, pvrighthandkeyinp_plug)
                    self.MDG2_mod.connect(riklowerarmjntDist_plug, nofliprighthandlobalscaleInp1Y_plug)
                    self.MDG2_mod.connect(rikupperarmjntDist_plug, nofliprightarmglobalscaleInp1Y_plug)
                    self.MDG2_mod.connect(riklowerarmjntDist_plug, nofliprighthandlobalscaleInp1Y_plug)
                    self.MDG2_mod.connect(masterlctrlsy_plug, nofliprightarmglobalscaleInp2Y_plug)
                    self.MDG2_mod.connect(masterlctrlsy_plug, nofliprighthandlobalscaleInp2Y_plug)
                    self.MDG2_mod.connect(nofliprightarmglobalscaleOtpY_plug, rikpvupperarmtransblendnodeinp1g_plug)
                    self.MDG2_mod.connect(nofliprighthandlobalscaleOtpY_plug, rikpvlowerarmtransblendnodeinp1g_plug)
                    self.MDG2_mod.connect(rikarmjntDist_plug, rightarmglobalscaleInp1Y_plug)
                    self.MDG2_mod.connect(masterlctrlsy_plug, rightarmglobalscaleInp2Y_plug)
                    self.MDG2_mod.connect(rightarmglobalscaleOtpY_plug, nofliprightelbowkeyinp_plug)
                    self.MDG2_mod.connect(rightarmglobalscaleOtpY_plug, nofliprighthandkeyinp_plug)
                    self.MDG2_mod.connect(rightarmglobalscaleOtpY_plug, pvrightelbowkeyinp_plug)
                    self.MDG2_mod.connect(rightarmglobalscaleOtpY_plug, pvrighthandkeyinp_plug)
                    self.MDG2_mod.commandToExecute('setAttr "IKNoFlipRightForeArmGlobalScale_Average.operation" 2')
                    self.MDG2_mod.commandToExecute('setAttr "IKNoFlipRightHandGlobalScale_Average.operation" 2')
                    self.MDG2_mod.commandToExecute('setAttr "IKRightArmGlobalScale_Average.operation" 2')

                # else:
                #     # self.MDG2_mod.commandToExecute('delete "IkStretchyRightJointArm_grp"')
                #     # self.MDG2_mod.commandToExecute('delete "RightArmIkCluster_grp"')

        else:
            self.MDG2_mod.commandToExecute('delete "Biped_IkRightHand_null"')
            self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false Biped_RightHandOptions_ctrl.fkik')
            self.MDG2_mod.commandToExecute('setAttr "IkRightArm.visibility" 0')

        rfinger_sl_ls = om2.MSelectionList()
        rfinger_sl_ls.add("RightFinger*")
        for index in range(rfinger_sl_ls.length()):
            jnt_obj = rfinger_sl_ls.getDependNode(index)
            jnt_string = rfinger_sl_ls.getSelectionStrings(index)

            if jnt_obj.hasFn(om2.MFn.kJoint):
                rfingerctrl_multMatrix = self.MDG2_mod.createNode("multMatrix")
                rfingerctrl_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                self.MDG2_mod.renameNode(rfingerctrl_multMatrix, str(jnt_string)[2:][:-3] + "_multMatrix")
                self.MDG2_mod.renameNode(rfingerctrl_decomposeMatrix, str(jnt_string)[2:][:-3] + "_decomposeMatrix")

                rfingermultMatrix_fs = om2.MFnDependencyNode(rfingerctrl_multMatrix)
                rfingerdecomposeMatrix_fs = om2.MFnDependencyNode(rfingerctrl_decomposeMatrix)
                rfingerjnt_fs = om2.MFnDependencyNode(jnt_obj)

                rfingermultMatrixSum_plug = rfingermultMatrix_fs.findPlug("matrixSum", False)
                rfingerdecomposeInpMatrix_plug = rfingerdecomposeMatrix_fs.findPlug("inputMatrix", False)
                rfingerdecomposeOtpTrans_plug = rfingerdecomposeMatrix_fs.findPlug("outputTranslate", False)
                rfingerdecomposeOtpRot_plug = rfingerdecomposeMatrix_fs.findPlug("outputRotate", False)
                rfingerjntTrans_plug = rfingerjnt_fs.findPlug("translate", False)
                rfingerjntRot_plug = rfingerjnt_fs.findPlug("rotate", False)

                self.MDG2_mod.commandToExecute('connectAttr -force Biped_{0}_ctrl.worldMatrix[0] {0}_multMatrix.matrixIn[0]'.format(str(jnt_string)[3:][:-3]))
                self.MDG2_mod.commandToExecute('connectAttr -force {0}.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(jnt_string)[3:][:-3]))
                self.MDG2_mod.connect(rfingermultMatrixSum_plug, rfingerdecomposeInpMatrix_plug)
                self.MDG2_mod.connect(rfingerdecomposeOtpTrans_plug, rfingerjntTrans_plug)
                self.MDG2_mod.connect(rfingerdecomposeOtpRot_plug, rfingerjntRot_plug)
                self.MDG2_mod.connect(lfingerdecomposeOtpRot_plug, lfingerjntRot_plug)
                if cmds.getAttr("{0}.jointOrientX".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientY".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientZ".format(str(jnt_string)[3:][:-3])) != 0:
                    self.MDG2_mod.commandToExecute('setAttr "{0}.jointOrientX" 0'.format(str(jnt_string)[3:][:-3]))
                    self.MDG2_mod.commandToExecute('setAttr "{0}.jointOrientY" 0'.format(str(jnt_string)[3:][:-3]))
                    self.MDG2_mod.commandToExecute('setAttr "{0}.jointOrientZ" 0'.format(str(jnt_string)[3:][:-3]))

                if cmds.objExists("Biped_{0}4_ctrl".format(str(jnt_string)[3:][:-4])):
                    self.MDG2_mod.commandToExecute('setAttr "Biped_{0}4_ctrl.visibility" 0'.format(str(jnt_string)[3:][:-4]))

        self.MDG2_mod.commandToExecute('addAttr -longName "curl" -niceName "Curl" -attributeType double -keyable true -minValue -10 -maxValue 10 -defaultValue 0 Biped_RightFingerOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "spread" -niceName "Spread" -attributeType double -keyable true -defaultValue 0 Biped_RightFingerOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "relax" -niceName "Relax" -attributeType double -minValue -10 -maxValue 10 -keyable true -defaultValue 0 Biped_RightFingerOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "curl" -niceName "Curl" -attributeType double -keyable true -minValue -10 -maxValue 10 -defaultValue 0 Biped_RightThumbOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "curl" -niceName "Curl" -attributeType double -keyable true -minValue -10 -maxValue 10 -defaultValue 0 Biped_RightIndexOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "curl" -niceName "Curl" -attributeType double -keyable true -minValue -10 -maxValue 10 -defaultValue 0 Biped_RightMiddleOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "curl" -niceName "Curl" -attributeType double -keyable true -minValue -10 -maxValue 10 -defaultValue 0 Biped_RightRingOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "curl" -niceName "Curl" -attributeType double -keyable true -minValue -10 -maxValue 10 -defaultValue 0 Biped_RightPinkyOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "lean" -niceName "Lean" -attributeType double -keyable true -defaultValue 0 Biped_RightThumbOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "lean" -niceName "Lean" -attributeType double -keyable true -defaultValue 0 Biped_RightIndexOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "lean" -niceName "Lean" -attributeType double -keyable true -defaultValue 0 Biped_RightMiddleOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "lean" -niceName "Lean" -attributeType double -keyable true -defaultValue 0 Biped_RightRingOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "lean" -niceName "Lean" -attributeType double -keyable true -defaultValue 0 Biped_RightPinkyOptions_ctrl')
        self.MDG2_mod.doIt()

        rfingercurl_sl_ls = om2.MSelectionList()
        rfingercurl_sl_ls.add("Biped_RightFinger*_curl")

        self.MDG2_mod.commandToExecute('float $rightfingeroptionsspread = `getAttr "Biped_RightFingerOptions_ctrl.spread"`; float $rightfingerthumbrotateZ = `getAttr "Biped_RightFingerThumb1_globalcurl.rotateZ"`; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.spread -driverValue $rightfingeroptionsspread -attribute "rotateZ" -value $rightfingerthumbrotateZ Biped_RightFingerThumb1_globalcurl;')
        self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 20.0; float $rightfingeroptionsspread = `getAttr "Biped_RightFingerOptions_ctrl.spread"`; float $rightfingerthumbrotateZ = `getAttr "Biped_RightFingerThumb1_globalcurl.rotateZ"`; float $totalrightfingeroptionsspread = $rightfingeroptionsspread + $add1; float $totalrightthumbrotateZ = $rightfingerthumbrotateZ + $add2; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.spread -driverValue $totalrightfingeroptionsspread -attribute "rotateZ" -value $totalrightthumbrotateZ Biped_RightFingerThumb1_globalcurl;')
        self.MDG2_mod.commandToExecute('float $rightfingeroptionsspread = `getAttr "Biped_RightFingerOptions_ctrl.spread"`; float $rightfingerindexrotateZ = `getAttr "Biped_RightFingerIndex1_globalcurl.rotateZ"`; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.spread -driverValue $rightfingeroptionsspread -attribute "rotateZ" -value $rightfingerindexrotateZ Biped_RightFingerIndex1_globalcurl;')
        self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 10.0; float $rightfingeroptionsspread = `getAttr "Biped_RightFingerOptions_ctrl.spread"`; float $rightfingerindexrotateZ = `getAttr "Biped_RightFingerIndex1_globalcurl.rotateZ"`; float $totalrightfingeroptionsspread = $rightfingeroptionsspread + $add1; float $totalrightindexrotateZ = $rightfingerindexrotateZ + $add2; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.spread -driverValue $totalrightfingeroptionsspread -attribute "rotateZ" -value $totalrightindexrotateZ Biped_RightFingerIndex1_globalcurl;')
        self.MDG2_mod.commandToExecute('float $rightfingeroptionsspread = `getAttr "Biped_RightFingerOptions_ctrl.spread"`; float $rightfingermiddlerotateZ = `getAttr "Biped_RightFingerMiddle1_globalcurl.rotateZ"`; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.spread -driverValue $rightfingeroptionsspread -attribute "rotateZ" -value $rightfingermiddlerotateZ Biped_RightFingerMiddle1_globalcurl;')
        self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 2.0; float $rightfingeroptionsspread = `getAttr "Biped_RightFingerOptions_ctrl.spread"`; float $rightfingermiddlerotateZ = `getAttr "Biped_RightFingerMiddle1_globalcurl.rotateZ"`; float $totalrightfingeroptionsspread = $rightfingeroptionsspread + $add1; float $totalrightmiddlerotateZ = $rightfingermiddlerotateZ + $add2; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.spread -driverValue $totalrightfingeroptionsspread -attribute "rotateZ" -value $totalrightmiddlerotateZ Biped_RightFingerMiddle1_globalcurl;')
        self.MDG2_mod.commandToExecute('float $rightfingeroptionsspread = `getAttr "Biped_RightFingerOptions_ctrl.spread"`; float $rightfingerringrotateZ = `getAttr "Biped_RightFingerRing1_globalcurl.rotateZ"`; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.spread -driverValue $rightfingeroptionsspread -attribute "rotateZ" -value $rightfingerringrotateZ Biped_RightFingerRing1_globalcurl;')
        self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = -8.0; float $rightfingeroptionsspread = `getAttr "Biped_RightFingerOptions_ctrl.spread"`; float $rightfingerringrotateZ = `getAttr "Biped_RightFingerRing1_globalcurl.rotateZ"`; float $totalrightfingeroptionsspread = $rightfingeroptionsspread + $add1; float $totalrightringrotateZ = $rightfingerringrotateZ + $add2; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.spread -driverValue $totalrightfingeroptionsspread -attribute "rotateZ" -value $totalrightringrotateZ Biped_RightFingerRing1_globalcurl;')
        self.MDG2_mod.commandToExecute('float $rightfingeroptionsspread = `getAttr "Biped_RightFingerOptions_ctrl.spread"`; float $rightfingerpinkyrotateZ = `getAttr "Biped_RightFingerPinky1_globalcurl.rotateZ"`; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.spread -driverValue $rightfingeroptionsspread -attribute "rotateZ" -value $rightfingerpinkyrotateZ Biped_RightFingerPinky1_globalcurl;')
        self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = -15.0; float $rightfingeroptionsspread = `getAttr "Biped_RightFingerOptions_ctrl.spread"`; float $rightfingerpinkyrotateZ = `getAttr "Biped_RightFingerPinky1_globalcurl.rotateZ"`; float $totalrightfingeroptionsspread = $rightfingeroptionsspread + $add1; float $totalrightpinkyrotateZ = $rightfingerpinkyrotateZ + $add2; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.spread -driverValue $totalrightfingeroptionsspread -attribute "rotateZ" -value $totalrightpinkyrotateZ Biped_RightFingerPinky1_globalcurl;')

        for index in range(rfingercurl_sl_ls.length()):
            rfingercurl_obj = rfingercurl_sl_ls.getDependNode(index)
            rfingercurl_string = rfingercurl_sl_ls.getSelectionStrings(index)

            if rfingercurl_obj.hasFn(om2.MFn.kTransform):
                self.MDG2_mod.commandToExecute('connectAttr -force Biped_Right{0}Options_ctrl.curl Biped_RightFinger{1}_curl.rotateX'.format(str(rfingercurl_string)[20:][:-9], str(rfingercurl_string)[20:][:-8]))
                self.MDG2_mod.commandToExecute('connectAttr -force Biped_Right{0}Options_ctrl.lean Biped_RightFinger{1}_curl.rotateZ'.format(str(rfingercurl_string)[20:][:-9], str(rfingercurl_string)[20:][:-8]))

            for index in range(1,5):
                self.MDG2_mod.commandToExecute('float $rightfingeroptionscurl = `getAttr "Biped_RightFingerOptions_ctrl.curl"`; float $rightfingerindexrotateX = `getAttr "Biped_RightFingerIndex{0}_globalcurl.rotateX"`; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.curl -driverValue $rightfingeroptionscurl -attribute "rotateX" -value $leftfingerindexrotateX Biped_RightFingerIndex{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 90.0; float $rightfingeroptionscurl = `getAttr "Biped_RightFingerOptions_ctrl.curl"`; float $rightfingerindexrotateX = `getAttr "Biped_RightFingerIndex{0}_globalcurl.rotateX"`; float $totalrightfingeroptionscurl = $rightfingeroptionscurl + $add1; float $totalrightindexrotateX = $rightfingerindexrotateX + $add2; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.curl -driverValue $totalrightfingeroptionscurl -attribute "rotateX" -value $totalrightindexrotateX Biped_RightFingerIndex{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = -10.0; float $add2 = -90.0; float $rightfingeroptionscurl = `getAttr "Biped_RightFingerOptions_ctrl.curl"`; float $rightfingerindexrotateX = `getAttr "Biped_RightFingerIndex{0}_globalcurl.rotateX"`; float $totalrightfingeroptionscurl = $rightfingeroptionscurl + $add1; float $totalrightindexrotateX = $rightfingerindexrotateX + $add2; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.curl -driverValue $totalrightfingeroptionscurl -attribute "rotateX" -value $totalrightindexrotateX Biped_RightFingerIndex{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $rightfingeroptionscurl = `getAttr "Biped_RightFingerOptions_ctrl.curl"`; float $rightfingermiddlerotateX = `getAttr "Biped_RightFingerMiddle{0}_globalcurl.rotateX"`; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.curl -driverValue $rightfingeroptionscurl -attribute "rotateX" -value $rightfingermiddlerotateX Biped_RightFingerMiddle{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 90.0; float $rightfingeroptionscurl = `getAttr "Biped_RightFingerOptions_ctrl.curl"`; float $rightfingermiddlerotateX = `getAttr "Biped_RightFingerMiddle{0}_globalcurl.rotateX"`; float $totalrightfingeroptionscurl = $rightfingeroptionscurl + $add1; float $totalrightmiddlerotateX = $rightfingermiddlerotateX + $add2; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.curl -driverValue $totalrightfingeroptionscurl -attribute "rotateX" -value $totalrightmiddlerotateX Biped_RightFingerMiddle{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = -10.0; float $add2 = -90.0; float $rightfingeroptionscurl = `getAttr "Biped_RightFingerOptions_ctrl.curl"`; float $rightfingermiddlerotateX = `getAttr "Biped_RightFingerMiddle{0}_globalcurl.rotateX"`; float $totalrightfingeroptionscurl = $rightfingeroptionscurl + $add1; float $totalrightmiddlerotateX = $rightfingermiddlerotateX + $add2; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.curl -driverValue $totalrightfingeroptionscurl -attribute "rotateX" -value $totalrightmiddlerotateX Biped_RightFingerMiddle{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $rightfingeroptionscurl = `getAttr "Biped_RightFingerOptions_ctrl.curl"`; float $rightfingerringrotateX = `getAttr "Biped_RightFingerRing{0}_globalcurl.rotateX"`; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.curl -driverValue $rightfingeroptionscurl -attribute "rotateX" -value $rightfingerringrotateX Biped_RightFingerRing{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 90.0; float $rightfingeroptionscurl = `getAttr "Biped_RightFingerOptions_ctrl.curl"`; float $rightfingerringrotateX = `getAttr "Biped_RightFingerRing{0}_globalcurl.rotateX"`; float $totalrightfingeroptionscurl = $rightfingeroptionscurl + $add1; float $totalrightringrotateX = $rightfingerringrotateX + $add2; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.curl -driverValue $totalrightfingeroptionscurl -attribute "rotateX" -value $totalrightringrotateX Biped_RightFingerRing{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = -10.0; float $add2 = -90.0; float $rightfingeroptionscurl = `getAttr "Biped_RightFingerOptions_ctrl.curl"`; float $rightfingerringrotateX = `getAttr "Biped_RightFingerRing{0}_globalcurl.rotateX"`; float $totalrightfingeroptionscurl = $rightfingeroptionscurl + $add1; float $totalrightringrotateX = $rightfingerringrotateX + $add2; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.curl -driverValue $totalrightfingeroptionscurl -attribute "rotateX" -value $totalrightringrotateX Biped_RightFingerRing{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $rightfingeroptionscurl = `getAttr "Biped_RightFingerOptions_ctrl.curl"`; float $rightfingerpinkyrotateX = `getAttr "Biped_RightFingerPinky{0}_globalcurl.rotateX"`; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.curl -driverValue $rightfingeroptionscurl -attribute "rotateX" -value $rightfingerpinkyrotateX Biped_RightFingerPinky{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 90.0; float $rightfingeroptionscurl = `getAttr "Biped_RightFingerOptions_ctrl.curl"`; float $rightfingerpinkyrotateX = `getAttr "Biped_RightFingerPinky{0}_globalcurl.rotateX"`; float $totalrightfingeroptionscurl = $rightfingeroptionscurl + $add1; float $totalrightpinkyrotateX = $rightfingerpinkyrotateX + $add2; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.curl -driverValue $totalrightfingeroptionscurl -attribute "rotateX" -value $totalrightpinkyrotateX Biped_RightFingerPinky{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = -10.0; float $add2 = -90.0; float $rightfingeroptionscurl = `getAttr "Biped_RightFingerOptions_ctrl.curl"`; float $rightfingerpinkyrotateX = `getAttr "Biped_RightFingerPinky{0}_globalcurl.rotateX"`; float $totalrightfingeroptionscurl = $rightfingeroptionscurl + $add1; float $totalrightpinkyrotateX = $rightfingerpinkyrotateX + $add2; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.curl -driverValue $totalrightfingeroptionscurl -attribute "rotateX" -value $totalrightpinkyrotateX Biped_RightFingerPinky{0}_globalcurl;'.format(index))

                self.MDG2_mod.commandToExecute('float $rightfingeroptionsrelax = `getAttr "Biped_RightFingerOptions_ctrl.relax"`; float $rightfingerindexrotateX = `getAttr "Biped_RightFingerIndex{0}_globalcurl.rotateX"`; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.relax -driverValue $rightfingeroptionsrelax -attribute "rotateX" -value $rightfingerindexrotateX Biped_RightFingerIndex{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 15.0; float $rightfingeroptionsrelax = `getAttr "Biped_RightFingerOptions_ctrl.relax"`; float $rightfingerindexrotateX = `getAttr "Biped_RightFingerIndex{0}_globalcurl.rotateX"`; float $totalrightfingeroptionsrelax = $rightfingeroptionsrelax + $add1; float $totalrightindexrotateX = $rightfingerindexrotateX + $add2; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.relax -driverValue $totalrightfingeroptionsrelax -attribute "rotateX" -value $totalrightindexrotateX Biped_RightFingerIndex{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = -10.0; float $add2 = 5.0; float $rightfingeroptionsrelax = `getAttr "Biped_RightFingerOptions_ctrl.relax"`; float $rightfingerindexrotateX = `getAttr "Biped_RightFingerIndex{0}_globalcurl.rotateX"`; float $totalrightfingeroptionsrelax = $rightfingeroptionsrelax + $add1; float $totalrightindexrotateX = $rightfingerindexrotateX + $add2; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.relax -driverValue $totalrightfingeroptionsrelax -attribute "rotateX" -value $totalrightindexrotateX Biped_RightFingerIndex{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $rightfingeroptionsrelax = `getAttr "Biped_RightFingerOptions_ctrl.relax"`; float $rightfingermiddlerotateX = `getAttr "Biped_RightFingerMiddle{0}_globalcurl.rotateX"`; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.relax -driverValue $rightfingeroptionsrelax -attribute "rotateX" -value $rightfingermiddlerotateX Biped_RightFingerMiddle{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 10.0; float $rightfingeroptionsrelax = `getAttr "Biped_RightFingerOptions_ctrl.relax"`; float $rightfingermiddlerotateX = `getAttr "Biped_RightFingerMiddle{0}_globalcurl.rotateX"`; float $totalrightfingeroptionsrelax = $rightfingeroptionsrelax + $add1; float $totalrightmiddlerotateX = $rightfingermiddlerotateX + $add2; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.relax -driverValue $totalrightfingeroptionsrelax -attribute "rotateX" -value $totalrightmiddlerotateX Biped_RightFingerMiddle{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = -10.0; float $add2 = 8.0; float $rightfingeroptionsrelax = `getAttr "Biped_RightFingerOptions_ctrl.relax"`; float $rightfingermiddlerotateX = `getAttr "Biped_RightFingerMiddle{0}_globalcurl.rotateX"`; float $totalrightfingeroptionsrelax = $rightfingeroptionsrelax + $add1; float $totalrightmiddlerotateX = $rightfingermiddlerotateX + $add2; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.relax -driverValue $totalrightfingeroptionsrelax -attribute "rotateX" -value $totalrightmiddlerotateX Biped_RightFingerMiddle{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $rightfingeroptionsrelax = `getAttr "Biped_RightFingerOptions_ctrl.relax"`; float $rightfingerringrotateX = `getAttr "Biped_RightFingerRing{0}_globalcurl.rotateX"`; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.relax -driverValue $rightfingeroptionsrelax -attribute "rotateX" -value $rightfingerringrotateX Biped_RightFingerRing{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 8.0; float $rightfingeroptionsrelax = `getAttr "Biped_RightFingerOptions_ctrl.relax"`; float $rightfingerringrotateX = `getAttr "Biped_RightFingerRing{0}_globalcurl.rotateX"`; float $totalrightfingeroptionsrelax = $rightfingeroptionsrelax + $add1; float $totalrightringrotateX = $rightfingerringrotateX + $add2; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.relax -driverValue $totalrightfingeroptionsrelax -attribute "rotateX" -value $totalrightringrotateX Biped_RightFingerRing{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = -10.0; float $add2 = 10.0; float $rightfingeroptionsrelax = `getAttr "Biped_RightFingerOptions_ctrl.relax"`; float $rightfingerringrotateX = `getAttr "Biped_RightFingerRing{0}_globalcurl.rotateX"`; float $totalrightfingeroptionsrelax = $rightfingeroptionsrelax + $add1; float $totalrightringrotateX = $rightfingerringrotateX + $add2; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.relax -driverValue $totalrightfingeroptionsrelax -attribute "rotateX" -value $totalrightringrotateX Biped_RightFingerRing{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $rightfingeroptionsrelax = `getAttr "Biped_RightFingerOptions_ctrl.relax"`; float $rightfingerpinkyrotateX = `getAttr "Biped_RightFingerPinky{0}_globalcurl.rotateX"`; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.relax -driverValue $rightfingeroptionsrelax -attribute "rotateX" -value $rightfingerpinkyrotateX Biped_RightFingerPinky{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = 10.0; float $add2 = 5.0; float $rightfingeroptionsrelax = `getAttr "Biped_RightFingerOptions_ctrl.relax"`; float $rightfingerpinkyrotateX = `getAttr "Biped_RightFingerPinky{0}_globalcurl.rotateX"`; float $totalrightfingeroptionsrelax = $rightfingeroptionsrelax + $add1; float $totalrightpinkyrotateX = $rightfingerpinkyrotateX + $add2; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.relax -driverValue $totalrightfingeroptionsrelax -attribute "rotateX" -value $totalrightpinkyrotateX Biped_RightFingerPinky{0}_globalcurl;'.format(index))
                self.MDG2_mod.commandToExecute('float $add1 = -10.0; float $add2 = 15.0; float $rightfingeroptionsrelax = `getAttr "Biped_RightFingerOptions_ctrl.relax"`; float $rightfingerpinkyrotateX = `getAttr "Biped_RightFingerPinky{0}_globalcurl.rotateX"`; float $totalrightfingeroptionsrelax = $rightfingeroptionsrelax + $add1; float $totalrightpinkyrotateX = $rightfingerpinkyrotateX + $add2; setDrivenKeyframe -currentDriver Biped_RightFingerOptions_ctrl.relax -driverValue $totalrightfingeroptionsrelax -attribute "rotateX" -value $totalrightpinkyrotateX Biped_RightFingerPinky{0}_globalcurl;'.format(index))

                self.MDG2_mod.commandToExecute('selectKey Biped_RightFingerThumb{0}_globalcurl; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative -preInfinite cycleRelative'.format(index))
                self.MDG2_mod.commandToExecute('selectKey Biped_RightFingerIndex{0}_globalcurl; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative -preInfinite cycleRelative'.format(index))
                self.MDG2_mod.commandToExecute('selectKey Biped_RightFingerMiddle{0}_globalcurl; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative -preInfinite cycleRelative'.format(index))
                self.MDG2_mod.commandToExecute('selectKey Biped_RightFingerRing{0}_globalcurl; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative -preInfinite cycleRelative'.format(index))
                self.MDG2_mod.commandToExecute('selectKey Biped_RightFingerPinky{0}_globalcurl; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative -preInfinite cycleRelative'.format(index))


        rfingergrp_sl_ls = om2.MSelectionList()
        rfingergrp_sl_ls.add("Biped_RightFingers_null")
        grp_obj = rfingergrp_sl_ls.getDependNode(0)

        rfingergrp_multMatrix = self.MDG2_mod.createNode("multMatrix")
        rfingergrp_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
        self.MDG2_mod.renameNode(rfingergrp_multMatrix, "RightFingers_multMatrix")
        self.MDG2_mod.renameNode(rfingergrp_decomposeMatrix, "RightFingers_decomposeMatrix")

        rfingergrpmultMatrix_fs = om2.MFnDependencyNode(rfingergrp_multMatrix)
        rfingergrpdecomposeMatrix_fs = om2.MFnDependencyNode(rfingergrp_decomposeMatrix)
        rfingergrp_fs = om2.MFnDependencyNode(grp_obj)

        rfingergrpmultMatrixSum_plug = rfingergrpmultMatrix_fs.findPlug("matrixSum", False)
        rfingergrpdecomposeInpMatrix_plug = rfingergrpdecomposeMatrix_fs.findPlug("inputMatrix", False)
        rfingergrpdecomposeOtpTrans_plug = rfingergrpdecomposeMatrix_fs.findPlug("outputTranslate", False)
        rfingergrpdecomposeOtpRot_plug = rfingergrpdecomposeMatrix_fs.findPlug("outputRotate", False)
        rfingergrpjntTrans_plug = rfingergrp_fs.findPlug("translate", False)
        rfingergrpjntRot_plug = rfingergrp_fs.findPlug("rotate", False)

        self.MDG2_mod.commandToExecute('connectAttr -force RightHand.worldMatrix[0] RightFingers_multMatrix.matrixIn[0]')
        self.MDG2_mod.commandToExecute('connectAttr -force Biped_RightFingers_null.parentInverseMatrix[0] RightFingers_multMatrix.matrixIn[1]')
        self.MDG2_mod.connect(rfingergrpmultMatrixSum_plug, rfingergrpdecomposeInpMatrix_plug)
        self.MDG2_mod.connect(rfingergrpdecomposeOtpTrans_plug, rfingergrpjntTrans_plug)
        self.MDG2_mod.connect(rfingergrpdecomposeOtpRot_plug, rfingergrpjntRot_plug)

        ikrleg_sl_ls = om2.MSelectionList()
        ikrleg_sl_ls.add("IkRightUpLeg")
        ikrleg_sl_ls.add("IkRightLeg")
        ikrleg_sl_ls.add("IkRightFoot")
        ikrleg_sl_ls.add("IkRightToeBase")

        noflipikrleg_sl_ls = om2.MSelectionList()
        noflipikrleg_sl_ls.add("IkNoFlipRightUpLeg")
        noflipikrleg_sl_ls.add("IkNoFlipRightLeg")
        noflipikrleg_sl_ls.add("IkNoFlipRightFoot")

        pvikrleg_sl_ls = om2.MSelectionList()
        pvikrleg_sl_ls.add("IkPVRightUpLeg")
        pvikrleg_sl_ls.add("IkPVRightLeg")
        pvikrleg_sl_ls.add("IkPVRightFoot")

        rlegoptions_sl_ls = om2.MSelectionList()
        rlegoptions_sl_ls.add("Biped_RightFootOptions_ctrl")
        rlegoptions_sl_ls.add("FkRightJointLeg_grp")
        rlegoptions_sl_ls.add("RightJointLeg_grp")
        rlegoptions_obj = rlegoptions_sl_ls.getDependNode(0)
        fkrleggrp_obj = rlegoptions_sl_ls.getDependNode(1)
        rleggrp_obj = rlegoptions_sl_ls.getDependNode(2)

        self.MDG2_mod.commandToExecute('addAttr -longName "stretchy" -niceName "Stretchy" -attributeType double -keyable true -defaultValue 0 Biped_FkRightUpLeg_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "stretchy" -niceName "Stretchy" -attributeType double -keyable true -defaultValue 0 Biped_FkRightLeg_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "fkik" -niceName "Fk/Ik" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_RightFootOptions_ctrl')
        self.MDG2_mod.commandToExecute('addAttr -longName "kneeswitch" -niceName "Auto/Manual Knee" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_RightFootOptions_ctrl')
        self.MDG2_mod.doIt()

        rlegoptions_fs = om2.MFnDependencyNode(rlegoptions_obj)
        rlegoptionsfkik_plug = rlegoptions_fs.findPlug("fkik", False)
        rlegoptionskneeswitch_plug = rlegoptions_fs.findPlug("kneeswitch", False)

        for index in range(fkrleg_sl_ls.length()):
            jnt_obj = fkrleg_sl_ls.getDependNode(index)
            jnt_string = fkrleg_sl_ls.getSelectionStrings(index)

            ikjnt_obj = ikrleg_sl_ls.getDependNode(index)
            ikjnt_string = ikrleg_sl_ls.getSelectionStrings(index)

            bindjnt_obj = rleg_sl_ls.getDependNode(index)
            bindjnt_string = rleg_sl_ls.getSelectionStrings(index)

            if jnt_obj.hasFn(om2.MFn.kJoint):
                rlegctrl_multMatrix = self.MDG2_mod.createNode("multMatrix")
                rlegctrl_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                self.MDG2_mod.renameNode(rlegctrl_multMatrix, str(jnt_string)[2:][:-3] + "_multMatrix")
                self.MDG2_mod.renameNode(rlegctrl_decomposeMatrix, str(jnt_string)[2:][:-3] + "_decomposeMatrix")

                rlegmultMatrix_fs = om2.MFnDependencyNode(rlegctrl_multMatrix)
                rlegdecomposeMatrix_fs = om2.MFnDependencyNode(rlegctrl_decomposeMatrix)
                rlegjnt_fs = om2.MFnDependencyNode(jnt_obj)

                rlegmultMatrixSum_plug = rlegmultMatrix_fs.findPlug("matrixSum", False)
                rlegdecomposeInpMatrix_plug = rlegdecomposeMatrix_fs.findPlug("inputMatrix", False)
                rlegdecomposeOtpTrans_plug = rlegdecomposeMatrix_fs.findPlug("outputTranslate", False)
                rlegdecomposeOtpRot_plug = rlegdecomposeMatrix_fs.findPlug("outputRotate", False)
                rlegjntTrans_plug = rlegjnt_fs.findPlug("translate", False)
                rlegjntRot_plug = rlegjnt_fs.findPlug("rotate", False)

                self.MDG2_mod.commandToExecute('connectAttr -force Biped_{0}_ctrl.worldMatrix[0] {0}_multMatrix.matrixIn[0]'.format(str(jnt_string)[3:][:-3]))
                self.MDG2_mod.commandToExecute('connectAttr -force {0}.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(jnt_string)[3:][:-3]))
                self.MDG2_mod.connect(rlegmultMatrixSum_plug, rlegdecomposeInpMatrix_plug)
                self.MDG2_mod.connect(rlegdecomposeOtpTrans_plug, rlegjntTrans_plug)
                self.MDG2_mod.connect(rlegdecomposeOtpRot_plug, rlegjntRot_plug)

                if cmds.getAttr("{0}.jointOrientX".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientY".format(str(jnt_string)[3:][:-3])) != 0 or cmds.getAttr("{0}.jointOrientZ".format(str(jnt_string)[3:][:-3])) != 0:
                    self.MDG2_mod.commandToExecute('setAttr "{0}.jointOrientX" 0'.format(str(jnt_string)[3:][:-3]))
                    self.MDG2_mod.commandToExecute('setAttr "{0}.jointOrientY" 0'.format(str(jnt_string)[3:][:-3]))
                    self.MDG2_mod.commandToExecute('setAttr "{0}.jointOrientZ" 0'.format(str(jnt_string)[3:][:-3]))

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

                if cmds.objExists("NoFlipRightLeg_Ik") and cmds.objExists("PVRightLeg_Ik"):
                    legrotblendnode = self.MDG2_mod.createNode("blendColors")
                    legtransblendnode = self.MDG2_mod.createNode("blendColors")
                    legjoint_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                    self.MDG2_mod.renameNode(legjoint_decomposeMatrix, str(bindjnt_string)[2:][:-3] + "Blend_decomposeMatrix")
                    self.MDG2_mod.renameNode(legrotblendnode, str(bindjnt_string)[2:][:-3] + "_blend")
                    self.MDG2_mod.renameNode(legtransblendnode, str(bindjnt_string)[2:][:-3] + "Trans_blend")

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

                    self.MDG2_mod.connect(iklegjointotp_plug, legdecomposeInpMatrix_plug)
                    self.MDG2_mod.connect(legdecomposeOtpRot_plug, legrotblendnodeinp1_plug)
                    self.MDG2_mod.connect(legdecomposeOtpTrans_plug, legtransblendnodeinp1_plug)
                    self.MDG2_mod.connect(fklegjointrototp_plug, legrotblendnodeinp2_plug)
                    self.MDG2_mod.connect(fklegjointtransotp_plug, legtransblendnodeinp2_plug)
                    self.MDG2_mod.connect(legrotblendnodeotp_plug, legjointrotinp_plug)
                    self.MDG2_mod.connect(legtransblendnodeotp_plug, legjointtransinp_plug)
                    self.MDG2_mod.connect(rlegoptionsfkik_plug, legrotblendnodeblender_plug)
                    self.MDG2_mod.connect(rlegoptionsfkik_plug, legtransblendnodeblender_plug)

                    if index < 3:
                        noflipjnt_obj = noflipikrleg_sl_ls.getDependNode(index)
                        noflipjnt_string = noflipikrleg_sl_ls.getSelectionStrings(index)

                        pvjnt_obj = pvikrleg_sl_ls.getDependNode(index)
                        pvjnt_string = pvikrleg_sl_ls.getSelectionStrings(index)

                        legrotblendnode = self.MDG2_mod.createNode("blendColors")
                        legtransblendnode = self.MDG2_mod.createNode("blendColors")
                        nofliplegjoint_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                        pvlegjoint_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                        self.MDG2_mod.renameNode(nofliplegjoint_decomposeMatrix, str(noflipjnt_string)[2:][:-3] + "Blend_decomposeMatrix")
                        self.MDG2_mod.renameNode(pvlegjoint_decomposeMatrix, str(pvjnt_string)[2:][:-3] + "Blend_decomposeMatrix")
                        self.MDG2_mod.renameNode(legrotblendnode, str(bindjnt_string)[2:][:-3] + "Rot_kneeblend")
                        self.MDG2_mod.renameNode(legtransblendnode, str(bindjnt_string)[2:][:-3] + "Trans_kneeblend")

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

                        self.MDG2_mod.connect(noflipiklegjointotp_plug, nofliplegdecomposeInpMatrix_plug)
                        self.MDG2_mod.connect(pviklegjointotp_plug, pvlegdecomposeInpMatrix_plug)
                        self.MDG2_mod.connect(pvlegdecomposeOtpRot_plug, legrotblendnodeinp1_plug)
                        self.MDG2_mod.connect(pvlegdecomposeOtpTrans_plug, legtransblendnodeinp1_plug)
                        self.MDG2_mod.connect(nofliplegdecomposeOtpRot_plug, legrotblendnodeinp2_plug)
                        self.MDG2_mod.connect(nofliplegdecomposeOtpTrans_plug, legtransblendnodeinp2_plug)
                        self.MDG2_mod.connect(legrotblendnodeotp_plug, iklegjointinpRot_plug)
                        self.MDG2_mod.connect(legtransblendnodeotp_plug, iklegjointinpTrans_plug)
                        self.MDG2_mod.connect(rlegoptionskneeswitch_plug, legrotblendnodeblender_plug)
                        self.MDG2_mod.connect(rlegoptionskneeswitch_plug, legtransblendnodeblender_plug)
                else:
                    self.MDG2_mod.connect(fklegjointtransotp_plug, legjointtransinp_plug)
                    self.MDG2_mod.connect(fklegjointrototp_plug, legjointrotinp_plug)

            if self.autostretch.currentIndex() == 1:
                if index < 2:
                    ikrleggrp_sl_lst = om2.MSelectionList()
                    ikrleggrp_sl_lst.add("RightUpperLegIkCluster_grp")
                    ikrleggrp_sl_lst.add("RightUpperLegIkCluster2_grp")
                    ikrleggrp_sl_lst.add("RightLowerLegIkCluster_grp")
                    ikrleggrp_sl_lst.add("RightLowerLegIkCluster2_grp")
                    grp_legupperikcluster = ikrleggrp_sl_lst.getDependNode(0)
                    grp_legupperikcluster2 = ikrleggrp_sl_lst.getDependNode(1)
                    grp_leglowerikcluster = ikrleggrp_sl_lst.getDependNode(2)
                    grp_armlowerikcluster2 = ikrleggrp_sl_lst.getDependNode(3)

                    rlegjoint_multMatrix = self.MDG2_mod.createNode("multMatrix")
                    legjoint_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")

                    rlegmultMatrix_fs = om2.MFnDependencyNode(rlegjoint_multMatrix)
                    rlegdecomposeMatrix_fs = om2.MFnDependencyNode(legjoint_decomposeMatrix)
                    iklupperleggrp_fs = om2.MFnDependencyNode(grp_legupperikcluster)
                    ikllowerleggrp_fs = om2.MFnDependencyNode(grp_leglowerikcluster)

                    rlegmultMatrixSum_plug = rlegmultMatrix_fs.findPlug("matrixSum", False)
                    rlegdecomposeInpMatrix_plug = rlegdecomposeMatrix_fs.findPlug("inputMatrix", False)
                    rlegdecomposeOtpTrans_plug = rlegdecomposeMatrix_fs.findPlug("outputTranslate", False)
                    rlegdecomposeOtpRot_plug = rlegdecomposeMatrix_fs.findPlug("outputRotate", False)
                    iklupperleggrpTrans_plug = iklupperleggrp_fs.findPlug("translate", False)
                    iklupperleggrpRot_plug = iklupperleggrp_fs.findPlug("rotate", False)
                    ikrlowerleggrpTrans_plug = ikllowerleggrp_fs.findPlug("translate", False)
                    ikrlowerleggrpRot_plug = ikllowerleggrp_fs.findPlug("rotate", False)

                    self.MDG2_mod.renameNode(rlegjoint_multMatrix, str(bindjnt_string)[2:][:-3] + "_multMatrix")
                    self.MDG2_mod.renameNode(legjoint_decomposeMatrix, str(bindjnt_string)[2:][:-3] + "_decomposeMatrix")
                    self.MDG2_mod.commandToExecute('connectAttr -force {0}.worldMatrix[0] {0}_multMatrix.matrixIn[0]'.format(str(bindjnt_string)[3:][:-3]))
                    self.MDG2_mod.connect(rlegmultMatrixSum_plug, rlegdecomposeInpMatrix_plug)

                    fkrlegstretch_expression = om1.MFnExpression()

                    if index == 0:
                        fkrlegstretch_expression.create("Biped_FkRightLeg_ctrl.translateY = Biped_FkRightUpLeg_ctrl.stretchy")
                        fkrlegstretch_expression.create("Biped_FkRightLeg_ctrl.translateZ = Biped_FkRightLeg_ctrl.translateY/10")

                        self.MDG2_mod.commandToExecute('connectAttr -force RightUpperLegIkCluster_grp.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(bindjnt_string)[3:][:-3]))
                        self.MDG2_mod.connect(rlegdecomposeOtpTrans_plug, iklupperleggrpTrans_plug)
                        self.MDG2_mod.connect(rlegdecomposeOtpRot_plug, iklupperleggrpRot_plug)

                        rupperlegcluster2_multMatrix = self.MDG2_mod.createNode("multMatrix")
                        rupperlegcluster2_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")

                        rupperlegcluster2multMatrix_fs = om2.MFnDependencyNode(rupperlegcluster2_multMatrix)
                        rupperlegcluster2decomposeMatrix_fs = om2.MFnDependencyNode(rupperlegcluster2_decomposeMatrix)
                        rupperlegcluster2_fs = om2.MFnDependencyNode(grp_legupperikcluster2)

                        rupperlegcluster2multMatrixSum_plug = rupperlegcluster2multMatrix_fs.findPlug("matrixSum", False)
                        rupperlegcluster2decomposeInpMatrix_plug = rupperlegcluster2decomposeMatrix_fs.findPlug("inputMatrix", False)
                        rupperlegcluster2decomposeOtpTrans_plug = rupperlegcluster2decomposeMatrix_fs.findPlug("outputTranslate", False)
                        rupperlegcluster2Trans_plug = rupperlegcluster2_fs.findPlug("translate", False)

                        self.MDG2_mod.renameNode(rupperlegcluster2_multMatrix, "RightUpperLegCluster2_multMatrix")
                        self.MDG2_mod.renameNode(rupperlegcluster2_decomposeMatrix, "RightUpperLegCluster2_decomposeMatrix")
                        self.MDG2_mod.connect(rupperlegcluster2multMatrixSum_plug, rupperlegcluster2decomposeInpMatrix_plug)
                        self.MDG2_mod.commandToExecute('connectAttr -force RightLeg.worldMatrix[0] RightUpperLegCluster2_multMatrix.matrixIn[0]')
                        self.MDG2_mod.commandToExecute('connectAttr -force RightUpperLegIkCluster2_grp.parentInverseMatrix[0] RightUpperLegCluster2_multMatrix.matrixIn[1]')
                        self.MDG2_mod.connect(rupperlegcluster2decomposeOtpTrans_plug, rupperlegcluster2Trans_plug)

                    elif index == 1:
                        fkrlegstretch_expression.create("Biped_FkRightFoot_ctrl.translateY = Biped_FkRightLeg_ctrl.stretchy")
                        fkrlegstretch_expression.create("Biped_FkRightFoot_ctrl.translateZ = Biped_FkRightFoot_ctrl.translateY*(-1.5)")

                        self.MDG2_mod.commandToExecute('connectAttr -force RightLowerLegIkCluster_grp.parentInverseMatrix[0] {0}_multMatrix.matrixIn[1]'.format(str(bindjnt_string)[3:][:-3]))
                        self.MDG2_mod.connect(rlegdecomposeOtpTrans_plug, ikrlowerleggrpTrans_plug)
                        self.MDG2_mod.connect(rlegdecomposeOtpRot_plug, ikrlowerleggrpRot_plug)

                        rlowerlegcluster2_multMatrix = self.MDG2_mod.createNode("multMatrix")
                        rlowerlegcluster2_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")

                        rlowerlegcluster2multMatrix_f = om2.MFnDependencyNode(rlowerlegcluster2_multMatrix)
                        rlowerlegcluster2decomposeMatrix_fs = om2.MFnDependencyNode(rlowerlegcluster2_decomposeMatrix)
                        rlowerlegcluster2_fs = om2.MFnDependencyNode(grp_armlowerikcluster2)

                        rlowerlegcluster2multMatrixSum_plug = rlowerlegcluster2multMatrix_f.findPlug("matrixSum", False)
                        rlowerlegcluster2decomposeInpMatrix_plug = rlowerlegcluster2decomposeMatrix_fs.findPlug("inputMatrix", False)
                        rlowerlegcluster2decomposeOtpTrans_plug = rlowerlegcluster2decomposeMatrix_fs.findPlug("outputTranslate", False)
                        rlowerlegcluster2Trans_plug = rlowerlegcluster2_fs.findPlug("translate", False)

                        self.MDG2_mod.renameNode(rlowerlegcluster2_multMatrix, "RightLowerLegCluster2_multMatrix")
                        self.MDG2_mod.renameNode(rlowerlegcluster2_decomposeMatrix, "RightLowerLegCluster2_decomposeMatrix")
                        self.MDG2_mod.commandToExecute('connectAttr -force RightFoot.worldMatrix[0] RightLowerLegCluster2_multMatrix.matrixIn[0]')
                        self.MDG2_mod.commandToExecute('connectAttr -force RightLowerLegIkCluster2_grp.parentInverseMatrix[0] RightLowerLegCluster2_multMatrix.matrixIn[1]')
                        self.MDG2_mod.connect(rlowerlegcluster2multMatrixSum_plug, rlowerlegcluster2decomposeInpMatrix_plug)
                        self.MDG2_mod.connect(rlowerlegcluster2decomposeOtpTrans_plug, rlowerlegcluster2Trans_plug)

            elif cmds.objExists("RightLegIkCluster_grp") and cmds.objExists("IkStretchyRightJointLeg_grp"):
                self.MDG2_mod.commandToExecute('delete "RightLegIkCluster_grp"')
                self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false Biped_FkRightUpLeg_ctrl.stretchy')
                self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false Biped_FkRightLeg_ctrl.stretchy')
                self.MDG2_mod.doIt()

        fkrleggrp_fs = om2.MFnDependencyNode(fkrleggrp_obj)
        rleggrp_fs = om2.MFnDependencyNode(rleggrp_obj)

        fkrleggrpScal_plug = fkrleggrp_fs.findPlug("scale", False)
        rleggrpScal_plug = rleggrp_fs.findPlug("scale", False)

        self.MDG2_mod.connect(masterdecomposeOtpScale_plug, fkrleggrpScal_plug)
        self.MDG2_mod.connect(masterdecomposeOtpScale_plug, rleggrpScal_plug)

        grp_legupperikcluster1 = om1.MObject()
        grp_legupperikcluster2 = om1.MObject()
        obj_stretchyrightfoot = om1.MObject()

        if self.autostretch.currentIndex() == 1:

            self.MDG2_mod.commandToExecute('addAttr -longName "stretchable" -niceName "Stretchable" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_RightFootOptions_ctrl')
            self.MDG2_mod.doIt()

            stretchy_sl_lst1.add("Biped_RightFootOptions_ctrl")
            stretchy_sl_lst1.getDependNode(5, obj_stretchyrightfoot)

            if cmds.objExists("IkSplineRightUpperLeg0"):
                ikrupperleg_sl_lst = om1.MSelectionList()
                ikrupperleg_sl_lst.add("IkSplineRightUpperLeg*")
                ikrupperleg_sl_lst.getDependNode(0, obj_root)
                ikrupperleg_sl_lst.getDependNode(ikrupperleg_sl_lst.length()-1, obj_endspine)

                ikrupperleggrp_sl_lst = om1.MSelectionList()
                ikrupperleggrp_sl_lst.add("RightUpperLegIkCluster1_grp")
                ikrupperleggrp_sl_lst.add("RightUpperLegIkCluster2_grp")
                ikrupperleggrp_sl_lst.getDependNode(0, grp_legupperikcluster1)
                ikrupperleggrp_sl_lst.getDependNode(1, grp_legupperikcluster2)

                rleg_pathnode = om1.MDagPath()
                rootspine_path = rleg_pathnode.getAPathTo(obj_root)

                try:
                    ikspineiksolver_lst.add("ikSplineSolver*")
                except:
                    cmds.createNode("ikSplineSolver")

                self.ikrleg_effector = self.IK_Effector.create(obj_endspine)
                ikrleg_effector_path = rleg_pathnode.getAPathTo(self.ikrleg_effector)

                self.rleg_ik = self.IK_Handle.create(rootspine_path, ikrleg_effector_path)

                obj_array = om1.MPointArray()
                obj_lst_mpoint = []
                obj = om1.MObject()
                for index in range(ikrupperleg_sl_lst.length()):
                    ikrupperleg_sl_lst.getDependNode(index, obj)
                    obj_path = self.MDag_path.getAPathTo(obj)
                    obj_tn = om1.MFnTransform(obj_path)
                    obj_t = obj_tn.translation(om1.MSpace.kWorld)
                    obj_lst_mpoint.append(om1.MPoint(obj_t))
                    obj_array.append(obj_lst_mpoint[index])

                self.ikspline_cv_tn = ikspinedag_n.create("transform", "RightUpperLeg_SplineCv")
                ikspline_cv = self.MNurbs1_cv.createWithEditPoints(obj_array, 1, 1, False, True, True, self.ikspline_cv_tn)
                cmds.parent("RightUpperLeg_SplineCv", "DoNotTouch")

                rlegcrv_info = ikspinedg_modifier.createNode("curveInfo")
                rlegstretchpercent = ikspinedg_modifier.createNode("multiplyDivide")
                rlegstretchpow = ikspinedg_modifier.createNode("multiplyDivide")
                rlegstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                rlegscalediv = ikspinedg_modifier.createNode("multiplyDivide")
                riklegstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                blendstretch = ikspinedg_modifier.createNode("blendColors")

                rlegcrvinfo_fs = om1.MFnDependencyNode(rlegcrv_info)
                rlegstretchpercent_fs = om1.MFnDependencyNode(rlegstretchpercent)
                rlegstretchpow_fs = om1.MFnDependencyNode(rlegstretchpow)
                rlegstretchdiv_fs = om1.MFnDependencyNode(rlegstretchdiv)
                rlegscalediv_fs = om1.MFnDependencyNode(rlegscalediv)
                riklegstretchdiv_fs = om1.MFnDependencyNode(riklegstretchdiv)
                riklegstretchcluster1_fs = om1.MFnDependencyNode(grp_legupperikcluster1)
                riklegstretchcluster2_fs = om1.MFnDependencyNode(grp_legupperikcluster2)
                blendstretch_fs = om1.MFnDependencyNode(blendstretch)
                rlegstretchoption_fs = om1.MFnDependencyNode(obj_stretchyrightfoot)

                rlegcrvinfoarc_plug = rlegcrvinfo_fs.findPlug("arcLength")
                rlegstretchpercentinp1y_plug = rlegstretchpercent_fs.findPlug("input1Y")
                rlegstretchpercentotp_plug = rlegstretchpercent_fs.findPlug("outputY")
                rlegstretchpowinp1x_plug = rlegstretchpow_fs.findPlug("input1X")
                rlegstretchpowinp1z_plug = rlegstretchpow_fs.findPlug("input1Z")
                rlegstretchpowotpx_plug = rlegstretchpow_fs.findPlug("outputX")
                rlegstretchpowotpz_plug = rlegstretchpow_fs.findPlug("outputZ")
                rlegstretchdivinp2x_plug = rlegstretchdiv_fs.findPlug("input2X")
                rlegstretchdivinp2z_plug = rlegstretchdiv_fs.findPlug("input2Z")
                rlegstretchdivotox_plug = rlegstretchdiv_fs.findPlug("outputX")
                rlegstretchdivotpz_plug = rlegstretchdiv_fs.findPlug("outputZ")
                rlegscaledivinp1y_plug = rlegscalediv_fs.findPlug("input1Y")
                rlegscaledivinp2y_plug = rlegscalediv_fs.findPlug("input2Y")
                rlegscaledivotpy_plug = rlegscalediv_fs.findPlug("outputY")
                riklegstretchdivinp1_plug = riklegstretchdiv_fs.findPlug("input1")
                riklegstretchdivotp_plug = riklegstretchdiv_fs.findPlug("output")
                riklegstretchclust1trans_plug = riklegstretchcluster1_fs.findPlug("translate")
                riklegstretchclust2trans_plug = riklegstretchcluster2_fs.findPlug("translate")
                blendstretchinp1r_plug = blendstretch_fs.findPlug("color1R")
                blendstretchinp1g_plug = blendstretch_fs.findPlug("color1G")
                blendstretchinp1b_plug = blendstretch_fs.findPlug("color1B")
                blendstretchotpr_plug = blendstretch_fs.findPlug("outputR")
                blendstretchotpg_plug = blendstretch_fs.findPlug("outputG")
                blendstretchotpb_plug = blendstretch_fs.findPlug("outputB")
                blendstretch_plug = blendstretch_fs.findPlug("blender")
                rlegstretchoption_plug = rlegstretchoption_fs.findPlug("stretchable")

                objparent = om1.MObject()
                objchild = om1.MObject()
                for index in range(ikrupperleg_sl_lst.length()):
                    if index < ikrupperleg_sl_lst.length()-1:
                        ikrupperleg_sl_lst.getDependNode(index, objparent)
                        ikrupperleg_sl_lst.getDependNode(index+1, objchild)
                        rlegparentjnt_fs = om1.MFnDependencyNode(objparent)
                        rlegchildjnt_fs = om1.MFnDependencyNode(objchild)
                        rlegjnt_syplug = rlegparentjnt_fs.findPlug("scaleY")
                        rlegjnt_sxplug = rlegparentjnt_fs.findPlug("scaleX")
                        rlegjnt_szplug = rlegparentjnt_fs.findPlug("scaleZ")
                        rlegjnt_sotpplug = rlegparentjnt_fs.findPlug("scale")
                        rlegjnt_invsplug = rlegchildjnt_fs.findPlug("inverseScale")
                        ikspinedg_modifier.connect(rlegstretchpercentotp_plug, blendstretchinp1g_plug)
                        ikspinedg_modifier.connect(rlegstretchdivotox_plug, blendstretchinp1r_plug)
                        ikspinedg_modifier.connect(rlegstretchdivotpz_plug, blendstretchinp1b_plug)
                        ikspinedg_modifier.connect(blendstretchotpg_plug, rlegjnt_syplug)
                        ikspinedg_modifier.connect(blendstretchotpr_plug, rlegjnt_sxplug)
                        ikspinedg_modifier.connect(blendstretchotpb_plug, rlegjnt_szplug)
                        ikspinedg_modifier.connect(rlegjnt_sotpplug, rlegjnt_invsplug)

                ikspinedg_modifier.renameNode(rlegcrv_info, "RightUpperLegSpline_Info")
                ikspinedg_modifier.renameNode(rlegstretchpercent, "RightUpperLegStretch_Percent")
                ikspinedg_modifier.renameNode(rlegstretchpow, "RightUpperLegStretch_Power")
                ikspinedg_modifier.renameNode(rlegstretchdiv, "RightUpperLegStretch_Divide")
                ikspinedg_modifier.renameNode(ikspline_cv, "RightUpperLeg_SplineCvShape")
                ikspinedg_modifier.renameNode(self.rleg_ik, "RightUpperLeg_Ik")
                ikspinedg_modifier.renameNode(self.ikrleg_effector, "RightUpperLeg_effector")
                ikspinedg_modifier.renameNode(rlegscalediv, "IkRightUpperLegGlobalScale_Average")
                ikspinedg_modifier.renameNode(riklegstretchdiv, "RightUpperLegStretch_Divide2")
                ikspinedg_modifier.renameNode(blendstretch, "RighUpperLegStretch_Blend")
                ikspinedg_modifier.commandToExecute('parent "RightUpperLeg_Ik" "DoNotTouch"')
                ikspinedg_modifier.commandToExecute('connectAttr -force RightUpperLeg_SplineCvShape.worldSpace[0] RightUpperLeg_Ik.inCurve')
                ikspinedg_modifier.commandToExecute('skinCluster -bm 3 -sm 1 -dr 2.0 -name "RightUpperLegIk_skin" IkCvSplineRightUpperLeg0 IkCvSplineRightUpperLeg1 IkCvSplineRightUpperLeg2 RightUpperLeg_SplineCv')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperLeg_Ik.dTwistControlEnable" 1')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperLeg_Ik.dWorldUpType" 4')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperLeg_Ik.dForwardAxis" 3')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperLeg_Ik.dWorldUpAxis" 4')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperLeg_Ik.dWorldUpVectorY" 0')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperLeg_Ik.dWorldUpVectorEndY" 0')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperLeg_Ik.dWorldUpVectorZ" -1')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperLeg_Ik.dWorldUpVectorEndZ" -1')
                ikspinedg_modifier.commandToExecute('connectAttr -force IkCvSplineRightUpperLeg0.worldMatrix[0] RightUpperLeg_Ik.dWorldUpMatrix')
                ikspinedg_modifier.commandToExecute('connectAttr -force IkCvSplineRightUpperLeg2.worldMatrix[0] RightUpperLeg_Ik.dWorldUpMatrixEnd')
                ikspinedg_modifier.commandToExecute('connectAttr -force RightUpperLeg_SplineCvShape.worldSpace[0] RightUpperLegSpline_Info.inputCurve')
                ikspinedg_modifier.connect(rlegcrvinfoarc_plug, rlegscaledivinp1y_plug)
                ikspinedg_modifier.connect(masterctrlsy_plug, rlegscaledivinp2y_plug)
                ikspinedg_modifier.connect(rlegscaledivotpy_plug, rlegstretchpercentinp1y_plug)
                ikspinedg_modifier.connect(rlegstretchpercentotp_plug, rlegstretchpowinp1x_plug)
                ikspinedg_modifier.connect(rlegstretchpercentotp_plug, rlegstretchpowinp1z_plug)
                ikspinedg_modifier.connect(rlegstretchpowotpx_plug, rlegstretchdivinp2x_plug)
                ikspinedg_modifier.connect(rlegstretchpowotpz_plug, rlegstretchdivinp2z_plug)
                ikspinedg_modifier.connect(riklegstretchclust2trans_plug, riklegstretchdivinp1_plug)
                ikspinedg_modifier.connect(riklegstretchdivotp_plug, riklegstretchclust1trans_plug)
                ikspinedg_modifier.connect(rlegstretchoption_plug, blendstretch_plug)
                ikspinedg_modifier.commandToExecute('float $rightupperlegstretchinput1Y = `getAttr "RightUpperLegStretch_Percent.input1Y"`; setAttr "RightUpperLegStretch_Percent.input2Y" $rightupperlegstretchinput1Y')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperLegStretch_Power.input2X" 0.5')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperLegStretch_Power.input2Z" 0.5')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperLegStretch_Divide.input1X" 1')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperLegStretch_Divide.input1Z" 1')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperLegStretch_Percent.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperLegStretch_Power.operation" 3')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperLegStretch_Divide.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "IkRightUpperLegGlobalScale_Average.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperLegStretch_Divide2.operation" 2')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperLegStretch_Divide2.input2X" 2')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperLegStretch_Divide2.input2Y" 2')
                ikspinedg_modifier.commandToExecute('setAttr "RightUpperLegStretch_Divide2.input2Z" 2')
                ikspinedg_modifier.commandToExecute('setAttr "RighUpperLegStretch_Blend.color2R" 1')
                ikspinedg_modifier.commandToExecute('setAttr "RighUpperLegStretch_Blend.color2G" 1')
                ikspinedg_modifier.commandToExecute('setAttr "RighUpperLegStretch_Blend.color2B" 1')
                ikspinedg_modifier.doIt()

                ikspline_solver = self.IK_System.findSolver("ikSplineSolver")
                self.IK_Handle.setSolver(ikspline_solver)

                grp_armlowerikcluster1 = om1.MObject()
                grp_armlowerikcluster2 = om1.MObject()

                if cmds.objExists("IkSplineRightLowerLeg0"):
                    ikrlowerleg_sl_lst = om1.MSelectionList()
                    ikrlowerleg_sl_lst.add("IkSplineRightLowerLeg*")
                    ikrlowerleg_sl_lst.getDependNode(0, obj_root)
                    ikrlowerleg_sl_lst.getDependNode(ikrlowerleg_sl_lst.length()-1, obj_endspine)

                    ikrlowerleggrp_sl_lst = om1.MSelectionList()
                    ikrlowerleggrp_sl_lst.add("RightLowerLegIkCluster1_grp")
                    ikrlowerleggrp_sl_lst.add("RightLowerLegIkCluster2_grp")
                    ikrlowerleggrp_sl_lst.getDependNode(0, grp_armlowerikcluster1)
                    ikrlowerleggrp_sl_lst.getDependNode(1, grp_armlowerikcluster2)

                    rleg_pathnode = om1.MDagPath()
                    rootspine_path = rleg_pathnode.getAPathTo(obj_root)

                    try:
                        ikspineiksolver_lst.add("ikSplineSolver*")
                    except:
                        cmds.createNode("ikSplineSolver")

                    self.ikrleg_effector = self.IK_Effector.create(obj_endspine)
                    ikrleg_effector_path = rleg_pathnode.getAPathTo(self.ikrleg_effector)

                    self.rleg_ik = self.IK_Handle.create(rootspine_path, ikrleg_effector_path)

                    obj_array = om1.MPointArray()
                    obj_lst_mpoint = []
                    obj = om1.MObject()
                    for index in range(ikrlowerleg_sl_lst.length()):
                        ikrlowerleg_sl_lst.getDependNode(index, obj)
                        obj_path = self.MDag_path.getAPathTo(obj)
                        obj_tn = om1.MFnTransform(obj_path)
                        obj_t = obj_tn.translation(om1.MSpace.kWorld)
                        obj_lst_mpoint.append(om1.MPoint(obj_t))
                        obj_array.append(obj_lst_mpoint[index])

                    self.ikspline_cv_tn = ikspinedag_n.create("transform", "RightLowerLeg_SplineCv")
                    ikspline_cv = self.MNurbs1_cv.createWithEditPoints(obj_array, 1, 1, False, True, True, self.ikspline_cv_tn)
                    cmds.parent("RightLowerLeg_SplineCv", "DoNotTouch")

                    rlegcrv_info = ikspinedg_modifier.createNode("curveInfo")
                    rlegstretchpercent = ikspinedg_modifier.createNode("multiplyDivide")
                    rlegstretchpow = ikspinedg_modifier.createNode("multiplyDivide")
                    rlegstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                    rlegscalediv = ikspinedg_modifier.createNode("multiplyDivide")
                    riklegstretchdiv = ikspinedg_modifier.createNode("multiplyDivide")
                    blendstretch = ikspinedg_modifier.createNode("blendColors")

                    rlegcrvinfo_fs = om1.MFnDependencyNode(rlegcrv_info)
                    rlegstretchpercent_fs = om1.MFnDependencyNode(rlegstretchpercent)
                    rlegstretchpow_fs = om1.MFnDependencyNode(rlegstretchpow)
                    rlegstretchdiv_fs = om1.MFnDependencyNode(rlegstretchdiv)
                    rlegscalediv_fs = om1.MFnDependencyNode(rlegscalediv)
                    riklegstretchdiv_fs = om1.MFnDependencyNode(riklegstretchdiv)
                    riklegstretchcluster1_fs = om1.MFnDependencyNode(grp_armlowerikcluster1)
                    riklegstretchcluster2_fs = om1.MFnDependencyNode(grp_armlowerikcluster2)
                    blendstretch_fs = om1.MFnDependencyNode(blendstretch)

                    rlegcrvinfoarc_plug = rlegcrvinfo_fs.findPlug("arcLength")
                    rlegstretchpercentinp1y_plug = rlegstretchpercent_fs.findPlug("input1Y")
                    rlegstretchpercentotp_plug = rlegstretchpercent_fs.findPlug("outputY")
                    rlegstretchpowinp1x_plug = rlegstretchpow_fs.findPlug("input1X")
                    rlegstretchpowinp1z_plug = rlegstretchpow_fs.findPlug("input1Z")
                    rlegstretchpowotpx_plug = rlegstretchpow_fs.findPlug("outputX")
                    rlegstretchpowotpz_plug = rlegstretchpow_fs.findPlug("outputZ")
                    rlegstretchdivinp2x_plug = rlegstretchdiv_fs.findPlug("input2X")
                    rlegstretchdivinp2z_plug = rlegstretchdiv_fs.findPlug("input2Z")
                    rlegstretchdivotox_plug = rlegstretchdiv_fs.findPlug("outputX")
                    rlegstretchdivotpz_plug = rlegstretchdiv_fs.findPlug("outputZ")
                    rlegscaledivinp1y_plug = rlegscalediv_fs.findPlug("input1Y")
                    rlegscaledivinp2y_plug = rlegscalediv_fs.findPlug("input2Y")
                    rlegscaledivotpy_plug = rlegscalediv_fs.findPlug("outputY")
                    riklegstretchdivinp1_plug = riklegstretchdiv_fs.findPlug("input1")
                    riklegstretchdivotp_plug = riklegstretchdiv_fs.findPlug("output")
                    riklegstretchclust1trans_plug = riklegstretchcluster1_fs.findPlug("translate")
                    riklegstretchclust2trans_plug = riklegstretchcluster2_fs.findPlug("translate")
                    blendstretchinp1r_plug = blendstretch_fs.findPlug("color1R")
                    blendstretchinp1g_plug = blendstretch_fs.findPlug("color1G")
                    blendstretchinp1b_plug = blendstretch_fs.findPlug("color1B")
                    blendstretchotpr_plug = blendstretch_fs.findPlug("outputR")
                    blendstretchotpg_plug = blendstretch_fs.findPlug("outputG")
                    blendstretchotpb_plug = blendstretch_fs.findPlug("outputB")
                    blendstretch_plug = blendstretch_fs.findPlug("blender")

                    objparent = om1.MObject()
                    objchild = om1.MObject()
                    for index in range(ikrlowerleg_sl_lst.length()):
                        if index < ikrlowerleg_sl_lst.length()-1:
                            ikrlowerleg_sl_lst.getDependNode(index, objparent)
                            ikrlowerleg_sl_lst.getDependNode(index+1, objchild)
                            rlegparentjnt_fs = om1.MFnDependencyNode(objparent)
                            rlegchildjnt_fs = om1.MFnDependencyNode(objchild)
                            rlegjnt_syplug = rlegparentjnt_fs.findPlug("scaleY")
                            rlegjnt_sxplug = rlegparentjnt_fs.findPlug("scaleX")
                            rlegjnt_szplug = rlegparentjnt_fs.findPlug("scaleZ")
                            rlegjnt_sotpplug = rlegparentjnt_fs.findPlug("scale")
                            rlegjnt_invsplug = rlegchildjnt_fs.findPlug("inverseScale")
                            ikspinedg_modifier.connect(rlegstretchpercentotp_plug, blendstretchinp1g_plug)
                            ikspinedg_modifier.connect(rlegstretchdivotox_plug, blendstretchinp1r_plug)
                            ikspinedg_modifier.connect(rlegstretchdivotpz_plug, blendstretchinp1b_plug)
                            ikspinedg_modifier.connect(blendstretchotpg_plug, rlegjnt_syplug)
                            ikspinedg_modifier.connect(blendstretchotpr_plug, rlegjnt_sxplug)
                            ikspinedg_modifier.connect(blendstretchotpb_plug, rlegjnt_szplug)
                            ikspinedg_modifier.connect(rlegjnt_sotpplug, rlegjnt_invsplug)

                    ikspinedg_modifier.renameNode(rlegcrv_info, "RightLowerLegSpline_Info")
                    ikspinedg_modifier.renameNode(rlegstretchpercent, "RightLowerLegStretch_Percent")
                    ikspinedg_modifier.renameNode(rlegstretchpow, "RightLowerLegStretch_Power")
                    ikspinedg_modifier.renameNode(rlegstretchdiv, "RightLowerLegStretch_Divide")
                    ikspinedg_modifier.renameNode(ikspline_cv, "RightLowerLeg_SplineCvShape")
                    ikspinedg_modifier.renameNode(self.rleg_ik, "RightLowerLeg_Ik")
                    ikspinedg_modifier.renameNode(self.ikrleg_effector, "RightLowerLeg_effector")
                    ikspinedg_modifier.renameNode(rlegscalediv, "IkRightLowerLegGlobalScale_Average")
                    ikspinedg_modifier.renameNode(riklegstretchdiv, "RightLowerLegStretch_Divide2")
                    ikspinedg_modifier.renameNode(blendstretch, "RightLowerLegStretch_Blend")
                    ikspinedg_modifier.commandToExecute('parent "RightLowerLeg_Ik" "DoNotTouch"')
                    ikspinedg_modifier.commandToExecute('connectAttr -f RightLowerLeg_SplineCvShape.worldSpace[0] RightLowerLeg_Ik.inCurve')
                    ikspinedg_modifier.commandToExecute('skinCluster -bm 3 -sm 1 -dr 2.0 -name "RightLowerLegIk_skin" IkCvSplineRightLowerLeg0 IkCvSplineRightLowerLeg1 IkCvSplineRightLowerLeg2 RightLowerLeg_SplineCv')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLeg_Ik.dTwistControlEnable" 1')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLeg_Ik.dWorldUpType" 4')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLeg_Ik.dForwardAxis" 3')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLeg_Ik.dWorldUpAxis" 4')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLeg_Ik.dWorldUpVectorY" 0')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLeg_Ik.dWorldUpVectorEndY" 0')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLeg_Ik.dWorldUpVectorZ" -1')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLeg_Ik.dWorldUpVectorEndZ" -1')
                    ikspinedg_modifier.commandToExecute('connectAttr -f IkCvSplineRightLowerLeg0.worldMatrix[0] RightLowerLeg_Ik.dWorldUpMatrix')
                    ikspinedg_modifier.commandToExecute('connectAttr -f IkCvSplineRightLowerLeg2.worldMatrix[0] RightLowerLeg_Ik.dWorldUpMatrixEnd')
                    ikspinedg_modifier.commandToExecute('connectAttr -f RightLowerLeg_SplineCvShape.worldSpace[0] RightLowerLegSpline_Info.inputCurve')
                    ikspinedg_modifier.connect(rlegcrvinfoarc_plug, rlegscaledivinp1y_plug)
                    ikspinedg_modifier.connect(masterctrlsy_plug, rlegscaledivinp2y_plug)
                    ikspinedg_modifier.connect(rlegscaledivotpy_plug, rlegstretchpercentinp1y_plug)
                    ikspinedg_modifier.connect(rlegstretchpercentotp_plug, rlegstretchpowinp1x_plug)
                    ikspinedg_modifier.connect(rlegstretchpercentotp_plug, rlegstretchpowinp1z_plug)
                    ikspinedg_modifier.connect(rlegstretchpowotpx_plug, rlegstretchdivinp2x_plug)
                    ikspinedg_modifier.connect(rlegstretchpowotpz_plug, rlegstretchdivinp2z_plug)
                    ikspinedg_modifier.connect(riklegstretchclust2trans_plug, riklegstretchdivinp1_plug)
                    ikspinedg_modifier.connect(riklegstretchdivotp_plug, riklegstretchclust1trans_plug)
                    ikspinedg_modifier.connect(rlegstretchoption_plug, blendstretch_plug)
                    ikspinedg_modifier.commandToExecute('float $rightlowerlegstretchinput1Y = `getAttr "RightLowerLegStretch_Percent.input1Y"`; setAttr "RightLowerLegStretch_Percent.input2Y" $rightlowerlegstretchinput1Y')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLegStretch_Power.input2X" 0.5')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLegStretch_Power.input2Z" 0.5')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLegStretch_Divide.input1X" 1')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLegStretch_Divide.input1Z" 1')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLegStretch_Percent.operation" 2')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLegStretch_Power.operation" 3')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLegStretch_Divide.operation" 2')
                    ikspinedg_modifier.commandToExecute('setAttr "IkRightLowerLegGlobalScale_Average.operation" 2')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLegStretch_Divide2.operation" 2')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLegStretch_Divide2.input2X" 2')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLegStretch_Divide2.input2Y" 2')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLegStretch_Divide2.input2Z" 2')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLegStretch_Blend.color2R" 1')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLegStretch_Blend.color2G" 1')
                    ikspinedg_modifier.commandToExecute('setAttr "RightLowerLegStretch_Blend.color2B" 1')
                    ikspinedg_modifier.doIt()

                    ikspline_solver = self.IK_System.findSolver("ikSplineSolver")
                    self.IK_Handle.setSolver(ikspline_solver)

        if cmds.objExists("NoFlipRightLeg_Ik") and cmds.objExists("PVRightLeg_Ik"):

            self.MDG2_mod.commandToExecute('addAttr -longName "follow" -niceName "Follow Body" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_IkRightFoot_ctrl')
            self.MDG2_mod.commandToExecute('parentConstraint -mo -weight 1 Biped_Root_ctrl Biped_IkRightFootRot_null')
            self.MDG2_mod.doIt()

            rlegik_sl_ls = om2.MSelectionList()
            rlegik_sl_ls.add("RightLegIk_grp")
            rlegik_sl_ls.add("Biped_NoFlipRightKnee_null")
            rlegik_sl_ls.add("Biped_IkRightFoot_ctrl")
            rlegik_sl_ls.add("IkRightJointLeg_grp")
            rlegik_sl_ls.add("IkStretchyRightJointLeg_grp")
            rikleggrpobj_fs = om2.MFnDependencyNode(rlegik_sl_ls.getDependNode(0))
            nofliprightkneenullobj_fs = om2.MFnDependencyNode(rlegik_sl_ls.getDependNode(1))
            iklegctrl_fs = om2.MFnDependencyNode(rlegik_sl_ls.getDependNode(2))
            ikrightjointleggrp_fs = om2.MFnDependencyNode(rlegik_sl_ls.getDependNode(3))

            if self.typeofRLegIK.currentIndex() == 1 or 2:
                riklegctrl_multMatrix = self.MDG2_mod.createNode("multMatrix")
                riklegctrl_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                self.MDG2_mod.renameNode(riklegctrl_multMatrix, "IkRightLegCtrl_multMatrix")
                self.MDG2_mod.renameNode(riklegctrl_decomposeMatrix, "IkRightLegCtrl_decomposeMatrix")

                riklegmultMatrix_fs = om2.MFnDependencyNode(riklegctrl_multMatrix)
                riklegdecomposeMatrix_fs = om2.MFnDependencyNode(riklegctrl_decomposeMatrix)

                riklegmultMatrixSum_plug = riklegmultMatrix_fs.findPlug("matrixSum", False)
                riklegdecomposeInpMatrix_plug = riklegdecomposeMatrix_fs.findPlug("inputMatrix", False)
                riklegdecomposeOtpTrans_plug = riklegdecomposeMatrix_fs.findPlug("outputTranslate", False)
                rikleggrpTrans_plug = rikleggrpobj_fs.findPlug("translate", False)
                riklegdecomposeOtpRot_plug = riklegdecomposeMatrix_fs.findPlug("outputRotate", False)
                rikleggrpRot_plug = rikleggrpobj_fs.findPlug("rotate", False)
                iklegctrlTrans_plug = iklegctrl_fs.findPlug("translate", False)
                nofliprightkneenullTrans_plug = nofliprightkneenullobj_fs.findPlug("translate", False)
                iklegctrlRot_plug = iklegctrl_fs.findPlug("rotate", False)
                nofliprightkneenullRot_plug = nofliprightkneenullobj_fs.findPlug("rotate", False)
                riklegjntScal_plug = rikleggrpobj_fs.findPlug("scale", False)

                self.MDG2_mod.commandToExecute('connectAttr -force Biped_IkRightFoot_ctrl.worldMatrix[0] IkRightLegCtrl_multMatrix.matrixIn[0]')
                self.MDG2_mod.commandToExecute('parent RightReverseFootHeel RightLegIk_grp')
                self.MDG2_mod.commandToExecute('poleVectorConstraint Biped_NoFlipRightKnee_ctrl NoFlipRightLeg_Ik')
                self.MDG2_mod.commandToExecute('poleVectorConstraint Biped_PVRightKnee_ctrl PVRightLeg_Ik')
                self.MDG2_mod.commandToExecute('setAttr "NoFlipRightLeg_Ik.twist" 90')
                self.MDG2_mod.commandToExecute('connectAttr -force Biped_IkRightFoot_ctrl.follow Biped_IkRightFootRot_null_parentConstraint1.Biped_Root_ctrlW0')
                self.MDG2_mod.connect(riklegmultMatrixSum_plug, riklegdecomposeInpMatrix_plug)
                self.MDG2_mod.connect(riklegdecomposeOtpTrans_plug, rikleggrpTrans_plug)
                self.MDG2_mod.connect(riklegdecomposeOtpRot_plug, rikleggrpRot_plug)
                self.MDG2_mod.connect(iklegctrlTrans_plug, nofliprightkneenullTrans_plug)
                self.MDG2_mod.connect(iklegctrlRot_plug, nofliprightkneenullRot_plug)
                self.MDG2_mod.connect(masterdecomposeOtpScale_plug, riklegjntScal_plug)

                stretchy_sl_lst2.add("Biped_RightFootOptions_ctrl")
                obj_stretchyrightleg2 = stretchy_sl_lst2.getDependNode(3)

                if self.autostretch.currentIndex() == 1:
                    riklegdistloc = om2.MFnDagNode()

                    rikupperlegdistloc1_tn = riklegdistloc.create("transform", "distloc_R_upleg1", rlegik_sl_ls.getDependNode(4))
                    rikupperlegdistloc_ln = riklegdistloc.create("locator", "R_upleg1_Shape", rikupperlegdistloc1_tn)
                    rikfootlegdistloc1_tn = riklegdistloc.create("transform", "distloc_R_legfoot1")
                    rikfootlegdistloc_ln = riklegdistloc.create("locator", "R_foot1_Shape", rikfootlegdistloc1_tn)
                    self.MDG2_mod.commandToExecute('createNode "distanceDimShape"')
                    self.MDG2_mod.commandToExecute('rename "distanceDimension1" "IkRightLegDistance_Info"')
                    self.MDG2_mod.doIt()

                    ruplegnull_transform_t = ruplegnull_transform.translation(om2.MSpace.kTransform)
                    rikupperlegdistloc_transform = om2.MFnTransform(rikupperlegdistloc1_tn)
                    rikupperlegdistloc_transform.setTranslation(ruplegnull_transform_t, om2.MSpace.kTransform)

                    IkRightLegDistance_sl_ls = om2.MSelectionList()
                    IkRightLegDistance_sl_ls.add("IkRightLegDistance_InfoShape")

                    rikfootlegDist_fs = om2.MFnDependencyNode(rikfootlegdistloc1_tn)
                    riklegjntDist_fs = om2.MFnDependencyNode(IkRightLegDistance_sl_ls.getDependNode(0))

                    riklegjntDistPoint2_plug = riklegjntDist_fs.findPlug("endPoint", False)
                    rikfootlegDistOtpTrans_plug = rikfootlegDist_fs.findPlug("translate", False)

                    self.MDG2_mod.commandToExecute('connectAttr -force R_upleg1_Shape.worldPosition[0] IkRightLegDistance_InfoShape.startPoint')
                    self.MDG2_mod.connect(rikfootlegDistOtpTrans_plug, riklegjntDistPoint2_plug)
                    self.MDG2_mod.connect(riklegdecomposeOtpTrans_plug, rikfootlegDistOtpTrans_plug)
                    self.MDG2_mod.commandToExecute('float $noflipikrightlegtranslateY = `getAttr "IkNoFlipRightLeg.translateY"`; float $noflipikrightfoottranslateY = `getAttr "IkNoFlipRightFoot.translateY"`; float $totalnoflipikrightlegtranslateY = $noflipikrightlegtranslateY + $noflipikrightfoottranslateY; setDrivenKeyframe -currentDriver IkRightLegDistance_InfoShape.distance -driverValue $totalnoflipikrightlegtranslateY -attribute "translateY" -value $noflipikrightlegtranslateY IkNoFlipRightLeg;')
                    self.MDG2_mod.commandToExecute('float $noflipikrightlegtranslateY = `getAttr "IkNoFlipRightLeg.translateY"`; float $noflipikrightfoottranslateY = `getAttr "IkNoFlipRightFoot.translateY"`; float $totalnoflipikrightlegtranslateY = $noflipikrightlegtranslateY + $noflipikrightfoottranslateY; setDrivenKeyframe -currentDriver IkRightLegDistance_InfoShape.distance -driverValue ($totalnoflipikrightlegtranslateY*2) -attribute "translateY" -value ($noflipikrightlegtranslateY*2) IkNoFlipRightLeg;')
                    self.MDG2_mod.commandToExecute('float $noflipikrightlegtranslateY = `getAttr "IkNoFlipRightLeg.translateY"`; float $noflipikrightfoottranslateY = `getAttr "IkNoFlipRightFoot.translateY"`; float $totalnoflipikrightlegtranslateY = $noflipikrightlegtranslateY + $noflipikrightfoottranslateY; setDrivenKeyframe -currentDriver IkRightLegDistance_InfoShape.distance -driverValue $totalnoflipikrightlegtranslateY -attribute "translateY" -value $noflipikrightfoottranslateY IkNoFlipRightFoot;')
                    self.MDG2_mod.commandToExecute('float $noflipikrightlegtranslateY = `getAttr "IkNoFlipRightLeg.translateY"`; float $noflipikrightfoottranslateY = `getAttr "IkNoFlipRightFoot.translateY"`; float $totalnoflipikrightlegtranslateY = $noflipikrightlegtranslateY + $noflipikrightfoottranslateY; setDrivenKeyframe -currentDriver IkRightLegDistance_InfoShape.distance -driverValue ($totalnoflipikrightlegtranslateY*2) -attribute "translateY" -value ($noflipikrightfoottranslateY*2) IkNoFlipRightFoot;')
                    self.MDG2_mod.commandToExecute('float $pvikrightlegtranslateY = `getAttr "IkPVRightLeg.translateY"`; float $pvikrightfoottranslateY = `getAttr "IkPVRightFoot.translateY"`; float $totalpvikrightlegtranslateY = $pvikrightlegtranslateY + $pvikrightfoottranslateY; setDrivenKeyframe -currentDriver IkRightLegDistance_InfoShape.distance -driverValue $totalpvikrightlegtranslateY -attribute "translateY" -value $pvikrightlegtranslateY IkPVRightLeg;')
                    self.MDG2_mod.commandToExecute('float $pvikrightlegtranslateY = `getAttr "IkPVRightLeg.translateY"`; float $pvikrightfoottranslateY = `getAttr "IkPVRightFoot.translateY"`; float $totalpvikrightlegtranslateY = $pvikrightlegtranslateY + $pvikrightfoottranslateY; setDrivenKeyframe -currentDriver IkRightLegDistance_InfoShape.distance -driverValue ($totalpvikrightlegtranslateY*2) -attribute "translateY" -value ($pvikrightlegtranslateY*2) IkPVRightLeg;')
                    self.MDG2_mod.commandToExecute('float $pvikrightlegtranslateY = `getAttr "IkPVRightLeg.translateY"`; float $pvikrightfoottranslateY = `getAttr "IkPVRightFoot.translateY"`; float $totalpvikrightlegtranslateY = $pvikrightlegtranslateY + $pvikrightfoottranslateY; setDrivenKeyframe -currentDriver IkRightLegDistance_InfoShape.distance -driverValue $totalpvikrightlegtranslateY -attribute "translateY" -value $pvikrightfoottranslateY IkPVRightFoot;')
                    self.MDG2_mod.commandToExecute('float $pvikrightlegtranslateY = `getAttr "IkPVRightLeg.translateY"`; float $pvikrightfoottranslateY = `getAttr "IkPVRightFoot.translateY"`; float $totalpvikrightlegtranslateY = $pvikrightlegtranslateY + $pvikrightfoottranslateY; setDrivenKeyframe -currentDriver IkRightLegDistance_InfoShape.distance -driverValue ($totalpvikrightlegtranslateY*2) -attribute "translateY" -value ($pvikrightfoottranslateY*2) IkPVRightFoot;')
                    self.MDG2_mod.commandToExecute('selectKey -attribute translateY IkNoFlipRightLeg; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative')
                    self.MDG2_mod.commandToExecute('selectKey -attribute translateY IkPVRightLeg; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative')
                    self.MDG2_mod.commandToExecute('selectKey -attribute translateY IkNoFlipRightFoot; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative')
                    self.MDG2_mod.commandToExecute('selectKey -attribute translateY IkPVRightFoot; keyTangent -inTangentType linear -outTangentType linear; setInfinity -postInfinite cycleRelative')
                    self.MDG2_mod.commandToExecute('parent "IkRightLegDistance_Info" "DoNotTouch"')
                    self.MDG2_mod.commandToExecute('parent "distloc_R_legfoot1" "DoNotTouch"')

                    self.MDG2_mod.commandToExecute('addAttr -longName "kneesnap" -niceName "Knee Snap" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_PVRightKnee_ctrl')

                    rikupperlegdistloc2_tn = riklegdistloc.create("transform", "distloc_R_upleg2", rlegik_sl_ls.getDependNode(4))
                    rikupperlegdistloc_ln = riklegdistloc.create("locator", "R_upleg2_Shape", rikupperlegdistloc2_tn)
                    rikkneedistloc_tn = riklegdistloc.create("transform", "distloc_R_legknee")
                    rikkneedistloc_ln = riklegdistloc.create("locator", "R_legknee_Shape", rikkneedistloc_tn)
                    rikfootlegdistloc2_tn = riklegdistloc.create("transform", "distloc_R_legfoot2")
                    rikfootlegdistloc_ln = riklegdistloc.create("locator", "R_legfoot2_Shape", rikfootlegdistloc2_tn)
                    pvrightkneectrl_decomposeMatrix = self.MDG2_mod.createNode("decomposeMatrix")
                    rikpvuppertransblendnode = self.MDG2_mod.createNode("blendColors")
                    rikpvlowertransblendnode = self.MDG2_mod.createNode("blendColors")
                    rikpvupperlegstretchblendnode = self.MDG2_mod.createNode("blendColors")
                    rikpvlowerlegstretchblendnode = self.MDG2_mod.createNode("blendColors")
                    self.MDG2_mod.commandToExecute('createNode "distanceDimShape"')
                    self.MDG2_mod.commandToExecute('createNode "distanceDimShape"')
                    self.MDG2_mod.renameNode(pvrightkneectrl_decomposeMatrix, "PVRightKnee_decomposeMatrix")
                    self.MDG2_mod.renameNode(rikpvuppertransblendnode, "PVRightUpperLegTrans_blend")
                    self.MDG2_mod.renameNode(rikpvlowertransblendnode, "PVRightLowerLegTrans_blend")
                    self.MDG2_mod.renameNode(rikpvupperlegstretchblendnode, "PVRightUpperLegStretch_blend")
                    self.MDG2_mod.renameNode(rikpvlowerlegstretchblendnode, "PVRightLowerLegStretch_blend")
                    self.MDG2_mod.commandToExecute('rename "distanceDimension1" "RightUpperLegDistance_Info"')
                    self.MDG2_mod.commandToExecute('rename "distanceDimension2" "RightLowerLegDistance_Info"')
                    self.MDG2_mod.doIt()

                    rikupperlegdistloc2_transform = om2.MFnTransform(rikupperlegdistloc2_tn)
                    rikupperlegdistloc2_transform.setTranslation(ruplegnull_transform_t, om2.MSpace.kTransform)

                    IkRightLegDistance_sl_ls.add("RightUpperLegDistance_InfoShape")
                    IkRightLegDistance_sl_ls.add("RightLowerLegDistance_InfoShape")
                    IkRightLegDistance_sl_ls.add("IkPVRightLeg_translateY")
                    IkRightLegDistance_sl_ls.add("IkPVRightFoot_translateY")
                    IkRightLegDistance_sl_ls.add("Biped_PVRightKnee_ctrl")
                    IkRightLegDistance_sl_ls.add("IkNoFlipRightLeg_translateY")
                    IkRightLegDistance_sl_ls.add("IkNoFlipRightFoot_translateY")

                    rikkneeDist_fs = om2.MFnDependencyNode(rikkneedistloc_tn)
                    rikfootlegDist_fs = om2.MFnDependencyNode(rikfootlegdistloc2_tn)
                    rikupperlegjntDist_fs = om2.MFnDependencyNode(IkRightLegDistance_sl_ls.getDependNode(1))
                    riklowerlegjntDist_fs = om2.MFnDependencyNode(IkRightLegDistance_sl_ls.getDependNode(2))
                    pvrightkneekey_fs = om2.MFnDependencyNode(IkRightLegDistance_sl_ls.getDependNode(3))
                    pvrightfootkey_fs = om2.MFnDependencyNode(IkRightLegDistance_sl_ls.getDependNode(4))
                    pvrightkneectrlDecomposeMatrix_fs = om2.MFnDependencyNode(pvrightkneectrl_decomposeMatrix)
                    rikpvuppertransblendnode_fs = om2.MFnDependencyNode(rikpvuppertransblendnode)
                    rikpvlowertransblendnode_fs = om2.MFnDependencyNode(rikpvlowertransblendnode)
                    pvrightkneectrl_fs = om2.MFnDependencyNode(IkRightLegDistance_sl_ls.getDependNode(5))
                    pvrightkneejnt_fs = om2.MFnDependencyNode(pvikrleg_sl_ls.getDependNode(1))
                    pvrightfootjnt_fs = om2.MFnDependencyNode(pvikrleg_sl_ls.getDependNode(2))
                    rikupperlegstretchblendnode_fs = om2.MFnDependencyNode(rikpvupperlegstretchblendnode)
                    riklowerlegstretchblendnode_fs = om2.MFnDependencyNode(rikpvlowerlegstretchblendnode)
                    rightlegoption_fs = om2.MFnDependencyNode(obj_stretchyrightleg2)

                    rikupperlegjntDistPoint2_plug = rikupperlegjntDist_fs.findPlug("endPoint", False)
                    riklowerlegjntDistPoint1_plug = riklowerlegjntDist_fs.findPlug("startPoint", False)
                    riklowerlegjntDistPoint2_plug = riklowerlegjntDist_fs.findPlug("endPoint", False)
                    rikkneeDistOtpTrans_plug = rikkneeDist_fs.findPlug("translate", False)
                    rikfootlegDistOtpTrans_plug = rikfootlegDist_fs.findPlug("translate", False)
                    pvrightkneectrlDecomposeMatrixOtpTrans_plug = pvrightkneectrlDecomposeMatrix_fs.findPlug("outputTranslate", False)
                    pvrightkneekeyotp_plug = pvrightkneekey_fs.findPlug("output", False)
                    pvrightfootkeyotp_plug = pvrightfootkey_fs.findPlug("output", False)
                    rikpvuppertransblendnodeinp1g_plug = rikpvuppertransblendnode_fs.findPlug("color1G", False)
                    rikpvuppertransblendnodeinp2g_plug = rikpvuppertransblendnode_fs.findPlug("color2G", False)
                    rikpvuppertransblendnodeotp_plug = rikpvuppertransblendnode_fs.findPlug("outputG", False)
                    rikpvuppertransblendnodeblender_plug = rikpvuppertransblendnode_fs.findPlug("blender", False)
                    rikpvlowertransblendnodeinp1g_plug = rikpvlowertransblendnode_fs.findPlug("color1G", False)
                    rikpvlowertransblendnodeinp2g_plug = rikpvlowertransblendnode_fs.findPlug("color2G", False)
                    rikpvlowertransblendnodeotp_plug = rikpvlowertransblendnode_fs.findPlug("outputG", False)
                    rikpvlowertransblendnodeblender_plug = rikpvlowertransblendnode_fs.findPlug("blender", False)
                    pvrightkneectrl_fs_plug = pvrightkneectrl_fs.findPlug("kneesnap", False)
                    rikpvupperlegstretchblendnodeinp1g_plug = rikupperlegstretchblendnode_fs.findPlug("color1G", False)
                    rikpvupperlegstretchblendnodeotp_plug = rikupperlegstretchblendnode_fs.findPlug("outputG", False)
                    rikpvupperlegstretchblendnodeblender_plug = rikupperlegstretchblendnode_fs.findPlug("blender", False)
                    rikpvlowerlegstretchblendnodeinp1g_plug = riklowerlegstretchblendnode_fs.findPlug("color1G", False)
                    rikpvlowerlegstretchblendnodeotp_plug = riklowerlegstretchblendnode_fs.findPlug("outputG", False)
                    rikpvlowerlegstretchblendnodeblender_plug = riklowerlegstretchblendnode_fs.findPlug("blender", False)
                    ikrightlegstretch_plug = rightlegoption_fs.findPlug("stretchable", False)
                    pvrightkneejntTrans_plug = pvrightkneejnt_fs.findPlug("translateY", False)
                    pvrightfootjntTrans_plug = pvrightfootjnt_fs.findPlug("translateY", False)

                    self.MDG2_mod.commandToExecute('connectAttr -force R_upleg2_Shape.worldPosition[0] RightUpperLegDistance_InfoShape.startPoint')
                    self.MDG2_mod.commandToExecute('connectAttr -force Biped_PVRightKnee_ctrl.worldMatrix[0] PVRightKnee_decomposeMatrix.inputMatrix')
                    self.MDG2_mod.connect(rikkneeDistOtpTrans_plug, rikupperlegjntDistPoint2_plug)
                    self.MDG2_mod.connect(rikkneeDistOtpTrans_plug, riklowerlegjntDistPoint1_plug)
                    self.MDG2_mod.connect(rikfootlegDistOtpTrans_plug, riklowerlegjntDistPoint2_plug)
                    self.MDG2_mod.connect(riklegdecomposeOtpTrans_plug, rikfootlegDistOtpTrans_plug)
                    self.MDG2_mod.connect(pvrightkneectrlDecomposeMatrixOtpTrans_plug, rikkneeDistOtpTrans_plug)

                    self.MDG2_mod.disconnect(pvrightkneekeyotp_plug, pvrightkneejntTrans_plug)
                    self.MDG2_mod.disconnect(pvrightfootkeyotp_plug, pvrightfootjntTrans_plug)
                    self.MDG2_mod.connect(pvrightkneekeyotp_plug, rikpvuppertransblendnodeinp2g_plug)
                    self.MDG2_mod.connect(pvrightfootkeyotp_plug, rikpvlowertransblendnodeinp2g_plug)
                    self.MDG2_mod.connect(pvrightkneectrl_fs_plug, rikpvuppertransblendnodeblender_plug)
                    self.MDG2_mod.connect(pvrightkneectrl_fs_plug, rikpvlowertransblendnodeblender_plug)
                    self.MDG2_mod.connect(rikpvuppertransblendnodeotp_plug, rikpvupperlegstretchblendnodeinp1g_plug)
                    self.MDG2_mod.connect(rikpvlowertransblendnodeotp_plug, rikpvlowerlegstretchblendnodeinp1g_plug)
                    self.MDG2_mod.connect(rikpvupperlegstretchblendnodeotp_plug, pvrightkneejntTrans_plug)
                    self.MDG2_mod.connect(rikpvlowerlegstretchblendnodeotp_plug, pvrightfootjntTrans_plug)
                    self.MDG2_mod.connect(ikrightlegstretch_plug, rikpvupperlegstretchblendnodeblender_plug)
                    self.MDG2_mod.connect(ikrightlegstretch_plug, rikpvlowerlegstretchblendnodeblender_plug)
                    self.MDG2_mod.commandToExecute('float $pvikrightlegtranslateY = `getAttr "PVRightUpperLegStretch_blend.color1G"`; setAttr "PVRightUpperLegStretch_blend.color2G" $pvikrightlegtranslateY;')
                    self.MDG2_mod.commandToExecute('float $pvikrightfoottranslateY = `getAttr "PVRightLowerLegStretch_blend.color1G"`; setAttr "PVRightLowerLegStretch_blend.color2G" $pvikrightfoottranslateY;')
                    self.MDG2_mod.commandToExecute('parent "distloc_R_legknee" "DoNotTouch"')
                    self.MDG2_mod.commandToExecute('parent "distloc_R_legfoot2" "DoNotTouch"')
                    self.MDG2_mod.commandToExecute('parent "RightUpperLegDistance_Info" "DoNotTouch"')
                    self.MDG2_mod.commandToExecute('parent "RightLowerLegDistance_Info" "DoNotTouch"')

                    self.MDG2_mod.commandToExecute('addAttr -longName "thighlength" -niceName "AutoKnee Thigh Length" -attributeType double -minValue 0 -keyable true -defaultValue 1 Biped_IkRightFoot_ctrl')
                    self.MDG2_mod.commandToExecute('addAttr -longName "calflength" -niceName "AutoKnee Calf Length" -attributeType double -minValue 0 -keyable true -defaultValue 1 Biped_IkRightFoot_ctrl')
                    self.MDG2_mod.doIt()

                    rikautokneeupperlegnode = self.MDG2_mod.createNode("multiplyDivide")
                    rikautokneelowerlegnode = self.MDG2_mod.createNode("multiplyDivide")
                    riknoflipupperlegtransblendnode = self.MDG2_mod.createNode("blendColors")
                    riknofliplowerlegtransblendnode = self.MDG2_mod.createNode("blendColors")
                    self.MDG2_mod.renameNode(rikautokneeupperlegnode, "NoFlipRightLegTrans_multiply")
                    self.MDG2_mod.renameNode(rikautokneelowerlegnode, "NoFlipRightFootTrans_multiply")
                    self.MDG2_mod.renameNode(riknoflipupperlegtransblendnode, "NoFlipRightUpperLegStretch_blend")
                    self.MDG2_mod.renameNode(riknofliplowerlegtransblendnode, "NoFlipRightLowerLegStretch_blend")

                    rikautokneeupperleg_fs = om2.MFnDependencyNode(rikautokneeupperlegnode)
                    rikautokneelowerleg_fs = om2.MFnDependencyNode(rikautokneelowerlegnode)
                    nofliprightkneekey_fs = om2.MFnDependencyNode(IkRightLegDistance_sl_ls.getDependNode(6))
                    nofliprightfootkey_fs = om2.MFnDependencyNode(IkRightLegDistance_sl_ls.getDependNode(7))
                    nofliprightkneejntTrans_fs = om2.MFnDependencyNode(noflipikrleg_sl_ls.getDependNode(1))
                    nofliprightfootjntTrans_fs = om2.MFnDependencyNode(noflipikrleg_sl_ls.getDependNode(2))
                    riknoflipupperlegstretchblendnode_fs = om2.MFnDependencyNode(riknoflipupperlegtransblendnode)
                    riknofliplowerlegstretchblendnode_fs = om2.MFnDependencyNode(riknofliplowerlegtransblendnode)

                    ikautoelbowupperarmInp1Y_plug = rikautokneeupperleg_fs.findPlug("input1Y", False)
                    ikautoelbowupperarmInp2Y_plug = rikautokneeupperleg_fs.findPlug("input2Y", False)
                    likautoelbowupperarmOtp_plug = rikautokneeupperleg_fs.findPlug("outputY", False)
                    ikautoelbowlowerarmInp1Y_plug = rikautokneelowerleg_fs.findPlug("input1Y", False)
                    ikautoelbowlowerarmInp2Y_plug = rikautokneelowerleg_fs.findPlug("input2Y", False)
                    likautoelbowlowerarmOtp_plug = rikautokneelowerleg_fs.findPlug("outputY", False)
                    nofliprightkneekeyotp_plug = nofliprightkneekey_fs.findPlug("output", False)
                    nofliprightfootkeyotp_plug = nofliprightfootkey_fs.findPlug("output", False)
                    nofliprightkneejnttty_plug = nofliprightkneejntTrans_fs.findPlug("translateY", False)
                    nofliprightfootjntty_plug = nofliprightfootjntTrans_fs.findPlug("translateY", False)
                    iklegctrrkneeupperleg_plug = iklegctrl_fs.findPlug("thighlength", False)
                    iklegctrrkneelowerleg_plug = iklegctrl_fs.findPlug("calflength", False)
                    riknoflipupperlegstretchblendnodeinp1g_plug = riknoflipupperlegstretchblendnode_fs.findPlug("color1G", False)
                    riknoflipupperlegstretchblendnodeotp_plug = riknoflipupperlegstretchblendnode_fs.findPlug("outputG", False)
                    riknoflipupperlegstretchblendnodeblender_plug = riknoflipupperlegstretchblendnode_fs.findPlug("blender", False)
                    riknofliplowerlegstretchblendnodeinp1g_plug = riknofliplowerlegstretchblendnode_fs.findPlug("color1G", False)
                    riknofliplowerlegstretchblendnodeotp_plug = riknofliplowerlegstretchblendnode_fs.findPlug("outputG", False)
                    riknofliplowerlegstretchblendnodeblender_plug = riknofliplowerlegstretchblendnode_fs.findPlug("blender", False)

                    self.MDG2_mod.disconnect(nofliprightkneekeyotp_plug, nofliprightkneejnttty_plug)
                    self.MDG2_mod.disconnect(nofliprightfootkeyotp_plug, nofliprightfootjntty_plug)
                    self.MDG2_mod.connect(iklegctrrkneeupperleg_plug, ikautoelbowupperarmInp1Y_plug)
                    self.MDG2_mod.connect(nofliprightkneekeyotp_plug, ikautoelbowupperarmInp2Y_plug)
                    self.MDG2_mod.connect(iklegctrrkneelowerleg_plug, ikautoelbowlowerarmInp1Y_plug)
                    self.MDG2_mod.connect(nofliprightfootkeyotp_plug, ikautoelbowlowerarmInp2Y_plug)
                    self.MDG2_mod.connect(likautoelbowupperarmOtp_plug, riknoflipupperlegstretchblendnodeinp1g_plug)
                    self.MDG2_mod.connect(likautoelbowlowerarmOtp_plug, riknofliplowerlegstretchblendnodeinp1g_plug)
                    self.MDG2_mod.connect(riknoflipupperlegstretchblendnodeotp_plug, nofliprightkneejnttty_plug)
                    self.MDG2_mod.connect(riknofliplowerlegstretchblendnodeotp_plug, nofliprightfootjntty_plug)
                    self.MDG2_mod.connect(ikrightlegstretch_plug, riknoflipupperlegstretchblendnodeblender_plug)
                    self.MDG2_mod.connect(ikrightlegstretch_plug, riknofliplowerlegstretchblendnodeblender_plug)
                    self.MDG2_mod.commandToExecute('float $noflipikrightlegtranslateY = `getAttr "NoFlipRightUpperLegStretch_blend.color1G"`; setAttr "NoFlipRightUpperLegStretch_blend.color2G" $noflipikrightlegtranslateY;')
                    self.MDG2_mod.commandToExecute('float $noflipikrightfoottranslateY = `getAttr "NoFlipRightLowerLegStretch_blend.color1G"`; setAttr "NoFlipRightLowerLegStretch_blend.color2G" $noflipikrightfoottranslateY;')
                    self.MDG2_mod.commandToExecute('setAttr "NoFlipRightLegTrans_multiply.operation" 1')
                    self.MDG2_mod.commandToExecute('setAttr "NoFlipRightFootTrans_multiply.operation" 1')

                    rightlegglobalscalenode = self.MDG2_mod.createNode("multiplyDivide")
                    nofliprightlegglobalscalenode = self.MDG2_mod.createNode("multiplyDivide")
                    nofliprigthfootlobalscalenode = self.MDG2_mod.createNode("multiplyDivide")
                    self.MDG2_mod.renameNode(rightlegglobalscalenode, "IKRightLegGlobalScale_Average")
                    self.MDG2_mod.renameNode(nofliprightlegglobalscalenode, "IKNoFlipRightLegGlobalScale_Average")
                    self.MDG2_mod.renameNode(nofliprigthfootlobalscalenode, "IKNoFlipRightFootGlobalScale_Average")

                    rightlegglobalscale_fs = om2.MFnDependencyNode(rightlegglobalscalenode)
                    nofliprightlegglobalscale_fs = om2.MFnDependencyNode(nofliprightlegglobalscalenode)
                    nofliprightfootlobalscale_fs = om2.MFnDependencyNode(nofliprigthfootlobalscalenode)
                    masterlctrl_fs = om2.MFnDependencyNode(obj_masterctrl2)

                    rikupperlegjntDist_plug = rikupperlegjntDist_fs.findPlug("distance", False)
                    riklowerlegjntDist_plug = riklowerlegjntDist_fs.findPlug("distance", False)
                    riklegjntDist_plug = riklegjntDist_fs.findPlug("distance", False)
                    masterlctrlsy_plug = masterlctrl_fs.findPlug("scaleY", False)
                    rightlegglobalscaleInp1Y_plug = rightlegglobalscale_fs.findPlug("input1Y", False)
                    rightlegglobalscaleInp2Y_plug = rightlegglobalscale_fs.findPlug("input2Y", False)
                    rigthlegglobalscaleOtpY_plug = rightlegglobalscale_fs.findPlug("outputY", False)
                    nofliprightlegglobalscaleInp1Y_plug = nofliprightlegglobalscale_fs.findPlug("input1Y", False)
                    nofliprightlegglobalscaleInp2Y_plug = nofliprightlegglobalscale_fs.findPlug("input2Y", False)
                    nofliprightlegglobalscaleOtpY_plug = nofliprightlegglobalscale_fs.findPlug("outputY", False)
                    nofliprightfootlobalscaleInp1Y_plug = nofliprightfootlobalscale_fs.findPlug("input1Y", False)
                    nofliprightfootlobalscaleInp2Y_plug = nofliprightfootlobalscale_fs.findPlug("input2Y", False)
                    nofliprightfootlobalscaleOtpY_plug = nofliprightfootlobalscale_fs.findPlug("outputY", False)
                    nofliprightkneekeyinp_plug = nofliprightkneekey_fs.findPlug("input", False)
                    nofliprightfootkeyinp_plug = nofliprightfootkey_fs.findPlug("input", False)
                    pvrightkneekeyinp_plug = pvrightkneekey_fs.findPlug("input", False)
                    pvrightfootkeyinp_plug = pvrightfootkey_fs.findPlug("input", False)
                    ikrightjointleggrps_plug = ikrightjointleggrp_fs.findPlug("scale", False)

                    self.MDG2_mod.disconnect(riklegjntDist_plug, nofliprightkneekeyinp_plug)
                    self.MDG2_mod.disconnect(riklegjntDist_plug, nofliprightfootkeyinp_plug)
                    self.MDG2_mod.disconnect(riklegjntDist_plug, pvrightkneekeyinp_plug)
                    self.MDG2_mod.disconnect(riklegjntDist_plug, pvrightfootkeyinp_plug)
                    self.MDG2_mod.connect(riklowerlegjntDist_plug, nofliprightfootlobalscaleInp1Y_plug)
                    self.MDG2_mod.connect(rikupperlegjntDist_plug, nofliprightlegglobalscaleInp1Y_plug)
                    self.MDG2_mod.connect(riklowerlegjntDist_plug, nofliprightfootlobalscaleInp1Y_plug)
                    self.MDG2_mod.connect(masterlctrlsy_plug, nofliprightlegglobalscaleInp2Y_plug)
                    self.MDG2_mod.connect(masterlctrlsy_plug, nofliprightfootlobalscaleInp2Y_plug)
                    self.MDG2_mod.connect(nofliprightlegglobalscaleOtpY_plug, rikpvuppertransblendnodeinp1g_plug)
                    self.MDG2_mod.connect(nofliprightfootlobalscaleOtpY_plug, rikpvlowertransblendnodeinp1g_plug)
                    self.MDG2_mod.connect(riklegjntDist_plug, rightlegglobalscaleInp1Y_plug)
                    self.MDG2_mod.connect(masterlctrlsy_plug, rightlegglobalscaleInp2Y_plug)
                    self.MDG2_mod.connect(rigthlegglobalscaleOtpY_plug, nofliprightkneekeyinp_plug)
                    self.MDG2_mod.connect(rigthlegglobalscaleOtpY_plug, nofliprightfootkeyinp_plug)
                    self.MDG2_mod.connect(rigthlegglobalscaleOtpY_plug, pvrightkneekeyinp_plug)
                    self.MDG2_mod.connect(rigthlegglobalscaleOtpY_plug, pvrightfootkeyinp_plug)
                    self.MDG2_mod.commandToExecute('setAttr "IKNoFlipRightLegGlobalScale_Average.operation" 2')
                    self.MDG2_mod.commandToExecute('setAttr "IKNoFlipRightFootGlobalScale_Average.operation" 2')
                    self.MDG2_mod.commandToExecute('setAttr "IKRightLegGlobalScale_Average.operation" 2')
                    self.MDG2_mod.connect(masterdecomposeOtpScale_plug, ikrightjointleggrps_plug)

                # else:
                #     self.MDG2_mod.commandToExecute('delete "IkStretchyRightJointLeg_grp"')
                #     self.MDG2_mod.commandToExecute('delete "RightLegIkCluster_grp"')

                self.MDG2_mod.commandToExecute('addAttr -longName "footrollswitch" -niceName "Auto/Manual Foot Roll" -attributeType double -minValue 0 -maxValue 1 -keyable true -defaultValue 0 Biped_RightFootOptions_ctrl')

                self.MDG2_mod.commandToExecute('addAttr -longName "autoroll" -niceName "Auto Roll" -attributeType "enum" -en "__________:" -keyable true Biped_IkRightFoot_ctrl')
                self.MDG2_mod.commandToExecute('addAttr -longName "roll" -niceName "Roll" -attributeType double -minValue -90 -keyable true -defaultValue 0 Biped_IkRightFoot_ctrl')
                self.MDG2_mod.commandToExecute('addAttr -longName "bendlimitangle" -niceName "Bend Limit Angle" -attributeType double -keyable true -defaultValue 45 Biped_IkRightFoot_ctrl')
                self.MDG2_mod.commandToExecute('addAttr -longName "toestraightangle" -niceName "Toe Straight Angle" -attributeType double -keyable true -defaultValue 70 Biped_IkRightFoot_ctrl')
                self.MDG2_mod.commandToExecute('addAttr -longName "manualroll" -niceName "Manual Roll" -attributeType "enum" -en "__________:" -keyable true Biped_IkRightFoot_ctrl')
                self.MDG2_mod.commandToExecute('addAttr -longName "heelroll" -niceName "Heel Roll" -attributeType double -keyable true -defaultValue 0 Biped_IkRightFoot_ctrl')
                self.MDG2_mod.doIt()

                rikheelclampnode = self.MDG2_mod.createNode("clamp")
                self.MDG2_mod.renameNode(rikheelclampnode, "RightHeel_rotclamp")
                rikheelblendernode = self.MDG2_mod.createNode("blendColors")
                self.MDG2_mod.renameNode(rikheelblendernode, "RightHeel_blend")
                leg_reverse_sl_ls = om2.MSelectionList()
                leg_reverse_sl_ls.add("RightReverseFootHeel")
                reverse_heel_obj = leg_reverse_sl_ls.getDependNode(0)

                rikheelclamp_fs = om2.MFnDependencyNode(rikheelclampnode)
                rikheelblender_fs = om2.MFnDependencyNode(rikheelblendernode)
                reverseheel_fs = om2.MFnDependencyNode(reverse_heel_obj)

                rlegoptionsfootrollswitch_plug = rlegoptions_fs.findPlug("footrollswitch", False)
                rikheelblender_plug = rikheelblender_fs.findPlug("blender", False)
                iklegctrlRoll_plug = iklegctrl_fs.findPlug("roll", False)
                rikheelclampInpR_plug = rikheelclamp_fs.findPlug("inputR", False)
                rikheelclampOtpR_plug = rikheelclamp_fs.findPlug("outputR", False)
                rikheelblendCol2R_plug = rikheelblender_fs.findPlug("color2R", False)
                iklegctrlHeelRoll_plug = iklegctrl_fs.findPlug("heelroll", False)
                rikheelblendCol1R_plug = rikheelblender_fs.findPlug("color1R", False)
                rikheelblendOtpR_plug = rikheelblender_fs.findPlug("outputR", False)
                rikheelclampInpX_plug = reverseheel_fs.findPlug("rotateX", False)

                self.MDG2_mod.connect(rlegoptionsfootrollswitch_plug, rikheelblender_plug)
                self.MDG2_mod.connect(iklegctrlRoll_plug, rikheelclampInpR_plug)
                self.MDG2_mod.connect(rikheelclampOtpR_plug, rikheelblendCol2R_plug)
                self.MDG2_mod.connect(iklegctrlHeelRoll_plug, rikheelblendCol1R_plug)
                self.MDG2_mod.connect(rikheelblendOtpR_plug, rikheelclampInpX_plug)
                self.MDG2_mod.commandToExecute('setAttr "RightHeel_rotclamp.minR" -90')

                self.MDG2_mod.commandToExecute('addAttr -longName "footroll" -niceName "Foot Roll" -attributeType double -keyable true -defaultValue 0 Biped_IkRightFoot_ctrl')
                self.MDG2_mod.doIt()

                rikballclampnode = self.MDG2_mod.createNode("clamp")
                self.MDG2_mod.renameNode(rikballclampnode, "RightBall_rotclamp")
                rikballrangenode = self.MDG2_mod.createNode("setRange")
                self.MDG2_mod.renameNode(rikballrangenode, "RightBall_range")
                rikballblendernode = self.MDG2_mod.createNode("blendColors")
                self.MDG2_mod.renameNode(rikballblendernode, "RightBall_blend")
                rikballminusnode = self.MDG2_mod.createNode("plusMinusAverage")
                self.MDG2_mod.renameNode(rikballminusnode, "RightBall_minus")
                rikballmultnode = self.MDG2_mod.createNode("multiplyDivide")
                self.MDG2_mod.renameNode(rikballmultnode, "RightBall_percetmult")
                rikballrollmultnode = self.MDG2_mod.createNode("multiplyDivide")
                self.MDG2_mod.renameNode(rikballrollmultnode, "RightBall_rollmult")
                leg_reverse_sl_ls.add("RightReverseFootToe")
                reverse_toe_obj = leg_reverse_sl_ls.getDependNode(1)

                rikballclamp_fs = om2.MFnDependencyNode(rikballclampnode)
                rikballrange_fs = om2.MFnDependencyNode(rikballrangenode)
                rikballsub_fs = om2.MFnDependencyNode(rikballminusnode)
                rikballmult_fs = om2.MFnDependencyNode(rikballmultnode)
                rikballrollmult_fs = om2.MFnDependencyNode(rikballrollmultnode)
                rikballblender_fs = om2.MFnDependencyNode(rikballblendernode)
                reversetoe_fs = om2.MFnDependencyNode(reverse_toe_obj)

                rikballblender_plug = rikballblender_fs.findPlug("blender", False)
                rikballclampInpR_plug = rikballclamp_fs.findPlug("inputR", False)
                rikballclampMinR_plug = rikballclamp_fs.findPlug("minR", False)
                iklegctrlBendLimit_plug = iklegctrl_fs.findPlug("bendlimitangle", False)
                rikballclampMaxR_plug = rikballclamp_fs.findPlug("maxR", False)
                rikballrangeValueX_plug = rikballrange_fs.findPlug("valueX", False)
                rikballrangeOldMinX_plug = rikballrange_fs.findPlug("oldMinX", False)
                rikballrangeOldMaxX_plug = rikballrange_fs.findPlug("oldMaxX", False)
                rikballrangeOutValueX_plug = rikballrange_fs.findPlug("outValueX", False)
                rikballmultInp1X_plug = rikballmult_fs.findPlug("input1X", False)
                rikballmultInp2X_plug = rikballmult_fs.findPlug("input2X", False)
                rikballmultOtpX_plug = rikballmult_fs.findPlug("outputX", False)
                rikballsubOtp1D_plug = rikballsub_fs.findPlug("output1D", False)
                rikballrollmultInp1X_plug = rikballrollmult_fs.findPlug("input1X", False)
                rikballrollmultInp2X_plug = rikballrollmult_fs.findPlug("input2X", False)
                rikballrollmultOtpX_plug = rikballrollmult_fs.findPlug("outputX", False)
                rikballblendCol2R_plug = rikballblender_fs.findPlug("color2R", False)
                iklegctrlBallRoll_plug = iklegctrl_fs.findPlug("footroll", False)
                rikballblendCol1R_plug = rikballblender_fs.findPlug("color1R", False)
                rikballblendOtpR_plug = rikballblender_fs.findPlug("outputR", False)
                rikballclampRotX_plug = reversetoe_fs.findPlug("rotateX", False)

                self.MDG2_mod.connect(rlegoptionsfootrollswitch_plug, rikballblender_plug)
                self.MDG2_mod.connect(iklegctrlRoll_plug, rikballclampInpR_plug)
                self.MDG2_mod.connect(iklegctrlBendLimit_plug, rikballclampMaxR_plug)
                self.MDG2_mod.connect(rikballclampInpR_plug, rikballrangeValueX_plug)
                self.MDG2_mod.connect(rikballclampMinR_plug, rikballrangeOldMinX_plug)
                self.MDG2_mod.connect(rikballclampMaxR_plug, rikballrangeOldMaxX_plug)
                self.MDG2_mod.connect(rikballrangeOutValueX_plug, rikballmultInp1X_plug)
                self.MDG2_mod.connect(rikballsubOtp1D_plug, rikballmultInp2X_plug)
                self.MDG2_mod.connect(rikballmultOtpX_plug, rikballrollmultInp1X_plug)
                self.MDG2_mod.connect(iklegctrlRoll_plug, rikballrollmultInp2X_plug)
                self.MDG2_mod.connect(rikballrollmultOtpX_plug, rikballblendCol2R_plug)
                self.MDG2_mod.connect(iklegctrlBallRoll_plug, rikballblendCol1R_plug)
                self.MDG2_mod.connect(rikballblendOtpR_plug, rikballclampRotX_plug)
                self.MDG2_mod.commandToExecute('setAttr "RightBall_range.minX" 0')
                self.MDG2_mod.commandToExecute('setAttr "RightBall_range.maxX" 1')
                self.MDG2_mod.commandToExecute('setAttr "RightBall_minus.input1D[0]" 1')
                self.MDG2_mod.commandToExecute('setAttr "RightBall_minus.operation" 2')
                self.MDG2_mod.commandToExecute('setAttr "RightBall_percetmult.operation" 1')
                self.MDG2_mod.commandToExecute('setAttr "RightBall_rollmult.operation" 1')

                self.MDG2_mod.commandToExecute('addAttr -longName "toeroll" -niceName "Toe Roll" -attributeType double -keyable true -defaultValue 0 Biped_IkRightFoot_ctrl')
                self.MDG2_mod.doIt()

                riktoeclampnode = self.MDG2_mod.createNode("clamp")
                self.MDG2_mod.renameNode(riktoeclampnode, "RightToe_rotclamp")
                riktoeblendernode = self.MDG2_mod.createNode("blendColors")
                self.MDG2_mod.renameNode(riktoeblendernode, "RightToe_blend")
                riktoerangernode = self.MDG2_mod.createNode("setRange")
                self.MDG2_mod.renameNode(riktoerangernode, "RightToe_range")
                riktoemultnode = self.MDG2_mod.createNode("multiplyDivide")
                self.MDG2_mod.renameNode(riktoemultnode, "RightToe_percetmultiply")
                leg_reverse_sl_ls.add("RightReverseFootToeEnd")
                reverse_toeend_obj = leg_reverse_sl_ls.getDependNode(2)

                riktoeclamp_fs = om2.MFnDependencyNode(riktoeclampnode)
                riktoerange_fs = om2.MFnDependencyNode(riktoerangernode)
                riktoemult_fs = om2.MFnDependencyNode(riktoemultnode)
                riktoeblender_fs = om2.MFnDependencyNode(riktoeblendernode)
                reversetoeend_fs = om2.MFnDependencyNode(reverse_toeend_obj)

                riktoeblender_plug = riktoeblender_fs.findPlug("blender", False)
                iklegctrlStraightLimit_plug = iklegctrl_fs.findPlug("toestraightangle", False)
                riktoeclampInpR_plug = riktoeclamp_fs.findPlug("inputR", False)
                riktoeclampMinR_plug = riktoeclamp_fs.findPlug("minR", False)
                riktoeclampMaxR_plug = riktoeclamp_fs.findPlug("maxR", False)
                riktoerangeValueX_plug = riktoerange_fs.findPlug("valueX", False)
                riktoerangeOldMinX_plug = riktoerange_fs.findPlug("oldMinX", False)
                riktoerangeOldMaxX_plug = riktoerange_fs.findPlug("oldMaxX", False)
                riktoerangeoOutValX_plug = riktoerange_fs.findPlug("outValueX", False)
                riktoemultInp1X_plug = riktoemult_fs.findPlug("input1X", False)
                riktoemultInp2X_plug = riktoemult_fs.findPlug("input2X", False)
                riktoemultOtpX_plug = riktoemult_fs.findPlug("outputX", False)
                riktoeblendCol2R_plug = riktoeblender_fs.findPlug("color2R", False)
                iklegctrlToeRoll_plug = iklegctrl_fs.findPlug("toeroll", False)
                riktoeblendCol1R_plug = riktoeblender_fs.findPlug("color1R", False)
                riktoeblendOtpR_plug = riktoeblender_fs.findPlug("outputR", False)
                riktoeclampRotX_plug = reversetoeend_fs.findPlug("rotateX", False)

                self.MDG2_mod.connect(rlegoptionsfootrollswitch_plug, riktoeblender_plug)
                self.MDG2_mod.connect(iklegctrlRoll_plug, riktoeclampInpR_plug)
                self.MDG2_mod.connect(iklegctrlBendLimit_plug, riktoeclampMinR_plug)
                self.MDG2_mod.connect(iklegctrlStraightLimit_plug, riktoeclampMaxR_plug)
                self.MDG2_mod.connect(riktoeclampInpR_plug, riktoerangeValueX_plug)
                self.MDG2_mod.connect(riktoeclampMinR_plug, riktoerangeOldMinX_plug)
                self.MDG2_mod.connect(riktoeclampMaxR_plug, riktoerangeOldMaxX_plug)
                self.MDG2_mod.connect(riktoerangeoOutValX_plug, riktoemultInp1X_plug)
                self.MDG2_mod.connect(riktoeclampInpR_plug, riktoemultInp2X_plug)
                self.MDG2_mod.connect(riktoemultOtpX_plug, riktoeblendCol2R_plug)
                self.MDG2_mod.commandToExecute('connectAttr -force RightToe_range.outValueX RightBall_minus.input1D[1]')
                self.MDG2_mod.connect(iklegctrlToeRoll_plug, riktoeblendCol1R_plug)
                self.MDG2_mod.connect(riktoeblendOtpR_plug, riktoeclampRotX_plug)
                self.MDG2_mod.commandToExecute('setAttr "RightToe_range.minX" 0')
                self.MDG2_mod.commandToExecute('setAttr "RightToe_range.maxX" 1')
                self.MDG2_mod.commandToExecute('setAttr "RightToe_percetmultiply.operation" 1')

                self.MDG2_mod.commandToExecute('addAttr -longName "common" -niceName "Common" -attributeType "enum" -en "__________:" -keyable true Biped_IkRightFoot_ctrl')
                self.MDG2_mod.commandToExecute('addAttr -longName "tilt" -niceName "Tilt" -attributeType double -minValue -180 -maxValue 180 -keyable true -defaultValue 0 Biped_IkRightFoot_ctrl')
                self.MDG2_mod.doIt()

                rikinnerlegtiltclampnode = self.MDG2_mod.createNode("clamp")
                self.MDG2_mod.renameNode(rikinnerlegtiltclampnode, "RightInnerLegTilt_clamp")
                rikouterlegtiltclampnode = self.MDG2_mod.createNode("clamp")
                self.MDG2_mod.renameNode(rikouterlegtiltclampnode, "RightOuterLegTilt_clamp")
                leg_reverse_sl_ls.add("RightReverseInnerFoot")
                leg_reverse_sl_ls.add("RightReverseOuterFoot")
                reverse_inner_obj = leg_reverse_sl_ls.getDependNode(3)
                reverse_outer_obj = leg_reverse_sl_ls.getDependNode(4)

                rikinnerclamp_fs = om2.MFnDependencyNode(rikinnerlegtiltclampnode)
                rikouterclamp_fs = om2.MFnDependencyNode(rikouterlegtiltclampnode)
                reverseinnerfoot_fs = om2.MFnDependencyNode(reverse_inner_obj)
                reverseouterfoot_fs = om2.MFnDependencyNode(reverse_outer_obj)

                iklegctrlTilt_plug = iklegctrl_fs.findPlug("tilt", False)
                rikinnerclampInpB_plug = rikinnerclamp_fs.findPlug("inputB", False)
                rikouterclampInpB_plug = rikouterclamp_fs.findPlug("inputB", False)
                rikinnerclampOtpB_plug = rikinnerclamp_fs.findPlug("outputB", False)
                rikinnerclampRotZ_plug = reverseinnerfoot_fs.findPlug("rotateZ", False)
                rikouterclampOtpB_plug = rikouterclamp_fs.findPlug("outputB", False)
                rikouterclampRotZ_plug = reverseouterfoot_fs.findPlug("rotateZ", False)

                self.MDG2_mod.connect(iklegctrlTilt_plug, rikinnerclampInpB_plug)
                self.MDG2_mod.connect(iklegctrlTilt_plug, rikouterclampInpB_plug)
                self.MDG2_mod.connect(rikinnerclampOtpB_plug, rikinnerclampRotZ_plug)
                self.MDG2_mod.connect(rikouterclampOtpB_plug, rikouterclampRotZ_plug)
                self.MDG2_mod.commandToExecute('setAttr "RightInnerLegTilt_clamp.minB" -180')
                self.MDG2_mod.commandToExecute('setAttr "RightOuterLegTilt_clamp.maxB" 180')

                self.MDG2_mod.commandToExecute('addAttr -longName "lean" -niceName "Lean" -attributeType double -keyable true -defaultValue 0 Biped_IkRightFoot_ctrl')
                self.MDG2_mod.commandToExecute('addAttr -longName "toespin" -niceName "Toe Spin" -attributeType double -keyable true -defaultValue 0 Biped_IkRightFoot_ctrl')
                self.MDG2_mod.commandToExecute('addAttr -longName "toewiggle" -niceName "Toe Wiggle" -attributeType double -keyable true -defaultValue 0 Biped_IkRightFoot_ctrl')
                self.MDG2_mod.doIt()

                leg_reverse_sl_ls.add("RightReverseFootToeWiggle")
                reverse_toewiggle_obj = leg_reverse_sl_ls.getDependNode(5)

                reversetoewiggle_fs = om2.MFnDependencyNode(reverse_toewiggle_obj)

                iklegctrlLean_plug = iklegctrl_fs.findPlug("lean", False)
                rikballclampRotZ_plug = reversetoe_fs.findPlug("rotateZ", False)
                iklegctrlToeSpin_plug = iklegctrl_fs.findPlug("toespin", False)
                riktoeclampRotY_plug = reversetoeend_fs.findPlug("rotateY", False)
                iklegctrlToeWiggle_plug = iklegctrl_fs.findPlug("toewiggle", False)
                reversetoewiggleRotX_plug = reversetoewiggle_fs.findPlug("rotateX", False)

                self.MDG2_mod.connect(iklegctrlLean_plug, rikballclampRotZ_plug)
                self.MDG2_mod.connect(iklegctrlToeSpin_plug, riktoeclampRotY_plug)
                self.MDG2_mod.connect(iklegctrlToeWiggle_plug, reversetoewiggleRotX_plug)
        else:
            self.MDG2_mod.commandToExecute('delete "Biped_IkRightFoot_null"')
            self.MDG2_mod.commandToExecute('delete "IkRightJointLeg_grp"')
            self.MDG2_mod.commandToExecute('setAttr -keyable false -channelBox false Biped_RightFootOptions_ctrl.fkik')
            self.MDG2_mod.doIt()

        self.MDG2_mod.commandToExecute('delete "Draw*"')
        self.MDG2_mod.commandToExecute('select -hierarchy "DoNotTouch"; hide -clearSelection;')
        self.MDG2_mod.doIt()

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

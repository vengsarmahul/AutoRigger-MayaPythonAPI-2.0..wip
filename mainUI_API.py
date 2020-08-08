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
        self.createUIConnection()
        
    def createWidgets(self):
        self.createLocatorBut = QtWidgets.QPushButton('Create Locator')
        self.createLocatorBut.clicked.connect(self.createLocator)
        self.deleteLocatorBut = QtWidgets.QPushButton('Delete Locator')
        self.deleteLocatorBut.clicked.connect(self.deleteLocator)
        self.mirrorLocatorBut = QtWidgets.QPushButton('Mirror Locator (X)-->(-X)')
        self.mirrorLocatorBut.clicked.connect(self.mirrorLocator)
        self.createJointBut = QtWidgets.QPushButton('Create Joints')
        self.createJointBut.clicked.connect(self.createJoints)
        self.deleteJointBut = QtWidgets.QPushButton('Delete Joints')
        self.deleteJointBut.clicked.connect(self.deleteJoints)

        self.createSpineText = QtWidgets.QLineEdit()
        self.countFingers = QtWidgets.QLineEdit()

        self.editModeCheckBox = QtWidgets.QCheckBox()

        self.typeofRigComboBox = QtWidgets.QComboBox()
        self.typeofRigComboBox.addItems(["Biped Rig", "Quadruple Rig"])

    def createLayout(self):
        form_layout_1 = QtWidgets.QFormLayout()
        form_layout_1.addRow("Enter No. Of Spine:", self.createSpineText)
        form_layout_1.addRow("Enter No. Of Finger:", self.countFingers)

        form_layout_2 = QtWidgets.QFormLayout()
        form_layout_2.addRow("Edit Mode", self.editModeCheckBox)

        form_layout_3 = QtWidgets.QFormLayout()
        form_layout_3.addRow("Choose Rig Type", self.typeofRigComboBox)

        horizonLayout = QtWidgets.QHBoxLayout()
        horizonLayout.addWidget(self.createLocatorBut)
        horizonLayout.addWidget(self.deleteLocatorBut)
        horizonLayout.addWidget(self.mirrorLocatorBut)
        horizonLayout.addLayout(form_layout_2)

    def createUIConnection(self):
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

            self.loc_transform = om.MFnTransform(self.loc_root_tn)

            loc_plug_ty = self.loc_transform.findPlug("translateY", False)
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

            self.spineloc_transform = om.MFnTransform(self.spine_tn)
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
        headloc_grp = om.MFnDagNode()

        neckloc_tn = headloc_grp.create("transform", "loc_neck", self.spine_tn)
        neckloc_ln = headloc_grp.create("locator", "locatorShape1", neckloc_tn)

        self.neckloc_transform_t = om.MFnTransform(neckloc_tn)

        neckloc_plug_s = self.neckloc_transform_t.findPlug("scale", False)
        if neckloc_plug_s.isCompound:
            for i in range(neckloc_plug_s.numChildren()):
                child_plug = neckloc_plug_s.child(i)
                attr_value = child_plug.setDouble(0.5)

        neckloc_plug_ty = self.neckloc_transform_t.findPlug("translateY", False)
        neckloc_plug_ty.setDouble((((int(self.createSpineText.text())-1)*0.5)+1.25))

        headlowloc_tn = headloc_grp.create("transform", "loc_headlower", neckloc_tn)
        headlowloc_ln = headloc_grp.create("locator", "locatorShape1", headlowloc_tn)

        self.headlowloc_transform_t = om.MFnTransform(headlowloc_tn)

        headlowloc_plug_ty = self.headlowloc_transform_t.findPlug("translateY", False)
        headlowloc_plug_ty.setDouble((((int(self.createSpineText.text())-1)*0.5)+0.75))

        headendloc_tn = headloc_grp.create("transform", "loc_headend", headlowloc_tn)
        headendloc_ln = headloc_grp.create("locator", "locatorShape1", headendloc_tn)

        self.headendloc_transform_t = om.MFnTransform(headendloc_tn)
        headendloc_plug_ty = self.headendloc_transform_t.findPlug("translateY", False)
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

                self.lshoulder_transform = om.MFnTransform(self.l_shoulder_tn)

                lshoulder_plug_s = self.lshoulder_transform.findPlug("scale", False)
                if lshoulder_plug_s.isCompound:
                    for i in range(lshoulder_plug_s.numChildren()):
                        child_plug = lshoulder_plug_s.child(i)
                        attr_value = child_plug.setDouble(0.5)

                lshoulder_plug_t = self.lshoulder_transform.translation(om.MSpace.kTransform)
                lshoulder_plug_t[0], lshoulder_plug_t[1] = 2.5, ((int(self.createSpineText.text())-1)*0.5)+0.50
                self.lshoulder_transform.setTranslation(lshoulder_plug_t, om.MSpace.kTransform)

    def createArms(self, side):
        loc_arm = ["loc_L_arm_grp", "loc_R_arm_grp"]
        obj_list = om.MSelectionList()
        armloc_grp = om.MFnDagNode()

        if side == 1:
            try:
                obj_list.add(loc_arm[0])
                print("loc_Larm_grp already exist")
            except:
                self.l_arm_Grp = armloc_grp.create("transform", "loc_L_arm_grp", self.l_shoulder_tn)
                self.up_Larm_tn = armloc_grp.create("transform", "loc_L_upperarm", self.l_arm_Grp)
                up_Larm_ln = armloc_grp.create("locator", "locatorShape1", self.up_Larm_tn)

                self.larmloc_transform = om.MFnTransform(self.l_arm_Grp)
                larmloc_t = self.larmloc_transform.translation(om.MSpace.kTransform)
                larmloc_t[0], larmloc_t[1] = 4.5, -(((int(self.createSpineText.text())-1)*0.5)+2)
                self.larmloc_transform.setTranslation(larmloc_t, om.MSpace.kTransform)

                l_elbow_tn = armloc_grp.create("transform", "loc_L_elbow", self.up_Larm_tn)
                l_elbow_ln = armloc_grp.create("locator", "locatorShape1", l_elbow_tn)

                self.lelbowloc_transform = om.MFnTransform(l_elbow_tn)
                lelbowloc_t = self.lelbowloc_transform.translation(om.MSpace.kTransform)
                lelbowloc_t[0], lelbowloc_t[1] = 4.35, -(((int(self.createSpineText.text())-1)*0.5)+5.25)
                self.lelbowloc_transform.setTranslation(lelbowloc_t, om.MSpace.kTransform)

                self.l_wrist_tn = armloc_grp.create("transform", "loc_L_wrist", l_elbow_tn)
                l_wrist_ln = armloc_grp.create("locator", "locatorShape1", self.l_wrist_tn)

                self.lwristloc_transform = om.MFnTransform(self.l_wrist_tn)
                lwristloc_t = self.lwristloc_transform.translation(om.MSpace.kTransform)
                lwristloc_t[0], lwristloc_t[1] = 6.35, -(((int(self.createSpineText.text())-1)*0.5)+6.25)
                self.lwristloc_transform.setTranslation(lwristloc_t, om.MSpace.kTransform)

                self.createHands(1)
                
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


    def mirrorLocator(self):
        allLeftLocator = "loc_L_*"
        leftloc_ls = om.MSelectionList()
        leftloc_ls.add(allLeftLocator)

        allRightLocator = "loc_R_*"
        rightloc_ls = om.MSelectionList()
        rightloc_ls.add(allRightLocator)

        for index in range(leftloc_ls.length()):
            obj_l_loc = leftloc_ls.getDependNode(index)
            l_obj_tn = om.MFnTransform(obj_l_loc)

            obj_r_loc = rightloc_ls.getDependNode(index)
            r_obj_tn = om.MFnTransform(obj_r_loc)

            translation = l_obj_tn.translation(om.MSpace.kTransform)
            rotation = l_obj_tn.rotation(om.MSpace.kTransform)
            translation[0] = -translation[0]
            rotation[1], rotation[2] = -rotation[1], -rotation[2]
            r_obj_tn.setTranslation(translation, om.MSpace.kTransform)
            r_obj_tn.setRotation(rotation, om.MSpace.kTransform)

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
        jnt_grp = "Rig_grp"
        obj_lst = om.MSelectionList()
        spinejnt_grp = om.MFnDagNode()
        loc_root_transform = self.loc_transform.transformation()
        loc_spine_transform = self.spineloc_transform.transformation()

        try:
            obj_lst.add(jnt_grp)
            print("Rig_grp already exist")
        except:
            jnt_grp = spinejnt_grp.create("transform", "Rig_grp")

            self.jnt_root_tn = spinejnt_grp.create("joint", "Hip", jnt_grp)

            jnt_root_tranform = om.MFnTransform(self.jnt_root_tn)
            jnt_root_tranform.transformation()
            jnt_root_tranform.setTransformation(loc_root_transform)

            spine_loc = "loc_Spine_*"
            spine_loc_ls = om.MSelectionList()
            spine_loc_ls.add(spine_loc)

            for index in range(spine_loc_ls.length()):
                if index == 0:
                    self.spine_jnt = spinejnt_grp.create("joint", "Spine"+str(index), self.jnt_root_tn)
                else:
                    self.spine_jnt = spinejnt_grp.create("joint", "Spine"+str(index), self.spine_jnt)

                jnt_spine_tranform = om.MFnTransform(self.spine_jnt)
                jnt_spine_tranform.transformation()
                jnt_spine_tranform.setTransformation(loc_spine_transform)

            self.createHeadJoints()
            self.createShoulderJoints(1)
            self.createShoulderJoints(-1)
            self.createArmJoints(1)
            self.createArmJoints(-1)

            lfinger_loc = "loc_L_finger_*"
            self.lfinger_lst = om.MSelectionList()
            self.lfinger_lst.add(lfinger_loc)

            rfinger_loc = "loc_R_finger_*"
            rfinger_lst = om.MSelectionList()
            rfinger_lst.add(rfinger_loc)

            self.createFingerJoints()

try:
    display_dailog.close()
    display_dailog.deleteLater()
except:
    pass

display_dailog = MainWindow()
display_dailog.show()

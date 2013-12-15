import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel

class ModifiersWidget(object):    
    """
    Maya widget that makes it easy to choose between various selection and visibility modifiers.
    
    usage:
			create an instance of the ModifiersWidget:
				myModWidget = ModifiersWidget()
    """
    
    def __init__(self):
        self.widgets = {}
        self.selectionModList = ["Surface",
                            "Rendering",
                            "Dynamic",    
                            "Deformer",
                            "Curve",    
                            "Joint",
                            "Marker",
                            "Other"]
        
        self.visibilityModList = [
                            "Polygons",
                            "Curves",
                            "NURBS Surfaces",
                            "Lights",
                            "Cameras",
                            "Dynamics",
                            "Joints",
                            "Deformers",
                            "Others"
                            ]
                            
        self.visTopList = [
                      "polymeshes",
                      "nurbsCurves",
                      "nurbsSurfaces",
                      "lights",
                      "cameras",    
                      "Dynamics",
                      "joints",
                      "deformers",
                      "Others"
                      ]
        
        self.visDynamicsList = [
                            "dynamics",
                            "fluids",
                            "hairSystems",
                            "follicles",
                            "nCloths",
                            "nParticles",
                            "nRigids",
                            "dynamicConstraints"
                           ]
        self.visOthersList = [
                          "subdivSurfaces",
                          "planes",
                          "controlVertices",
                          "hulls",
                          "ikHandles",
                          "locators",
                          "dimensions",
                          "handles",
                          "pivots",
                          "textures",
                          "strokes"
                        ]
        
        '''                
        self.visOthersList = [
                          "subdivSurfaces",
                          "planes",
                          "controlVertices",
                          "grid",
                          "hulls",
                          "ikHandles",
                          "locators",
                          "manipulators",
                          "dimensions",
                          "handles",
                          "pivots",
                          "textures",
                          "strokes"
                        ]
        '''
        
        self.visibilityModDict = {}
        self.visibilityModDict.update({self.visibilityModList[0] : self.visTopList[0]})
        self.visibilityModDict.update({self.visibilityModList[1] : self.visTopList[1]})
        self.visibilityModDict.update({self.visibilityModList[2] : self.visTopList[2]})
        self.visibilityModDict.update({self.visibilityModList[3] : self.visTopList[3]})
        self.visibilityModDict.update({self.visibilityModList[4] : self.visTopList[4]})
        self.visibilityModDict.update({self.visibilityModList[5] : self.visDynamicsList})
        self.visibilityModDict.update({self.visibilityModList[6] : self.visTopList[6]})
        self.visibilityModDict.update({self.visibilityModList[7] : self.visTopList[7]})
        self.visibilityModDict.update({self.visibilityModList[8] : self.visOthersList})
        
        self.makeUI()
        
    def setSelectionModifier(self):
        selectedMods = cmds.textScrollList(self.widgets['selectionModList1'], query = True, selectItem = True)
        allMods = cmds.textScrollList(self.widgets['selectionModList1'], query = True, allItems = True)
        
        if selectedMods == None and selectedMods == []:
            return False;
        
        for mod in allMods:
            if mod in selectedMods:
                mel.eval('setObjectPickMask "' + mod + '" true;')
            else:
                mel.eval('setObjectPickMask "' + mod + '" false;')
    
        mel.eval('updateObjectSelectionMasks;')
        mel.eval('updateComponentSelectionMasks;')
        
        return;
        
    def setVisibilityModifier(self):
        visibilityModDict = self.visibilityModDict
        selectedMods = cmds.textScrollList(self.widgets['visibilityModList1'], query = True, selectItem = True)
        allMods = cmds.textScrollList(self.widgets['visibilityModList1'], query = True, allItems = True)
        
        if selectedMods == None and selectedMods == []:
            return False;
        
        modelPanelList = []
        modelEditorList = cmds.lsUI(editors=True)
        for myModelPanel in modelEditorList:
            if myModelPanel.find('modelPanel') != -1:
                modelPanelList.append(myModelPanel)
        
        for modelPanel in modelPanelList:
            for mod in allMods:
              if mod != "Others" and mod != "Dynamics":
                if mod in selectedMods:
                    command = 'cmds.modelEditor("' + modelPanel + '", edit=True, ' + visibilityModDict[mod] + ' = True, panel = True)'
                    exec(command)
                else:
                    command = 'cmds.modelEditor("' + modelPanel + '", edit=True, ' + visibilityModDict[mod] + ' = False, panel = True)'
                    exec(command)
              else:
                if mod == "Others" or mod == "Dynamics":
                    othersList = visibilityModDict[mod]
                    if mod in selectedMods:
                        for item in othersList:
                            command = 'cmds.modelEditor("' + modelPanel + '", edit=True, ' + item + ' = True, panel = True)'
                            exec(command)
                    else:
                        for item in othersList:
                            command = 'cmds.modelEditor("' + modelPanel + '", edit=True, ' + item + ' = False, panel = True)'
                            exec(command)
                            
        return;
    
    def makeUI(self):
        if cmds.dockControl('ModifiersDockControl', exists=True):
            cmds.deleteUI('ModifiersDockControl')
        
        if cmds.window('ModifiersWindow', exists=True):
            cmds.deleteUI('ModifiersWindow')
        
        self.widgets['ModifiersWindow'] = pm.window('ModifiersWindow', title='Modifiers', mnb=True, mxb=True, sizeable=False, titleBar = True)
        
        self.widgets['selectVisiModRow1'] = pm.rowLayout(numberOfColumns = 2, parent = self.widgets['ModifiersWindow'], columnAttach=[(1, 'left', 0), (2, 'left', 0)], width = 120)
        
        self.widgets['selectVisiModCol1'] = pm.columnLayout(adjustableColumn = True, rowSpacing = 0, columnAttach=('left', 0), parent = self.widgets['selectVisiModRow1'], width = 150, height = 135)
        self.widgets['selectVisiModCol2'] = pm.columnLayout(adjustableColumn = True, rowSpacing = 0, columnAttach=('left', 0), parent = self.widgets['selectVisiModRow1'], width = 150, height = 135)
        
        cmds.text("Selection Modifiers:", parent = self.widgets['selectVisiModCol1'])
        self.widgets['selectionModList1'] = cmds.textScrollList(numberOfRows = 8, allowMultiSelection = True, append = self.selectionModList, parent = self.widgets['selectVisiModCol1'], height = 110, selectCommand = pm.windows.Callback(self.setSelectionModifier))
        
        cmds.text("Visibility Modifiers:", parent = self.widgets['selectVisiModCol2'])
        self.widgets['visibilityModList1'] = cmds.textScrollList(numberOfRows = 9, allowMultiSelection = True, append = self.visibilityModList, parent = self.widgets['selectVisiModCol2'], height = 125, selectCommand = pm.windows.Callback(self.setVisibilityModifier))
        
        allowedAreas = ['left', 'right', 'bottom', 'top']
        self.widgets['ModifiersDockControl'] = cmds.dockControl('ModifiersDockControl', label = 'Modifiers', area='top', content=self.widgets['ModifiersWindow'], allowedArea=allowedAreas, width = 400, floating=True)

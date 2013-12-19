import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os.path as path

def renameAllFileTextures():
    '''Renames all file nodes to the file that they are holding.'''
    list_of_files = cmds.ls(type='file')
    
    for files in list_of_files:
        myFile = cmds.getAttr(str(files) + '.fileTextureName')
        try:
            cmds.rename(files, path.splitext(myFile.split('/')[len(myFile.split('/'))-1])[0])
        except:
            pass
        
def reloadAllFileTextures():
    '''Reloads (refreshes) all textures.'''
    list_of_files = cmds.ls(type='file')

    for files in list_of_files:
        pm.mel.eval('AEfileTextureReloadCmd '+str(files)+'.fileTextureName')

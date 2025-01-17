
import os
import shutil

class ModManagement:
    '''
    This class manages what the user can do to a mod
    in the mod launcher.
    '''

    def delete_mod(modFolder, modName):
        '''
        This define deletes a mod folder from the mod install folder 
        if confirmed by the user.
        '''

        shutil.rmtree(os.path.join(modFolder, modName))

    def move_mod_folder(modFolder, newModFolder):
        '''
        This define moves the contents of the old mod install folder
        to the new mod install folder.
        '''

        for x in os.listdir(modFolder):
            if os.path.isdir(os.path.join(modFolder, x)):
                shutil.move(os.path.join(modFolder, x), os.path.join(newModFolder, x))
            else:
                shutil.copy2(os.path.join(modFolder, x), os.path.join(newModFolder, x))

    def delete_rpa(modFolder, rpaName):
        '''
        This define deletes a RPA from the mod folder 
        if confirmed by the user.
        '''

        os.remove(os.path.join(modFolder, rpaName))
#!/usr/bin/env python
###################################################################################################
### -                            {Translator}                                                   ##-#
### -                                                                                          ##-#
### - Authors: Luis Monteiro                                                                   ##-#
###################################################################################################
from platform   import system
from os.path    import normpath, isdir, join

# #################################################################################################
# -------------------------------------------------------------------------------------------------
# Translator
# -------------------------------------------------------------------------------------------------
# #################################################################################################
class Translator:
    #####################################################################################
    # -----------------------------------------------------------------------------------
    # init
    #------------------------------------------------------------------------------------
    def __init__(self, cwd):
        self.__cwd = normpath(cwd) if isinstance(cwd, str) else '.'

    #####################################################################################
    # -----------------------------------------------------------------------------------
    # translate
    #------------------------------------------------------------------------------------
    def digest(self, line):
        cmd, *args = line.split(' ')
        try:
            return {
                'rm' : self.__remove,
                'cp' : self.__copy,
                'mv' : self.__move,
            }[cmd](*args)
        except KeyError:
            return normpath(line)

    #####################################################################################
    # -----------------------------------------------------------------------------------
    # translate - remove
    #------------------------------------------------------------------------------------
    def __remove(self, path):
        path = normpath(path)
        # check if is a directory
        if isdir(join(self.__cwd, path)):
            return {
                'Windows': f'rmdir /q/s {path}', 
                'Linux'  : f'rm -rf {path}'
            }[system()]
        # default commands
        return {
            'Windows': f'del /f/q {path}', 
            'Linux'  : f'rm -f {path} || true'
        }[system()]

    #####################################################################################
    # -----------------------------------------------------------------------------------
    # translate - copy
    #------------------------------------------------------------------------------------
    def __copy(self, src, dst):
        src = normpath(src)
        dst = normpath(dst)
        return {
            'Windows' : f'copy {src} {dst}',
            'Linux'   : f'cp {src} {dst}',
        }[system()]

    #####################################################################################
    # -----------------------------------------------------------------------------------
    # translate - move
    #------------------------------------------------------------------------------------
    def __move(self, src, dst):
        src = normpath(src)
        dst = normpath(dst)
        return {
            'Windows' : f'move {src} {dst}',
            'Linux'   : f'mv {src} {dst}',
        }[system()]

###################################################################################################
# -------------------------------------------------------------------------------------------------
# End
# -------------------------------------------------------------------------------------------------
###################################################################################################
    


import os

class SuperTmpHandler:
    # TODO: make this comment more accurate
    # python thread has a cwd by default, this has to be saved, and set to the cwd
    #   of this object; this must be called at the very beginning of every method
    #   of this class; THE VALUE OF self.origSuperCwd MUST NOT BE CHANGED BY ANY
    #   OTHER METHOD OF THIS CLASS
    def superTmpCwd(self, executorCwd: str):
        self.__superOrigCwd = os.getcwd()
        os.chdir(executorCwd)
        return self

    # TODO: make this comment more accurate
    # at the exit of every method the cwd of the thread has to be reset to that value,
    #   which was set to it before the invocation of any method of this class;
    #   this method has to be invoked at the very end of every method of this class
    def revertSuperTmpCwd(self):
        os.chdir(self.__superOrigCwd)
        self.__superOrigCwd = None
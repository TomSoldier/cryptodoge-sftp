import os

class SuperTmpHandler:
    # python thread has a cwd by default, this has to be saved, and set to the cwd
    #   of this object; this must be called at the very beginning of every method
    #   of CmdExecutor class; THE VALUE OF self.__superOrigCwd MUST NOT BE CHANGED BY ANY
    #   EXTERNAL METHOD
    def superTmpCwd(self, executorCwd: str):
        self.__superOrigCwd = os.getcwd()
        os.chdir(executorCwd)
        return self

    # at the exit of every method the cwd of the thread has to be reset to that value,
    #   which was set to it before the invocation of any method of CmdExecutor class;
    #   this method has to be invoked at the very end of every method of CmdExecutor class
    def revertSuperTmpCwd(self):
        os.chdir(self.__superOrigCwd)
        self.__superOrigCwd = None
import os
from SuperTmpCwdHandler import SuperTmpHandler

class CmdExecutor:
    def __init__(self, rootDir: str = "./"):
        self.superOrigCwd = os.getcwd()

        self.root = rootDir
        os.chdir(rootDir)
        self.root = os.getcwd()
        self.currentWorkDir = os.getcwd()

        os.chdir(self.superOrigCwd)
        self.__delattr__("superOrigCwd")

    def __tmpCwd(self, path):
        if path == "":
            return
        os.chdir(path)
        if len(os.getcwd()) < len(self.root):
            os.chdir(self.root)

    def mkd(self, dir:str, path:str = ""):
        handler = SuperTmpHandler().superTmpCwd(self.currentWorkDir)
        self.__tmpCwd(path)
        try:
            os.mkdir(dir)
        finally:
            handler.revertSuperTmpCwd()


    def rmd(self, dir:str, path:str = ""):
        handler = SuperTmpHandler().superTmpCwd(self.currentWorkDir)
        self.__tmpCwd(path)
        try:
            os.rmdir(dir)
        finally:
            handler.revertSuperTmpCwd()

    def gwd(self):
        handler = SuperTmpHandler().superTmpCwd(self.currentWorkDir)
        cwd = os.getcwd()
        i = 0
        while i < len(cwd) and i < len(self.root) and cwd[i] == self.root[i]:
            i += 1
        retVal = cwd[i:]
        if retVal == "":
            retVal = ":\\"
        else:
            retVal = ":"+retVal
        handler.revertSuperTmpCwd()
        return retVal.encode("ascii")

    def cwd(self, path: str):
        handler = SuperTmpHandler().superTmpCwd(self.currentWorkDir)
        if path == "":
            return
        try:
            os.chdir(path)
            if len(os.getcwd()) < len(self.root):
                os.chdir(self.root)
            self.currentWorkDir = os.getcwd()
            return self.gwd()
        finally:
            handler.revertSuperTmpCwd()

    def lst(self):
        handler = SuperTmpHandler().superTmpCwd(self.currentWorkDir)
        files = os.listdir()
        for i in range(len(files)):
            files[i] = files[i]+"\n"
        fileString = ""
        for el in files:
            fileString += el
        handler.revertSuperTmpCwd()
        return fileString.encode("ascii")

    def upl(self, file: bytes, filename: str, path: str = ""):
        handler = SuperTmpHandler().superTmpCwd(self.currentWorkDir)
        self.__tmpCwd(path)
        try:
            with open(filename, "wb") as handle:
                handle.write(file)
        finally:
            handler.revertSuperTmpCwd()

    def dnl(self, filename: str, path: str = ""):
        handler = SuperTmpHandler().superTmpCwd(self.currentWorkDir)
        self.__tmpCwd(path)
        try:
            with open(filename, "rb") as handle:
                file = handle.read()
            return file
        finally:
            handler.revertSuperTmpCwd()

    def rmf(self, filename: str, path: str = ""):
        handler = SuperTmpHandler().superTmpCwd(self.currentWorkDir)
        self.__tmpCwd(path)
        try:
            os.remove(filename)
        finally:
            handler.revertSuperTmpCwd()


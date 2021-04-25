import os

class CmdExecutor:
    def __init__(self, rootDir: str):
        self.root = rootDir
        os.chdir(rootDir)
        self.root = os.getcwd()

    def __tmpCwd(self, path):
        self.cwd = os.getcwd()
        if path == "":
            return
        os.chdir(path)
        if len(os.getcwd()) < len(self.root):
            os.chdir(self.root)

    def __revertTmpCwd(self):
        os.chdir(self.cwd)
        self.cwd = None

    def mkd(self, dir:str, path:str = ""):
        self.__tmpCwd(path)
        try:
            os.mkdir(dir)
        finally:
            self.__revertTmpCwd()

    def rmd(self, dir:str, path:str):
        self.__tmpCwd(path)
        try:
            os.rmdir(dir)
        finally:
            self.__revertTmpCwd()

    def gwd(self):
        cwd = os.getcwd()
        i = 0
        while i < len(cwd) and i < len(self.root) and cwd[i] == self.root[i]:
            i += 1
        retVal = cwd[i:]
        if retVal == "":
            retVal = ":\\"
        else:
            retVal = ":"+retVal
        return retVal.encode("ascii")

    def cwd(self, path: str):
        os.chdir(path)
        if len(os.getcwd()) < len(self.root):
            os.chdir(self.root)
        return self.gwd()

    def lst(self):
        files = os.listdir()
        for i in range(len(files)):
            files[i] = files[i]+"\n"
        fileString = ""
        for el in files:
            fileString += el
        return fileString.encode("ascii")

    def upl(self, file: bytes, filename: str, path: str):
        self.__tmpCwd(path)
        try:
            with open(filename, "wb") as handle:
                handle.write(file)
        finally:
            self.__revertTmpCwd()
    def dnl(self, filename: str, path: str):
        self.__tmpCwd(path)
        try:
            with open(filename, "rb") as handle:
                file = handle.read()
        finally:
            self.__revertTmpCwd()
        return file

    def rmf(self, filename: str, path: str):
        self.__tmpCwd(path)
        try:
            os.remove(filename)
        finally:
            self.__revertTmpCwd()


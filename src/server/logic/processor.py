import os
import shutil
from utils.validation.validator import Validator


class Processor:
    def __init__(self, user_home_dir):
        self.CWD = user_home_dir
        self.validator = Validator()

    @staticmethod
    def __get_param_values(params):
        paramdict = dict()
        for p in params:
            parts = p.split('=')
            paramdict[parts[0].replace('-', '')] = parts[1]
        return paramdict

    def process(self, command):
        if not self.validator.validate(command):
            return

        parts = command.split(' ')
        cmd = parts[0]

        if cmd == "mkd":
            paramdict = self.__get_param_values(parts[1:])
            self.__mkd(paramdict['dir'], paramdict['path'] if 'path' in paramdict else None)
        elif cmd == "rmd":
            paramdict = self.__get_param_values(parts[1:])
            self.rmd(paramdict['dir'], paramdict['path'] if 'path' in paramdict else None)
        elif cmd == "gwd":
            self.__gwd()
        elif cmd == "cwd":
            paramdict = self.__get_param_values(parts[1:])
            self.__cwd(paramdict['path'])
        elif cmd == "lst":
            return self.__lst()
        elif cmd == "upl":
            paramdict = self.__get_param_values(parts[1:])
            self.__upl(paramdict['spath'], paramdict['ddir'] if 'ddir' in paramdict else None)
        elif cmd == "dnl":
            paramdict = self.__get_param_values(parts[1:])
            self.dnl(paramdict['spath'], paramdict['ddir'] if 'ddir' in paramdict else None)
        elif cmd == "rmf":
            paramdict = self.__get_param_values(parts[1:])
            self.__rmf(paramdict['path'])

    def __mkd(self, directory, path):
        #TODO: check if given path is valid and is inside of users directory
        os.mkdir(os.path.join(self.CWD, path, directory))

    def __rmd(self, directory, path):
        #TODO: check if given path is valid and is inside of users directory
        shutil.rmtree(os.path.join(self.CWD, path, directory))

    def __gwd(self):
        return self.CWD

    def __cwd(self, path):
        #TODO: check if given path is valid and is inside of users directory
        pass

    def __lst(self):
        return os.listdir(self.CWD)

    def __upl(self, source_path, destination_path):
        #TODO: check if given destination path is valid and is inside of users directory
        pass

    def __dnl(self, source_path, destination_path):
        #TODO: check if source path is valid and is inside of users directory
        pass

    def __rmf(self, path):
        #TODO: check if given path is valid and is inside of users directory
        os.remove(os.path.join(self.CWD, path))

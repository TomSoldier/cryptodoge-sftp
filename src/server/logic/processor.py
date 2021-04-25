from utils.validation.validator import Validator
from utils.commandExecution.cmdExecutor import CmdExecutor

class Processor:
    def __init__(self, user_home_dir):
        self.CWD = user_home_dir
        self.validator = Validator()
        self.executor = CmdExecutor(user_home_dir)

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
            self.executor.mkd(paramdict['dir'], paramdict['path'] if 'path' in paramdict else None)
        elif cmd == "rmd":
            paramdict = self.__get_param_values(parts[1:])
            self.executor.rmd(paramdict['dir'], paramdict['path'] if 'path' in paramdict else None)
        elif cmd == "gwd":
            self.executor.gwd()
        elif cmd == "cwd":
            paramdict = self.__get_param_values(parts[1:])
            self.executor.cwd(paramdict['path'])
        elif cmd == "lst":
            return self.executor.lst()
        elif cmd == "upl":
            paramdict = self.__get_param_values(parts[1:])
            self.executor.upl(paramdict['spath'], paramdict['ddir'] if 'ddir' in paramdict else None)
        elif cmd == "dnl":
            paramdict = self.__get_param_values(parts[1:])
            self.executor.dnl(paramdict['spath'], paramdict['ddir'] if 'ddir' in paramdict else None)
        elif cmd == "rmf":
            paramdict = self.__get_param_values(parts[1:])
            self.executor.rmf(paramdict['path'])

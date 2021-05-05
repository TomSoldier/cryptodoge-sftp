from typing import List

from utils.validation.validator import Validator
from utils.validation.validator import mandatory, optional, description, example, hasResult
from utils.commandExecution.cmdExecutor import CmdExecutor

class Processor:
    def __init__(self, user_home_dir):
        self.CWD = user_home_dir
        self.validator = Validator()
        self.validator.commands["upl"] = {
                mandatory: ["filename", "file"],
                optional: ["ddir"],
                description: "Used to upload files to the server.",
                example: "upl -spath=spath OR upl -spath=spath -ddir=ddir",
                hasResult: False
            }
        self.executor = CmdExecutor(user_home_dir)

    @staticmethod
    def __get_param_values(params: List[str]):
        paramdict = dict()
        for p in params:
            parts = p.split('=')
            param = parts[0].replace('-', '')
            paramdict[param] = parts[1]
            if param == "file":
                paramdict[param] += " "+" ".join(params[params.index(p)+1:])
                return paramdict
        return paramdict

    def process(self, command):
        if not self.validator.validate(command):
            return

        parts = command.split(' ')
        cmd = parts[0]

        if cmd == "mkd":
            paramdict = self.__get_param_values(parts[1:])
            self.executor.mkd(paramdict['dir'], paramdict['path'] if 'path' in paramdict else "")
            return None
        elif cmd == "rmd":
            paramdict = self.__get_param_values(parts[1:])
            self.executor.rmd(paramdict['dir'], paramdict['path'] if 'path' in paramdict else "")
            return None
        elif cmd == "gwd":
            return self.executor.gwd()
        elif cmd == "cwd":
            paramdict = self.__get_param_values(parts[1:])
            self.executor.cwd(paramdict['path'])
            return None
        elif cmd == "lst":
            return self.executor.lst()
        elif cmd == "upl":
            paramdict = self.__get_param_values(parts[1:])
            self.executor.upl(paramdict['file'].encode("ascii"),
                              paramdict['filename'],
                              paramdict['ddir'] if 'ddir' in paramdict else "")
            return None
        elif cmd == "dnl":
            paramdict = self.__get_param_values(parts[1:])
            return self.executor.dnl(paramdict['spath'])
        elif cmd == "rmf":
            paramdict = self.__get_param_values(parts[1:])
            self.executor.rmf(paramdict['path'])
            return None

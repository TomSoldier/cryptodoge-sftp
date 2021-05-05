from .error import InputError

optional = "optional"
mandatory = "mandatory"
description = "description"
example = "example"
hasResult = "hasResult"


class Validator:

    def __init__(self):
        self.commands = {
            "mkd": {
                mandatory: ["dir"],
                optional: ["path"],
                description: "Used to create a folder.",
                example: "mkd -dir=dir OR mkd -dir=dir -path=path",
                hasResult: False
            },
            "rmd": {
                mandatory: ["dir"],
                optional: ["path"],
                description: "Used to remove a folder and its content.",
                example: "rmd -dir=dir OR rmd -dir=dir -path=path",
                hasResult: False
            },
            "gwd": {
                mandatory: [],
                optional: [],
                description: "Used to get the current working directory name.",
                example: "gwd",
                hasResult: True
            },
            "cwd": {
                mandatory: ["path"],
                optional: [],
                description: "Used to change the current working directory.",
                example: "cwd -path=path",
                hasResult: False
            },
            "lst": {
                mandatory: [],
                optional: [],
                description: "Used to list all the files in the current working directory.",
                example: "lst",
                hasResult: True
            },
            "upl": {
                mandatory: ["spath"],
                optional: ["ddir"],
                description: "Used to upload files to the server.",
                example: "upl -spath=spath OR upl -spath=spath -ddir=ddir",
                hasResult: False
            },
            "dnl": {
                mandatory: ["spath"],
                optional: ["ddir"],
                description: "Used to download files from the server.",
                example: "dnl -spath=spath OR dnl -spath=spath -ddir=ddir",
                hasResult: True
            },
            "rmf": {
                mandatory: ["path"],
                optional: [],
                description: "Used to delete a file from the server.",
                example: "rmf -path=path",
                hasResult: False
            },
            "lgn": {
                mandatory: ["user", "pwd"],
                optional: [],
                description: "Used to login to the server.",
                example: "lgn -user=user -pwd=pwd",
                hasResult: True
            },
            "exit": {
                mandatory: [],
                optional: [],
                description: "Used to exit from the program.",
                example: "exit",
                hasResult: False
            },
        }

    def hasResult(self, cmd):
        return self.commands[cmd][hasResult]

    def __validate_params(self, cmd, params):
        p = []
        for param in params:
            p.append(param.split("=")[0].replace('-', ''))
            if param == "file":
                break

        if not all(i in p for i in self.commands[cmd][mandatory]):
            raise InputError("Not all mandatory parameters specified.")

        return True

    def __hasParams(self, cmd):
        return len(self.commands[cmd][mandatory]) > 0

    def validate(self, cmd):
        parts = cmd.split()
        c = parts[0].strip()
        if c in self.commands and self.__hasParams(c):
            return self.__validate_params(c, parts[1:])
        return c in self.commands

    def help(self):
        for cmd in self.commands:
            if cmd == "help":
                continue
            params = self.commands[cmd]
            print(cmd,
                  ' '.join(
                      list(('<' + i + '>' for i in params[mandatory]))),
                  ' '.join(
                      list(('[' + i + ']' for i in params[optional]))),
                  ' - ' + params[description],
                  ' Example: ' + params[example])

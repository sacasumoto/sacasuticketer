import cx_Freeze
import sys

base = None
##if sys.platform == 'win32':
##    base = "Win32GUI"

executables = [cx_Freeze.Executable("SacaSuTicketer.py",
                                    base=base,
                                    icon="ngcc.ico")]

cx_Freeze.setup(
    name = "SacaSuTicketer",
    options = {"build_exe":{"packages":["tkinter",
                                        "requests",
                                        "os",
                                        "time",
                                        "pytz",
                                        "datetime"],
                            "include_files":["StringExtractor.py",
                                             "TextEditor.py",
                                             "recent.txt",
                                             "cacert.pem",
                                             "ngcc.ico"]}},
    version = "0.02",
    description = "Smash.gg parser to get sets in a txt file for OBS",
    executables = executables
    )
    

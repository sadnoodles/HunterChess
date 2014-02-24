import sys

from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"
# scriptname=open('setup.txt','r').read().split('\\')[-1][:-1]
scriptname="hunter_chess.py"
setup(
        name = "HunterChess",
        version = "0.1",
        description = "A chess game.",
        executables = [Executable(scriptname, base = base)])


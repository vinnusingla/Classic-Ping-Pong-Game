import cx_Freeze
import os

os.environ['TCL_LIBRARY'] = "C:\\Users\Vinayak Singla\\Appdata\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\Vinayak Singla\\Appdata\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"

executables = [cx_Freeze.Executable("pong.py")]

cx_Freeze.setup(
    name="Pongy",
    version="1.0",
    options={"build_exe": {"packages":["pygame","sys","random","time"],"include_files":["data"]}},
    executables = executables
)
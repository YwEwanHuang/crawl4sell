import cx_Freeze
import sys
import matplotlib
from tkinter import *

root = Tk()
thelabel = Label(root, text = 'Srsly?')
thelabel.pack()
root.mainloop()



















# base = None

# if sys.platform == 'win32':
# 	base = 'Win32GUI'

# executables = [cx_Freeze.Executable('crawling.py', base=base, icon='clienticon.ico')]

# cx_Freeze.setup(
# 	name = 'SeaofBTC-Client',
# 	options = {"build_exe": {'packages':['matplotlib'], 'include_files':['clienticon.ico']}},
# 	version = '0.0.1',
# 	description = 'Nothing showed plz',
# 	executables = executables

# 	)
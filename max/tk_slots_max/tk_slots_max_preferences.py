import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Preferences(Init):
	def __init__(self, *args, **kwargs):
		super(Preferences, self).__init__(*args, **kwargs)




	def b000(self): #init tk_main
			print "init: tk_main"
			reload(tk_main)

	def b001(self): #color settings
		maxEval('colorPrefWnd;')

	def b002(self): #fbx presets
		maxEval('FBXUICallBack -1 editExportPresetInNewWindow fbx;')

	def b003(self): #obj presets
		maxEval('FBXUICallBack -1 editExportPresetInNewWindow obj;')

	def b004(self): #
		maxEval('')

	def b005(self): #
		maxEval('')

	def b006(self): #
		maxEval('')

	def b007(self): #
		maxEval('')

	def b008(self): #Hotkeys
		mel.eval("HotkeyPreferencesWindow;")

	def b009(self): #Plug-in manager
		maxEval('PluginManager;')

	def b010(self): #Settings/preferences
		mel.eval("PreferencesWindow;")



#print module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------
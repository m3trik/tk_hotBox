from __future__ import print_function
from tk_slots_max_init import *

import os.path



class Subdivision(Init):
	def __init__(self, *args, **kwargs):
		super(Subdivision, self).__init__(*args, **kwargs)

		#Set 3ds Max specific naming
		self.parentUi.gb000.setTitle('TurboSmooth')
		self.parentUi.lbl000.setText('Iterations:')
		self.parentUi.lbl001.setText('RenderIters:')
		self.parentUi.s000.setValue(0)
		self.parentUi.s001.setValue(0)


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.parentUi.pin

		if state=='setMenu':
			pin.add(QComboBox_, setObjectName='cmb000', setToolTip='3dsMax Subdivision Modifiers')

			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb000

		list_ = ['TurboSmooth','TurboSmooth Pro','OpenSubDiv','Subdivide','Subdivide (WSM)','MeshSmooth','Optimize','Pro Optimizer','Add Divisions']
		contents = cmb.addItems_(list_, '3dsMax Subdivision Modifiers')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==1: #TurboSmooth
				mod = rt.TurboSmooth()
				mod.iterations = 0
				mod.renderIterations = 1
				mod.useRenderIterations = True
				mod.explicitNormals = True
				mod.sepByMats = True
				rt.modpanel.addModToSelection(mod)

			if index==2: #TurboSmooth Pro
				mod = TurboSmooth_Pro()
				mod.iterations = 0
				mod.renderIterations = 1
				mod.useRenderIterations = True
				mod.explicitNormals = True
				mod.visualizeCreases = True
				mod.smmoothCorners = False
				mod.creaseSmoothingGroups = True
				mod.creaseMaterials = True
				rt.modpanel.addModToSelection(mod)

			if index==3: #OpenSubDiv
				mod = OpenSubdiv()
				mod.iterations = 0
				mod.renderIterations = 1
				mod.useRenderIterations = True
				rt.modpanel.addModToSelection(mod)

			if index==4: #Subdivide
				mod = subdivide()
				mod.size = 0.075
				rt.modpanel.addModToSelection(mod)

			if index==5: #Subdivide (WSM)
				mod = subdivideSpacewarpModifier()
				mod.size = 40
				rt.modpanel.addModToSelection(mod)

			if index==6: #MeshSmooth
				mod = meshsmooth()
				mod.iterations = 0
				mod.renderIterations = 1
				mod.useRenderIterations = True
				mod.useRenderSmoothness = True
				rt.modpanel.addModToSelection(mod)

			if index==7: #Optimize
				mod = optimize()
				rt.modpanel.addModToSelection(mod)

			if index==8: #Pro optimizer
				mod = ProOptimizer()
				rt.modpanel.addModToSelection(mod)

			if index==contents.index('Add Divisions'):
				maxEval('''
				Try 
				(
					local A = modPanel.getCurrentObject()
					A.popupDialog #Tessellate
				)
				Catch ()
				''')
			cmb.setCurrentIndex(0)


	def s000(self):
		'''
		Division Level
		'''
		value = self.parentUi.s000.getValue()

		geometry = rt.selection

		for obj in geometry:
			try:
				obj.modifiers['TurboSmooth'].iterations = value
			except: pass


	def s001(self):
		'''
		Tesselation Level
		'''
		value = self.parentUi.s001.getValue()

		geometry = rt.selection

		for obj in geometry:
			try:
				obj.modifiers['TurboSmooth'].renderIterations = value
			except: pass


	@Slots.message
	def b000(self):
		'''
		Toggle Subdiv Proxy Display
		'''
		state = self.cycle([1,1,0], 'subdivProxy')
		try:
			mel.eval("smoothingDisplayToggle "+str(state))
		except:
			traceback.print_exc()
			return 'Error: Nothing Selected.'


	def b001(self):
		'''
		Subdiv Proxy
		'''
		global polySmoothBaseMesh
		polySmoothBaseMesh=[]
		#disable creating seperate layers for subdiv proxy
		pm.optionVar (intValue=["polySmoothLoInLayer",0])
		pm.optionVar (intValue=["polySmoothHiInLayer",0])
		#query smooth proxy state.
		sel = mel.eval("polyCheckSelection \"polySmoothProxy\" \"o\" 0")
		
		if len(sel)==0 and len(polySmoothBaseMesh)==0:
			print(" Warning: Nothing selected. ")
			return
		if len(sel)!=0:
			del polySmoothBaseMesh[:]
			for object_ in sel:
				polySmoothBaseMesh.append(object_)
		elif len(polySmoothBaseMesh) != 0:
			sel = polySmoothBaseMesh

		transform = pm.listRelatives (sel[0], fullPath=1, parent=1)
		shape = pm.listRelatives (transform[0], pa=1, shapes=1)

		#check shape for an existing output to a smoothProxy
		attachedSmoothProxies = pm.listConnections (shape[0], type="polySmoothProxy", s=0, d=1)
		if len(attachedSmoothProxies) == 0: #subdiv on
			self.toggleWidgets(self.parentUi, self.childUi, setEnabled='b000', setChecked='b009')
		else:
			self.toggleWidgets(self.parentUi, self.childUi, setDisabled='b000', setChecked_False='b009')
			mel.eval("smoothingDisplayToggle 0;")

		#toggle performSmoothProxy
		mel.eval("performSmoothProxy 0;") #toggle SubDiv Proxy;


	def b004(self):
		'''
		Poly Reduce
		'''
		mel.eval("polyReduce -version 1 -keepCreaseEdgeWeight 1;")


	def b005(self):
		'''
		Reduce
		'''
		mel.eval("ReducePolygon;")


	def b008(self):
		'''
		Add Divisions - Subdivide Mesh
		'''
		maxEval('macros.run \"Modifiers\" \"Tessellate\"')


	def b009(self):
		'''
		Smooth
		'''
		maxEval('macros.run \"Modifiers\" \"Smooth\"')


	def b010(self):
		'''
		
		'''
		pass


	def b011(self):
		'''
		Convert Smooth Preview
		'''
		#convert smooth mesh preview to polygons
		geometry = rt.selection

		if not len(geometry):
			geometry = rt.geometry

		for obj in geometry:
			try:
				renderIters = obj.modifiers['TurboSmooth'].renderIterations
				obj.modifiers['TurboSmooth'].iterations = renderIters

				modifiers = [mod.name for mod in obj.modifiers]
				if modifiers:
					index = modifiers.index('TurboSmooth') +1
				rt.maxOps.CollapseNodeTo(obj, index, False)
			except: pass







#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------